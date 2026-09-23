import os
import json

dannye = "data"
logi = "logs"
faile_serverov = os.path.join(dannye, "servers.json")
faile_nastroek = os.path.join(dannye, "settings.json")
faile_prilozhenia = os.path.join(logi, "application.log")
nastroyki = {
    "max_threads":4,
    "max_processes":4,
    "porog_anomalii":1.0,
    "test_servers":50,
    "test_logs":100000
}

def sozdat_papki():
    if not os.path.exists(dannye):
        os.makedirs(dannye)
    if not os.path.exists(logi):
        os.makedirs(logi)

def zagruzka_nastroek():
    if os.path.exists(faile_nastroek):
        try:
            with open(faile_nastroek, "r", encoding ="utf8") as f:
                data = json.load(f)
                nastroyki.update(data)
        except Exception as e:
            print("Ошибка чтения настроек:", e)
            print("Файл будет пересоздан")
            save_nastroyki()
    return nastroyki
def save_nastroyki():
    try:
        with open(faile_nastroek, "w", encoding ="utf8") as f:
            json.dump(nastroyki, f,ensure_ascii=False, indent=4)
    except Exception as e:
        print("Ошибка сохранение настроек:",e)