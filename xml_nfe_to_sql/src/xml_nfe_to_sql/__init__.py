__version__ = '0.1.0'

# import Leitor_XML
import abc
import io
import xmlschema
from xmlschema import helpers
from pprint import pprint
import pandas as pd
import sqlalchemy



# component_list = nfe_schema.findall('.//*')
   

class Handler:

    @abc.abstractmethod
    def create_table(self, table_name: str):
        pass

    @abc.abstractmethod
    def create_field(self, table_name: str, field_name: str, type_name: str = 'VARCHAR', length: int = 40):
        pass

    @abc.abstractmethod
    def set_field_type(self, table_name: str, field_name: str, type: str):
        pass

    @abc.abstractmethod
    def delete_table(self, table_name: str):
        pass

    @abc.abstractmethod
    def delete_field(self, table_name: str, field_name: str):
        pass

    @abc.abstractmethod
    def relationship(self, foreing_key: str, foreing_table: str, referenced_table_name: str, referenced_field: str):
        pass

    @abc.abstractmethod
    def delete_relationship(self, foreing_table_name: str, foreing_key: str):
        pass

    @abc.abstractmethod
    def has_table(self, table_name: str) -> bool:
        pass

    @abc.abstractmethod
    def has_field(self, table_name: str, field_name: str) -> bool:
        pass 



class Parser:
    
    @abc.abstractmethod
    def parse(self, xmlShema: xmlschema.XMLSchema, handler: Handler):
        print('C')



class ParserDecorator(Parser):

    def __init__(self, wrappee_parser: Parser):
        self.wrappee = wrappee_parser

    def parse(self, xmlschema: xmlschema.XMLSchema, db_randler: Handler):
        print('Executada funcao parse() da classe ParserDecorator base.')



class UnormalizedTablesCreator(Parser):
    """Classe a ser encapsulada por decoradores que chama função no handler para
    criar tabelas SQL não normalizadas. A funcao parce() dessa classe deve ser a
    primeira a ser executada na pilha de decoradores, já que cria as tabelas sobre
    as quais os campos e relacionamentos do banco de dados serão criados.
    """

    def parse(self, xmlschema: xmlschema.XMLSchema, db_randler: Handler):
        # Criando lista com todos os componentes do schema, usando XPath API da biblioteca xmlschema. 
        component_list = xmlschema.findall('.//*')

        for xsd_component in component_list:
            if xsd_component.type.has_complex_content():
                db_randler.create_table(xsd_component.local_name) 
                # print('==============================================================')
                # print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                # print('==============================================================')
                # print('Criada a tabela: ' + xsd_component.local_name)
                
                for child in xsd_component.iterchildren():
                    # print ('iterou no child: ' + child.local_name)
                    # pprint (child.type)                    

                    if child.type.is_simple():                                            
                        db_randler.create_field(xsd_component.local_name, child.local_name, 'string', 10 ) # string e 10 para testes!!!
                        # print('\t criado o campo: ' + child.local_name)


class RelationalCreator(ParserDecorator):

    def __init__(self, wrappee_parser: Parser):
        super(RelationalCreator, self).__init__(wrappee_parser)

    def parse(self, xmlschema: xmlschema.XMLSchema, db_randler: Handler):
        self.wrappee.parse(xmlschema, db_randler)

        component_list = xmlschema.findall('.//*')

        for xsd_component in component_list:
            pass 



# =================================================================================


class TableStruct:

    def __init__(self, table_name: str = None, field_tuple: tuple = ()):
        self.name = table_name
        self.fields = field_tuple
        
        
class FieldStruct:

    def __init__(self, field_name: str, data_type: str = None, length: int = 8, auto_increment: bool = False, not_null: bool = False, unique_index: bool = False, binary_column: bool = False, unsigned_type: bool = False, fill_w_zero: bool = False, generated_column: bool = False):
        self.name = field_name
        self.column_type = data_type
        self.data_length = length
        self.is_auto_increment = auto_increment
        self.is_not_null = not_null
        self.is_unique_index = unique_index
        self.is_binary_column = binary_column
        self.is_unsigned_data_type = unsigned_type
        self.fill_with_zero = fill_w_zero
        self.generated_column = generated_column


class RelationshipStruct:

    def __init__(self, primary_tabe_name: str = None, foreing_table_name: str = None, primary_key_name: str = None, foreing_key_name: str = None):
        self.primary_table = primary_tabe_name
        self.foreing_table = foreing_table_name
        self.primary_key = primary_key_name
        self.foreing_key = foreing_key_name


class DataBaseStruct:

     def __init__(self):
        self.table_list = []
        self.field_list = []
        self.relationship_list = []
       

class MetaProgramingHandler(Handler): 
    data_base_map = DataBaseStruct()

    code = ''
        
    def create_table(self, table_name: str):
        self.data_base_map.table_list.append(TableStruct(table_name))
   
    def create_field(self, table_name: str, field_name: str, type_name: str = 'VARCHAR', length: int = 40):
        for table in self.data_base_map.table_list:
            if table.name == table_name:
                new_field = FieldStruct(field_name, type_name, length)
                table.fields += (new_field,)

                # PRINT TEMPORARIO PARA TESTES
                print(f'{table.name} == {table_name}')
                print(f'apensado o campo \t{new_field.name}\t na tabela\t {table.name}')
                print(f'agora existem {len(table.fields)} campos na tabela {table.name}')
             
    def set_field_type(self, table_name: str, field_name: str, type: str):
        for table in self.data_base_map.table_list:
            if table.name == table_name:
                for field in table.fields:
                    if field.name == field_name:
                        field.column_type = type
        
    def delete_table(self, table_name: str):
        for table in self.data_base_map.table_list:
            if table.name == table_name:
                self.data_base_map.table_list.remove(table)
    
    def delete_field(self, table_name: str, field_name: str):
        for table in self.data_base_map.table_list:
            if table.name == table_name:
                for field in table.fields:
                    if field.name == field_name:
                        table.fields.remove(field)
    
    def relationship(self, foreing_key: str, foreing_table: str, referenced_table_name: str, referenced_field: str):
        relationship_struct = RelationshipStruct(referenced_table_name, foreing_table, referenced_field, foreing_key)
        self.relationship_list.append(relationship_struct)
    
    def delete_relationship(self, foreing_table_name: str, foreing_key: str):
        for relationship in self.relationship_list:
            if relationship.foreing_table and relationship.foreing_key:
                self.relationship_list.remove(relationship)

   
    def has_table(self, table_name: str) -> bool:
        has_table_var = False

        for table in self.table_list:
            if table.name == table_name:
                has_table_var = True

        return has_table_var
    
    def has_field(self, table_name: str, field_name: str) -> bool:
        has_field_var = False

        for table in self.table_list:
            if table.name == table_name:
                for field in table.fields:
                    if field.name == field_name:
                        has_field_var = True

        return has_field_var


# =============================================================================


nfe_v4_schema_file = open('./resourse/xsd/NFe/v3.10/nfe_v3.10.xsd')
nfe_v4_base_url = './resourse/xsd/NFe/v3.10/'

nfe_schema = xmlschema.XMLSchema(nfe_v4_schema_file, base_url= nfe_v4_base_url )

parser_a = UnormalizedTablesCreator()
parser_b = RelationalCreator(parser_a)

handler = MetaProgramingHandler()

parser_b.parse(nfe_schema, handler)




# print('Foram ciradas as seguintes tabelas: ')

# for table in handler.table_list:
#     print(table.name)
#     print('com os seguintes campos: ')

#     for field in table.fields:
#         print(field.name)




# print('Foram criadas os seguintes relacionamentos')

# for relationship in handler.relationship_list:
#     print('Foreing table: ' + relationship.foreing_table)
#     print('Foreing key: ' + relationship.foreing_key)
#     print('Primary table: ' + relationship.primary_table)





# print('Foram criadas as seguintes tabelas: ')

# for table in handler.table_list:
#     print(table.name)
#     # print(f'com {len(table.fields)} campos')
#     entrada = input('mostrar campos? (s/n)')

#     if entrada == 's':
#         print('campos: ')

#         for field in table.fields:
#             print(field.name)
