import numpy as np
from latex.templator import TemplateGenerator

# Complex Template Generator
''' Generate a table with a table in one of its columns. Results string representing the tabular in latex. 
The required input is 2 pandas dataframes (inner and outer). Extends the Template Generator.
- Embedded (bordered outer table in which one of the columns contains a tables generate by template generator) '''

class ComplexTemplateGenerator(TemplateGenerator):
    ''' all borders for outer tables '''
    def bordered(self,df_c)->str:
        df = df_c.copy()
        r_index = np.random.randint(0,df.shape[0])
        c_index = np.random.randint(0,df.shape[1])
        index = c_index
        df.iat[r_index,c_index] = '*'
        columns = self.format_columns(df)
        column_format = ["c" for i in range(len(df.columns))]
        column_format[index] = '@{}c@{}'
        column_format = "|".join(column_format)
        column_format = "".join(["|",column_format,"|"])
        template = df.to_latex(index=False,column_format=column_format,header=columns)
        template = template.replace("\\toprule","\hline")
        template = self.clean_template(template)
        template = template.replace("\\\\","\\\\ \hline")
        template = self.format_template(template)
        return template
    
    ''' format a complex(embedded) template '''
    def format_complex_template(self,outer_template:str,inner_template:str):
        lines = outer_template.split("\n")
        for i in range(len(lines)):
            line = lines[i]
            if line.find("*")!=-1:
                lines[i] = lines[i].replace("*",inner_template)
            
        template = "\n".join(lines)
        return template
    
    ''' format inner template'''
    def format_inner_template(self,template):
        border = '\\fcolorbox{white}{white!30}{\n'
        template = "".join([border,template,'}'])
        return template
    
    def embedded(self,df_outer,df_inner,f)->str:
        df_outer = df_outer.astype(str)
        df_inner = df_inner.astype(str)
        outer_str = self.bordered(df_outer)
        inner_str = f(df_inner)
        inner_str = self.format_inner_template(inner_str)
        template = self.format_complex_template(outer_str,inner_str)
        return template
