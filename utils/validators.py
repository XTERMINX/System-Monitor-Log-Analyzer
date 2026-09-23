def proverka_chisla(stroka):
    try:
        int(stroka)
        return True
    except ValueError:
        return False

def poluchit_chislo(stroka2):
    while True:
        vvod = input(stroka2).strip()
        if proverka_chisla(vvod):
            return int(vvod)
        print("Нужно ввести число")