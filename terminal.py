import lexer
import matrix
import parser
import semantic
import RPN
import ASM

source_path = "source.txt"
stream = open(source_path, 'r')

lex = lexer.Lexer(stream)
operators = []
operators_semantic = []
operator_values = []
while lex.symbol != lexer.Lexer.EOF:
    lex.next_token()
    if lex.error:
        break
    operators.append(lexer.decrypt_to_operators[lex.symbol])

    if lex.symbol == lexer.Lexer.ID or lex.symbol == lexer.Lexer.NUM or lex.symbol == lexer.Lexer.REAL or lex.symbol == lexer.Lexer.BOOL_VAL:
        operators_semantic.append(semantic.Operator(lex.symbol, lexer.decrypt_to_operators[lex.symbol], lex.value))
        operator_values.append([lexer.decrypt[lex.symbol], lex.value])
    else:
        operators_semantic.append(semantic.Operator(lex.symbol, lexer.decrypt_to_operators[lex.symbol], None))
        operator_values.append([lexer.decrypt[lex.symbol]])


print(lex.error_msg)

stream.close()
source_path = "grammar.txt"
stream = open(source_path, 'r')
gen = matrix.MatrixGenerator(stream)
gen.generate()
print(gen.error_msg)
stream.close()

rules = gen.rules
print(operators)
for rule_name in rules.keys():
    for rule in rules[rule_name]:
        for i in range(len(rule)):
            if rule[i] not in gen.T:
                rule[i] = "E"

pars = parser.Parser(gen.operator_matrix, operators, rules)
pars.check()
print(pars.error_msg)
sem = semantic.Semantic(operators_semantic)
sem.check()
print(sem.error_msg)

# i = 0
# while i < len(operator_values):
#     if operator_values[i][0] == ",":
#         operator_values[i-1][0] += " " + operator_values[i+1][0]
#         operator_values.pop(i)
#         operator_values.pop(i)
#     else:
#         i += 1

print(operator_values)
rpn = RPN.RPN(operator_values)
declare_res, res = rpn.convert()
# print()
# print(res)

asm_gen = ASM.ASM(declare_res, res)
asm_gen.generate()