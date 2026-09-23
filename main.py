import logging
from logging.handlers import TimedRotatingFileHandler
import config
import modules.servers as servers
import modules.generator as generator
import utils.validators as validators
import utils.helpers as helpers
import modules.logs as logs
import modules.parser as parser
import modules.analyzer as analyzer
import modules.statistics as statistics
import modules.benchmark as benchmark
import modules.reports as reports

def nastroika_logov():
    handler = TimedRotatingFileHandler(
        config.faile_prilozhenia,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)d %(message)s"
    )
    handler.setFormatter(formatter)
    logging.basicConfig(level = logging.INFO, handlers = [handler])

def menu():
    helpers.razdelitel()
    print("SYSTEM MONITOR")
    helpers.razdelitel()
    print("1. Servers")
    print("2. Logs")
    print("3. Analyze")
    print("4. Statistics")
    print("5. Anomalies")
    print("6. Reports")
    print("7. Generate test servers")
    print("8. Generate test logs")
    print("9. Benchmark")
    print("0. Exit")

def menu_logs():
    print("\n--- Logs ---")
    print("1. All record")
    print("2. Only ERROR")
    print("3. Only CRITICAL")
    print("4. Only WARNING")
    print("5. Search within the message")
    print("6. Search the server")
    print("7. Search by date")
    print("0. Back")

    vybor = input("Выбор: ").strip()
    puti = logs.spisok_logov()

    if not puti:
        print("Логов нету, сгенерируйте")
        return
    if vybor == "1":
        pokazat_zapisi(parser.razbor_vsego(puti))
    elif vybor == "2":
        pokazat_zapisi(filtrovat(puti, "uroven","ERROR"))
    elif vybor == "3":
        pokazat_zapisi(filtrovat(puti, "uroven","CRITICAL"))
    elif vybor == "4":
        pokazat_zapisi(filtrovat(puti, "uroven","WARNING"))
    elif vybor == "5":
        text = input("Что искать в сообщении?").strip()
        pokazat_zapisi(filtrovat(puti,"soobshenie", text))
    elif vybor == "6":
        server = input("Какой сервер?").strip()
        pokazat_zapisi(filtrovat(puti, "server", server))
    elif vybor == "7":
        data = input("Дата (YYYY-MM-DD)? ").strip()
        pokazat_zapisi(filtrovat(puti, "data", data))
    elif vybor == "0":
        return
    else:
        print("Такого пункта нету")

def filtrovat(puti, pole, znachenie):
    for zapis in parser.razbor_vsego(puti):
        if pole == "soobshenie":
            if znachenie.lower() in zapis.soobshenie.lower():
                yield zapis
        else:
            if getattr(zapis,pole) == znachenie:
                yield zapis
def pokazat_zapisi(gen):
    kol = 0
    for zapis in gen:
        print(zapis)
        kol += 1
        if kol >=50:
            print("")
            break
    print(f"Показано записей: {kol}")
    logging.info("Показано записей: %d", kol)

def menu_servers(servery):
    print("\n--- Список серверов ---")
    if not servery:
      print("Список пуст. Сначала сгенерируй серверы (пункт 7)")
      return
    for s in servery:
        print(s)
def genmenu_servers():
    kol = validators.poluchit_chislo("Сколько серверов создать?")
    spisok = generator.gen_server(kol)
    print(f"Созданно серверов: {len(spisok)}")
    logging.info("Создано серверов: %d", len(spisok))

def genmenu_logs():
    zapisi = validators.poluchit_chislo("Сколько записей? ")
    failov = validators.poluchit_chislo("Сколько файлов? ")
    generator.gen_logs(zapisi, failov)
    print(f"Созданно файлов: {failov}, записей: {zapisi}")
    logging.info("Созданно логов: %d ",failov)
    logging.info("Записей в: %d ",zapisi)

def stat_menu():
    puti = logs.spisok_logov()
    if not puti:
        print("Логов нет, сгенерируйте")
        return
    stat =statistics.poluchitat_statistiku(puti)
    statistics.pokazat_statistiku(stat)
    logging.info("Показана статистика")

def anom_menu():
    puti = logs.spisok_logov()
    if not puti:
        print("Логов нет, сгенерируйте")
        return
    anomali = analyzer.nayti_anomali(puti)
    analyzer.pokaz_anomali(anomali)
    logging.info("Найдено аномалий: %d", len(anomali))

def analyzer_menu():
    puti = logs.spisok_logov()
    if not puti:
        print("Логов нет, сгенерируйте")
        return
    print("\n--- Анализ логов ---")
    shet = analyzer.schet_yrovnei(puti)
    analyzer.pokaz_urovni(shet)
    df = analyzer.dataframe(puti)
    print(f"\nВсего записей в DataFrame: {len(df)}")
    group = analyzer.problem_servery(df)
    analyzer.pokaz_problem(group)
    svodka = analyzer.grup_serverov(df)
    print("\n--- Сводка по серверам ---")
    print(svodka.to_string(index=False))
    logging.info("Анализ завершен")

def bench_menu():
    puti = logs.spisok_logov()
    if not puti:
        print("Логов нет, сгенерируйте")
        return
    if len(puti)<2:
        print("Требуется хотя бы 2 файла для сравнения")
        return
    benchmark.sravnenie(puti, kol_potokov=4,kol_proccessov=4)
    logging.info("Benchmark завершён")

def report_menu():
    print("\n--- Reports ---")
    print("1. General report")
    print("2. Server report")
    print("3. Error report")
    print("4. Load report")
    print("5. Anomaly report")
    print("6. All reports at once")
    print("0. Back")

    vybor = input("Выбор: ").strip()
    puti = logs.spisok_logov()
    if not puti:
        print("Логов нету сгенерируйте")
        return
    if vybor == "1":
        reports.obshiy_otchet()
    elif vybor == "2":
        reports.otchet_po_serveram()
    elif vybor == "3":
        reports.otchet_po_oshibkam()
    elif vybor == "4":
        reports.otchet_po_nagruzke()
    elif vybor == "5":
        reports.otchet_po_anomaliam()
    elif vybor == "6":
        reports.obshiy_otchet()
        reports.otchet_po_serveram()
        reports.otchet_po_oshibkam()
        reports.otchet_po_nagruzke()
        reports.otchet_po_anomaliam()
        print("\nВсе отчёты сохранены в папке reports/")
    elif vybor == "0":
        return
    else:
        print("Такого пункта нет")
    logging.info("Отчеты сформированы")

def main():
    nastroika_logov()
    logger = logging.getLogger("main")
    config.sozdat_papki()
    config.zagruzka_nastroek()
    logger.info("Программа запущена")
    servery = servers.zagruzka_serverov()
    logger.info("Загружено серверов: %d", len(servery))

    while True:
        menu()
        vybor = input("Выбор: ").strip()
        if vybor == "1":
            menu_servers(servery)
        elif vybor == "2":
            menu_logs()
        elif vybor == "3":
            analyzer_menu()
        elif vybor == "4":
            stat_menu()
        elif vybor == "5":
            anom_menu()
        elif vybor == "6":
            report_menu()
        elif vybor == "7":
            genmenu_servers()
            servery = servers.zagruzka_serverov()
        elif vybor == "8":
            genmenu_logs()
        elif vybor == "9":
            bench_menu()
        elif vybor == "0":
            logger.info("Программа завершена")
            print("Выход")
            break
        else:
            print("Такого пункта пока нет")
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error("Общая ошибка: %s", e)
        print ("Произошла ошибка, вся инфрормация находится logs/application.log")



