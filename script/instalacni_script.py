#!/bin/bash

# instalace Pythonu 3
sudo apt-get update
sudo apt-get install python3

# instalace závislostí
sudo apt-get install python3-pip
sudo pip3 install configparser

# spuštění programu jako služby
sudo cp program.py /usr/local/bin/
sudo chmod +x /usr/local/bin/program.py

sudo cp program.service /etc/systemd/system/
sudo systemctl enable program.service
sudo systemctl start program.service
