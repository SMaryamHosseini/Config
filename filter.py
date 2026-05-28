import socket
import ssl
import time
import requests
import base64
import statistics
import random

MAX_NODES = 100
TIMEOUT = 2.2

subs = open("subs.txt","r",encoding="utf-8").read().splitlines()

nodes = []

# -----------------------
# 1. LOAD SUBS
# -----------------------
for url in subs:
    try:
        r = requests.get(url, timeout=10)
        text = r.text.strip()

        try:
            decoded = base64.b64decode(text + "==").decode(errors="ignore")
        except:
            decoded = text

        for line in decoded.splitlines():
            if "vless://" in line or "vmess://" in line or "trojan://" in line:
                nodes.append(line)

    except:
        continue

nodes = nodes[:MAX_NODES]

print("TOTAL NODES:", len(nodes))


# -----------------------
# 2. PARSE
# -----------------------
parsed = []

for n in nodes:
    try:
        hp = n.split("@")[1]
        host = hp.split(":")[0]
        port = int(hp.split(":")[1].split("?")[0])
        parsed.append((host, port, n))
    except:
        continue


# -----------------------
# 3. ISP-LIKE BEHAVIOR MODEL
# -----------------------
def simulate_isp_noise(lat):
    """
    Simulates mobile ISP behavior:
    - MCI has jitter + occasional spikes
    """
    noise = random.uniform(0, lat * 0.3)
    spike = random.choice([0, 0, 0, lat * 0.8])  # rare spike
    return lat + noise + spike


def test_node(host, port):
    samples = []

    for _ in range(3):
        try:
            start = time.time()

            sock = socket.create_connection((host, port), timeout=TIMEOUT)

            ctx = ssl.create_default_context()
            ssock = ctx.wrap_socket(sock, server_hostname=host)
            ssock.close()

            lat = time.time() - start

            # simulate ISP-like instability
            lat = simulate_isp_noise(lat)

            samples.append(lat)

        except:
            return None

    if len(samples) < 2:
        return None

    avg = statistics.mean(samples)
    jitter = statistics.pstdev(samples)

    # ISP-aware scoring model
    stability_score = 1 / (avg + jitter * 2)

    # penalize unstable routes (mobile-like behavior)
    penalty = jitter * 1.5

    final_score = stability_score - penalty

    return avg, jitter, final_score


# -----------------------
# 4. RUN TESTS
# -----------------------
results = []

for i, (host, port, node) in enumerate(parsed):
    try:
        res = test_node(host, port)
        if res:
            avg, jitter, score = res
            results.append((score, avg, jitter, node))

        print(f"{i+1}/{len(parsed)}")

    except:
        continue


# -----------------------
# 5. SORTING
# -----------------------
results.sort(reverse=True)

best_mci_like = [x[3] for x in results if x[0] > 2.5]
stable_mci_like = [x[3] for x in results if 1.2 < x[0] <= 2.5]
weak = [x[3] for x in results if x[0] <= 1.2]


# -----------------------
# 6. OUTPUT
# -----------------------
open("mci_best.txt","w",encoding="utf-8").write("\n".join(best_mci_like))
open("mci_stable.txt","w",encoding="utf-8").write("\n".join(stable_mci_like))
open("mci_weak.txt","w",encoding="utf-8").write("\n".join(weak))

print("BEST MCI-LIKE:", len(best_mci_like))
print("STABLE:", len(stable_mci_like))
print("WEAK:", len(weak))
print("DONE")
