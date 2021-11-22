from typing import List
import re

class StructureGenerator:
    def __init__(self):
        self.expression = '<table|<row|<cell|</cell>|</row>|</table>'
        self.regex = re.compile(self.expression)

    ''' markup representing table '''
    def structure(self,table:str)->str:
        html = (table)
        html = html.replace("<thead>\n","")
        html = html.replace("</thead>","")
        html = html.replace("<tr","<row")
        html = html.replace("/tr>","/row>")
        html = html.replace("<th","<td")
        html = html.replace("/th>","/td>")
        html = html.replace("<td","<cell")
        html = html.replace("/td>","/cell>")
        lines = re.findall(self.regex, html)
        lines = [lines[i]+'>' if lines[i].find(">")==-1 else lines[i] for i in range(len(lines))]
        structure = "\n".join(lines)
        return structure
    
    ''' generate table structures '''
    def structures(self,tables:List[str])->List[str]:
        structures = []
        for table in tables:
            structure = self.structure(table)
            structures.append(structure)
        return structures