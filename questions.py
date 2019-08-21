import testdata

class Questions:
# questionsXML is a WordToXML object

# headings is an object with Class, Instructor, Instructions
# all_questions is an array of the question/choices/answer objects

	def __init__(self, questionsXML):


		self.headings = testdata.Header()  # for Class, Instructor and instructions
		self.all_questions = []
		self.folder = questionsXML.folder
		self.wordfile=questionsXML.word_document
		self.convert_test(questionsXML.xml_etree[0])

	def __str__(self):
		result = ''
		for q in self.all_questions:
			result = result + str(q) + '\n'
		return result

	def create_question(self, q):
		question = testdata.Question(q.question_num, q.question_text, 
									 q.choices, q.answer_num, q.alloftheabove, q.noneoftheabove)
		return question

	def process_question(self, list_level, q):
		if list_level == '0':

		# save the previous question - there is not one the first time
			if q.question_num > 0:
				self.all_questions.append(self.create_question(q))
			q.question_num = q.question_num + 1
			q.reset_question()
		else:
			q.choice_num = q.choice_num + 1
			q.choice_text = ''
			q.is_question = False
			q.is_choice = True
		return 

# The answers are in the rPr tag
	def process_tag_rPr(self, rtag, q, text_tags):
		answer = False
		for rt in rtag:
			if rt.tag[-2:] == '}b':
				text_tags.bold = True
				answer = True
				q.answer_num = q.choice_num
			elif rt.tag[-2:] == '}i':
				text_tags.italic = True
			elif rt.tag[-2:] == '}u':
				text_tags.underline = True
			else:
				answer = False	# ensure choice right after 'b' is marked answer
		return answer

	def remove_end_comma(self, choice):
		if choice[-1:] == "}":
			save = '}'
		else:
			save = ''
# TODO: This does not work for a choice that ends: "word, I" 
		if ',' in choice[-3:]:
			if choice[-1:] == ',':
				choice = choice[:-1]
			if choice[-2:-1] == ',':
				choice = choice[:-2]
			if choice[-3:-2] == ',':
				# TODO need to make sure that there are no non-brace char at the end
				choice = choice[:-3]
			return choice + save
		return choice


	def add_choice(self, q):
		q.choice_text = self.remove_end_comma(q.choice_text)		
		if q.choice_text != '':
			if 'none of the above' in q.choice_text:
				q.noneoftheabove = True
			if 'all of the above' in q.choice_text:
				q.alloftheabove = True
			q.choices.append(q.choice_text)
			q.choice_text = ''
		

	def process_tag_pPr(self, pPr, on_questions, q, text_tags):
		for pPrtag in pPr:
			if pPrtag.tag[-5:] == 'numPr':
				for numtag in pPrtag:
					if numtag.tag[-4:] == 'ilvl':	#indicates question or a choice
						# if there is a choice, save it now
						if q.choice_text != '':
							self.add_choice(q)
#							if 'none of the above' in q.choice_text:
#								q.noneoftheabove = True
#							if 'all of the above' in q.choice_text:
#								q.alloftheabove = True
#							q.choices.append(q.choice_text)
#							q.choice_text = ''
						if not on_questions:
							# instructions are complete if you have a level
							self.headings.instructions = \
											text_tags.tag_phrase(q.heading_text)
							on_questions = True
						level = numtag.attrib.get(numtag.attrib.keys()[0])
						self.process_question(level, q)							
		return

	def process_tag_text(self, text, q, text_tags):
		if q.is_question:
			q.question_text = q.question_text + text_tags.tag_phrase(text)
		elif q.is_choice:
			text_tags.bold = False # do not keep the answer choice bolded
			q.choice_text = q.choice_text + text_tags.tag_phrase(text)
		else: # it is a heading, 1st line contains section, 2nd test name
			q.heading_num = q.heading_num + 1
			if q.heading_num == 1:
				self.headings.section = text
			elif q.heading_num == 2:
				self.headings.test_name = text
			else:
				q.heading_text = q.heading_text + text_tags.tag_phrase(text)
		return

	def convert_test(self, doc):
		on_questions = False	# changed to true after headers are processed

		tf = testdata.TestFields()
		text_tags = testdata.Text_Tags()

		for paragraph in doc:
			for tg in paragraph:
				if tg.tag[-2:] == '}r':
					for rtag in tg:
						if rtag.tag[-1:] == 't':
							self.process_tag_text(rtag.text, tf, text_tags)
						if rtag.tag[-3:] == 'rPr':
							answer = self.process_tag_rPr(rtag, tf, text_tags)
				if tg.tag[-3:] == 'pPr':
					self.process_tag_pPr(tg, on_questions, tf, text_tags)

		#save the last question
		if tf.choice_text != '':
			self.add_choice(tf)

#			if 'none of the above' in tf.choice_text:
#				tf.noneoftheabove = True
#			if 'all of the above' in tf.choice_text:
#				tf.alloftheabove = True
#			tf.choices.append(tf.choice_text)

		self.all_questions.append(self.create_question(tf))
