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

class Pruebas(unittest.TestCase):
    def test_no_hay_tokens(self):
        self.assertEqual(tokeniza(""), [])
        
unittest.main()
