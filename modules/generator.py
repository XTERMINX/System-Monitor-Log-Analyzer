import os
import random
from datetime import datetime, timedelta
import config
import modules.servers as servers

def gen_server(kollichestvo):
    os_varianty = ["Linux", "Windows", "Ubuntu", "CentOS"]
    sreda = ["production", "staging", "development", "test"]
    statusy = ["active", "active", "active", "inactive", "offline"]

    spisok = []
    for i in range(1, kollichestvo + 1):
        s = servers.Server(
            id=i,
            name=f"server-{i:02d}",
            os_name=random.choice(os_varianty),
            ip=f"192.168.1.{i}",
            environment=random.choice(sreda),
            cpu=random.choice([4, 8, 16, 32]),
            ram=random.choice([8, 16, 32, 64]),
            status=random.choice(statusy)
        )
        spisok.append(s)
    servers.save_server(spisok)
    return spisok

def gen_logs(kollichestvo_zapis, kollichestvo_failow=5):
    if not os.path.exists(config.logi):
        os.makedirs(config.logi)
    urovni = ["INFO", "INFO", "INFO", "WARNING", "ERROR", "CRITICAL"]
    soobshenia = [
        "CPU usage: {}",
        "Memory usage: {}",
        "Disk usage: {}",
        "Network traffic: {}",
        "Database connection timeout",
        "Service restarted",
        "User login failed",
        "Backup completed"
    ]

    na_fail = kollichestvo_zapis // kollichestvo_failow
    vremya = datetime(2026, 9, 12, 10, 0, 0)
    for nomer in range(1, kollichestvo_failow + 1):
        name_faila = f"server_{nomer:02d}.log"
        put = os.path.join(config.logi, name_faila)
        with open(put, "w", encoding="utf-8") as f:
            for i in range(na_fail):
                uroven = random.choice(urovni)

                shablon = random.choice(soobshenia)
                if "{}" in shablon:
                    znachenie = random.randint(1, 100)
                    soob = shablon.format(znachenie)
                else:
                    soob = shablon
                vremya = vremya + timedelta(seconds=random.randint(1, 5))
                stroka_vremeni = vremya.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{stroka_vremeni} | server_{nomer:02d} | {uroven} | {soob}\n")
    return kollichestvo_failow