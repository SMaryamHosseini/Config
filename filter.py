import requests
import socket
import ssl
import base64
from urllib.parse import urlparse

subs = open("subs.txt","r",encoding="utf-8").read().splitlines()

nodes = []

# -------------------------
# 1. extract nodes
# -------------------------
for url in subs:
    try:
        r = requests.get(url, timeout=15)
        text = r.text.strip()

        try:
            decoded = base64.b64decode(text + "==").decode(errors="ignore")
        except:
            decoded = text

        for line in decoded.splitlines():
            if "vless://" in line or "vmess://" in line or "trojan://" in line:
                nodes.append(line)

    except:
        pass

print("TOTAL NODES:", len(nodes))


# -------------------------
# 2. TLS test (REAL CHECK)
# -------------------------
def test_node(host, port):
    try:
        ctx = ssl.create_default_context()
        sock = socket.create_connection((host, port), timeout=3)
        ssock = ctx.wrap_socket(sock, server_hostname=host)

        ssock.settimeout(3)
        ssock.close()

        return True
    except:
        return False


# -------------------------
# 3. parse + test
# -------------------------
good = []

for i, n in enumerate(nodes):
    try:
        if "@" not in n:
            continue

        hp = n.split("@")[1]
        host = hp.split(":")[0]
        port = int(hp.split(":")[1].split("?")[0])

        if test_node(host, port):
            good.append(n)

        print(i, "tested")

    except:
        pass


# -------------------------
# 4. output
# -------------------------
open("mci_best.txt","w",encoding="utf-8").write("\n".join(good))

print("GOOD:", len(good))
