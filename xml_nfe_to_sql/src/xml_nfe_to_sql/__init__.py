__version__ = '0.1.0'

# import Leitor_XML
import abc
import xmlschema
from xmlschema import helpers
from pprint import pprint
import pandas as pd
import sqlalchemy


nfe_v4_schema_file = open('./resourse/xsd/NFe/v3.10/nfe_v3.10.xsd')
nfe_v4_base_url = './resourse/xsd/NFe/v3.10/'

nfe_schema = xmlschema.XMLSchema(nfe_v4_schema_file, base_url= nfe_v4_base_url )

component_list = nfe_schema.findall('.//*')
   

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
        pass


class ParserDecorator(Parser):

    def __init__(self, wrappee_parser: Parser):
        self.wrappee = wrappee_parser

    def parse(self, xmlschema: xmlshema.XMLSchema, db_randler: Handler):
        pass

