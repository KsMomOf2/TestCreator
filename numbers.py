#https://virantha.com/2013/08/16/reading-and-writing-microsoft-word-docx-files-with-python/
#Because it is never easy.  See if you can look through the xml and retreive the ilvl tags

import docx.package
import docx.parts.document
import docx.parts.numbering

path = 'C:\\My Documents\\Coding Club\\TestCreator\\'
file = 'SeniorEnglishFinal'

package = docx.package.Package.open(path+file+ '.docx')

main_document_part = package.main_document_part
assert isinstance(main_document_part, docx.parts.document.DocumentPart)

numbering_part = main_document_part.numbering_part
assert isinstance(numbering_part, docx.parts.numbering.NumberingPart)

ct_numbering = numbering_part._element
print(ct_numbering)  # CT_Numbering
for num in ct_numbering.num_lst:
    print(num)  # CT_Num
    print(num.abstractNumId)  # CT_DecimalNumber