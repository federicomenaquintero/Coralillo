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
        
    def numero(self, valor):
        self.tipo = TipoToken.Numero
        self.valor_num = valor
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
        elif caracter == '*':
            tokens.append(Token().simple(TipoToken.Oper_Mul))
        elif caracter == '/':
            tokens.append(Token().simple(TipoToken.Oper_Div))
        elif caracter == '(':
            tokens.append(Token().simple(TipoToken.Paren_Izq))
        elif caracter == ')':
            tokens.append(Token().simple(TipoToken.Paren_Der))

        elif caracter == ' ':
            cursor += 1
            continue

        elif caracter not in CARACTERES_BUENOS:
            tokens.append(Token().error(cursor, "unexpected token"))
            return tokens
        
        else:
            principio = cursor
            while cursor < len(input_) and input_[cursor] in CARACTERES_BUENOS:
                cursor += 1
            
            num = int(input_[principio:cursor])
            tokens.append(Token().numero(num))
            continue

        cursor += 1

    return tokens
        
class Pruebas(unittest.TestCase):
    def test_no_hay_tokens(self):
        self.assertEqual(tokeniza(""), [])

    def test_tokeniza_tokens_simples(self):
        self.assertEqual(tokeniza("+ -*    / ()"), [ 
            Token().simple(TipoToken.Oper_Mas),
            Token().simple(TipoToken.Oper_Menos),
            Token().simple(TipoToken.Oper_Mul),
            Token().simple(TipoToken.Oper_Div),
            Token().simple(TipoToken.Paren_Izq),
            Token().simple(TipoToken.Paren_Der),
        ])
        
    def test_encuentra_token_no_esperado(self):
        tokens = tokeniza("1234hola")
        self.assertEqual(tokens, [ 
            Token().numero(1234), 
            Token().simple(TipoToken.Error) 
        ])
        self.assertEqual(tokens[1].error_pos, 4)
        self.assertEqual(tokens[1].error_msg, "unexpected token")
        
    def test_tokeniza_numero(self):
        tokens = tokeniza("1234")
        self.assertEqual(tokens, [ Token().numero(1234) ])
        self.assertEqual(tokens[0].valor_num, 1234)
        
        


unittest.main()
