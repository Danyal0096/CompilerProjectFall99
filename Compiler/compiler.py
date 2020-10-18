import os 

def scan():
    hereDir = os.path.realpath(__file__)
    scannerDir = hereDir[0:-12] + "\\scanner.py"
    exec(open(scannerDir).read(),globals())

scan()
