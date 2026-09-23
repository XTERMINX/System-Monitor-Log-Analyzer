import numpy as np
import modules.parser as parser

def stat_dannye(puti):
    cpu=[]
    ram=[]
    disk=[]
    network=[]
    for zapis in parser.razbor_vsego(puti):
        soob = zapis.soobshenie
        if soobshenie_stat(soob,"CPU usage"):
            cpu.append(izvlech_chislo(soob))
        elif soobshenie_stat(soob,"Memory usage"):
            ram.append(izvlech_chislo(soob))
        elif soobshenie_stat(soob,"Disk usage"):
            disk.append(izvlech_chislo(soob))
        elif soobshenie_stat(soob, "Network traffic"):
            network.append(izvlech_chislo(soob))
    return cpu, ram, disk, network

def soobshenie_stat(soob,key):
    return soob.startswith(key)
def izvlech_chislo(soob):
    chasti = soob.split(":")
    if len(chasti)==2:
        try:
            return int(chasti[1].strip())
        except ValueError:
            return 0
    return 0

def rasshitat_statistiku(dannye):
    if not dannye:
        return None
    massiv = np.array(dannye)
    return {
        "sred":float(np.mean(massiv)),
        "min":int(np.min(massiv)),
        "max":int(np.max(massiv)),
        "mediana":float(np.median(massiv)),
        "otklonenie":float(np.std(massiv)),
        "kollichestvo":len(dannye)
    }
def poluchitat_statistiku(puti):
    cpu, ram, disk, network = stat_dannye(puti)
    return {
        "cpu":rasshitat_statistiku(cpu),
        "ram":rasshitat_statistiku(ram),
        "disk":rasshitat_statistiku(disk),
        "network":rasshitat_statistiku(network)
    }
def pokazat_statistiku(stat):
    for nazvanie, pokazateli in stat.items():
        if pokazateli is None :
            print(f"{nazvanie.upper()}:нет данных")
            continue
        print(f"\n{nazvanie.upper()}:")
        print(f"Среднее:  {pokazateli['sred']:.2f}")
        print(f"Минимум:  {pokazateli['min']}")
        print(f"Максимум: {pokazateli['max']}")
        print(f"Медиана:  {pokazateli['mediana']:.2f}")
        print(f"Отклонение: {pokazateli['otklonenie']:.2f}")
        print(f"Записей: {pokazateli['kollichestvo']}")

