import json
import os
from json import JSONDecodeError
import config

class Server:
    __slots__ = ("id", "name", "os_name", "ip", "environment", "cpu", "ram", "status")
    def __init__(self, id, name, os_name, ip, environment, cpu, ram, status):
        self.id = id
        self.name = name
        self.os_name = os_name
        self.ip = ip
        self.environment = environment
        self.cpu = cpu
        self.ram = ram
        self.status = status
    def __str__(self):
        return f"{self.name} ({self.os_name},{self.environment}) - {self.status}"
    def __repr__(self):
        return f"Server ({self.id},'{self.name}')"

def zagruzka_serverov():
    if not os.path.exists(config.faile_serverov):
        return []
    try:
        with open(config.faile_serverov,"r",encoding="utf-8") as f:
            data = json.load(f)
    except JSONDecodeError:
        print("Ошибка: файл поврежден")
        return []
    except FileNotFoundError:
        print("Ошибка: файл не найден")
        return []

    servery = []
    for item in data:
        try:
            s = Server(
                id=item["id"],
                name=item["name"],
                os_name=item["os_name"],
                ip=item["ip"],
                environment=item["environment"],
                cpu=item["cpu"],
                ram=item["ram"],
                status=item["status"]
            )
            servery.append(s)
        except KeyError as e:
            print("Пропущена запись сервера",e)
    return servery

def save_server(servery):
    spisok = []
    for s in servery:
        spisok.append({
            "id": s.id,
            "name": s.name,
            "os_name": s.os_name,
            "ip": s.ip,
            "environment": s.environment,
            "cpu": s.cpu,
            "ram": s.ram,
            "status": s.status
        })
    try:
        with open(config.faile_serverov,"w",encoding="utf-8") as f:
            json.dump(spisok,f,ensure_ascii=False,indent=4)
    except Exception as e:
        print("Ошибка сохранения сервера",e)

