import io
from enum import Enum
from multiprocessing import Value
from sys import argv


# Estados do Protocolo de Coerência - MOESI
class Estado(Enum):
    M = "Modified"
    O = "Owned"
    E = "Exclusive"
    S = "Shared"
    I = "Invalid"


# Possíveis algoritmos de Substituição
class Algoritmo(Enum):
    LRU = "Least Recently Used"
    LFU = "Least Frequently Used"
    FIFO = "First In - First Out"
    RAND = "Aleatório"


class Instrucao(Enum):
    LEITURA_INSTRUCAO = 0
    LEITURA_DADO = 2
    ESCRITA_DADO = 3


class Operacao:
    def __init__(self, elems: list[str]):
        self.cpu: int = int(elems[0])
        self.instrucao: Instrucao = Instrucao(int(elems[1]))
        self.endereco: int = int(elems[2], 16)

    def __str__(self):
        return f"Operação: {Instrucao(self.instrucao).name} - Processador {self.cpu} - Endereço: {self.endereco}"


class Linha:
    def __init__(self, tamLinha):
        self.bloco: int | None = None
        self.tamanho = tamLinha

    # len é mais usado mas posso tá exagerando (kkkkkkk
    def __len__(self) -> int:
        return self.tamanho


class LinhaPrivada(Linha):
    def __init__(self, tamLinha):
        super().__init__(tamLinha)
        self.estado: Estado = Estado.I
        # deixa só o endereco Base do bloco (o primeiro endereco)
        self.bloco: int | None = None  # faz sentido deixar None?

    def __str__(self):
        return f"Endereço: {self.bloco} - Estado: {self.estado.name}"


class Cache:
    def __init__(self, qntLinhas, tamLinha):
        self.memoria = [Linha(tamLinha) for _ in range(qntLinhas)]

    def __contains__(self, endereco) -> bool:
        for linha in self.memoria:
            if endereco - {endereco % len(linha)} == linha.bloco:
                return True
        return False
    
    def __getitem__(self, endereco) -> Linha :
        for linha in self.memoria:
            if endereco - {endereco % len(linha)} == linha.bloco:
                return linha
        raise IndexError


class CachePrivada(Cache):
    def __init__(self, qntLinhas, tamLinha):
        # super().__init__(qntLinhas, tamLinha)
        self.memoria = [LinhaPrivada(tamLinha) for _ in range(qntLinhas)]

    def __contains__(self, endereco) -> bool:
        for linha in self.memoria:
            if endereco - {endereco % len(linha)} == linha.bloco and linha.estado != Estado.I:
                return True
        return False

    # def modify(self, endereco)
    # def own(self, endereco)
    # def exclusive(self, endereco)
    # def share(self, endereco)
    # def invalidate(self, endereco)


class Barramento:
    def __init__(self):
        self.cpus: list[Cpu]

    # def broadcast()


class Cpu:
    def __init__(self, id: int, qntLinhas, tamLinha, sharedCache: Cache, barramento):
        self.id = id
        self.privateCache = CachePrivada(qntLinhas, tamLinha)
        self.sharedCache = sharedCache
        self.barramento = barramento
        self.hits = 0
        self.miss = 0

    def processar(self, instrucao, endereco):
        if endereco in self.privateCache:
            self.hits += 1
            # if instrucao == escrita
            #   self.barramento.bus_upgrade(endereco) # mensagem bus_upgrade - invalida o restante
            #   self.privateCache.modify(endereco)
            # return

        self.miss += 1
        # if self.barramento.bus_read(endereco):
        #    self.privateCache.addShared(endereco)
        # else if endereco in self.sharedCache
        #    self.privateCache.addExclusive(endereco)
        # else:
        #    busca endereco na MP e deixa na cache privada e na compartilhada

        # CORRIGIR ALGUNS PROBLEMAS DE LOGICA
        # nao chequei os estados atuais das linhas de cache

        pass

    def __str__(self):
        return "\n".join(
            [
                f"Processador {self.id} (Hits: {self.hits} - Miss: {self.miss}):",
                # f"[Linha {i}]" for i in self.cache.linhas
            ]
        )

        # Processador 1 (Hits: 150 - Miss: 402):
        # [Linha 0] Endereço: a4512f34 - Estado: S
        # [Linha 1] Endereço: 00000000 - Estado: I
        # [Linha 2] Endereço: bc122312 - Estado: S
        # [Linha 3] Endereço: d9845678 - Estado: E


class Simulador:
    def __init__(self, qntdCpus, qntLinhas, tamLinha, algoritmoSubsitituicao):
        self.barramento = Barramento()
        self.sharedCache = Cache(qntdCpus * qntLinhas * 2, tamLinha)
        self.cpus = [
            Cpu(i, self.sharedCache, qntLinhas, tamLinha, self.barramento)
            for i in range(qntdCpus)
        ]

        self.barramento.cpus = self.cpus

    def processar(self, op: Operacao):
        try:
            self.cpus[op.cpu].processar(op.instrucao, op.endereco)
        except IndexError:
            print(f"Operacao inválida, não há Processador {op.cpu}")
            return
        # talvez só checar aqui se *cpu* é um parametro valido com try catch
        # self.print()

    # def __str__(self):


# print(operacao)
# print(simulador)
#         A operação realizada, o endereço no qual ela foi feita e o processador que a realizou

# ◦ Em outras palavras, a linha do arquivo de entrada;
# • A mensagem enviada no barramento devido a realização daquela operação;
# • O estado da cache privada de cada processador;
# ◦ Quais blocos estão em cache cada linha da cache;
# ◦ Qual o estado de cada bloco;
# • Os endereços dos dados que estão na cache compartilhada
# • A quantidade de acertos (hit) e erros (miss) em cada uma das caches privadas.
# ◦ Lembre-se que a tentativa de acessar uma linha inválida é um miss na cache.
# A saída pode ser mostrada em tela (com uma interface gráfica ou terminal) ou um arquivo de log
# deve ser gerado.


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
        simulador = Simulador(qntCpus, numLinhasCache, tamLinha, algSubstituicaoCache)

    with open(argv[2]) as f:
        print(f"\nInício do Simulador - {argv[2]}")
        print("=" * 30)
        print()
        i = 1
        while linha := f.readline():
            elems = linha.split()
            # prevencao de erros
            if len(elems) != 3:
                print(f"erro na linha {i}")
                break

            try:
                operacao = Operacao(elems)

            except ValueError as e:
                print(e)
                break

            # if cpu < 0 or cpu >= qntCpus:
            #     print("cpu invalida")

            #     break
            print(f"Linha {i} - {operacao}")
            simulador.processar(operacao)

            # simulador.print()

            # print(elems)
            i += 1


# =============================================

# Operação: LEITURA - Processador 3 - Endereço: b8590400
# Mensagem no barramento: Busca de dados (Read Miss)

# --- Caches Privadas ---
# Processador 0 (Hits: 232 - Miss: 320):
# [Linha 0] Endereço: b3212238 - Estado: S
# [Linha 1] Endereço: bc431221 - Estado: M
# [Linha 2] Endereço: bc122312 - Estado: I
# [Linha 3] Endereço: 00000000 - Estado: I


# --- Cache Compartilhada ---
# Endereços presentes:
# b3212238 | bc431221 | bc122312 | a4512f34
# d9845678 | 00000000 | 00000000 | 00000000

# =============================================
# Próxima operação...

if __name__ == "__main__":
    main()
