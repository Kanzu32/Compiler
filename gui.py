import PySimpleGUI as sg
import io
import lexer

layout = [[sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-FILE-"), sg.Button("Load"), sg.Button('Compile', size=(12, 2), key="_COMPILE_")],
          [sg.Text("Source code:", size=(46, 1)), sg.Text("Lexemes:", size=(45, 1))],
          [sg.Multiline(s=(50, 30), key="-INPUT-"), sg.Multiline(s=(50, 30), disabled=True, key="-OUTPUT-")],
          [sg.Text("Errors:")],
          [sg.Multiline(s=(50, 5), key="-ERROR-")]]

window = sg.Window('Compiler', layout)


def compile_stream(stream):
    lex = lexer.Lexer(stream)
    res = ""
    while lex.symbol != lexer.Lexer.EOF:
        lex.next_token()
        if lex.error:
            window["-ERROR-"].update(lex.error_msg)
            break
        if lex.symbol == lexer.Lexer.ID or lex.symbol == lexer.Lexer.NUM or lex.symbol == lexer.Lexer.REAL:
            res += "(" + lexer.decrypt[lex.symbol] + "," + str(lex.value) + ")\n"
        else:
            res += "(" + lexer.decrypt[lex.symbol] + ")\n"
    window["-OUTPUT-"].update(res)
    window["-ERROR-"].update(lex.error_msg)


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "_COMPILE_":
        compile_stream(io.StringIO(values["-INPUT-"]))
    elif event == "Load":
        file = open(values["-IN-FILE-"])
        window["-INPUT-"].update(file.read())


window.close()
