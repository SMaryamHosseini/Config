import requests
import re

SUB_URL = "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt"

# CDN IP list (همونایی که دادی)
CDN_IPS = [
"23.211.53.248","2.16.53.35","184.86.2.78","104.66.72.213","23.58.201.211",
"2.22.0.41","2.21.200.81","104.66.76.103","95.100.183.211","92.123.122.13",
"23.207.120.215","104.66.125.77","2.16.23.144","23.12.35.88","172.225.189.99",
"23.32.238.115","184.85.248.67","23.211.175.176","104.80.212.143","2.20.176.177",
"23.210.232.36","23.208.87.74","23.42.164.57","23.54.15.99","184.24.24.49",
"23.209.239.170","2.22.2.3","23.222.49.45","23.61.234.146","23.197.148.242"
]

def extract_ips(text):
    return re.findall(r"@?([\w\.-]+):\d+|(\d+\.\d+\.\d+\.\d+)", text)

def ping_check(ip):
    # ساده‌ترین تست (DNS resolve + socket simulation سبک)
    try:
        r = requests.get(f"http://{ip}", timeout=2)
        return True
    except:
        return False

def main():
    data = requests.get(SUB_URL).text

    nodes = extract_ips(data)
    good = []

    for n in nodes:
        ip = n[1] if n[1] else n[0]
        if not ip:
            continue

        if ip in CDN_IPS:
            good.append(ip)

    print("TOTAL:", len(nodes))
    print("GOOD:", len(good))

    # خیلی مهم: خروجی واقعی
    with open("mci_best.txt", "w") as f:
        for ip in good:
            f.write(ip + "\n")

    with open("sub.txt", "w") as f:
        for ip in good:
            f.write(f"vless://{ip}\n")

if __name__ == "__main__":
    main()
