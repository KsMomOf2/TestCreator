import wordtoxml
import questions
import testcreator
from lxml import etree

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

testcreator.TestCreator(test)

#for q in test.all_questions:
#	print(q)


