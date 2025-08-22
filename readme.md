# TeleParser

This is my project for parsing Telegram channels and chats and processing received data

## ❗️ IMPORTANT
Telegram has been updated API<br>
**DO NOT** use this project until I will update it!<br>
If You will try to use this project, **you can loose Your Telegram account!**

### Requirements
1. Python `3.12.0` or earlier (CPython)
2. MongoDB
3. Your Telegram API token, learn more <a href='https://core.telegram.org/api#getting-started'>here</a>

### Get started
1. Run <i>git clone</i>: 
   ```bat
   git clone https://github.com/artmih24/TeleParser.git
   ```
2. Go to project directory: 
   ```bash
   cd TeleParser
   ```
3. Create Python venv:
   - on Windows: 
     ```bat
     python -m venv .
     ```
   - on Linux/macOS/other Unix-like OS: 
     ```bash
     python3 -m venv .
     ```
4. Select project Python venv:
   - on Windows: 
     ```bat
     .\Scripts\activate
     ```
   - on Linux/macOS/other Unix-like OS: 
     ```bash
     source ./bin/activate
     ```
5. Install dependencies:
   - on Windows: 
     ```bat
     pip install -r .\requirements.txt
     ```
   - on Linux/macOS/other Unix-like OS: 
     ```bash
     pip3 install -r ./requirements.txt
     ```
6. You can use setup scripts:
   - on Windows: 
     ```bat
     .\setup.cmd
     ```
     or
     ```bat
     .\setup.bat
     ```
     or
     ```pwsh
     .\setup.ps1
     ```
   - on Linux/macOS/other Unix-like OS: 
     ```bash
     ./setup.sh
     ```
7. Get your own Telegram API token <a href='https://core.telegram.org/api#getting-started'>here</a>

### How to use
0. Make sure that:
   - You have received Your Telegram API token
   - And You have replaced contents in `config.ini` file by your Telegram API token
1. Launch this script:
   - on Windows: 
     ```bat
     python .\TeleParser.py
     ```
   - on Linux/macOS/other Unix-like OS: 
     ```bash
     python3 ./TeleParser.py
     ```
   - You can write channel or chat name (written after '@' or `t.me/`/`https://t.me/`) as command-line argument
2. Login in Telegram if You weren't logged in (trust me, this script doesn't steal your Telegram token, login and password)
3. If You haven't written channel or chat name as command-line argument, enter channel or chat name (written after '@' or `t.me/`/`https://t.me/`) and press Enter key
4. Wait until this script will parse and process all data (it can take a lot of time, please be patient and wait) and press Enter key
5. You can view all `.json` and `.csv` files with received data and view all data in MongoDB database

### WARNING
Don't give Your Telegram API token to anyone!


