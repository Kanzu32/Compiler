class PRN:

    OPERANDS = ["ID", "NUM", "REAL", "BOOL_VAL"]
    UNARY = ["NOT"]
    PRIORITY = {
        "(":        [100, 0],
        ")":        [0, 0],
        "+":        [5, 5],
        "-":        [5, 5],
        ">":        [7, 7],
        "<":        [7, 7],
        ">=":       [0, 7],
        "<=":       [0, 7],
        "=":        [0, 7],
        "!=":       [0, 7],
        "*":        [0, 4],
        "/":        [0, 4],
        ";":        [0, 0],
        ".":        [0, 0],
        ",":        [0, 13],
        "{":        [0, 0],
        "}":        [0, 0],
        "if":       [0, 0],
        "else":     [0, 0],
        "elseif":   [0, 0],
        "for":      [0, 0],
        "to":       [0, 0],
        "do":       [0, 0],
        "while":    [0, 0],
        "ass":      [0, 0],
        "dim":      [0, 0],
        "and":      [0, 0],
        "or":       [0, 0],
        "not":      [0, 0],
        "read":     [0, 0],
        "output":   [0, 0],
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
                self.stack.append(symbol[1])
            else:
                if symbol[0] in self.UNARY:
                    res.append(symbol[0])
                    res.append(self.stack.pop()[1])
                else:
                    res.append(symbol[0])
                    res.append(self.stack.pop()[1])
                    res.append(self.stack.pop()[1])


        return res



if __name__ == "__main__":
    print("ONLY AS MODULE")
