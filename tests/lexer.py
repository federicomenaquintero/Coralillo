import unittest
import enum

class TipoToken(enum.Enum):
    Numero = 0
    Oper_Mas = 1
    Oper_Menos = 2
    Oper_Mul = 3
    Oper_Div = 4
    Paren_Izq = 5
    Paren_Der = 6

def tokeniza(input_: str):
    if len(input_) == 0:
        return []

    cursor = 0
    tokens = []
    while cursor < len(input_):
        if input_[cursor:cursor + 1] == '+':
            tokens.append(TipoToken.Oper_Mas)

        cursor += 1

    return tokens
        
class Pruebas(unittest.TestCase):
    def test_no_hay_tokens(self):
        self.assertEqual(tokeniza(""), [])

    def test_tokeniza_un_operador(self):
        self.assertEqual(tokeniza("+"), [ TipoToken.Oper_Mas ])

unittest.main()
