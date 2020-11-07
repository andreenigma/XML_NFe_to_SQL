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
    def set_field_type(self, table_name: str, field_name: str, data_type: str):
        pass

    @abc.abstractmethod
    def delete_table(self, table_name: str):
        pass

    @abc.abstractmethod
    def delete_field(self, table_name: str, field_name: str):
        pass

    @abc.abstractmethod
    def primary_key(self, table_name: str) -> str:
        pass

    @abc.abstractmethod
    def relationship(self, foreing_table: str, foreing_key: str, referenced_table_name: str, referenced_field: str):
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

    def parse(self, xmlschema: xmlschema.XMLSchema, db_handler: Handler):
        # Criando lista com todos os componentes do schema, usando XPath API da biblioteca xmlschema. 
        component_list = xmlschema.findall('.//*')

        for xsd_component in component_list:
            if xsd_component.type.has_complex_content():
                db_handler.create_table(xsd_component.local_name) 

                # criando chave primária padrão (id)
                db_handler.create_field(xsd_component.local_name, 'id', 'integer', 8)
                
                # criando colunas além da chave primária
                for child in xsd_component.iterchildren():
                  
                    if child.type.is_simple():                                            
                        db_handler.create_field(xsd_component.local_name, child.local_name, 'string', 10 ) # string e 10 para testes!!!
                       

class RelationalCreator(ParserDecorator):

    def __init__(self, wrappee_parser: Parser):
        super(RelationalCreator, self).__init__(wrappee_parser)

    def parse(self, xmlschema: xmlschema.XMLSchema, db_handler: Handler):
        # executa primeiro a função parse do parser decorado
        self.wrappee.parse(xmlschema, db_handler)

        # executa as operações próprias
        component_list = xmlschema.findall('.//*')

        for xsd_component in component_list:
            for component_child in xsd_component.iterchildren():
                if db_handler.has_table(component_child.local_name):
                    foreing_key_string: str = xsd_component.local_name + '_id'
                    db_handler.create_field(component_child.local_name, foreing_key_string, 'integer', 8)
                    db_handler.relationship(component_child.local_name, foreing_key_string, xsd_component.local_name, db_handler.primary_key(xsd_component.local_name))

        # for xsd_component in component_list:
        #     if xsd_component.parent != None:
        #         print (type(xsd_component.parent.local_name))
        #         foreing_key_string = str(xsd_component.parent.local_name) + '_id'
        #         db_randler.create_field(xsd_component.local_name, foreing_key_string, 'interger', 8)
        #         db_randler.relationship(xsd_component.local_name, foreing_key_string, xsd_component.parent.local_name, 'id')







# =================================================================================


class TableStruct:

    def __init__(self, table_name: str = None, primary_key_name: str = None):
        self.name = table_name
        self.primary_key = primary_key_name
        
        
        
class FieldStruct:

    def __init__(self, table_name: str, field_name: str, data_type: str = None, length: int = 8, auto_increment: bool = False, not_null: bool = False, unique_index: bool = False, binary_column: bool = False, unsigned_type: bool = False, fill_w_zero: bool = False, generated_column: bool = False):
        self.table = table_name
        self.name = field_name
        self.type = data_type
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
                new_field = FieldStruct(table_name, field_name, type_name, length)
                self.data_base_map.field_list.append(new_field)

                # # PRINT TEMPORARIO PARA TESTES
                # print(f'{table.name} == {table_name}')
                # print(f'apensado o campo \t{new_field.name}\t na tabela\t {table.name}')

                # field_counter = 0

                # for field in self.data_base_map.field_list:
                #     if field.table == table.name:
                #         field_counter += 1

                # print(f'agora existem {field_counter} campos na tabela {table.name}')
             
    def set_field_type(self, table_name: str, field_name: str, data_type: str):
        for field in self.data_base_map.field_list:
            if field.table == table_name and field.name == field_name:
                field.type = data_type
        
    def delete_table(self, table_name: str):
        for table in self.data_base_map.table_list:
            if table.name == table_name:
                self.data_base_map.table_list.remove(table)

        for field in self.data_base_map.field_list:
            if field.table == table_name:
                self.data_base_map.field_list.remove(field)
    
    def delete_field(self, table_name: str, field_name: str):
        for field in self.data_base_map.field_list:
            if field.table == table_name and field.name == field_name:
                self.data_base_map.field_list.remove(field)

    def primary_key(self, table_name: str) -> str:
        primary_key_name = ''

        for table in self.data_base_map.table_list:
            if table.name == table_name:
                primary_key_name = table.primary_key

        return primary_key_name
    
    def relationship(self, foreing_key: str, foreing_table: str, referenced_table_name: str, referenced_field: str):
        relationship_struct = RelationshipStruct(referenced_table_name, foreing_table, referenced_field, foreing_key)
        self.data_base_map.relationship_list.append(relationship_struct)
    
    def delete_relationship(self, foreing_table_name: str, foreing_key: str):
        for relationship in self.data_base_map.relationship_list:
            if relationship.foreing_table and relationship.foreing_key:
                self.data_base_map.relationship_list.remove(relationship)

   
    def has_table(self, table_name: str) -> bool:
        has_table_var = False

        for table in self.data_base_map.table_list:
            if table.name == table_name:
                has_table_var = True

        return has_table_var
    
    def has_field(self, table_name: str, field_name: str) -> bool:
        has_field_var = False

        for field in self.data_base_map.field_list:
            if field.name == field_name and field.table == table_name:
                has_field_var = True
                pass

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




print('Foram criadas os seguintes relacionamentos')

for relationship in handler.data_base_map.relationship_list:
    print('Foreing table: ' + relationship.foreing_table)
    print('Foreing key: ' + relationship.foreing_key)    
    print('Primary table: ' + str(relationship.primary_table))





# print('Foram criadas as seguintes tabelas: ')

# for table in handler.table_list:
#     print(table.name)
#     # print(f'com {len(table.fields)} campos')
#     entrada = input('mostrar campos? (s/n)')

#     if entrada == 's':
#         print('campos: ')

#         for field in table.fields:
#             print(field.name)
