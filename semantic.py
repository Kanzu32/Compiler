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
                for x in range(i + 1, j + 1, 2):
                    self.variables[self.operators[x].value] = Variable(vars_type)

            elif self.operators[i].type == lexer.Lexer.ID and self.operators[i + 1].type == lexer.Lexer.ASSIGN:
                if self.variables.get(self.operators[i].value) is None:
                    self.error = True
                    self.error_msg = "Undeclared variable " + self.operators[i].value

                id_type = self.variables[self.operators[i].value].type
                const_type = lexer.decrypt[self.operators[i + 2].type]
                operation_return = lexer.decrypt[self.operators[i + 3].type]

                if operation_return == ";" or operation_return == "to":

                    if const_type == "ID" and self.variables[self.operators[i].value].type != id_type:
                        print("ID SEMANTIC")
                        self.error = True
                        if self.variables.get(self.operators[i + 2].value) is None:
                            self.error_msg = "Undeclared variable " + self.operators[i+2].value
                            break
                        self.error_msg = ("Wrong type: " + self.operators[i].value + " is " +
                                          id_type + " unable to assign " +
                                          self.variables[self.operators[i + 2].value].type + " type")
                        break

                    elif const_type != "ID" and not ((id_type == "INT" or id_type == "FLOAT") and (const_type == "NUM"
                         or const_type == "REAL") or (id_type == "BOOL" and const_type == "BOOL_VAL")):
                        print("CONST SEMANTIC")
                        self.error = True
                        self.error_msg = ("Wrong type: " + self.operators[i].value + " is " +
                                          id_type + " unable to assign " +
                                          const_type + " type")
                        break

                elif ((id_type == "INT" or id_type == "FLOAT") and operation_return not in
                        self.RETURN_NUM) or id_type == "BOOL" and operation_return not in self.RETURN_BOOL:
                    print(operation_return)
                    print("OPERATOR SEMANTIC")
                    self.error = True
                    if operation_return in self.RETURN_NUM:
                        self.error_msg = ("Wrong type: " + self.operators[i].value + " is " + id_type
                                          + " unable to assign number type")
                    else:
                        self.error_msg = ("Wrong type: " + self.operators[i].value + " is " + id_type
                                          + " unable to assign BOOL type")
                    break

            elif self.operators[i].type == lexer.Lexer.ID:
                if self.variables.get(self.operators[i].value) is None:
                    self.error = True
                    self.error_msg = "Undeclared variable " + self.operators[i].value

            i += 1
