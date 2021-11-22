from typing import List

# Template Generator
''' Generate table with certain properties (borderless,boredered and so on). Results in a string representing the tabular in latex. The required input is a pandas dataframe.
- borderless (no borders)
- bordered header (only header bordered)
- bordered header and bottom (only header and end bordered)
- bordered internal columns (only internal column bordered)
- bordered columns (columns bordered)
- bordered (grid table ) '''
class TemplateGenerator:
    ''' remove top rule, mid rule , bottom rule'''
    def clean_template(self,template:str)->str:
        line = template.replace("\\toprule\n","")
        line = line.replace("\\midrule\n","")
        line = line.replace("\\bottomrule\n","")
        return line
    
    ''' format the column names '''
    def format_columns(self,df)->List[str]:
        cols = list(df.columns)
        formated_cols = [''.join(['[',col,']']) for col in cols]
        return formated_cols
    
    ''' format column names to bold '''
    def format_template(self,template:str)->str:
        line = template.replace("[","\\textbf{")
        line = line.replace("]","}")
        return line
        
    ''' no borders'''
    def borderless(self,df)->str:
        columns = self.format_columns(df)
        column_format = "".join(["c" for i in range(len(df.columns))])
        template = df.to_latex(index=False,column_format=column_format,header=columns)
        template = self.clean_template(template)
        template = self.format_template(template)
        return template
    
    ''' no border except in header'''
    def bordered_header(self,df)->str:
        columns = self.format_columns(df)
        column_format = "".join(["c" for i in range(len(df.columns))])
        template = df.to_latex(index=False,column_format=column_format,header=columns)
        template = template.replace("\\toprule","\hline")
        template = template.replace("\\midrule","\hline")
        template = self.clean_template(template)
        template = self.format_template(template)
        return template
    
    ''' no border except in header and bottom'''
    def bordered_header_bottom(self,df)->str:
        columns = self.format_columns(df)
        column_format = "".join(["c" for i in range(len(df.columns))])
        template = df.to_latex(index=False,column_format=column_format,header=columns)
        template = template.replace("\\toprule","\hline")
        template = template.replace("\\midrule","\hline")
        template = template.replace("\\bottomrule","\hline")
        template = self.clean_template(template)
        template = self.format_template(template)
        return template
    
    ''' only internal columns bordered '''
    def bordered_internal_columns(self,df)->str:
        columns = self.format_columns(df)
        column_format = "".join(["|c" if i!=0 else "c" for i in range(len(df.columns))])
        template = df.to_latex(index=False,column_format=column_format,header=columns)
        template = template.replace("\\midrule","\hline")
        template = template.replace("\\bottomrule","\hline")
        template = self.clean_template(template)
        template = self.format_template(template)
        return template
    
    ''' only columns bordered '''
    def bordered_columns(self,df)->str:
        columns = self.format_columns(df)
        column_format = "".join(["c|" for i in range(len(df.columns))])
        column_format = "".join(["|",column_format])
        template = df.to_latex(index=False,column_format=column_format,header=columns)
        template = template.replace("\\toprule","\hline")
        template = template.replace("\\midrule","\hline")
        template = template.replace("\\bottomrule","\hline")
        template = self.clean_template(template)
        template = self.format_template(template)
        return template
    
    ''' partialy bordered'''
    def partialy_bordered(self,df)->str:
        template = self.bordered(df)
        lines = template.split("\n")
        idx = []
        for i in range(len(lines)):
            line = lines[i]
            found = line.find("hline")
            if found!=-1:
                idx.append(i)
        mid = len(idx)//2
        replaced = []
        for i in idx[2:mid]:
            temp = lines[i]
            temp = temp.replace('\\hline','')
            lines[i] = temp
        template = "\n".join(lines)
        return template
    
    ''' all borders '''
    def bordered(self,df)->str:
        columns = self.format_columns(df)
        column_format = "".join(["c|" for i in range(len(df.columns))])
        column_format = "".join(["|",column_format])
        template = df.to_latex(index=False,column_format=column_format,header=columns)
        template = template.replace("\\toprule","\hline")
        template = self.clean_template(template)
        template = template.replace("\\\\","\\\\ \hline")
        template = self.format_template(template)
        return template     