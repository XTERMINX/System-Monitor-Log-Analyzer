import time
from datetime import datetime

def poluchit_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def izmerit_time(func):
    def wrapper(*args, **kwargs):
        nachalo = time.time()
        result = func(*args, **kwargs)
        konec = time.time()
        raznica = konec - nachalo
        print(f"Время выполнение: {raznica:.2f}сек")
        return result
    return wrapper

def razdelitel(sim="=",dlinna = 40):
    print(sim * dlinna)
def format_razmer(chislo):
    return f"{chislo:,}".replace(",", " ")