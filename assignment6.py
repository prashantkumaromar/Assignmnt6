import sqlite3

import numpy as np
import pandas as pd
from faker import Faker


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

    df3 = pd.DataFrame({'Exams':list(s)})
    df3 = df3.Exams.str.split(expand =True)
    df3.columns =['Exams', 'Date']
    df3.Date = df3.Date.str.strip(to_strip = "()").astype('int32')
    df3.sort_values('Exams', inplace = True)
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
    df4.columns =['Second_Name', 'First_Name']
    df4['StudentID'] = df['StudentID']
    df4['Degree'] = df['Degree']
    df5 = df4.reindex(columns=['StudentID', 'First_Name', 'Second_Name','Degree'])
    return df5

# #Very important to check the code
if __name__ == '__main__':

    df_students_from_func = create_df_students('non_normalized.db')
    df_students_from_file = pd.read_csv("df_students.csv")
    print (df_students_from_func)
    print (df_students_from_file)
    print(df_students_from_func == df_students_from_file)
    print(df_students_from_func.equals(df_students_from_file))
    print(df_students_from_func - df_students_from_file)

    df_exams_from_func = create_df_exams('non_normalized.db')
    df_exams_from_file = pd.read_csv("df_exams.csv")
    print (df_students_from_func)
    print (df_students_from_file)
    print(df_students_from_func == df_students_from_file)
    print(df_students_from_func.equals(df_students_from_file))
    print(df_students_from_func - df_students_from_file)


            # END SOLUTION

def create_df_studentexamscores(non_normalized_db_filename, df_students):
    """
    Open connection to the non-normalized database and generate a 'df_studentexamscores' dataframe that 
    contains StudentID, exam and score
    See screenshot below. 
    """

    # BEGIN SOLUTION
    pass
    # END SOLUTION


def ex1(df_exams):
    """
    return df_exams sorted by year
    """
    # BEGIN SOLUTION
    pass
    # END SOLUTION
    return df_exams


def ex2(df_students):
    """
    return a df frame with the degree count
    # NOTE -- rename name the degree column to Count!!!
    """
    # BEGIN SOLUTION
    pass
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

    # BEGIN SOLUTION
    pass
    # END SOLUTION
    return df


def ex4(df_studentexamscores, df_students):
    """
    return a datafram that merges df_studentexamscores and df_exams and finds the average of the degrees. Sort
    the average in descending order. See screenshot below of the output. You have to fix up the column/index names.
    Hints:
    # https://stackoverflow.com/a/45451905
    # https://stackoverflow.com/a/11346337
    # round to two decimal places
    """

    # BEGIN SOLUTION
    pass
    # END SOLUTION
    return df


def ex5(df_studentexamscores, df_students):
    """
    merge df_studentexamscores and df_students to produce the output below. The output shows the average of the top 
    10 students in descending order. 
    Hint: https://stackoverflow.com/a/20491748
    round to two decimal places

    """

    # BEGIN SOLUTION
    pass
    # END SOLUTION


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
    pass
    # END SOLUTION
    


def part2_step2():

    # ---- DO NOT CHANGE
    np.random.seed(0)
    # ---- DO NOT CHANGE

    # BEGIN SOLUTION
    pass
    # END SOLUTION


def part2_step3(df2_scores):
    # BEGIN SOLUTION
    pass
    # END SOLUTION


def part2_step4(df2_students, df2_scores, ):
    # BEGIN SOLUTION
    pass
    # END SOLUTION


def part2_step5():
    # BEGIN SOLUTION
    pass
    # END SOLUTION


def part2_step6():
    # BEGIN SOLUTION
    pass
    # END SOLUTION
