from enums import Estado, Instrucao, Mensagem
from memoria import Cache, CachePrivada, MemoriaPrincipal


class Barramento:
    def __init__(self):
        self.cpus: list[Cpu]
        self.sharedCache: Cache

    def read(self, endereco, id):  # fix
        print(Mensagem.READ)
        bloco = None
        for cpu in self.cpus:
            if cpu.id == id:
                pass

            if (linha := cpu.privateCache[endereco]) is not None:
                bloco = linha.bloco
                if linha.estado in [Estado.O, Estado.M]:
                    linha.estado = Estado.O
                if linha.estado == Estado.E:
                    linha.estado = Estado.S

        return bloco

    def read_exclusive(self, endereco, id) -> int | None:
        print(Mensagem.READ_EXCLUSIVE)
        bloco = None
        for cpu in self.cpus:
            if cpu.id == id:
                pass

            if (linha := cpu.privateCache[endereco]) is not None:
                bloco = linha.bloco
                linha.estado = Estado.I
        return bloco

    def upgrade(self, endereco, id):
        print(Mensagem.UPGRADE)
        for cpu in self.cpus:
            if cpu.id != id:
                cpu.privateCache.invalidate(endereco)

    def invalidate(self, endereco, id):
        print(Mensagem.INVALIDATE)
        for cpu in self.cpus:
            if cpu.id != id:
                cpu.privateCache.invalidate(endereco)

    def readSharedCache(self, endereco):
        bloco = None
        if (linha := self.sharedCache[endereco]) is not None:
            bloco = linha.bloco

        return bloco


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
        self._tamLinha = tamLinha

    @property
    def tamLinha(self):
        return self._tamLinha

    # vamo tratar "bloco" como a informacao e "linha" como estrutura fisica
    # "O bloco X está na linha Y da cache"
    # "A linha Y contém o bloco X"
    def processar(self, instrucao, endereco):
        if (linha := self.privateCache[endereco]) is not None:
            self.privateCache.hits += 1
            if instrucao == Instrucao.ESCRITA_DADO:
                if linha.estado == Estado.S:
                    self.barramento.upgrade(endereco, self.id)
                elif linha.estado == Estado.O:
                    self.barramento.invalidate(endereco, self.id)
                else:  # estado M ou E
                    print(Mensagem.NENHUMA)
                linha.estado = Estado.M
            return

        # if bloco not in cachePrivado
        self.privateCache.miss += 1
        if instrucao == Instrucao.ESCRITA_DADO:
            # bloco = self.barramento.read_exclusive(endereco, self.id)
            # if bloco is None:
            #     bloco = self.barramento.readSharedCache(endereco)
            # if bloco is None:
            #     bloco = self.busca(endereco)

            # o que fica melhor??
            if (bloco := self.barramento.read_exclusive(endereco, self.id)) is None:
                if (bloco := self.barramento.readSharedCache(endereco)) is None:
                    bloco = self.busca(endereco)
            self.insereM(bloco)
            return

        # instrucao == Leitura
        if (bloco := self.barramento.read(endereco, self.id)) is None:
            if (bloco := self.barramento.readSharedCache(endereco)) is None:
                bloco = self.busca(endereco)
            self.insereE(bloco)
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

    def insereM(self, bloco):
        self.privateCache.insereM(bloco)

    def insereE(self, bloco):
        self.privateCache.insereE(bloco)

    def insereS(self, bloco):
        self.privateCache.insereS(bloco)

    def busca(self, endereco):
        print(f"buscando {hex(endereco)[2:]:0>8} na memoria")
        bloco = MemoriaPrincipal.busca(endereco, self.tamLinha)
        self.sharedCache.insere(bloco)
        return bloco

    def atualizaMemoria(self, bloco):
        if (linha := self.sharedCache[bloco]) is not None:
            # atualiza cache
            linha.bloco = bloco
        else:
            # atualiza MP
            MemoriaPrincipal.atualiza(bloco)
