from subprocess import run, PIPE
import uuid
import os
import glob

# Word To Pdf
''' Convert word document to relevant pdf '''

class WordToPdf:
    def doc_to_pdf(self,doc):
        _id = str(uuid.uuid4().int & (1<<64)-1)
        docx_fname = f'temp/{_id}.docx'
        doc.save(docx_fname)
        p = run(['libreoffice','--headless','--convert-to','pdf',docx_fname,'--outdir','temp'],stdout=PIPE)
        with open(f'temp/{_id}.pdf','rb') as f:
            pdf = f.read()
        os.remove(f'temp/{_id}.docx')
        os.remove(f'temp/{_id}.pdf')
        return pdf
    
    def docs_to_pdfs(self,docs):
        pdfs = []
        for doc in docs:
            pdf = self.doc_to_pdf(doc)
            pdfs.append(pdf)
        return pdfs