import modules.logs as logs
from itertools import chain

class LogRecord:
    __slots__ = ("data", "vremya", "server", "uroven", "soobshenie")
    def __init__(self, data, vremya, server, uroven, soobshenie):
        self.data = data
        self.vremya = vremya
        self.server = server
        self.uroven = uroven
        self.soobshenie = soobshenie

    def __str__(self):
        return f"{self.data} {self.vremya} | {self.server} | {self.uroven} | {self.soobshenie}"
    def __repr__(self):
        return f"LogRecord({self.server}, {self.uroven})"

def razbor_strok(stroka):
    chasti = stroka.split(" | ")
    if len(chasti) != 4:
        return None
    data_vremya = chasti[0].split(" ")
    if len(data_vremya) != 2:
        return None
    data = data_vremya[0]
    vremya = data_vremya[1]
    server = chasti[1]
    uroven = chasti[2]
    soobshenie = chasti[3]

    if uroven not in ("INFO", "WARNING", "ERROR", "CRITICAL"):
      return None
    return LogRecord(data, vremya, server, uroven, soobshenie)

def razbor_failov(put):
    for stroka in logs.chtenie_failov(put):
        zapis = razbor_strok(stroka)
        if zapis is not None:
            yield zapis

def razbor_vsego(puti):
    return chain.from_iterable(razbor_failov(put) for put in puti)

class LogIterator:
    def __init__(self, puti):
        self.puti = puti
        self.fail_index = 0
        self.zapisi = None
    def __iter__(self):
        return self

    def __next__(self):
        while self.fail_index < len(self.puti):
            if self.zapisi is None:
                put = self.puti[self.fail_index]
                self.zapisi = iter(razbor_failov(put))
            try:
                return next(self.zapisi)
            except StopIteration:
                self.zapisi = None
                self.fail_index += 1
        raise StopIteration()