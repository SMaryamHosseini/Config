import requests
import socket
from urllib.parse import urlparse

SOURCE = "https://raw.githubusercontent.com/barry-far/V2ray-config/main/All_Configs_base64_Sub.txt"

ALLOWED = {
    150,104,23,172,162,141,198,192,190,156,66,82,37,45,
    1,173,2,95,184,92,199,167,151,146,140,185,157,34,205
}

def get_host(link):
    try:
        return urlparse(link).hostname
    except:
        return None

text = requests.get(SOURCE, timeout=60).text

result = []

for line in text.splitlines():
    line = line.strip()

    host = get_host(line)
    if not host:
        continue

    try:
        ip = socket.gethostbyname(host)

        if int(ip.split('.')[0]) in ALLOWED:
            result.append(line)

    except:
        pass

with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(result))
