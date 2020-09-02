__version__ = '0.1.0'

# import Leitor_XML
import xmlschema
from xmlschema import helpers
from pprint import pprint
import pandas as pd


nfe_v4_schema_file = open('./resourse/xsd/NFe/v3.10/nfe_v3.10.xsd')
nfe_v4_base_url = './resourse/xsd/NFe/v3.10/'

nfe_schema = xmlschema.XMLSchema(nfe_v4_schema_file, base_url= nfe_v4_base_url )

component_list = nfe_schema.findall('.//*')
   

# def schema_iterate(schema: xmlschema.XsdComponent, handler=None):

#     component_list = schema.findall('.//*')

#     # for component in schema.iter_components(xsd_classes=xmlschema.XsdElement):
#     for component in component_list:
#         if component.type.is_complex():          
#             columns_components = []
#             complex_content = []
            
#             # for sub_comp in component.iter_components(xsd_classes=xmlschema.XsdElement):
#             for sub_comp in component.iterchildren():
#                 if sub_comp.type.is_simple():
#                     columns_components.append(sub_comp)

#                 if sub_comp.type.is_complex():
#                     complex_content.append(sub_comp)
            
#             print('Tipo complexo de nome ', component.local_name)

#             if component.attributes:
#                 print('tem os seguintes atributos:')
#                 for att in component.attributes:
#                     print(att)

          
#             if columns_components:               
#                 print('Criar tabela com os seguintes campos: ')
                
#                 for s_comp in columns_components:
#                     print('\t', s_comp.local_name)

#             if complex_content:               
#                 print('\t contem os seguintes tipos complexos: ')
                
#                 for c_comp in complex_content:
#                     print('\t \t', c_comp.local_name)
            

# schema_iterate(nfe_schema)

class DbBuilder:
    
    def create_table(self, name: str, fields = {}):
        #experimental para testes
        print('Contruindo a tabela {table}'.format(table = name))

    def create_field(self, table_name: str, field_name: str, type_name: str, type_length):
        #experimental para testes
        print('Criado o campo {field} na seguinte tabela {table}'.format(field=field_name,
        table= table_name ))


def create_tables(xml_schema: xmlschema.XMLSchema, db_builder):
    component_list = xml_schema.findall('.//*')

    # varredura dos componentes
    for schema_component in component_list:
