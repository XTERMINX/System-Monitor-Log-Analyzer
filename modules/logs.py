import os
import config

def spisok_logov():
    if not os.path.exists(config.logi):
        return []

    faily = []
    for name in os.listdir(config.logi):
        if name.endswith(".log") and name != "application.log":
            put = os.path.join(config.logi, name)
            faily.append(put)
    return faily

def chtenie_failov(put):
    try:
        with open(put, "r", encoding= "utf-8") as f:
            for stroka in f:
                yield stroka.strip()
    except FileNotFoundError:
        print("Файл не найден",put)
    except Exception as e:
        print("Ошибка чтение файла",e)

def schet_strok(put):
    kol = 0
    for _ in chtenie_failov(put):
        kol += 1
    return kol