import pandas as pd
import sys
import string
import os

#Static list of ad server domains
adserver_domain_list = [
    'admarvel.com',
    'adnxs.com',
    'adtech.com',
    'aerserv.com',
    'amazon-adsystem.com',
    'doubleclick.net',
    'fwmrm.net',
    'googleadservices.com',
    'googlesyndication.com',
    'inner-active.mobi',
    'madsone.com',
    'mobileposse.com',
    'mopub.com',
    'mydas.mobi',
    'nexage.com',
    'openx.net',
    'rubiconproject.com',
    'smaato.net'
    ]

def remove_domains(csv_file_name ,error_domains):
    """
    This function will accept the csv_file_name and error_domains as arguments. Upon completion the script will write two csv files, 'edited_{csv_file_name}' containing the domains considered valid and 'removed_domains_{csv_file_name}' containing the domains considered invalid.

    The csv_file_name is the original.csv file provided by the client
    
    The error_domains is the errors.csv file generated from the blocking tool

    This function will also run a check against the adserver_domain_list array and exclude matches when writing the edited_{csv_file_name} spreadsheet
    """

    #Reads the csv_file_name and assigns to a dataframe
    df = pd.read_csv(csv_file_name,index_col=False,header=None, encoding='utf_8')
    df.columns = ['domains']

    #Reads the error_domains and assigns to a dataframe
    df_remove = pd.read_csv(error_domains,header=None, skipinitialspace=True)
    df_remove.columns = ['domains']
    df_remove = df_remove['domains'].str.strip()

    #Concatenates the adserver_domain_list and rows from df_remove
    error_domains_list=df_remove.tolist() + adserver_domain_list

    sub = '"'
    index_list=[]
    n=2

    #Iterates over the error_domains_list and assigns each value an index in the dataframe
    for int, text in enumerate(error_domains_list):
        if sub in text:
            index_list.append(int)
    final = [index_list[i * n:(i + 1) * n] for i in range((len(index_list) + n - 1) // n )]
    for i in final:
        x = i[0]
        y = i[1] + 1

        #joins the list by comma delimeter
        error_domains_list[x] = ", ".join(error_domains_list[x:y])
        
        #remove quotes
        error_domains_list[x] = error_domains_list[x].replace('"',"")

    #If a value from the csv_file_name is not in the error_domains_list, assign the value to the new_df_list variable
    new_df = df[~df['domains'].isin(error_domains_list)]
    new_df.columns = ['domains']
    new_df_list = new_df['domains'].tolist()
    
    #if a value from the csv_file_name is in the error_domains_list, assign the value to the removed_domains_list variable
    removed = df[df['domains'].isin(error_domains_list)]
    removed.columns = ['error_domains']
    removed_domains_list = removed['error_domains'].tolist()

    #append each item from the removed_domains_list to an empty array called invalid_list
    invalid_list = []
    for domain in removed_domains_list:
        invalid_list.append(domain)

    #Cleans up the new_df_list by checking for non-standard characters.
    #Values that pass this check will be categorized as valid and appended onto the valid_list array. 
    #Values that do not pass this check will be categorized as invalid and appended onto the invalid_list array.
    allowed = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + '.' + '-' + '_')
    valid_list = []
    for x in new_df_list:
        extra = set(x) <= allowed
        if extra == True:
            valid_list.append(x)
        elif extra == False:
            invalid_list.append(x)
        else:
            pass

    #assigns the valid_list array to a new dataframe called cleanup_df
    cleanup_df = pd.DataFrame(valid_list)
    number_of_rows_revised = cleanup_df.size
    
    #assigns the invalid_list array to a new dataframe called removed_df
    removed_df = pd.DataFrame(invalid_list)
    number_of_rows_removed = removed_df.size

    path = os.getcwd()

    #Write the contents from the cleanup_df to a csv called 'edited_{csv_file_name}'
    cleanup_df.to_csv('edited_{}'.format(csv_file_name), index=False,header=None)

    #Write the contents from the removed_df to a csv called 'removed_domains_{csv_file_name}'
    removed_df.to_csv('removed_domains_{}'.format(csv_file_name), index=False,header=None)

    #Output instructions for the user. This code will write the .csv's in the working directory
    print(f'\nI have added two files in {path}: "edited_{csv_file_name}" and "removed_domains_{csv_file_name}"\n\n Number of rows in the "edited_{csv_file_name}" file: {number_of_rows_revised}\n Number of rows in the "removed_domains_{csv_file_name}" file: {number_of_rows_removed}\n')

arg1 = sys.argv[1]
arg2 = sys.argv[2]

remove_domains(arg1 ,arg2)
