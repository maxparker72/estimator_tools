import fitz
import csv
import sys

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
    doc_in.save('_'+pdf_filename)
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
    
    io = argv[1]
    pdf = argv[2]
    toccsv = argv[3]

    if pdf[-4:] != '.pdf':
        print('fail arguments pdf')
        print()
        quit(pdf)

    if toccsv[-4:] != '.csv':
        print('fail arguments csv')
        print(toccsv)
        quit()
    
    if io == '-load':
        my_toc = get_bookmarks(pdf)
        export_bookmarks(my_toc, toccsv)
    elif io == '-write':
        my_toc_mod = import_bookmarks(toccsv)
        set_bookmarks(pdf, my_toc_mod)
    else:
        print('fail arguments load write')
        print(io)
        quit()

if __name__ == "__main__":
    main(sys.argv)