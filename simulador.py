import io
from sys import argv
from enum import Enum

# Estados do Protocolo de Coerência - MOESI
class Estado(Enum):
    M = "M"
    O = "O"
    E = "E"
    S = "S"
    I = "I"

# Possíveis algoritmos de Substituição
class Algoritmo(Enum):
    LRU = "Least Recently Used"
    LFU = "Least Frequently Used"
    FIFO = "First In - First Out"
    RAND = "Aleatório"

class LinhaCache:
    def __init__(self, tamLinha):
        self.estado: Estado = Estado.I
        self.bloco: list[int] = [0 for _ in range(tamLinha)]

class Cpu:
    def __init__(self, sharedCache):
        self.status = "A"
        # self.cache
        self.sharedCache = sharedCache
    
    def processarInstrucao(self, instrucao, endereco): # talvez trocar o nome de uma das duas processarInstrucao
        pass
        

class Cache:
    def __init__(self, qntLinhas, tamLinha):
        self.memoria = None

class Simulador:
    def __init__(self, qntdCpus, qntLinhas, tamLinha, algoritmoSubsitituicao):
        self.sharedCache = Cache(qntdCpus * qntLinhas * 2, tamLinha)
        self.cpus = [Cpu() for _ in range(qntdCpus)]

    def processarInstrucao(self, cpu, instrucao, endereco):
        self.cpus[cpu].processarInstrucao(instrucao, endereco)
        # talvez só checar aqui se *cpu* é um parametro valido com try catch
        # self.print()

def main():
    if len(argv) != 3:
        print("\nQuantidade inesperada de argumentos")
        print("Entrada deve ser do tipo:")
        print("python simulador.py config.data arquivo_de_entrada.data\n")
        return

    with open(argv[1]) as configFile:
        # adicionar leitura das constantes

        tamLinha = 4

        numLinhasCache = 8
        # numPrivada tem q ser menor que a da numCompartilhada

        # LRU, LFU, FIFO, Random - implementar ao menos 2
        algSubstituicaoCache = "FIFO"

        qntCpus = 1

        # mapeamento = associativo
        simulador = Simulador(qntdCpus, numLinhasCache, tamLinha,algSubstituicaoCache)

    with open(argv[2]) as f:
        

        i = 1
        while linha := f.readline():
            elems = linha.split()

            # prevencao de erros
            if len(elems) != 3:
                print(f"erro na linha {i}")
                break

            try:
                cpu = int(elems[0])
                instrucao = int(elems[1])
                endereco = int(elems[2], 16)

            except:
                print("deu ruim")
                break

            if cpu < 0 or cpu >= numProcessadores:
                print("cpu invalida")
                break

            

            print(elems)
            i += 1


if __name__ == "__main__":
    main()
