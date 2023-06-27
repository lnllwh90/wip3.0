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
file_headers = ['Advertiser ID','Advertiser Label','Campaign ID','Campaign Label','Ad Group ID','Ad Group Label','Creative ID','Creative Label']

#sort column headers in the file
# sort_headers = ['Advertiser ID', 'Advertiser Label', 'Campaign ID', 'Campaign Label', 'Line Item ID', 'Line Item Label', 'Creative ID', 'Creative Label']
#,'Line Item ID', 'Line Item Label', 'Creative ID', 'Creative Label'

# moat_headers = ['level1','level1label','level2','level2label','level3','level3label','level4','level4label']
#Moat column headers
# moat_headers = ['level2', 'level2label', 'level3', 'level3label', 'level4', 'level4label', 'slicer1', 'slicer1label']

#function to extract the id and label from a csv, output will return a new df with unique values per column

def modify_csv(file_name):
    new_headers = []

    csv_file = pd.read_csv(file_name, index_col=False, header=0,encoding='utf_8' )

    header_names = list(csv_file.columns)

    print(f'\nHere were all the header names I detected in {file_name}:\n\n {header_names}\n')

    new_file_headers = input("Begin entering the column names as you would like for each to appear in the final .csv file. If the file consists of IDs and labels that are needed in the final .csv that I will generate for you, please ensure the ID column headers are paired with its label column header. This may be important in the next step! \n Feel free to copy/paste header names from the above!\n Please separate each column header with by comma: ")

    edit_headers = new_file_headers.replace("'", "")
    edit_headers_list = edit_headers.strip().split(",")

    #Iterate through the list of header names enters, comma separator
    for col in edit_headers_list:

        #Remove leading whitespace
        file_headers_clean = col.lstrip()

        #append the list of headers entered by the user to the  new_headers array
        new_headers.append(file_headers_clean)
        # new_headers_beta.append(file_headers_clean)

    #Confirm column headers
    print('Thanks! Here are the header names I have down: \n',new_headers,'\n')

    confirm_headers = input('Is this correct?:')

    if confirm_headers == 'y' or 'Y':
        preview_column = pd.read_csv(file_name, index_col=False, header=0, encoding='utf_8', usecols=new_headers)
    else:
        print('Not A Valid Input: Exiting...')
        sleep(seconds)
        exit()

    preview = pd.DataFrame(preview_column)
    first_five = preview.head(5)
    print(f'\nBefore we proceed, here\'s a sample of the .csv file I will be generating for you:\n\n')
    sleep(milliseconds)
    print(first_five)

    print('\nI can perform the following task based on the information given so far:')
    print('\n1. Remove duplicate rows from the .csv')
    print('2. Return a count of each occurence')
    print('3. I\'m all set, generate my new .csv file please!\n')

    confirm_next_steps = int(input('Type the number of the action you would like for me to perform next: '))
    #If 1 was entered, pass file_name into the deduplicate_headers() function
    if confirm_next_steps == 1:
        csv_file = pd.read_csv(file_name, index_col=False, header=0, encoding='utf_8', usecols=new_headers)

        dedupe_columns = csv_file[new_headers]

        for i in range(0, len(new_headers), 2):
            id_column = dedupe_columns[new_headers[i]]
            label_column = dedupe_columns[new_headers[i + 1]]
            dedupe_columns = dedupe_columns.drop_duplicates(subset=[new_headers[i], new_headers[i + 1]])
        final_csv = pd.DataFrame(dedupe_columns)

        #prints the new dataframe in a .csv file
        final_csv.to_csv(f'deduped_{file_name}', index=False, columns=new_headers)
        path = os.getcwd()
        t = path

        sleep(seconds)
        #confirm the file was generated and sent to the folder the user is running the script in.
        print(f'\nOkay! I just created a file named deduped_{file_name} and added it to your {t} folder.')
    elif confirm_next_steps == 2:
        csv_file = pd.read_csv(file_name, index_col=False, header=0,encoding='utf_8', usecols=new_headers)

        row_counts = csv_file.groupby(csv_file.columns.tolist()).size().reset_index().rename(columns={0:'impression'})

        row_counts = row_counts.sort_values('impression', ascending=False)

        row_counts.to_csv(f'sorted_{file_name}', index=False)
        path = os.getcwd()
        t = path

        sleep(seconds)
        #confirm the file was generated and sent to the folder the user is running the script in.
        print(f'\nOkay! I just created a file named sorted_{file_name} and added it to your {t} folder.')

    elif confirm_next_steps == 3:
        csv_file = pd.read_csv(file_name, index_col=False, header=0,encoding='utf_8', usecols=new_headers)
                #Adds the csv to a new dataframe
        final_csv = pd.DataFrame(csv_file)
        #get the path the user is running the script in
        path = os.getcwd()
        t = path

        sleep(seconds)

        # print(final_df)

        #prints the new dataframe in a .csv file
        final_csv.to_csv(f'modified_{file_name}', index=False, columns=new_headers)

        print(f'\nOkay! I just created the .csv!\n\nmodified_{file_name} the file is now in your {t} folder.')
    #If 3 was entered pass file_name into the create_csv() function
    else:
        print('Not A Valid Input: Exiting...')
        sleep(seconds)
        exit()

#     remove_headers = input('(y/n): ')

#         # If yes, ask if user would like to remove any duplicates rows from the .csv
#     if remove_headers == 'y' or remove_headers == 'Y':
#         for header in header_names:
#             final_header_list = header.strip()
#             temp_file_headers.append(final_header_list)
#         print(f'Okay! I\'ll use the same header names as the original: \n {temp_file_headers}')

#     # , usecols=file_headers
#     # [sort_headers]
#     # dedupe = decoder.drop_duplicates()
#     # final_csv = pd.DataFrame(dedupe)
#     # print(len(decoder), len(final_csv))
# # # # assigning first two columns to a variable
#     decode =  decoder[['Advertiser ID','Advertiser Label']]
#     # decode['Level1ID'] = decode['Level1ID'].apply(lambda x: x if pd.isnull(x) else str(int(x)))
# # #Creating a new series with params assigned from the decode variable (and its records).

# # #code will remove duplicates from df by running a boolean comparison. *Note if you were to print the series variable you will recieve a boolean (False implies no duplicate values/True implies there's a matching record).

# # #if you want to print the df after running the below run print(decoder[~deduped_series1])

#     deduped_series1 = decode.drop_duplicates()

# # # ignore the index and modify the original data (inplace=True)
#     deduped_series1.reset_index(drop=True, inplace=True)

# # # #Creating a new series with params from the second pairing assigned from the decode variable (and its records).

#     decode2 = decoder[['Campaign ID','Campaign Label']]
# #     decode2['Site ID'] = decode2['Site ID'].apply(lambda x: x if pd.isnull(x) else str(int(x)))
#     deduped_series2 = decode2.drop_duplicates()

# # #     # ignore the index and modify the original data (inplace=True)

#     deduped_series2.reset_index(drop=True, inplace=True)

# # #Creating a new series with params from the third pairing assigned from the decode variable (and its records).

#     decode3 = decoder[['Ad Group ID','Ad Group Label']]
# #     decode3['Placement ID'] = decode3['Placement ID'].apply(lambda x: x if pd.isnull(x) else str(int(x)))
#     deduped_series3 = decode3.drop_duplicates()

# # #     # ignore the index and modify the original data (inplace=True)
#     deduped_series3.reset_index(drop=True, inplace=True)

# # #Creating a new series with params from the third pairing assigned from the decode variable (and its records).

#     decode4 = decoder[['Creative ID','Creative Label']]

#     deduped_series4 = decode4.drop_duplicates()

# #     # ignore the index and modify the original data (inplace=True)
#     deduped_series4.reset_index(drop=True, inplace=True)

# #Creating a new series with params from the third pairing assigned from the decode variable (and its records).

#     # decode5 = decoder[["Site ID","Site Label"]]

#     # deduped_series5 = decode5.drop_duplicates()

# #     # ignore the index and modify the original data (inplace=True)
#     # deduped_series5.reset_index(drop=True, inplace=True)

#     #Creating a new series with params from the third pairing assigned from the decode variable (and its records).

#     # decode6 = decoder[["Placement ID","Placement Label"]]

#     # deduped_series6 = decode6.drop_duplicates()

# #     # ignore the index and modify the original data (inplace=True)
#     # deduped_series6.reset_index(drop=True, inplace=True)


# # #concatenate each of the series along the horizontal axis. Since you've already ignored the index, no need to include ignore_index=True
#     new_series = pd.concat([deduped_series1, deduped_series2, deduped_series3, deduped_series4], axis=1)

# # # # add the new series as a dataframe. Assign to a variable name sample_columns
#     deduped_columns = pd.DataFrame(new_series)

#     #below can be used to specify the length of the output, help with debug/troubleshooting.
#     # lines1 = len(sample_columns)

#     #statement to return on success
#     # print(f'\nFile is now file parser script complete!')

#     #prints all de-duped rows Revised csv file

#     #For now file will output without header column, this is because the index was ignored and is now a range....

#     # to add column headers to the csv, add the header flag. Can either assign column names to the header variable or assign a variable.
#     # preview = decoder.head(5)
#     # print(preview)
#     # preview_csv = preview.to_csv(f'sample_{encoded_file}', index=False)
#     final_csv = pd.DataFrame(deduped_columns)
#     final_csv.to_csv(f'Deduped_{encoded_file}', index=False, header=file_headers)
#     #Prints all the domains removed from the file to a separate CSV for review
#     path = os.getcwd()
#     t = path

#     sleep (seconds)
#     print(f'Okay! your new .csv file "Deduped_{encoded_file}" is now in your {t} folder!')
    # excluded_domains.to_csv(f'Removed_Domains.csv', index=False, header=None)

    # print(f'\nThe Deduped and decoded urls were sent to "Revised_{encoded_file}".\n \nNumber of rows in "Revised_{encoded_file}" : {lines2}\n \nA list of the domains removed from the "{encoded_file}" file were output in the "Removed_Domains.csv" file.\n \nNumber of rows in "Removed_Domains.csv" : {lines3}\n')

#Number of arguments accepted via the CLI
arg1 = sys.argv[1]

modify_csv(arg1)