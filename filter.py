import requests
import base64
import re
import socket
from concurrent.futures import ThreadPoolExecutor

SUB_LINKS = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/All_Configs_base64_Sub.txt"
]

# timeout خیلی مهمه (برای MCI باید کم باشه)
TIMEOUT = 1.5

PORT = 443

good = []

def decode_sub(text):
    try:
        return base64.b64decode(text).decode("utf-8", errors="ignore")
    except:
        return text

def extract_ip(vless_line):
    m = re.search(r'@([\d\.]+):', vless_line)
    return m.group(1) if m else None

def tcp_check(ip):
    try:
        s = socket.socket()
        s.settimeout(TIMEOUT)
        s.connect((ip, PORT))
        s.close()
        return True
    except:
        return False

def process_line(line):
    if "vless://" not in line:
        return None

    ip = extract_ip(line)
    if not ip:
        return None

    if tcp_check(ip):
        return line

    return None

for sub in SUB_LINKS:
    print("FETCH:", sub)

    raw = requests.get(sub, timeout=20).text
    decoded = decode_sub(raw)

    lines = decoded.splitlines()
    print("TOTAL:", len(lines))

    with ThreadPoolExecutor(max_workers=50) as ex:
        results = list(ex.map(process_line, lines))

    good = [x for x in results if x]

good = list(set(good))

print("FOUND:", len(good))

with open("mci_best.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(good))

with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(good))

print("DONE")
