#!/usr/bin/env python
# coding: utf-8

# In[119]:


import requests
from bs4 import BeautifulSoup

# from PyPDF2 import PdfReader

from pdfminer.high_level import extract_text
import os


# In[120]:


from PyPDF4 import PdfFileReader, PdfFileWriter
from pikepdf import Pdf
import pdfplumber


# In[ ]:


from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import re


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


def getHTML(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    return soup


# In[22]:


print("#"*30 + "create 'thema.txt' from '테마여행'" + "#"*30)

url_bbs = 'https://www.taiwantour.or.kr/bbs'
url_thema = "https://www.taiwantour.or.kr/bbs/board.php?bo_table=m08_01&sca=%ED%9C%B4%EC%96%91"  # 휴양
thema_content = ""

a_list = getHTML(url_thema).select('div.sub_menu a')

if not (os.path.exists(file_dir+"/thema.txt")):
    for a in a_list:
        url_bbs_subPage = url_bbs + a['href'][1:]
        title = getHTML(url_bbs_subPage).select('div.page h1')
        subtitle = getHTML(url_bbs_subPage).select('div.page h2')
        thema_content += title[0].text
        thema_content += "\n"
        thema_content += subtitle[0].text

        tags = getHTML(url_bbs_subPage).select('div.rt p')
        for tag in tags:
            if(tag.parent.h3):
                thema_content += "\n"*2
                thema_content += tag.parent.h3.text
                thema_content += "\n"
            thema_content += tag.text

# print(thema_content)
f = open("thema.txt", "w+")
f.write(thema_content)
f.close()

print("thema.txt downloaded")
print("\n")


# In[20]:


print("#"*30+" create 'pro.txt' from '프로대만족'" + "#"*30)

url_pro = 'https://www.taiwantour.or.kr/bbs/board.php?bo_table=m06_12'
pro_content = ""


def get_pro_content(url):
    global pro_content
    a_list = getHTML(url).select('div.subject a')
    for a in a_list:
        pro_content += "\n"*1
        title = getHTML(a["href"]).select('div.magazine_view h3')
        pro_content += title[0].text
        pro_content += "\n"*2
        p_list = getHTML(a["href"]).select('div.magazine_view p')

        for p in p_list:
            pro_content += p.text


def get_all_content(url):
    global place_content
    dis_list = getHTML(url).select('div.list-details')
    for dis in dis_list:
        place_content += dis.text


def get_pro_page(pages):
    temp_url = url_pro
    for page in range(1, pages):
        print(f"downloading page {page}")
        next_page_url = url_pro + "&page=" + str(page)
        temp_url = next_page_url
        get_pro_content(temp_url)


if not (os.path.exists(file_dir+"/pro.txt")):
    get_pro_page(21)
# print(pro_content)

f = open("pro.txt", "w+")
f.write(pro_content)
f.close()

print("pro.txt downloaded")
print("\n")


# In[21]:


print("#"*30 + "create 'place.txt' from '대만 명소'" + "#"*30)

url_place = 'https://www.taiwantour.or.kr/bbs/board.php?bo_table=m03&'
place_content = ""

url_content = "https://www.taiwantour.or.kr/bbs/board.php?bo_table=m03&wr_id=63"


def get_content(url):
    global place_content
    view_content_list = getHTML(url).select('div.view-content')
    content_list = getHTML(url).select('div.content')
    all_content_list = view_content_list + content_list

    for all_content in all_content_list:
        contents = all_content.contents
        title = contents[0].parent.parent.h1 or contents[0].parent.parent.div
        place_content = place_content + "\n" + title.text + "\n"
#         if there's more than one block in description, the first sentence will disappear due to unknown reason.
#         so the first sentence have to be handled separately
        if(len(contents) != 1 and ("\n" not in contents)):
            first_sentence = contents[0]
            place_content += first_sentence

        for sentence in contents:
            #             remove Tags such as <br/>
            if str(type(sentence)) != "<class 'bs4.element.Tag'>":
                place_content += sentence

#     print("place_content", place_content)


def get_links(url):
    a_list = getHTML(url).select('div.list-link a')
    for a in a_list:
        get_content(a["href"])


def get_place_dis(url):
    global place_content
    dis_list = getHTML(url).select('div.list-details')
    for dis in dis_list:
        place_content += dis.text


def get_place_page(pages):
    temp_url = url_place
    for page in range(1, pages):
        print(f"downloading page {page}")
        next_page_url = url_place + "page=" + str(page)
        temp_url = next_page_url
        get_links(temp_url)


if not (os.path.exists(file_dir+"/place.txt")):
    get_place_page(9)

# print(place_content)

f = open("place.txt", "w+")
f.write(place_content)
f.close()

print("place.txt downloaded")
print("\n")


# In[10]:


print("#"*30+"download quarterly magazine PDF"+"#"*30)

url_magazine = "https://www.tva.org.tw/Publications?k2=021ed026180c400ea0fd7c6fe5d61588&"
vol_list = getHTML(url_magazine).select('ul.text li span')
target_list = []


def get_magazine_page(pages):
    global vol_list
    temp_url = url_magazine + "page=2"
    for page in range(3, pages+2):
        vol_list += getHTML(temp_url).select('ul.text li span')
        next_page_url = url_magazine + "page=" + str(page)
        temp_url = next_page_url


get_magazine_page(3)

# for span in vol_list:
#     print(span.text.strip())

for i in range(1, 48):
    target_list.append("Vol. " + str(i).zfill(2))

for span in vol_list:
    #     if "Vol." in span.text:
    if span.text.strip() in target_list:
        name = span.text.strip()
        a_tag = span.parent.previous_sibling.previous_sibling["href"]
        number = name.split(' ')[-1]
        url_pdf = f"https://www.tva.org.tw{a_tag}"

        # Get response object for link
        if not (os.path.exists(file_dir+'/pdf/'+f"v{number}.pdf")):
            print("Downloading file: ", f"v{number}.pdf")
            response = requests.get(url_pdf)

            # Write content in pdf file
            os.chdir(file_dir)
            pdf = open(os.path.join(file_dir, "pdf", f"v{number}.pdf"), 'wb')
            pdf.write(response.content)
            pdf.close()

print("Downloaded all PDF files")
print("\n")


# In[178]:


print("#"*30+"Seperate all PDFs"+"#"*30)

black_list = ['도표', "통계", "Content", "fax"]
for vol in range(1, 48):
    pdf_in_file = f"pdf/v{str(vol).zfill(2)}.pdf"
    try:
        with pdfplumber.open(pdf_in_file) as pdf_plumber:
            for page in pdf_plumber.pages:
                if str(page.page_number) == "1":
                    continue

                pdf_out_file = f"cache/v{str(vol).zfill(2)}-p{str(page.page_number).zfill(2)}.pdf"
                if (os.path.exists(pdf_out_file)):
                    continue

                pageContent = page.extract_text()
                if not (("통계" in pageContent and "%" in pageContent) or ("Content" in pageContent) or ("FAX" in pageContent)):
                    with open(pdf_out_file, "wb") as outputStream:
                        output = PdfFileWriter()
                        output.addPage(PdfFileReader(
                            open(pdf_in_file, "rb")).getPage(page.page_number - 1))
                        output.write(outputStream)

    except Exception as e:
        print(f"Error processing {pdf_in_file}: {e}")

print("Seperated all PDF files.")
print("\n")


# In[189]:


pdfList = os.listdir(os.path.join(file_dir, "cache"))
pdfList.sort()


# In[243]:


print("#"*30+"Convert seperated PDFs to txt"+"#"*30)
for li in pdfList:
    if li == ".DS_Store":
        continue
    output_string = StringIO()
    txt_out_file = f"txt_pages/{li.replace('pdf','txt')}"
    try:
        if (os.path.exists('cache/'+li)):
            continue
        with open('cache/'+li, 'rb') as fInput:
            extract_text_to_fp(fInput, output_string, codec='utf-8')
            cleaned_text = re.sub(r'\(cid:\d+\)', '',
                                  output_string.getvalue().strip())
            # skip the page if the content is less than 140 chars
            if len(cleaned_text) > 140:
                with open(os.path.join(file_dir, txt_out_file), "w") as fOutput:
                    fOutput.write(cleaned_text)
#                     print("="*48+txt_out_file+"="*48)
#                     print(len(cleaned_text))

    except Exception as e:
        print(f"Error processing {li}: {e}")
#             continue

print("All txt_pages converted.")
print("\n")


# In[240]:


txtList = os.listdir(os.path.join(file_dir, "txt_pages"))
txtList.sort()
txtList.pop(0)


# In[245]:


print("#"*30+"txt_volumes"+"#"*30)

for num in range(1, 48):
    volume = f"v{str(num).zfill(2)}"
    with open(os.path.join(file_dir, "txt_volumes", f"{volume}.txt"), "w") as ouputTxt:
        for txt in txtList:
            if volume in txt:
                with open(os.path.join(file_dir, "txt_pages", txt)) as inputTxt:
                    for line in inputTxt:
                        ouputTxt.write(line)
                    ouputTxt.write("\n"*3)
print("All txt_volumes downloaded")
print("\n")
