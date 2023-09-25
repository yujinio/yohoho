import re

import httpx
from bs4 import BeautifulSoup
from lxml import html

from ..data_types import SearchOutput


async def search(query: str) -> list[SearchOutput]:
    url = "http://www.kinopoisk.ru/index.php"
    params = {"kp_query": query}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, follow_redirects=True)

    response.raise_for_status()

    content = response.content.decode("utf-8")
    html_content = html.fromstring(content)

    if response.history and "/film/" in response.url.path:
        url_xpath = './/meta[@property="og:url"]/@content'
        title_xpath = ".//h1/span/text()"

        url_elements = html_content.xpath(url_xpath)
        url_value = " ".join(url_elements)
        kinopoisk_id = url_value.split("/")[-2].split("-")[-1]

        title_elements = html_content.xpath(title_xpath)
        title_value = " ".join(title_elements)

        return [SearchOutput(movie_id=int(kinopoisk_id), movie_title=title_value)]

    if content.find('<h2 class="textorangebig" style="font:100 18px">') != -1:
        return []

    content_from = content.find('<div class="search_results">')
    content_to = content.find('<div style="height: 40px"></div>')
    content_results = content[content_from:content_to]

    if not content_results:
        return []

    soup_results = BeautifulSoup(content_results, "html.parser")
    results = soup_results.findAll("div", attrs={"class": re.compile("element")})
    if not results:
        return []

    outputs = []
    for result in results:
        result_content = html.fromstring(str(result))

        url_xpath = './/p[@class="name"]/a/@data-url'
        title_xpath = './/p[@class="name"]/a/text()'

        url_elements = result_content.xpath(url_xpath)
        url_value = " ".join(url_elements)

        if "/film/" not in url_value:
            continue

        kinopoisk_id = url_value.split("/")[2]

        title_elements = result_content.xpath(title_xpath)
        title_value = " ".join(title_elements)

        outputs.append(SearchOutput(movie_id=int(kinopoisk_id), movie_title=title_value))

    return outputs
