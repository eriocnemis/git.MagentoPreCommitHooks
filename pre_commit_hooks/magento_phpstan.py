#!/usr/bin/env python3
"""
 A pre-commit hook that, when passed one or more php files, using PHPStan will finds
bugs in your PHP code without writing tests. PHPStan catches whole classes of bugs
even before you write tests for the code. It moves PHP closer to compiled languages
in the sense that the correctness of each line of the code can be checked before you
run the actual line.
"""
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
        '-l', '--level', default = 'max', dest = 'level',
        help = 'specifies the rule level to run'
    )
    parser.add_argument(
        '--error-format', default = 'raw', dest = 'errorformat',
        help = 'specifies a custom error formatter'
    )
    parser.add_argument(
        '-a', '--autoload-file', default = False, dest = 'autoload',
        help = 'specifies the path to a custom autoloader'
    )
    parser.add_argument(
        '-c', '--configuration', default = False, dest = 'config',
        help = 'specifies the path to a configuration file'
    )
    parser.add_argument(
        'filenames', nargs='*',
        help = 'PHP filenames to check'
    )
    args = parser.parse_args(argv)

    if module.match(PATHPATERN):
        # path to the root of magento
        magento = module.parent.parent.parent.parent
        # path to the phpstan
        exe = magento / 'vendor/bin/phpstan'

        if exe.is_file():
            command = [args.php, f'{exe}', 'analyse', '--no-progress', '-l',  args.level, '--error-format', args.errorformat]

            if args.autoload:
                autoload = magento / args.autoload.strip('/')
                if autoload.is_file():
                    command += ['-a', str(autoload)]
                else:
                    parser.error(f'{module}: incorrect autoload file path')

            if args.config:
                config = magento / args.config.strip('/')
                if config.is_file():
                    command += ['-c', str(config)]
                else:
                    parser.error(f'{module}: incorrect config file path')

            command += args.filenames

            process = subprocess.run(command, capture_output=True, universal_newlines=True)
            retval = process.returncode
            if retval:
                print(f'{process.stdout}')
        else:
            print('phpstan is not installed')
            retval = 1
    else:
        print(f'{module}: incorrect module path')
        retval = 1

    return retval

if __name__ == '__main__':
    exit(main())
