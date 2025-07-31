from colorama import Fore, init
init(autoreset=True)

print(Fore.GREEN + r"""
       ______    ____  _  _  ____  _  _   __   __ _    ______    
      (______)  (  _ \( \/ )(_  _)/ )( \ /  \ (  ( \  (______)   
   ___  _____    ) __/ )  /   )(  ) __ ((  O )/    /   _____  ___    
  (___)(_____)  (__)  (__/   (__) \_)(_/ \__/ \_)__)  (_____)(___)   
  ____   __  ____  ____    ____   ___   __   __ _  __ _  ____  ____ 
 (  _ \ /  \(  _ \(_  _)  / ___) / __) / _\ (  ( \(  ( \(  __)(  _ \
  ) __/(  O ))   /  )(    \___ \( (__ /    \/    //    / ) _)  )   /
 (__)   \__/(__\_) (__)   (____/ \___)\_/\_/\_)__)\_)__)(____)(__\_)    
      """)

import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

print_lock = Lock()

target = input("Enter IP or domain to scan: ")
ports = range(1,1025)

print(Fore.CYAN + "="*69)
print(f"Scanning target: {target}")
print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(Fore.CYAN + "="*69)

open_ports = []

def scan_port(port, print_lock):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                banner = sock.recv(1024).decode().strip()
            except:
                banner = "Not available"
            with print_lock:
                print(Fore.GREEN + f"[+]Port {port:<3} is OPEN | Banner: {banner}")
                open_ports.append(port)
        sock.close()
    except Exception as e:
        pass # Ignore errors to keep scanning

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(lambda port: scan_port(port, print_lock), ports)

print(Fore.CYAN + "="*69)
print(f"Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total open ports found: {len(open_ports)}")
if open_ports:
    print(Fore.GREEN + f"Open ports: {', '.join(map(str, open_ports))}")

print(Fore.CYAN + "="*69)