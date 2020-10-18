import os

def scan():
    exec(open(os.path.realpath('./Compiler/scanner.py')).read())

# scan()
exec(open(os.path.realpath('./Compiler/scanner.py')).read()) #wtaf