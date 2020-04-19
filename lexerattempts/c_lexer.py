# My lexer attempt
import unittest, enum
from string import ascii_letters, digits

class TokenType(enum.Enum):
    Error =     -1
    Number =     0
    Identifier = 2
    
    Opr_Plus =  3 # +
    Opr_Min =   4 # -
    Opr_Star =  5 # *
    Opr_Slash = 6 # /
    Opr_Eq =    7 # =
    Opr_Not =   8 # !
    Opr_Ter =   9 # ?
    
    Opr_MThan = 10 # >
    Opr_LThan = 11 # <

    Sep_Dot =   12 # .
    Sep_Comm =  13 # ,
    Sep_DDot =  14 # :
    Sep_DCom =  15 # ;
    Sep_Quote = 16 # "

    Agr_LPar =  17 # (
    Agr_RPar =  18 # )
    
    Opr_PlusEq =  19 # +=
    Opr_MinEq =   20 # -=
    Opr_StarEq =  21 # *=
    Opr_SlashEq = 22 # /=
    Opr_NotEq =   23 # !=
    Opr_EqEq =    24 # ==

TOKEN_SYMBOLS = {
    '+': TokenType.Opr_Plus,
    '-': TokenType.Opr_Min,
    '*': TokenType.Opr_Star,
    '/': TokenType.Opr_Slash,
    '!': TokenType.Opr_Not,
    '=': TokenType.Opr_Eq,
    '?': TokenType.Opr_Ter,
    '>': TokenType.Opr_MThan,
    '<': TokenType.Opr_LThan,

    '.': TokenType.Sep_Dot,
    ':': TokenType.Sep_DDot,
    ',': TokenType.Sep_Comm,
    ';': TokenType.Sep_DCom,
    '"': TokenType.Sep_Quote,

    '(': TokenType.Agr_LPar,
    ')': TokenType.Agr_RPar, 
    
    '+=': TokenType.Opr_PlusEq,
    '-=': TokenType.Opr_MinEq,
    '*=': TokenType.Opr_StarEq,
    '/=': TokenType.Opr_SlashEq,
    '!=': TokenType.Opr_NotEq,
    '==': TokenType.Opr_EqEq,
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

    def quote(self, pos:int):
        self.type = TokenType.Sep_Quote
        self.pos = pos
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
            if current_char == '"':
                tokens.append(Token().quote(cursor))
                cursor += 1
                continue

            tokens.append(Token().simple(TOKEN_SYMBOLS[current_char]))

        elif current_char in VALID_IDENTIFIER_CHARS:
            first_pos = cursor
            while cursor < len(line) and line[cursor] in VALID_IDENTIFIER_CHARS:
                cursor += 1

            tokens.append(Token().indentifier(line[first_pos:cursor]))
            continue

        elif current_char in VALID_NUMBER_CHARS:
            first_pos = cursor
            while cursor < len(line) and line[cursor] in VALID_NUMBER_CHARS:
                cursor += 1

            num = int(line[first_pos:cursor])
            tokens.append(Token().number(num))
            continue

        elif current_char == ' ':
            cursor += 1
            continue

        else: # Error
            pass

        cursor += 1

    return tokens


class TokenTests(unittest.TestCase):
    def test_empty_token(self):
        tokens = tokenize('')
        expected = []
        
        self.assertEqual(tokens, expected)

    def test_single_operator_token(self):
        symbs = list(TOKEN_SYMBOLS)[0:16]

        for t in symbs:
            tokens = tokenize(t)
            expected = [Token().simple(TOKEN_SYMBOLS[t])]
            
            self.assertEqual(tokens, expected)

    def test_multiple_non_ligated_operator_separator_agrupation_tokens(self):
        tokens = tokenize('-.=:;+(<')
        expected = [
            Token().simple(TokenType.Opr_Min),
            Token().simple(TokenType.Sep_Dot),
            Token().simple(TokenType.Opr_Eq),
            Token().simple(TokenType.Sep_DDot),
            Token().simple(TokenType.Sep_DCom),
            Token().simple(TokenType.Opr_Plus),
            Token().simple(TokenType.Agr_LPar),
            Token().simple(TokenType.Opr_LThan),
        ]

        self.assertEqual(tokens, expected)

    def test_identifier_token(self):
        tokens = tokenize('Hola ')
        expected = [Token().indentifier('Hola')]

        self.assertEqual(tokens, expected)
        self.assertEqual(tokens[0].name, 'Hola')

    def test_number_token(self):
        tokens = tokenize('1234')
        expected = [Token().number(1234)]
        
        self.assertEqual(tokens, expected)

    def test_quote_tokens(self):
        tokens = tokenize('"Hola"')
        expected = [
            Token().quote(0),
            Token().indentifier('Hola'),
            Token().quote(5),
        ]

        self.assertEqual(tokens, expected)
        self.assertEqual(tokens[0].pos, 0)
        self.assertEqual(tokens[1].name, 'Hola')
        self.assertEqual(tokens[2].pos, 5)

if __name__ == "__main__":
    unittest.main()