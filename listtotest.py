import docx
from lxml import etree
from testdata import Teacher

RSIDR = '007244DA'
RSIDRDEFAULT = '007244DA'
RSIDRP = '007244DA'

ITALIC_TAG = '<i>'
ITALIC_TAG_END = '</i>'
PARAGRPH_START = '<w:p w:rsidRDefault="003F5639" w:rsidR="009705BC">'
PARAGRAPH_END = '</w:t></w:r>'

ITALIC = '<w:r><w:rPr><w:i/></w:rPr><w:t>'
BOLD = '<w:r><w:rPr><w:b/></w:rPr><w:t>'
UNDERLINE = '<w:r><w:rPr><w:u w:val="single"/></w:rPr><w:t>'
NEW_PARAGRAPH_START = '<w:r><w:t xml:space="preserve">'

#s = "First Question, it has some <u>underlined</u>and some <i>italicized</i> text."

#1. Find the first tag ... 
#2. s1 = "First Question, it has some "
#3. s3 = 'and some <i>italicized</i> text.'
#4. s2 = "underlined"
#5. new text = s1 + PARAGRAPH_END + UNDERLINE + s2 + PARAGRAPH_END + NEW_PARAGRAPH_START
#6. new text = text + s3 ... but, need to check if s3 has any tags.

# So, when you have a bold tag
# you have to put the Bold paragraph before it
# and you have to separate the text into three parts
# unbolded
# bolded
# unbolded
#
# so, you need the pre-paragraph part
# and, the post paragraph part
# split the string into three parts
# start, middle, end
# where the middle is the bolded piece
# put in the end paragraph and a start paragraph after start
# put in the bold paragraph
# put in the bold text
# put in the end paragraph
# now you have the end of the string left and you need 
# to determine if it has bolds in it, so ... do it again

# what order do I put the tags in if there are multiple? Bold, Underline, Italic
# so, bold would be on the inside and italic on the outside
# look for the outer one first, I think

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
		s = '<w:p w:rsidR="%s" w:rsidRDefault="%s"/>' % (RSIDR, RSIDRP)
		s += '<w:p w:rsidR="%s" w:rsidRDefault="%s" w:rsidP="%s">' % (RSIDR, RSIDRDEFAULT, RSIDRP)
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

	def isBold(self, text):
		return False

	def isItalic(self, text):
		if ITALIC_TAG in text:
			return True
		else:
			return False

	def isUnderline(self, text):
		return False

	def replaceItalicTag(self, text):
		start_index = text.find(ITALIC_TAG)
		end_index = text.find(ITALIC_TAG_END)
		s1 = text[:start_index]
		s2 = text[start_index+len(ITALIC_TAG):end_index]
		s3 = text[end_index+len(ITALIC_TAG_END):]
#5. text = s1 + PARAGRAPH_END + UNDERLINE + s2 + PARAGRAPH_END + NEW_PARAGRAPH_START
#6. new text = text + s3 ... but, need to check if s3 has any tags.

		result = s1 + PARAGRAPH_END + ITALIC + s2 + \
					  PARAGRAPH_END + NEW_PARAGRAPH_START

		if self.isItalic(result):
			result = replaceItalicTag(self, result)
		return result
																				#
	def createNewXML(self):
		test = ''
		for q in self.questions:
			if self.isItalic(q.question):
				q.question = self.replaceItalicTag(q.question)
				print("Italic: ", q.question)
			test += self.addQuestion(q.question)
			for c in q.choices:
				if self.isItalic(c):
					c = self.replaceItalicTag(c)
					print("Italic: ", c)
				test += self.addChoice(c)
		return test

