import sys
import csv
import urllib
from urllib.parse import urlparse, unquote
import os
import string
import xlrd
import pandas as pd

def oboPixel():
    ''' Create OBO pixel'''
    new_headers = []
    file_name = input ('insert the name of the .xls file: ')
    xlsFile =  pd.read_excel(file_name, index_col=0, engine="xlrd", skiprows=10)
    header_names = list(xlsFile.columns)
    print(f'Here were each of the column headers detected in {file_name}: \n\n {header_names}\n\n')

    headersToUse = input('Please specify the columns that contain the values that I should insert inside of the OBO pixel(s): ')

    edit_headers = headersToUse.replace("'","")
    edit_headers_list = edit_headers.strip().split(",")
    for col in edit_headers_list:

        file_headers_clean = col.strip()

        new_headers.append(file_headers_clean)
    
    print(f'Thanks! Here are the columns detected \n\n')
    
    preview = pd.read_excel(file_name, engine="xlrd", skiprows=10, usecols=new_headers)
    new_headers_preview = pd.DataFrame(preview)
    print(new_headers_preview)
    new_headers_preview.to_csv(f'oboPixels.csv', index=0)
    
    path = os.getcwd()
    t = path
    
    print(f'A sample file is now available in your {t} folder. \n\n file_name: oboPixels.csv')

    # l1 = input('level1: ')
    # l2 = input('level2: ')
    # l3 = input('level3: ')
    # l4 = input('level4: ')
    # zMoat = input('zMoatADV: ')

    
    # attributes = input('Should there be any zMoat\'s added? (y/n): ')
    # if attributes == 'y' or 'Y':
    #     attrCount = int(input(' How many additional zMoat\'s will be needed in the OBO pixels: '))
        
    #     confColumn = input(' Does the column containing the value you would like to assign against the zMoat exists in the .xls file? (y/n): ')
    #     if confColumn == 'y' or 'Y':
    


    
    # oboPixelHeader = 'https://obo.moatads.com/pixel.gif?e=0&g=0&ac=1&bq=7&f=1&gh=0&hc=0&i='
    # ikey = input('Insert the iKey: ')
    # timestamp = input('Insert timestamp macro: ')
    # cachebuster = input('Insert Cache-buster macro: ')
    # akamaiCachebuster = input('Insert a Session id macro. If one does note exist Insert the cachebuster macro: ')

oboPixel()
