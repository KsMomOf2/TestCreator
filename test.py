import docx
path = 'C:\\My Documents\\Coding Club\\TestCreator\\'
file = 'Yello.docx'
doc = docx.Document()
doc.add_paragraph('Hello world!')
doc.add_paragraph('First Item',style=doc.styles['List'])
doc.add_paragraph('Second Item',style=doc.styles['List'])
doc.add_paragraph('Third Item',style=doc.styles['List'])

doc.save(path + file)
print("I'm done")