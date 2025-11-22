#include <iostream>
#include <fstream>
#include <cstdio>

using namespace std;

int main(int arc, char* argv[]) {
    cout << endl;
    if (arc != 3) {
        cout << "Quantidade inesperada de argumentos" << endl;
        cout << "Entrada deve ser do tipo:" << endl;
        cout << "./simulador.exe config.data arquivo_de_entrada.data" << endl;
        return 1;
    }


    ifstream instructionsFile(argv[2]);

    if (!instructionsFile.is_open()) {
        cerr << "Nao foi possível abrir o arquivo" << argv[2] << endl;
        return 1;
    }

    string instrucao;
    // int cpu, op, endereco;

    while (getline(instructionsFile, instrucao)) {
        cout << instrucao << endl;
        // sscanf(instrucao, "%u %u %x", cpu, op, endereco);
    }

    instructionsFile.close();
    return 0;
}
