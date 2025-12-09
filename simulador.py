import io
from enum import Enum
from multiprocessing import Value
from random import randint
from sys import argv


# MOSI - modificacao do estado MOESI focado em Corencia entre
# caches Privada, cache Compartlhada e Memoria Principal
# Estados do Protocolo de Coerência - MOSI
nsagens do Barramento
class Mensagem(Enum):
    READ = "Bus Read"
    READ_EXCLUSIVE = "Bus Read EXCLUSIVE"
    UPGRADE = "Bus Upgrade"
    INVALIDATE = "Bus Invalidate"
    NENHUMA = ""

    def __str__(self):
        if self == Mensagem.NENHUMA:
            return "Nenhuma Mensagem enviado ao barramento"
        return f"Mensagem no Barramento: {self.name}"


# Possíveis algoritmos de Substituição
# class Algoritmo(Enum):
#     LRU = "Least Recently Used"
#     LFU = "Least Frequently Used"
#     FIFO = "First In - First Out"
#     RAND = "Aleatório"


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
        return f"Processador {self.cpu} - Endereço: {hex(self.endereco)[2:]:0>8}\nOperação: {Instrucao(self.instrucao).name:<17} "


class Linha:
    def __init__(self, tamLinha):
        self.bloco: int = 0
        self._tamanho: int = tamLinha
        self.aux: int = 0  # parametro usado nos metodos de substituicao

    # len é mais usado mas posso tá exagerando (kkkkkkk
    def __len__(self) -> int:
        return self._tamanho

    def __str__(self):
        return f"{hex(self.bloco)[2:]:0>8}"


class LinhaPrivada(Linha):
    def __init__(self, tamLinha):
        super().__init__(tamLinha)
        self.estado: Estado = Estado.I

    def __str__(self):
        return f"Endereço: {hex(self.bloco)[2:]:0>8} - Estado: {self.estado.name}"

    # nao precisa de funcao pra mudar os estados ne


def algoritmoLRU(cache):
    return 0


def algoritmoLFU(cache):
    return 0


def algoritmoFIFO(cache):
    cache.aux += 1
    return cache.aux - 1


def algoritmoRAND(cache):
    return randint(0, cache.tamanho - 1)


class Cache:
    ALGORITMOS = {
        "LRU": algoritmoLRU,
        "LFU": algoritmoLFU,
        "FIFO": algoritmoFIFO,
        "RAND": algoritmoRAND,
    }

    def __init__(
        self, qntLinhas: int, tamLinha: int, /, tipoLinha=Linha, algoritmo="FIFO"
    ):
        self._tamanho = qntLinhas
        self.memoria = [tipoLinha(tamLinha) for _ in range(qntLinhas)]
        self.hits = 0
        self.miss = 0
        self.aux = 0
        if algoritmo.upper() not in self.ALGORITMOS.keys():
            algoritmo = "FIFO"

        self._algoritmoDeSubstituicao = self.ALGORITMOS[algoritmo.upper()]

    def __contains__(self, endereco) -> bool:
        for linha in self.memoria:
            if endereco - (endereco % len(linha)) == linha.bloco:
                return True
        return False

    def __getitem__(self, endereco) -> Linha | None:
        for linha in self.memoria:
            if endereco - (endereco % len(linha)) == linha.bloco:
                self.hits += 1
                return linha
        self.miss += 1
        return None

    def __len__(self) -> int:
        return self._tamanho

    @property
    def tamanho(self) -> int:
        return self._tamanho

    def substituicao(self):
        return self._algoritmoDeSubstituicao()

    def __str__(self):
        txt = f"(Hits: {self.hits:>4} - Miss: {self.miss:>4})\n"
        txt += "Enderecos presentes:\n"
        for i in range(0, self.tamanho, 4):
            txt += " | ".join([str(linha) for linha in self.memoria[i : i + 4]])
            txt += "\n"
        return txt
        # Endereços presentes:
        # b3212238 | bc431221 | bc122312 | a4512f34
        # d9845678 | 00000000 | 00000000 | 00000000

    def insere(self, bloco):
        # id_remove = self.substituicao()
        # FIFO
        self.memoria[self.aux].bloco = bloco
        self.aux = (self.aux + 1) % self.tamanho
        return self.memoria[self.aux]

    def atualizaMemoria(self, linha):
        MemoriaPrincipal.atualiza(linha.bloco)


class CachePrivada(Cache):
    def __init__(self, qntLinhas: int, tamLinha: int, cpu, /, tipoLinha=LinhaPrivada):
        super().__init__(qntLinhas, tamLinha, tipoLinha)
        self.cpu = cpu
        # remover isso aqui, so deixei pra n ficar apitano o pydantic
        self.memoria = [tipoLinha(tamLinha) for _ in range(qntLinhas)]

    def __contains__(self, endereco) -> bool:
        for linha in self.memoria:
            if (
                endereco - {endereco % len(linha)} == linha.bloco
                and linha.estado != Estado.I
            ):
                return True
        return False

    def __getitem__(self, endereco) -> LinhaPrivada | None:
        for linha in self.memoria:
            if (
                endereco - (endereco % len(linha)) == linha.bloco
                and linha.estado != Estado.I
            ):
                return linha
        return None

    # fazem sentido esses nomes de metodos?
    # def modify(self, endereco):
    #     if (linha := self[endereco]) is not None:
    #         linha.estado = Estado.M

    # def own(self, endereco):
    #     if linha := self[endereco]:
    #         linha.estado = Estado.O

    # def exclusive(self, endereco):
    #     if (linha := self[endereco]) is not None:
    #         linha.estado = Estado.O

    # def share(self, endereco):
    #     if (linha := self[endereco]) is not None:
    #         linha.estado = Estado.S

    def invalidate(self, endereco):
        if (linha := self[endereco]) is not None:
            linha.estado = Estado.I

    # melhor forma de fazer isso?
    def insereM(self, bloco):
        self.insere(bloco).estado = Estado.M

    def insereO(self, bloco):
        self.insere(bloco).estado = Estado.O

    def insereS(self, bloco):
        self.insere(bloco).estado = Estado.S

    def insere(self, bloco):
        print("inserindo...")
        for linha in self.memoria:
            if linha.estado == Estado.I:
                linha.bloco = bloco
                return linha

        # FIFO
        linha = self.memoria[self.aux]

        if linha.estado in [Estado.M, Estado.O]:
            self.atualizaMemoria(linha)

        self.memoria[self.aux].bloco = bloco.bloco
        self.aux = (self.aux + 1) % self.tamanho
        return self.memoria[self.aux]

    def atualizaMemoria(self, linha):
        self.cpu.atualizaMemoria(linha)


class MemoriaPrincipal:
    @staticmethod
    def busca(endereco: int) -> int:
        """
        "Busca" na memoria
        """
        return endereco

    @staticmethod
    def atualiza(endereco: int) -> int:
        """
        "Atualiza" o endereco de memoria
        """
        pass


class Barramento:
    def __init__(self):
        self.cpus: list[Cpu]
        self.sharedCache: Cache

    def read(self, endereco, id):
        print(Mensagem.READ)
        bloco = None
        for cpu in self.cpus:
            if cpu.id == id:
                pass

            if (linha := cpu.privateCache[endereco]) is not None:
                if linha.estado in [Estado.O, Estado.M]:
                    linha.estado = Estado.O
                    bloco = linha.bloco

        if bloco is None:
            if (linha := self.sharedCache[endereco]) is not None:
                print("ta na cache1")
                bloco = linha.bloco
                print(bloco)

        return bloco

    def read_exclusive(self, endereco, id) -> int | None:
        print(Mensagem.READ_EXCLUSIVE)
        bloco = None
        for cpu in self.cpus:
            if cpu.id == id:
                pass

            if (linha := cpu.privateCache[endereco]) is not None:
                if linha.estado != Estado.S:
                    # em tese, so pode haver uma linha em M ou O entre os cpus com o bloco
                    # procurado entao da pra pegar o bloco de qualquer linha que nao for S
                    # pq só vai ter ele (I nem pode ser retornado ali em cima)
                    bloco = linha.bloco
                linha.estado = Estado.I

        if bloco is None:
            if (linha := self.sharedCache[endereco]) is not None:
                print("ta na cache2")
                bloco = linha.bloco

        return bloco

    def upgrade(self, endereco, id):
        # upgrade nao deveria invalidar blocos M, O ou E.
        # como não há manipulacao real de dados, vamos fingir
        # que o sistema preza pela consistencia de dados
        print(Mensagem.UPGRADE)
        self.invalidate(endereco, id)

    def invalidate(self, endereco, id):
        for cpu in self.cpus:
            if cpu.id != id:
                cpu.privateCache.invalidate(endereco)


class Cpu:
    def __init__(
        self,
        id: int,
        qntLinhas: int,
        tamLinha: int,
        sharedCache: Cache,
        barramento: Barramento,
    ):
        self.id = id
        self.privateCache = CachePrivada(qntLinhas, tamLinha, self)
        self.sharedCache = sharedCache
        self.barramento = barramento

    # vamo tratar "bloco" como a informacao e "linha" como estrutura fisica
    # "O bloco X está na linha Y da cache"
    # "A linha Y contém o bloco X"
    # "Miss na cache - preciso trazer o bloco para uma linha"
    def processar(self, instrucao, endereco):
        if (linha := self.privateCache[endereco]) is not None:
            self.privateCache.hits += 1
            if instrucao == Instrucao.ESCRITA_DADO:
                if linha.estado == Estado.S:
                    self.barramento.upgrade(endereco, self.id)
                elif linha.estado == Estado.O:
                    self.barramento.invalidate(endereco, self.id)
                else:  # estado == Estado.M
                    print(Mensagem.NENHUMA)
                linha.estado = Estado.M  # funcao pra isso?
            return

        # if bloco not in cachePrivado
        self.privateCache.miss += 1
        if instrucao == Instrucao.ESCRITA_DADO:
            if (bloco := self.barramento.read_exclusive(endereco, self.id)) is None:
                bloco = self.busca(endereco)
            self.insereM(bloco)
            return

        # instrucao == Leitura
        if (bloco := self.barramento.read(endereco, self.id)) is None:
            bloco = self.busca(endereco)
            self.insereO(bloco)
            return
        self.insereS(bloco)
        return

    def __str__(self):
        txt = f"\nProcessador {self.id:>2} (Hits: {self.privateCache.hits:>4} - Miss: {self.privateCache.miss:>4}):"
        txt += "\n"
        txt += "\n".join(
            [
                f"[Linha {i}] {str(self.privateCache.memoria[i])} "
                for i in range(len(self.privateCache))
            ]
        )
        return txt
        # Processador 1 (Hits: 150 - Miss: 402):
        # [Linha 0] Endereço: a4512f34 - Estado: S
        # [Linha 1] Endereço: 00000000 - Estado: I
        # [Linha 2] Endereço: bc122312 - Estado: S
        # [Linha 3] Endereço: d9845678 - Estado: E

    def insereM(self, bloco):
        self.privateCache.insereM(bloco)

    def insereO(self, bloco):
        self.privateCache.insereO(bloco)

    def insereS(self, bloco):
        self.privateCache.insereS(bloco)

    def busca(self, endereco):
        print(f"buscando {hex(endereco)[2:]:0>8} na memoria")
        bloco = MemoriaPrincipal.busca(endereco)
        self.sharedCache.insere(bloco)
        return bloco

    def atualizaMemoria(self, bloco):
        if (linha := self.sharedCache[bloco]) is not None:
            # atualiza cache
            linha.bloco = bloco
        else:
            # atualiza MP
            MemoriaPrincipal.atualiza(bloco)


# Processador 0 (Hits: 232 - Miss: 320):
# [Linha 0] Endereço: b3212238 - Estado: S
# [Linha 1] Endereço: bc431221 - Estado: M
# [Linha 2] Endereço: bc122312 - Estado: I
# [Linha 3] Endereço: 00000000 - Estado: I


class Simulador:
    def __init__(self, qntdCpus, qntLinhas, tamLinha, algoritmoSubsitituicao):
        self.barramento = Barramento()
        self.sharedCache = Cache(qntdCpus * qntLinhas * 2, tamLinha)
        self.cpus = [
            Cpu(i, qntLinhas, tamLinha, self.sharedCache, self.barramento)
            for i in range(qntdCpus)
        ]

        self.barramento.cpus = self.cpus
        self.barramento.sharedCache = self.sharedCache

    def processar(self, op: Operacao):
        try:
            self.cpus[op.cpu].processar(op.instrucao, op.endereco)
        except IndexError as e:
            print(e)
            print(f"Operacao inválida, não há Processador {op.cpu}")
            return
        # talvez só checar aqui se *cpu* é um parametro valido com try catch
        # self.print()

    def __str__(self):
        txt = f"\n{' Caches Privadas ':-^45}"
        txt += "\n".join([str(cpu) for cpu in self.cpus])
        txt += "\n\n"
        txt += f"\n{' Cache Compartilhada ':-^45}\n"
        txt += str(self.sharedCache)
        return txt


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

        qntCpus = 2

        # mapeamento = associativo
        simulador = Simulador(qntCpus, numLinhasCache, tamLinha, algSubstituicaoCache)

    with open(argv[2]) as f:
        print(f"\nInício do Simulador - {argv[2]}")
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
            # =============================================

            # Operação: LEITURA - Processador 3 - Endereço: b8590400
            # Mensagem no barramento: Busca de dados (Read Miss)

            print("=" * 50)
            print()
            print(f"Linha {i:>3} - {operacao}")
            simulador.processar(operacao)
            print(simulador)
            print()
            i += 1


if __name__ == "__main__":
    main()
