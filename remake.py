import wordtoxml
import questions
import latex

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


# Get the xml tree for the template file

#	This is a temporary assignment and should be replaced by allowing the 
#	user to specify the template file
TEMPLATE_FILE = "word/TestTemplate.docx"
template = wordtoxml.WordToXML(TEMPLATE_FILE, "Choose the template file")

tmp_dir = template.extract_zip()
xml_file = tmp_dir + '/word/document.xml'
print(xml_file)

# Get the xml tree for the test questions/answers file

TEST_FILE = "word/CPIdesOfMarch.docx"
test = wordtoxml.WordToXML(TEST_FILE, "Choose the test file")

# Evaluate the questions/answers, determine questions and answers
questionsArray = questions.Questions(test)

for q in questionsArray.all_questions:
	print(q)


