# same as or replacement for xml to list

import os
import tempfile
import docx
import wordtoxml
import testdata
from lxml import etree 


class Questions:


	def __init__(self):
		# Get XML for the Questions Word Document
		filename = 'CPIdesofMarch'
		questionsXML = wordtoxml.WordToXML('word/' + filename + '.docx', "Select Test File")
		self.questiontree = questionsXML.xml_etree[0]
		# Create a temporary file that will become the combination of the template and the questions

		self.tmp_dir = tempfile.mkdtemp()
		newfilename = self.tmp_dir + '/' + filename + 'new.docx'
		self.newdoc = docx.Document()
		self.newdoc.save(newfilename)

		newWordXML = wordtoxml.WordToXML(newfilename)
		self.newdoctree = newWordXML.xml_etree[0]
		#zipfile.ZipFile(filename).extractall(newfilename)
		#print('New Document Tree')
		for paragraph in self.newdoctree:
			#print('Paragraph: ',paragraph, type(paragraph))
			p = paragraph
			#for tg in paragraph:
				#print ("tg: ", tg, '\ntag: ', tg.tag, '\nattrib: ', tg.attrib, '\nlist: ', list(tg))
				#if tg.tag[-2:] == '}r':
			#		for rtag in tg:
		#				if rtag.tag[-1:] == 't':
		#					print(rtag.text)
		#				if rtag.tag[-3:] == 'rPr':
		#					print(rtag)
		#		if tg.tag[-3:] == 'pPr':
		#			print(tg)
		#print('Original Questions')
		index = 1
		for paragraph in self.questiontree:
			#print('Paragraph: ',paragraph, type(paragraph))
			self.newdoctree.insert(index, paragraph)
			index += 1
			#for tg in paragraph:
				#print ("tg: ", tg, '\ntag: ', tg.tag, '\nattrib: ', tg.attrib, '\nlist: ', list(tg))
		#		if tg.tag[-2:] == '}r':
		#			for rtag in tg:
		#				if rtag.tag[-1:] == 't':
		#					print(rtag.text)
		#				if rtag.tag[-3:] == 'rPr':
		#					print(rtag)
		#		if tg.tag[-3:] == 'pPr':
		#			print(tg)

		#print('Newer Document Tree')
		#for paragraph in self.newdoctree:
		#	print('Paragraph: ',paragraph, type(paragraph))

		#print('\n\nFile String')
		tree = newWordXML.xml_etree

		xmlstr = etree.tostring(tree)
		print(xmlstr)
		new_file = self.tmp_dir + '/document.xml'
		print (self.tmp_dir)
		#with open(os.path.join(self.tmp_dir,'word/document.xml'), 'w') as f:
		with open(os.path.join(self.tmp_dir,'document.xml'), 'wb') as f:
			xmlstr = etree.tostring (tree, pretty_print=True)
			f.write(xmlstr)
			f.close()
		#newWordXML.xml_etree.write('newxml.xml')

		#For now, just add all of the tags from the test to the new file


		self.zip = questionsXML.zip
		self.filename = questionsXML.word_document
		self.doc = questionsXML.xml_etree[0]
		self.test_fields = testdata.TestFields()
		self.headings = self.test_fields.headings  # for Class, Instructor and instructions
		self.all_questions = []



		#doc.save() # what does this do?  What is doc that it needs to be closed?

#	def stripbold(self, questionsXML):
#		for tag in questionsXML:


	def __str__(self):
		result = ''
		for q in self.all_questions:
			result = result + str(q) + '\n'
		return result

	def create_question(self, q):
		question = testdata.Question(q.question_num, q.question_text, 
									 q.choices, q.answer_num)
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

	def process_tag_pPr(self, pPr, on_questions, q, text_tags):
		for pPrtag in pPr:
			if pPrtag.tag[-5:] == 'numPr':
				for numtag in pPrtag:
					if numtag.tag[-4:] == 'ilvl':	#indicates question or a choice
						# if there is a choice, save it now
						if q.choice_text != '':
							q.choices.append(q.choice_text)
							q.choice_text = ''
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
			text_tags.bold = False # do not keep the bolded answer choice
			q.choice_text = q.choice_text + text_tags.tag_phrase(text)
		else: # it is a heading
			q.heading_num = q.heading_num + 1
			if q.heading_num == 1:
				self.headings.section = text
			elif q.heading_num == 2:
				self.headings.test_name = text
			else:
				q.heading_text = q.heading_text + text_tags.tag_phrase(text)
		return

	def convert_test(self):
		on_questions = False

		text_tags = testdata.Text_Tags()
		tf = self.test_fields

		for paragraph in self.doc:
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
			tf.choices.append(tf.choice_text)

		self.all_questions.append(self.create_question(tf))

#TODO this is in combinexml - need to make its own class sometime
	def extract_zip(self, filename):
   		tmp_dir = tempfile.mkdtemp()
   		zipfile.ZipFile(filename).extractall(tmp_dir)
   		return tmp_dir
