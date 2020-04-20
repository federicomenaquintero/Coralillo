# My lexer attempt
import unittest, enum
from string import ascii_letters, digits

class TokenType(enum.Enum):
    Error       = -1
    Comment     = 0
    Number      = 1
    Identifier  = 2
    String      = 3

    Opr_Plus    = 4 # +
    Opr_Min     = 5 # -
    Opr_Star    = 6 # *
    Opr_Slash   = 7 # /
    Opr_Eq      = 8 # =
    Opr_Not     = 9 # !
    Opr_Ter     = 10 # ?

    Opr_MThan   = 11 # >
    Opr_LThan   = 12 # <

    Sep_Dot     = 13 # .
    Sep_Comm    = 14 # ,
    Sep_DDot    = 15 # :
    Sep_DCom    = 16 # ;

    Agr_LPar    = 17 # (
    Agr_RPar    = 18 # )

    Opr_PlusEq  = 19 # +=
    Opr_MinEq   = 20 # -=
    Opr_StarEq  = 21 # *=
    Opr_SlashEq = 22 # /=
    Opr_NotEq   = 23 # !=
    Opr_EqEq    = 24 # ==

    LArrow      = 25 # ->

SINGLE_CHARACTER_SYMBOLS = {
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

    '(': TokenType.Agr_LPar,
    ')': TokenType.Agr_RPar,
}

MULTIPLE_CHARACTER_SYMBOLS = {
    '+=': TokenType.Opr_PlusEq,
    '-=': TokenType.Opr_MinEq,
    '*=': TokenType.Opr_StarEq,
    '/=': TokenType.Opr_SlashEq,
    '!=': TokenType.Opr_NotEq,
    '==': TokenType.Opr_EqEq,
    '->': TokenType.LArrow,
    '//': TokenType.Comment,
}

class ErrorMsgs(enum.Enum):
    UnexpectedChar = 0
    MissingQuote =   1


ERROR_MESSAGES = {
    ErrorMsgs.UnexpectedChar: "Unexpected Character",
    ErrorMsgs.MissingQuote: "Missing Quote"
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
        self.pos = pos
        self.msg = msg
        return self

    def number(self, value:int):
        self.type = TokenType.Number
        self.value = value
        return self

    def identifier(self, name:str):
        self.type = TokenType.Identifier
        self.name = name
        return self

    def string(self, s:str):
        self.type = TokenType.String
        self.string = s
        return self

def tokenize(line:str):
    tokens = []
    cursor = 0

    while cursor < len(line):
        current_char = line[cursor:cursor +1]

        if current_char == '"': # Strings
            _rm_line = line[cursor+1:]

            second_quote_pos = _rm_line.find('"')
            if second_quote_pos == -1: #Error
                tokens.append(Token().error(cursor, ERROR_MESSAGES[ErrorMsgs.MissingQuote]))
                break

            tokens.append(Token().string(_rm_line[:second_quote_pos]))

            cursor += second_quote_pos + 2
            continue

        elif current_char in SINGLE_CHARACTER_SYMBOLS.keys():
            if cursor < len(line): # Double char tokens
                next_char = line[cursor +1:cursor +2]

                if current_char + next_char in MULTIPLE_CHARACTER_SYMBOLS:
                    new_token_type = MULTIPLE_CHARACTER_SYMBOLS[current_char + next_char]
                    tokens.append(Token().simple(new_token_type))

                    if new_token_type == TokenType.Comment:
                        break

                    cursor += 2
                    continue

            tokens.append(Token().simple(SINGLE_CHARACTER_SYMBOLS[current_char]))
            cursor += 1

        elif current_char in VALID_IDENTIFIER_CHARS:
            first_pos = cursor
            while cursor < len(line) and line[cursor] in VALID_IDENTIFIER_CHARS:
                cursor += 1

            tokens.append(Token().identifier(line[first_pos:cursor]))

        elif current_char in VALID_NUMBER_CHARS:
            first_pos = cursor
            while cursor < len(line) and line[cursor] in VALID_NUMBER_CHARS:
                cursor += 1

            num = int(line[first_pos:cursor])
            tokens.append(Token().number(num))

        elif current_char == ' ':
            cursor += 1

        else: # Error
            tokens.append(Token().error(cursor, ERROR_MESSAGES[ErrorMsgs.UnexpectedChar]))
            break

    return tokens


class TokenTests(unittest.TestCase):
    def test_empty_token(self):
        tokens = tokenize('')
        expected = []

        self.assertEqual(tokens, expected)

    def test_single_character_token(self):
        symbs = tuple("+-*/!?=<>.,:;()")

        for t in symbs:
            tokens = tokenize(t)
            expected = [Token().simple(SINGLE_CHARACTER_SYMBOLS[t])]

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
        expected = [Token().identifier('Hola')]

        self.assertEqual(tokens, expected)
        self.assertEqual(tokens[0].name, 'Hola')

    def test_number_token(self):
        tokens = tokenize('1234')
        expected = [Token().number(1234)]

        self.assertEqual(tokens, expected)

    def test_string_tokens(self):
        tokens = tokenize('123 "Hola mundo" "hola"')
        expected = [
            Token().number(123),
            Token().string("Hola mundo"),
            Token().string("hola"),
        ]

        self.assertEqual(tokens, expected)

    def test_error_msg(self):
        tokens = tokenize('#')
        expected = [Token().error(0, ERROR_MESSAGES[ErrorMsgs.UnexpectedChar])]

        self.assertEqual(tokens, expected)
        self.assertEqual(tokens[0].pos, 0)
        self.assertEqual(tokens[0].msg, ERROR_MESSAGES[ErrorMsgs.UnexpectedChar])

    def test_double_char_tokens(self):
        symbs = list(MULTIPLE_CHARACTER_SYMBOLS.keys())

        for t in symbs:
            tokens = tokenize(t)
            expected = [Token().simple(MULTIPLE_CHARACTER_SYMBOLS[t])]

            self.assertEqual(tokens, expected)

    def test_comments(self):
        tokens = tokenize("1234 ho//la mi nombre es cris #")
        expected = [
            Token().number(1234),
            Token().identifier('ho'),
            Token().simple(TokenType.Comment),
        ]

        self.assertEqual(tokens, expected)

    def test_general(self):
        tokens = tokenize('Hola, "Esto es un string" -> 123 //')
        expected = [
            Token().identifier('Hola'),
            Token().simple(TokenType.Sep_Comm),
            Token().string("Esto es un string"),
            Token().simple(TokenType.LArrow),
            Token().number(123),
            Token().simple(TokenType.Comment),
        ]

        self.assertEqual(tokens, expected)

if __name__ == "__main__":
    unittest.main()
