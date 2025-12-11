from algoritmosSubstituicao import (
    algoritmoFIFO,
    algoritmoLFU,
    algoritmoLRU,
    algoritmoRAND,
)
from enums import Estado
from linha import Linha, LinhaPrivada


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
        return self._algoritmoDeSubstituicao(self)  # vai da errado?

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
        # self.memoria = [tipoLinha(tamLinha) for _ in range(qntLinhas)]

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

    def invalidate(self, endereco):
        if (linha := self[endereco]) is not None:
            linha.estado = Estado.I

    def insereM(self, bloco):
        self.insere(bloco).estado = Estado.M

    def insereE(self, bloco):
        self.insere(bloco).estado = Estado.E

    def insereS(self, bloco):
        self.insere(bloco).estado = Estado.S

    def insere(self, bloco) -> LinhaPrivada:
        print("inserindo...")
        for linha in self.memoria:
            if linha.estado == Estado.I:
                linha.bloco = bloco
                return linha

        # FIFO
        linha = self.memoria[self.aux]

        if linha.estado in [Estado.M, Estado.O]:
            self.atualizaMemoria(linha)

        self.memoria[self.aux].bloco = bloco
        self.aux = (self.aux + 1) % self.tamanho
        return self.memoria[self.aux]

    def atualizaMemoria(self, linha):
        self.cpu.atualizaMemoria(linha)


class MemoriaPrincipal:
    @staticmethod
    def busca(endereco: int, tamLinha) -> int:
        """
        "Busca" na memoria
        """
        return endereco - (endereco % tamLinha)

    @staticmethod
    def atualiza(endereco: int) -> int:
        """
        "Atualiza" o endereco de memoria
        """
        return endereco
