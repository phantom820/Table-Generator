from typing import List
import itertools
import json
import cv2 as cv
import numpy as np
import concurrent.futures

from Word.table_writer import TableWriter
from Word.word_to_pdf import WordToPdf
from Word.structure_generator import StructureGenerator
import os, sys
path = os.path.abspath('.')
sys.path.insert(1, path)
from common.data_source import DataSource
from common.pdf_to_img import PdfToImg
from common.mask_generator import MaskGenerator
from common.transformer import Transformer
from common.labeler import Labeler


class WordGeneratorPipeline:
    def __init__(self,path):
        self.table_writer = TableWriter()
        self.word_to_pdf = WordToPdf()
        self.pdf_to_img = PdfToImg()
        self.mask_generator = MaskGenerator()
        self.transformer = Transformer()
        self.labeler = Labeler(StructureGenerator())
        self.data_source = DataSource(path)
        
    ''' generate simple templates from given dfs and types'''
    def samples(self,types:List[int])->List[str]:
        n = len(types)
        if n<3:
            sample = self.data_source.sample(n,0)
        else:
            sample = self.data_source.sample(n+1,0)
        outer_samples = []
        inner_samples = []
        for i in range(n):
            index = types[i]
            if index!=4:
                outer_samples.append(sample[i])
                inner_samples.append(None)
            else:
                if n == 1:
                    df_outer,df_inner = self.data_source.sample(2,1)[:2]
                elif n==2:
                    df_outer,df_inner = self.data_source.sample(n,1)[:2]
                else:
                    df_outer,df_inner = self.data_source.sample(n+1,1)[:2]
                outer_samples.append(df_outer)
                inner_samples.append(df_inner)
        
        return outer_samples,inner_samples
    
    ''' generate a single datapoint {mask,pdf,tables,img} '''
    def datum(self,types:List[int])->dict:
        outer_samples,inner_samples = self.samples(types)
        # step 1 pdf and outlined pdf
        doc,outlined_doc = self.table_writer.write(types,outer_samples,inner_samples)
        #outlined_doc = self.table_writer.write_outlined(types,outer_samples,inner_samples)
        pdfs = self.word_to_pdf.docs_to_pdfs([doc])
        outlined_pdfs = self.word_to_pdf.docs_to_pdfs([outlined_doc])
        # step 2 images and masks 
        imgs = self.pdf_to_img.pdfs_to_imgs(pdfs)
        outlined_imgs = self.pdf_to_img.pdfs_to_imgs(outlined_pdfs)
        masks = self.mask_generator.masks(imgs,outlined_imgs)
        
        # step 3 make results
        results = {"mask":masks[0],"img":imgs[0],"pdf":pdfs[0],'tables':doc.tables}
        
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
        
    ''' generate dataset '''    
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
            # for c in sub_types:
            #     stats[c] = stats[c]+1
            datum = self.datum(sub_types)
            theta = np.random.uniform(-2,2)
            img,mask = self.distort_datum(datum,theta=theta)
            datum['img'] = img
            datum['mask'] = mask
            label = self.label(datum)
            label['types'] = sub_types
            label["id"] = str(_id)                    
            _id =_id+1
            self.save(datum,label,config)
        return _id,stats

    ''' generate dataset '''    
    def generate_data_parallel(self,config):
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


