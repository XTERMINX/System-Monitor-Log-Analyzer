import os
import threading
import asyncio
import multiprocessing
import modules.parser as parser

def obrabotka_posledovatelnosti(puti):
    kol = 0
    for put in puti:
        for zapis in parser.razbor_failov(put):
            kol += 1
    return kol

def obrabotka_potokov(put, result, index):
    kol = 0
    for zapis in parser.razbor_failov(put):
        kol += 1
    result[index] = kol
def obrabotka_potokami(puti,kol_potokov=4):
    result = [0] * len(puti)
    potoki = []
    ochered = list(range(len(puti)))
    def rabochiy():
        while ochered:
            try:
                i = ochered.pop(0)
            except IndexError:
                break
            obrabotka_potokov(puti[i],result,i)
    for i in range(kol_potokov):
        t = threading.Thread(target=rabochiy)
        potoki.append(t)
        t.start()
    for t in potoki:
        t.join()
    return sum(result)

async def obrabotat_fail(put):
    kol = 0
    for zapis in parser.razbor_failov(put):
        kol += 1
    return kol
async def obrabotka_async(puti):
    zadachi = [obrabotat_fail(put) for put in puti]
    result = await asyncio.gather(*zadachi)
    return sum(result)

def obrabotat_1_fail(put):
    kol = 0
    for zapis in parser.razbor_failov(put):
        kol += 1
    return kol

def obrabotat_proccesami(put,kol_processov=4):
    with multiprocessing.Pool(kol_processov) as pool:
        result = pool.map(obrabotat_1_fail, put)
    return sum(result)