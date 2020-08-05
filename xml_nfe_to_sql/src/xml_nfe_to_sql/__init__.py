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
   
# print('\n****all components:\n')

# for comp in component_list:    

#     if comp.type.is_complex(): 

#         print('Crida a tabela: ', comp.local_name)
#         print('com os seguintes campos: ') 
#         # print('\tcampo(chave_secundária):', comp.parent.)  

#         for sub_comp in comp.iter_components(xsd_classes=xmlschema.XsdElement):

#            if sub_comp.type.is_simple():

#                print('\tcampo: ', sub_comp.local_name)



# class BaseHandler:
#     def __init__(self, stream):
#         self._stream_obj = stream

#     def 



def schema_iterate(schema: xmlschema.XsdComponent, handler=None):

    for component in schema.iter_components(xsd_classes=xmlschema.XsdElement):
        if component.type.is_complex():          
            columns_components = []
            complex_components = []

            for sub_comp in component.iter_components(xsd_classes=xmlschema.XsdElement):
                if sub_comp.type.is_simple():
                    columns_components.append(sub_comp)

                elif sub_comp.type.is_complex():
                    complex_components.append(sub_comp)


            if columns_components:
                print('Tipo complexo de nome ', component.local_name)
                print('Criar tabela com os seguintes campos? ')
                
                for s_comp in columns_components:
                    print(s_comp.local_name)

            if complex_components:
                for c_comp in complex_components:
                    schema_iterate(c_comp)



schema_iterate(nfe_schema)


# for comp in nfe_schema.iter_components(xsd_classes=xmlschema.XsdElement):    

#     if comp.type.is_complex(): 

#         print('Crida a tabela: ', comp.local_name)
#         print('com os seguintes campos: ') 
#         # print('\tcampo(chave_secundária):', comp.parent.)  

#         for sub_comp in comp.iter_components(xsd_classes=xmlschema.XsdElement):

#            if sub_comp.type.is_simple():

#                print('\tcampo: ', sub_comp.local_name)

#             elif sub_comp.type.is_complex():
 










