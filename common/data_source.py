import pandas as pd
import numpy as np
import glob

# Data Source
''' A pool of dataframes in which table data is pulled from. When data is needed for a table following happens
a call to sample with number of datafframes needed and mode (important for limits). 
The sample randomly selects dataframes and samples each randomly. Then shuffles dataframes order. '''

class DataSource:
    def __init__(self,path):
        self.data = self.load(path)
        self.N = len(self.data)
        self.MIN_ROWS = 2
        self.MIN_OUTER_ROWS = 4
        self.MAX_ROWS = 30
        self.MIN_COLS = 2
        self.MAX_COLS = 7
        self.MAX_COLS_INNER = 3
        self.MAX_COLS_OUTER = 3
        self.STATE = 42
        
    ''' prepare dataframe '''
    def prepare(self,df):
        df.columns = self.format_columns(df.columns)
        nan_value = float("NaN")
        df.replace("", "-", inplace=True)
        df.replace("NaN","-", inplace=True)
        df.dropna(inplace=True)
        df = df.iloc[:300,:]
        df = df.astype(str)
        return df
    
    ''' load dataframes '''
    def load(self,path):
        fnames = glob.glob(path)
        data = []
        for fname in fnames:
            df = pd.read_csv(fname,encoding="utf-8")
            df = self.prepare(df)
            for c in df.columns:
                df[c] = df[c].apply(self.reduce)
            data.append(df)
        return data
    
    ''' reduce rows '''
    def reduce(self,x:str)->str:
        if type(x) is not str:
            return x
        if len(x)>12:
            return x[:12]
        return x
    
    ''' format column headers '''
    def format_columns(self,columns):
        new_columns = []
        for c in columns:
            c = c.replace("_"," ")
            c = c.title()
            if len(c)>12:
                c = c.split(' ')[0][:12]
            new_columns.append(c)
        return new_columns
    
    ''' shuffle '''
    def shuffle(self):
        p = np.random.permutation(self.N)
        self.data = [self.data[p[i]] for i in range(len(p))]
    
    ''' select a dataframe '''
    def select(self,i,rows,cols):
        df = self.data[i].copy()
        df = df.sample(frac=1,random_state=self.STATE)
        df = df.iloc[:rows,np.random.permutation(cols)]
        df = df.iloc[:,:cols]
        return df
        
    ''' sample for simple tables'''
    def sample(self,n,mode=0):
        sample = []
        p = np.random.permutation(n)
        max_rows = self.MAX_ROWS//n
        if mode == 0:
            max_cols = 7
        else:
            max_rows = max(self.MIN_OUTER_ROWS,max_rows//2)
            max_cols = 3
        for i in range(n):
            rows = int(np.random.uniform(self.MIN_ROWS,max_rows+1))
            cols = int(np.random.uniform(self.MIN_COLS,max_cols+1))
            df = self.select(p[i],rows,cols)
            sample.append(df)
        self.shuffle()
        return sample