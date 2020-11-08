import re
import os

def is_keyword(KEYWORDS, ID: str):
    if (ID in KEYWORDS):
        return True
    else:
        return False

def get_next_state(start_state: int, character: str):
    out = [False, "next_state or error type", False]
    symbol_list = [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "<"]
    whitespace = [" ", "\n", "\t", "\r", "\f", "\v"]

    if (start_state == 0):
        if (re.match('[a-zA-Z]', character)):
            out[1] = 1
        elif (re.match('[0-9]', character)):
            out[1] = 3
        elif (character in symbol_list):
            out[1] = 5
        elif (character == "="):
            out[1] = 6
        elif (character == "*"):
            out[1] = 8
        elif (character == "/"):
            out[1] = 10
        elif (character in whitespace):
            out[1] = 15
        else:
            out[0] = True
            out[1] = "Invalid input"
    elif (start_state == 1):
        if (re.match('[a-zA-Z0-9]', character)):
            out[1] = 1
        elif (character not in (symbol_list + whitespace + ["=", "*", "/"])):
            out[0] = True
            out[1] = "Invalid input"
        else:
            out[1] = 2
            out[2] = True
    elif (start_state == 3):
        if (not re.match('[0-9]', character) and (
                character not in (symbol_list + whitespace + ["=", "*", "/"]) or re.match('[a-zA-Z]', character))):
            out[0] = True
            out[1] = "Invalid number"
        elif (not re.match('[0-9]', character)):
            out[1] = 4
            out[2] = True
    elif (start_state == 6):
        if (character == "="):
            out[1] = 7
        elif (character in (symbol_list + whitespace + ["=", "*", "/"]) or re.match('[a-zA-Z0-9]', character)):
            out[1] = 9
            out[2] = True
        else:
            out[0] = True
            out[1] = "Invalid input"
    elif (start_state == 8):
        if (character == "/"):
            out[0] = True
            out[1] = "Unmatched comment"
        elif (character in (symbol_list + whitespace + ["=", "*", "/"]) or re.match('[a-zA-Z0-9]', character)):
            out[1] = 9
            out[2] = True
        else:
            out[0] = True
            out[1] = "Invalid input"
    elif (start_state == 10):
        if (character == "/"):
            out[1] = 11
        elif (character == "*"):
            out[1] = 13
        else:
            out[0] = True
            out[1] = "Invalid input"
    elif (start_state == 11):
        if (character == "\n"):
            out[1] = 12
    elif (start_state == 13):
        if (character == "*"):
            out[1] = 14
    elif (start_state == 14):
        if (character == "/"):
            out[1] = 12
        elif (not character == "*"):
            out[1] = 13

    if (out[1] == "next_state or error type"):
        out[1] = start_state

    return out


def get_next_token(INPUT, KEYWORDS):
    STATE_SITUATION = ["", "", "ID", "", "NUM", "SYMBOL", "", "SYMBOL", "", "SYMBOL", "", "", "COMMENT", "", "",
                       "WHITESPACE"]
    STATE = 0
    change_line = 0
    lexeme = ""

    while (True):
        i = 1
        while (True):
            try:
                character = INPUT.read(i).decode()
                break
            except:
                INPUT.seek(-1 * i, os.SEEK_CUR)
                i += 1

        if (character == ""):
            break

        next_state = get_next_state(STATE, character)
        STATE = next_state[1]

        if (character == "\n" and not next_state[2]):
            change_line += 1

        if (next_state[0]):
            return [next_state[1], lexeme + character, change_line, False]
        elif (STATE_SITUATION[STATE] != ""):
            if (STATE == 2 or STATE == 9 or STATE == 4):
                INPUT.seek(-1 * i, os.SEEK_CUR)
                if (STATE == 2):
                    if (is_keyword(KEYWORDS, lexeme)):
                        return ["KEYWORD", lexeme, change_line, False]
                return [STATE_SITUATION[STATE], lexeme, change_line, False]
            else:
                return [STATE_SITUATION[STATE], lexeme + character, change_line, False]

        lexeme += character

    if (STATE == 10 or STATE == 11 or STATE == 13 or STATE == 14):
        return ["Unclosed comment", lexeme, change_line, True]
    elif (STATE_SITUATION[STATE] == "" and not STATE == 0):
        return ["Invalid input", lexeme, change_line, True]
    else:
        return ["", "$", -1, True]

def get_next_token_for_parser(INPUT, KEYWORDS, line : int):
    next_token = get_next_token(INPUT, KEYWORDS)
    line += next_token[2]
    while (next_token[0] == "Invalid input" or next_token[0] == "Unclosed comment" or next_token[0] == "Invalid number" or next_token[0] == "Unmatched comment" or next_token[0] == "COMMENT" or next_token[0] == "WHITESPACE"):
        next_token = get_next_token(INPUT, KEYWORDS)
        line += next_token[2]

    if (next_token[3] and next_token[2] == -1):
        return ["", "$", line, True]
    return [next_token[0], next_token[1], line]







































from anytree import Node, RenderTree

def get_first(first, a: str):
    for i in first:
        if (i.split(" ")[0] == a):
            return i.split(" ")[1:len(i.split(" "))]
    return [a]


def get_follow(follow, a: str):
    for i in follow:
        if (i.split(" ")[0] == a):
            return i.split(" ")[1:len(i.split(" "))]

def reverse_array(array):
    array_out = []
    for i in range(len(array)-1, -1, -1):
        array_out.append(array[i])
    return array_out


def set_parse_table(parse_table, grammer, follow, first, non_terminals, terminals):
    for non_terminal in non_terminals:
        element_of_parse_table = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                  "", "", "", "", "", "", ""]
        for command in grammer:
            if (not command.split(" ")[0] == non_terminal):
                continue
            if (not command.split(" ")[1] == "epsilon"):
                right_grammer = ""
                all_first = []
                continue_for_first = True
                for i in range(len(command.split(" "))):
                    if (i == 0):
                        continue
                    if (i == len(command.split(" ")) - 1):
                        right_grammer += command.split(" ")[i]
                    else:
                        right_grammer += command.split(" ")[i] + " "
                    if (continue_for_first):
                        all_first += get_first(first, command.split(" ")[i])
                    if (not "epsilon" in get_first(first, command.split(" ")[i])):
                        continue_for_first = False
                for i in all_first:
                    if (i == "epsilon"):
                        continue
                    element_of_parse_table[terminals.index(i)] = right_grammer
            all_follow = get_follow(follow, command.split(" ")[0])
            is_epsilon = True
            right_grammer = ""
            for i in range(len(command.split(" "))):
                if (i == 0):
                    continue
                if (i == len(command.split(" ")) - 1):
                    right_grammer += command.split(" ")[i]
                else:
                    right_grammer += command.split(" ")[i] + " "
                if (not "epsilon" in get_first(first, command.split(" ")[i])):
                    is_epsilon = False
                    break
            if (is_epsilon):
                for i in all_follow:
                    element_of_parse_table[terminals.index(i)] = right_grammer
        all_follow = get_follow(follow, non_terminal)
        for i in all_follow:
            if (element_of_parse_table[terminals.index(i)] == ""):
                element_of_parse_table[terminals.index(i)] = "synch"

        parse_table.append(element_of_parse_table)


KEYWORDS = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"]
ID = []

INPUT = open("/home/shajusahar/Desktop/input.txt", "rb")
parse = open("/home/shajusahar/Desktop/parse_tree.txt", "w")
errors = open("/home/shajusahar/Desktop/syntax_errors.txt", "w")
grammer = open("/home/shajusahar/Desktop/grammer.txt", "r")
follow = open("/home/shajusahar/Desktop/follow.txt", "r")
first = open("/home/shajusahar/Desktop/first.txt", "r")

non_terminals = ["Program", "Declaration-list", "Declaration", "Declaration-initial", "Declaration-prime",
                 "Var-declaration-prime", "Fun-declaration-prime", "Type-specifier", "Params", "Param-list-void-abtar",
                 "Param-list", "Param", "Param-prime", "Compound-stmt", "Statement-list", "Statement",
                 "Expression-stmt", "Selection-stmt", "Iteration-stmt", "Return-stmt", "Return-stmt-prime",
                 "Switch-stmt", "Case-stmts", "Case-stmt", "Default-stmt", "Expression", "B", "H",
                 "Simple-expression-zegond", "Simple-expression-prime", "C", "Relop", "Additive-expression",
                 "Additive-expression-prime", "Additive-expression-zegond", "D", "Addop", "Term", "Term-prime",
                 "Term-zegond", "G", "Signed-factor", "Signed-factor-prime", "Signed-factor-zegond", "Factor",
                 "Var-call-prime", "Var-prime", "Factor-prime", "Factor-zegond", "Args", "Arg-list", "Arg-list-prime"]
terminals = ["$", "ID", ";", "[", "NUM", "]", "(", ")", "int", "void", ",", "break", "if", "else", "while", "return",
             "switch", "{", "}", "case", ":", "default", "=", "<", "==", "+", "-", "*"]
parse_table = []
set_parse_table(parse_table, grammer.read().split("\n"), follow.read().split("\n"), first.read().split("\n"),
                non_terminals, terminals)
Program = Node("Program")
stack = [Program]
first_token = get_next_token_for_parser(INPUT, KEYWORDS, 1)
exist_error = False
while(True):
    if (len(first_token) == 4):
        break
    if (stack[-1].name in terminals):
        if (not (first_token[0] == stack[-1].name or first_token[1] == stack[-1].name)):
            if (exist_error):
                errors.write("\n")
            exist_error = True
            errors.write("#" + str(first_token[2]) + " : syntax error, missing " + str(stack.pop().name))
            continue
    else:
        index_in_non_terminal = non_terminals.index(stack[-1].name)
        index_in_terminal = 0
        if (first_token[0] in terminals):
            index_in_terminal = terminals.index(first_token[0])
        else:
            index_in_terminal = terminals.index(first_token[1])
        if (parse_table[index_in_non_terminal][index_in_terminal] == ""):
            if (exist_error):
                errors.write("\n")
            exist_error = True
            if (first_token[1] in terminals):
                errors.write("#" + str(first_token[2]) + " : syntax error, illegal " + str(first_token[1]))
            else:
                errors.write("#" + str(first_token[2]) + " : syntax error, illegal " + str(first_token[0]))
            first_token = get_next_token_for_parser(INPUT, KEYWORDS, first_token[2])
            continue
        elif (parse_table[index_in_non_terminal][index_in_terminal] == "synch"):
            if (exist_error):
                errors.write("\n")
            exist_error = True
            errors.write("#" + str(first_token[2]) + " : syntax error, missing " + str(stack.pop().name))
            continue
    if (first_token[0] == stack[-1].name or first_token[1] == stack[-1].name):
        stack[-1].name = "(" + first_token[0] + ", " + first_token[1] + ") "
        stack.pop()
        first_token = get_next_token_for_parser(INPUT, KEYWORDS, first_token[2])
        continue
    else:
        index_in_non_terminal = non_terminals.index(stack[-1].name)
        index_in_terminal = 0
        if (first_token[0] in terminals):
            index_in_terminal = terminals.index(first_token[0])
        else:
            index_in_terminal = terminals.index(first_token[1])
        grams = parse_table[index_in_non_terminal][index_in_terminal]
        if (grams.split(" ")[0] == "epsilon"):
            epsilon = Node("epsilon", stack[-1])
            stack.pop()
            continue
        node = stack.pop()
        grams_array = []
        for gram in grams.split(" "):
            grams_array.append(Node(gram, node))
        for nodee in reverse_array(grams_array):
            stack.append(nodee)

while (True):
    if (stack[-1].name == "$"):
        break
    if (not parse_table[non_terminals.index(stack[-1].name)][0] == "epsilon"):
        if (exist_error):
            errors.write("\n")
        exist_error = True
        errors.write("#" + str(first_token[2]+1) + " : syntax error, unexpected EOF")
        break
    else:
        epsilon = Node("epsilon", stack[-1])
        stack.pop()

if (not exist_error):
    errors.write("There is no syntax error.")
for pre, fill, node in RenderTree(Program):
    parse.write("%s%s\n" % (pre, node.name))

INPUT.close()
parse.close()
errors.close()
grammer.close()
follow.close()
first.close()



