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
        '--standard', default = 'Magento2', dest = 'standard',
        help = 'the name or path of the coding standard to use'
    )
    parser.add_argument(
        '--autofix', action='store_true', dest='autofix',
        help='automatically fixes encountered violations as possible',
    )
    parser.add_argument(
        'filenames', nargs='*',
        help = 'PHP filenames to check'
    )
    args = parser.parse_args(argv)

    if module.match('**/app/code/*/*'):
        # path to the root of magento
        magento = module.parent.parent.parent.parent
        # path to the phpcs
        if args.autofix:
            exe = magento / 'vendor/bin/phpcbf'
        else:
            exe = magento / 'vendor/bin/phpcs'

        if exe.is_file():
            command = [args.php, f'{exe}', f'--standard={args.standard}']
            command += args.filenames

            process = subprocess.run(command, capture_output=True, universal_newlines=True)
            retval = process.returncode
            if retval:
                print(f'{process.stdout}')
        else:
            print('phpcs is not installed')
            retval = 1
    else:
        print(f'{module}: incorrect module path')
        retval = 1

    return retval

if __name__ == '__main__':
    exit(main())
