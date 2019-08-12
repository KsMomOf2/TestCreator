from testdata import Question as q
from questions import Questions as qs

from pylatex import Document, Package, Section, Subsection, Command

from pylatex.utils import italic, NoEscape

from pylatex.base_classes.command import Arguments
from pylatex.base_classes.command import Options

all_qs = []

def mcExamOptions(output='concept', versions=4, version=1, randomq='true', randoma='true'):
    #output=concept, exam, key, answers, analysis
    options = 'output=' + output + ', '
    options += 'numberofversions=' + str(versions) + ', '
    options += 'version=' + str(version) + ', '
    options += 'seed=' + str(7) + ', '
    options += 'randomizequestions=' + randomq + ', '
    options += 'randomizeanswers=' + randoma + ', '
    options += 'writeRfile=' + 'false'
    return options

def keep_qandas_together():
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

def fill_document(doc):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    with doc.create(Section('A section')):
        doc.append('Some regular text and some ')
        doc.append(italic('italic text. '))

        with doc.create(Subsection('A subsection')):
            doc.append('Also some crazy characters: $&#{}')

def addQuestion(question):
    global doc
    if question.instructions != None:
        doc.append(Command('begin', 'mcquestioninstruction'))
        doc.append(question.instructions)
        doc.append(Command('end','mcquestioninstruction'))
    
    doc.append(Command('question'))
    doc.append(question.question)

    # this does not work properly - to fix the last answer in place 
    # ... the order is wrong in the resulting latex.  Need to figure it out
    #ans = Command('begin', extra_arguments = None, arguments='mcanswerslist', options='fixlast')
    ans = Command('begin', arguments='mcanswerslist')
    doc.append(ans)
#    print(ans.dumps())
    for index in range(0, len(question.choices)):
        if index + 1 == question.answer:
            opt = 'correct'
        else:
            opt = ''

        doc.append(Command('answer', options=opt))
        doc.append(question.choices[index])
    doc.append(Command('end', 'mcanswerslist'))

def add_allQs():
    global all_qs

    for quest in all_qs:
        addQuestion(quest)

doc = Document(document_options="letter")
 
def men():
    global doc
    create_qs()

    # Document with `\maketitle` command activated
    doc.packages.append(Package('mcexam', mcExamOptions('concept', 4, 1, 'true', 'true')))
    doc.packages.append(Package('calc'))
 
    doc.preamble.append(Command(command='renewenvironment', arguments=keep_qandas_together()))
    doc.append(Command('begin','mcquestions'))
    add_allQs()
    doc.append(Command('end', 'mcquestions'))

 #   doc.preamble.append(Command('title', 'Awesome TitBle'))
 #   doc.preamble.append(Command('author', 'Anonymous author'))
 #   doc.preamble.append(Command('date', NoEscape(r'\today')))
 #   doc.append(NoEscape(r'\maketitle'))

 #   fill_document(doc)

 #
    # Add stuff to the document
 #   with doc.create(Section('A second section')):
 #       doc.append('Some text.')

    doc.generate_pdf('basic_maketitle2', clean_tex=False, compiler='pdflatex')
    #tex = doc.dumps()  # The document as string in LaTeX syntax
    #print("\nText: \n" + tex + "\n")

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

men()