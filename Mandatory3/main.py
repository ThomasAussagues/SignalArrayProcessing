from questions.question1 import run_question_1
from questions.question2 import run_question_2
from questions.question3 import run_question_3
from questions.question4 import run_question_4
from questions.test import run_test
import sys
import os
sys.path.append(os.getcwd())

# tex: boolena, if true, the slides will be automaticaly compiled
tex = False

# disp: boolean, if true the slides will be open in a pdf reader
disp = False

if __name__ == '__main__':

    
    
    #run_question_1()
    #run_question_2()
    #run_question_3()
    #run_question_4()
    #run_test()

     # We compile the slides if tex = True
    if tex:
        print('-'*80)
        print('\nSlides complilation')
        if disp:
            os.system('''cd slides/
            pdflatex mandatory3.tex
            open mandatory3.pdf''')
        else :
            os.system('''cd slides/
            pdflatex mandatory3.tex
            ''')

        print('\nSlides compiled :)\n')