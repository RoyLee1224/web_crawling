# Download Travel-related data from Korean websites

This is a Python script that downloads data related to travel in Taiwan. The script scrapes text data from various Korean websites, including:

- [Taiwan the heart of Asia(대만관광청)](https://www.taiwantour.or.kr)
- [Taiwan Visitor Association(타이완 관광협회)](http://www.tva.org.tw)

## Prerequisite

This script uses Python3. Before running this script, please make sure you have the following libraries installed:

- requests
- beautifulsoup4
- PyPDF2
- pdfminer

If you have not installed these libraries, please install them with the following command:

`!pip install requests beautifulsoup4 PyPDF2 pdfminer`

## How to use

1. Clone or download the repository to your computer.
2. Navigate to the folder where you downloaded the repository.
3. Open main.py with any Python IDE.
4. Run the script.
5. Quarterly magazine PDF files will be downloaded in the pdf directory.
6. Quarterly magazine txt files will be downloaded in the txt directory.

## Description

- `thema.txt` - **Theme Travel** from [테마여행](https://www.taiwantour.or.kr/bbs/board.php?bo_table=m08_01&sca=%ED%9C%B4%EC%96%91).
- `pro.txt` - **Professional travel** from [프로대만족](https://www.taiwantour.or.kr/bbs/board.php?bo_table=m03).
- `place.txt` - **Taiwan's attractions** from [대만 명소](https://www.taiwantour.or.kr/bbs/board.php?bo_table=m03).
- `Quarterly magazine PDFs` - **Vol. 44~46 quarterly magazine PDF(대만관광격월간)** from [TVA website](http://www.tva.org.tw).

## Note

- If you encounter any error or the PDF files are not downloading, please check your internet connection and try again.
- Please change the `file_dir` variale to the directory where you want to save the download files.
- There are `20` pages in the **Professional travel(프로대만족)** and `8` pages in **Taiwan's attractions(대만 명소)** currently. Please adjust the number of pages in the `get_pro_page` and `get_place_page` functions if there's new article in those pages.
