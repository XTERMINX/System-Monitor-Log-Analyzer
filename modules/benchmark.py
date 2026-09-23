import  time
import  asyncio
import  modules.parallel as parallel

def zamer(func,*args, **kwargs):
    nachalo = time.time()
    result = func(*args, **kwargs)
    konec = time.time()
    return result, konec - nachalo

def sravnenie(puti, kol_potokov = 4, kol_proccessov = 4):
    print("\n" + "=" * 40)
    print("PERFORMANCE TEST")
    print("=" * 40)
    rez1, t1 = zamer(parallel.obrabotka_posledovatelnosti, puti)
    rez2, t2 = zamer(parallel.obrabotka_potokami,puti, kol_potokov)
    nachalo = time.time()
    rez3 = asyncio.run(parallel.obrabotka_async(puti))
    t3 = time.time() - nachalo
    rez4, t4 = zamer(parallel.obrabotat_proccesami, puti, kol_proccessov)

    print(f"Файлов:           {len(puti)}")
    print(f"Записей:          {rez1}")
    print(f"Sequential:       {t1:.2f} сек")
    print(f"Threads ({kol_potokov}): {t2:.2f} сек")
    print(f"Asyncio:          {t3:.2f} сек")
    print(f"Multiprocessing:  {t4:.2f} сек")

    vremena = {
        "Sequential": t1,
        "Threads": t2,
        "Asyncio": t3,
        "Multiprocessing": t4
    }
    samiy_bystriy = min(vremena, key=vremena.get)
    print(f"Fastest: {samiy_bystriy}")
    print("=" * 40)

    return vremena