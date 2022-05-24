import fitz
trans = fitz.open('trans.pdf')
pg = trans[0]

blocks = pg.get_text('blocks')
for ea in blocks:
    pg.add_rect_annot(fitz.Rect(ea[0], ea[1], ea[2], ea[3]))
print(blocks)
#trans.save('new-trans.pdf')
