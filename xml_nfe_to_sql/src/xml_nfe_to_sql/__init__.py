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
        raise NotImplementedError()

    @abc.abstractmethod
    def create_field(self, table_name: str, field_name: str, type_name: str = 'VARCHAR', length: int = 40):
        raise NotImplementedError()

    @abc.abstractmethod
    def set_field_type(self, table_name: str, field_name: str, data_type: str):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_table(self, table_name: str):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_field(self, table_name: str, field_name: str):
        raise NotImplementedError()

    @abc.abstractmethod
    def primary_key(self, table_name: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def relationship(self, foreing_table: str, foreing_key: str, referenced_table_name: str, referenced_field: str):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_relationship(self, foreing_table_name: str, foreing_key: str):
        raise NotImplementedError()

    @abc.abstractmethod
    def has_table(self, table_name: str) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def has_field(self, table_name: str, field_name: str) -> bool:
        raise NotImplementedError() 



class Parser:
    
    @abc.abstractmethod
    def parse(self, xmlShema: xmlschema.XMLSchema, handler: Handler):
        raise NotImplementedError()



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

    def is_element_only_single_content(self, xsd_component: xmlschema.XsdComponent) -> bool:
        element_only_sigle_content = False
        
        if xsd_component.type.is_element_only():
            child_element_count = 0
            for child in xsd_component.iterchildren():                  
                if child.type.is_simple():
                    child_element_count += 1

            if child_element_count == 1: element_only_sigle_content = True

        return element_only_sigle_content        


    def parse(self, xmlschema: xmlschema.XMLSchema, db_handler: Handler):
        # Criando lista com todos os componentes do schema, usando XPath API da biblioteca xmlschema. 
        component_list = xmlschema.findall('.//*')        

        for xsd_component in component_list:

            has_complex_content = xsd_component.type.has_complex_content()                          
            
            if has_complex_content and not self.is_element_only_single_content(xsd_component):
                db_handler.create_table(xsd_component.local_name)                

                # criando chave primária padrão (id)
                db_handler.create_field(xsd_component.local_name, 'id', 'integer', 8)
                
                # criando colunas além da chave primária
                for child in xsd_component.iterchildren():

                    if self.is_element_only_single_content(child):
                        single_content_name = ''

                        for iner_child in child.iterchildren():
                            single_content_name = iner_child.local_name

                        db_handler.create_field(xsd_component.local_name, single_content_name, 'string', 10)

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
                # verifica se o componente corresponde a uma tabela sql
                if db_handler.has_table(component_child.local_name):
                    for parent_component in component_child.iter_ancestors():
                        # verifica se o componente pai corresponde a uma tabela sql
                        if db_handler.has_table(parent_component.local_name):
                            foreing_key_string: str = parent_component.local_name + '_id'
                            db_handler.create_field(component_child.local_name, foreing_key_string, 'integer', 8)
                            db_handler.relationship(component_child.local_name, foreing_key_string, parent_component.local_name, db_handler.primary_key(parent_component.local_name))
                            break



# =================================================================================

class CodeVisitor:
    
    @abc.abstractmethod
    def list_variable(self, name: str, list_attribute: list) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def dictionary_variable(self, name: str, pair: dict) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def string_variable(self, name: str, str_value: str) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def boolean_variable(self, name: str, value: bool) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def integer_variable(self, name: str, value) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def decimal_variable(self, name: str, value) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def type_name(self, object_type_name: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def class_declaration(self, name: str, inherited_class_list: list = [], open_definition: bool = False) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def function_declaration(self, name: str, parameter_dictionary: dict = {}, return_type: str = '', open_definition = False) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def function_call(self, name: str, parameter_dictionary: dict = {}) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def open_block(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def close_block(self) -> str:
        raise NotImplementedError()

# ==========================================================================================================   

class DbVisitedElement:
   
    @abc.abstractmethod
    def accept(self, visitor: CodeVisitor):
        raise NotImplementedError()


class DbLeafElement(DbVisitedElement):

    def __init__(self, name: str):
        self.name = name

    @property
    def name(self) -> str:
        return self.name

class DbCompositeElement(DbLeafElement):
    def __init__(self, name: str):
        super().__init__(name)
        self.children = []

    @abc.abstractmethod
    def accept(self, visitor: CodeVisitor):
        raise NotImplementedError

    def add(self, child: DbVisitedElement):
        self.children.append(child)
  
    def remove(self, child: DbVisitedElement):
        self.children.remove(child)

    def chid_instance(self, child_name: str) -> DbVisitedElement:

        instance = None

        for child in self.children:
            if child.name == child_name:
                instance = child
             
        return instance
    

class ColumnStruct(DbLeafElement):

    def __init__(self, column_name: str = None, data_type: str = None, length: int = 8, auto_increment: bool = False, not_null: bool = False, unique_index: bool = False, binary_column: bool = False, unsigned_type: bool = False, fill_w_zero: bool = False, generated_column: bool = False):
        super().__init__(column_name)
        self.type = data_type
        self.data_length = length
        self.is_auto_increment = auto_increment
        self.is_not_null = not_null
        self.is_unique_index = unique_index
        self.is_binary_column = binary_column
        self.is_unsigned_data_type = unsigned_type
        self.fill_with_zero = fill_w_zero
        self.generated_column = generated_column

    def accept(self, visitor: CodeVisitor):
        visitor.type_name(type(self))
        visitor.string_variable('name', self.name)
        visitor.string_variable('type', self.type)
        visitor.integer_variable('data_length', self.data_length)
        visitor.boolean_variable('is_auto_increment', self.is_auto_increment)
        visitor.boolean_variable('is_not_null', self.is_not_null)
        visitor.boolean_variable('is_unique_index', self.is_unique_index)
        visitor.boolean_variable('is_binary_column', self.is_binary_column)
        visitor.boolean_variable('is_unsigned_data_type', self.is_unsigned_data_type)
        visitor.boolean_variable('fill_with_zero', self.fill_with_zero)
        visitor.boolean_variable('generated_column', self.generated_column)


class TableStruct(DbCompositeElement):

    def __init__(self, table_name: str):
        super().__init__(table_name)
        
    def accept(self, visitor: CodeVisitor):
        visitor.type_name(type(self))
        visitor.string_variable('name', self.name)
        visitor.open_block()

        for child in self.children:
            child.accept(visitor)

        visitor.close_block()

    def add(self, child: DbVisitedElement):
        if type(child) == type(ColumnStruct()):
            super().add(child)

        else: print('O objeto de nome ' + child.name + ' não é um ColumnStruct!!')



class RelationshipStruct(DbVisitedElement):

    def __init__(self, primary_tabe_name: str = None, foreing_table_name: str = None, primary_key_name: str = None, foreing_key_name: str = None):
        self.primary_table = primary_tabe_name
        self.foreing_table = foreing_table_name
        self.primary_key = primary_key_name
        self.foreing_key = foreing_key_name

    def accept(self, visitor: CodeVisitor):
        visitor.type_name(type(self))
        visitor.open_block()
        visitor.string_variable('primary_table', self.primary_table)
        visitor.string_variable('primary_key', self.primary_key)          
        visitor.string_variable('foreing_table', self.foreing_table)
        visitor.string_variable('foreing_key', self.foreing_key)
        visitor.open_block()             
        
            

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
    
    def relationship(self, foreing_table: str, foreing_key: str, referenced_table_name: str, referenced_field: str):
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





