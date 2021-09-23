import copy
import json
import subprocess
from pprint import pprint

import click
import xmltodict


@click.command()
@click.option('--fromcommit', help='From commit or branch', required=True)
@click.option('--tocommit', help='To commit or branch', required=True)
@click.option('--packagexml', help='package.xml file name and path', required=True)

def main(fromcommit, tocommit, packagexml):

    filelist = subprocess.run(['git', 'diff', '--name-only', fromcommit, tocommit], check=False, stdout=subprocess.PIPE).stdout.decode('utf-8') 

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
            
            for mem in members:
                lookup = name + "/" + mem + ".class"
                if (lookup in filelist):
                    print(str(pos) + " " + lookup)
                    pprint(data_dict['Package']['types'])
            pos = pos + 1

if __name__ == '__main__':
    main()
