from __future__ import print_function
import fitz
import argparse
import sys

def main(argv):
    #--------------------------------------------------------------------
    # use argparse to handle invocation arguments
    #--------------------------------------------------------------------
    parser = argparse.ArgumentParser(description="Enter CSV delimiter [;] and documment filename")
    parser.add_argument('-d', help='CSV delimiter [;]', default = ';')
    parser.add_argument('doc', help='document filename')
    args = parser.parse_args(argv[1:])
    delim = args.d               # requested CSV delimiter character
    fname = args.doc          # input document filename

    doc = fitz.open(fname)
    toc = doc.get_toc(simple = False)
    ext = fname[-3:].lower()
    fname1 = fname[:-4] + "-toc.csv"
    outf = open(fname1, "w")
    for t in toc:
        t4 = t[3]
        if ext == "pdf":
            if t4["kind"] == 1:
                p4 = str(t4["to"].y)
            else:
                p4 = "0"
        else:
            p4 = "0"
        rec = delim.join([str(t[0]), t[1].strip(), str(t[2]), p4])
        outf.writelines([rec, "\n"])
    outf.close()

if __name__=="__main__":
    main(sys.argv)