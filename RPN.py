class PRN:

    OPERANDS = ["ID", "NUM", "REAL", "BOOL_VAL"]
    UNARY = ["NOT"]
    IGNORED = ["to", "do", "EOF"]
    UNPRINTABLE = [";", "{", "(", "}", ")"]
    PRIORITY = {
        "INT":      [2, 2],
        "FLOAT":    [2, 2],
        "BOOL":     [2, 2],
        "(":        [3, 1],
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
        ",":        [3, 2],
        "{":        [1, 0],
        "}":        [0, 0],
        "if":       [1, 2],
        "else":     [1, 0],
        "elseif":   [1, 2],
        "for":      [1, 2],
        "while":    [1, 2],
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
        self.end_stack = []
        self.if_stack = []
        self.if_count = 0
        self.end_count = 0


    def set_error(self, msg):
        self.error = True
        self.error_msg = "Reverse Polish notation: " + msg

    def convert(self):
        res = []
        for i in range(len(self.operators)):
            print("OPERATOR:", self.operators[i][0])
            if self.operators[i][0] in self.OPERANDS:
                res.append(self.operators[i][0])
                print("OPERAND")
            else:
                if self.operators[i][0] == "if" or self.operators[i][0] == "for" or self.operators[i][0] == "while":
                    self.end_stack.append("END" + str(self.end_count))
                    self.end_count += 1
                if self.operators[i][0] in self.IGNORED:
                    print("CONTINUE WITH: " + self.operators[i][0])
                    continue
                if len(self.stack) == 0 or self.PRIORITY[self.stack[-1]][1] < self.PRIORITY[self.operators[i][0]][0]:
                    print("STACK:", len(self.stack))
                    self.stack.append(self.operators[i][0])
                else:
                    stack_symbol = ""
                    if self.operators[i][0] == ")":
                        while stack_symbol != "(":
                            stack_symbol = self.stack.pop()
                            if stack_symbol not in self.UNPRINTABLE:
                                if stack_symbol == "elseif":
                                    stack_symbol = "if"
                                res.append(stack_symbol)
                        stack_symbol = self.stack.pop()
                        if stack_symbol == "if" or stack_symbol == "else" or stack_symbol == "elseif":
                            self.if_stack.append("M" + str(self.if_count))
                            self.if_count += 1
                            res.append("[" + self.if_stack[-1] + "]")
                        if stack_symbol not in self.UNPRINTABLE:
                            res.append(stack_symbol)
                    if self.operators[i][0] == "}":
                        while stack_symbol != "{":
                            stack_symbol = self.stack.pop()
                            if stack_symbol not in self.UNPRINTABLE:
                                if stack_symbol == "elseif":
                                    stack_symbol = "if"
                                res.append(stack_symbol)
                        if len(self.stack) == 0 or self.stack[-1] != "else":
                            res.append("[" + self.end_stack[-1] + "]")
                            res.append("(" + self.if_stack.pop() + ")")
                        else:
                            # stack_symbol = self.stack.pop()
                            # res.append(stack_symbol)
                            res.append("(" + self.end_stack.pop() + ")")

                    if self.operators[i][0] == ";":
                        while stack_symbol != "{" and len(self.stack) != 0:
                            stack_symbol = self.stack.pop()
                            if stack_symbol not in self.UNPRINTABLE:
                                if stack_symbol == "elseif":
                                    stack_symbol = "if"
                                res.append(stack_symbol)
                        if stack_symbol == "{":
                            self.stack.append(stack_symbol)

                    if self.operators[i][0] == "INT" or self.operators[i][0] == "FLOAT" or self.operators[i][0] == "BOOL":
                        stack_symbol = self.stack.pop()
                        while stack_symbol == ",":
                            res.append(stack_symbol)
                            stack_symbol = self.stack.pop()
                        self.stack.append(stack_symbol)
                        res.append(self.operators[i][0])



                # if self.operators[i][0] == "}" and self.operators[i+1][0] == ";":
                #     res.append("(" + self.end_stack.pop() + ")")

            print(self.stack)
            print(res)
            print("---")



        return res



if __name__ == "__main__":
    print("ONLY AS MODULE")
