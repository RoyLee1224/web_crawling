#!/usr/bin/env python
# coding: utf-8

# In[506]:


import requests
from bs4 import BeautifulSoup

from PyPDF2 import PdfReader

from pdfminer.high_level import extract_text
import os

file_dir = os.getcwd()
# script_dir = os.path.dirname(file_name)
if not (os.path.exists(file_dir+"/"+'pdf')):
    os.mkdir('pdf')
if not (os.path.exists(file_dir+"/"+'txt')):
    os.mkdir('txt')


def getHTML(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    return soup


print("#"*30 + "create 'thema.txt' from '테마여행'" + "#"*30)

url_bbs = 'https://www.taiwantour.or.kr/bbs'
url_thema = "https://www.taiwantour.or.kr/bbs/board.php?bo_table=m08_01&sca=%ED%9C%B4%EC%96%91"  # 휴양
a_list = getHTML(url_thema).select('div.sub_menu a')
thema_content = ""

for a in a_list:
    url_bbs_subPage = url_bbs + a['href'][1:]
    tags = getHTML(url_bbs_subPage).select('div.rt p')
    for tag in tags:
        thema_content += tag.text

# print(thema_content)
f = open("thema.txt", "w+")
f.write(thema_content)
f.close()

print("thema.txt downloaded")
print("\n")

print("#"*30+" create 'pro.txt' from '프로대만족'" + "#"*30)

url_pro = 'https://www.taiwantour.or.kr/bbs/board.php?bo_table=m06_12'
pro_content = ""


def get_pro_content(url):
    global pro_content
    a_list = getHTML(url).select('div.subject a')
    for a in a_list:
        p_list = getHTML(a["href"]).select('div.magazine_view p')

        for p in p_list:
            pro_content += p.text


def get_pro_page(pages):
    temp_url = url_pro
    for page in range(1, pages):
        print(f"downloading page {page}")
        next_page_url = url_pro + "&page=" + str(page)
        temp_url = next_page_url
        get_pro_content(temp_url)


get_pro_page(21)

f = open("pro.txt", "w+")
f.write(pro_content)
f.close()

print("pro.txt downloaded")
print("\n")


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
        if (len(contents) != 1 and ("\n" not in contents)):
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


get_place_page(9)

# print(place_content)

f = open("place.txt", "w+")
f.write(place_content)
f.close()

print("place.txt downloaded")
print("\n")

print("#"*30+"download quarterly magazine PDF"+"#"*30)

url_magazine = "https://www.tva.org.tw/Publications?"
url_start_page = "https://www.tva.org.tw/Publications?page=1"
span_list = getHTML(url_magazine).select('ul.text li span')
target_list = []
download_list = []


def get_magazine_page(pages):
    global span_list
    temp_url = url_start_page
    for page in range(2, pages):
        span_list += getHTML(temp_url).select('ul.text li span')
        next_page_url = url_magazine + "page=" + str(page)
        temp_url = next_page_url


get_magazine_page(21)

for i in range(44, 47):
    target_list.append("Vol. " + str(i))

print("Search for: ", target_list)

for span in span_list:
    #     if "Vol." in span.text:
    if span.text.strip() in target_list:
        name = span.text.strip()
        a_tag = span.parent.previous_sibling.previous_sibling["href"]
        number = name.split(' ')[-1]
        url_pdf = f"https://www.tva.org.tw{a_tag}"

        print("Downloading file: ", f"v{number}.pdf")

        # Get response object for link
        response = requests.get(url_pdf)

        # Write content in pdf file
        os.chdir(file_dir)
        pdf = open(os.path.join(file_dir, "pdf", f"v{number}.pdf"), 'wb')
        pdf.write(response.content)
        pdf.close()

print("All PDF files downloaded")
print("\n")

print("#"*30+"convert pdf to txt"+"#"*30)

for target in target_list:
    number = target.split(' ')[-1]
    print(f"Converting v{number}.pdf")
    os.chdir(os.path.join(file_dir, "pdf"))
    text = extract_text(f"v{number}.pdf", 'rb')
    f = open(os.path.join(file_dir, "txt", f"v{number}.txt"), "w+")
    f.write(text)
    f.close()

print("All pdf files converted")
print("\n")


print("#"*30+"merge txt"+"#"*30)

filenames = []
for target in target_list:
    number = target.split(' ')[-1]
    filenames.append(f"v{number}.txt")

os.chdir(file_dir)
with open('44~46.txt', 'w') as outfile:
    for fname in filenames:
        with open(os.path.join(file_dir, "txt", fname)) as infile:
            for line in infile:
                outfile.write(line)
print("44~46.txt downloaded")
print("\n")
