from testdata import Question as q
from testdata import Teacher
from questions import Questions as qs

from pylatex import Document, Package, PageStyle, Head, Foot, LineBreak, simple_page_number, \
Section, Subsection, Command, HorizontalSpace

from pylatex.utils import italic, bold, NoEscape

from pylatex.base_classes.command import Arguments
from pylatex.base_classes.command import Options
import os

class TestCreator:

    def __init__(self, questions):
        self.all_qs = questions.all_questions
        self.headers = questions.headings
        self.folder = questions.folder
        self.filename, self.extension = os.path.splitext(os.path.basename(questions.wordfile))
        self.doc = None
        self.convert()

    def generate_header(self, output = "Exam", instructor="Vaccaro", section="English", test_name="Final Exam", version = 1):
        header = PageStyle("header")
        with header.create(Head("C")):
            header.append(instructor)
            header.append(LineBreak())
        with header.create(Head("L")):
            header.append(section)
            header.append(LineBreak())
            header.append(test_name + str(version) if output != 'key' else test_name)
        with header.create(Head("R")):
            if (output == "exam"):
                header.append("Student: _____________")
            elif (output == "answers"):
                header.append("Answers v" + str(version))
            else:
                header.append("Key")
        with header.create(Foot("R")):
             header.append(simple_page_number())
        return header

    def mcExamOptions(self, output='concept', versions=4, version=1, randomq='true', randoma='true'):
        #output=concept, exam, key, answers, analysis
        options = 'output=' + output + ', '
        options += 'numberofversions=' + str(versions) + ', '
        options += 'version=' + str(version) + ', '
        options += 'seed=' + str(7) + ', '
        options += 'randomizequestions=' + randomq + ', '
        options += 'randomizeanswers=' + randoma + ', '
        options += 'writeRfile=' + 'false'
        return options

    def keep_qandas_together(self):
    # Code to keep the questions and answers on the same page
    # Returns an Arguments type
        linewidthCmd = Command(command='linewidth')
        labelWidthCmd = Command(command='labelwidth')
        beginMiniPgCmd = Command(command='begin',arguments='minipage', options='t', extra_arguments=NoEscape(linewidthCmd.dumps() + '-' + labelWidthCmd.dumps()))
        endMiniPgCmd = Command(command='end', arguments='minipage')
        parCmd = Command(command='par')
        arg2 = NoEscape(beginMiniPgCmd.dumps())
        arg3 = NoEscape(endMiniPgCmd.dumps()+parCmd.dumps())
        return Arguments('setmcquestion', arg2 , arg3)

    def addAnswerList(self, question):
        self.doc.append(Command('begin', arguments='mcanswerslist'))

        if question.alloftheabove and question.noneoftheabove:
            self.doc.append(NoEscape("[permutenone]"))
        elif question.alloftheabove or question.noneoftheabove:
            self.doc.append(NoEscape("[fixlast]"))
  
        for index in range(0, len(question.choices)):
            if str(index + 1) == question.answer:
                opt = 'correct'
            else:
                opt = ''

            self.doc.append(Command('answer', options=opt))
            self.strip_tags(question.choices[index])

        self.doc.append(Command('end', 'mcanswerslist'))


    def addQuestion(self, question):
        if question.instructions != None:
            self.doc.append(Command('begin', 'mcquestioninstruction'))
            self.doc.append(question.instructions)           
            self.doc.append(Command('end','mcquestioninstruction'))
        
        self.doc.append(Command('question'))
        self.strip_tags(question.question)

        self.addAnswerList(question)

        
    def add_allQs(self):
        for quest in self.all_qs:
            self.addQuestion(quest)

    def strip_tags(self, string):
        while '\\' in string:
            # Find slash, grab the text before the slash (left), find the other locations
            # that are key - the braces - and grab the key and the emphaszied text, then
            # send the rest of the rest of the string back through the while loop in case
            # there are other tags that need to be stripped
            # TODO: what happens if text is both italicized and underlined?

            slashLocation = string.find('\\')
            left = string[:slashLocation]
            textStart = string.find('{')
            tag = string[slashLocation+1:textStart]
            tagEnd = string.find('}')
            emphasizedText = string[textStart+1:tagEnd]
#            if '\\' in emphasizedText:
                # so ... with a double tag ... you have to 
                # update where the tagEnd is, put the left stuff in the document
                # put the first tag in and the first part of the emphasized text in
                # then the strip the tags from the new emphasized text
                # and what do you do with the right side ... hmmmm
#                self.strip_tags(emphasizedText)

            # Append the text as appropriate
            self.doc.append(left)
            if tag =='underline':
                self.doc.append(Command('underline', emphasizedText)) 
            elif tag == 'textit':
                self.doc.append(italic(emphasizedText)) 
            elif tag == 'textbf':
                self.doc.append(bold(emphasizedText))
            else:
                self.doc.append(emphasizedText)
            if string[tagEnd+1:tagEnd+2]==' ': # Force a space
                self.doc.append(bold(' '))
            string = string[tagEnd+1:]  # remove what was added to the doc already from the string
#   After the while loop is done, if there is any string left, append it (it is not emphasized)
        self.doc.append(string)


    def add_instructions(self, instructions):
        # Leaving this in its own method in case we want to add different formatting for the instructions
        self.strip_tags(instructions)

 
    def add_mcexam_package(self, output='exam', version=1, versions=4, randomq='true', randoma='true'):
        return Package('mcexam', self.mcExamOptions(
                output=output, #concept, exam, key, answers, analysis
                versions=versions, 
                version=version, 
                randomq=randomq, 
                randoma=randoma))

    def add_packages(self, output, version, versions=4, randomq='true', randoma='true'):
    #        self.doc.packages.append(Package('mcexam', self.mcExamOptions('concept', 4, 1, 'true', 'true')))
        self.doc.packages.append(self.add_mcexam_package( output, version, versions, randomq, randoma))
        self.doc.packages.append(Package('calc'))
        self.doc.packages.append(Package('geometry', options='margin=0.75in'))


    def convert(self, versions=4, randomq='true', randoma='true'):
        #create_qs()
        newfolder = self.folder + '/' + self.filename
        if not os.path.exists(newfolder):
            os.mkdir(newfolder)

        output = 'exam' # output needs to run through a list to get all versions
        for output in {'exam', 'answers', 'key'}:
            for version in range(1, versions+1):
                if output == 'key' and version > 1: # Only create 1 key document with all versions
                    break

                self.doc = Document(document_options="letter")
                self.add_packages(output, version, versions, randomq, randoma)

                self.doc.preamble.append(Command(command='renewenvironment', arguments=self.keep_qandas_together()))
                self.doc.preamble.append(self.generate_header(output,
                    Teacher.NAME, 
                    self.headers.section, 
                    self.headers.test_name,
                    version))
                self.doc.change_document_style("header")

                self.add_instructions(self.headers.instructions)
                self.doc.append(Command('begin','mcquestions'))
                self.add_allQs()
                self.doc.append(Command('end', 'mcquestions'))

        #        self.doc.generate_pdf('basic_maketitle2', clean_tex=False, compiler='pdflatex')
                if (output == 'key'):
                    newfilename = newfolder+'/'+self.filename+'_'+output
                else:
                    newfilename = newfolder+'/'+self.filename+'_'+output+'_v'+str(version)
                self.doc.generate_pdf(newfilename, clean_tex=False, compiler='pdflatex')
                print("." + " " + newfilename)
                #tex = doc.dumps()  # The document as string in LaTeX syntax
                #print("\nText: \n" + tex + "\n")

    # Just creating a few questions for testing purposes.

def create_qs():
    global all_qs
    all_qs = []

    ans1 = []
    ans1.append("Answer 1")
    ans1.append("Answer 2")
    ans1.append("Answer 3")
    ans1.append("Answer 4")
    ans1.append("Answer 5")
    q1 = q(1, "Question 1", ans1, 3)

    ans2 = []
    ans2.append("Answer 6")
    ans2.append("Answer 7")
    ans2.append("Answer 8")
    ans2.append("Answer 9")
    q2 = q(2, "Question 2", ans2, 1, "Question two instructions")

    all_qs.append(q1)
    all_qs.append(q2)

    #for question in all_qs:
    #    print(question)
