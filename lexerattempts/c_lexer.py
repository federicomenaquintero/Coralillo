# My lexer attempt
import unittest
from enum import Enum, auto
from string import ascii_letters, digits

class TokenType(Enum):
    Error       = auto()
    Comment     = auto()
    Number      = auto()
    Identifier  = auto()
    String      = auto()

    Opr_Plus    = auto() # +
    Opr_Min     = auto() # -
    Opr_Star    = auto() # *
    Opr_Slash   = auto() # /
    Opr_Eq      = auto() # =
    Opr_Not     = auto() # !
    Opr_Ter     = auto() # ?

    Opr_MThan   = auto() # >
    Opr_LThan   = auto() # <

    Sep_Dot     = auto() # .
    Sep_Comm    = auto() # ,
    Sep_DDot    = auto() # :
    Sep_DCom    = auto() # ;

    Agr_LPar    = auto() # (
    Agr_RPar    = auto() # )

    Opr_PlusEq  = auto() # +=
    Opr_MinEq   = auto() # -=
    Opr_StarEq  = auto() # *=
    Opr_SlashEq = auto() # /=
    Opr_NotEq   = auto() # !=
    Opr_EqEq    = auto() # ==

    LArrow      = auto() # ->

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

class ErrorMsgs(Enum):
    UnexpectedChar     = auto()
    MissingQuote       = auto()
    UnterminatedEscape = auto()
    InvalidEscape      = auto()

ERROR_MESSAGES = {
    ErrorMsgs.UnexpectedChar: "Unexpected Character",
    ErrorMsgs.MissingQuote: "Missing Quote",
    ErrorMsgs.UnterminatedEscape: "Unterminated escape",
    ErrorMsgs.InvalidEscape: "Invalid escape character, only \" and \\ are valid",
}

VALID_IDENTIFIER_CHARS = tuple(ascii_letters + "_ñÑ")
VALID_NUMBER_CHARS = tuple(digits)

class Token:
    def __eq__(self, other):
        if self.type != other.type:
            return False
        elif self.type in SINGLE_CHARACTER_SYMBOLS.values():
            return True
        elif self.type in MULTIPLE_CHARACTER_SYMBOLS.values():
            return True
        elif self.type == TokenType.Error:
            return self.pos == other.pos and self.msg == other.msg
        elif self.type == TokenType.Comment:
            # We don't store the contents of comments, so all comments are equivalent
            return True
        elif self.type == TokenType.Number:
            return self.value == other.value
        elif self.type == TokenType.Identifier:
            return self.name == other.name
        elif self.type == TokenType.String:
            return self.svalue == other.svalue
        else:
            # Return False in case we forget to add another case above
            # if we add another TokenType
            return False

    def __repr__(self):
        s = str(self.type)
        if self.type == TokenType.Error:
            s += ": pos=%s msg=%s" % (self.pos, self.msg)
        elif self.type == TokenType.Number:
            s += ": value=%s" % self.value
        elif self.type == TokenType.Identifier:
            s += ": name=%s" % self.name
        elif self.type == TokenType.String:
            s += ": svalue=%s" % self.svalue

        return s

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
        self.svalue = s
        return self

# Reads a string token.  Assumes the line starts with a " character.
#
# Returns a tuple (token, n_skip)
#
# If the line has a valid string token, this function returns a token
# with Token.type = TokenType.String, and n_skip with the number of
# characters that must be skipped over to find the next token.
#
# If the line does not have a valid string token, this function
# returns a token with Token.type = TokenType.Error, and n_skip will
# have a useless value.
def consume_string(line: str, start_pos: int):
    first = line[0]
    assert(first == '"')

    in_escape = False

    result = ""

    for idx, ch in enumerate(line[1:]):
        if in_escape:
            if ch == '\\' or ch == '"':
                result += ch
                in_escape = False
            else:
                return Token().error(start_pos + idx + 1, ERROR_MESSAGES[ErrorMsgs.InvalidEscape]), -1
        elif ch == '\\':
            in_escape = True
        elif ch == '"':
            return Token().string(result), idx + 2
        else:
            result += ch

    # If we got here, there is an error

    if in_escape:
        return Token().error(start_pos + idx + 1, ERROR_MESSAGES[ErrorMsgs.UnterminatedEscape]), -1
    else:
        return Token().error(start_pos, ERROR_MESSAGES[ErrorMsgs.MissingQuote]), -1

def tokenize(line:str):
    tokens = []
    cursor = 0

    while cursor < len(line):
        current_char = line[cursor:cursor +1]
        next_char = line[cursor + 1:cursor + 2]

        if current_char == '"': # Strings
            token, n_skip = consume_string(line[cursor:], cursor)
            tokens.append(token)
            if token.type == TokenType.String:
                cursor += n_skip
            else:
                # an error was detected
                break

        elif current_char + next_char in MULTIPLE_CHARACTER_SYMBOLS:
            token = Token().simple(MULTIPLE_CHARACTER_SYMBOLS[current_char + next_char])
            tokens.append(token)

            if token.type == TokenType.Comment:
                break

            cursor += 2

        elif current_char in SINGLE_CHARACTER_SYMBOLS:
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

class TokenEqTests(unittest.TestCase):
    def test_different_tokens(self):
        self.assertNotEqual(Token().identifier("hola"), Token().identifier("mundo"))
        self.assertNotEqual(Token().number(123), Token().number(456))
        self.assertNotEqual(Token().number(1), Token().simple(TokenType.Opr_Plus))
        self.assertNotEqual(Token().simple(TokenType.Opr_Plus), Token().simple(TokenType.Opr_Min))
        self.assertNotEqual(Token().string("hola"), Token().string("mundo"))
        self.assertNotEqual(Token().error(1, "hola"), Token().error(2, "hola"))
        self.assertNotEqual(Token().error(1, "hola"), Token().error(1, "mundo"))

    def test_equal_tokens(self):
        self.assertEqual(Token().simple(TokenType.Opr_Plus), Token().simple(TokenType.Opr_Plus))
        self.assertEqual(Token().number(123), Token().number(123))
        self.assertEqual(Token().identifier("hola"), Token().identifier("hola"))
        self.assertEqual(Token().string("hola"), Token().string("hola"))
        self.assertEqual(Token().error(2, "hola"), Token().error(2, "hola"))

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

    def test_number_token(self):
        tokens = tokenize('1234')
        expected = [Token().number(1234)]

        self.assertEqual(tokens, expected)

    def test_string_with_missing_quote(self):
        tokens = tokenize('"hola')
        expected = [
            Token().error(0, ERROR_MESSAGES[ErrorMsgs.MissingQuote])
        ]
        self.assertEqual(tokens, expected)

        tokens = tokenize(r'"hola \"')
        expected = [
            Token().error(0, ERROR_MESSAGES[ErrorMsgs.MissingQuote])
        ]
        self.assertEqual(tokens, expected)

    def test_string_with_unterminated_escape(self):
        tokens = tokenize('"hola\\')
        expected = [
            Token().error(5, ERROR_MESSAGES[ErrorMsgs.UnterminatedEscape])
        ]
        self.assertEqual(tokens, expected)

    def test_string_with_invalid_escape(self):
        tokens = tokenize(r'"hola\q"')
        expected = [
            Token().error(6, ERROR_MESSAGES[ErrorMsgs.InvalidEscape])
        ]
        self.assertEqual(tokens, expected)

    def test_string_tokens(self):
        tokens = tokenize(r'123 "Hola mundo" "hola \"mundo\" \\\\"')
        expected = [
            Token().number(123),
            Token().string("Hola mundo"),
            Token().string(r'hola "mundo" \\'),
        ]

        self.assertEqual(tokens, expected)

    def test_error_msg(self):
        tokens = tokenize('#')
        expected = [Token().error(0, ERROR_MESSAGES[ErrorMsgs.UnexpectedChar])]

        self.assertEqual(tokens, expected)

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
