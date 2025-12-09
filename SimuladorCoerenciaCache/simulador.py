from cpu import Barramento, Cpu
from enums import Instrucao
from memoria import Cache


class Operacao:
    def __init__(self, elems: list[str]):
        self.cpu: int = int(elems[0])
        self.instrucao: Instrucao = Instrucao(int(elems[1]))
        self.endereco: int = int(elems[2], 16)

    def __str__(self):
        return f"Processador {self.cpu} - Endereço: {hex(self.endereco)[2:]:0>8}\nOperação: {Instrucao(self.instrucao).name:<17} "


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

    def __str__(self):
        txt = f"\n{' Caches Privadas ':-^45}"
        txt += "\n".join([str(cpu) for cpu in self.cpus])
        txt += "\n\n"
        txt += f"\n{' Cache Compartilhada ':-^45}\n"
        txt += str(self.sharedCache)
        return txt
