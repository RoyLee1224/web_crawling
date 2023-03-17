#!/usr/bin/env python
# coding: utf-8

# In[119]:
import os

from htmlRequest import getHTML

file_dir = os.getcwd()
# In[22]:


def getTaiwanTour():
    # print("#"*30 + "create 'thema.txt' from '테마여행'" + "#"*30)

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

    # print("#"*30+" create 'pro.txt' from '프로대만족'" + "#"*30)

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

    # print("#"*30 + "create 'place.txt' from '대만 명소'" + "#"*30)

    url_place = 'https://www.taiwantour.or.kr/bbs/board.php?bo_table=m03&'
    place_content = ""

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
