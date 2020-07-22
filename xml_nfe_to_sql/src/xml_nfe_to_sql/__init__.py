__version__ = '0.1.0'

# import Leitor_XML
import xmlschema
from pprint import pprint

nfe_v4_schema_file = open('D:/XML_NFe_to_SQL/xml_nfe_to_sql/resourse/xsd/NFe/v3.10/leiauteNFe_v3.10.xsd')

# nfe_schema = xmlschema.XMLSchema(nfe_v4_schema_file, base_url= 'D:/XML_NFe_to_SQL/xml_nfe_to_sql/resourse/xsd/NFe/v3.10/' )

nfe_schema = xmlschema.XMLSchema(nfe_v4_schema_file)

# print (nfe_schema.is_valid('D:/OneDrive/Documentos/TRABALHO/AFE 07/Ressarcimento ICMS/E04 079 1502 2018 APPLE COMPUTER BRASIL LTDA - rest de ICMS ST pago a maior - erro de calculo/NFEs dez-2017/NFE_35171200623904000335550010036024861420964251.xml'))

# pprint (nfe_schema.to_dict('D:/OneDrive/Documentos/TRABALHO/AFE 07/Ressarcimento ICMS/E04 079 1502 2018 APPLE COMPUTER BRASIL LTDA - rest de ICMS ST pago a maior - erro de calculo/NFEs dez-2017/NFE_35171200623904000335550010036024861420964251.xml'))

# print (nfe_schema.validate('D:/OneDrive/Documentos/TRABALHO/AFE 07/Ressarcimento ICMS/E04 079 1502 2018 APPLE COMPUTER BRASIL LTDA - rest de ICMS ST pago a maior - erro de calculo/NFEs dez-2017/NFE_35171200623904000335550010036024861420964251.xml'))

for xsd_component in nfe_schema.iter_components():
    print (xsd_component)

print('teste de run do arquvo __init__.py')


