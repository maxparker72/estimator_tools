import fitz
import csv
import sys
import argparse

fields = ['level','name','page'] #default fields

# get bookmarks from pdf
# return bookmarks as data structure
def get_bookmarks(pdf_filename):
    doc_in = fitz.open(pdf_filename)
    toc_store = doc_in.get_toc()
    doc_in.close()
    return toc_store

# given bookmarks data structure and a filename
# will write bookmark datastrucure to that file. 
def export_bookmarks(toc, toc_filename):
    with open(toc_filename, 'w', newline = '') as f:
        writer = csv.DictWriter(f, fieldnames = fields, dialect = csv.excel)
        writer.writeheader()
        for bkmark in toc:
                writer.writerow({fields[0]:bkmark[0], fields[1]:bkmark[1], fields[2]:bkmark[2]})

# given
def set_bookmarks(pdf_filename, toc):
    doc_in = fitz.open(pdf_filename)
    doc_in.set_toc(toc)
    doc_in.save('new-'+pdf_filename)
    doc_in.close()

def import_bookmarks(toc_filename):
    with open(toc_filename, 'r', newline = '') as f: 
        reader = csv.DictReader(f, dialect = csv.excel)
        toc = list()
        for row in reader:
            row_struct = [int(row[fields[0]]), row[fields[1]], int(row[fields[2]])]
            print(row_struct)
            toc.append(row_struct)
    
    return toc

def main(argv):
    print('PDF Bookmark Editor - JE Dunn - Author: Maxwell Parker - 2021-12-22')
    load = 'load'
    write = 'write'
    parser = argparse.ArgumentParser(description='Bookmark Editor Arguments')
    parser.add_argument('--mode', dest='mode', metavar='MODE', nargs=1, help='a pdf file to load/write bookmarks from', action='store', required=True, choices = [load,write])
    parser.add_argument('--pdf', dest='pdf', metavar='MYFILE.pdf', nargs=1, help='a pdf file to load/write bookmarks from', action='store', required=True)
    parser.add_argument('--csv', dest='csv', metavar='MYBOOKMARKS.csv', nargs=1, help='a csv file to load/write bookmarks from', action='store', required=True)
    args = parser.parse_args(argv[1:])

    io = args.mode[0] #loading or writing
    pdf = args.pdf[0] #pdf file for load or write
    toccsv = args.csv[0] #csv file to load or write

    #must be PDF
    if pdf[-4:] != '.pdf':
        print('{} fail argument not pdf'.format(pdf))
        sys.exit()
    #must be CSV
    if toccsv[-4:] != '.csv':
        print('{} fail argument not csv'.format(toccsv))
        sys.exit()
    
    if io == load:
        my_toc = get_bookmarks(pdf)
        export_bookmarks(my_toc, toccsv)
    elif io == write:
        my_toc_mod = import_bookmarks(toccsv)
        set_bookmarks(pdf, my_toc_mod)
    else:
        print('--mode fail!')
        sys.exit()

if __name__ == "__main__":
    main(sys.argv)