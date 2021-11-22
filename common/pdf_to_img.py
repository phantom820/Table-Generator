from typing import List
from pdflatex import PDFLaTeX
from pdf2image import convert_from_bytes
import numpy as np
import pyvips

# Pdf 2 Imgs
''' Convert pdf to images, so we can convert to images and generate masks.'''
class PdfToImg:
    ''' pdf to img '''
    def pdf_to_img(self,pdf_bytes:bytes):
        img = pyvips.Image.new_from_buffer(pdf_bytes,options='dpi=200')
        img_arr = np.ndarray(buffer=img.write_to_memory(),
                   dtype=np.uint8,
                   shape=[img.height, img.width, img.bands])
        img_arr = img_arr[:,:,:3]
        return img_arr
    
    ''' pdfs to imgs '''
    def pdfs_to_imgs(self,pdfs:List[bytes]):
        pdf_imgs = []
        for pdf in pdfs:
            img_pdf = self.pdf_to_img(pdf)
            pdf_imgs.append(img_pdf)
        return pdf_imgs
