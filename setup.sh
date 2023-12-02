#!/usr/bin/env bash

python3 -m venv .
source ./bin/activate
sed -i.bak 's/\r$//g' requirements.txt
sed -i.bak 's/\r$//g' TeleParser.py
pip3 install -r ./requirements.txt
