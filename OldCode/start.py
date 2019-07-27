# Read in the Template Document
import wordtoxml
#import os
import zipfile
import tempfile
from lxml import etree as ET
#from xml.etree import ElementTree

TEMPLATE_FILE = "word/TestTemplate.docx"

#template = wordtoxml.WordToXML("word/TestTemplate.docx")
template = wordtoxml.WordToXML(TEMPLATE_FILE, "Choose the template file")
# Write the Template to a new Document
def extract_zip(filename):
	tmp_dir = tempfile.mkdtemp()
	zipfile.ZipFile(filename).extractall(tmp_dir)
	print(tmp_dir)
	return tmp_dir

tmp_dir = extract_zip(TEMPLATE_FILE)
xml_file = tmp_dir + '/word/document.xml'

def write_and_close_docx(xml_string, output_filename, tmp_dir):
	print(xml_string)
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

#xml_string = writeFile(filename, xml_string)
#newFilename = headings.section + headings.test_name + ' master.docx'
#self.write_and_close_docx(new_xml_string, newFilename, tmp_dir)

# See if you can open the new Document

#write_and_close_docx()