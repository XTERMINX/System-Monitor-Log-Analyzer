import pandas as pd
import modules.parser as parser
import modules.statistics as statistics

def schet_yrovnei(puti):
    shet = {"INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}

    for zapis in parser.razbor_vsego(puti):
        if zapis.uroven in shet:
            shet[zapis.uroven] += 1
    return shet

def dataframe(puti):
    dannye = []
    for zapis in parser.razbor_vsego(puti):
        dannye.append({
            "data": zapis.data,
            "vremya":zapis.vremya,
            "server":zapis.server,
            "uroven":zapis.uroven,
            "soobshenie":zapis.soobshenie
        })
    return pd.DataFrame(dannye)

def problem_servery(df, top=10):
    if df.empty:
        return df
    tolko_error = df[df["uroven"]=="ERROR"]
    group = tolko_error.groupby("server").size()
    group = group.sort_values(ascending=False)
    return group.head(top)
def nayti_anomali(puti,porog=1.7):
    cpu,ram,_,_ = statistics.stat_dannye(puti)
    anomali = []
    if cpu:
        stat = statistics.rasshitat_statistiku(cpu)
        granica = stat["sred"] + porog * stat["otklonenie"]
        for zapis in parser.razbor_vsego(puti):
            if zapis.soobshenie.startswith("CPU usage"):
                znach = statistics.izvlech_chislo(zapis.soobshenie)
                if znach > granica:
                    anomali.append((zapis.server,"CPU",znach,round(granica,2)))
    if ram:
        stat = statistics.rasshitat_statistiku(ram)
        granica = stat["sred"] + porog * stat["otklonenie"]
        for zapis in parser.razbor_vsego(puti):
            if zapis.soobshenie.startswith("Memory usage"):
                znach = statistics.izvlech_chislo(zapis.soobshenie)
                if znach > granica:
                    anomali.append((zapis.server,"Memory",znach,round(granica,2)))
    return anomali

def grup_serverov(df):
    if df.empty:
        return df
    itog = []
    for server in df["server"].unique():
        dannye_servera= df [df["server"]==server]
        oshibki = len(dannye_servera[dannye_servera["uroven"]=="ERROR"])
        preduprezhdenia = len(dannye_servera[dannye_servera["uroven"]=="WARNING"])
        vsego = len (dannye_servera)
        itog.append({
            "server":server,
            "vsego":vsego,
            "oshibki":oshibki,
            "preduprezhdenia":preduprezhdenia,
        })
    result = pd.DataFrame(itog)
    result = result.sort_values(by="oshibki",ascending=False)
    return result
def pokaz_urovni(shet):
    print("\n--- Записи по уровням ---")
    for uroven, kol in shet.items():
        print(f"{uroven}:{kol}")
def pokaz_anomali(anomali):
    print(f"\n--- Аномалии (найдено: {len(anomali)}) ---")
    if not anomali:
        print("Аномалий не обнаружено")
        return
    for server, tip, znach, granica in anomali[:20]:
        print(f"{server} | {tip}: {znach} (порог: {granica})")
    if len(anomali) > 20:
        print(f"и ещё {len(anomali) - 20}")
def pokaz_problem(group):
    print("\n--- Проблемные серверы (топ по ERROR) ---")
    if group.empty:
        print("Нет данных")
        return
    for server, kol in group.items():
        print(f"{server} | {kol}")