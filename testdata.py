class Teacher:


	NAME = 'Dr. Vacarro'


class Question:


	def __init__(self, number, text, choices, answer, instructions = None):
		self.number = str(number)
		self.question = text
		self.choices = choices
		self.answer = str(answer)
		self.instructions = instructions

	def __str__(self):
		if self.instructions != None:
			result = self.instructions
		else:
			result = ""
		result += str(self.number)
		result = result + '. ' + self.question
		for choice in self.choices:
			result = result + '\n\t' + choice
		result = result + '\n' + 'The answer is ' + self.answer
		return result


class Header:


	def __init__(self, section = 'Senior English', test_name = 'Exam', 
				 instructions = 'Write in capital letters.'):
		self.section = section
		self.test_name = test_name
		self.instructions = instructions

	def __init__(self):
		self.section = ''
		self.test_name = ''
		self.instructions = ''

	def __str__(self):
		result = self.section
		result = result + '\n' + self.test_name
		result = result + '\n\n' + self.instructions
		return result


class Text_Tags:


	def __init__(self):
		self.bold = False
		self.italic = False
		self.underline = False

	def tag_text(self, text, texttag):
		brace = f"{{"
		endbrace = f"}}"
		backslash = f"\\"
		tagged = backslash + texttag + brace + text + endbrace
		print (tagged)
		return tagged
		#return text + " (" + t + ") "

	def reset_text_tags(self):
		self.bold = False
		self.underline = False
		self.italic = False

	def tag_phrase(self, text):
		tagged_text = text
		if self.bold:
			tagged_text = self.tag_text(tagged_text,'textbf')
		if self.underline:
			tagged_text = self.tag_text(tagged_text, 'underline')
		if self.italic:
			tagged_text = self.tag_text(tagged_text, 'textit')
		self.reset_text_tags()
		return tagged_text

class TestFields:

	def __init__(self):
		self.question_text = ''
		self.choice_text = ''
		self.is_question = False
		self.is_choice = False
		self.choice_num = 0
		self.choices = []
		self.answer_num = 0
		self.headings = Header()
		self.heading_num = 0
		self.heading_text = ''
		self.question_num = 0

	def __str__(self):
		result = str(self.headings)

	def reset_question(self):
		self.question_text = ''
		self.is_question = True
		self.is_choice = False
		self.choice_num = 0
		self.choices = []
		self.answer_num = 0	