## [EN] Description
Model programming language compiler. The application includes lexical, syntactic, semantic analysis and translation into Polish inverse notation. The result of the application is to search for errors in the written code and translate the model language into a low-level language (NASM) with the ability to compile into an executable file.

The grammar of the language is described in the file `grammar.txt`, which lists all terminal and non-terminal symbols and rules of the language.

## Features
* Lexical, syntactic and semantic analysis;
* Translation into Polish inverse recording;
* Conversion to assembly code;
* Compiling exe file.

## Technologies
* Python;
* Assembler (NASM).

## [RU]Описание
Компилятор модельного языка программирования. Приложение включает в себя лексический, синтаксический, семантический анализ и трансляцию в польскую инверсную запись. Результатом работы приложения является поиск ошибок в написанном коде и перевод модельного языка в низкоуровневый язык с последующим преобразованием в исполняемый файл.

Подробное описание работы представлено [здесь](https://github.com/Kanzu32/Compiler/blob/main/%D0%9F%D0%BE%D1%8F%D1%81%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20%D0%B7%D0%B0%D0%BF%D0%B8%D1%81%D0%BA%D0%B0.pdf).

Грамматика языка описана в файле `grammar.txt`, где перечисляются все терминальные и нетерминальные символы и правила языка. 

#### 1. Лексический анализ
Исходный текст разбивается на лексемы и проверяется их корректность.

#### 2. Синтаксический анализ
По правилам грамматики строится матрица операторного предшествия и последовательность лексем проверяется на соответствие этим правилам.

#### 3. Семантический анализ
Проверяется соответствие типов и существование переменных.

#### 4. Перевод в польскую инверсную запись
Для перевода в польскую инверсную запись используется алгоритм Замельсона и Бауэра.

#### 5. Генерация ассемблерного кода из ПОЛИЗа
Для перевода в ассемблер NASM используется алгоритм, считывающий поэлементно ПОЛИЗ и генерирующий ассемблерный код в соответствии со встретившимся элементом.

## Особенности
* Лексический, синтаксический и семантический анализ;
* Трансляцию в польскую инверсную запись;
* Преобразование в ассемблерный код;
* Компиляция exe файла.
