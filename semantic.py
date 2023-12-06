import lexer


class Variable:
    def __init__(self, type):
        self.type = type


class Operator:
    def __init__(self, type, name, value=None):
        self.type = type
        self.name = name
        self.value = value


class Semantic:
    RETURN_BOOL = [">", ">=", "<", "<=", "=", "!=", "and", "or", "not"]
    RETURN_NUM = ["+", "-", "*", "/"]

    def __init__(self, operators):
        self.operators: list[Operator] = operators
        self.error = False
        self.error_msg = "Semantic: OK"
        self.variables: dict[Variable] = {}

    def set_error(self, msg):
        self.error = True
        self.error_msg = "Semantic: " + msg

    def check(self):
        i = 0
        while i < len(self.operators):
            if self.operators[i].type == lexer.Lexer.DIM:
                j = i + 1
                while self.operators[j].name != "TYPE":
                    j += 1
                vars_type = lexer.decrypt[self.operators[j].type]
                print(vars_type)
                for x in range(i + 1, j + 1, 2):
                    self.variables[self.operators[x].value] = Variable(vars_type)

            elif self.operators[i].type == lexer.Lexer.ID and self.operators[i + 1].type == lexer.Lexer.ASSIGN:
                if self.variables.get(self.operators[i].value) is None:
                    self.error = True
                    self.error_msg = "Undeclared variable " + self.operators[i].value

                id_type = self.variables[self.operators[i].value].type
                const_type = lexer.decrypt[self.operators[i + 2].type]
                operation_return = lexer.decrypt[self.operators[i + 3].type]

                if operation_return == ";":

                    if const_type == "ID" and self.operators[i].type != id_type:
                        print("ID SEMANTIC")
                        self.error = True
                        self.error_msg = ("Wrong type: " + self.operators[i].value + " is " +
                                          id_type + " unable to assign " +
                                          const_type + " type")
                        break

                    if not ((id_type == "INT" and const_type == "NUM") or (id_type == "FLOAT" and const_type == "REAL") or
                        (id_type == "BOOL" and (const_type == "FALSE" or const_type == "TRUE"))):

                        print("CONST SEMANTIC")
                        self.error = True
                        self.error_msg = ("Wrong type: " + self.operators[i].value + " is " +
                                          id_type + " unable to assign " +
                                          const_type + " type")
                        break

                elif operation_return != ";" and not ((id_type == "INT" or id_type == "FLOAT") and operation_return in
                        self.RETURN_NUM) or not (id_type == "BOOL" and operation_return in self.RETURN_BOOL):

                    print("OPERATOR SEMANTIC")
                    self.error = True
                    self.error_msg = ("Wrong type: " + self.operators[i].value + " is " + id_type
                                      + " unable to assign " + operation_return + " type")


                # else:
                #     self.variables[self.operators[i].value].value = self.operators[i + 2].value

            elif self.operators[i].type == lexer.Lexer.ID:
                if self.variables.get(self.operators[i].value) is None:
                    self.error = True
                    self.error_msg = "Undeclared variable " + self.operators[i].value
                # elif self.variables[self.operators[i].value].value is None:
                #     self.error = True
                #     self.error_msg = "Uninitialized variable " + self.operators[i].value
            i += 1

        for name in self.variables.keys():
            print(name, self.variables[name].type)

# if __name__ == "__main__":
#     source_path = "grammar.txt"
#
#     input_stream = open(source_path, 'r')
#     gen = matrix.MatrixGenerator(input_stream)
#     gen.generate()
#     print(gen.error_msg)
