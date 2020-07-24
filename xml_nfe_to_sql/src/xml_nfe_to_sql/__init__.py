__version__ = '0.1.0'

# import Leitor_XML
import xmlschema
from pprint import pprint

nfe_v4_schema_file = open('./resourse/xsd/NFe/v3.10/procNFe_v3.10.xsd')

nfe_schema = xmlschema.XMLSchema(nfe_v4_schema_file, base_url= './resourse/xsd/NFe/v3.10/' )

nfe_schema_tabular = xmlschema.XMLSchema(nfe_v4_schema_file, base_url= './resourse/xsd/NFe/v3.10/', converter= xmlschema.ColumnarConverter)


for xsd_component in nfe_schema.iter_globals():
    pprint (xsd_component)

print('teste de run do arquvo __init__.py')

print('========================================\n')

pprint(nfe_schema_tabular.to_dict)

print('========================================\n')

nfeProc_element = nfe_schema.elements['nfeProc']
print('nfeProc_element.schema: ')
pprint(nfeProc_element.schema)
print('nfeProc_element.elem:')
pprint(nfeProc_element.elem)
print('nfeProc_elem.attribute:')
pprint(nfeProc_element.attributes)






