#mohammad shojaeyan-97110014
#danyal farahany-97105725

import os

def parse():
    hereDir = os.path.realpath(__file__)
    scannerDir = hereDir[0:-12] + "/parser.py"
    exec(open(scannerDir).read(),globals())

parse()
