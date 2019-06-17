import zipfile

path = 'C:\\My Documents\\Coding Club\\TestCreator\\'
file = 'SeniorEnglishFinal'
xml_filename = 'document.xml'

word_filename = path + file + '.docx'
xml_file = path + xml_filename
zip = zipfile.ZipFile(open(word_filename, 'rb'))
xml_string = zip.read('word/document.xml')

from lxml import etree
#xtree = etree.fromstring(xml_string)
xtree = etree.fromstring(xml_string)

#etree.tostring(xtree, pretty_print=True)

#def _itertext(my_etree):
#	for node in my_etree.iter(tag=etree.Element):
#		#if _check_element_is(node, 't'):
#		yield(node, node.text)

#def _check_element_is(element, type_char):
	#word_schema = 'http:/schemas.openxmlformats.org/wordprocessingml/2006/main'
	#return element.tag == '{%s}%s' % (word_schema, type_char)
#	return element.tag

#print ('start')

#for node, txt in _itertext(xtree):
#	print (txt)
#	print('')

#print('end')
#print (xtree)
#print ('starting')
#for node in xtree:
#	print(node.tag, node.attrib)
import xml.etree.cElementTree as ET

def parseXML(xml_file):
    """
    Parse XML with ElementTree
    """
    tree = ET.ElementTree(file=xml_file)
    print(tree.getroot())
    root = tree.getroot()
    print("tag=%s, attrib=%s" % (root.tag, root.attrib))

    for child in root:
        print(child.tag," attr: ", child.attrib)
        if child.tag == "ilvl":
       # if child.tag == "appointment":
            for step_child in child:
                print("tag: ",step_child.tag)

    # iterate over the entire tree
    print("-" * 40)
    print("Iterating using a tree iterator")
    print("-" * 40)
    iter_ = tree.getiterator()
    for elem in iter_:
        if elem.tag[-4:] == 'ilvl':
        	print(elem.tag,elem.attrib)
        	#print (list(elem))
        	#for es in list(elem):
        	 # print (es.text)
    	#print("elem: ",elem.tag)

    # get the information via the children!
    print("-" * 40)
    print("Iterating using getchildren()")
    print("-" * 40)
#    appointments = root.getchildren()
#    for appointment in appointments:
#        appt_children = appointment.getchildren()
#        for appt_child in appt_children:
#            print("%s=%s" % (appt_child.tag, appt_child.text))

if __name__ == "__main__":
	parseXML(xml_file)