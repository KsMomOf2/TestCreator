
import os
import zipfile
import tempfile

TEMPLATE_FILE = "English Test Template.docx"
REPLACEMENT = "***"

class CreateNewXML:


	def __init__(self, templatefile, questionsxml, headings, templatezip):
		#TODO - this currently re-writes the xml file two different times - that is unnecessary
		self.zipfile = templatezip

		tmp_dir = self.extract_zip(templatefile)
		xml_file = tmp_dir + '/word/document.xml'
		
		templateArray, index = self.readFile(xml_file)
		templateArray[index] = str(headings) + questionsxml
		new_xml_string = self.create_xml_string(templateArray)

		print("New xml string", new_xml_string)

		#xml_string = writeFile(filename, xml_string)
		newFilename = headings.section + headings.test_name + ' master.docx'
		self.write_and_close_docx(new_xml_string, newFilename, tmp_dir)

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