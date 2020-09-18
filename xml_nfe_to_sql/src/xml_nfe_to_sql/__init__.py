__version__ = '0.1.0'

# import Leitor_XML
import abc
import xmlschema
from xmlschema import helpers
from pprint import pprint
import pandas as pd
import sqlalchemy


# nfe_v4_schema_file = open('./resourse/xsd/NFe/v3.10/nfe_v3.10.xsd')
# nfe_v4_base_url = './resourse/xsd/NFe/v3.10/'

# nfe_schema = xmlschema.XMLSchema(nfe_v4_schema_file, base_url= nfe_v4_base_url )

# component_list = nfe_schema.findall('.//*')
   

class Handler:

    @abc.abstractmethod
    def create_table(table_name: str):
        pass

    @abc.abstractmethod
    def create_field(table_name: str, field: str, type: str):
        pass

    @abc.abstractmethod
    def delete_table(table_name: str):
        pass

    @abc.abstractmethod
    def delete_field(table_name: str, field: str)

    @abc.abstractmethod
    def relationship(table_name: str, foreing_key: str, foreing_table: str, referenced_field: str):
        pass

    

class Parser:
    
    @abc.abstractmethod
    def parse(xmlShema: xmlschema.XMLSchema, handler: Handler):
        print('C')



class ParserDecorator(Parser):

    def __init__(self, wrappee_parser: Parser):
        self.wrappee = wrappee_parser

    def parse(self, xmlschema: xmlshema.XMLSchema, db_randler: Handler):
        print('Executada funcao parse() da classe ParserDecorator base.')



class UnormalizedTablesCreator(Parser):
    """Classe a ser encapsulada por decoradores que chama função no handler para
    criar tabelas SQL não normalizadas. A funcao parce() dessa classe deve ser a
    primeira a ser executada na pilha de decoradores, já que cria as tabelas sobre
    as quais os campos e relacionamentos do banco de dados serão criados.
    """

    def parse(self, xmlschema: xmlshema.XMLSchema, db_randler: Handler):
        component_list = xmlschema.findall('.//*')
        for xsd_component in component_list:
            # faca alguma coisa


class RelationalCreator(ParserDecorator):

    def __init__(self, wrappee_parser: Parser):
        super.__init__(wrappee_parser)

    def parse(self, xmlschema: xmlshema.XMLSchema, db_randler: Handler):
        self.wrappee.parse(xmlschema, db_randler)
        component_list = xmlschema.findall('.//*')
        for xsd_component in component_list:
            # faca alguma coisa 
