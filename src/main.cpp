#include <iostream>
#include <fstream>

using namespace std;

int main(int arc, char* argv[]) {
    cout << endl;
    if (arc != 3) {
        cout << "Quantidade inesperada de argumentos" << endl;
        cout << "Entrada deve ser do tipo:" << endl;
        cout << "./simulador.exe config.data arquivo_de_entrada.data" << endl;
        return 1;
    }

    cout << endl;
    cout << arc << argv[arc-1] <<  " oshi";
    return 0;
}
