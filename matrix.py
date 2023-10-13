from enum import Enum


class ORDER(Enum):
    PRECEDED = 1
    FOLLOWS = 2
    EQUALS = 3


class LastSymbols:
    def __init__(self):
        self.left = {}
        self.right = {}

    def __eq__(self, other):
        if isinstance(other, LastSymbols):
            return self.left == other.left and self.right == other.right
        return NotImplemented


class MatrixGenerator:
    SYMBOLS = []

    WORDS = []

    T = []

    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.operator_matrix = {}
        self.error = False
        self.error_msg = "OK"
        self.rules = {}
        self.lr = LastSymbols()


    def set_error(self, msg):
        self.error = True
        self.error_msg = "Matrix generator: " + msg

    def generate(self):
        rule_names = input_stream.readline().split()
        MatrixGenerator.SYMBOLS = input_stream.readline().split()
        MatrixGenerator.WORDS = input_stream.readline().split()
        MatrixGenerator.T = [*MatrixGenerator.SYMBOLS, *MatrixGenerator.WORDS]
        symbols_lr = LastSymbols()
        words_lr = LastSymbols()
        for name in rule_names:  # инициализация имён
            self.rules[name] = []
            self.lr.left[name] = []
            self.lr.right[name] = []
            symbols_lr.left[name] = []
            symbols_lr.right[name] = []
            words_lr.left[name] = []
            words_lr.right[name] = []

        for symbol in ["/begin/", *MatrixGenerator.SYMBOLS, *MatrixGenerator.WORDS, "/end/"]:
            self.operator_matrix[symbol] = {}

        lines = input_stream.read().split('\n')  # заполнение правил вывода
        for line in lines:
            last_token_index = 0
            tokens = line.split()
            if tokens[1] == ":" and tokens[0] in rule_names and len(tokens) > 2:
                rule_name = tokens[0]
                tokens = tokens[2:]
                for i in range(len(tokens)):
                    if tokens[i] == "|":
                        self.rules[rule_name].append(tokens[last_token_index:i])
                        last_token_index = i+1
                    elif tokens[i] not in MatrixGenerator.SYMBOLS and tokens[i] not in MatrixGenerator.WORDS and tokens[i] not in rule_names:
                        self.set_error('unknown symbol "' + tokens[i] + '"')
                        return self.error
                self.rules[rule_name].append(tokens[last_token_index:])
            else:
                self.set_error("wrong file formatting")
                return self.error

        for rule_name in self.rules.keys():  # начальное заполнение крайних левых, правых
            for arr in self.rules[rule_name]:
                first_word = None
                last_word = None
                first_symbol = None
                last_symbol = None
                for item in arr:
                    if item in MatrixGenerator.SYMBOLS or item in self.rules.keys():
                        if first_symbol is None:
                            first_symbol = item
                            last_symbol = item
                        else:
                            last_symbol = item
                    else:
                        if first_word is None:
                            first_word = item
                            last_word = item
                        else:
                            last_word = item

                if last_word is not None:
                    if first_word not in words_lr.left[rule_name]:
                        words_lr.left[rule_name].append(first_word)
                    if last_word not in words_lr.right[rule_name]:
                        words_lr.right[rule_name].append(last_word)

                if last_symbol is not None:
                    if first_symbol not in symbols_lr.left[rule_name]:
                        symbols_lr.left[rule_name].append(first_symbol)
                    if last_symbol not in symbols_lr.right[rule_name]:
                        symbols_lr.right[rule_name].append(last_symbol)

        changed = True
        while changed:  # алгоритм для терм симв
            changed = False
            for rule_name in self.rules.keys():
                for item in symbols_lr.left[rule_name]:
                    if item in self.rules.keys():
                        for i in symbols_lr.left[item]:
                            if i not in symbols_lr.left[rule_name]:
                                symbols_lr.left[rule_name].append(i)
                                changed = True

                for item in symbols_lr.right[rule_name]:
                    if item in self.rules.keys():
                        for i in symbols_lr.right[item]:
                            if i not in symbols_lr.right[rule_name]:
                                symbols_lr.right[rule_name].append(i)
                                changed = True

        changed = True
        while changed:  # алгоритм для нетерм симв
            changed = False
            for rule_name in self.rules.keys():
                for item in symbols_lr.left[rule_name]:
                    if item in self.rules.keys():
                        for i in words_lr.left[item]:
                            if i not in words_lr.left[rule_name]:
                                words_lr.left[rule_name].append(i)
                                changed = True
                self.lr.left[rule_name] = [*symbols_lr.left[rule_name], *words_lr.left[rule_name]]

                for item in symbols_lr.right[rule_name]:
                    if item in self.rules.keys():
                        for i in words_lr.right[item]:
                            if i not in words_lr.right[rule_name]:
                                words_lr.right[rule_name].append(i)
                                changed = True
                self.lr.right[rule_name] = [*symbols_lr.right[rule_name], *words_lr.right[rule_name]]

        # print(MatrixGenerator.SYMBOLS)
        # print(MatrixGenerator.WORDS)
        # print(symbols_lr.left)
        # print(symbols_lr.right)
        # print(words_lr.left)
        # print(words_lr.right)
        #
        # print(self.rules)
        # print("LEFT: ")
        # print(self.lr.left["S"])
        # print("\nRIGHT: ")
        # print(self.lr.right["S"])
        # print(len(MatrixGenerator.ALL_LANG_SYMBOLS))
        # passed = []
        # for rule_name in self.rules.keys():  # начало, символы, слова, конец (из полей)
        #     for rule in self.rules[rule_name]:
        #         if rule not in passed:
        #             self.operator_matrix.append([])
        #             for search_rule_name in self.rules.keys():
        #                 for search_item in range(len(self.rules[rule_name])):
        #                     if self.rules[search_rule_name][search_item] == rule:
        #                         pass # слева справа

        # for symbol in ["/begin/", *MatrixGenerator.SYMBOLS, *MatrixGenerator.WORDS, "/end/"]:  # end begin
        #     for rule in self.rules.values():
        #         for item in rule:
        #             for i in range(len(item)):
        #                 if symbol == item[i]:
        #                     if i < len(item)-2 and symbol in MatrixGenerator.SYMBOLS:
        #
        #                         if item[i+2] in MatrixGenerator.SYMBOLS:
        #                             self.operator_matrix[symbol][item[i+2]] = ORDER.EQUALS
        #                         elif item[i+2] in self.rules.keys():
        #                             for s in self.lr.left[item[i+2]]:
        #                                 if s in MatrixGenerator.SYMBOLS:
        #                                     self.operator_matrix[symbol][s] = ORDER.EQUALS
        #                                     print("ПОПАЛ? ХУЙ ЗНАЕТ")
        #                                     if (self.operator_matrix[symbol].get(item[i + 2]) is not None) and not(self.operator_matrix[symbol][item[i + 2]] == ORDER.EQUALS):
        #                                         print("ХУЙНЯ ПЕРЕДЕЛЫВАЙ РАВНО КСТААА", symbol, item[i + 2], "СПРАВА")
        #
        #                         if item[i+1] in MatrixGenerator.SYMBOLS:
        #                             self.operator_matrix[symbol][item[i+1]] = ORDER.EQUALS
        #                             continue
        #                         elif item[i+1] in self.rules.keys():
        #                             for s in self.lr.left[item[i+1]]:
        #                                 if s in MatrixGenerator.SYMBOLS:
        #                                     self.operator_matrix[symbol][s] = ORDER.EQUALS
        #                                     if (self.operator_matrix[symbol].get(item[i + 1]) is not None) and not(self.operator_matrix[symbol][item[i + 1]] == ORDER.EQUALS):
        #                                         print("ХУЙНЯ ПЕРЕДЕЛЫВАЙ РАВНО КСТААА", symbol, item[i + 1], "СПРАВА")
        #                             continue
        #
        #                     if i > 0:
        #                         if item[i-1] in self.rules.keys():
        #                             for R in self.lr.right[item[i-1]]:
        #                                 if R not in self.rules.keys():
        #                                     if (self.operator_matrix[symbol].get(R) is not None) and not(self.operator_matrix[symbol][R] == ORDER.FOLLOWS):
        #                                         print("ХУЙНЯ ПЕРЕДЕЛЫВАЙ", symbol, R, "СПРАВА")
        #                                     self.operator_matrix[symbol][R] = ORDER.FOLLOWS
        #                         else:
        #                             if (self.operator_matrix[symbol].get(item[i-1]) is not None) and not (self.operator_matrix[symbol][item[i-1]] == ORDER.FOLLOWS):
        #                                 print("ХУЙНЯ ПЕРЕДЕЛЫВАЙ", symbol, item[i-1], "СПРАВА")
        #                             self.operator_matrix[symbol][item[i-1]] = ORDER.FOLLOWS
        #                     if i < len(item)-1:
        #                         if item[i+1] in self.rules.keys():
        #                             for L in self.lr.left[item[i+1]]:
        #                                 if L not in self.rules.keys():
        #                                     if (self.operator_matrix[symbol].get(L) is not None) and not (self.operator_matrix[symbol][L] == ORDER.PRECEDED):
        #                                         print("ХУЙНЯ ПЕРЕДЕЛЫВАЙ", symbol, L, "СЛЕВА")
        #                                     self.operator_matrix[symbol][L] = ORDER.PRECEDED
        #                         else:
        #                             if (self.operator_matrix[symbol].get(item[i+1]) is not None) and not (self.operator_matrix[symbol][item[i+1]] == ORDER.PRECEDED):
        #                                 print("ХУЙНЯ ПЕРЕДЕЛЫВАЙ", symbol, i+1, "СЛЕВА")
        #                             self.operator_matrix[symbol][item[i+1]] = ORDER.PRECEDED

        for symbol in MatrixGenerator.T:
            for rule in self.rules.values():
                for item in rule:
                    for i in range(len(item)):
                        if symbol == item[i]:

                            if i < len(item)-1 and item[i+1] in MatrixGenerator.T:  # x ai b y
                                if self.operator_matrix[symbol].get(item[i+1]) is not None and self.operator_matrix[symbol][item[i+1]] != ORDER.EQUALS:
                                    print("ОШИБКА", item[i:i+2], "x ai b y")
                                self.operator_matrix[symbol][item[i+1]] = ORDER.EQUALS
                            elif i < len(item)-2 and item[i+1] not in MatrixGenerator.T and item[i+2] in MatrixGenerator.T:  # x ai U b y
                                if self.operator_matrix[symbol].get(item[i+2]) is not None and self.operator_matrix[symbol][item[i+2]] != ORDER.EQUALS:
                                    print("ОШИБКА", item[i:i+3], "x ai U b y")
                                self.operator_matrix[symbol][item[i+2]] = ORDER.EQUALS

                            if i < len(item)-1 and item[i+1] not in MatrixGenerator.T:  # x ai U y
                                for L in self.lr.left[item[i+1]]:
                                    if L in MatrixGenerator.T:
                                        if self.operator_matrix[symbol].get(item[i + 1]) is not None and self.operator_matrix[symbol][item[i + 1]] != ORDER.PRECEDED:
                                            print("ОШИБКА", L, item[i:i + 2], "x ai U y")
                                        self.operator_matrix[symbol][L] = ORDER.PRECEDED
                                        continue

                            if i > 0 and item[i-1] not in MatrixGenerator.T:  # x U ai y
                                for R in self.lr.right[item[i-1]]:
                                    if R in MatrixGenerator.T:
                                        if self.operator_matrix[symbol].get(item[i - 1]) is not None and self.operator_matrix[symbol][item[i - 1]] != ORDER.FOLLOWS:
                                            print("ОШИБКА", R, item[i - 1:i + 1], "x U ai y")
                                        self.operator_matrix[symbol][R] = ORDER.FOLLOWS
                                        continue



        print("      ", end="")
        for x in MatrixGenerator.T:
            print("{0:<6}".format(x), end="")
        print()
        for i in MatrixGenerator.T:
            print("{0:<6}".format(i), end="")

            for j in MatrixGenerator.T:
                if self.operator_matrix[i].get(j) is None:
                    print(".     ", end="")
                elif self.operator_matrix[i][j] == ORDER.PRECEDED:
                    print("PRE   ", end="")
                elif self.operator_matrix[i][j] == ORDER.EQUALS:
                    print("EQ    ", end="")
                elif self.operator_matrix[i][j] == ORDER.FOLLOWS:
                    print("FOL   ", end="")

            print()




if __name__ == "__main__":
    source_path = "grammar.txt"

    input_stream = open(source_path, 'r')
    gen = MatrixGenerator(input_stream)
    gen.generate()
    print(gen.error_msg)

