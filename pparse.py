# Program to convert an xml
# file to json file
 
# import json module and xmltodict
# module provided by python
import json
import xmltodict
from pprint import pprint
 
# open the input xml file and read
# data in form of python dictionary
# using xmltodict module
with open('/Users/steve/git/pparse/package.xml') as xml_file:
     
    data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()
     
    package = data_dict.get('Package')
    types = package.get('types')

    for atype in (types):
        name = atype.get('name')
        members = atype.get('members') 
        
        for mem in members:
            print(name + "/" + mem + ".class")
            text_file = open(name + "/" + mem + ".class", "w")
            text_file.write('Welcome to pythonexamples.org')
            text_file.close()

    # generate the object using json.dumps()
    # corresponding to json data