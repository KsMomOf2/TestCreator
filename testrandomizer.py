import xmltolist
import listtoxls
import listtotest
from testdata import Teacher

def __main__():
	xtl = xmltolist.XMLToList()
	xtl.convert_test()

	ltx = listtoxls.ListToXLS(xtl.filename, xtl.headings, xtl.all_questions)
	ltt = listtotest.ListToTest(xtl.filename, xtl.headings, xtl.all_questions, Teacher.NAME)

	new_text = ltt.createNewXML()
	print(len(new_text))
	print(new_text)
	#for i in range (0,4):
	#	print(new_text[i])
	#	i += i + 1
__main__()


