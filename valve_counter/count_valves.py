# Maxwell Parker
# Created: 2021-09-12
# Valve Counter Script
# Input CSV file - Lateral Matrix
# Output CSV file - Counted Valves

"""
    File Notes: 
    Input file must have data formatted in the following fashion to work properly. 
    Columns: [Current lateral size (string), Current FPOC Qty(int), Current POC Size(str), Lateral Valve Tag(str), Lateral Root Valve Size(str), Lateral Root Valve(str), Lateral EOL Valve Tag (assume line size unless otherwise listed)]
    EOL Valve Tag might contain overriding sizes and quantities for EOL and for high and low point valves. 
    Valves must be separated by commas in EOL cell to work with parsing. Size must have number with inch notation, quantity must be in parenthesis, and valve must be standard tag. 
    EOL example with overrides and high low points: "1" (1) DA-28, 1" (1) SP-63, 1" (1) SP-73"
    Edit this code to work best with your file.  
"""

import csv
import re
import sys

#TODO IMPLEMENT CONFIGURATION PARAMETERS BELOW
'''
#CONFIGURATION
HEADER = False

#COLUMNS
LATERAL_SIZE = 0 #STRING
FPOC_QT = 1 #INT
POC_SIZE = 2 #INT
LATERAL_VALVE_TAG = 3 #STRING
LATERAL_ROOT_VALVE_SIZE = 4 #STRING
LATERAL_ROOT_VALVE_TAG = 5 #STRING
LATERAL_EOL = 6 #COMPLICATED LINE ITEM THAT REQUIRES PARSING
'''
#FILES
input_file = "test.csv"
output_file = "delete.csv"

# REGULAR EXPRESSIONS USED TO PARSE CELLS
tagr = re.compile("\w*-\w*") #A VALVE TAG TAKES THE FORM XX-XX FOR ANY NUMBER OF "X"
quantityr = re.compile("\(\d*\)") #QUANTITIES ARE AN INTEGER INSIDE OF PARENTHESIS 
sizer = re.compile("\S*\"") #THE SIZE OF A VALVE IS LISTED WITH INCH MARKING UNLESS IN DEDICATED COLUMN

# DESIGNED TO EXTRACT TAG, SIZE, AND QUANTITY FROM A CELL THAT MIGHT CONTAIN ALL THAT INFORMATION
def parse(cell, default_size):
    # AT A MINIMUM, A GIVEN CELL MUST CONTAIN A TAG IF IT IS BEING PARSED
    has_tag = tagr.search(cell)
    has_size = sizer.search(cell)
    has_qt = quantityr.search(cell)
    
    if has_tag:
        
        if has_size:
            #THERE CAN ONLY BE ONE INSTANCE OF A SIZE MATCH
            size = sizer.findall(cell)
            if len(size) != 1:
                #CANNOT PRECEDE NONE, NONE
                return None, None
            else:
                size = size[0]
                size = size[0:-1] # REMOVES THE EXPECTED INCH SYMBOL REQUIRED TO MATCH
        else:
            size = default_size #STRING, PER VALVE SHEET, THIS IS PASSED AS THE LATERAL SIZE
        
        if has_qt:
            #THERE CAN ONLY BE ONE INSTANCE OF A QUANTITY MATCH
            quantity = quantityr.findall(cell)
            if len(quantity) != 1:
                #CANNOT PRECEDE NONE, NONE
                return None, None
            else:
                quantity = quantity[0]
                qt = int(quantity[1:-1])  # REMOVE PARENTHESIS REQUIRED TO MATCH AND CAST AS INTEGER 
        else:
            qt = 1 #ASSUMED DEFAULT
    else:
        #IF THERE WAS NO TAG IT WILL RETURN NONE, NONE
        return None, None

    kind = tagr.findall(cell)
    # MUST ONLY BE ONE INSTANCE OF A TAG MATCH TO PROCEED OTHERWISE RETURNS NONE, NONE
    if len(kind) != 1:
        return None, None
    else:
        kind = kind[0]

    code = "{}-{}".format(size, kind) #CREATE UNIQUE VALVE CODE USING STRING FORMATTING AND PARSED INFORMATION

    return code, qt #RETURN UNIQUE VALVE CODE AND QUANTITY FOR PROCESSING IN MAIN LOOP

#MAIN FUNCTION CALL
def main():
    # DICTIONARY DATA STRUCTURE USED TO STORE VALVES WHERE KEY IS VALVE CODE AND VALUE IS THE QUANTITY
    valve_table = dict()

    # OPEN THE SOURCE FILE USING WITH STATEMENT TO AUTOMATICALLY CATCH FILE NOT FOUND ERRORS
    with open(input_file, encoding = 'utf-8-sig') as valves:
        csv_reader = csv.reader(valves, delimiter = ",")
        
        # FOR EACH ROW
        index = 0 # REFERENCE INDEX FOR PRINTING ERRORS
        for row in csv_reader:
            # EXTRACT THE LATERAL VALVE AND QUANTITY
            lat_code = "{}-{}".format(row[2], row[5])  # SIZE AND TYPE TO CREATE VALVE CODE IE: 1-BA-28
            lat_qt = int(row[1]) #QUANTITY WILL BE INTEGER

            # RECORD QUANTITY IN DICTIONARY
            if lat_code in valve_table:
                # INCREMENT THE QUANTITY 
                valve_table[lat_code] += lat_qt
            else:
                # CREATE NEW ENTRY AND PRINT CREATION
                valve_table[lat_code] = lat_qt
                print("Created: {}".format(lat_code))

            # EXTRACT THE ROOT VALVE AND QUANTITY 
            root_code = "{}-{}".format(row[3], row[4])
            root_qt = 1  # SPECIFIC TO VALVE DOCUMENT. QUANTITIES WERE NOT LISTED BUT ASSUMED TO BE 1

            # RECORD QUANTITY IN DICTIONARY 
            if root_code in valve_table:
                # INCREMENT THE QUANTITY 
                valve_table[root_code] += root_qt
            else:
                # CREATE NEW ENTRY AND PRINT CREATION
                valve_table[root_code] = root_qt
                print("Created: {}".format(root_code))

            # EOL VALVES, SOME CONTAIN UPPER AND LOWER VALVE
            # THIS CELL IS EXPECTED TO HAVE 1 OR MORE ENTRIES SEPARATED BY COMMAS.
            # EACH LISTING CAN CONTAIN MULTIPLE PIECES OF INFORMATION WHICH ARE EXTRACTED USING PARSE FUNCTION
            for v in row[6].split(','):
                code, qt = parse(v, row[0])
                if code == None:
                    print("Row {}: {} has a problem! Review and rerun script!".format(index,row))
                    index += 1
                    break #TODO: TEST IF THIS CAUSES MISCOUNT IN THE EVENT THAT A PROBLEM OCCURS. FOR NOW, MAKE SURE THERE ARE NO PROBLEMS DURING COUNT.
                if code in valve_table:
                    #INCREMENT QUANTITY 
                    valve_table[code] += qt
                else:
                    #CREATE ENTRY AND QUANTITY
                    valve_table[code] = qt
                    print("Created: {}".format(code))
            index += 1 #TRACK INDEX

    # RECORD RESULTS TO NEW FILE
    with open(output_file, mode = "w") as valve_quantities:
        writer = csv.writer(valve_quantities, delimiter = ",", quotechar = '"', lineterminator = '\n', quoting = csv.QUOTE_MINIMAL)
        for item in valve_table:
            writer.writerow([item,valve_table[item]])

if __name__ == "__main__":
    main() # THIS IS THE EQUAL TO MAIN METHOD IN JAVA OR C++, NOT A FAN PYTHON.