import numpy as np
from html.templator import TemplateGenerator

class ComplexTemplateGenerator(TemplateGenerator):

    def __init__(self):
        super().__init__()
        self.colors = ['','table-primary','table-success','table-danger','table-info',
        'table-warning','table-active']
	
    ''' all borders for outer tables '''
    def bordered(self,df_c)->str:
        df = df_c.copy()
        r_index = np.random.randint(0,df.shape[0])
        c_index = np.random.randint(0,df.shape[1])
        index = c_index
        df.iat[r_index,c_index] = '*'
        template = df.to_html(index=False,border=1)
        template = self.clean_template(template)
        template = self.format_template(template)
        return template
    
    ''' format a complex(embedded) template '''
    def format_complex_template(self,outer_template:str,inner_template:str):
        lines = outer_template.split("\n")
        for i in range(len(lines)):
            line = lines[i]
            if line.find("*")!=-1:
                # print('found')
                lines[i] = lines[i].replace("*",inner_template)
            
        template = "\n".join(lines)
        return template
    
    def embedded(self,df_outer,df_inner,f)->str:
        df_outer = df_outer.astype(str)
        df_inner = df_inner.astype(str)
        outer_str = self.bordered(df_outer)
        inner_str = f(df_inner)
        style = '<td style="outline:thin solid black;"'
        outer_str = outer_str.replace("<td",style)
        style = '<tr style="outline:thin solid black;border:thin solid black;"'
        outer_str = outer_str.replace("<tr",style)
        template = self.format_complex_template(outer_str,inner_str)
        template = template.replace('border="1"','')
        template = template.replace('<table','<table class="table table-bordered"',1)
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