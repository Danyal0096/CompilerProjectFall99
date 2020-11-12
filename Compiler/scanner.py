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