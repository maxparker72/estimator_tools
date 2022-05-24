import fitz
orig = fitz.open('test.pdf')
slip = fitz.open('test-slip.pdf')

slip_table = {'old': 0, 'new': 0}

orig.insert_pdf(slip, slip_table['old'], slip_table['old'], slip_table['new'], annots = True)

old_annots = []
for annot in orig[slip_table['old']].annots():
    xref_obj = orig.xref_object(annot.xref, compressed=False)
    old_annots.append(xref_obj)
    with open(f'{annot.xref}.txt', 'w') as f: 
        f.write(xref_obj)


orig.close()
slip.close()