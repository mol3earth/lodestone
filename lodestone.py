#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 21:18:36 2020

@author: mark
"""


import pandas as pd 
import numpy as np
from datetime import datetime as dt
import matplotlib as mpl

def agreement(l1, l2):
    agree = []
    for i in range(len(l1)):
        if l1[i] == l2[i]:
            agree.append(True)
        else:
            agree.append(False)
    return agree

def avgAgree(what, n, n3, n5):
    avg3 = 100*n3/n
    avg5 = 100*n5/n
    return avg3, avg5

def getAverages(df, column, true_locs, column2=False, true_col=False):
    averages = {}
    for val in (df[column]).unique():
        val_locs = df[column] == val  
        val_df = df[val_locs]
        val_and = df[val_locs & true_locs]
        n_vals = len(val_df)
        averages[val] = {
            #'n' : n_vals,
            'avg' : 100*len(val_and)/n_vals
        }
        if column2:
            temp = getAverages(
                val_df, 
                column2, 
                (val_df[true_col] == True) 
            )
            temp2 = {}
            for key in temp.keys():
                temp2[key+'-'+'avg'] = temp[key]['avg']
            temp2['avg'] = averages[val]['avg']            
            averages[val] = temp2
    return averages

def dailyAgreement(df, n_labels):
    print('What is the agreement rate between the engineer and \
          all the raters for each day?')
    avg = getAverages(
        df, 
        'Date', 
        (df['%d-label agreement' % (n_labels)] == True), 
        'Rater', 
        '%d-label agreement' % (n_labels)
    )
    return avg

def getWeekStart(date, start_date=1):
    day = date.day #int(date.split('/')[1])
    week_day_start = int((day - start_date)/7)*7 + 1
    date = date.replace(day=week_day_start)
    #date = "10/" + str(week_day_start) + "/05"
    return date

def weeklyAgreement(df, n_labels):
    print('What is the agreement rate between the engineer and \
          all the raters for each week?')
    df_by_week = df.sort_values('Date')
    for i in range(len(df_by_week)):
        df_by_week.iat[i,0] = getWeekStart(df_by_week.iat[i,0])
    avg = getAverages(
        df_by_week, 
        'Date', 
        (df_by_week['%d-label agreement' % (n_labels)] == True), 
        'Rater', 
        '%d-label agreement' % (n_labels)
    )
    return avg

def raterAgreement(df, n_labels):
    avg = getAverages(
        df, 
        'Rater', 
        (df['%d-label agreement' % (n_labels)] == True)
    )
    print('Identify raters that have the highest agreement \
              rates with the engineer.')
    print('Identify raters that have the lowest agreement \
              rates with the engineer.')
    return avg

def tasks(df):    
    print('Identify raters that have completed the most Task IDs.')
    print('Identify raters that have completed the least Task IDs.')
    task_n = {}
    for rater in (df['Rater']).unique():
        rater_locs = df['Rater'] == rater  
        rater_df = df[rater_locs]
        task_n[rater] = {
            'n Tasks' : len((rater_df['Task ID']).unique())
        }
    return task_n

def precision(df, n_labels):
    print('What is the precision for each of the %d labels?' % (n_labels) )
    avg = getAverages(
        df, 
        'Correct Answers %d label' % (n_labels) , 
        (df['%d-label agreement'  % (n_labels)] == True)
    )
    return avg

def recall(df, n_labels):
    print('What is the recall for each of the %d labels?' % (n_labels) )
    avg = getAverages(
        df, 
        'Rater Answers %d Label' % (n_labels) , 
        (df['%d-label agreement'  % (n_labels)] == True)
    )
    return avg
     
def overallAgreement():
    print("What is the overall agreement rate considering that the" + 
          "raters have to be in agreement with both the" +
          "engineer's 3-label answer and the engineer's 5-label answer.")
    n_overall_agree = len(df[five_label_true & three_label_true])
    n_total = len(df)
    overall_agree_percent = 100*n_overall_agree/n_total
    print('Overall agreement: %.2f%%' % (overall_agree_percent))
    return overall_agree_percent

def barPlot(d, title, field=False, order=False, save_fig=False):
    if order:
        fig = pd.DataFrame(d).transpose().sort_index().plot.bar(
            title=title)
    else:
        fig = pd.DataFrame(d).transpose().plot.bar(
            title=title)
    fig.legend(loc='lower right')
    if save_fig:
        print('saving: %s' % (save_fig))
        fig.get_figure().savefig(save_fig, bbox_inches='tight')  

def makeDateArray(start='10/1/05',end='10/31/05'):
    start = start.split('/')
    end = end.split('/')
    dates = []
    day1 = int(start[1])
    day2 = int(end[1])
    n = day2 - day1 + 1 # inclusive
    for d in zip(
            [start[0]+'/']*n,
            [str(x) for x in range(day1,day2)],
            ['/'+start[2]]*n
            ):
        dates.append(
            dt.strptime('%s%s%s' % d,'%m/%d/%y')
        )
    return dates

dates = makeDateArray()
rater_ids = ['A','B','C','D','E']
five_labels = ['Bad', 'Okay', 'Intermediate', 'Great', 'Exceptional']
three_labels = ['Low', 'Average', 'High']
n_rows = 10000
 
rater_date = {
    'Date': 
        np.full(shape=1,fill_value='10/', dtype=object) + \
        np.random.randint(1, 30, n_rows).astype(str) + \
        np.full(shape=1,fill_value='/05', dtype=object),
    'Rater' : np.random.choice(rater_ids, n_rows),
    'Correct Answers 3 label' : np.random.choice(three_labels, n_rows),
    'Correct Answers 5 label' : np.random.choice(five_labels, n_rows),
    'Rater Answers 3 Label' : np.random.choice(three_labels, n_rows),
    'Rater Answers 5 Label' : np.random.choice(five_labels, n_rows),
    'Task ID' : np.random.randint(1, n_rows, n_rows)
}

for i in range(len(rater_date['Date'])):
    rater_date['Date'][i] = dt.strptime(
        rater_date['Date'][i],
        '%m/%d/%y')    
    
rater_date['3-label agreement'] = agreement(
        rater_date['Correct Answers 3 label'],
        rater_date['Rater Answers 3 Label']
)
rater_date['5-label agreement'] = agreement(
        rater_date['Correct Answers 5 label'],
        rater_date['Rater Answers 5 Label']
)
    

df = pd.DataFrame(rater_date)

five_label_true = (df['5-label agreement'] == True)
three_label_true = (df['3-label agreement'] == True)

d_avg_3 = dailyAgreement(df, 3)
d_avg_5 = dailyAgreement(df, 5)
barPlot(d_avg_3, 'Daily 3 label agreement', 'Date', dates, 'q1_3.png')
barPlot(d_avg_5, 'Daily 5 label agreement', 'Date', dates, 'q1_5.png')

w_avg_3 = weeklyAgreement(df, 3)
w_avg_5 = weeklyAgreement(df, 5)
barPlot(w_avg_3, 'Weekly 3 label agreement', 'q2_3.png')
barPlot(w_avg_5, 'Weekly 5 label agreement', 'q2_5.png')

r_avg_3 = raterAgreement(df, 3)
r_avg_5 = raterAgreement(df, 5)
barPlot(r_avg_3, 'Rater 3 label agreement', 'Rater', rater_ids, 'q3-4_3.png')
barPlot(r_avg_5, 'Rater 5 label agreement', 'Rater', rater_ids, 'q3-4_5.png')

task_n = tasks(df)
barPlot(task_n, 'Rater unique Tasks', 'Rater', rater_ids, 'q5-6.png')
precise_5 = precision(df, 5)
barPlot(precise_5, 'Precision 5 label', 'Correct Answers 5 label',  five_labels, 'q7.png')
recall_5 = recall(df, 5)
barPlot(recall_5, 'Recall 5 label', 'Rater Answers 5 Label', five_labels, 'q8.png')
precise_3 = precision(df, 3)
barPlot(precise_3, 'Precision 3 label', 'Correct Answers 3 label', three_labels, 'q9.png')
recall_3 = recall(df, 3)
barPlot(recall_3, 'Recall 3 label', 'Rater Answers 3 Label', three_labels, 'q10.png')


overallAgreement()