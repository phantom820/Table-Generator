from typing import List
from jinja2 import Environment, FileSystemLoader
import json

# Table writer
''' writes the table to html template '''

class TableWriter:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('.'))
        self.template = self.env.get_template("templates/template.html")
        with open('templates/paragraphs.json','r') as f:
            paragraphs = json.load(f)
        self.paragraphs = []
        for key in paragraphs:
            text = "\n".join(paragraphs[key])
            self.paragraphs.append(text)
            
    ''' just write a single table '''
    def write_single(self,table:str)->str:
        tables = [{"header":"Table 1",
                 "table": table,'text':self.paragraphs[0]}]
        template_vars = {"title" : "Sales Funnel Report - National",
                 "tables": tables,"close":self.paragraphs[-1]}
        html_out = self.template.render(template_vars)
        return html_out
    
    ''' write multiple tables '''
    def write(self,tables:List[str])->str:
        result = []
        for i in range(len(tables)):
            t = {"header":"Table "+str(i+1),"table":tables[i],'text':self.paragraphs[i]}
            result.append(t)
        template_vars = {"title" : "Sales Funnel Report - National",
                 "tables": result,"close":self.paragraphs[-1]}
        html_out = self.template.render(template_vars)
        return html_out