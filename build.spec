# build.spec

import sys
from pathlib import Path
from PyInstaller import __main__ as pyi_main

if __name__ == '__main__':
    sys.argv.append('main.py')
    sys.argv.append('--onefile')
    sys.argv.append('--windowed')
    sys.argv.append('--name=CalendarManager')
    pyi_main.run()
