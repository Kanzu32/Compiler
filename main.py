import sys
from sys import argv
import re

decrypt = ['NUM', 'ID', 'IF', 'ELSE', 'ELSEIF', 'ENDIF', 'FOR', 'TO', 'DO', 'WHILE', 'LOOP', 'LPAR', 'RPAR', 'PLUS',
           'MINUS', 'GREAT', 'LESS', 'EQUAL', 'MULTIPLY', 'DIVIDE', 'SEMICOLON', 'DOT', 'COMMA', 'PROGRAM', 'BEGIN',
           'END', 'ASSUME', 'DIM', 'VAR', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE', 'READ', 'OUTPUT', 'INT', 'FLOAT',
           'BOOL', 'EOF']


class Lexer:
    (NUM, ID, IF, ELSE, ELSEIF, ENDIF, FOR, TO, DO, WHILE, LOOP, LPAR, RPAR, PLUS, MINUS, GREAT, LESS,
     EQUAL, MULTIPLY, DIVIDE, SEMICOLON, DOT, COMMA, PROGRAM, BEGIN, END, ASSUME, DIM, VAR, AND, OR,
     NOT, TRUE, FALSE, READ, OUTPUT, INT, FLOAT, BOOL, EOF) = range(40)

    SYMBOLS = {';': SEMICOLON, '+': PLUS, '-': MINUS, '*': MULTIPLY, '/': DIVIDE, '>': GREAT, '<': LESS, '=': EQUAL,
               '.': DOT, ',': COMMA, '(': LPAR, ')': RPAR, '%': INT, "!": FLOAT, '$': BOOL}

    WORDS = {'if': IF, 'endif': ENDIF, 'else': ELSE, 'elseif': ELSEIF, 'for': FOR, 'to': TO, 'do': DO, 'while': WHILE,
             'loop': LOOP, 'begin': BEGIN, 'end': END, 'ass': ASSUME, 'dim': DIM, 'program': PROGRAM, 'var': VAR,
             'read': READ, 'output': OUTPUT, 'and': AND, 'or': OR, 'not': NOT, 'true': TRUE, 'false': FALSE}

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
        global inputFile
        self.char = inputFile.read(1)
        # self.char = sys.stdin.read(1)

    def next_token(self):
        self.value = None
        self.symbol = None
        while self.symbol is None:
            if len(self.char) == 0:
                self.symbol = Lexer.EOF
            elif self.char.isspace():
                self.getc()
            elif self.char in Lexer.SYMBOLS:
                self.symbol = Lexer.SYMBOLS[self.char]
                self.getc()
            elif self.char.isdigit():
                intval = 0
                while self.char.isdigit():
                    intval = intval * 10 + int(self.char)
                    self.getc()
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


source_path: str

if len(argv) > 1:
    source_path = argv[1]
else:
    source_path = "source.txt"

inputFile = open(source_path, 'r')

lex = Lexer()
while lex.symbol != Lexer.EOF:
    lex.next_token()
    if lex.symbol == Lexer.ID or lex.symbol == Lexer.NUM:
        print(decrypt[lex.symbol], lex.value)
    else:
        print(decrypt[lex.symbol])

# source_file: str = open(source_path, "r").read()
# tokens: list[str] = list(filter(None, re.split(" |\n|;", source_file)))
#
# for i in range(len(tokens)):
#     print(tokens[i], end=" | ")
