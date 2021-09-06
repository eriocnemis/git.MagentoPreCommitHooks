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
        '--rule-sets', default = 'codesize,cleancode,design', dest = 'sets',
        help = 'set of rules which will be applied against the source under test'
    )
    parser.add_argument(
        'filenames', nargs='*',
        help = 'PHP filenames to check'
    )
    args = parser.parse_args(argv)

    if module.match('**/app/code/*/*'):
        # path to the root of magento
        magento = module.parent.parent.parent.parent
        # path to the phpmd
        exe = magento / 'vendor/bin/phpmd'

        if exe.is_file():
            for filename in args.filenames:
                command = [args.php, f'{exe}', f'{module}/{filename}', 'text', args.sets]
                process = subprocess.run(command, capture_output=True, universal_newlines=True)
                if process.returncode:
                    print(f'{process.stdout}')
                    retval = 1
        else:
            print('phpmd is not installed')
            retval = 1
    else:
        print(f'{module}: incorrect module path')
        retval = 1

    return retval

if __name__ == '__main__':
    exit(main())
