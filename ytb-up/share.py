import re
import os
import pandas
from datetime import date

pat_oco = re.compile("OCO-(\d+).?R?(\d+)?")
pat_ext = re.compile("EXT(\d+).?R?(\d+)?")

excel_in = "old.xlsx"
oco_in = pandas.read_excel(excel_in, sheet_name='OCO EXPORT', index_col=0)
ext_in = pandas.read_excel(excel_in, sheet_name='EXT EXPORT', index_col=0)

oco_path = "OCO_PATH_ENTER"
ext_path = "EXT_PATH_ENTER"

ocos = os.listdir(oco_path)
exts = os.listdir(ext_path)

OCOS = {}
EXTS = {}

for o in ocos:
    m = re.match(pat_oco, o)
    if(m==None):
        continue
    num = m.group(1)
    if m.group(2)==None:
        rev = '0'
    else:
        rev = m.group(2)
    OCOS[(f"{int(num):04d}R{rev}")] = {'NUM':int(num), 'REV':int(rev)}

for e in exts:
    m = re.match(pat_ext, e)
    if(m==None):
        continue
    num = m.group(1)
    if m.group(2)==None:
        rev = '0'
    else:
        rev = m.group(2)
    
    EXTS[(f"{int(num):04d}R{rev}")] = {'NUM':int(num), 'REV':int(rev), 'STATUS':"UNKNOWN"}

OCOKEYS = OCOS.keys()

for e in EXTS.keys():
    if e in OCOKEYS:   
        EXTS[e]['STATUS']="TRUE"

ocodf = pandas.DataFrame.from_dict(OCOS).transpose()
extdf = pandas.DataFrame.from_dict(EXTS).transpose()
new_ocos = pandas.concat([ocodf, oco_in]).drop_duplicates(keep=False) 
new_exts = pandas.concat([extdf, ext_in]).drop_duplicates(keep=False) 

today = date.today().strftime("%Y-%m-%d")
output = f"ext_oco_export - {today}.xlsx"

with pandas.ExcelWriter(output) as writer:
    ocodf.to_excel(writer, sheet_name = "OCO EXPORT")
    new_ocos.to_excel(writer, sheet_name = "OCO DELTA")

    extdf.to_excel(writer, sheet_name = "EXT EXPORT")
    new_exts.to_excel(writer, sheet_name = "EXT DELTA")

