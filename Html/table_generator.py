from typing import List
import re
# Table Generator
''' Wraps a generated tabular around a table and adds a caption. 
Also draws borders for use later in making table mask. 
The expected input is a html format string coming from the template or complex template generator.'''

class TableGenerator:
    def __init__(self):
        self.transparent = ' bgcolor="white"'
        self.colour = ' bgcolor="green"'
        
    def outlined_table(self,template:str)->str:
        template = template.replace('<table',''.join(['<table',self.colour]))
        template = re.sub(r'<tr.+>', '<tr>', template)
        return template
        
    def outlined_tables(self,templates:List[str])->List[str]:
        tables = []
        for template in templates:
            table = self.outlined_table(template)
            tables.append(table)
        return tables
        
    def table(self,template:str)->str:
        template = template.replace('<table',''.join(['<table',self.transparent]))
        return template
    
    def tables(self,templates:List[str])->List[str]:
        tables = []
        for template in templates:
            table = self.table(template)
            tables.append(table)
        return tables
        