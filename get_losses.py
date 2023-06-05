import cloudscraper
from bs4 import BeautifulSoup
import re


base_url = "https://www.mil.gov.ua/en/"
news_url = base_url + "news"


def parse_input(input_string):
    output = {}
    pattern = r"([\w\s\/-]+) [–‒] (\d+) \([-+]?(\d+)\)"

    matches = re.findall(pattern, input_string)
    for match in matches:
        key = match[0].strip()
        value = int(match[1])
        change = int(match[2])

        output[key] = {"total": value, "change": change}

    return output


# scrape news page

scraper = cloudscraper.create_scraper()
content = scraper.get(news_url).text
soup = BeautifulSoup(content, "html.parser")

# first combat loss in results
target_url = base_url + soup.find("a", href=re.compile("the-total-combat"))["href"]
print(target_url)

# get data
scraper = cloudscraper.create_scraper()
content = scraper.get(target_url).text
soup = BeautifulSoup(content, "html.parser")
target_paragraph = str(soup.find("p"))

# parse
losses = parse_input(target_paragraph)
print(losses)
