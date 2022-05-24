import fitz
import os

def cleanpdf(doc):
    document = fitz.open(doc)
    document.set_toc([])
    for page in document:
        for link in page.get_links():
            page.delete_link(link)
    document.saveIncr()
    document.close()

cw = os.getcwd()
for dir,sub,file in os.walk(cw):
    for f in file:
        if(f[-4:]=='.pdf'):
            cleanpdf(os.path.join(dir,f))



