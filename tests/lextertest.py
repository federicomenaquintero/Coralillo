# Vairiable names must start with a letter or _ and are alowed to have any visvible chatacter in them that's not an operator.
# A name ends when a space or an operator is found.
from string import digits, ascii_letters

DIGITS = tuple(digits)
OPERATORS = (
    '+', '-', '/', '*',                 # Arithmetic
    '=', '+=', '-=', '*=', '/=',        # Assignment
    '!', '&&', '||',                    # Logic
    '==', '!=', '>', '<', '>=', '<=',   # Comparative
    '[', ']', '.',                      # Information retrieval
    )
AGROUPATION_SYMBOLS = ('(', ')')
SEPARATORS = (',', ':', ';')


def unintrusive_split(line:str):
    expressions = []
    e_begin = 0
    inside_parenthesis = False

    i = 0
    while i < len(line):
        inside_parenthesis = not inside_parenthesis if line[i] == '\"' or line[i] == '\'' else inside_parenthesis
        
        if not inside_parenthesis:
            if line[i] == ' ' and e_begin != i:
                expressions.append(line[e_begin:i])
                e_begin = i+1
            
            if line[i] in AGROUPATION_SYMBOLS or line[i] in OPERATORS or line[i] in SEPARATORS:
                if e_begin == i:
                    expressions.append(line[i])
                    e_begin = i+1
                else:
                    expressions.append(line[e_begin:i])
                    e_begin = i
        
        i += 1

    expressions.append(line[e_begin:i])
    return expressions


operation = "(11)+[-(2121212121)] + \'Hola, me llamo Cris\') a(1, 2, 3)"
print(unintrusive_split(operation))
