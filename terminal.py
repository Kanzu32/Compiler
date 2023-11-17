import lexer
import matrix
import parser
import semantic

source_path = "source.txt"
stream = open(source_path, 'r')

lex = lexer.Lexer(stream)
operators = []
operators_val = []
while lex.symbol != lexer.Lexer.EOF:
    lex.next_token()
    if lex.error:
        break
    operators.append(lexer.decrypt_to_operators[lex.symbol])

    if lex.symbol == lexer.Lexer.ID or lex.symbol == lexer.Lexer.NUM or lex.symbol == lexer.Lexer.REAL:
        operators_val.append(semantic.Operator(lex.symbol, lexer.decrypt_to_operators[lex.symbol], lex.value))
    else:
        operators_val.append(semantic.Operator(lex.symbol, lexer.decrypt_to_operators[lex.symbol], None))


print(lex.error_msg)

stream.close()
source_path = "test.txt"
stream = open(source_path, 'r')
gen = matrix.MatrixGenerator(stream)
gen.generate()
print(gen.error_msg)
stream.close()

# print(operators)
pars = parser.Parser(gen.operator_matrix, operators, gen.rules)
pars.check()
print(pars.error_msg)

sem = semantic.Semantic(operators_val)
sem.check()
print(sem.error_msg)