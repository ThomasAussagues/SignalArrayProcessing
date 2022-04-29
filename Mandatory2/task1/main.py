# LaTeX should be installed as it is used in the plots labels, titles, legends...

# Packages that you should install before executing main.py

# numpy: (obvious)
# matplotlib: (obvious)
# scipy: for finding peaks and loading .mat file
# cmcrameri: colormaps from Fabio Crameri

import sys
import os
sys.path.append(os.getcwd())

from utils.general_functions import generate_all_data,from_matlab_to_python
from questions.question1 import run_question1
from questions.question2 import run_question2
from questions.question3 import run_question3
from questions.question4 import run_question4
from questions.question5 import run_question5
from questions.question6 import run_question6
from questions.question7 import run_question7
from questions.question8 import run_question8
from questions.music_performances import assess_music_performances
from questions.snr_analysis import analysis

# tex: boolena, if true, the slides will be automaticaly compiled
tex = True

# disp: boolean, if true the slides will be open in a pdf reader
disp = True

# data: string, if data = 'python', then the script will use python data. Elif, data == 'matlab' the script will use matlab data
data = 'matlab'

# If you use matlab data, make sure that you converted the data before callling main.py 
# This can be done using the from_matlab_to_python function in utils.general_functions
# Note that even if you use matlab data, you should still edit the configuration file with the used matlab parameters


#################################################################################################################################
if __name__ == '__main__':

    

    print('\n'*4)
    print('-'*80)
    print('''\n\033[01m\033[34mIN5450 Mandatory 2

High-Resolution Beamforming on farfield monochromatic signals

Thomas Aussaguès, 24/03/2022
thomas.aussagues@imt-atlantique.net\033[0m\n''')
    print('\n'*2)
  

    # What data do you want to use? You can either use simulated data using MATLAB or python

    # python data
    if data == 'python':
        print('')
        #print('\n\033[01m\033[31mI am using python data\033[0m\n')
        # Uncomment these lines if you want to generate new data
        #print('Data generation')
        #generate_all_data()

    elif data == 'matlab':

        # I placed my matlab data (data_incoherent.mat and data_coherent.mat in data/matlab/) and I convert them into numpy objects

        from_matlab_to_python(matlab_file_name='data_incoherent.mat',numpy_file_name='data_incoherent')
        from_matlab_to_python(matlab_file_name='data_coherent.mat',numpy_file_name='data_coherent')
        for SNR in range(-10,11):
            from_matlab_to_python(matlab_file_name='data_coherent_{}.mat'.format(SNR),numpy_file_name='data_coherent_{}'.format(SNR))

        print('\n\033[01m\033[31mI am using MATLAB data\033[0m\n')

    # For each question, we specify which data we want to use with the string 'data'

    # Question 1
    print('\nQuestion 1')
    run_question1(data=data)
    # Question 2
    print('\nQuestion 2')
    run_question2(data=data)
    # Question 3
    print('\nQuestion 3')
    run_question3(data=data)
    # Question 4
    print('\nQuestion 4')
    run_question4(data=data)
    # Question5
    print('\nQuestion 5')
    run_question5(data=data)
    # Question6
    print('\nQuestion 6')
    run_question6(data=data)
    # Question7
    print('\nQuestion 7')
    run_question7(data=data)
    # Question8
    print('\nQuestion 8')
    run_question8(data=data)
    # MUSIC peformances: bias, angular resolution?
    print('\nMUSIC performances')
    assess_music_performances(data=data)
    # SNR analysis: How are performances affected when decreasing the SNR?
    print('\nSNR analysis')
    analysis(data=data)

    
    # We compile the slides if tex = True
    if tex:
        print('-'*80)
        print('\nSlides complilation')
        if disp:
            os.system('''cd slides/
            pdflatex mandatory2.tex
            open mandatory2.pdf''')
        else :
            os.system('''cd slides/
            pdflatex mandatory2.tex
            ''')
        os.system('''cd ../
            pdflatex readme.tex
            ''')

        print('\nSlides compiled :)\n')

    print('-'*80)
        
