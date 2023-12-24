decrypt = ['NUM', 'REAL', 'ID', 'if', 'else', 'elseif', 'for', 'to', 'do', 'while', '(', ')', '+', '-',
           '>', '>=', '<', '<=', '=', '!=', '*', '/', ';', '.', ',', '{', '}', 'ass', 'dim', 'and', 'or',
           'not', 'BOOL_VAL', 'read', 'output', 'INT', 'FLOAT', 'BOOL', 'EOF']

decrypt_to_operators = ['NUM', 'NUM', 'ID', 'if', 'else', 'elseif', 'for', 'to', 'do', 'while', '(', ')', '+', '-',
                        '>', '>=', '<', '<=', '=', '!=', '*', '/', ';', '.', ',', '{', '}', 'ass', 'dim', 'and', 'or',
                        'not', 'BOOL', 'read', 'output', 'TYPE', 'TYPE', 'TYPE', '/e/']

decrypt_to_lexemes = ["NUM", "REAL", "ID", "IF", "ELSE", "ELSEIF", "FOR", "TO", "DO", "WHILE", "LPAR", "RPAR", "PLUS",
                      "MINUS", "GREAT", "GREAT_EQUAL", "LESS", "LESS_EQUAL", "EQUAL", "NOTEQUAL", "MULTIPLY", "DIVIDE",
                      "SEMICOLON", "DOT", "COMMA", "LBRA", "RBRA", "ASSIGN", "DIM", "AND", "OR", "NOT", "BOOL_VAL",
                      "READ", "OUTPUT", "INT", "FLOAT", "BOOL", "EOF"]


class Lexer:
    (NUM, REAL, ID, IF, ELSE, ELSEIF, FOR, TO, DO, WHILE, LPAR, RPAR, PLUS, MINUS, GREAT, GREAT_EQUAL, LESS, LESS_EQUAL,
     EQUAL, NOTEQUAL, MULTIPLY, DIVIDE, SEMICOLON, DOT, COMMA, LBRA, RBRA, ASSIGN, DIM, AND, OR,
     NOT, BOOL_VAL, READ, OUTPUT, INT, FLOAT, BOOL, EOF) = range(39)

    SYMBOLS = {';': SEMICOLON, '+': PLUS, '-': MINUS, '*': MULTIPLY, '/': DIVIDE, '>': GREAT, '>=': GREAT_EQUAL,
               '<': LESS, '<=': LESS_EQUAL, '=': EQUAL, '!=': NOTEQUAL, '.': DOT, ',': COMMA, '(': LPAR, ')': RPAR,
               '{': LBRA, '}': RBRA, '%': INT, "!": FLOAT, '$': BOOL}

    WORDS = {'if': IF, 'else': ELSE, 'elseif': ELSEIF, 'for': FOR, 'to': TO, 'do': DO, 'while': WHILE, 'ass': ASSIGN,
             'dim': DIM, 'read': READ, 'output': OUTPUT, 'and': AND, 'or': OR, 'not': NOT, 'true': BOOL_VAL, 'false': BOOL_VAL}

    char = ' '
    lines_count = 1

    def __init__(self, input_stream):
        self.symbol = None
        self.value = None
        self.input_stream = input_stream
        self.error = False
        self.error_msg = "Lexer: OK"

    def set_error(self, msg):
        self.error = True
        self.error_msg = "Lexer: " + msg


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
                double_symbol = new_symbol + self.char
                if new_symbol == '-':
                    if self.char.isdigit():
                        intval = int(self.char)
                        self.getc()
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
                            self.value = -(intval + floatval)
                            self.symbol = Lexer.REAL
                        else:
                            self.value = -intval
                            self.symbol = Lexer.NUM
                    else:
                        self.symbol = Lexer.SYMBOLS[new_symbol]
                elif double_symbol in Lexer.SYMBOLS:
                    self.symbol = Lexer.SYMBOLS[double_symbol]
                    self.getc()
                elif double_symbol == '/*':
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
            elif 'a' <= self.char <= 'z':
                identifier = ''
                while 'a' <= self.char <= 'z':
                    identifier += self.char.lower()
                    self.getc()
                if identifier in Lexer.WORDS:
                    self.symbol = Lexer.WORDS[identifier]
                    if identifier == "false":
                        self.value = False
                    elif identifier == "true":
                        self.value = True
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
    source_path = "source.txt"

    stream = open(source_path, 'r')

    lex = Lexer(stream)
    while lex.symbol != Lexer.EOF:
        lex.next_token()
        if lex.error:
            print(lex.error_msg)
            break
        elif lex.symbol == Lexer.ID or lex.symbol == Lexer.NUM or lex.symbol == Lexer.REAL:
            print(decrypt[lex.symbol], lex.value)
        else:
            print(decrypt[lex.symbol])
        # print(decrypt_to_operators[lex.symbol], end=" ")

