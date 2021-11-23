import cv2 as cv
import numpy as np
from typing import List
import re
from subprocess import run, PIPE

# Table Structure Generator
''' Generate xml like string representing table structure. This is done by making system call to latexml. '''
class StructureGenerator:
    def __init__(self):
        self.expression = '<table|<row|<cell|</cell>|</row>|</table>'
        self.regex = re.compile(self.expression)

    ''' markup representing table '''
    def structure(self,table:str)->str:
        with open('temp/tmp.tex','w') as f:
            f.write(table)
        p = run(['tralics','-output_dir','temp','temp/tmp.tex'],stdout=PIPE)
        with open('temp/tmp.xml','r') as f:
            xml = "".join(f.readlines())
        lines = re.findall(self.regex, xml)
        lines = lines[1:-1]
        lines = [lines[i]+'>' if lines[i].find(">")==-1 else lines[i] for i in range(len(lines))]
        structure = "\n".join(lines)
        return structure
    
    ''' generate table structures '''
    def structures(self,tables:List[str])->List[str]:
        structures = []
        for table in tables:
            structure = self.structure(table)
            structures.append(structure)
        return structures
