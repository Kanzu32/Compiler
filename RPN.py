class PRN:

    OPERANDS = ["ID", "NUM", "REAL", "BOOL_VAL"]
    UNARY = ["NOT"]
    IGNORED = ["to", "do", "EOF"]
    UNPRINTABLE = [";", "{", "(", "}", ")"]
    PRIORITY = {
        "(":        [2, 1],
        ")":        [0, 0],
        "+":        [5, 5],
        "-":        [5, 5],
        ">":        [5, 5],
        "<":        [5, 5],
        ">=":       [5, 5],
        "<=":       [5, 5],
        "=":        [5, 5],
        "!=":       [5, 5],
        "*":        [5, 5],
        "/":        [5, 5],
        ";":        [0, 0],
        ",":        [5, 5],
        "{":        [0, 1],
        "}":        [0, 0],
        "if":       [0, 1],
        "else":     [0, 1],
        "elseif":   [0, 1],
        "for":      [0, 1],
        "while":    [0, 1],
        "ass":      [2, 1],
        "dim":      [2, 2],
        "and":      [5, 5],
        "or":       [5, 5],
        "not":      [5, 5],
        "read":     [2, 2],
        "output":   [2, 2],
    }

    def __init__(self, operators):
        self.operators = operators
        self.error = False
        self.error_msg = "Reverse Polish notation: OK"
        self.stack = []


    def set_error(self, msg):
        self.error = True
        self.error_msg = "Reverse Polish notation: " + msg

    def convert(self):
        res = []
        for symbol in self.operators:
            if symbol[0] in self.OPERANDS:
                res.append(symbol[1])
            else:
                if symbol[0] in self.IGNORED:
                    continue
                if len(self.stack) == 0 or self.PRIORITY[self.stack[-1]][1] < self.PRIORITY[symbol[0]][0]:
                    self.stack.append(symbol[0])
                else:
                    stack_symbol = self.stack.pop()
                    if stack_symbol not in self.UNPRINTABLE:
                        res.append(stack_symbol)
                    if symbol[0] not in self.UNPRINTABLE:
                        self.stack.append(symbol[0])
        print(self.stack)
        return res



if __name__ == "__main__":
    print("ONLY AS MODULE")
