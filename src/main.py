import socket
import threading
import ipaddress
import configparser

# načíst konfigurační soubor
config = configparser.ConfigParser()
config.read('config.ini')

# slovník s překlady
translations = {
    "house": "dům",
    "tree": "strom",
    "car": "auto",
    "book": "kniha",
    "dog": "pes"
}

# adresa sítě a rozsah pro skenování z konfigurace
network_address = config['server']['network_address']

def handle_client(conn, addr):
    """Funkce pro zpracování připojení klienta
    :return: None
    :param conn: socket pro komunikaci s klientem
    :param addr: adresa klienta
    :type conn: socket.socket
    :type addr: tuple
    """
    while True:
        data = conn.recv(1024).decode()
        if data == "\r\n" or data == "\n" or data == "":
            continue
        if not data:
            break
        if data.startswith("TRANSLATELOCL"):
            word = data.split('"')[1]
            if word in translations:
                conn.sendall(f"TRANSLATEDSUC\"{translations[word]}\"".encode())
            else:
                conn.sendall("TRANSLATEDERR\"Slovo nebylo nalezeno\"".encode())
        elif data.startswith("TRANSLATESCAN"):
            word = data.split('"')[1]
            found = False
            for host in ipaddress.IPv4Network(network_address):
                if host != ipaddress.IPv4Address(addr[0]):
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        try:
                            s.connect((str(host), int(config['server']['port'])))
                            s.sendall(f'TRANSLATELOCL"{word}"'.encode())
                            response = s.recv(1024).decode()
                            if response.startswith("TRANSLATEDSUC"):
                                translation = response.split('"')[1]
                                conn.sendall(f"TRANSLATEDSUC\"{translation}\"".encode())
                                found = True
                                break
                        except (ConnectionRefusedError, socket.timeout):
                            pass
            if not found:
                conn.sendall("TRANSLATEDERR\"Slovo nebylo nalezeno\"".encode())
        elif data.startswith("TRANSLATEPING"):
            program_name = data.split('"')[1]
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                try:
                    s.connect((str(host), int(config['server']['port'])))
                    s.sendall(f'TRANSLATEPONG"{program_name}"'.encode())
                except (ConnectionRefusedError, socket.timeout):
                    pass
        elif data.startswith("TRANSLATEDERR"):
            # zpracování chybové odpovědi
            error_message = data.split('"')[1]
        else:
            conn.sendall("TRANSLATEDERR\"Neznámý příkaz\"".encode())
    #conn.close()

def start_server(port):
    """Funkce pro spuštění serveru
    :return: None
    :param port: port, na kterém bude server naslouchat
    :type port: int
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", port))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    # spustit server na pozadovanem portu z konfigurace
    port = int(config['server']['port'])
    start_server(port)

