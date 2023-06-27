import sys
import csv
import urllib
from urllib.parse import urlparse, unquote
import os
import string
from numpy import sort
import pandas as pd
from time import sleep

milli = 600
milliseconds = .001 * milli
seconds = 1
#list of column headers in the file
# file_headers = ['Site ID(Placement)', 'Site name(Placement)', 'Placement ID(Placement)', 'Placement name(Placement)', 'Creative ID(Creative)', 'Creative name(Creative)']
file_headers = ['Advertiser ID','Advertiser Label','Campaign ID','Campaign Label','Line Item ID','Line Item Label','Creative ID','Creative Label']

# dtypes = {
#     'Site ID(Placement)': 'Int64',
#     'Site name(Placement)': str,
#     'Placement ID(Placement)': 'Int64',
#     'Placement name(Placement)': str,
#     'Creative ID(Creative)': 'Int64',
#     'Creative name(Creative)': str
# }

dtypes = {
    'Campaign ID':'Int64',
    'Campaign Label':'Int64',
    'Advertiser ID':'Int64',
    'Advertiser Label':'Int64',
    'Line Item ID':'Int64',
    'Line Item Label':'Int64',
    'Creative ID':'Int64',
    'Creative Label':'Int64'
}

#sort column headers in the file
# sort_headers = ['Advertiser ID', 'Advertiser Label', 'Campaign ID', 'Campaign Label', 'Line Item ID', 'Line Item Label', 'Creative ID', 'Creative Label']
#,'Line Item ID', 'Line Item Label', 'Creative ID', 'Creative Label'

# moat_headers = ['level2','level2label','level3','level3label','level4','level4label']
#Moat column headers
# moat_headers = ['level2', 'level2label', 'level3', 'level3label', 'level4', 'level4label', 'slicer1', 'slicer1label']

#function to extract the id and label from a csv, output will return a new df with unique values per column

def format_urls(file_name):
    # decoder = pd.read_csv(file_name, index_col=False, encoding='utf_8', usecols=file_headers)
    # temp_file_headers =[]
    # placeholder = ''
    csv_file = pd.read_csv(file_name, index_col=False, encoding='utf_8',dtype=dtypes, usecols=file_headers )

    # header_names = list(csv_file.columns)
    # , usecols=file_headers
    # [sort_headers]
    # dedupe = decoder.drop_duplicates()
    # final_csv = pd.DataFrame(dedupe)
    # print(len(decoder), len(final_csv))
# # # assigning first two columns to a variable
    decode =  csv_file[['Advertiser ID','Advertiser Label']]
    # decode['Level1ID'] = decode['Level1ID'].apply(lambda x: x if pd.isnull(x) else str(int(x)))
# #Creating a new series with params assigned from the decode variable (and its records).

# #code will remove duplicates from df by running a boolean comparison. *Note if you were to print the series variable you will recieve a boolean (False implies no duplicate values/True implies there's a matching record).

# #if you want to print the df after running the below run print(decoder[~deduped_series1])

    deduped_series1 = decode.drop_duplicates()

# # ignore the index and modify the original data (inplace=True)
    deduped_series1.reset_index(drop=True, inplace=True)

# # #Creating a new series with params from the second pairing assigned from the decode variable (and its records).

    decode2 = csv_file[['Campaign ID','Campaign Label']]
#     decode2['Site ID'] = decode2['Site ID'].apply(lambda x: x if pd.isnull(x) else str(int(x)))
    deduped_series2 = decode2.drop_duplicates()

# #     # ignore the index and modify the original data (inplace=True)

    deduped_series2.reset_index(drop=True, inplace=True)

# #Creating a new series with params from the third pairing assigned from the decode variable (and its records).

    decode3 = csv_file[['Line Item ID','Line Item Label']]
#     decode3['Placement ID'] = decode3['Placement ID'].apply(lambda x: x if pd.isnull(x) else str(int(x)))
    deduped_series3 = decode3.drop_duplicates()

# #     # ignore the index and modify the original data (inplace=True)
    deduped_series3.reset_index(drop=True, inplace=True)

# #Creating a new series with params from the third pairing assigned from the decode variable (and its records).

    decode4 = csv_file[['Creative ID','Creative Label']]

    deduped_series4 = decode4.drop_duplicates()

#     # ignore the index and modify the original data (inplace=True)
    # deduped_series4.reset_index(drop=True, inplace=True)

#Creating a new series with params from the third pairing assigned from the decode variable (and its records).

    # decode5 = decoder[["Site ID","Site Label"]]

    # deduped_series5 = decode5.drop_duplicates()

#     # ignore the index and modify the original data (inplace=True)
    # deduped_series5.reset_index(drop=True, inplace=True)

    #Creating a new series with params from the third pairing assigned from the decode variable (and its records).

    # decode6 = decoder[["Placement ID","Placement Label"]]

    # deduped_series6 = decode6.drop_duplicates()

#     # ignore the index and modify the original data (inplace=True)
    # deduped_series6.reset_index(drop=True, inplace=True)


# #concatenate each of the series along the horizontal axis. Since you've already ignored the index, no need to include ignore_index=True
    new_series = pd.concat([deduped_series1, deduped_series2, deduped_series3, deduped_series4], axis=1)

# # # add the new series as a dataframe. Assign to a variable name sample_columns
    deduped_columns = pd.DataFrame(new_series)

    #below can be used to specify the length of the output, help with debug/troubleshooting.
    # lines1 = len(sample_columns)

    #statement to return on success
    # print(f'\nFile is now file parser script complete!')

    #prints all de-duped rows Revised csv file

    #For now file will output without header column, this is because the index was ignored and is now a range....

    # to add column headers to the csv, add the header flag. Can either assign column names to the header variable or assign a variable.
    # preview = decoder.head(5)
    # print(preview)
    # preview_csv = preview.to_csv(f'sample_{encoded_file}', index=False)
    final_csv = pd.DataFrame(deduped_columns)
    final_csv.to_csv(f'Deduped_{file_name}', index=False, encoding='utf_8',header=file_headers)
    #Prints all the domains removed from the file to a separate CSV for review
    path = os.getcwd()
    t = path

    sleep (seconds)
    print(f'Okay! your new .csv file "Deduped_{file_name}" is now in your {t} folder!')
    # excluded_domains.to_csv(f'Removed_Domains.csv', index=False, header=None)

    # print(f'\nThe Deduped and decoded urls were sent to "Revised_{encoded_file}".\n \nNumber of rows in "Revised_{encoded_file}" : {lines2}\n \nA list of the domains removed from the "{encoded_file}" file were output in the "Removed_Domains.csv" file.\n \nNumber of rows in "Removed_Domains.csv" : {lines3}\n')

#Number of arguments accepted via the CLI
arg1 = sys.argv[1]

format_urls(arg1)