
from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask import Blueprint, render_template 
from flask_login import login_required, current_user
import random, copy
from .extensions import db
from .models import User
import itertools 

main = Blueprint('main', __name__)

edc = {
    #Format is 'question':[options]
    'Where does the Q point lie for class B amplifier?':['Cut off','Active','Saturation','Between saturation and active'],
    'What is the value of the maximum efficiency of the class B amplifier?':['50% to 70%','35%','35% to 50%','25%'],
    'Which is the main disadvantage of class B amplifiers?':['Expensive','Less efficient','More power dissipation','More heat dissipation'],
    'How to avoid cross over distortion?':['By shifting the Q point above cut off','By using more resistance','By using more capacitance','By using more Inductance'],
    'What is the conduction angle for Class B push-pull amplifier?':['180','270','0','90'],
    'The maximum efficiency of transformer coupled class A power amplifier is ____________':[' 50%','25%','30%','5%'],
    'In class A operation, the operating point is generally located ____________ of the d.c. load line.':['At the middle','At cut off point','At saturation point','In active region']
}

ss = {
    #Format is 'question':[options]
    'Unit impulse ∂(t) is _____ of time t.':['Even function','Odd function','Neither even nor odd function','Odd function of even amplitude'],
    'What is the full form of the LTI system?':['Linear Time Invariant system','Late time inverse system','Linear time inverse system','Linearity times invariant system'],
    'How are the convolution integral of signals represented?':['x(t)*h(t)','x(t)+h(t)','x(t)+h(t)','x(t)**h(t)'],
    'If h1, h2 and h3 are cascaded, find the overall impulse response':['h1 * h2 * h3','h1 + h2 + h3','h3','h1 * h2'],
    'What are the tools used in a graphical method of finding convolution of discrete time signals?':['Plotting, shifting, folding, multiplication, and addition in order','Scaling, shifting, multiplication, and addition in order','Scaling, multiplication and addition in order','Scaling, plotting, shifting, multiplication and addition in order'],
    'The convolution of x(n)={1,2,3,1} and h(n)={1,2,1,-1}, origin at 2, is?':['{1,4,8,8,3,-2,-1}, origin at 4','{1,4,8,8,3,-2,1}, origin at 4',' {1,3,8,8,3,-2,-1}, origin at 4','{1,4,8,3,-2,-1}, origin at 4'],
    'Find the convolution of x1[n] = {1, 2, 3, 4} and x2[n] = {2, 1, 2, 1}.':['Y [n] = {14, 16, 14, 16}','Y[n] = {14, 10, 14, 10}','Y [n] = {14, 16,-14,-16}','Y [n] = {14,-16,-14, 16}']
}

python = {
    #Format is 'question':[options]
    'Is Python case sensitive when dealing with identifiers?':['yes','no','machine dependent','none of the mentioned'],
    'Which of the following is an invalid variable?':['1_string','string_1','goo','___string___'],
    'Which of the following is an invalid statement?':['a b c = 1000 2000 3000','abc = 1,000,000','a_b_c = 1,000,000','a,b,c = 1000, 2000, 3000'],
    'Which of the following cannot be a variable?':['in','it','on','__init__'],
    'What does ~4 evaluate to?':['-5','-4','-3','+3'],
    'What does 3 ^ 4 evaluate to?':['7','81','12','0.75'],
    'Which of the following is the truncation division operator?':['//','|','%','/']
}

#questions = copy.deepcopy(original_questions)

def shuffle(q):
    selected_keys = []
    i = 0
    while i < len(q):
        current_selection = random.choice(list(q.keys()))
        if current_selection not in selected_keys:
            selected_keys.append(current_selection)
            i = i+1
    return selected_keys


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/select')
@login_required
def select():    
    return render_template('solve.html', name=current_user.name)
    

@main.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if 'logged' in session:
        if request.method == 'POST':    
            if request.form['choice'] == 'edc':
                session['quiz_session'] = 'edcquiz'
                title = 'Electronic Devices & Circuits'
                original_questions = edc
            elif request.form['choice'] == 'ss':
                session['quiz_session'] = 'ssquiz'
                title = 'Signals & Systems'
                original_questions = ss
            elif request.form['choice'] == 'python':
                session['quiz_session'] = 'pyquiz'
                title = 'Python'
                original_questions = python

            if 'quiz_session' in session:
                questions = copy.deepcopy(original_questions)
                questions_shuffled = shuffle(questions)

                #correct_ans = original_questions[i][0]

                for i in questions.keys():
                    random.shuffle(questions[i])

                return render_template('main.html', name=current_user.name, q = questions_shuffled, o = questions, t = title)
            else: 
                return redirect(url_for('main.select'))
        
        else:
            flash('Please select one of the quiz')
            return redirect(url_for('main.select'))
    
    else:
        flash('Please login details to access this page.')
        return redirect(url_for('auth.login'))


@main.route('/quiz_answers', methods=['GET', 'POST'])
@login_required
def quiz_answers():
    if 'logged' in session:
        if request.method == 'POST':
            correct = 0
            if request.form['subjectname'] == 'Electronic Devices & Circuits':
                title = 'Electronic Devices & Circuits'
                original_questions = edc
            elif request.form['subjectname'] == 'Signals & Systems':
                title = 'Signals & Systems'
                original_questions = ss
            elif request.form['subjectname'] == 'Python':
                title = 'Python'
                original_questions = python
            else:
                pass

            questions = copy.deepcopy(original_questions)

            for i in questions.keys():
                answered = request.form[i]
                if original_questions[i][0] == answered:
                    correct = correct + 1
            ques = len(original_questions)
            marks = (float(correct)/float(ques))*100

            if marks>=45:
                result = 'PASS'
            else:
                result = 'FAIL'

            if 'quiz_session' in session:
                session.pop('quiz_session', None)
                
            return render_template('result.html', name=current_user.name, o = questions, c=str(correct), q=str(ques), p=str(marks), r=result, t=title )

        else:
            flash('Access denied!')
            return redirect(url_for('main.quiz'))

    else:
        flash('Please login details to access this page.')
        return redirect(url_for('auth.login'))

