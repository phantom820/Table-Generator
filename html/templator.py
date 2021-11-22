from typing import List
import numpy as np

class TemplateGenerator:

    ''' colors '''
    def __init__(self):
        self.colors = ['','table-primary','table-success','table-danger','table-info',
        'table-warning','table-active']

    ''' remove top rule, mid rule , bottom rule'''
    def clean_template(self,template:str)->str:
        line = template.replace('style="text-align: right;"',"")
        return line
    
    ''' format the column names '''
    def format_columns(self,df)->List[str]:
        cols = list(df.columns)
        formated_cols = [''.join(['[',col,']']) for col in cols]
        return formated_cols
    
    ''' format column names to bold '''
    def format_template(self,template:str)->str:
        line = template.replace('class="dataframe"',"")
        return line
        
    ''' no borders'''
    def borderless(self,df)->str:
        template = df.to_html(index=False,border=0)
        template = self.clean_template(template)
        template = template.replace('dataframe','table table-sm table-borderless')
        return template
    
    ''' no border except in header'''
    def bordered_header(self,df)->str:
        template = df.to_html(index=False,border=0)
        template = self.clean_template(template)
        template = template.replace('border="0"','')
        schemes = ['table table-sm','table table-sm, table-striped']
        idx = np.random.uniform(0,1)
        idz = 1 if idx>0.5 else 0
        scheme = schemes[idz]
        template = template.replace('dataframe',scheme)
        return template
    
    ''' no border except in header and bottom '''
    def bordered_header_bottom(self,df)->str:
        template = self.bordered_header(df)
        lines = (template.split("\n"))
        style = '<tr style = "border-bottom: thin solid black;"'
        for i in range(len(lines)-1,-1,-1):
            if lines[i].find("<tr")!=-1:
                lines[i] = lines[i].replace("<tr",style)
                break;
        template = "\n".join(lines)
        return template
    
    ''' only internal columns bordered would essentialy be same as latex so no need '''
    def bordered_internal_columns(self,df)->str:
        template = self.borderless(df)
        t_style = '<table style="border-collapse:collapse; border-style: hidden;"'
        style = '<td style="border-left: thin solid black;border-right: thin solid black  "'
        template = template.replace('table-borderless','table-striped')
        template = template.replace("<td",style)
        template = template.replace('<table',t_style)
        return template
    
    ''' only rows striped '''
    def striped_rows(self,df)->str:
        template = self.borderless(df)
        template = template.replace('table-borderless','table-striped')
        track = -1
        lines = template.split('\n')
        idc = int(np.random.uniform(0,len(self.colors)))
        color = self.colors[idc]
        style = f'<tr class="{color}"'
        if color!='':
            for i in range(0,len(lines)):
                if lines[i].find("<tr")!=-1:
                    track = track+1
                if lines[i].find("<tr")!=-1 and track==2 or track==0:
                    lines[i] = lines[i].replace("<tr",style)
                    track = 0
        template = "\n".join(lines)
        return template
    
    ''' partialy bordered'''
    def partialy_bordered(self,df)->str:
        df = df.iloc[:,:2]
        template = self.striped_rows(df)
        style = '<td style="border-right: thin solid black; border-left: thin solid black;"'
        template = template.replace("<td",style)
        lines = template.split("\n")
        idx = []
        for i in range(len(lines)):
            line = lines[i]
            found = line.find("<tr")
            if found!=-1:
                idx.append(i)
        mid = len(idx)//2
        for i in idx[2:mid]:
            temp = lines[i]
            temp = temp.replace('<tr','<tr style="border-bottom:thin solid black"')
            lines[i] = temp
        template = "\n".join(lines)
        return template
    
    ''' all borders '''
    def bordered(self,df,idx=-1)->str:
        template = df.to_html(index=False,border=1)
        template = self.clean_template(template)
        template = self.format_template(template)
        style = '<td style="outline:thin solid black;"'
        template = template.replace("<td",style)
        style = '<tr style="outline:thin solid black;border:thin solid black;"'
        template = template.replace("<tr",style)
        template = template.replace('border="1"','')
        template = template.replace('<table','<table class="table table-sm table-bordered"')
        idx = int(np.random.uniform(0,len(self.colors)))
        color = self.colors[idx]
        if color!='':
            template = template.replace('<tr',f'<tr class="{color}"')
        return template  