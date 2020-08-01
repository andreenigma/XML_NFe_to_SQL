__version__ = '0.1.0'

# import Leitor_XML
import xmlschema
from pprint import pprint
import pandas as pd


nfe_v4_schema_file = open('./resourse/xsd/NFe/v3.10/nfe_v3.10.xsd')
nfe_v4_base_url = './resourse/xsd/NFe/v3.10/'

nfe_schema = xmlschema.XMLSchema(nfe_v4_schema_file, base_url= nfe_v4_base_url )



print('______________________________________\n')
for xsd_component in nfe_schema.iter_components():    
    pprint (xsd_component)
    print('______________________________________\n')

nfe_elem = nfe_schema.elements['NFe']

element_list = nfe_schema.findall('.//*')

for element in element_list:
    pprint(element)
    print(' e do tipo: ')
    pprint(element.type)
    # print('annotation:')
    # annotation = xmlschema.XsdAnnotation(element)
    # pprint(annotation.documentation)
    print('com os seguines atributos:')
    pprint(element.attributes)
    print('e com o seguintes conteudos (contents)')
    for element_content in element.type.content.iter_elements():
        pprint(element_content)
    print('**********************************************\n')











