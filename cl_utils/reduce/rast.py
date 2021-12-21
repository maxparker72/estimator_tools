import fitz
import sys

def main(args):
    # fname = 'CPK07_AT60 - ARCH.pdf'
    fname = args[1]

    doc = fitz.open(fname) #document
    zm = float(args[2])
    mat = fitz.Matrix(zm,zm) #high resolution

    fnameshort = fname.replace('.pdf','') #name only

    #newdoc = fitz.open() #reduced document

    for page in doc:
        pix = page.get_pixmap(matrix=mat) #convert each page to pixmap high res
        pix.save('{} - {}.png'.format(fnameshort, page.number))
        #page_im_name = '{} - {}.png'.format(fnameshort, page.number)
        #pix.save(page_im_name)
        #page_im = fitz.open(page_im_name)
        #pdf_bytes = page_im.convert_to_pdf() #create PDF from pixmap and OCR. 
        #page_im.close()
        #newdoc.insert_pdf(imgpdf) #add pdf page to newdoc
        #pix = None #reset pix for next iteration
        #imgpdf.close() #close stream before reopening in next iteration
        
    
    #newdoc.save('{}-RED-OCR.pdf'.format(fnameshort))

if __name__ == "__main__":
    # Must have two arguments one is the command, one is the file. 
    if len(sys.argv) != 3:
        print('USAGE: rast [mypdf.pdf] [zoom]')
        quit()
    #file must be PDF
    if sys.argv[1][-4:] != '.pdf':
        print('Wrong file type!')
        quit()
    main(sys.argv)