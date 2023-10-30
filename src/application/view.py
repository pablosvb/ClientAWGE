from src.domain.cabecera import __header_AWGE__, __header_W__, __header_PMC__, __header_sxplain__, __header_line__

import os

class View:

    def cabecera():
        print(__header_W__)
        print(__header_PMC__)
    
        print()

    def clear():
        # Para windows
        if os.name == 'nt':
            _ = os.system('cls')
        # Para mac y linux(here, os.name is 'posix')
        else:
            _ = os.system('clear')


