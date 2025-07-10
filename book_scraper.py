import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
import re  # Add this for extracting price safely

def scrape_books_to_inr():
    url = 'https://books.toscrape.com/'
    exchange_rate = 105  # 1 GBP ≈ ₹105

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        if not books:
            print("❌ No books found.")
            return

        console = Console()
        table = Table(title="📚 Top 10 Books - Price Converted to ₹ INR")

        table.add_column("S.No", style="cyan", justify="center")
        table.add_column("Title", style="bold magenta")
        table.add_column("Price (₹)", style="green")
        table.add_column("Availability", style="yellow")

        for i, book in enumerate(books[:10], 1):
            title = book.h3.a['title']
            price_text = book.find('p', class_='price_color').text  # e.g., '£51.77'
            price_number = re.findall(r"\d+\.\d+", price_text)
            price_value = float(price_number[0]) if price_number else 0.0
            price_inr = f"₹{int(price_value * exchange_rate)}"

            availability = book.find('p', class_='instock availability').text.strip()
            table.add_row(str(i), title, price_inr, availability)

        console.print(table)

    except requests.exceptions.RequestException as e:
        print(f"🌐 Network Error: {e}")
    except Exception as e:
        print(f"⚠️ Error: {e}")

scrape_books_to_inr()
