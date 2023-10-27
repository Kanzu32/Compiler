import matrix

class Parser:

    def __init__(self, op_matrix, operators, rules):
        self.operators = operators
        self.t = ['/b/', *operators]
        self.operator_matrix = op_matrix
        self.error = False
        self.error_msg = "Parser: OK"
        self.stack = []
        self.rules: dict = rules


    def set_error(self, msg):
        self.error = True
        self.error_msg = "Parser: " + msg

    def print_matrix(self):
        pass

    def get_t(self, n=1):
        if n < 1:
            n = 1
        for item in self.stack[::-1]:
            if item in self.t:
                n -= 1
                if n == 0:
                    return item
        return "ERROR"

    def check(self):
        self.stack.append('/b/')
        i = 0
        while True:
            if self.get_t() == '/b/' and self.operators[i] == '/e/':
                break
            if self.get_t() not in self.operator_matrix.keys() or self.operators[i] not in self.operator_matrix[self.get_t()].keys():
                self.set_error("unknown construction '" + self.get_t() + " " + self.operators[i] + "' in " + " ".join(self.operators[i-2:i+1]))
                break
            if self.operator_matrix[self.get_t()][self.operators[i]] == matrix.ORDER.EQUALS or self.operator_matrix[self.get_t()][self.operators[i]] == matrix.ORDER.PRECEDED:
                self.stack.append(self.operators[i])
                i += 1
            elif self.operator_matrix[self.get_t()][self.operators[i]] == matrix.ORDER.FOLLOWS:
                rule = []
                if self.operator_matrix[self.get_t(2)][self.get_t()] == matrix.ORDER.PRECEDED:
                    count = 1
                    while True:
                        if self.stack[-1] in self.t:
                            if count == 0:
                                break
                            count -= 1
                        rule.append(self.stack.pop())
                    find = False
                    rule.reverse()
                    print("RULE:", rule)
                    for name in self.rules.keys():
                        for r in self.rules[name]:
                            if rule == r:
                                find = True
                                self.stack.append(name)
                                break
                        if find:
                            break
                    if not find:
                        self.set_error("Unable to locate rule " + " ".join(rule))
                        break
                    print("NAME:", name)
                    print(self.stack)

                elif self.operator_matrix[self.get_t(2)][self.get_t()] == matrix.ORDER.EQUALS:
                    count = 2
                    while self.operator_matrix[self.get_t(count+1)][self.get_t(count)] == matrix.ORDER.EQUALS:
                        count += 1
                    print(count)
                    while True:
                        if self.stack[-1] in self.t:
                            if count == 0:
                                break
                            count -= 1
                        rule.append(self.stack.pop())
                    find = False
                    rule.reverse()
                    print("RULE:", rule)
                    for name in self.rules.keys():
                        for r in self.rules[name]:
                            if rule == r:
                                find = True
                                self.stack.append(name)
                                break
                        if find:
                            break
                    if not find:
                        self.set_error("Unable to locate rule " + " ".join(rule))
                        break
                    print("NAME:", name)
                    print(self.stack)

if __name__ == "__main__":
    source_path = "grammar.txt"

    input_stream = open(source_path, 'r')
    gen = matrix.MatrixGenerator(input_stream)
    gen.generate()
    print(gen.error_msg)
