import fitz
import sys
import argparse

def main(args):
    print('PDF Vector Reducer - JE Dunn - Author: Maxwell Parker - 2021-12-22')
    parser = argparse.ArgumentParser(description='PDF Vector Reducer')
    parser.add_argument('--pdf', dest='pdf', metavar='MYFILE.pdf', nargs=1, help='a pdf file to reduce', action='store', required=True)
    parser.add_argument('--zm', dest='zm', metavar='ZOOM', nargs=1, help='zoom between 1-4, higher zoom = higher res.', action='store', required=True, choices=["1","1.5","2","2.5","3","3.5","4"])
    args = parser.parse_args(args[1:])
    if args.pdf[0][-4:] != '.pdf':
        print('Wrong file type!')
        sys.exit()
    
    fname = args.pdf[0]
    doc = fitz.open(fname) #document
    zm = float(args.zm[0])
    mat = fitz.Matrix(zm,zm) #high resolution

    target = fitz.open()
    for page in doc:
        pix = page.get_pixmap(matrix=mat)
        tarpage = target.new_page(width=pix.width, height=pix.height)
        tarpage.insert_image(tarpage.rect, stream=pix.pil_tobytes("JPEG"))
    target.ez_save("new-"+fname)  # targetname = parameter

if __name__ == "__main__":
    main(sys.argv)