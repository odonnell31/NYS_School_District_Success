# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:49:30 2020

@author: ODsLaptop
"""

# import libraries
import numpy as np
import pandas as pd


### import data

# load dataset of grades 3-8 math and ELA scores at the school level
# the column MEAN_SCALE_SCORE shows the mean score of the school for that grade level
nys_3through8_data = pd.read_excel("data/NYSED/ELA_AND_MATH_RESEARCHER_FILE_2019.xlsx")

# load dataset of Grad Rate and outcomes
nys_high_school_data = pd.read_csv("data/NYSED/GRAD_RATE_AND_OUTCOMES_2019_v2.csv")

# load dataset of NYS Teacher Pay
nys_teacher_pay = pd.read_excel("data/SeeThroughNY/Teacher_Pay_by_District_v2.xlsx")

# mainpulate nys_3through8_data to have only one school per row
"""
nys_3through8_data = nys_3through8_data.pivot_table(index = 'SCHOOL_NAME',
                                                    columns = 'ITEM_DESC',
                                                    values = 'MEAN_SCALE_SCORE',
                                                    aggfunc='first')
"""
nys_3through8_data = pd.read_excel("data/NYSED/ELA_AND_MATH_RESEARCHER_FILE_2019_v4.xlsx")


# merge datasets to create one table

# merge nys_3through8_data and nys_high_school_data by School into nys_students
student_data = pd.merge(nys_3through8_data, nys_high_school_data,
                        left_on = 'SCHOOL_NAME', right_on = 'District',
                        how = 'inner')

# merge nys_teacher pay and nys_students by School District
NYS_Ed_data = pd.merge(student_data, nys_teacher_pay,
                       left_on = 'District', right_on = 'District',
                       how = 'inner')

# export NYS_Ed_data to excel for Dash app with xlsxwriter
writer = pd.ExcelWriter('NYS_Education_2019.xlsx', engine='xlsxwriter')
NYS_Ed_data.to_excel(writer, sheet_name='Sheet1')
writer.save()


