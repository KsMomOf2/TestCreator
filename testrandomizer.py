import wordtoxml
import xmltolist
import listtoxls
import listtotest
import combinexml

import create_new_xml
from testdata import Teacher

def __main__():

	template = wordtoxml.WordToXML("word/TestTemplate.docx")

	template_doc = template.word_document
	template_zip = template.zip

	test = xmltolist.XMLToList()
	test.convert_test()

	ltx = listtoxls.ListToXLS(test.filename, test.headings, test.all_questions)
	ltt = listtotest.ListToTest(test.filename, test.headings, test.all_questions, Teacher.NAME)

	new_text, new_array = ltt.createNewXML() # this is an xml_string and the corresponding xml_array

	#create_new_xml.CreateNewXML(template_doc, new_text, test.headings, template_zip)
	newXML = combinexml.Combine(template_doc, new_text, new_array, test.headings, template_zip)


	# TODO Next Steps ... 
	#	Find the location in the test document
	#	Add the new_text
	#	Re-Write the XML
	# 	Re-Create the Docx
__main__()


