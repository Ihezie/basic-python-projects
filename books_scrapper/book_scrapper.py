import pprint
import random
from bs4 import BeautifulSoup
import requests

category = input("Please input category: ")
rating = input("Please input rating: ")

baseUrl = "https://books.toscrape.com/"
``

def get_categories():
    categories = {"all": "catalogue/category/books_1/index.html"}
    res = requests.get("https://books.toscrape.com/index.html")
    home_page = res.text
    soup = BeautifulSoup(home_page, "html.parser")

    categories_element = soup.select(".side_categories .nav-list li ul li")

    for item in categories_element:
        genre = item.find("a").getText(strip=True).lower()
        categories[genre] = item.find("a").get("href", None)

    return categories


categories = get_categories()


def get_books(category="romance", rating=None):
    category_url = baseUrl + categories[category]
    res = requests.get(category_url)
    soup = BeautifulSoup(res.text, "html.parser")
    book_data = soup.select("section .row li")
    if len(soup.select(".pager")) > 0:
        page_2_url = category_url.replace("index", "page-2")
        res_2 = requests.get(page_2_url)
        soup_2 = BeautifulSoup(res_2.text, "html.parser")
        extra_book_data = soup_2.select("section .row li")
        book_data.extend(extra_book_data)

    result = sorted(
        process_books(book_data, rating),
        key=lambda x: float(x["price"][1:]),
        reverse=True,
    )
    return result


def process_books(book_data, rating):
    books = []
    if rating:
        digit_to_words = {
            "1": "One",
            "2": "Two",
            "3": "Three",
            "4": "Four",
            "5": "Five",
        }
        counter = 0
        while counter < 10:
            stars = (
                (book := book_data[counter]).select(".star-rating")[0].get("class")[1]
            )
            if digit_to_words[rating] == stars:
                books.append(format_book(book))
            counter += 1
    else:
        for i in range(10):
            book = random.choice(book_data)
            formatted_book = format_book(book)
            books.append(formatted_book)
    return books


def get_description(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    description = soup.select(".product_page > p")
    return description


def format_book(book):
    words_to_figures = {
        "One": "1",
        "Two": "2",
        "Three": "3",
        "Four": "4",
        "Five": "5",
    }
    title = book.select("h3 a")[0].get_text()
    price = book.select(".price_color")[0].get_text()
    stars = words_to_figures[book.select(".star-rating")[0].get("class")[1]]
    book_url = (
        baseUrl
        + "catalogue"
        + book.select("h3 a")[0].get("href").replace("../../..", "")
    )
    book_dict = {
        "title": title,
        "price": price[1:],
        "rating": stars + " star(s)",
        # "description": description,
        "link": book_url,
    }
    return book_dict


pprint.pprint(get_books(category, rating))
