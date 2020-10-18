import os

def scan():
    exec(open(os.path.realpath('./Compiler/scanner.py')).read())

# scan()
# exec(open(os.path.realpath('./Compiler/scanner.py')).read()) #wtaf
sth = os.path.dirname("compiler.py")
sth = sth.replace("compiler","scanner")
print(sth)