import pandas
import fitz
#from progressbar import progressbar

'''
ASSUME CPKXX DATA ONLY PASSED TO THIS PROGRAM. 
1. FOR EACH DRAWING NUMBER
    A. SORT THAT DRAWING NUMBER
    B. SORT THAT PACKAGE
    C. GET DATE ISSUED FOR THAT DRAWING
    D. GO BACK TO RESULT FRAME FROM A. 
    E. SORT FRAME BY DATE
    F. GO TO DATE ISSUED IN THAT PACKAGE AND GO UP ONE INDEX TO NEXT THEORETICAL ISSUANCE. 
2. CREATE A STAMP TEXT
3. CREATE ANNOTATION ON THAT PAGE. 
'''
# files
pkg_track = 'package_sourcecpk03.xlsx'
pkg_pages = 'A - CPK03-R3 - IFC - MSB_WATD_(ATTD) - 2022-3-2_Bookmarks.csv'
package = 'A - CPK03-R3 - IFC - MSB_WATD_(ATTD) - 2022-3-2.pdf'
pkg_code = 'CPK03-R3-IFC'

#load files
doc = fitz.open(package)
tracker = pandas.read_excel(pkg_track, sheet_name=1, header=0, index_col=None, usecols="A:D")
pages = pandas.read_csv(pkg_pages, header = None)

# clean pages
pages[pages.columns[1]]-=1 # based page numbers
pages_lst = pages.to_numpy()

# boolean matrices 
inst = tracker['Instances'] > 1 #boolean matrix where instance over 1

# filtered dataframes
duplicates = tracker[inst] #contains all drawings that aren't uniquely issued in one page

# functions
def stampPage(pno, message):
    page = doc[pno]
    an = page.add_freetext_annot(page.rect, message, fontsize = 144, text_color = (1,0,0))
    an.set_opacity(0.5)
    an.update()

# if applicable, retrieve the next newest page and get a string to mark the drawing with. 
def getSuper(page, pkg_code):
    # get a specific page number
    draw = duplicates['Drawing Number in Set'] == page #boolean matrix
    if draw.sum()==0:
        return 0 #key not found
    
    drawing = duplicates[draw] #contains a specific drawing number only

    # fresh copy, TODO: is there a faster way to do this? 
    drawing_sorted = drawing.sort_values(by=['Date Issued']).reset_index() #contains a specific drawing number only sorted by date issued. 
    pkg = drawing_sorted['PKG-CODE'] == pkg_code # package boolean

    if pkg.sum()==0:
        return 0 #key not found

    index = drawing_sorted[pkg].index[0] #get iloc of the drawing of interest in the sorted list
    
    if(index>=(drawing_sorted.size/5)-1): #specific to the spreadsheet I load. 
        return 1 #out of bounds
    else:
        return f"maxpar - {page} issued on {drawing_sorted.iloc[index]['Date Issued'].date().__str__()} was superseded by {drawing_sorted.iloc[index+1]['PKG-CODE']} on {drawing_sorted.iloc[index+1]['Date Issued'].date().__str__()}"
    
errs = {'BOUNDS-OR-NEW': 0, 'NTFOUND-OR-UNIQUE': 0, 'STAMPED': 0}
for page_set in pages_lst:
    sup = getSuper(page_set[0], pkg_code)
    if sup==0:
        #print('key not found')
        errs['NTFOUND-OR-UNIQUE']+=1
    elif sup ==1:
        #print('out of bounds')
        errs['BOUNDS-OR-NEW']+=1
    else:
        stampPage(page_set[1], sup)
        errs['STAMPED']+=1
        
print(f"REPORT: {errs}")
print('SAVING...')
doc.saveIncr() #TODO save new doesn't work only incr. 
print('DONE!')