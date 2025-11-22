import io
from sys import argv


class Cpu:
    def __init__(self):
        self.status = "A"

class Cache:
    def __init__(self):
        self.

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

        numProcessadores = 1

        # mapeamento = associativo

    with open(argv[2]) as f:
        cpus: list[Cpu]
        for _ in range(numProcessadores):
            cpus.append(Cpu())

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

            cpus[cpu]

            print(elems)
            i += 1


if __name__ == "__main__":
    main()
