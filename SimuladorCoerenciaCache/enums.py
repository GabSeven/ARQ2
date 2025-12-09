from enum import Enum


class Estado(Enum):
    M = "Modified"
    O = "Owned"
    E = "Exclusive"
    S = "Shared"
    I = "Invalid"


# Mensagens do Barramento
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


class Instrucao(Enum):
    LEITURA_INSTRUCAO = 0
    LEITURA_DADO = 2
    ESCRITA_DADO = 3
