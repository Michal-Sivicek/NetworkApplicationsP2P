Název: Sitova aplikace pomocí architektury P2P
Jméno a příjmení: Michal Siviček
Datum vypracování: 20.2.2023
Škola: Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30
Třída: C4c
Jedná se o školní projekt 


Spuštění programu:

Jako první věc si upravíme soubor config.ini 
		V něm si nastavíme port = 
				   network_address = 
				   server = 127.0.0.1

Jako další věc si otevřeme přikazový řádek a nasměřujeme se do složky pomocí přikazu cd v mém případě cd C:\Users\Admin\PycharmProjects\alfa4\src u vás složka kde je projekt uložený 

Poté program spustíme pomocí main.py

Jako další krok si spustíme putty kde zadáme port který jsem si zadali v config souboru a server 

Po spuštění putty můžeme zadávat přikazy například:

					TRANSLATELOCL"dog"
					TRANSLATESCAN"a"
					TRANSLATEPING"a"

Instalační skript pro debian je bud v prilozeny v slozce script a nebo zde:

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




