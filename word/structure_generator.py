import re
from typing import List

class StructureGenerator:
    def __init__(self):
        self.expression = '<table|<row|<cell|</cell>|</row>|</table>'
        self.regex = re.compile(self.expression)
    
    ''' clean and format str '''
    def clean(self,table:str)->str:
        line = table
        to_remove = ['w:tblPr','w:tblStyle','w:tblW','w:tblLook','w:tblGrid','w:tcPr','w:tblW','w:type','w:tcW']
        for s in to_remove:
            line = line.replace(s,'*')
        to_replace = ['w:tbl','w:tr','w:tc']
        replacement = ['table','row','cell']
        for i in range(len(to_replace)):
            line = line.replace(to_replace[i],replacement[i])
        line = line.replace('cellr','*')
        return line
    
    ''' markup representing table '''
    def structure(self,table:str)->str:
        table = self.clean(table)
        lines = re.findall(self.regex, table)
        lines = [lines[i]+'>' if lines[i].find(">")==-1 else lines[i] for i in range(len(lines))]
        structure = "\n".join(lines)
        return structure
    
    ''' generate table structures '''
    def structures(self,tables:List[str])->List[str]:
        structures = []
        for table in tables:
            structure = self.structure(table._element.xml)
            structures.append(structure)
        return structures