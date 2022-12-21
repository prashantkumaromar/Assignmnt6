import sqlite3
from sqlite3 import Error

import numpy as np
import pandas as pd
from faker import Faker
pd.set_option('mode.chained_assignment', 'raise')


def create_connection(db_file, delete_db=False):
    import os
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)
    return conn


#conn = create_connection('non_normalized.db')
#sql_statement = "select * from Students;"
#df = pd.read_sql_query(sql_statement, conn)
#print(df)



"""
Open connection to the non-normalized database and generate a 'df_degrees' dataframe that contains only
the degrees. See screenshot below. 
"""

    # BEGIN SOLUTION

def create_df_degrees(non_normalized_db_filename): 
    conn = create_connection(non_normalized_db_filename)
    sql_statement = "SELECT DISTINCT degree FROM Students;"
    df_degrees=pd.read_sql_query(sql_statement, conn) 
    return df_degrees  

    
    
    
    
    

    # END SOLUTION


    
    """
    Open connection to the non-normalized database and generate a 'df_exams' dataframe that contains only
    the exams. See screenshot below. Sort by exam!
    hints:
    # https://stackoverflow.com/a/16476974
    # https://stackoverflow.com/a/36108422
    """

    # BEGIN SOLUTION
def create_df_exams(non_normalized_db_filename):
    conn=create_connection (non_normalized_db_filename)  
    sql_statement = "SELECT Exams FROM Students;"
    df_exams=pd.read_sql_query(sql_statement, conn)   
    s=set()
    for i,row in df_exams.iterrows():
        for j in row['Exams'].split(','):
            j= j.strip()
            s.add(j)
    df3 = pd.DataFrame({'Exam':list(s)})
    df3 = df3.Exam.str.split(expand =True)
    df3.columns =['Exam', 'Year']
    df3.Year = df3.Year.str.strip(to_strip = "()").astype('int64')
    df3 = df3.sort_values('Exam')
    df3 = df3.reset_index(drop=True)
    return df3









def create_df_students(non_normalized_db_filename):
    """
    Open connection to the non-normalized database and generate a 'df_students' dataframe that contains the student
    first name, last name, and degree. You will need to add another StudentID column to do pandas merge.
    See screenshot below. 
    You can use the original StudentID from the table. 
    hint: use .split on the column name!
    """

    # BEGIN SOLUTION
    conn=create_connection (non_normalized_db_filename)
    sql_statement = "SELECT StudentID, Name, Degree FROM Students;"  
    df = pd.read_sql_query(sql_statement, conn)  
    df4 = df.Name.str.split(',',expand =True)
    df4.columns =['Last_Name', 'First_Name']
    df4.First_Name= df4.First_Name.str.strip()
    df4.Last_Name= df4.Last_Name.str.strip()
    df4['StudentID'] = df['StudentID']
    df4['Degree'] = df['Degree']
    df5 = df4.reindex(columns=['StudentID', 'First_Name', 'Last_Name','Degree'])
    return df5

# #Very important to check the code
# if __name__ == '__main__':

#     df_students_from_func = create_df_students('non_normalized.db')
#     df_students_from_file = pd.read_csv("df_students.csv")
#     print (df_students_from_func)
#     print (df_students_from_file)
#     print(df_students_from_func == df_students_from_file)
#     print(df_students_from_func.equals(df_students_from_file))
#     print(df_students_from_func - df_students_from_file)

#     df_exams_from_func = create_df_exams('non_normalized.db')
#     df_exams_from_file = pd.read_csv("df_exams.csv")
#     print (df_students_from_func)
#     print (df_students_from_file)
#     print(df_students_from_func == df_students_from_file)
#     print(df_students_from_func.equals(df_students_from_file))
#     print(df_students_from_func - df_students_from_file)


            # END SOLUTION

def create_df_studentexamscores(non_normalized_db_filename, df_students):
    """
    Open connection to the non-normalized database and generate a 'df_studentexamscores' dataframe that 
    contains StudentID, exam and score
    See screenshot below. 
    """
    conn=create_connection (non_normalized_db_filename)
    sql_statement = 'SELECT StudentID, Exams, Scores From Students'
    df = pd.read_sql_query(sql_statement, conn)   
    df2 = pd.DataFrame({'StudentID' : pd.Series(dtype='int64'),
                        'Exam' : pd.Series(dtype='str'),
                        'Score': pd.Series(dtype='int64')})
    for i, row in df.iterrows():
        for exam_year, score in zip(row['Exams'].split(','), row['Scores'].split(',')):
            exam = exam_year.strip().split(' ')[0]
            int_score = np.int64(score.strip())
            lastindex = df2.shape[0]
            df2.loc[lastindex, 'StudentID'] = row['StudentID']
            df2.loc[lastindex, 'Exam'] = exam
            df2.loc[lastindex, 'Score'] = np.int64(int_score)
    df2.StudentID = df2.StudentID.astype('int64')
    df2.Score = df2.Score.astype('int64')
    return df2


def ex1(df_exams):
    """
    return df_exams sorted by year
    """
    return df_exams.sort_values(by = 'Year')


def ex2(df_students):
    """
    return a df frame with the degree count
    # NOTE -- rename name the degree column to Count!!!
    """
    # BEGIN SOLUTION
    df = df_students.Degree.value_counts().to_frame()
    df.columns = [['Count']]
    # END SOLUTION
    return df


def ex3(df_studentexamscores, df_exams):
    """
    return a datafram that merges df_studentexamscores and df_exams and finds the average of the exams. Sort
    the average in descending order. See screenshot below of the output. You have to fix up the column/index names.
    Hints:
    # https://stackoverflow.com/a/45451905
    # https://stackoverflow.com/a/11346337
    # round to two decimal places
    """

    df3 = df_exams.set_index(keys='Exam').merge(df_studentexamscores.groupby('Exam').Score.mean().round(2), on='Exam').sort_values(by='Score', ascending=False)
    df3.columns = ['Year', 'average']
    return df3




def ex4(df_studentexamscores, df_students):
    """
    return a datafram that merges df_studentexamscores and df_exams and finds the average of the degrees. Sort
    the average in descending order. See screenshot below of the output. You have to fix up the column/index names.
    Hints:
    # https://stackoverflow.com/a/45451905
    # https://stackoverflow.com/a/11346337
    # round to two decimal places
    """

    df2 = df_students.merge(df_studentexamscores, on='StudentID').groupby('Degree').Score.mean().round(decimals=2).to_frame()
    df4 = df2.rename(columns={'Score': 'Average'})
    return df4


def ex5(df_studentexamscores, df_students):
    """
    merge df_studentexamscores and df_students to produce the output below. The output shows the average of the top 
    10 students in descending order. 
    Hint: https://stackoverflow.com/a/20491748
    round to two decimal places

    """
    df = df_students.set_index(keys='StudentID').merge(df_studentexamscores.groupby('StudentID').Score.mean(), on='StudentID').sort_values(by='Score', ascending=False).head(10).rename(columns={'Score': 'Average'})
    df.Average = df.Average.round(decimals=2)
    return df


# DO NOT MODIFY THIS CELL OR THE SEED

# THIS CELL IMPORTS ALL THE LIBRARIES YOU NEED!!!


np.random.seed(0)
fake = Faker()
Faker.seed(0)


def part2_step1():

    # ---- DO NOT CHANGE
    np.random.seed(0)
    fake = Faker()
    Faker.seed(0)
    # ---- DO NOT CHANGE

    # BEGIN SOLUTION
    fake = Faker()
    df_dict = [{"name":fake.name(), 'suffix': np.random.randint(1000,9999)} for x in range(100) ]
    df_from_faker = pd.DataFrame(df_dict)
    full_name_df = df_from_faker.name.str.split(n=1, expand=True)
    full_name_df.columns   =['first_name', 'last_name']
    full_name_df.loc[:, 'initial_two_char'] = full_name_df.first_name.str.lower().str.slice(start=0, stop=2)
    full_name_df.loc[:, 'username'] = full_name_df.initial_two_char+df_from_faker.suffix.astype('str')
    df = full_name_df[['username', 'first_name', 'last_name']]
    return df
    # END SOLUTION
    


def part2_step2():

    # ---- DO NOT CHANGE
    np.random.seed(0)
    # ---- DO NOT CHANGE

    # BEGIN SOLUTION
    df = np.random.normal([35, 75, 25, 45, 45, 75, 25, 45, 35],[9, 15, 7, 10, 5, 20, 8, 9, 10], (100,9)).round()
    df = np.clip(df, [1,1,1,1,1,1,1,1,1],[50,100,40,60,50,100,50,60,50])
    df_final = pd.DataFrame(data=df, columns=['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5', 'Exam1', 'Exam2', 'Exam3', 'Exam4'])
    return df_final
    # END SOLUTION


def part2_step3(df2_scores):
    # BEGIN SOLUTION
    df = df2_scores.describe().transpose()[['mean', 'std']]
    df['expeted_mean'] = [35, 75, 25, 45, 45, 75, 25, 45, 35]
    df['expeted_std'] = [9, 15, 7, 10, 5, 20, 8, 9, 10]
    df['abs_mean_diff'] = (df['mean'] - df.expeted_mean).abs().round(decimals=2)
    df['abs_std_diff'] = (df['std'] - df.expeted_std).abs().round(decimals=2)
    df['std'] = df['std'].round(decimals=2)
    df2 = df[['mean', 'std', 'expeted_mean', 'expeted_std', 'abs_mean_diff', 'abs_std_diff']]
    # print(df2)
    return df2
    # END SOLUTION


def part2_step4(df2_students, df2_scores, ):
    # BEGIN SOLUTION
    df2_scores = df2_scores.astype('int64')
    expeted_mean_std_max = pd.DataFrame({
    'expeted_mean' :   [35, 75, 25, 45, 45, 75, 25, 45, 35],
    'expeted_std' : [9, 15, 7, 10, 5, 20, 8, 9, 10],
    'score_max_possibe': [50, 100, 40, 60, 50, 100, 50, 60, 50]},
    index = ['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5', 'Exam1', 'Exam2', 'Exam3', 'Exam4'], dtype='int64')
    scaled_df2_scores = df2_scores
    scaled_df2_scores = scaled_df2_scores.astype('int64')
    for exam_name in df2_scores.columns:
        scaled_df2_scores[exam_name] = np.round(100*df2_scores[exam_name]/expeted_mean_std_max.score_max_possibe[exam_name].round(decimals=2))
        if expeted_mean_std_max.score_max_possibe[exam_name] == 40:
            scaled_df2_scores.loc[df2_scores[exam_name] == 23, exam_name] = 57
            # for i in range(100):
            #     if df2_scores[exam_name][i] == 23:
            #         scaled_df2_scores.at[i, exam_name] = 57
    df_part2_step4 = df2_students.merge(scaled_df2_scores, left_index=True, right_index=True)
    return df_part2_step4


def part2_step5():
    # BEGIN SOLUTION
    df = pd.read_csv('part2_step5-input.csv').astype('object')
    hw_ex_list = ['Hw1',       'Hw2',    'Hw3',       'Hw4',    'Hw5',  'Exam1',     'Exam2',     'Exam3',  'Exam4']
    is_ai_issue = df[hw_ex_list] == 'AI_ISSUE'
    df.loc[:, 'AI_Count'] = is_ai_issue.sum(axis=1)
    return df.loc[df.AI_Count > 0, ['username', 'first_name', 'last_name', 'AI_Count']]


# def part2_step6_small():
#     df = pd.read_csv('part2_step5-input.csv')
#     df = df.replace(to_replace={'AI_ISSUE': 0})
#     exam_list = ['Exam1', 'Exam2', 'Exam3', 'Exam4']
#     homework_list = ['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5']
#     df[exam_list+homework_list] = df[exam_list+homework_list].astype('float')
#     exam_mean = df[exam_list].mean(axis=1, skipna=True).round()
#     homework_mean = df[homework_list].mean(axis=1, skipna=True).round()
#     df.loc[:, exam_list] = df[exam_list].fillna(exam_mean)
#     df.loc[:, homework_list]=df[homework_list].fillna(homework_mean)
#     df.loc[:,'Grade'] = df[homework_list].sum(axis=1)*0.05 + df[['Exam1', 'Exam2', 'Exam3']].sum(axis=1)*0.2+df['Exam4']*0.15
#     df.loc[:,'Grade'] = df.Grade.round()
#     df.loc[:,'LetterGrade'] = pd.cut(
#         x=df["Grade"],
#         bins=  [0, 39.9,  49.9,  69.9, 79.9,  101],
#         labels=['F', 'D', 'C', 'B', 'A']).astype('object')
#     mean_std_columns = exam_list+homework_list + ['Grade']
#     df_mean = df[mean_std_columns].mean().round()
#     df_std = df[mean_std_columns].std().round()
#     df.loc['mean', mean_std_columns] = df_mean
#     df.loc['std', mean_std_columns] = df_std
#     return df

def part2_step6():
    df = pd.read_csv('part2_step5-input.csv')
    df = df.replace(to_replace={'AI_ISSUE': 0})
    list_ex = ['Exam1', 'Exam2', 'Exam3', 'Exam4']
    list_hw = ['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5']
    for exam in list_ex:
        df[exam] = df[exam].astype('float')
    for homework in list_hw:
        df[homework] = df[homework].astype('float')
    exam_mean = df[list_ex].mean(axis=1, skipna=True).round()
    homework_mean = df[list_hw].mean(axis=1, skipna=True).round()
    for exam in list_ex:
        df[exam] = df[exam].fillna(exam_mean)
    for homework in list_hw:
        df[homework] = df[homework].fillna(homework_mean)
    homework_grade = df[list_hw].sum(axis=1)*0.05
    exam_20_percent_grade = df[['Exam1', 'Exam2', 'Exam3']].sum(axis=1)*0.2
    df.loc[:,'Grade'] =  homework_grade + exam_20_percent_grade + df['Exam4']*0.15
    df.loc[:,'Grade'] = df.Grade.round()
    df.loc[:,'LetterGrade'] = pd.cut(
        x=df["Grade"],
        bins=  [0, 39.9,  49.9,  69.9, 79.9,  101],
        labels=['F', 'D', 'C', 'B', 'A']).astype('object')
    std_mean = list_ex+list_hw + ['Grade']
    df_mean = df[std_mean].mean().round()
    df_std = df[std_mean].std().round()
    df.loc['mean', std_mean] = df_mean
    df.loc['std', std_mean] = df_std
    return df


# def part2_step6_clever():
#     df_full = pd.read_csv('part2_step5-input.csv')
#     df = df_full.drop(columns = ['username', 'first_name', 'last_name'])
#     df = df.replace(to_replace={'AI_ISSUE': 0})
#     df = df.dtype('float')
#     exam_list = ['Exam1', 'Exam2', 'Exam3', 'Exam4']
#     homework_list = ['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5']
#     exam_mean = df[exam_list].mean(axis=1, skipna=True).round()
#     homework_mean = df[homework_list].mean(axis=1, skipna=True).round()
#     df.loc[:, exam_list] = df[exam_list].fillna(exam_mean)
#     df.loc[:, homework_list]=df[homework_list].fillna(homework_mean)
#     df.loc[:,'Grade'] = df[homework_list].sum(axis=1)*0.05 + df[['Exam1', 'Exam2', 'Exam3']].sum(axis=1)*0.2+df.Exam4*0.15
#     df.loc[:,'Grade'] = df.Grade.round()
#     df.loc[:,'LetterGrade'] = pd.cut(
#         x=df["Grade"],
#         bins=  [0, 39.9,  49.9,  69.9, 79.9,  101],
#         labels=['F', 'D', 'C', 'B', 'A']).astype('object')
#     mean_std_columns = exam_list+homework_list + ['Grade']
#     df_mean = df.mean().round()
#     df_std = df.std().round()
#     df.loc['mean', mean_std_columns] = df_mean
#     df.loc['std', mean_std_columns] = df_std
#     return df
