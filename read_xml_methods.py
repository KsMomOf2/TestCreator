import zipfile
from lxml import etree

# Set up the location of the test document
path = 'C:\\My Documents\\Coding Club\\TestCreator\\'
file = 'SeniorEnglishFinal'
word_document = path + file + '.docx'

# reads the word document xml and returns it as a tree.  Could actually just return the very first entry
def get_xml_tree(docx_filename):
	with open(docx_filename, 'rb') as f:
		zip = zipfile.ZipFile(f)
		xml_content = zip.read('word/document.xml')
		print(type(xml_content))
	return etree.fromstring(xml_content)

def create_question(num, text, choices, answer):
	question = []
	question.append(num)
	question.append(text)
	question.append(choices)
	question.append(answer)
	return question

def reset_question():
	global question_text, is_question, is_choice, choice_num, choices, answer_num
	question_text = ''
	is_question = True
	is_choice = False
	choice_num = 0
	choices = []
	answer_num = 0	

def process_question(list_level):
	global questions, question_num, question_text, choices, answer_num, choice_num, is_question, is_choice, headings, heading_text
	if not questions:
		headings.append(tag_phrase(heading_text, bold, italic, lined)) # save the instructions, which are complete now
		questions = True
	if list_level == '0':
	# save the previous question, if there is one (not the first time)
		if question_num > 0:
			all_questions.append(create_question(question_num, question_text, choices, answer_num))
		question_num = question_num + 1
		reset_question()
	else:
		choice_num = choice_num + 1
		choice_text = ''
		is_question = False
		is_choice = True

def tag_text(text, t):
	return '<' + t + '>' + text + '</' + t + '>' 

def reset_text_tags():
	global bold, italic, lined
	bold = False
	lined = False
	italic = False

def tag_phrase(text, b, i, u):
	tagged_text = text
	if b:
		tagged_text = tag_text(tagged_text,'b')
	if u:
		tagged_text = tag_text(tagged_text, 'u')
	if i:
		tagged_text = tag_text(tagged_text, 'i')
	reset_text_tags()
	return tagged_text

# global variables
bold = False
lined = False
italic = False

headings = []
heading_num = 0
heading_text = ''
all_questions = []
questions = False
is_question = False
is_choice = False
is_answer = False
question_text = ''
choices = []
question_num = 0
choice_text = ''
choice_num = 0
answer_num = 0
# this will be main, eventually
def convert_test():
	global headings, heading_text, all_questions, questions, is_question, is_choice, is_answer, question_text, choices, question_num, choice_text, choice_num, answer_num, bold, italic, lined

	xml_etree = get_xml_tree(word_document)
	doc = xml_etree[0]

	headings = []
	heading_num = 0

	for paragraph in doc:
		for tg in paragraph:
			if tg.tag[-2:] == '}r':
				for rtag in tg:
					if rtag.tag[-1:] == 't':
						if is_question:
							question_text = question_text + tag_phrase(rtag.text, bold, italic, lined)
						else:
							if is_choice:
								choice_text = choice_text + tag_phrase(rtag.text, False, italic, lined)
							else:
								heading_num = heading_num + 1
								if heading_num < 3:
									headings.append(rtag.text)
								else:
									heading_text = heading_text + tag_phrase(rtag.text, bold, italic, lined)
					if rtag.tag[-3:] == 'rPr':
						for rt in rtag:
							if rt.tag[-2:] == '}b':
								bold = True
								answer = True
								answer_num = choice_num
							elif rt.tag[-2:] == '}i':
								italic = True
							elif rt.tag[-2:] == '}u':
								lined = True
							else:
								answer = False	# ensure only the choice right after the 'b' is marked answer
			if tg.tag[-3:] == 'pPr':
				for pPrtag in tg:
					if pPrtag.tag[-5:] == 'numPr':
						for numtag in pPrtag:
							if numtag.tag[-4:] == 'ilvl':	#indicates either a question or a choice
								# if there is a choice, save it now
								if choice_text != '':
									choices.append(choice_text)
									choice_text = ''
								process_question(numtag.attrib.get(numtag.attrib.keys()[0]))							

	#save the last question
	all_questions.append(create_question(question_num, question_text, choices, answer_num))

	# print the headings and the questions

	for h in headings:
		print(h)
	print()
	for q in all_questions:
		print (q[0], ". ", q[1])
		for c in q[2]:
			print ('\t',c)
		print (q[3], ' is the answer')

convert_test()