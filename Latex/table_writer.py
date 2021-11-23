from typing import List
import json 
import numpy as np

# Table Writer
''' Uses a default latex template and writes tables to it 
(Includes writing random text), which can later be converted to pdf.'''

class TableWriter:    
    def __init__(self):
        self.begin = '\\begin{document}\n'
        self.end = '\\end{document}'
        
        with open('templates/template.tex','r') as f:
            template = "".join(f.readlines())
            
        with open('templates/paragraphs.json','r') as f:
            paragraphs = json.load(f)
            
        self.template = template
        self.paragraphs = []
        for key in paragraphs:
            text = "\n".join(paragraphs[key])
            self.paragraphs.append(text)
            
    ''' just write a single table '''
    def write_single(self,table:str)->str:
        text = self.paragraphs[0]
        data = "".join([self.begin,'\n',text,'\n',table,"\n",self.end])
        template = "".join([self.template,'\n',data])
        return template
    
    ''' write multiple tables '''
    def write(self,tables:List[str])->str:
        data = '\n'
        texts = self.paragraphs
        for i in range(len(tables)):
            table = tables[i]
            if i<len(texts):
                text = texts[i]
            else:
                j = np.random.randint(0,len(texts)-1)
                text = texts[j]
            data = "".join([data,text,'\n\n',table,'\n\n'])
        
        data = "".join([data,texts[-1],'\n\n'])
        data = "".join([self.begin,data,"\n",self.end])
        template = "".join([self.template,data])
        return template    