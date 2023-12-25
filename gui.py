import PySimpleGUI as sg
import io
import os
import lexer
import matrix
import parser
import semantic
import RPN
import ASM

# sg.theme('Black')
layout = [[sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-FILE-"), sg.Button("Load"), sg.Button('Compile', size=(12, 2), key="_COMPILE_"), sg.Button('Build EXE', size=(12, 2), key="_BUILD_")],
          [sg.Text("Source code:", size=(46, 1)), sg.Text("Lexemes:", size=(45, 1)), sg.Text("Reverse Polish notation:", size=(45, 1)), sg.Text("Assembler (NASM):", size=(45, 1)),],
          [sg.Multiline(s=(50, 30), key="-INPUT-"), sg.Multiline(s=(50, 30), disabled=True, key="-LEXER-"), sg.Multiline(s=(50, 30), disabled=True, key="-RPN-"), sg.Multiline(s=(50, 30), disabled=True, key="-ASM-")],
          [sg.Text("Errors:")],
          [sg.Multiline(s=(50, 7), key="-ERROR-", disabled=True)]]

window = sg.Window('Compiler', layout)

def do_compile(stream):
    lex = lexer.Lexer(stream)
    operators = []
    operators_semantic = []
    operator_values = []
    res = ""
    err = ""
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

        if lex.symbol == lexer.Lexer.ID:
            res += lexer.decrypt_to_lexemes[lex.symbol] + ": " + str(lex.value) + "\n"
        elif lex.symbol == lexer.Lexer.ID or lex.symbol == lexer.Lexer.NUM or lex.symbol == lexer.Lexer.REAL:
            res += "CONSTANT: " + lexer.decrypt_to_lexemes[lex.symbol] + "," + str(lex.value) + "\n"
        elif lex.symbol in lexer.Lexer.SYMBOLS.values() or lex.symbol == lexer.Lexer.EOF:
            res += "SYMBOL: " + lexer.decrypt_to_lexemes[lex.symbol] + "\n"
        else:
            res += "WORD: " + lexer.decrypt_to_lexemes[lex.symbol] + "\n"
    if lex.error:
        window["-ERROR-"].update(lex.error_msg)
        return
    window["-LEXER-"].update(res)
    err += lex.error_msg + "\n"
    stream.close()

    source_path = "grammar.txt"
    stream = open(source_path, 'r')
    gen = matrix.MatrixGenerator(stream)
    gen.generate()
    if gen.error:
        window["-ERROR-"].update(gen.error_msg)
        return
    err += gen.error_msg + "\n"
    stream.close()

    rules = gen.rules
    for rule_name in rules.keys():
        for rule in rules[rule_name]:
            for i in range(len(rule)):
                if rule[i] not in gen.T:
                    rule[i] = "E"

    pars = parser.Parser(gen.operator_matrix, operators, rules)
    pars.check()
    if pars.error:
        window["-ERROR-"].update(pars.error_msg)
        return
    err += pars.error_msg + "\n"

    sem = semantic.Semantic(operators_semantic)
    sem.check()
    if sem.error:
        window["-ERROR-"].update(sem.error_msg)
        return
    err += sem.error_msg + "\n"

    rpn = RPN.RPN(operator_values)
    declare_res, res = rpn.convert()
    if rpn.error:
        window["-ERROR-"].update(rpn.error_msg)
        return
    res_string = ""
    for el in declare_res:
        res_string += str(el) + " "
    for el in res:
        res_string += str(el) + " "
    window["-RPN-"].update(res_string)
    err += rpn.error_msg + "\n"
    asm_gen = ASM.ASM(declare_res, res)
    res_string = asm_gen.generate()
    if asm_gen.error:
        window["-ERROR-"].update(asm_gen.error_msg)
        return
    window["-ASM-"].update(res_string)
    err += asm_gen.error_msg + "\n"
    window["-ERROR-"].update(err)


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "_COMPILE_":
        do_compile(io.StringIO(values["-INPUT-"]))
    elif event == "Load":
        if values["-IN-FILE-"] != "":
            file = open(values["-IN-FILE-"])
            window["-INPUT-"].update(file.read())
    elif event == "_BUILD_":
        asm_file = open("asm.asm", "w")
        asm_file.write(values["-ASM-"])
        asm_file.close()
        os.system('.\\NASM\\nasm.exe --gprefix _ -f win32 asm.asm -o asm.obj')
        os.system(".\MinGW\\bin\gcc.exe asm.obj .\\NASM\macro.o -g -o asm.exe -m32")

window.close()
