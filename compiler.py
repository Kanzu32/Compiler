import sys
from sys import argv
import re

decrypt = ['NUM', 'REAL', 'ID', 'IF', 'ELSE', 'ELSEIF', 'FOR', 'TO', 'DO', 'WHILE', 'LPAR', 'RPAR', 'PLUS',
           'MINUS', 'GREAT', 'GREATEQUAL', 'LESS', 'LESSEQUAL', 'EQUAL', 'NOTEQUAL', 'MULTIPLY', 'DIVIDE', 'SEMICOLON',
           'DOT', 'COMMA', 'BEGIN', 'END', 'ASSUME', 'DIM', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE', 'READ',
           'OUTPUT', 'INT', 'FLOAT', 'BOOL', 'EOF']


class Lexer:
    (NUM, REAL, ID, IF, ELSE, ELSEIF, FOR, TO, DO, WHILE, LPAR, RPAR, PLUS, MINUS, GREAT, GREATEQUAL, LESS, LESSEQUAL,
     EQUAL, NOTEQUAL, MULTIPLY, DIVIDE, SEMICOLON, DOT, COMMA, BEGIN, END, ASSUME, DIM, AND, OR,
     NOT, TRUE, FALSE, READ, OUTPUT, INT, FLOAT, BOOL, EOF) = range(40)

    SYMBOLS = {';': SEMICOLON, '+': PLUS, '-': MINUS, '*': MULTIPLY, '/': DIVIDE, '>': GREAT, '>=': GREATEQUAL, '<': LESS, '<=': LESSEQUAL, '=': EQUAL,
               '!=': NOTEQUAL, '.': DOT, ',': COMMA, '(': LPAR, ')': RPAR, '%': INT, "!": FLOAT, '$': BOOL}

    WORDS = {'if': IF, 'else': ELSE, 'elseif': ELSEIF, 'for': FOR, 'to': TO, 'do': DO, 'while': WHILE,
             'begin': BEGIN, 'end': END, 'ass': ASSUME, 'dim': DIM, 'read': READ,
             'output': OUTPUT, 'and': AND, 'or': OR, 'not': NOT, 'true': TRUE, 'false': FALSE}

    char = ' '

    def __init__(self):
        self.symbol = None
        self.value = None

    @staticmethod
    def error(msg):
        print('Lexer error: ', msg)
        sys.exit(1)

    # def error(self, msg):
    #     print('Lexer error: ', msg)
    #     sys.exit(1)

    def getc(self):
        global input_stream
        self.char = input_stream.read(1)
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
                if self.char in Lexer.SYMBOLS and self.char != Lexer.MINUS:
                    new_symbol += self.char
                    if new_symbol == '/*':
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
                        self.symbol = Lexer.SYMBOLS[self.char]
                        self.getc()
                else:
                    self.symbol = Lexer.SYMBOLS[new_symbol]
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
                    self.value = identifier  # !!!!
                else:
                    self.error('Unknown identifier: ' + identifier)
            else:
                self.error('Unexpected symbol: ' + self.char)


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

    lex = Lexer()
    while lex.symbol != Lexer.EOF:
        lex.next_token()
        if lex.symbol == Lexer.ID or lex.symbol == Lexer.NUM or lex.symbol == Lexer.REAL:
            print(decrypt[lex.symbol], lex.value)
        else:
            print(decrypt[lex.symbol])
