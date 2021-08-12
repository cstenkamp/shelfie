#!/usr/bin/env python
# coding: utf-8

# # Title matching
# 
# Given the actual titles of books on bookshelves (manually entered), queries each of the book information sources for the titles that they return; this is used in order to actually determine whether a true match is made or not when some book information is obtained
# 
# Saves the information to the correct place.

# ## Imports

# In[1]:


import csv
import os
import time
import sys


sys.path.append('..')
import main

sys.path.append('../models')
import scraper


# ## Load a bookshelf

# In[2]:


# Set directories
SHELFY_BASE_PATH = os.path.abspath(os.path.dirname(main.__file__))
bookshelf_directory = SHELFY_BASE_PATH + '/data/shelves/'
bookshelf_name = 'home_6'
bookshelf_path = bookshelf_directory + bookshelf_name + '/titles'


# Output file paths
isbn_output_path = bookshelf_directory + bookshelf_name + '/isbns'
amazon_products_titles_output_path = bookshelf_directory + bookshelf_name + '/titles_amazon_products'



# Read book titles in from plain text file
book_titles = []
with open(bookshelf_path, 'r') as file_handle:
    for book_title in file_handle:
        book_titles.append(book_title.replace('\n', ''))
        
print(book_titles)


# ## Perform the queries

# In[3]:


query_google_urls = [scraper.get_google_search_url_from_query(book_title) for book_title in book_titles]
query_google_urls[:2]


# ##### Write ISBN's to file

# In[4]:


# Get the info

isbns = []
for i in range(len(query_google_urls)):
    print(i+1, '/', len(query_google_urls))
    
    isbn = None
    while isbn == None:
        isbn = scraper.get_isbn10_from_google_search(query_google_urls[i])
    print(isbn)
    isbns.append(isbn)
    
        


# In[ ]:


# Write results to file

with open(isbn_output_path, 'w') as file_handle:
    writer = csv.writer(file_handle, delimiter = ',')
    for isbn in isbns:
        writer.writerow([isbn])


# ##### Load ISBNs

# In[ ]:


# Load isbns
isbns = []
with open(isbn_output_path, 'r') as file_handle:
    reader = csv.reader(file_handle, delimiter = ',')
    for isbn in reader:
        isbns.append(isbn[0])
        
print(isbns)


# ##### Amazon Products API

# In[ ]:


# Get the info

amazon = scraper.get_amazon_object()
amazon_products_titles = []
for i in range(len(isbns)):
    print(i, '/', len(isbns) - 1)
    
    title = 'NONE'
    
    num_attempts = 0
    while title == 'NONE':
        try:
            num_attempts += 1
            book_info = scraper.query_amazon_products_api(isbns[i], amazon)
            print(book_info)
            title = book_info['title']
            
            
        except:
            print('\tfailed')
            pass
        
        if num_attempts > 10:
            break
        
    print('\t', title, '\t', isbns[i])
    amazon_products_titles.append(title)


# In[ ]:


# Write results to file
with open(amazon_products_titles_output_path, 'w') as file_handle:
    writer = csv.writer(file_handle, delimiter = ',')
    for i in range(len(isbns)):
        writer.writerow([isbns[i], amazon_products_titles[i]])


# In[ ]:




