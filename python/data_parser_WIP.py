import sys
import csv
import urllib
from urllib.parse import urlparse, unquote
import os
import string
import pandas as pd
from time import sleep


milli = 600
milliseconds1 = .001 * milli
seconds = 1



# file_headers = ['Insertion Order', 'Insertion Order ID', 'Line Item', 'Line Item ID', 'Creative', 'Creative ID', 'Exchange', 'Exchange ID']
#Array List, Header names to use from the file
file_headers =[]
# sort_headers = ['Insertion Order ID', 'Insertion Order', 'Line Item ID', 'Line Item', 'Creative ID', 'Creative', 'Exchange ID', 'Exchange']

#Array List, sort column order
sort_headers = []
subset = []

def welcome():
    ''' Takes the user input, on success script continues, else program exits.'''

    # Intro
    # print('\n')
    # sleep(milliseconds1)
    # print('With your help, I can perform the following task for you!\n')
    # print('\n**********************************************************************************************************************\n')
    # print('Enter \'edit_csv\' to remove columns or duplicate rows from a .csv')
    # print('Enter \'decoder\' to decode urls in a .csv file')
    # print('\n********************************************************************************************************************** \n')

    # Asks user to enter the reason for using the script
    purpose = input(f'\nWhat can I do for you today?: ')
    # (modify_csv, decode_urls, convert_to_csv)
    # If condition, is edit_csv move to confirm_purpose(). 2 (Pending)
    if purpose == 'modify_csv' or purpose == 'MODIFY_CSV':
        #Prints
        print(f'\nModify a .csv file')
        sleep(milliseconds1)
        #pass the purpose to the confirm_purpose function
        confirm_purpose(purpose)
    else:
        print('Not A Valid Input: Exiting...')
        sleep(seconds)
        exit()

def confirm_purpose(purpose):
    ''' confirms purpose, on success script continues '''

    # Ask user if they would like to continue
    confirmation = input("\nIs this correct? (y/n): ")
    # If yes and purpose is equal to 'edit_csv'........
    if confirmation == 'y' or confirmation == 'Y':
        if purpose == 'modify_csv' or purpose == 'MODIFY_CSV':
            sleep(milliseconds1)
            print('\nOkay got it! Let\'s get started!')
            sleep(seconds)

            specify_file()

def specify_file():
    ''' User asked to add the file name along with its extension. Code blocks only supports .csv files for now.'''

    # print('MOAT_-_Placement_Report_sample.csv')
    print(f'Before we begin I will need to make a reference to the file.')
    sleep(milliseconds1)
    # Asks the user to enter the name of the .csv file
    file_name = input(f'Enter the file name. Please be sure to include the files\' extension (e.g. file_name.csv): ')
    sleep(milliseconds1)

    #add check to confirm the name ends in .csv
    # Confirm file name
    print('File name entered: ', file_name)
    sleep(milliseconds1)
    conf_file = input('Is this correct(y/n)?: ')
    # If yes pass file into the the return_headers function
    if conf_file == 'y' or conf_file == 'Y':
        header_index = input('Does your csv have column headers?: ')
        if header_index == 'y' or header_index == 'Y':
            return_headers(file_name)
        elif header_index == 'n' or header_index == 'N':
            first_five_index(file_name)
        else:
            print('Not A Valid Input: Exiting...')
            sleep(seconds)
            exit()
    # elif conf_file == 'n' or conf_file == 'N':
    #     pass

def return_index(file_name):
    confirm_column_index = input('Okay, before we begin will you need all of the columns in the csv file (y/n)?: ')
    #Read csv file
    if confirm_column_index == 'y' or confirm_column_index == 'Y':
        confirm_column_header = input('Would you like to assign column headers to the file (y/n)?: ')
        # confirm_columns_sort = input('Okay, will you need to sort any of the columns in the csv (y/n)?: ')
        # if confirm_columns_sort == 'y' or confirm_columns_sort == 'Y':
        #     pass

        # elif confirm_columns_sort == 'n' or confirm_columns_sort == 'N':
        #     first_five_index(file_name)
                # confirm_columns_sort = input('Okay, will you need to sort any of the columns in the csv (y/n)?: ')
        if confirm_column_header == 'y' or confirm_column_header == 'Y':
            create_columns(file_name)

        elif confirm_column_header == 'n' or confirm_column_header == 'N':
            first_five_index(file_name)
        else:
            print('Not A Valid Input: Exiting...')
            sleep(seconds)
            exit()
    if confirm_column_index == 'n' or confirm_column_index == 'N':
        pass

def first_five_index(file_name):
    ''' Function to allow the user to preview the .csv file without column headers.'''

    preview_index = pd.read_csv(file_name, index_col=False, header=none, encoding='latin_1')

    #assign the csv to a new dataframe
    preview = pd.DataFrame(preview_index)
    #print the first 5 rows of the .csv file
    first_five = preview.head(5)
    print(f'\nOkay, before we proceed, here\'s a sample of the .csv file I will be generating for you:\n\n')
    sleep(milliseconds1)
    print(first_five)
    sleep(seconds)
    print('\nI can perform the perform the following task based on the information given so far:')
    print('\n1. Remove duplicate rows from a .csv')
    print('2. Decode urls in the .csv file')
    print('3. Write the first five columns of the file to a new .csv')
    print('4. I\'m all set, generate my new .csv file please!\n')

    confirm_next_steps = int(input('Type the number of the action you would like for me to perform next: '))
    #If 1 was entered, pass file_name into the deduplicate_headers() function
    if confirm_next_steps == 1:
        deduplicate_file_by_index(file_name)
    elif confirm_next_steps == 2:
        exit()
        # decoder(file_name)

    elif confirm_next_steps == 3:
        create_csv(file_name)
    #If 3 was entered pass file_name into the create_csv() function
    elif confirm_next_steps == 4:
        create_csv(file_name)
    else:
        print('Not A Valid Input: Exiting...')
        sleep(seconds)
        exit()

def deduplicate_file_by_index(file_name):
    csv_file = pd.read_csv(file_name, index_col=False, header=none, encoding='latin_1')
    deduplicate_column = csv_file.drop_duplicates()
    final_csv = pd.DataFrame(deduplicate_column)

    #prints the new dataframe in a .csv file
    final_csv.to_csv(f'modified_{file_name}', index=False)
    path = os.getcwd()
    t = path

    sleep(seconds)
    #confirm the file was generated and sent to the folder the user is running the script in.
    print(f'\nOkay! I just created the .csv!\n\nmodified{file_name} is now in your {t} folder.')

def return_headers(file_name):
    temp_file_headers =[]
    placeholder = ''
    csv_file = pd.read_csv(file_name, index_col=False, header=0,encoding='latin_1' )

    header_names = list(csv_file.columns)
    sleep(seconds)
    print('Thank you! One sec...\n')
    sleep(seconds)
    print(f'\nHere were all the header names I detected in {file_name}:\n\n {header_names}\n')
    sleep(milliseconds1)

    #Confirm if the header columns extracted from the .csv file are correct
    confirm_headers = input('Is this correct (y/n)?: ')

    # Confirm if the program should remove any columns from the .csv file
    if confirm_headers == 'y' or confirm_headers == 'Y':

        print(f'\nWould you like for all of the columns in {file_name} to be in the .csv file that I create for you?')

        remove_headers = input('(y/n): ')

        # If yes, ask if user would like to remove any duplicates rows from the .csv
        if remove_headers == 'y' or remove_headers == 'Y':
            for header in header_names:
                final_header_list = header.strip()
                temp_file_headers.append(final_header_list)
            print(f'Okay! I\'ll use the same header names as the original: \n {temp_file_headers}')
            sleep(milliseconds1)
            confirm_ColumnHeaders(file_name, temp_file_headers, placeholder)

            # print('Are the columns already sorted?')
            # conf_csv2 = input('(y/n): ')
            # if conf_csv2 == 'y' or conf_csv == 'y':
            #     pass
            # elif conf_csv2 == 'n' or conf_csv == 'n':

        #If user enters 'n' pass the .csv file and header_names to column_headers() function
        elif remove_headers == 'n' or remove_headers == 'N':
            column_headers(file_name, header_names)
        else:
            print('Not A Valid Input: Exiting...')
            sleep(seconds)
            exit()
    else:
        print('Not A Valid Input: Exiting...')
        sleep(seconds)
        exit()
            # sort_cols(file_name)

# sort_headers = ['Insertion Order ID', 'Insertion Order', 'Line Item ID', 'Line Item', 'Creative ID', 'Creative', 'Exchange ID', 'Exchange']

def sort_columns(file_name, file_headers):
    ''' Sort column headers'''

    #array for the column order, will be used as a placeholder before passing to the global sort_headers array

    # MOAT_-_Placement_Report_sample.csv
    temp_sorted_headers = []
    confirm_sort = input('Okay, now that I have the column names, did the original .csv file have column headers sorted in the order you would like (y/n)?: ')
    #confirm_sort(file_name, )
    if confirm_sort == 'n' or confirm_sort == 'N':
        print(f'\nOkay thanks!\n')
        print(f'\n{file_headers}\n\n')
        begin_sort = input('Is the order above the order you would like the columns to appear in the final .csv file (y/n)?: ')

        if begin_sort == 'y' or begin_sort == 'Y':
            #iterate through the list of strings
            for col in file_headers:
                final_sort = col.strip()
                sort_headers.append(final_sort)
                #Route to print the first five rows of the file
            first_five_headers(file_name)

        elif begin_sort == 'n' or begin_sort =='N':
            cols = input('Enter column names in the order you would like each to appear in the final .csv that I create:')
            #Remove special characters
            confirm_sort = cols.replace("'", "")
            #Remove whitespace, converts to list
            sort_list = confirm_sort.strip().split(",")

            #iterate through the list of header names
            for col in sort_list:

                #Remove leading whitespace
                sort_header_clean = col.lstrip()

                #append list to temp_sorted_headers array
                temp_sorted_headers.append(sort_header_clean)
            confirm_sort_headers(file_name, temp_sorted_headers)

    elif confirm_sort == 'y' or confirm_sort == 'Y':
        # for col in file_headers:
        #     final_sort = col.strip()
        #     sort_headers.append(final_sort)
        # print(sort_headers)
        first_five_headers(file_name)

        # sort_headers = file_headers
        # print(sort_headers)
    # confirm_deduplication(file_name)
        #     col_sorted_list = list(col)
        #     sorted = col_sorted_list(", ")
    #Pass file_name and temp_sorted_headers to confirm_sort_headers() function

# sort_headers = ['Insertion Order ID', 'Insertion Order', 'Line Item ID', 'Line Item', 'Creative ID', 'Creative', 'Exchange ID', 'Exchange']
def confirm_sort_headers(file_name, temp_sorted_headers):
    ''' confirm column order in the final .csv file '''
    # MOAT_-_Placement_Report_sample.csv
    sleep(milliseconds1)

    #Prints the column order the new .csv file will follow
    print(f'\n\nThanks! Here\'s the order that I will follow when creating the .csv file:\n\n {temp_sorted_headers} \n\n')
    sleep(milliseconds1)
    # Asks user yes or no
    confirm_sort = input('Are the above column headers in the order in which you would like the columns to appear in the final file? (y/n): ')

    #if user enters y append local temp_sorted_header array to global sort_headers array
    if confirm_sort == 'y' or confirm_sort == 'Y':
        for item in temp_sorted_headers:
            #Remove white spaces
            final_list = item.strip()
            #append the
            sort_headers.append(final_list)

        print('\nGreat! Now that I have the columns and order that I should reference, what would you like to do next?\n')

        #passes file_name to first_five_headers() function
        first_five_headers(file_name)
    else:
        print('Sorry it seems that something went wrong! Please rerun the script.')
        sleep(milliseconds1)
        print('Exiting...')
        sleep(seconds)
        exit()

def first_five_headers(file_name):
    ''' Function to allow users to preview new the .csv file. Preview will follow the order specified in the file_headers and sort_headers global objects.'''
    if not sort_headers:
        preview_headers = pd.read_csv(file_name, index_col=False, header=0,encoding='latin_1', usecols=file_headers)
    #read csv
    else:
        preview_headers = pd.read_csv(file_name, index_col=False, header=0,encoding='latin_1', usecols=file_headers) [sort_headers]

    #assign the csv to a new dataframe
    preview = pd.DataFrame(preview_headers)
    #print the first 5 rows of the .csv file
    first_five = preview.head(5)
    print(f'\nBefore we proceed, here\'s a sample of the .csv file I will be generating for you:\n\n')
    sleep(milliseconds1)
    print(first_five)
    sleep(seconds)
    print('\nI can perform the perform the following task based on the information given so far:')
    print('\n1. Remove duplicate rows from a .csv')
    print('2. Decode urls in the .csv file')
    print('3. I\'m all set, generate my new .csv file please!')
    print('4. I\'m all set, generate my new .csv file please!\n')

    confirm_next_steps = int(input('Type the number of the action you would like for me to perform next: '))
    #If 1 was entered, pass file_name into the deduplicate_headers() function
    if confirm_next_steps == 1:
        deduplicate_file_with_headers(file_name)
    elif confirm_next_steps == 2:
        exit()
        # decoder(file_name)
    #If 3 was entered pass file_name into the create_csv() function
    elif confirm_next_steps == 3:
        create_csv(file_name)

    elif confirm_next_steps == 4:
        preview_csv_with_headers(file_name)

    else:
        print('Not A Valid Input: Exiting...')
        sleep(seconds)
        exit()

# sort_headers = ['Insertion Order ID', 'Insertion Order', 'Line Item ID', 'Line Item', 'Creative ID', 'Creative', 'Exchange ID', 'Exchange']

def create_csv_with_index(file_name):
    if not sort_index:
        pass

def preview_csv_with_headers(file_name):
    ''' Generate the new .csv file '''
    #Takes the original .csv file entered

    if not sort_headers:
        csv_file = pd.read_csv(file_name, index_col=False, header=0,encoding='latin_1', usecols=file_headers)
                #Adds the csv to a new dataframe
        final_df = pd.DataFrame(csv_file)
        #get the path the user is running the script in
        path = os.getcwd()
        t = path

        sleep(seconds)

        # print(final_df)
            #assign the csv to a new dataframe
        preview = pd.DataFrame(final_df)
        #print the first 5 rows of the .csv file
        first_five = preview.head(5)
        print(first_five)
        #prints the new dataframe in a .csv file
        # preview.to_csv(f'sample_{file_name}', index=False)

    elif sort_headers:
        # len(sort_headers) == len(file_headers)
        filtered_csv_file = pd.read_csv(file_name, index_col=False, header=0,encoding='latin_1', usecols=file_headers) [sort_headers]
        #Adds the csv to a new dataframe
        sorted_final_df = pd.DataFrame(filtered_csv_file)
        #get the path the user is running the script in
        path = os.getcwd()
        t = path

        sleep(seconds)

        previewSorted = pd.DataFrame(sorted_final_df)
        #print the first 5 rows of the .csv file
        first_five_sorted = previewSorted.head(5)
        #prints the new dataframe in a .csv file
        print(first_five_sorted)
        # first_five_sorted.to_csv(f'preview-sort_{file_name}', index=False, columns=sort_headers)


    #confirm the file was generated and sent to the folder the user is running the script in.
    # print(f'\nOkay! I just created the .csv!\n\nIt is now in the {t} folder.')

def create_csv_with_headers(file_name):
    ''' Generate the new .csv file '''
    #Takes the original .csv file entered

    if not sort_headers:
        csv_file = pd.read_csv(file_name, index_col=False, header=0,encoding='latin_1', usecols=file_headers)
                #Adds the csv to a new dataframe
        final_df = pd.DataFrame(csv_file)
        #get the path the user is running the script in
        path = os.getcwd()
        t = path

        sleep(seconds)

        # print(final_df)

        #prints the new dataframe in a .csv file
        final_df.to_csv(f'modified_{file_name}', index=False)

    elif sort_headers:
        # len(sort_headers) == len(file_headers)
        filtered_csv_file = pd.read_csv(file_name, index_col=False, header=0,encoding='latin_1', usecols=file_headers) [sort_headers]
        #Adds the csv to a new dataframe
        sorted_final_df = pd.DataFrame(filtered_csv_file)
        #get the path the user is running the script in
        path = os.getcwd()
        t = path

        sleep(seconds)


        #prints the new dataframe in a .csv file
        sorted_final_df.to_csv(f'modified-sort_{file_name}', index=False, columns=sort_headers)


    #confirm the file was generated and sent to the folder the user is running the script in.
    print(f'\nOkay! I just created the .csv!\n\nIt is now in the {t} folder.')
        # print('1. Generate all data from the .csv using the following header names?: ', sort_headers)
        # print('2. Use the')
        # sleep(seconds)
        # input('')
        #Next would be to ask whether to remove duplicates from all columns or specific ones. Leave a note that if they remove duplicates from all columns, the rows will no longer be tied to an index
    # print(sort_headers)


        # sleep(milliseconds1)

        # print('Now that I have the column order there are a few more things I would like to confirm before generating the file.')


        #     ' '.join(sorted)
        # print(sorted)

            #remove white spaces
            # list_of_headers = col.strip()

            #remove quotes
            # temp_sorted_list = eval(list_of_headers)

            #append the list of headers entered by the user to the  new_headers array
            # temp_sorted_headers.append(temp_sorted_list)

            # sleep(milliseconds1)

            # print('Here\'s the list that I have: ', temp_sorted_list)
            # sleep(milliseconds1)

            # confirm_temp_sorted_list = input('Are the columns ordered correctly?')
            # if confirm_temp_sorted_list == 'y' or confirm_temp_sorted_list == 'Y':
            #Iterate through the list of new_headers
                # for item in temp_sorted_list:
                # #Remove white spaces
                #     final_list = item.strip()
                #append the
    #                 sort_headers.append(final_list)
    # print(sort_headers)
    # sleep(milliseconds1)
    # print('\n**********************************************************************************************************************\n')
    # print('1. Ingest a .csv file, remove duplicates....')
    # print('2. Ingest a .csv file, remove duplicates from each row....')
    # print('3. I only need the column headers you would like returned in the new datatable upon completion of this program.')
    # print('\n********************************************************************************************************************** \n')
    # sleep(seconds)

    # col_conf1 = input('Will you need all existing columns in the final file that I create for you?: ')
    # srt = input('Should I sort column headers?: ')
    # print(decoder.columns)
    # sample_columns = pd.DataFrame(decoder)
    # sample_columns.to_csv(f'sample_columns_{encoded_file}', index=False, header=sort_headers)



# # print('Okay, let\'s start over. Please re-run the script')


# def indName():
#     print('\nBefore we proceed tell me how I should reference the columns in the file. By it\'s column index or Header Name?')
#     sleep(milliseconds1)
#     ind_or_name = input('\nType \'1\' to reference columns by its index or \'one\' to reference by column header: ')
#     if ind_or_name == '1':
#         ind = int(ind_or_name)
#         sleep(milliseconds1)
#         confCol(ind)
#         # sleep(seconds)
# #         for :
# #             pass
# #         print(type(ind))
#     elif ind_or_name == 'one' or ind_or_name == 'One' or ind_or_name == 'ONE':
#         name = ind_or_name
#         confCol(name)
#     else:
#         print('Not A Valid Input: Exiting...')
#         sleep(seconds)
#         exit()

# #         headerName_conf = input('Reference columns in the file by its Header Name? (y/n): ')
# #         for:
# #             pass
# def confCol(value):
#     ''' Function to confirm how the script should reference the columns in the pd datatable, by int or string (Header name)'''
#     if value == 1:
#         colNum_conf = input('Reference columns in the file by its index? (y/n): ')
#         sleep(milliseconds1)
#     elif value == 'one' or value == 'One' or value == 'ONE':
#         headerName_conf = input('Reference columns in the file by its Header Name? (y/n): ')
#         sleep(seconds)
#         colHeaders()
#     else:
#         print('Not A Valid Input: Exiting...')
#         sleep(seconds)
#         exit()

# #     print('I see that there are ',,'in',,)
# #     print(type(name))
# # else:
# #     pass


# # else:


# #     column_index1 = input("")
# #     column_index1_label = input("")



def confirm_ColumnHeaders(file_name, temp_file_headers, temp_file_headers_beta):
    '''Confirm column Headers. If yes append the headers the user would like added in the final report to the file_headers array.'''

    #Confirm column headers
    confirmation = input('Have I listed the columns names above correctly? (y/n): ')

    if confirmation == 'y' or confirmation == 'Y':
        #If yes iterate through the list of temp_file_headers
        for col in temp_file_headers:
            #Remove white spaces
            final_list = col.strip()
        #append the list to the file_headers array
            file_headers.append(final_list)

    elif confirmation == 'n' or confirmation == 'N':
        column_headers(file_name, temp_file_headers_beta)
        # print('Not A Valid Input: Exiting...')
        # sleep(seconds)
        # exit()
    else:
        print('Not A Valid Input: Exiting...')
        sleep(seconds)
        exit()

    #Pass file_name and file_headers to sort_columns() function
    sort_columns(file_name, file_headers)


def column_headers(file_name, temp_file_headers):
    '''Specifies the columns to use in the new dataframe.'''

    #List of file headers to use in the .csv
    new_headers = []
    #Copy of file headers
    new_headers_beta = []

    #Creates a copy of the file headers, values assigned to new_headers_beta 
    for col1 in temp_file_headers:

        #Remove leading whitespace
        file_headers_beta = col1.lstrip()

        #append the list of headers entered by the user to the  new_headers array
        new_headers_beta.append(file_headers_beta)


    print('Got it!')
    sleep(milliseconds1)
    print(f'\nBefore we move on, the next few steps will cover the columns that I should return in the final .csv file and the order that the columns should follow.\n')
    sleep(milliseconds1)
    #Header names should be entered as a list, can be entered with or without quotations. 

    '''sleep(milliseconds1)

    print('\n**********************************************************************************************************************\n')
    print('1. Column order is not important in this step.....')
    print('2. Enter each of the column headers as it appears in the CSV file.')
    print('3. I only need the column headers you would like returned in the new datatable upon completion of this program.')
    print('\n********************************************************************************************************************** \n')
    # sleep(seconds)'''

    #prints the headers names from the .csv file for the user to reference

    sleep(milliseconds1)

    print(f'**If you would like the columns in the new .csv file to follow a different order than the original, I recommend entering the header names in the order in which you would like each to appear in the new .csv file**\n\n')
    sleep(milliseconds1)
    print(f'For convenience here were all of the header names from {file_name}\n\n{temp_file_headers}\n\n')

    # print("'Insertion Order', 'Insertion Order ID', 'Line Item', 'Line Item ID', 'Creative', 'Creative ID', 'Exchange', 'Exchange ID'")

    #Ask user to confirm header names to use in the .csv file
    new_file_headers = input("Begin entering the column names as you would like for each to appear in the final .csv file, comma separated (Feel free to copy/paste header names from the above!): ")

    #Edit .csv
    #Remove special characters
    edit_headers = new_file_headers.replace("'", "")
    #Remove whitespaces and separates the string into a list
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

    #passes the file_name and new_headers to the confirm_ColumnHeaders function
    confirm_ColumnHeaders(file_name, new_headers, new_headers_beta)

    # sort_cols(file_name)


# # print(file_headers)


#     # print(file_headers)

#     # print('I can return the file with unique values for each column or for a single column. Which would you prefer?')
#     # sleep(milliseconds1)
#     # print('***********************')
#     # print('Please note: Values returned from the \'Multi column\' opiton may no longer be associated with its index value upon completion of the script. If column index is important, the single column option may be better suited for your needs.')
#     # print('***********************')
#     # sleep(milliseconds1)
#     # sortOpt = int(input('Type \'1\' to deduplicate a single column in the datatable. Type \'2\' to deduplicate each column in the datatable.'))

#     # headers = input('enter the columns you would like output in the file.')

# def deduplicate_headers(file_name):
#     ''' Specify columns to deduplicate'''
#     temp_subset = []

#     print(f'Please specify the columns that you would like deduplicated. \n\n{file_headers}\n\n')
#     header_name = input('Header Name(s): ')

#     confirm_headers = header_name.replace("'", "")
#     #Remove whitespace, converts to list
#     header_list = confirm_headers.strip().split(",")

#     #iterate through the list of header names
#     for item in header_list:

#     #Remove leading whitespace
#         header_clean = item.lstrip()

#         #append list to temp_sorted_headers array
#         temp_subset.append(header_clean)
#     confirm_dedupe_header(file_name, temp_subset)

# def confirm_dedupe_header(file_name, temp_subset):
#     ''' Confirm user input '''
#     #confirms the headers to remove
#     print(f'Columns to deduplicate: {temp_subset}')
#     #Asks y/n
#     deduplicate_col = input('Is this correct?: ')
#         #If yes, add list to subset global array
#     if deduplicate_col == 'y' or deduplicate_col == 'Y':
#         for value in temp_subset:
#             dedupe_header = value.strip()
#             subset.append(dedupe_header)
#         deduplicate_file_with_headers(file_name)
#     elif deduplicate_col == 'n' or deduplicate_col == 'N':
#         pass
#     else:
#         print('Not A Valid Input: Exiting...')
#         sleep(seconds) 
#         exit()

    # print(subset)
                # deduplicate_file_with_headers(file_name)


        # header_name
        #         #Adds the csv to a new dataframe
        # final_df = pd.DataFrame(csv_file)
        # #get the path the user is running the script in
        # path = os.getcwd()
        # t = path

        # sleep(seconds)

        # # print(final_df)

        # #prints the new dataframe in a .csv file
        # final_df.to_csv(f'modified_{file_name}', index=False)



def deduplicate_file_with_headers(file_name):
    ''' Deduplicate rows from a file'''
    print('Removing rows')
    sleep(milliseconds1)
    if not sort_headers:
        csv_file = pd.read_csv(file_name, index_col=False, header=0, encoding='latin_1', usecols=file_headers)
        deduplicate_column = csv_file.drop_duplicates()
        final_csv = pd.DataFrame(deduplicate_column)

        #prints the new dataframe in a .csv file
        final_csv.to_csv(f'modified_{file_name}', index=False, columns=file_headers)
        path = os.getcwd()
        t = path

        sleep(seconds)
        #confirm the file was generated and sent to the folder the user is running the script in.
        print(f'\nOkay! I just created the .csv!\n\nmodified_{file_name} is now in your {t} folder.')

    else:
        csv_file = pd.read_csv(file_name, index_col=False, header=0, encoding='latin_1', usecols=file_headers)[sort_headers]
        deduplicate_column = csv_file.drop_duplicates()
        final_csv = pd.DataFrame(deduplicate_column)

        final_csv.to_csv(f'modified-sort_{file_name}', index=False, columns=sort_headers)


        path = os.getcwd()
        t = path

        sleep(seconds)
        #confirm the file was generated and sent to the folder the user is running the script in.
        print(f'\nOkay! I just created the .csv!\n\nmodified-sort_{file_name} is now in your {t} folder.')
        # duplicates = csv_file.loc[csv_file.duplicated(), :]
        # sduplicates = csv_file.loc[not duplicates]
        # drop = drop.append(csv_file.loc[duplicates])
        # second = csv_file.drop_duplicates(keep = 'first')
        # drop = pd.DataFrame(second)
        # duplicate_val = csv_file.loc[csv_file.duplicated(keep = 'first')]
        # removed_rows =
        # if val in duplicates == True:

        # print(csv_file, len(csv_file))
        # print(csv_file[~deduplicate_column])
        # print(duplicates, len(duplicates))
        # print(drop, len(drop))
        # print(second, len(second))
        # print(duplicate_val, len(duplicate_val))
        # print(sduplicates, len(sduplicates))
        # path = os.getcwd()
        # t = path
        # final_csv.to_csv(f'modified_{file_name}', index=False)

        #confirm the file was generated and sent to the folder the user is running the script in.
        # print(f'\nOkay! I just created the .csv!\n\nIt is now in the {t} folder.')
    # elif sort_headers:
    #     # len(sort_headers) == len(file_headers)
    #     filtered_csv_file = pd.read_csv(file_name, index_col=False, header=0,encoding='latin_1', usecols=file_headers) [sort_headers]
    #     #Adds the csv to a new dataframe
    #     sorted_final_df = pd.DataFrame(filtered_csv_file)
    #     #get the path the user is running the script in
    #     path = os.getcwd()
    #     t = path
#     # decode =  decoder[['Insertion Order ID', 'Insertion Order']]

#     # deduped_series1 = decode.drop_duplicates()
#     # deduped_series1.reset_index(drop=True, inplace=True)

#     # decode2 = decoder[['Line Item ID', 'Line Item']]

#     # deduped_series2 = decode2.drop_duplicates()
#     # deduped_series2.reset_index(drop=True, inplace=True)


#     # decode3 = decoder[['Creative ID', 'Creative']]

#     # deduped_series3 = decode3.drop_duplicates()
#     # deduped_series3.reset_index(drop=True, inplace=True)
#     # # print(deduped_series3)

#     # decode4 = decoder[['Exchange ID', 'Exchange']]

#     # deduped_series4 = decode4.drop_duplicates()
#     # deduped_series4.reset_index(drop=True, inplace=True)
#     # print(deduped_series4)
#     # decode5 = decoder
#     # print(decode2)
#     # deduped_series5 = decode5.drop_duplicates()
#     # p = deduped_series5.where(pd.notnull(deduped_series5), None)
#     # print(p)

#     # print(decoder[~deduped_series1])
#     # print(decoder[~deduped_series2])
#     # print(decoder[~deduped_series3])
#     # print(decoder[~deduped_series4])
#     # new_series = pd.concat([deduped_series1, deduped_series2, deduped_series3, deduped_series4], axis=1)
#     # new_series[['Insertion Order ID']].astype(int)
#     # new_series.fillna('')
#     # print(new_series.dtypes)
#     # col1.append(new_series)
#     # for key, value in new_series.items():
#     #     if value == 'Nan':
#     #         print('n')
#         # print(key)

#     # print(new_series)
#     # #Convert to a list
#     # encoded_url_item = list(decode)
#     # lines = len(list(encoded_url_item))
#     # print(f'\nNumber of rows in "{encoded_file}" file : {lines}')

#     # #loop through the rows in the encoded file
#     # for item in encoded_url_item:
#     #   #Decode the urls
#     #     decoded_url = urllib.parse.unquote(item)
#     #   #Decodes the list again
#     #     double_decoded_url = urllib.parse.unquote(decoded_url)
#     #     d = double_decoded_url.split(", ")
#     #     "".join(double_decoded_url)
#     #   #De-duplicate the URLs
#     #     for url in d:
#     #       #If the URL/Domain is a duplicate move to duplicates
#     #       if url in urls:
#     #         duplicates.append(url)
#     #       else:
#     #       #If the URL/Domain is not a duplicate move to urls
#     #         urls.append(url)

#     # sample_columns = pd.DataFrame(new_series)
#     # lines2 = len(revised_domain)

#     # excluded_domains = pd.DataFrame(duplicates)
#     # lines3 = len(excluded_domains)

#     # print(f'\nFile is now Decoded and Deduplicated!')

#     # #prints all de-duped URLs/domains to Revised csv file
#     # sample_columns.to_csv(f'sample_columns_{encoded_file}', index=False, header=sort_headers)
#     # #Prints all the domains removed from the file to a separate CSV for review
#     # excluded_domains.to_csv(f'Removed_Domains.csv', index=False, header=None)

#     # print(f'\nThe Deduped and decoded urls were sent to "Revised_{encoded_file}".\n \nNumber of rows in "Revised_{encoded_file}" : {lines2}\n \nA list of the domains removed from the "{encoded_file}" file were output in the "Removed_Domains.csv" file.\n \nNumber of rows in "Removed_Domains.csv" : {lines3}\n')

# arg1 = sys.argv[1]
# format_urls(arg1)


# Step 1: read diff data from location
# Step 2: Create a pretty print out like the compare_stack_tool
# Step 3: We dont need slow and all that because we will compare otherwise
# See what metrics does compare_stack tool compare on
 
# import pandas as pd
# import dask.dataframe as dd
# from colorama import Fore
 
# s3_path = 's3://moat-data-pipeline-scratch/diffs/adtype=display/year=2022/month=8/day=29/sources=sc-ilf-kafka-test-sc-ilf-control/'
# input_path = s3_path + '*.parquet'
# threshold = 10
# source1 = "sc-ilf-kafka-test"
# source2 = "sc-ilf-control"
 
# df = dd.read_parquet(input_path)
# df = df.compute()
# if not df.index.is_unique:
#     df = df.reset_index()
#     df = df.drop(columns=['index'])
 
# # Drop Mater level0tops for comparision tool
# df['master'] = df.level0top.str.contains('MASTER')
# df = df[df['master'] == False]
 
# pct_cols = [ col for col in df.columns if col.endswith('_pct') ]
# len(pct_cols)
# df2 = df[pct_cols]
# level0tops = list(df.level0top)
 
# def above_threshold(x, threshold):
#     return abs(x)>threshold
 
# def pretty_print(val):
#     # if abs(val) > 50:
#     #     return ['background-color: red'] * len(val)
#     # else:
#     #     return ['background-color: white'] * len(s)
#     pass
 
# for level0top in level0tops[:1]:
#     level0top_df = df[df['level0top'] == level0top][pct_cols]
#     pct_conditonals = level0top_df.apply(above_threshold, threshold=threshold, axis=1)
# # df.gt(threshold)?
#     # print(level0top_df.gt(threshold))
#     # break
#     cols_above_threshold = [col for col in pct_conditonals.columns if list(pct_conditonals[col])[0]]
 
#     level0top_df = level0top_df[cols_above_threshold]
#     print("Level0top {} has the following discrepancy which is outside the threshold of {}".format(level0top, threshold))
     
#     base_metrics = [c[:-4] for c in cols_above_threshold]
#     s1cols = []
#     s2cols = []
#     cols = []
#     for m in base_metrics:
#         cols.append(source1+"_"+ m)
#         s1cols.append(source1+"_"+ m)
#         cols.append(source2+"_"+ m)
#         s2cols.append(source2+"_"+ m)
     
#     level0top_df = df[df['level0top'] == level0top][cols_above_threshold]
#     t1 = df[df['level0top'] == level0top][s1cols]
#     t2 = df[df['level0top'] == level0top][s2cols]
 
 
#     # df1 for source 1
#     t1.rename(columns=lambda x: x.replace(source1+"_" ,""), inplace=True)
#     t1_dict = t1.to_dict('list')
 
#     for k in t1_dict.keys():
#         t1_dict[k] = t1_dict[k][0]
 
#     test1 = pd.DataFrame.from_dict(t1_dict, orient='index', columns=[source1])
 
#     # df2 for source 1
#     t2.rename(columns=lambda x: x.replace(source2+"_" ,""), inplace=True)
#     t2_dict = t2.to_dict('list')
 
#     for k in t2_dict.keys():
#         t2_dict[k] = t2_dict[k][0]
 
#     test2 = pd.DataFrame.from_dict(t2_dict, orient='index', columns=[source2])
 
#     # df3 for percentage (%)
#     level0top_df.rename(columns=lambda x: x.replace("_pct" ,""), inplace=True)
#     level0top_df_dict = level0top_df.to_dict('list')
 
#     for k in level0top_df_dict.keys():
#         level0top_df_dict[k] = level0top_df_dict[k][0]
 
#     level0top_df = pd.DataFrame.from_dict(level0top_df_dict, orient='index', columns=["percentage"])
 
# print(level0top_df.shape)
# print(df.shape)
# print(t1.shape)
# print(t2.shape)
 
# Level0top UMMLB1 has the following discrepancy which is outside the threshold of 10
# (1, 127)
# (97, 777)
# (1, 127)
# (1, 127)

welcome()