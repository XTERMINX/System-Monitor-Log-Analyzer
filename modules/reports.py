import modules.logs as logs
import modules.parser as parser
import modules.analyzer as analyzer
import modules.statistics as statistics
import modules.servers as servers
import modules.storage as storage
from functools import reduce

def obshiy_otchet():
    servery = servers.zagruzka_serverov()
    puti = logs.spisok_logov()
    vsego_serverov = len(servery)
    aktivny = 0
    for server in servery:
        if server.status == "active":
            aktivny = aktivny + 1
    shet = analyzer.schet_yrovnei(puti)
    vsego_zapisey = sum(shet.values())
    otchet ={
        "servera":{
            "vsego":vsego_serverov,
            "aktivnyh":aktivny,
            "neaktivnyh":vsego_serverov - aktivny
        },
        "logi":{
            "vsego":vsego_zapisey,
            "INFO":shet["INFO"],
            "WARNING":shet["WARNING"],
            "ERROR":shet["ERROR"],
            "CRITICAL":shet["CRITICAL"]
        }
    }
    storage.save_json("summary.json", otchet)
    return otchet

def otchet_po_serveram():
    puti = logs.spisok_logov()
    df = analyzer.dataframe(puti)

    if df.empty:
        print("Нет данных")
        return
    svodka = analyzer.grup_serverov(df)
    zagolovki = ["server", "vsego", "oshibki", "preduprezhdenia"]
    stroki = []
    for _, row in svodka.iterrows():
        stroki.append([row["server"], row["vsego"], row["oshibki"], row["preduprezhdenia"]])
    storage.save_csv("summary.csv",stroki, zagolovki)
    return svodka

def otchet_po_oshibkam():
    puti = logs.spisok_logov()
    schet_soobsheniy = {}
    for zapis in parser.razbor_vsego(puti):
        if zapis.uroven == "ERROR":
            soob = zapis.soobshenie
            schet_soobsheniy[soob] = schet_soobsheniy.get(soob, 0) + 1
    vsego_oshibok = reduce(lambda a, b: a + b, schet_soobsheniy.values(), 0)
    top = sorted(schet_soobsheniy.items(), key=lambda x: x[1], reverse=True)
    otchet = {
        "vsego_oshibok": vsego_oshibok,
        "top": []
    }
    for soob, kol in top[:10]:
        otchet["top"].append({"soobshenie": soob, "kolichestvo": kol})
    storage.save_json("errors.json", otchet)
    print(f"\nВсего ошибок: {vsego_oshibok}")
    print("--- ТОП-10 ошибок ---")
    for soob, kol in top[:10]:
        print(f"  {kol} раз: {soob}")
    return otchet
def otchet_po_nagruzke():
    puti = logs.spisok_logov()
    stat = statistics.poluchitat_statistiku(puti)
    zagolovki = ["pokazatel", "srednee", "min", "max", "mediana", "otklonenie"]
    stroki = []
    for nazvanie, pokazateli in stat.items():
        if pokazateli is None:
            continue
        stroki.append([
            nazvanie,
            round(pokazateli["sred"], 2),
            pokazateli["min"],
            pokazateli["max"],
            round(pokazateli["mediana"], 2),
            round(pokazateli["otklonenie"], 2)
        ])
    storage.save_csv("statistics.csv", stroki, zagolovki)
    return stat

def otchet_po_anomaliam():
    puti = logs.spisok_logov()
    anomali = analyzer.nayti_anomali(puti)
    otchet = {
        "vsego_anomaliy": len(anomali),
        "primer": []
    }
    for server,tip,znach,granica in anomali[:20]:
        otchet["primer"].append({
            "server":server,
            "tip":tip,
            "znachenie":znach,
            "granica":granica
        })
    storage.save_json("anomalies.json", otchet)
    return otchet