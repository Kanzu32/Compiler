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
        self.error_msg = "Matrix generator: OK"
        self.rules = {}
        self.symbols_lr = LastSymbols()
        self.t_lr = LastSymbols()


    def set_error(self, msg):
        self.error = True
        self.error_msg = "Matrix generator: " + msg

    def print_matrix(self):
        print(" " * 6, end="")
        for x in [*MatrixGenerator.T, "/e/"]:
            print("{0:<6}".format(x), end="")
        print()
        for i in [*MatrixGenerator.T, "/b/"]:
            print("{0:<6}".format(i), end="")

            for j in [*MatrixGenerator.T, "/e/"]:
                if self.operator_matrix[i].get(j) is None:
                    print("." + " " * 5, end="")
                elif self.operator_matrix[i][j] == ORDER.PRECEDED:
                    print("<." + " " * 4, end="")
                elif self.operator_matrix[i][j] == ORDER.EQUALS:
                    print("=." + " " * 4, end="")
                elif self.operator_matrix[i][j] == ORDER.FOLLOWS:
                    print(".>" + " " * 4, end="")

            print()

    def generate(self):
        rule_names = self.input_stream.readline().split()
        # MatrixGenerator.SYMBOLS = input_stream.readline().split()
        # MatrixGenerator.WORDS = input_stream.readline().split()
        MatrixGenerator.T = self.input_stream.readline().split()
        for name in rule_names:  # инициализация имён
            self.rules[name] = []
            self.symbols_lr.left[name] = []
            self.symbols_lr.right[name] = []
            self.t_lr.left[name] = []
            self.t_lr.right[name] = []

        for symbol in ["/b/", *MatrixGenerator.T, "/e/"]:
            self.operator_matrix[symbol] = {}

        lines = self.input_stream.read().split('\n')  # заполнение правил вывода
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
                    elif tokens[i] not in MatrixGenerator.T and tokens[i] not in rule_names:
                        self.set_error('unknown symbol "' + tokens[i] + '"')
                        return self.error
                self.rules[rule_name].append(tokens[last_token_index:])
            else:
                self.set_error("wrong file formatting")
                return self.error

        for rule_name in self.rules.keys():  # начальное заполнение крайних левых, правых
            for arr in self.rules[rule_name]:
                first_t = None
                last_t = None
                first_symbol = None
                last_symbol = None
                for item in arr:
                    if item in MatrixGenerator.T:
                        if first_t is None:
                            first_t = item
                            last_t = item
                        else:
                            last_t = item

                    if first_symbol is None:
                        first_symbol = item
                        last_symbol = item
                    else:
                        last_symbol = item

                if last_t is not None:
                    if first_t not in self.t_lr.left[rule_name]:
                        self.t_lr.left[rule_name].append(first_t)
                    if last_t not in self.t_lr.right[rule_name]:
                        self.t_lr.right[rule_name].append(last_t)

                if last_symbol is not None:
                    if first_symbol not in self.symbols_lr.left[rule_name]:
                        self.symbols_lr.left[rule_name].append(first_symbol)
                    if last_symbol not in self.symbols_lr.right[rule_name]:
                        self.symbols_lr.right[rule_name].append(last_symbol)

        # print(self.symbols_lr.left)
        # print(self.symbols_lr.right)
        # print(self.t_lr.left)
        # print(self.t_lr.right)

        changed = True
        while changed:  # алгоритм для всех симв
            changed = False
            for rule_name in self.rules.keys():
                for item in self.symbols_lr.left[rule_name]:
                    if item in self.rules.keys():
                        for i in self.symbols_lr.left[item]:
                            if i not in self.symbols_lr.left[rule_name]:
                                self.symbols_lr.left[rule_name].append(i)
                                changed = True

                for item in self.symbols_lr.right[rule_name]:
                    if item in self.rules.keys():
                        for i in self.symbols_lr.right[item]:
                            if i not in self.symbols_lr.right[rule_name]:
                                self.symbols_lr.right[rule_name].append(i)
                                changed = True

        for rule_name in self.rules.keys():  # алгоритм для терм симв
            for item in self.symbols_lr.left[rule_name]:
                if item not in MatrixGenerator.T:
                    for i in self.t_lr.left[item]:
                        if i not in self.t_lr.left[rule_name] and i in MatrixGenerator.T:
                            self.t_lr.left[rule_name].append(i)

            for item in self.symbols_lr.right[rule_name]:
                if item not in MatrixGenerator.T:
                    for i in self.t_lr.right[item]:
                        if i not in self.t_lr.right[rule_name] and i in MatrixGenerator.T:
                            self.t_lr.right[rule_name].append(i)


        # print(MatrixGenerator.SYMBOLS)
        # print(MatrixGenerator.WORDS)
        # print("SYMBOLS: ")
        # print(self.symbols_lr.left)
        # print(self.symbols_lr.right)
        # print("T: ")
        # print(self.t_lr.left)
        # print(self.t_lr.right)
        #
        # print(self.rules)
        # print("LEFT: ")_
        # print(self.symbols_lr.left)
        # print("\nRIGHT: ")
        # print(self.symbols_lr.right)
        # print(len(MatrixGenerator.ALL_LANG_SYMBOLS))

        for symbol in MatrixGenerator.T:
            for rule in self.rules.values():
                for item in rule:
                    for i in range(len(item)):
                        if symbol == item[i]:

                            if i < len(item)-1 and item[i+1] in MatrixGenerator.T:  # x ai b y
                                if self.operator_matrix[symbol].get(item[i+1]) is not None and self.operator_matrix[symbol][item[i+1]] != ORDER.EQUALS:
                                    print("ОШИБКА", item, item[i:i+2], "x ai b y OLD:", self.operator_matrix[symbol][item[i+1]])
                                # print(item[i:i + 2], "x ai b y")
                                self.operator_matrix[symbol][item[i+1]] = ORDER.EQUALS
                            elif i < len(item)-2 and item[i+1] not in MatrixGenerator.T and item[i+2] in MatrixGenerator.T:  # x ai U b y
                                if self.operator_matrix[symbol].get(item[i+2]) is not None and self.operator_matrix[symbol][item[i+2]] != ORDER.EQUALS:
                                    print("ОШИБКА", item, item[i:i+3], "x ai U b y")
                                # print(item[i:i + 3], "x ai U b y")
                                self.operator_matrix[symbol][item[i+2]] = ORDER.EQUALS

                            if i < len(item)-1 and item[i+1] not in MatrixGenerator.T:  # x ai U y
                                for L in self.t_lr.left[item[i+1]]:
                                    if L in MatrixGenerator.T:
                                        if self.operator_matrix[symbol].get(L) is not None and self.operator_matrix[symbol][L] != ORDER.PRECEDED:
                                            print("ОШИБКА", item, L, item[i:i + 2], "x ai U y")
                                        # print(L, item[i:i + 2], "x ai U y")
                                        self.operator_matrix[symbol][L] = ORDER.PRECEDED
                                        continue

                            if i > 0 and item[i-1] not in MatrixGenerator.T:  # x U ai y
                                for R in self.t_lr.right[item[i-1]]:
                                    if R in MatrixGenerator.T:
                                        if self.operator_matrix[R].get(symbol) is not None and self.operator_matrix[R][symbol] != ORDER.FOLLOWS:
                                            print("ОШИБКА", item, R, item[i - 1:i + 1], "x U ai y")
                                        self.operator_matrix[R][symbol] = ORDER.FOLLOWS
                                        continue

        for s in self.t_lr.left[rule_names[0]]:
            self.operator_matrix["/b/"][s] = ORDER.PRECEDED

        for s in self.t_lr.right[rule_names[0]]:
            self.operator_matrix[s]["/e/"] = ORDER.FOLLOWS

        self.print_matrix()
        return self.operator_matrix





if __name__ == "__main__":
    source_path = "danil.txt"

    stream = open(source_path, 'r')
    gen = MatrixGenerator(stream)
    gen.generate()
    print(gen.error_msg)

