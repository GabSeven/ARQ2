from sys import argv

import toml
from simulador import Operacao, Simulador


def main():
    if len(argv) != 3:
        print("\nQuantidade inesperada de argumentos")
        print("Entrada deve ser do tipo:")
        print("python simulador.py config.data arquivo_de_entrada.data\n")
        return

    config = toml.load(argv[1])
    tamLinha = config["linha"]["tamanho"]
    numLinhasCache = config["cache"]["linhas"]
    algSubstituicaoCache = config["algoritmo"]
    qntCpus = config["cpu"]["quantidade"]
    # mapeamento = associativo

    simulador = Simulador(qntCpus, numLinhasCache, tamLinha, algSubstituicaoCache)

    with open(argv[2]) as f:
        print(f"\nInício do Simulador - {argv[2]}")
        print()
        i = 1
        while linha := f.readline():
            try:
                operacao = Operacao(linha.split())

            except ValueError as e:
                print(e)
                break

            print("=" * 50)
            print()
            print(f"Linha {i:>3} - {operacao}")

            simulador.processar(operacao)

            print(simulador)
            print()

            i += 1


if __name__ == "__main__":
    main()
