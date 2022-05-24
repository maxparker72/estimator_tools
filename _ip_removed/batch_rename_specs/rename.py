import os
import csv

cw = os.getcwd()

relative_src_dir = 'Specs2Rename'
abs_src_dir = os.path.join(cw,relative_src_dir)

relative_src_table = 'rename_table.csv'
abs_src_table = os.path.join(cw,relative_src_table)

relative_dest_dir = 'RenamedSpecs'
abs_dest_dir = os.path.join(cw, relative_dest_dir)

# os.chdir(os.path.join(cw,relative_src_dir))
# print(f'Working In: {os.getcwd()}')

with open(abs_src_table, 'r', encoding='utf-8-sig') as table:
    reader = csv.DictReader(table)
    for line in reader:
        #print(line)
        OLD_NAME = os.path.join(abs_src_dir,line['OLD_NAME'])
        NEW_NAME = os.path.join(abs_dest_dir,line['NEW_NAME'])

        try:
            os.rename(OLD_NAME, NEW_NAME)
        except FileNotFoundError:
            print(f"Cannot Find {OLD_NAME}. Passing.")
        except OSError:
            print(f"OS ERROR CAUGHT! {OSError}")