# TeleParser

This is my project for parsing Telegram channels and chats and processing received data

### Requirements
1. Python `3.12.0` (CPython)
2. MongoDB
3. Your Telegram API token, learn more <a href='https://core.telegram.org/api#getting-started'>here</a>

### Get started
1. Run <i>git clone</i>: 
   ```
   git clone https://github.com/artmih24/TeleParser.git
   ```
2. Go to project directory: 
   ```
   cd TeleParser
   ```
3. Create Python venv:
   - on Windows: 
     ```
     python -m venv .
     ```
   - on Linux/macOS/other Unix-like OS: 
     ```
     python3 -m venv .
     ```
4. Select project Python venv:
   - on Windows: 
     ```
     .\Scripts\activate
     ```
   - on Linux/macOS/other Unix-like OS: 
     ```
     source bin/activate
     ```
5. Install dependencies:
   - on Windows: 
     ```
     pip install -r .\requirements.txt
     ```
   - on Linux/macOS/other Unix-like OS: 
     ```
     pip3 install -r ./requirements.txt
     ```
6. Get your own Telegram API token <a href='https://core.telegram.org/api#getting-started'>here</a>

### How to use
0. Make sure that:
   - You have received Your Telegram API token
   - And You have replaced contents in `config.ini` file by yor Telegram API token
1. Launch this script:
   - on Windows: `python .\TeleParser.py`
   - on Linux/macOS/other Unix-like OS: `python3 ./TeleParser.py`
2. Login in Telegram if You weren't logged in (trust me, this script doesn't steal your Telegram token, login and password)
3. Enter channel or chat name (written after '@' or `t.me/`/`https://t.me/`) and press Enter
4. Wait until this script will parse and process al data and press Enter
5. You can view all `.json` and `.csv` files with received data and view all data in MongoDB database

### WARNING
Don't give Your Telegram API token to anyone