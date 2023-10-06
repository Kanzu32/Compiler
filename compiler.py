import sys
from sys import argv

decrypt = ['NUM', 'REAL', 'ID', 'IF', 'ELSE', 'ELSEIF', 'FOR', 'TO', 'DO', 'WHILE', 'LPAR', 'RPAR', 'PLUS',
           'MINUS', 'GREAT', 'GREAT_EQUAL', 'LESS', 'LESS_EQUAL', 'EQUAL', 'NOTEQUAL', 'MULTIPLY', 'DIVIDE',
           'SEMICOLON', 'DOT', 'COMMA', 'BEGIN', 'END', 'ASSUME', 'DIM', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE', 'READ',
           'OUTPUT', 'INT', 'FLOAT', 'BOOL', 'EOF']


class Lexer:
    (NUM, REAL, ID, IF, ELSE, ELSEIF, FOR, TO, DO, WHILE, LPAR, RPAR, PLUS, MINUS, GREAT, GREAT_EQUAL, LESS, LESS_EQUAL,
     EQUAL, NOTEQUAL, MULTIPLY, DIVIDE, SEMICOLON, DOT, COMMA, BEGIN, END, ASSUME, DIM, AND, OR,
     NOT, TRUE, FALSE, READ, OUTPUT, INT, FLOAT, BOOL, EOF) = range(40)

    SYMBOLS = {';': SEMICOLON, '+': PLUS, '-': MINUS, '*': MULTIPLY, '/': DIVIDE, '>': GREAT, '>=': GREAT_EQUAL,
               '<': LESS, '<=': LESS_EQUAL, '=': EQUAL, '!=': NOTEQUAL, '.': DOT, ',': COMMA, '(': LPAR, ')': RPAR,
               '%': INT, "!": FLOAT, '$': BOOL}

    WORDS = {'if': IF, 'else': ELSE, 'elseif': ELSEIF, 'for': FOR, 'to': TO, 'do': DO, 'while': WHILE,
             'begin': BEGIN, 'end': END, 'ass': ASSUME, 'dim': DIM, 'read': READ,
             'output': OUTPUT, 'and': AND, 'or': OR, 'not': NOT, 'true': TRUE, 'false': FALSE}

    char = ' '
    lines_count = 1

    def __init__(self, input_stream):
        self.symbol = None
        self.value = None
        self.input_stream = input_stream
        self.error = False
        self.error_msg = "OK"

    def set_error(self, msg):
        print("ggg")
        self.error = True
        self.error_msg = "Lexer error: " + msg

    # def error(self, msg):
    #     print('Lexer error: ', msg)
    #     sys.exit(1)

    def getc(self):
        self.char = self.input_stream.read(1)
        if self.char == "\n":
            self.lines_count += 1
        # self.char = sys.stdin.read(1)
# /* */ != <= >=
    def next_token(self):
        self.value = None
        self.symbol = None
        while self.symbol is None:
            if len(self.char) == 0:
                self.symbol = Lexer.EOF
            elif self.char.isspace():
                self.getc()
            elif self.char in Lexer.SYMBOLS:
                new_symbol = self.char
                self.getc()
                new_symbol += self.char
                if new_symbol in Lexer.SYMBOLS:
                    self.symbol = Lexer.SYMBOLS[new_symbol]
                    self.getc()
                elif new_symbol == '/*':
                    out_char = ''
                    while out_char != '*/':
                        self.getc()
                        if len(self.char) == 0:
                            self.symbol = Lexer.EOF
                            break
                        out_char += self.char
                        if out_char == '*' or out_char == '*/':
                            continue
                        out_char = ''
                    self.getc()
                else:
                    self.symbol = Lexer.SYMBOLS[new_symbol[0]]
            elif self.char.isdigit():
                intval = 0
                while self.char.isdigit():
                    intval = intval * 10 + int(self.char)
                    self.getc()
                if self.char == '.':
                    floatval = 0
                    count = 1
                    self.getc()
                    while self.char.isdigit():
                        floatval = floatval + int(self.char) / (10 ** count)
                        count += 1
                        self.getc()
                    self.value = intval + floatval
                    self.symbol = Lexer.REAL
                else:
                    self.value = intval
                    self.symbol = Lexer.NUM
            elif self.char.isalpha():
                identifier = ''
                while self.char.isalpha():
                    identifier += self.char.lower()
                    self.getc()
                if identifier in Lexer.WORDS:
                    self.symbol = Lexer.WORDS[identifier]
                elif len(identifier) == 2 and self.char.isdigit():
                    identifier += self.char
                    self.getc()
                    while self.char.isdigit():
                        identifier += self.char
                        self.getc()
                    self.symbol = Lexer.ID
                    self.value = identifier
                else:
                    self.set_error('Unknown identifier "' + identifier + '" in line ' + str(self.lines_count))
                    break
            else:
                self.set_error('Unexpected symbol "' + self.char + '" in line ' + str(self.lines_count))
                break


# source_file: str = open(source_path, "r").read()
# tokens: list[str] = list(filter(None, re.split(" |\n|;", source_file)))
#
# for i in range(len(tokens)):
#     print(tokens[i], end=" | ")


if __name__ == "__main__":
    source_path: str

    if len(argv) > 1:
        source_path = argv[1]
    else:
        source_path = "source.txt"

    input_stream = open(source_path, 'r')

    lex = Lexer(input_stream)
    while lex.symbol != Lexer.EOF:
        lex.next_token()
        if lex.symbol == Lexer.ID or lex.symbol == Lexer.NUM or lex.symbol == Lexer.REAL:
            print(decrypt[lex.symbol], lex.value)
        else:
            print(decrypt[lex.symbol])

