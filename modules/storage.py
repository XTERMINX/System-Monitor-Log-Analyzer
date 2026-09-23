import json
import os
import csv

def sozdanie_papkiotch():
    if not os.path.exists('reports'):
        os.makedirs('reports')

def save_json(name, data):
    sozdanie_papkiotch()
    put = os.path.join('reports', name)
    try:
        with open(put, 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Сохранено: {put}")
    except Exception as e:
        print("Ошибка сохранение JSON:", e)

def save_csv(name, stroki, zagolovki):
    sozdanie_papkiotch()
    put = os.path.join('reports', name)
    try:
        with open(put, 'w', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(zagolovki)
            writer.writerow(stroki)
        print(f"Сохранено: {put}")
    except Exception as e:
        print("Ошибка сохранения CSV:", e)

def sohranit_txt(name, text):
    sozdanie_papkiotch()
    put = os.path.join('reports', name)
    try:
        with open(put, 'w', encoding="utf-8") as f:
            f.write(text)
        print(f"Сохранено: {put}")
    except Exception as e:
        print("Ошибка сохранение TXT:", e)