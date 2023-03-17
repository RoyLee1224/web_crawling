#!/usr/bin/env python
# coding: utf-8

# In[119]:
import os
from taiwanTour import getTaiwanTour
from magazine import getMagazine
# In[ ]:

file_dir = os.getcwd()
# script_dir = os.path.dirname(file_name)
if not (os.path.exists(file_dir+"/"+'pdf')):
    os.mkdir('pdf')
if not (os.path.exists(file_dir+"/"+'txt_Pages')):
    os.mkdir('txt_pages')
if not (os.path.exists(file_dir+"/"+'txt_Volumes')):
    os.mkdir('txt_volumes')
if not (os.path.exists(file_dir+"/"+'cache')):
    os.mkdir('cache')

# In[6]:
getTaiwanTour()
# In[10]:
getMagazine()
