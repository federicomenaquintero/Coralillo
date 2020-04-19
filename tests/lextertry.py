# Vairiable names must start with a letter or _ and are alowed to have any visvible chatacter in them that's not an operator.
# A name ends when a space or an operator is found.

DIGITS = tuple('0123456789')
OPERATORS = (
    '+', '-', '/', '*',                 # Arithmetic
    '=', '+=', '-=', '*=', '/=',        # Assignment
    '!', '&&', '||',                    # Logic
    '==', '!=', '>', '<', '>=', '<=',   # Comparative
    '[', ']', '.',                      # Information retrieval
    '->',                               # Miscelaneous
    )
AGROUPATION_SYMBOLS = ('(', ')')
SEPARATORS = (',', ':', ';', ' ')
KEYWORDS = (
    'let', 'fn', 'context',
    'for', 'while', 'loop',
    'continue', 'break',
    'return'
)


def separate_line_by_separators(line:str):
    separated_line = []
    inside_parenthesis = False
    new_separation = ""

    i = 0
    while i < len(line):
        inside_parenthesis = not inside_parenthesis if line[i] == '\'' else inside_parenthesis
        
        if line[i] in SEPARATORS and not inside_parenthesis:
            if new_separation: separated_line.append(new_separation)
            if line[i] != ' ': separated_line.append(line[i])
            new_separation = ""
        else:
            new_separation += line[i]
        
        i += 1

    separated_line.append(new_separation)
    return separated_line

def separate_line_by_strings(space_separated_line:list):
    if type(space_separated_line) != list:
        raise ValueError(f'Function separate_line_by_strings expects a list, given: {type(space_separated_line)}')


    string_separated_expressions = []
    quote_count = 0
    inside_parenthesis = False

    for line_to_separate in space_separated_line:
        while True:
            quote_pos = line_to_separate.find('\'')

            if quote_pos == -1: break
            
            separated_slice = line_to_separate[:quote_pos]
            if inside_parenthesis: separated_slice = f'\'{separated_slice}\''
            if separated_slice: string_separated_expressions.append(separated_slice)
            
            inside_parenthesis = not inside_parenthesis
            quote_count += 1

            line_to_separate = line_to_separate[quote_pos+1:]
        
        string_separated_expressions.append(line_to_separate)

        if inside_parenthesis:
            raise ValueError("Uneven quote count.")

    return string_separated_expressions

def separate_line_by_operators(string_separated_line:str):
    cursor = 0
    while cursor < len(string_separated_line[0]):
        

def split_elements(line:str):

    # Separate by spaces ------------------------------------------- #
    line_separated_by_separators = separate_line_by_separators(line)
    # Separate by strings ------------------------------------------ #
    line_separated_by_strings = separate_line_by_strings(line_separated_by_separators)
    # -------------------------------------------------------------- #

    # print(line_separated_by_spaces)
    print(line_separated_by_strings)
    pass

line = "(11)-(\'212\'12\'12\'121) + \'Hola, me llamo Cris\'awdnajdn   a -> (1, 2,s 3)"
split_elements(line)