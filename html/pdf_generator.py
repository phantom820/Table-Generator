from typing import List
import pdfkit

class PdfGenerator:
    ''' returns pdf bytes '''
    def pdf(self,html_str:str)->bytes:
        pdf = pdfkit.from_string(html_str,False,options={'--quiet':'','--dpi':200,"enable-local-file-access": None})
        return pdf
    
    ''' return list of pdf bytes'''
    def pdfs(self,html_strs:List[str])->List[bytes]:
        pdfs = []
        for html_str in html_strs:
            pdf = self.pdf(html_str)
            pdfs.append(pdf)
        return pdfs