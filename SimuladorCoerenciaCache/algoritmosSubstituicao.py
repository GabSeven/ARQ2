from random import randint


def algoritmoLRU(cache):
    return 0


def algoritmoLFU(cache):
    return 0


def algoritmoFIFO(cache):
    cache.aux += 1
    return cache.aux - 1


def algoritmoRAND(cache):
    return randint(0, cache.tamanho - 1)
