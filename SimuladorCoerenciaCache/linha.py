from enums import Estado


class Linha:
    def __init__(self, tamLinha):
        self.bloco: int = 0
        self._tamanho: int = tamLinha
        self.aux: int = 0  # parametro usado nos metodos de substituicao

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
