import zipfile

path = 'C:\\My Documents\\Coding Club\\TestCreator\\'
file = 'SeniorEnglishFinal'
file = 'NoLists'
file = 'nl.zip'
word_document = path + file + '.docx'
word_document = path + file
print(word_document)

def get_word_xml(docx_filename):
	with open(docx_filename) as f:
		zip = zipfile.ZipFile(f)
		xml_content = zip.read('word/document.xml')
	return xml_content

#from lxml import etree

#def get_xml_tree(xml_string):
#	 return etree.fromstring(xml_string)


xml_stuff = get_word_xml(word_document)

#etree.tostring(xmltree, pretty_print=True)