
import os
import zipfile
import tempfile
from lxml import etree as ET
from xml.etree import ElementTree

TEMPLATE_FILE = "word/TestTemplate.docx"
REPLACEMENT = "***"
PTAG = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'

class Combine:



	def __init__(self, templatefile, questionsxml, questions_array, headingsxml, templatezip):
		#print (ElementTree.XML(questionsxml)) # needs full tags, I think
		self.zipfile = templatezip

		tmp_dir = self.extract_zip(templatefile)
		xml_file = tmp_dir + '/word/document.xml'
		templateTree = ET.parse(xml_file)
		templateRoot = templateTree.getroot()[0]

		#self.print_tree(templateRoot)

		paragraphs = templateRoot.findall(PTAG)
		#print (paragraphs)

		for p in paragraphs:
			if "Questions" == ''.join(p.itertext()):
				qloc = p
			elif "Instructions" == ''.join(p.itertext()):
				iloc = p
		#print("Questions Tag\n", self.print_sublist("q",qloc))

		qparent = iloc.getparent()
		index = qparent.index(iloc)+1
		for q_p in questions_array:
			qparent.insert(index, self.create_paragraph(q_p))
		#qloc.insert(self.create_paragraph("This is a new paragraph!"))
		#self.print_sublist("qr", qloc)

		paragraphs = templateRoot.findall(PTAG)
		#print (paragraphs)
		templateTree.write('test.xml')
		#print("Instructions Tag\n", self.print_sublist("I",instructionsloc))
		
		#print (questionsloc.tag)
		#print (questionsloc.attrib)
		#print ("".join(questionsloc.itertext()))

		#print (questionsloc.text)
		#print (questionsloc.tail)

			#self.print_sublist("elem",list(questionsloc.attrib))
			#self.print_sublist("keys",questionsloc.keys())
			#self.print_sublist("items",questionsloc.items())
			#self.print_tree(questionsloc)

		#xml_string = writeFile(filename, xml_string)
		#newFilename = headings.section + headings.test_name + ' master.docx'
		#self.write_and_close_docx(new_xml_string, newFilename, tmp_dir)

	def create_paragraph(self, txt):
		print(txt)
		p = ET.Element(PTAG)
		p.text = txt
		return p

	def print_sublist(self, subtype, list):
		for n in list:
			print ('\t', subtype, '\t', n)

	def print_tree(self, tree):
		print ('tag: ', tree.tag)
		for i in tree.items():
			print ("\titem: ",i)
		for k in tree.keys():
			print ("\tkey : ",k)
		print (tree.keys())
		for a in tree.attrib:
			print ('\tattrib:', a)
		print ('\ttail: ', tree.tail)
		print ('\ttext: ', tree.text)
		for child in tree:
			if child is not None:
				self.print_tree (child)

	def create_xml_string(self, xml_array):
		xml = ''
		for line in xml_array:
			xml += line
		return xml
	
	def readFile(self, filename):
		initialFile = []
		line_num = 0
		index = 0
		print(filename)
		
		f = open(filename, "r")
		for line in f:
			if REPLACEMENT in line:
				loc = line.find(REPLACEMENT)
				initialFile.append(line[:loc])
				line_num += 1
				initialFile.append(REPLACEMENT)
				index = line_num
				line_num += 1
				newloc = loc + len(REPLACEMENT) - len(line)
				initialFile.append(line[newloc:])
				print("Loc: ", loc)
				print("Prefix ", line[:loc])
				print("New Loc ", newloc)
				print("Post ", line[newloc:])
			else:
				initialFile.append(line)
			line_num += 1
		f.close
		print (index, " - ", initialFile)
		return initialFile, index

	#def writeFile(self, filename, xml_string):
	#	f = open(filename, "w")
	#	f.write(xml_string)
	#	f.close()

#	def zipdir(path, ziph):
	# ziph is zipfile handle
#	for root, dirs, files in os.walk(path):
#	for file in files:
			#	ziph.write(os.path.join(root, file))

	#def zipdoc(filename):
#	zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
#	zipdir('words/', zipf)
   # 	zipf.close()

	def extract_zip(self, filename):
   		tmp_dir = tempfile.mkdtemp()
   		zipfile.ZipFile(filename).extractall(tmp_dir)
   		return tmp_dir

	def write_and_close_docx(self, xml_string, output_filename, tmp_dir):

		with open (os.path.join(tmp_dir, 'word/document.xml'), 'w') as f:
			f.write(xml_string)
		f.close()

		filenames = self.zipfile.namelist()
		print(filenames)

		zip_copy_filename = output_filename
		with zipfile.ZipFile(zip_copy_filename, "w") as docx:
			for filename in filenames:
				docx.write(os.path.join(tmp_dir,filename), filename)

		# Clean up the temp dir
		#shutil.rmtree(tmp_dir)