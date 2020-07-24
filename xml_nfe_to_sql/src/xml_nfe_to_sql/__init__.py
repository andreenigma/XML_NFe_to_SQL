__version__ = '0.1.0'

# import Leitor_XML
import xmlschema
from pprint import pprint
import pandas as pd

nfe_v4_schema_file = open('./resourse/xsd/NFe/v3.10/procNFe_v3.10.xsd')

nfe_schema = xmlschema.XMLSchema(nfe_v4_schema_file, base_url= './resourse/xsd/NFe/v3.10/', converter=xmlschema.ParkerConverter )




print('______________________________________\n')
for xsd_component in nfe_schema.iter_components():    
    pprint (xsd_component)
    print('______________________________________\n')

# print('teste de run do arquvo __init__.py')

# print('========================================\n')

# print('ColumnarConverter: \n')
# pprint(nfe_schema.to_dict(nfe_xml_document, dict_class=dict, indent=4))

# print('========================================\n')

nfeProc_element = nfe_schema.elements['nfeProc']
print('nfeProc_element.schema: ')
pprint(nfeProc_element.schema)
print('nfeProc_element.elem:')
pprint(nfeProc_element.elem)
print('nfeProc_elem.attribute:')
pprint(nfeProc_element.attributes)

det = nfe_schema.elements['nfeProc']
print('det.maps: ')
pprint(nfe_schema.maps.elements[det.qualified_name])






