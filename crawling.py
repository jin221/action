import requests
from bs4 import BeautifulSoup


def parsing_beautifulsoup(url):
    
    data = requests.get(url)

    html = data.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def extract_book_data(soup):
    """
    BeautifulSoup Object에서 book data를 추출하는 함수
    :param soup: BeautifulSoup soup Object
    :return: contents(str)
    """

    upload_contents = ''
    new_books = soup.select(".goodsTxtInfo")
    url_prefix = "https://www.barnesandnoble.com/"

    for new_book in new_books:
        book_name = new_book.select("a")[0].text
        url_suffix = new_book.select("a")[1].attrs['href']
        url = url_prefix + url_suffix
        price = new_book.select(".priceB")[0].text

        content = f"<a href={url}>" + book_name + "</a>" + ", " + price + "<br/>\n"
        upload_contents += content

    return upload_contents