# My lexer attempt
import unittest, enum
from string import ascii_letters, digits

class TokenType(enum.Enum):
    Error =      -1
    Identifier = 0
    Number =     1
    
    Opr_Sum =   2 # +
    Opr_Sub =   3 # -
    Opr_Mul =   4 # *
    Opr_Div =   5 # /
    Opr_Eq =    6 # =
    Opr_Not =   7 # !
    Opr_Ter =   8 # ?
    
    Sep_Dot =    9 # .
    Sep_Comm =  10 # ,
    Sep_DDot =  11 # :
    Sep_DCom =  12 # ;

    Agr_LPar =  13 # (
    Agr_RPar =  14 # )

TOKEN_SYMBOLS = {
    '+': TokenType.Opr_Sum,
    '-': TokenType.Opr_Sub,
    '*': TokenType.Opr_Mul,
    '/': TokenType.Opr_Div,
    '=': TokenType.Opr_Eq,
    '!': TokenType.Opr_Not,
    '?': TokenType.Opr_Ter,

    '.': TokenType.Sep_Dot,
    ':': TokenType.Sep_DDot,
    ',': TokenType.Sep_Comm,
    ';': TokenType.Sep_DCom,

    '(': TokenType.Agr_LPar,
    ')': TokenType.Agr_RPar, 
}


VALID_IDENTIFIER_CHARS = tuple(ascii_letters + "_ñÑ")
VALID_NUMBER_CHARS = tuple(digits)

class Token:
    def __eq__(self, other):
        return self.type == other.type

    def __repr__(self):
        return str(self.type)

    def simple(self, _type:TokenType):
        self.type = _type
        return self

    def error(self, pos:int, msg:str):
        self.type = TokenType.Error
        self.error_pos = pos
        self.error_msg = msg
        return self

    def number(self, value:int):
        self.type = TokenType.Number
        self.value = value
        return self

    def indentifier(self, name:str):
        self.type = TokenType.Identifier
        self.name = name
        return self

def tokenize(line:str):

    tokens = []
    cursor = 0
    while cursor < len(line):
        current_char = line[cursor:cursor +1]
        
        if current_char in TOKEN_SYMBOLS.keys():
            tokens.append(Token().simple(TOKEN_SYMBOLS[current_char]))

        elif current_char in VALID_IDENTIFIER_CHARS:
            pass

        elif current_char in VALID_NUMBER_CHARS:
            pass

        elif current_char == ' ':
            cursor += 1
            continue

        else: # Error
            pass

        cursor += 1

    return tokens


print(tokenize('()'))

class TokenTests(unittest.TestCase):
    def test_empty_token(self):
        pass
