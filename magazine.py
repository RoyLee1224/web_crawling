import requests

from pdfminer.high_level import extract_text
import os

# In[120]:


from PyPDF4 import PdfFileReader, PdfFileWriter
import pdfplumber


# In[ ]:

from io import StringIO
from pdfminer.high_level import extract_text_to_fp
import re

from htmlRequest import getHTML
# In[ ]:


file_dir = os.getcwd()


def getMagazine():
    # print("#"*30+"download quarterly magazine PDF"+"#"*30)

    url_magazine = "https://www.tva.org.tw/Publications?k2=021ed026180c400ea0fd7c6fe5d61588&"
    vol_list = getHTML(url_magazine).select('ul.text li span')
    target_list = []

    def get_magazine_page(pages, vol_list):
        temp_url = url_magazine + "page=2"
        for page in range(3, pages+2):
            vol_list += getHTML(temp_url).select('ul.text li span')
            next_page_url = url_magazine + "page=" + str(page)
            temp_url = next_page_url

    get_magazine_page(3, vol_list)

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
                pdf = open(os.path.join(
                    file_dir, "pdf", f"v{number}.pdf"), 'wb')
                pdf.write(response.content)
                pdf.close()

    print("Downloaded all PDF files")
    print("\n")

    # In[178]:

    # print("#"*30+"Seperate all PDFs"+"#"*30)

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

    print("Seperated all PDFs.")
    print("\n")

    # In[189]:

    pdfList = os.listdir(os.path.join(file_dir, "cache"))
    pdfList.sort()

    # In[243]:

    # print("#"*30+"Convert seperated PDFs to txt"+"#"*30)
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

    print("txt_pages converted.")
    print("\n")

    # In[240]:

    txtList = os.listdir(os.path.join(file_dir, "txt_pages"))
    txtList.sort()
    txtList.pop(0)

    # In[245]:

    # print("#"*30+"txt_volumes"+"#"*30)

    for num in range(1, 48):
        volume = f"v{str(num).zfill(2)}"
        with open(os.path.join(file_dir, "txt_volumes", f"{volume}.txt"), "w") as ouputTxt:
            for txt in txtList:
                if volume in txt:
                    with open(os.path.join(file_dir, "txt_pages", txt)) as inputTxt:
                        for line in inputTxt:
                            ouputTxt.write(line)
                        ouputTxt.write("\n"*3)
    print("txt_volumes downloaded")
    print("\n")


getMagazine()
