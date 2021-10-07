import copy
import json
import subprocess
from pathlib import Path

import click
import xmltodict
from dict2xml import dict2xml


@click.command()
@click.option('--fromcommit', help='From commit or branch', required=True)
@click.option('--tocommit', help='To commit or branch', required=True)
@click.option('--packagexml', help='package.xml file name and path', required=True)
@click.option('--outpackagexml', help='Output package.xml file name and path', required=True)
def main(fromcommit, tocommit, packagexml, outpackagexml):

    filelist = subprocess.run(['git', 'diff', '--name-only', fromcommit, tocommit], check=False, stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()

    cleanfiles = []
    for filename in filelist:
        print("Processing " + filename)
        parts = filename.split('/')
        name = parts[-1].split('.')[0] + "."
        cleanfiles.append(name)

    # open the input xml file and read
    # data in form of python dictionary
    # using xmltodict module
    with open(packagexml) as xml_file:

        data_dict = xmltodict.parse(xml_file.read())
        clean_dict = copy.deepcopy(data_dict)

        xml_file.close()

        package = data_dict.get('Package')
        types = package.get('types')

        pos = 0
        for atype in (types):
            name = atype.get('name')
            members = atype.get('members')

            if (not (type(members) == list)):
                members = [members]

            for mem in members:
                lookup = mem + "."
                helper_lookup = mem + "Helper."
                controller_lookup = mem + "Controller."

                if (lookup not in cleanfiles and helper_lookup not in cleanfiles and controller_lookup not in cleanfiles):
                    if (type(clean_dict['Package']['types'][pos]['members']) == list):
                        clean_dict['Package']['types'][pos]['members'].remove(mem)
                    else:
                        clean_dict['Package']['types'][pos]['members'] = []
            pos = pos + 1

        data_dict = copy.deepcopy(clean_dict)
        package = data_dict.get('Package')
        types = package.get('types')

        pos = 0
        tlist = []
        for atype in (types):
            name = atype.get('name')
            members = atype.get('members')
            if (len(members) != 0):
                tlist.append(data_dict['Package']['types'][pos])
            pos = pos + 1

        if (tlist):
            clean_dict['Package']['types'] = tlist
            clean_dict['Package'].pop('@xmlns')

            xml = dict2xml(clean_dict, indent="    ")
            xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + xml
            xml = xml.replace('<Package>', '<Package xmlns="http://soap.sforce.com/2006/04/metadata">')

            with open(outpackagexml, 'w') as fileout:
                fileout.write(xml)
                fileout.write("\n")
        else:
            Path(outpackagexml).unlink(missing_ok=True)


if __name__ == '__main__':
    main()
