#!/usr/bin/env python3

import argparse
import subprocess

from lxml import etree
from typing import Optional
from typing import Sequence
from pathlib import Path

def getResource(filename: str):
    # xsd resources
    resource = {}
    with open(filename, 'rb') as content:
        tree = etree.parse(content)
        root = tree.getroot()
        for child in root.iter('resource'):
            resource[child.attrib['url']] = child.attrib['location'].replace('$PROJECT_DIR$/', '')
    return resource

def getXsd(filename: str):
    with open(filename, 'rb') as content:
        tree = etree.parse(content)
        root = tree.getroot()
        return root.attrib['{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation']

def validate(filename: str, xsd: str) -> bool:
    try:
        schema = ''
        xml = ''
        with open(xsd, 'rb') as content:
            schema = etree.XMLSchema(etree.parse(content))
        with open(filename, 'rb') as content:
            xml = etree.parse(content)
        result = schema.validate(xml)
        if not result:
            log = schema.error_log
            print(log.last_error)
        return result
    except etree.LxmlError as exc:
        print(f'{filename}: Failed to xml parse ({exc})')
        pass

def main(argv: Optional[Sequence[str]] = None) -> int:
    # return flag
    retval = 0
    # xsd resources
    resource = {}
    # path to the tested module
    module = Path.cwd()
    # prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help = 'PHP filenames to check'
    )
    args = parser.parse_args(argv)

    if module.match('**/app/code/*/*'):
        # path to the root of magento
        magento = module.parent.parent.parent.parent
        xsdmap = magento / '.misc.xml'
        if xsdmap.is_file():
            resource = getResource(xsdmap)
        else:
            print('.misc.xml is not generated')
            retval = 1

        for filename in args.filenames:
            xsd = getXsd(filename)
            if xsd and resource[xsd]:
                xsd = magento / resource[xsd]
                result = validate(filename, xsd)
                if not result:
                    retval = 1
            else:
                print('xsd not found')
                retval = 1
    else:
        print(f'{module}: incorrect module path')
        retval = 1

    return retval

if __name__ == '__main__':
    exit(main())
