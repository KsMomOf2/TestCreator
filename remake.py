import wordtoxml
import questions
from lxml import etree

question_node = None

def find_questions_node(node):
	global question_node
	if node.text is not None:
	  if "Questions" in node.text:
	  	question_node = node
	else:
		for child in node:
			find_questions_node(child)


def print_tree(node, level):
	result = ""
	for x in range (0, level):
		result += "\t"
	result += node.tag
	if node.text is not None:
	  result += " - " + node.text
	k = sorted(node.items())
	if (len(k) > 0):
		for name, value in k:
			result += name + "=" + value + ","
		result += str(sorted(node.keys()))
	print(result)
	for child in node:
		print_tree(child, level+1)

def create_question_paragraph(txt, lvl, num):
	p = etree.Element("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p")
	pPr = etree.SubElement(p, "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr")
	pStyle = etree.SubElement(pPr, "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pStyle")
	numPr = etree.SubElement(pPr, "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numPr")
	ilvl = etree.SubElement(numPr, "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ilvl",
	val=lvl)
	numid = etree.SubElement(numPr, "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numId", 
		val=num)
	r = etree.Element("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r")
	t = etree.SubElement(r,"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t")
	t.text = txt
	return p

# Get the xml tree for the template file

#	This is a temporary assignment and should be replaced by allowing the 
#	user to specify the template file
TEMPLATE_FILE = "word/TestTemplate.docx"
template = wordtoxml.WordToXML(TEMPLATE_FILE, "Choose the template file")

#	Write the Template to a new Document
tmp_dir = template.extract_zip()
xml_file = tmp_dir + '/word/document.xml'

# Get the xml tree for the test questions/answers file

TEST_FILE = "word/CPIdesOfMarch.docx"
test = wordtoxml.WordToXML(TEST_FILE, "Choose the test file")

# Evaluate the questions/answers, determine questions and answers
questionsArray = questions.Questions(test)

# Randomize the quesions/Answers

# Remake the xml tree
template_etree = template.xml_etree
template_root = template_etree[0]
#print(etree.tostring(template_root, pretty_print=True))
#for child in template_root:
#	print(child.tag)

test_etree = test.xml_etree
test_root = test_etree[0]
#print(etree.tostring(test_root, pretty_print=True))
#for child in test_root:
#	print(child.tag)

#print_tree(test_root, 0)
#print_tree(template_root, 0)

#find_questions_node(template_root)
#print(question_node)

# INSERT a TEMPORARY NODE
#elem = etree.Element(question_node.tag)
#elem.text = "New Question"
#question_node.getparent().insert(0,elem)

#print_tree(template_root, 0)

#print(question_node)
# Insert the xml tree into the template xml tree

next_question_node = create_question_paragraph("This is the question", "0", "1")
print_tree(next_question_node, 0)

# Rezip the files into a docx file

# Write the test file