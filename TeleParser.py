# импорт библиотек
import os
import sys
import json
import csv
import configparser
import pandas as pd
if sys.version_info.minor >= 12:
    import pymorphy3
else:
    import pymorphy2
import nltk
from nltk.stem import WordNetLemmatizer
from math import *
from pymongo import MongoClient

from telethon.sync import TelegramClient
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/2)

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

# создание объекта клиента Telegram
client = TelegramClient(username, api_id, api_hash)

client.start()

class DateTimeEncoder(json.JSONEncoder):
    '''Класс для сериализации записи дат в JSON'''
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)

async def dump_all_participants(channel, short_url_, datetime_):
    """Записывает json-файл с информацией о всех участниках канала/чата"""
    offset_user = 0    # номер участника, с которого начинается считывание
    limit_user = 100   # максимальное число записей, передаваемых за один раз

    all_participants = []   # список всех участников канала
    filter_user = ChannelParticipantsSearch('')

    while True:
        participants = await client(GetParticipantsRequest(channel,
                                                           filter_user, offset_user, limit_user, hash=0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset_user += len(participants.users)
        print(f'{str(datetime.now())} | Получено записей: {len(all_participants)}', end='\r')

    with open(f'{short_url_}_participants_{datetime_}.json', 'w', encoding='utf8') as outfile:
        json.dump(all_participants, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def dump_all_messages(channel, short_url_, datetime_):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0    # номер записи, с которой начинается считывание
    limit_msg = 100   # максимальное число записей, передаваемых за один раз

    all_messages = []   # список всех сообщений
    total_messages = 0
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        print(f'{str(datetime.now())} | Получено записей: {len(all_messages)}', end='\r')
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open(f'{short_url_}_messages_{datetime_}.json', 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main():
    channel = await client.get_entity(url)
    await dump_all_participants(channel, channel_string, datetime_string)
    await dump_all_messages(channel, channel_string, datetime_string)

# загрузка необходимых компонентов
nltk.download('wordnet')
nltk.download('punkt')

# очистка консоли от лишней информации
cls = lambda: os.system('cls')
cls()

# парсинг чата или канала в Telegram и сохранение в JSON-файл
if len(sys.argv) == 1:
    url = 't.me/' + sys.argv[1]
else:
    url = 't.me/' + input("Введите ссылку на канал или чат: @")
channel_string = url.split('/')[-1]
print(f'{str(datetime.now())} | Парсинг начат')
datetime_string = str(datetime.now()).replace("-", "").replace(" ", "T").replace(":", "").split(".")[0]
with client:
    client.loop.run_until_complete(main())
print(f'{str(datetime.now())} | Парсинг закончен!')

# копирование содержимого JSON-файла в CSV-файл
print(f'{str(datetime.now())} | Начато копирование содержимого JSON-файла в CSV-файл')
json_file = pd.read_json(f'{channel_string}_messages_{datetime_string}.json')
json_file.to_csv(f'{channel_string}_messages_{datetime_string}.csv', index=None, encoding='utf8')
print(f'{str(datetime.now())} | Копирование содержимого JSON-файла в CSV-файл завершено!')

# импорт содержимого JSON-файла в базу данных
# mongoimport_path = '"C:\\Program Files\\MongoDB\\Server\\4.4\\bin\\mongodb-database-tools-windows-x86_64-100.3.1\\bin\\mongoimport.exe"'
# os.popen(f'{mongoimport_path} -d KM5_BigData -c {channel_string}_{datetime_string} --file {channel_string}_messages_{datetime_string}.json --jsonArray')
print(f'{str(datetime.now())} | Начат импорт содержимого JSON-файла в базу данных')
db_original = MongoClient('mongodb://127.0.0.1:27017')['KM5_BigData'][f'{channel_string}_{datetime_string}']
with open(f'{channel_string}_messages_{datetime_string}.json', 'r', encoding='utf8') as json_file:
    json_file_data = json.load(json_file)
db_original.insert_many(json_file_data)
print(f'{str(datetime.now())} | Импорт содержимого JSON-файла в базу данных завершен!')

# удаление лишних столбцов в базе данных
print(f'{str(datetime.now())} | Начато удаление лишних столбцов в базе данных')
db_original.update_many({}, {'$unset': {'_': '',
                                         'out': '',
                                         'mentioned': '',
                                         'media_unread': '',
                                         'silent': '',
                                         'post': '',
                                         'from_scheduled': '',
                                         'legacy': '',
                                         'edit_hide': '',
                                         'pinned': '',
                                         'fwd_from': '',
                                         'via_bot_id': '',
                                         'reply_to': '',
                                         'reply_markup': '',
                                         'replies': '',
                                         'edit_date': '',
                                         'post_author': '',
                                         'grouped_id': '',
                                         'restriction_reason': '',
                                         'ttl_period': '',
                                         'action': ''}})
print(f'{str(datetime.now())} | Удаление лишних столбцов в базе данных завершено!')

# леммирование текста
print(f'{str(datetime.now())} | Леммирование текста')
if sys.version_info.minor >= 12:
    morph = pymorphy3.MorphAnalyzer()
else:
    morph = pymorphy2.MorphAnalyzer()
data = []
with open(f'{channel_string}_messages_{datetime_string}.csv', 'r', encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)
text_to_lemm = []
for i in range(len(data)):
    text_to_lemm.append(data[i]['message'])
lemm_text_list = []
for i in range(len(text_to_lemm)):
    word_list = nltk.word_tokenize(text_to_lemm[i])
    lemm_text = ' '.join([morph.parse(w)[0].normal_form for w in word_list])
    lemm_text_list.append(lemm_text)
for i in range(len(lemm_text_list)):
    data[i]['message'] = lemm_text_list[i]
print(f'{str(datetime.now())} | Леммирование текста завершено!')

# запись леммированного текста в CSV-файл
print(f'{str(datetime.now())} | Запись леммированного текста в CSV-файл')
fieldnames = [t for i, t in enumerate(data[0])]
with open(f'{channel_string}_messages_{datetime_string}_lemm.csv', 'w', encoding='utf-8-sig', newline='') as csvlemmfile:
    writer = csv.DictWriter(csvlemmfile, delimiter=';', fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
print(f'{str(datetime.now())} | CSV-файл с леммированным текстом создан!')


# копирование коллекции для А/В-тестирования
def CopyFromColl1ToColl2(database1, collection1, database2, collection2):
    db1 = MongoClient('mongodb://127.0.0.1:27017')[database1][collection1]
    db2 = MongoClient('mongodb://127.0.0.1:27017')[database2][collection2]
    # here you can put the filters you like.
    for a in db1.find():
        try:
            db2.insert_one(a)
            print(f'{str(datetime.now())} | Запись успешно скопирована', end='\r')
        except:
            print(f'{str(datetime.now())} | Копирование не удалось')


print(f'{str(datetime.now())} | Копирование коллекции для А/В-тестирования')
CopyFromColl1ToColl2('KM5_BigData', f'{channel_string}_{datetime_string}', 'KM5_BigData',
                    f'{channel_string}_{datetime_string}_AB')
print(f'{str(datetime.now())} | Копирование коллекции для А/В-тестирования завершено!')

# подготовка коллекции к A/B-тестированию
print(f'{str(datetime.now())} | Подготовка коллекции к A/B-тестированию')
db_for_AB = MongoClient('mongodb://127.0.0.1:27017')['KM5_BigData'][f'{channel_string}_{datetime_string}_AB']
db_for_AB_len = db_for_AB.estimated_document_count()
db_for_AB_len_A = ceil(db_for_AB_len * 0.75)
db_for_AB_len_B = db_for_AB_len - db_for_AB_len_A
db_for_AB.update_many({}, {'$set': {'flag': 'A'}})
db_for_AB.update_many({'$expr': {'$eq': [1, {'$mod': ['$id', 4]}]}}, {'$set': {'flag': 'B'}})
db_for_AB_docs_A = db_for_AB.count_documents({'flag': 'A'})
db_for_AB_docs_B = db_for_AB.count_documents({'flag': 'B'})
#print(ceil(db_for_AB_len * 0.75), '!=', db_for_AB_docs_A)
#print(db_for_AB_len - db_for_AB_len_A, '!=', db_for_AB_docs_B)
while (db_for_AB_docs_B < db_for_AB_len_B):
    db_for_AB.update_one({'flag': 'A'}, {'$set': {'flag': 'B'}})
    db_for_AB_docs_A = db_for_AB.count_documents({'flag': 'A'})
    db_for_AB_docs_B = db_for_AB.count_documents({'flag': 'B'})
while (db_for_AB_docs_A < db_for_AB_len_A):
    db_for_AB.update_one({'flag': 'B'}, {'$set': {'flag': 'A'}})
    db_for_AB_docs_A = db_for_AB.count_documents({'flag': 'A'})
    db_for_AB_docs_B = db_for_AB.count_documents({'flag': 'B'})
#print(ceil(db_for_AB_len * 0.75), '!=', db_for_AB_docs_A)
#print(db_for_AB_len - db_for_AB_len_A, '!=', db_for_AB_docs_B)
print(f'{str(datetime.now())} | Подготовка коллекции к A/B-тестированию завершена!')

cursor = db_for_AB.find({})
df = pd.DataFrame(list(cursor))
df.to_csv(f'{channel_string}_messages_{datetime_string}_AB.csv', index=False, encoding='utf-8-sig')

csvfile = open(f'{channel_string}_messages_{datetime_string}_AB.csv', 'r', encoding='utf-8-sig')
jsonfile = open(f'{channel_string}_messages_{datetime_string}_AB.json', 'w', encoding='utf8')

reader = csv.DictReader(csvfile, delimiter=';')
jsonfile.write('[')
for row in reader:
    json.dump(row, jsonfile, ensure_ascii=False)
    jsonfile.write(',')
jsonfile.write(']')

input('Для закрытия нажмите Enter')