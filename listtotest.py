import docx
from lxml import etree
from testdata import Teacher

RSIDR = '007244DA'
RSIDRDEFAULT = '007244DA'
RSIDRP = '007244DA'


class ListToTest:


	def __init__(self, filename, headings, questions, teacher):
		self.filename = filename
		self.headings = headings
		self.questions = questions
		self.teacher = Teacher.NAME
		self.doc = docx.Document()

#todo tHIS DOES NOT DO ANYTHING
	def addInstructions(self):
		self.doc.add_paragraph(headings[3])

	def addQuestion(self, question):
		s = '<w:p w:rsidR="%s" w:rsidRDefault="%s" w:rsidP="%s">' % (RSIDR, RSIDRDEFAULT, RSIDRP)
		s += '<w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="0"/>'
		s += '<w:numId w:val="1"/></w:numPr></w:pPr><w:r><w:t>'
		s += question
		s += '</w:t></w:r></w:p>'
		return s

	def addChoice(self, choice):
		s = '<w:p w:rsidR="%s" w:rsidRDefault="%s" w:rsidP="%s">' % (RSIDR, RSIDRDEFAULT, RSIDRP)
		s += '<w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="1"/>'
		s += '<w:numId w:val="1"/></w:numPr></w:pPr><w:r><w:t>'
		s += choice
		s += '</w:t></w:r></w:p>'
		return s

	def createNewXML(self):
		test = ''
		for q in self.questions:
			test += self.addQuestion(q.question)
			for c in q.choices:
				test += self.addChoice(c)
		return test

