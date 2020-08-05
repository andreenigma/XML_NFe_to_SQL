__version__ = '0.1.0'

# import Leitor_XML
import xmlschema
from xmlschema import helpers
from pprint import pprint
import pandas as pd


nfe_v4_schema_file = open('./resourse/xsd/NFe/v3.10/nfe_v3.10.xsd')
nfe_v4_base_url = './resourse/xsd/NFe/v3.10/'

nfe_schema = xmlschema.XMLSchema(nfe_v4_schema_file, base_url= nfe_v4_base_url )


# print('________nodes___________________\n')
# for xsd_component in nfe_schema.iter_components(): 
#     pprint (xsd_component)
#     print('______________________________________\n')

# nfe_elem = nfe_schema.elements['NFe']

component_list = nfe_schema.findall('.//*')

# for element in element_list:
#     print('>> element in element_list')
#     pprint(element)
#     print('>> element.type')
#     pprint(element.type)   
#     print('>> element.attributes')
#     pprint(element.attributes)
#     print('>> helpers.get_xsd_annotation(element)')
#     print(helpers.get_xsd_annotation(element))
#     print('>> element_content in element.type.content.iter_elements(): pprint(element_content) ')
#     print('----------------------------------------------------------')
#     for element_content in element.type.content.iter_elements():
#         pprint(element_content)
#         print('>> element_content.type')
#         pprint(element_content.type)        
#     print('**********************************************\n')



# print('XSD built-in types: ', nfe_schema.builtin_types(), sep='\n')

# print('\nroot elements:\n ', nfe_schema.root_elements)

# print('\n****global simple types:\n ')
# for simple_t in nfe_schema.simple_types:
#     print( simple_t)    

# print('\n****global complex types:\n ')
# for complex_t in nfe_schema.complex_types:
#     print(complex_t)
#     print(complex_t.annotation.documentation[0].text)

# print('\n****global definitions or declarations:\n ')
# for global_defs in nfe_schema.iter_globals():
#     pprint(global_defs)

# print('\n****schema components:\n ')
# for component_itr in nfe_schema.iter_components():
#     pprint(component_itr)

# print('\n****components tags:\n')
# for element_group in nfe_schema.iter_components():    
#     print('element tag: ', element_group.tag)
   
print('\n****all components:\n')

for comp in component_list:    

    if comp.type.is_complex(): 

        print('Crida a tabela: ', comp.local_name)
        print('com os seguintes campos: ') 
        # print('\tcampo(chave_secundária):', comp.parent.)  

        for sub_comp in comp.content():

           if sub_comp.type.is_simple():

               print('\tcampo: ', sub_comp.local_name)

            









