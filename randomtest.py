import wordtoxml
import questions
import testcreator
import listtoxls
from lxml import etree

# After running this, to make sure the page numbers are correct
# run latex -pdf filename.tex from the command line (eventually using perl)
# TODO
#		Fix text that is both italicized and underlined
#		Consider moving the underline to the right margin
#		Is the vertical space between questions too big
#		Test the code on different files and folders

def print_tree(node, level):
	result = ""
	for x in range (0, level):
		result += "\t"
	result += node.tag
	if node.text is not None:
	  result += " - " + node.text
	items = sorted(node.items())
	if (len(items) > 0):
		result += " attributes: "
		for name, value in items:
			result += " [" + name + "=" +  value + "]"
		#result += str(sorted(node.keys()))
	print(result)
	for child in node:
		print_tree(child, level+1)

TEST_FILE = "C:/My Documents/Coding Club/TestCreator/word/CPIdesOfMarch.docx"
#TEST_FILE = None
word = wordtoxml.WordToXML(TEST_FILE, "Choose the test file")

# Evaluate the questions/answers, determine questions and answers
test = questions.Questions(word)

# Save information stripped from word into an excel document
listtoxls.ListToXLS(TEST_FILE, test.headings, test.all_questions)

# Create the LaTeX document and the test versions
testcreator.TestCreator(test)
