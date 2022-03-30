import pandas
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
xl = pandas.read_excel("test.xlsx", sheet_name=1, header=0, index_col=None, usecols="A:D")
inst = xl['Instances'] > 1 #boolean matrix where instance over 1
duplicates = xl[inst] #contains all drawings that aren't uniquely issued in one page

def getSuper(page, pkg_code):
    # get a specific page number
    draw = duplicates['Drawing Number in Set'] == page #boolean matrix
    drawing = duplicates[draw] #contains a specific drawing number only

    # fresh copy, TODO: is there a faster way to do this? 
    drawing_sorted = drawing.sort_values(by=['Date Issued']).reset_index() #contains a specific drawing number only sorted by date issued. 
    # return f" Superceded By: {drawing_sorted.iloc[-2]['PKG-CODE']} on {drawing_sorted.iloc[-2]['Date Issued']}"
    pkg = drawing_sorted['PKG-CODE'] == pkg_code # package boolean
    index = drawing_sorted[pkg].index[0]
    if(index>=(drawing_sorted.size/5)-1):
        return None
    else:
        return f" Superceded By: {drawing_sorted.iloc[index+1]['PKG-CODE']} on {drawing_sorted.iloc[index+1]['Date Issued']}"
    

print(getSuper('MS1-SSD0000', 'CPK03-R2-IFC'))
