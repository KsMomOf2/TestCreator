import tkinter as tk
from tkinter import filedialog
import zipfile
import tempfile
from lxml import etree
import os


class WordToXML:

#	word_document is the name (including the path) of the word document
#	zip is the zip archive of the word_document
#	xml_etree is the xml_tree of the word_document

#	Instantiating the WordToXML class fills all of the properties

	def __init__(self, filename=None, title = "Select Word File"):

		# Set up the location of the document

		if filename == None:
			self.word_document = self.getFile(title)
		else:
			self.word_document = filename	
		self.zip, self.xml_etree = self.get_xml_tree()
		self.folder = os.path.split(self.word_document)[0]

#	Using tkinter, allow the user to select a file (specifically a docx file)
#	Return the file name complete with its path.

	def getFile(self, title = "Select Word File"):
		root = tk.Tk()
		root.withdraw()

		directory = 'C:\''
		ext = ( ("All Word Documents", "*.docx"),("all files", "*.*"))
		path_file = filedialog.askopenfilename(initialdir = directory, 
											   title = title, filetypes = ext)

		return path_file


#	Read the word document xml and returns it as a tree.  

	def get_xml_tree(self):
		with open(self.word_document, 'rb') as f:
			zip = zipfile.ZipFile(f)
			xml_content = zip.read('word/document.xml')
		return zip, etree.fromstring(xml_content)

# 	Create a copy of the word document in a temporary folder by extracting
#	the archive and return the location of the folder.  
	def extract_zip(self):
		tmp_dir = tempfile.mkdtemp()
		zipfile.ZipFile(self.word_document).extractall(tmp_dir)
		return tmp_dir


