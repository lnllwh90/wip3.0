import sys
import csv
import urllib.parse
import os
import pandas as pd
# import string

def encoded_urls(encoded_file, error_domains):
    	df = pd.read_csv(encoded_file, index_col=False, header=None, encoding='latin_1')
    df.columns = ['domains']

# with open('decoded_deduplicated_lld_file_1.6.csv', 'a', newline='') as csvwritefile:
   	deencoded_writer = pd.reach_csv(error_domains, header=None, skipinitialspace=True) as 
	   # csv.writer(csvwritefile, delimiter=' ')
#    	with open('bluehivecanadavpaid2957924003_moat_logs_2020-06-07_2.csv', 'r', newline='') as csvfile:
#    		deduplicated_file = csv.reader(csvfile)
   		for row in encoded_file:
   			# row[0]= url
   			# print (url)
   			#converts to a list
   			list_row = list(row)
   			#references the 2nd column of the CSV file
   			encoded_url_item = list_row[1]
   			#URLs are double encoded, following will decode the URLs twice
   			decoded_url = urllib.parse.unquote(encoded_url_item)
   			double_decoded_url = urllib.parse.unquote(decoded_url)
   			#convert to a list, then write contents to a csv file
   			deencoded_writer.writerow([double_decoded_url])


