import requests
import re
import ipaddress


SUB_URL = "https://raw.githubusercontent.com/barry-far/V2ray-config/main/All_Configs_base64_Sub.txt"

# CDN IP list (همونایی که دادی)
CDN_IPS = [
"23.211.53.248","2.16.53.35","184.86.2.78","104.66.72.213","23.58.201.211",
"2.22.0.41","2.21.200.81","104.66.76.103","95.100.183.211","92.123.122.13",
"23.207.120.215","104.66.125.77","2.16.23.144","23.12.35.88","172.225.189.99",
"23.32.238.115","184.85.248.67","23.211.175.176","104.80.212.143","2.20.176.177",
"23.210.232.36","23.208.87.74","23.42.164.57","23.54.15.99","184.24.24.49",
"23.209.239.170","2.22.2.3","23.222.49.45","23.61.234.146","23.197.148.242"
]

def extract_ip(cfg): try: m = re.search(r'@([\d\.]+):', cfg) if m: return m.group(1) except: pass return None for sub in SUB_LINKS: try: text = requests.get(sub, timeout=20).text for line in text.splitlines(): if not line.startswith("vless://"): continue ip = extract_ip(line) if not ip: continue for cdn in CDN_IPS: if ip.startswith(cdn): good.append(line) break except Exception as e: print("SUB ERROR:", e) good = list(set(good)) with open("mci_best.txt", "w", encoding="utf-8") as f: for x in good: f.write(x + "\n") with open("sub.txt", "w", encoding="utf-8") as f: for x in good: f.write(x + "\n") print("FOUND:", len(good)) print("DONE")
