import unittest
import enum

from string import digits

CARACTERES_BUENOS = tuple(digits)

class TipoToken(enum.Enum):
    Numero = 0
    Oper_Mas = 1
    Oper_Menos = 2
    Oper_Mul = 3
    Oper_Div = 4
    Paren_Izq = 5
    Paren_Der = 6
    Error = 7
    
class Token:
    def __eq__(self, other):
        return self.tipo == other.tipo

    def simple(self, tipo):
        self.tipo = tipo
        return self

    def error(self, posicion, mensaje):
        self.tipo = TipoToken.Error
        self.error_pos = posicion
        self.error_msg = mensaje
        return self

def tokeniza(input_: str):
    if len(input_) == 0:
        return []

    cursor = 0
    tokens = []
    while cursor < len(input_):
        caracter = input_[cursor:cursor + 1]

        if caracter == '+':
            tokens.append(Token().simple(TipoToken.Oper_Mas))
        elif caracter == '-':
            tokens.append(Token().simple(TipoToken.Oper_Menos))

        elif caracter == ' ':
            cursor += 1
            continue

        elif caracter not in CARACTERES_BUENOS:
            tokens.append(Token().error(cursor, "unexpected token"))
            return tokens

        cursor += 1

    return tokens
        
class Pruebas(unittest.TestCase):
    def test_no_hay_tokens(self):
        self.assertEqual(tokeniza(""), [])

    def test_tokeniza_un_operador(self):
        self.assertEqual(tokeniza("+"), [ Token().simple(TipoToken.Oper_Mas) ])

    def test_tokeniza_dos_operadores(self):
        self.assertEqual(tokeniza("+ -"), [ 
            Token().simple(TipoToken.Oper_Mas),
            Token().simple(TipoToken.Oper_Menos)
        ])
        
    def test_encuentra_token_no_esperado(self):
        tokens = tokeniza("+hola")
        self.assertEqual(tokens, [ 
            Token().simple(TipoToken.Oper_Mas), 
            Token().simple(TipoToken.Error) 
        ])
        self.assertEqual(tokens[1].error_pos, 1)
        self.assertEqual(tokens[1].error_msg, "unexpected token")


unittest.main()
