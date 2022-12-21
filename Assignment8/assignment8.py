import datetime
import math
import operator 

def ex1():
    """
    Reproduce ex1.tsv from 'AdmissionsCorePopulatedTable.txt'
    https://mkzia.github.io/eas503-notes/sql/sql_6_conditionals.html#conditionals
    Separate the columns by a tab
    """

    # BEGIN SOLUTION
    age_range_count = {}
    output = []
    with open('AdmissionsCorePopulatedTable.txt', 'r') as f:
        # Read the contents of the file
        for line in f.readlines()[1:]:
            p = line.split('\t')
            AdmissionStartDate = datetime.datetime.strptime(p[2].split()[0], "%Y-%m-%d")
            month = AdmissionStartDate.strftime("%B")
            age_range_count[month] = age_range_count.get(month, 0) + 1
        age_range_count_list = sorted(age_range_count.items(), key=lambda item: (100-int(item[1]), item[0]))
        # print(age_range_count_list)
        output.append('AdmissionMonth' + '\t' + 'AdmissionCount' + '\n')

        for age_range_count in age_range_count_list:
            output.append(age_range_count[0]+"\t" + str(age_range_count[1]) + '\n')
        # print(output)
        ex1 = open('ex1.tsv', 'w')
        ex1.writelines(output)
        ex1.close()

    # END SOLUTION


def ex2():
    """
    Repeat ex1 but add the Quarter column 
    This is the last SQL query on https://mkzia.github.io/eas503-notes/sql/sql_6_conditionals.html#conditionals
    Hint: https://stackoverflow.com/questions/60624571/sort-list-of-month-name-strings-in-ascending-order
    """

    # BEGIN SOLUTION
    # BEGIN SOLUTION
    age_range_count = {}
    output = []
    with open('AdmissionsCorePopulatedTable.txt', 'r') as f:
        # Read the contents of the file
        for line in f.readlines()[1:]:
            p = line.split('\t')
            AdmissionStartDate = datetime.datetime.strptime(p[2].split()[0], "%Y-%m-%d")
            month = AdmissionStartDate.strftime("%B")
            month_number = AdmissionStartDate.month
            quarter = (month_number-1)//3+1
            age_range_count[(month_number, month, quarter)] = age_range_count.get((month_number, month,quarter), 0) + 1
        age_range_count_list = sorted(age_range_count.items(), key=lambda item: (100-int(item[1]), item[0]))
        age_range_count_list = sorted(age_range_count.items())
        # print(age_range_count_list)
        output.append('Quarter' + '\t' + 'AdmissionMonth' + '\t' + 'AdmissionCount' + '\n')

        for age_range_count in age_range_count_list:
            output.append('Q' + str(age_range_count[0][2])+"\t" + age_range_count[0][1] + "\t" + str(age_range_count[1]) + '\n')
        ex2 = open('ex2.tsv', 'w')
        ex2.writelines(output)
        ex2.close() 

    # END SOLUTION


def ex3():
    """
    Reproduce 
    SELECT
        LabsCorePopulatedTable.PatientID,
        PatientCorePopulatedTable.PatientGender,
        LabName,
        LabValue,
        LabUnits,
        CASE
            WHEN PatientCorePopulatedTable.PatientGender = 'Male'
            AND LabValue BETWEEN 0.7
            AND 1.3 THEN 'Normal'
            WHEN PatientCorePopulatedTable.PatientGender = 'Female'
            AND LabValue BETWEEN 0.6
            AND 1.1 THEN 'Normal'
            ELSE 'Out of Range'
        END Interpretation
    FROM
        LabsCorePopulatedTable
        JOIN PatientCorePopulatedTable ON PatientCorePopulatedTable.PatientID = LabsCorePopulatedTable.PatientID
    WHERE
        LabName = 'METABOLIC: CREATININE'
    ORDER BY
        - LabValue

    using PatientCorePopulatedTable.txt and LabsCorePopulatedTable

    **** ADD  LabDateTime
    **** SORT BY Patient ID and then LabDateTime in ascending order 
    """
    PatientCorePopulatedTable = open('PatientCorePopulatedTable.txt')
    LabsCorePopulatedTable = open('LabsCorePopulatedTable.txt')
 
 
    patient_to_gender = dict()
    for patient_core in PatientCorePopulatedTable.readlines()[1:]:
       p = patient_core.split('\t')
       PatientID = p[0]
       PatientGender = p[1]
       patient_to_gender[PatientID] = PatientGender
    #    print(patient_to_gender)
    g = []
    for  labs_core in LabsCorePopulatedTable.readlines()[1:]:
        l = labs_core.split('\t')
        if l[2].strip() == 'METABOLIC: CREATININE':
            LabName = l[2].strip()
            LabValue = float(l[3])
            LabUnits = l[4].strip()
            LabDateTime = l[5].strip()
            PatientID = l[0]
            PatientGender = patient_to_gender[PatientID]
            if PatientGender == 'Male' and LabValue >= 0.7 and LabValue < 1.3:
                Interpretation = 'Normal'
            elif PatientGender == 'Female' and LabValue >= 0.6 and LabValue < 1.1:
                Interpretation = 'Normal'
            else:
                Interpretation = 'Out of Range'
            g.append((PatientID, LabDateTime,  PatientGender,LabName, LabValue, LabUnits, Interpretation))

    sorted(g, key= operator.itemgetter(0, 1))
    print(g[0])
    output = []
    output.append('PatientID' + '\t' + 	'PatientGender'	 + '\t' + 'LabName'	 + '\t' + 'LabValue'	 + '\t' + 'LabUnits'	 + '\t' + 'LabDateTime'	 + '\t' + 'Interpretation'  + '\n')
    ex3 = open('ex3.tsv', 'w')
    for f in g:
        output.append(f[0]+ "\t" + f[2] + "\t" +str(f[3]) +"\t" + str(f[4]) + "\t" + str(f[5]) + "\t" + str(f[1]) + "\t" +f[6] + '\n')
    ex3.writelines(output)
    ex3.close()
    PatientCorePopulatedTable.close()
    LabsCorePopulatedTable.close()

    # lab_file = open('LabsCorePopulatedTable.txt', 'r')
    # patient_file = 'PatientCorePopulatedTable.txt'
    # gender = {}; data = []
    # header1 = None
    # with open (patient_file) as file:
    #     if header1 == None:
    #         header1 = line
    #     else:
    #         for line in file: 
    #             pID = line.split("\t")[0]
    #             genderID = line.split("\t")[1]
    #             gender[pID] = genderID
    # header2 = None
    # with open (lab_file) as fp:
    #     if header2 == None:
    #         header2 = line
    #     else:
    #         for line in fp: 
    #             test_name = line.split("\t")[2].strip()
    #             patientID = line.split("\t")[0].strip()
    #             labvalue = line.split("\t")[3].strip()
    #             labunits = line.split("\t")[4].strip()
    #             timestamp = line.split("\t")[5].strip()
    #             if test_name == 'METABOLIC: CREATININE':
    #                 if gender[patientID] == 'Male' and 0.7<=float(labvalue)<=1.3:
    #                     data.append((patientID, gender[patientID], test_name,labvalue,labunits,timestamp, 'Normal'))
    #                 elif gender[patientID] == 'Female' and 0.6<=float(labvalue)<=1.1:
    #                     data.append((patientID, gender[patientID], test_name,labvalue,labunits,timestamp, 'Normal'))
    #                 else:
    #                     data.append((patientID, gender[patientID], test_name,labvalue,labunits,timestamp, 'Out of Range'))
    #         data_sorted = sorted(data, key= operator.itemgetter(0, 5))
    # with open("ex3.tsv", "w") as record_file:
    #     record_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % ('PatientID','PatientGender','LabName','LabValue','LabUnits','LabDateTime','Interpretation'))
    #     for index, record in enumerate(data_sorted):
    #         if index!=len(data_sorted) - 1:
    #             record_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (record[0],record[1],record[2],record[3],record[4],record[5],record[6]))
    #         else:
    #             record_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s" % (record[0],record[1],record[2],record[3],record[4],record[5],record[6]))
    # END SOLUTION

 

def ex4():
    """
    Reproduce this
    WITH AGE AS (
        SELECT 
            PATIENTID,
            ROUND((JULIANDAY('NOW') - JULIANDAY(PATIENTDATEOFBIRTH))/365.25) AGE
        FROM 
            PATIENTCOREPOPULATEDTABLE
    )
    SELECT 
        CASE 
            WHEN AGE < 18 THEN 'YOUTH'
            WHEN AGE BETWEEN 18 AND 35 THEN 'YOUNG ADULT'
            WHEN AGE BETWEEN 36 AND 55 THEN 'ADULT'
            WHEN AGE >= 56 THEN 'SENIOR'
        END AGE_RANGE,
        COUNT(*) AGE_RANGE_COUNT
    FROM 
        AGE
    GROUP BY AGE_RANGE
    ORDER BY AGE

    ****** VERY IMPORTANT: Use the Date: 2022-12-11 as today's date!!!! VERY IMPORTANT otherwise your result will change everyday!
    ****** VERY IMPORTANT divide the number of days by 365.25; to get age do math.floor(delta.days/365.25), where delta days is now-dob

    """
    # BEGIN SOLUTION
    PatientCorePopulatedTable = open('PatientCorePopulatedTable.txt')
    output = []
    age_range_count = {}
    today_date = datetime.datetime.strptime('2022-12-11', "%Y-%m-%d").date()
    for patient_core in PatientCorePopulatedTable.readlines()[1:]:
        p = patient_core.split('\t')
        PATIENTID = p[0]
        # print(p[0])
        PatientDateOfBirth = datetime.datetime.strptime(p[2].split()[0], "%Y-%m-%d").date()
        Age = math.floor((today_date -PatientDateOfBirth).days/365.25)
        if Age < 18:
            AGE_RANGE = 'YOUTH'
        elif Age < 36:
            AGE_RANGE = 'YOUNG ADULT'
        elif Age < 56:
            AGE_RANGE = 'ADULT'
        else:
            AGE_RANGE = 'SENIOR'
        age_range_count[AGE_RANGE] = age_range_count.get(AGE_RANGE, 0) + 1
    age_range_count_list = list(age_range_count.items())

    ex4 = open('ex4.tsv', 'w')
    age_priority = {'YOUTH': 1, 'YOUNG ADULT' : 2, 'ADULT' : 3, 'SENIOR' : 4}
    key=lambda age: age_priority[age[0]]
    age_range_count_list.sort(key=key)
    output.append('AGE_RANGE' + '\t' + 'AGE_RANGE_COUNT' + '\n')
    for age_range_count in age_range_count_list:
        output.append(age_range_count[0]+"\t" + str(age_range_count[1]) + '\n')
    ex4.writelines(output)
    ex4.close()
    PatientCorePopulatedTable.close()
