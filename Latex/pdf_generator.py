from typing import List
from pdflatex import PDFLaTeX
import subprocess

# Pdf Generator
''' Generate a pdf in bytes from a given latex string. '''
class PdfGenerator:
    
    ''' returns pdf bytes '''
    def pdf(self,latex_str:str)->bytes:
        with open('temp/t.tex','w',encoding='utf-8') as f:
            f.write(latex_str)
        subprocess.run(['pdflatex','-output-directory','temp','temp/t.tex'],stdout=subprocess.PIPE)
        # pdfl = PDFLaTeX.from_binarystring(bytes(latex_str,'utf-8'),"job")
        # pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=False,keep_log_file=True)
        # return pdf
        with open('temp/t.pdf','rb') as f:
            pdf = f.read()
        return pdf

    ''' return list of pdf bytes'''
    def pdfs(self,latex_strs:List[str])->List[bytes]:
        pdfs = []
        for latex_str in latex_strs:
            pdf = self.pdf(latex_str)
            pdfs.append(pdf)
        return pdfs

