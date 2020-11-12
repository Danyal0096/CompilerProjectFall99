import os
from anytree import Node, RenderTree
from scanner import get_next_token_for_parser

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


hereDir = os.path.realpath(__file__)
projDir = hereDir[0:-12]

INPUT = open(projDir + "/input.txt", "rb")
parse = open(projDir + "/parse_tree.txt", "w", encoding='utf-8')
errors = open(projDir + "/syntax_errors.txt", "w", encoding='utf-8')
grammer = open(projDir + "/grammer.txt", "r")
follow = open(projDir + "/follow.txt", "r")
first = open(projDir + "/first.txt", "r")

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
            nodeeee = stack.pop()
            errors.write("#" + str(first_token[2]) + " : syntax error, missing " + str(nodeeee.name))
            nodeeee.parent = Node("delete")
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
            nodeee = stack.pop()
            errors.write("#" + str(first_token[2]) + " : syntax error, missing " + str(nodeee.name))
            nodeee.parent = Node("delete")
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
        errors.write("#" + str(first_token[2]+1) + " : Syntax Error, unexpected EOF")
        for node in stack:
            node.parent = Node("delete")
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