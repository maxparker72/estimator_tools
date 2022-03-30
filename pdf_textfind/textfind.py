import fitz
import re

# find text as blocks
# find block with text (regular expression option)
# find next block north, south, east, west

doc = fitz.open('MS1-111-MW-A03.pdf')
page = doc[0]
blocks = page.get_text('blocks')
#print(blocks)
search = 'MS1-111-MW-A03'
for block in blocks:
    page.add_rect_annot(fitz.Rect(block[0],block[1],block[2],block[3]))
    if re.match(search.lower(), block[4].lower()):
        print(block)
doc.save('newpage.pdf')