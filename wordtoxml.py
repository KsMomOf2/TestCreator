import tkinter as tk
from tkinter import filedialog
import zipfile
from lxml import etree


class WordToXML:


	def __init__(self, filename='', title = "Select Word File"):

		# Set up the location of the test document
		# This is used again when determing the name of the xls file
		if filename == '':
			self.word_document = self.getFile(title)
		else:
			self.word_document = filename	
		self.zip, self.xml_etree = self.get_xml_tree(self.word_document)

	def getFile(self, title = "Select Word File"):
		root = tk.Tk()
		root.withdraw()

		directory = 'C:\''
		ext = ( ("All Word Documents", "*.docx"),("all files", "*.*"))
		path_file = filedialog.askopenfilename(initialdir = directory, 
											   title = title, filetypes = ext)

		return path_file


	# Reads the word document xml and returns it as a tree.  
	# Could actually just return the very first entry

	def get_xml_tree(self, docx_filename):
		with open(docx_filename, 'rb') as f:
			zip = zipfile.ZipFile(f)
			xml_content = zip.read('word/document.xml')
			print (xml_content)
		return zip, etree.fromstring(xml_content)
