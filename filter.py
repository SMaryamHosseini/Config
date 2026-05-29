import requests
import base64
import re
import socket
import ssl
import time
from concurrent.futures import ThreadPoolExecutor

SUB_LINKS = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/All_Configs_base64_Sub.txt"
]

TIMEOUT = 1.2
SNI = "www.cloudflare.com"

# ساده‌سازی ASN detection بدون API
ASN_HINTS = {
    "CLOUDFLARE": ["104.", "172.64", "23.227", "141.101"],
    "AWS": ["13.", "52.", "54.", "3."],
    "GOOGLE": ["142.250", "142.251", "172.217"],
    "MCI": ["185.", "78.", "5.", "151."]
}

mci = []
others = []

def decode(text):
    try:
        return base64.b64decode(text).decode("utf-8", errors="ignore")
    except:
        return text

def extract_ip(line):
    m = re.search(r'@([\d\.]+):', line)
    return m.group(1) if m else None

def guess_asn(ip):
    for k, prefixes in ASN_HINTS.items():
        for p in prefixes:
            if ip.startswith(p):
                return k
    return "UNKNOWN"


def tls_test(ip, port=443):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        s = socket.create_connection((ip, port), timeout=TIMEOUT)
        s.settimeout(TIMEOUT)

        start = time.time()

        ssl_sock = context.wrap_socket(s, server_hostname=SNI)
        ssl_sock.close()

        latency = time.time() - start
        return True, latency

    except:
        return False, None


def process(line):
    if "vless://" not in line:
        return None

    ip = extract_ip(line)
    if not ip:
        return None

    asn = guess_asn(ip)

    ok, lat = tls_test(ip)

    if not ok:
        return None

    score = lat

    # scoring logic
    if asn == "CLOUDFLARE" or asn == "AWS":
        return ("OTHER", line)

    if score < 0.3:
        return ("MCI", line)

    return ("OTHER", line)


for sub in SUB_LINKS:
    print("FETCH:", sub)

    raw = requests.get(sub, timeout=20).text
    decoded = decode(raw)

    lines = decoded.splitlines()
    print("TOTAL:", len(lines))

    results = []

    with ThreadPoolExecutor(max_workers=50) as ex:
        for r in ex.map(process, lines):
            if r:
                results.append(r)

for t, v in results:
    if t == "MCI":
        mci.append(v)
    else:
        others.append(v)

mci = list(set(mci))
others = list(set(others))

print("MCI:", len(mci))
print("OTHER:", len(others))

with open("mci_best.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(mci))

with open("sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(mci + others))

print("DONE")
