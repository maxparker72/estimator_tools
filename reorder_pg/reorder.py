import fitz
from progressbar import ProgressBar

bk_i = 1017
doc = fitz.open('mega.pdf')
tocl = range(len(doc.get_toc()[0:bk_i]))
pbar = ProgressBar()


for index in pbar(tocl):
    toc = doc.get_toc()[0:bk_i]
    page = toc[index][2]-1 #starting at zero
    name = toc[index][1]
    #print("Moving {} from {} to before {}".format(name, page, index))
    doc.move_page(page, index)

doc.save('mega_reordered.pdf')