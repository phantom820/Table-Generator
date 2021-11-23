from typing import List
import numpy as np
import cv2 as cv
import json
import itertools
import cProfile
import concurrent.futures

from Latex.templator import TemplateGenerator
from Latex.complex_templator import ComplexTemplateGenerator
from Latex.table_generator import TableGenerator
from Latex.table_writer import TableWriter
from Latex.pdf_generator import PdfGenerator
from Latex.structure_generator import StructureGenerator
import os, sys
path = os.path.abspath('.')
sys.path.insert(1, path)
from common.data_source import DataSource
from common.pdf_to_img import PdfToImg
from common.mask_generator import MaskGenerator
from common.transformer import Transformer
from common.labeler import Labeler

class LatexGeneratorPipeline:
    def __init__(self,path):
        self.data_source = DataSource(path)
        self.templator = TemplateGenerator()
        self.c_templator = ComplexTemplateGenerator()
        self.table_generator = TableGenerator()
        self.table_writer = TableWriter()
        self.pdf_generator = PdfGenerator()
        self.pdf_to_img = PdfToImg()
        self.mask_generator = MaskGenerator()
        self.transformer = Transformer()
        self.labeler = Labeler(StructureGenerator())
        
        self.template_funcs = [
            self.templator.borderless,
            self.templator.bordered_header,
            self.templator.bordered_header_bottom,
            self.templator.bordered_internal_columns,
            self.templator.bordered_columns,
            self.templator.partialy_bordered,
            self.templator.bordered,
            self.c_templator.embedded
        ]
        
    ''' generate simple templates from given dfs and types'''
    def templates(self,types:List[int])->List[str]:
        n = len(types)
        templates = []
        sample = self.data_source.sample(n,0)
        for i in range(n):
            index = types[i]
            if index!=7:
                df = sample[i]
                func = self.template_funcs[index]
                template = func(df)
                templates.append(template)
            else:
                if n == 1:
                    df_outer,df_inner = self.data_source.sample(2,1)[:2]
                else:
                    df_outer,df_inner = self.data_source.sample(n,1)[:2]
                df_inner = df_inner.iloc[:len(df_outer)//2,:]
                func = self.template_funcs[index]
                func_inner = self.template_funcs[np.random.randint(0,7)]
                template = func(df_outer,df_inner,func_inner)
                templates.append(template)              
        return templates
    
    ''' generate a single datapoint {mask,pdf,tables,img} '''
    def datum(self,types:List[int])->dict:
        templates = self.templates(types)
        # step 1 pdf and outlined pdf
        tables = self.table_generator.tables(templates)
        outlined_tables = self.table_generator.outlined_tables(templates)
        tex = self.table_writer.write(tables)
        pdf = self.pdf_generator.pdf(tex)
        outlined_table = self.table_writer.write(outlined_tables)
        outlined_pdf = self.pdf_generator.pdf(outlined_table)        
        
        # step 2 images and masks 
        pdfs = [pdf]
        outlined_pdfs = [outlined_pdf]
        imgs = self.pdf_to_img.pdfs_to_imgs(pdfs)
        outlined_imgs = self.pdf_to_img.pdfs_to_imgs(outlined_pdfs)
        masks = self.mask_generator.masks(imgs,outlined_imgs)
        
        # step 3 make results
        results = {"mask":masks[0],"img":imgs[0],"pdf":pdfs[0],'tables':tables}
        
        return results
    
    ''' apply transformation using params to dirty data (img and mask) '''
    def distort_datum(self,datum:dict,k:int=7,s_x:int=1,s_y:int=1,theta:float=0)->dict:
        img = datum['img']
        mask = datum['mask']
        img = self.transformer.dirtify(img,k,s_x,s_y,theta,False)
        mask = self.transformer.dirtify(mask,k,s_x,s_y,theta,True)
        return img,mask
    
    ''' label a datum '''
    def label(self,datum:dict):
        mask = datum['mask']
        tables = datum['tables']
        label = self.labeler.label(mask,tables)
        return label
    
    ''' combinations of tables '''
    def generate_combinations(self,types:List[str]):
        combinations = []
        counts = {i:0 for i in types}
        for i in range(1,4):
            c = itertools.combinations(types, i)
            for j in c:
                combinations.append(list(j))
                for k in j:
                    counts[k] = counts[k]+1
        return counts,combinations
    
    ''' save datum along with its annotation '''
    def save(self,datum:dict,annotation:dict,config):
        _id = annotation['id']
        img_path = config['img_path']+_id+'.png'
        mask_path = config['mask_path']+_id+'.png'
        annotation_path = config['annotation_path']+_id+'.json'
        
        # save img and mask
        img = datum['img']
        mask = datum['mask']
        
        cv.imwrite(img_path,img)
        cv.imwrite(mask_path,mask)
        
        # save annotation
        with open(annotation_path,'w') as f:
            json.dump(annotation,f)
        
    ''' generate dataset in parallel'''    
    def generate_data_parallel(self,config):
        sample_size = config["sample_size"]
        types = config["types"]
        N = sample_size
        counts,combinations = self.generate_combinations(types)
        n = len(combinations)
        stats = {i:0 for i in types}
        _id = 0
        batch_size = 5
        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
            for j in range(0,N,batch_size):
                idx = (np.random.uniform(0,n,(batch_size)))
                sub_types = [combinations[int(idx[k])] for k in range(0,batch_size)]
                # for sub in sub_types:
                #     for t in sub:
                #         stats[t] = stats[t]+1
                for k,datum in enumerate(executor.map(self.datum,sub_types)):
                    theta = np.random.uniform(-2,2)
                    img,mask = self.distort_datum(datum,theta=theta)
                    datum['img'] = img
                    datum['mask'] = mask
                    label = self.label(datum)
                    label['types'] = sub_types[k]
                    label["id"] = str(_id)                    
                    _id = _id+1
                    k = k+1
                    self.save(datum,label,config)
        return _id,stats

    ''' generate dataset serially'''    
    def generate_data(self,config):
        sample_size = config["sample_size"]
        types = config["types"]
        N = sample_size
        counts,combinations = self.generate_combinations(types)
        n = len(combinations)
        stats = {i:0 for i in types}
        _id = 0
        for i in range(N):
            idx = int(np.random.uniform(0,n))
            sub_types = combinations[idx]
            for c in sub_types:
                stats[c] = stats[c]+1
            datum = self.datum(sub_types)
            theta = np.random.uniform(-2,2)
            img,mask = self.distort_datum(datum,theta=theta)
            datum['img'] = img
            datum['mask'] = mask
            label = self.label(datum)
            label["id"] = str(_id)
            self.save(datum,label,config)
            _id =_id+1
        return _id,stats

        

