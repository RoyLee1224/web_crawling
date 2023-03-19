# Download Travel-related data from Korean websites

This is a Python script that downloads data related to travel in Taiwan. The script scrapes text data from various Korean websites, including:

- [Taiwan the heart of Asia(대만관광청)](https://www.taiwantour.or.kr)
- [Taiwan Visitor Association(타이완 관광협회)](http://www.tva.org.tw)

## Prerequisite

This script uses Python3. Before running this script, please make sure you have the following libraries installed:

- requests
- beautifulsoup4
- PyPDF4
- pdfminer
- pdfplumber

If you have not installed these libraries, please install them with the following command:

`!pip install requests beautifulsoup4 PyPDF4 pdfminer pdfplumber`

## How to use

1. Clone or download the repository to your computer.
2. Open main.py with any Python IDE.
3. Run the script.
4. Magazine PDF will be downloaded in the pdf directory.
5. Magazine txt will be downloaded in two versions.
   1. `txt_pages`: Separated by pages(ex: v01-p1.txt)
   2. `txt_volumes`: Separated by volumes(ex: v01.txt)

## Description

- `thema.txt` - **Theme Travel** from [테마여행](https://www.taiwantour.or.kr/bbs/board.php?bo_table=m08_01&sca=%ED%9C%B4%EC%96%91).
- `pro.txt` - **Professional travel** from [프로대만족](https://www.taiwantour.or.kr/bbs/board.php?bo_table=m03).
- `place.txt` - **Taiwan's attractions** from [대만 명소](https://www.taiwantour.or.kr/bbs/board.php?bo_table=m03).
- `Quarterly magazine PDFs` - **Vol. 1~47 quarterly magazine PDF(대만관광격월간)** from [TVA website](http://www.tva.org.tw).

## Note

- Currently, there are `20` pages in **Professional travel(프로대만족)** and `8` pages in **Taiwan's attractions(대만 명소)** . If there're new articles in those pages, adjust the numbers in `get_pro_page` and `get_place_page` functions in **taiwanTour.py** .
- Currently, there are `47` volumes of magazines. If there's new article, adjust the number of `getMagazine` function in **main.py** .
- The usefulness of each magazin page depends on the following conditions:
  - If the number of characters exceeds a certain number, it will be judged as useful content. (Based on experiment, using 140 characters as a criterion provides better quality)
  - If the content includes key words such as **'도표', "통계", "Content", "fax"**, the page will be skipped. (To avoid extracting tables, contacts, and content tables)
