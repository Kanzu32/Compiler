import lexer
import matrix
import parser

source_path = "source.txt"
stream = open(source_path, 'r')

lex = lexer.Lexer(stream)
operators = []
while lex.symbol != lexer.Lexer.EOF:
    lex.next_token()
    if lex.error:
        break
    operators.append(lexer.decrypt_to_operators[lex.symbol])

print(lex.error_msg)

stream.close()

source_path = "test.txt"
stream = open(source_path, 'r')
gen = matrix.MatrixGenerator(stream)
gen.generate()
print(gen.error_msg)
stream.close()

print(operators)
pars = parser.Parser(gen.operator_matrix, operators, gen.rules)
pars.check()
print(pars.error_msg)