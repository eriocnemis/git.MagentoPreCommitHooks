#!/usr/bin/env python3

import argparse
import subprocess

from lxml import etree
from typing import List
from typing import Optional
from typing import Sequence
from pathlib import Path

"""
Return a dictionary of every urn and corresponding absolute path
associated with it.
"""
def getSchemas(filename: str, path: str) -> List[str]:
    schemas = {}
    with open(filename, 'rb') as content:
        tree = etree.parse(content)
        root = tree.getroot()
        for child in root.iter('resource'):
            location = child.attrib['location'].replace('$PROJECT_DIR$/', '')
            schemas[child.attrib['url']] = f'{path}/{location}'
        return schemas
    raise ValueError('Cannot open a file %r' % filename)

"""
Return a schema location based on attribute xsi:noNamespaceSchemaLocation.
"""
def getUrn(filename: str) -> str:
    parser = etree.XMLParser()
    with open(filename, 'rb') as content:
        tree = etree.parse(content)
        root = tree.getroot()
        for attr in root.attrib:
            if 'noNamespaceSchemaLocation' in attr:
                return root.attrib.get(attr)
        raise ValueError('Cannot parse %r - not a attribute xsi:noNamespaceSchemaLocation' % filename)
    raise ValueError('Cannot open a file %r' % filename)

"""
Return result of validation XML documents against an XML schema
definition language(XSD) schema.
"""
def validate(filename: str, urn: str, schemas) -> bool:
    """
    Return a callable for the specified schemas which can be used
    to validate xml documents.
    """
    class SchemaResolver(etree.Resolver):
        def __init__(self, schemas, *args, **kwargs):
            super(SchemaResolver, self).__init__(*args, **kwargs)
            self.schemas = schemas

        def resolve(self, url, pubid, context):
            if url in self.schemas:
                url = self.schemas[url]
                return self.resolve_filename(url, context)
            raise ValueError('Cannot resolve %r - not a known schema' % url)

    parser = etree.XMLParser()
    parser.resolvers.add(SchemaResolver(schemas))

    with open(urn, 'rb') as schemaContent, open(filename, 'rb') as xmlContent:
        schema = etree.XMLSchema(etree.parse(schemaContent, parser))
        xml = etree.parse(xmlContent, parser)
        result = schema.validate(xml)
        if not result:
            print(schema.error_log)
        return result
    raise ValueError('Cannot open a file %r' % filename)

"""
Return result of validation XML files.
"""
def main(argv: Optional[Sequence[str]] = None) -> int:
    # return flag
    retval = 0
    # path to the tested module
    module = Path.cwd()
    # prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help = 'Xml filenames to check'
    )
    args = parser.parse_args(argv)

    if module.match('**/app/code/*/*'):
        # path to the root of magento
        magento = module.parent.parent.parent.parent
        dictionary = magento / '.misc.xml'
        if dictionary.is_file():
            try:
                schemas = getSchemas(dictionary, magento)
                for filename in args.filenames:
                    urn = getUrn(filename)
                    if urn and schemas[urn]:
                        urn = magento / schemas[urn]
                        result = validate(filename, urn, schemas)
                        if not result:
                            retval = 1
                    else:
                        print('urn not found')
                        retval = 1
            except etree.LxmlError as exc:
                print(f'{filename}: Failed to xml parse ({exc})')
                retval = 1
        else:
            print('.misc.xml is not generated')
            retval = 1
    else:
        print(f'{module}: incorrect module path')
        retval = 1

    return retval

if __name__ == '__main__':
    exit(main())
