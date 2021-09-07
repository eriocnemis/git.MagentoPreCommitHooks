#!/usr/bin/env python3

import argparse
import subprocess

from typing import Optional
from typing import Sequence
from pathlib import Path

def main(argv: Optional[Sequence[str]] = None) -> int:
    # return flag
    retval = 0
    # path to the tested module
    module = Path.cwd()
    # prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--php', default = 'php', dest = 'php',
        help = 'alias or full path to the executable file of PHP'
    )
    parser.add_argument(
        '--min-lines', default = '5', dest = 'lines',
        help = 'specify a minimum number of identical lines'
    )
    args = parser.parse_args(argv)

    if module.match('**/app/code/*/*'):
        # path to the root of magento
        magento = module.parent.parent.parent.parent
        # path to the phpcpd
        exe = magento / 'vendor/bin/phpcpd'

        if module.is_dir():
            if exe.is_file():
                command = [args.php, f'{exe}', '--min-lines', args.lines, str(module)]
                process = subprocess.run(command, capture_output=True, universal_newlines=True)
                if process.returncode:
                    print(f'{process.stdout}')
                    retval = 1
            else:
                print('phpcpd is not installed')
                retval = 1
    else:
        print(f'{module}: incorrect module path')
        retval = 1

    return retval

if __name__ == '__main__':
    exit(main())
