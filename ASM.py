from ieee754 import single

class ASM:

    TYPES = ["INT", "BOOL", "FLOAT"]
    OPERATORS = ["+", "-", "*", "/", ">", ">=", "<", "<=", "=", "!=", ",", "if", "else",
                 "elseif", "for", "while", "ass", "read", "output", "and", "or", "not"]
    def __init__(self, declare_rpn, main_rpn):
        self.error = False
        self.error_msg = "OK"
        self.declare_rpn = declare_rpn
        self.main_rpn = main_rpn
        self.variables = []
        self.var_names = []
        self.stack = []
        self.calced = False
        self.labels_count = 0

    def set_error(self, msg):
        self.error = True
        self.error_msg = "Assembler generator: " + msg

    def two_operands_calc(self):
        res = ""
        second = self.stack.pop()
        first = self.stack.pop()
        res += "\tfinit\n"
        if first in self.var_names:
            res += "\tfld dword[" + first + "]\n"
        else:
            res += "\tmov dword[TMP], 0x" + single(first).hex()[0] + "\n\tfld dword[TMP]\n"
        if second in self.var_names:
            res += "\tfld dword[" + second + "]\n"
        else:
            res += "\tmov dword[TMP], 0x" + single(second).hex()[0] + "\n\tfld dword[TMP]\n"
        return res

    # TODO [",", "read", "output", "not"]


    def generate(self):
        res = "section .data\n\tZEROS equ 0x0\n\tFALSE equ 0x0\n\tTRUE equ 0x3f800000\n\tTMP dd 0.0\n\tRES dd ZEROS\n"
        for el in self.declare_rpn:
            if el == "," or el == "dim":
                continue
            elif el in self.TYPES:
                for i in range(len(self.variables)):
                    if self.variables[i][1] is None:
                        self.variables[i][1] = el
                        res += "\t" + self.variables[i][0] + " dd ZEROS\n"
            else:
                self.variables.append([el, None])
                self.var_names.append(el)

        res += "\nsection .text\nglobal main\nmain:\n\tmov ebp, esp\n"

        for i in range(len(self.main_rpn)):
            el = str(self.main_rpn[i])
            if el == "+":
                res += self.two_operands_calc()
                res += "\tfadd\n"
                self.calced += 1
                res += "\tfstp dword[RES]\n"

            elif el == "-":
                res += self.two_operands_calc()
                res += "\tfsub\n"
                self.calced += 1
                res += "\tfstp dword[RES]\n"

            elif el == "*":
                res += self.two_operands_calc()
                res += "\tfmul\n"
                self.calced += 1
                res += "\tfstp dword[RES]\n"

            elif el == "/":
                res += self.two_operands_calc()
                res += "\tfdiv\n"
                self.calced += 1
                res += "\tfstp dword[RES]\n"

            elif el == "ass":
                if self.calced:
                    res += "\tmov eax, dword[RES]\n"
                    res += "\tmov dword["+self.stack.pop()+"], eax\n"
                    self.calced = False
                else:
                    second = self.stack.pop()
                    first = self.stack.pop()
                    if second in self.var_names:
                        res += "\tmov dword[" + first + "], dword[" + second + "]\n"
                    else:
                        res += "\tmov dword["+first+"], 0x"+single(second).hex()[0]+"\n"

            elif el == ">":
                res += self.two_operands_calc()
                res += "\tfcomi\n"
                res += "\tjb label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "\tmov dword[RES], FALSE\n"
                res += "\tjmp label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "label"+str(self.labels_count-2)+":\n"
                res += "\tmov dword[RES], TRUE\n"
                res += "label"+str(self.labels_count-1)+":\n"
                self.calced = True

            elif el == ">=":
                res += self.two_operands_calc()
                res += "\tfcomi\n"
                res += "\tjbe label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "\tmov dword[RES], FALSE\n"
                res += "\tjmp label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "label"+str(self.labels_count-2)+":\n"
                res += "\tmov dword[RES], TRUE\n"
                res += "label"+str(self.labels_count-1)+":\n"
                self.calced = True

            elif el == "=":
                res += self.two_operands_calc()
                res += "\tfcomi\n"
                res += "\tjz label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "\tmov dword[RES], FALSE\n"
                res += "\tjmp label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "label"+str(self.labels_count-2)+":\n"
                res += "\tmov dword[RES], TRUE\n"
                res += "label"+str(self.labels_count-1)+":\n"
                self.calced = True

            elif el == "<":
                res += self.two_operands_calc()
                res += "\tfcomi\n"
                res += "\tja label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "\tmov dword[RES], FALSE\n"
                res += "\tjmp label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "label"+str(self.labels_count-2)+":\n"
                res += "\tmov dword[RES], TRUE\n"
                res += "label"+str(self.labels_count-1)+":\n"
                self.calced = True

            elif el == "<=":
                res += self.two_operands_calc()
                res += "\tfcomi\n"
                res += "\tjae label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "\tmov dword[RES], FALSE\n"
                res += "\tjmp label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "label"+str(self.labels_count-2)+":\n"
                res += "\tmov dword[RES], TRUE\n"
                res += "label"+str(self.labels_count-1)+":\n"
                self.calced = True

            elif el == "!=":
                res += self.two_operands_calc()
                res += "\tfcomi\n"
                res += "\tjnz label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "\tmov dword[RES], FALSE\n"
                res += "\tjmp label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "label"+str(self.labels_count-2)+":\n"
                res += "\tmov dword[RES], TRUE\n"
                res += "label"+str(self.labels_count-1)+":\n"
                self.calced = True

            elif el == "and":
                second = self.stack.pop()
                first = self.stack.pop()
                if first in self.var_names:
                    res += "\tmov eax, dword[" + first + "]\n"
                else:
                    res += "\tmov eax, 0x" + single(first).hex()[0] + "\n"
                if second in self.var_names:
                    res += "\tand eax, dword[" + second + "]\n"
                else:
                    res += "\tand eax, 0x" + single(second).hex()[0] + "\n"
                res += "\tmov dword[RES], eax\n"
                self.calced = True

            elif el == "or":
                second = self.stack.pop()
                first = self.stack.pop()
                if first in self.var_names:
                    res += "\tmov eax, dword[" + first + "]\n"
                else:
                    res += "\tmov eax, 0x" + single(first).hex()[0] + "\n"
                if second in self.var_names:
                    res += "\tor eax, dword[" + second + "]\n"
                else:
                    res += "\tor eax, 0x" + single(second).hex()[0] + "\n"
                res += "\tmov dword[RES], eax\n"
                self.calced = True

            elif el[0] == "[" and (self.main_rpn[i+1] == "if" or self.main_rpn[i+1] == "elseif"):
                res += "\tfinit\n"
                res += "\tfld dword[RES]\n"
                res += "\tmov dword[TMP], 0x" + single(str(0)).hex()[0] + "\n\tfld dword[TMP]\n"
                res += "\tfcomi\n"
                res += "\tjnz label"+str(self.labels_count)+"\n"
                self.labels_count += 1
                res += "\tjmp "+el[1:-1:]+"\n"
                res += "label"+str(self.labels_count-1) + ":\n"
                self.calced = False

            elif el[0] == "[" and self.main_rpn[i+1] == "for":
                second = self.stack.pop()
                first = self.stack.pop()
                res += "\tfinit\n"
                res += "\tfld dword["+first+"]\n"
                if second in self.var_names:
                    res += "\tfld dword["+second+"]\n"
                else:
                    res += "\tmov dword[TMP], 0x" + single(second).hex()[0] + "\n\tfld dword[TMP]\n"
                res += "\tfcomi\n"
                res += "\tjz " + el[1:-1:] + "\n"

            elif el[0] == "[" and self.main_rpn[i+1] == "while":
                res += "\tfld dword[RES]\n"
                res += "\tmov dword[TMP], 0x" + single(str(0)).hex()[0] + "\n\tfld dword[TMP]\n"
                res += "\tfcomi\n"
                res += "\tjz "+el[1:-1:]+"\n"

            elif el[0] == "[":
                res += "\tjmp "+el[1:-1:]+"\n"
            elif el[0] == "(":
                res += el[1:-1:] + ":\n"
            else:
                self.stack.append(el)

        res += "\tret\n"
        return res



if __name__ == "__main__":
    print("ONLY AS MODULE")
