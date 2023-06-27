import sys
import csv
import urllib
from urllib.parse import urlparse, unquote
import os
import string
import pandas as pd

def format_urls(encoded_file):
    decoder = pd.read_csv(encoded_file, index_col=False, header=None, encoding='latin_1')
    decoder.columns = ['URL']

    urls = []
    duplicates = []

    decode =  decoder['URL'].str.strip()
    #Convert to a list
    encoded_url_item = list(decode)

    #loop through the rows in the encoded file
    for item in encoded_url_item:
      #Decode the urls
        decoded_url = urllib.parse.unquote(item)
      #Decodes the list again
        double_decoded_url = urllib.parse.unquote(decoded_url)
        d = double_decoded_url.split(", ")
        "".join(double_decoded_url)

      #De-duplicate the URLs
        for url in d:
        #If the URL/Domain is a duplicate move to duplicates
          if url in urls:
            duplicates.append(url)
          else:
        #If the URL/Domain is not a duplicate move to urls
            urls.append(url)

    revised_domain = pd.DataFrame(urls)
    excluded_domains = pd.DataFrame(duplicates)

    #Prints all de-duped URLs/domains to Revised csv file
    revised_domain.to_csv(f'Revised_{encoded_file}', index=False, header=None)
    #Prints all the domains removed from the file to a separate CSV for review
    excluded_domains.to_csv(f'Modified_Domains.csv', index=False, header=None)

    print('Domains are now Decoded and Deduplicated!')
    print('Domains removed from csv were output in "Modified_Domains.csv" file.')

arg1 = sys.argv[1]

format_urls(arg1)