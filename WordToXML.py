import tkinter as tk
from tkinter import filedialog
import zipfile
from lxml import etree

class WordToXML:

	def __init__(self):

		# Set up the location of the test document
		self.word_document = self.getFile()		
		self.xml_etree = self.get_xml_tree(self.word_document)

	def getFile(self):
		root = tk.Tk()
		root.withdraw()

		directory = 'C:\''
		title = "Select Test Document"
		ext = ( ("All Word Documents", "*.docx"),("all files", "*.*"))
		path_file = filedialog.askopenfilename(initialdir = directory, title = title, filetypes = ext)

		return path_file


	# reads the word document xml and returns it as a tree.  Could actually just return the very first entry
	def get_xml_tree(self, docx_filename):
		with open(docx_filename, 'rb') as f:
			zip = zipfile.ZipFile(f)
			xml_content = zip.read('word/document.xml')
		return etree.fromstring(xml_content)
