#!/usr/bin/env python3

import argparse
import subprocess

from typing import Optional
from typing import Sequence
from pathlib import Path

# magento module relative path patern
PATHPATERN = '**/app/code/*/*'

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
        '-c', '--configuration', dest = 'config',
        help = 'specifies the path to a configuration file'
    )
    args = parser.parse_args(argv)

    if module.match(PATHPATERN):
        # path to the root of magento
        magento = module.parent.parent.parent.parent
        # path to the phpunit
        exe = magento / 'vendor/bin/phpunit'
        test = module / 'Test/Api/'

        if test.is_dir():
            if exe.is_file():
                config = magento / args.config.strip('/')
                command = [args.php, f'{exe}', '-c', str(config), str(test)]
                process = subprocess.run(command, capture_output=True, universal_newlines=True)
                retval = process.returncode
                if retval:
                    print(f'{process.stdout}')
            else:
                print('phpunit is not installed')
                retval = 1
    else:
        print(f'{module}: incorrect module path')
        retval = 1

    return retval

if __name__ == '__main__':
    exit(main())
