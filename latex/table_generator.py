from typing import List

class TableGenerator:
    def __init__(self):
        self.top = '\\begin{table}[h]\n\centering\n\caption{*}\n\\vspace{1mm}\n'
        self.bottom = '\\end{table}'
        
    def outlined_table(self,template:str,caption:str="Table",mode="simple")->str:
        if mode=="simple":
            top = self.top.replace("*",caption)
            separation = '\\setlength{\\fboxsep}{1pt}\n'
            border = "".join([separation,'\\fcolorbox{red}{white}{\n'])
            bottom = self.bottom
            table = "".join([top,border,template[:-1],'}\n',bottom])
            return table
                             
        elif mode=="complex":
            top = self.top.replace("*",caption)
            border = '\\fcolorbox{red}{white}{\n'
            bottom = self.bottom
            table = "".join([top,border,template[:-1],'}\n',bottom])
            table = table.replace("fcolorbox{white}","fcolorbox{red}")
            return table
    
    def outlined_tables(self,templates:List[str],mode="simple")->List[str]:
        tables = []
        for template in templates:
            table = self.outlined_table(template,mode=mode)
            tables.append(table)
        return tables
        
    def table(self,template:str,caption:str="Table")->str:
        top = self.top.replace("*",caption)
        separation = '\\setlength{\\fboxsep}{1pt}\n'
        border = "".join([separation,'\\fcolorbox{white}{white}{\n'])
        bottom = self.bottom
        table = "".join([top,border,template[:-1],'}\n',bottom])
        return table
    
    def tables(self,templates:List[str])->List[str]:
        tables = []
        for template in templates:
            table = self.table(template)
            tables.append(table)
        return tables
        