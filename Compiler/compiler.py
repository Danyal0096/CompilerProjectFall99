#mohammad shojaeyan-97110014
#danyal farahany-97105725

import os

def scan():
    hereDir = os.path.realpath(__file__)
    scannerDir = hereDir[0:-12] + "\\scanner.py"
    exec(open(scannerDir).read(),globals())

scan()
