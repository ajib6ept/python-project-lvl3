from bs4 import BeautifulSoup

from page_loader.resources import get_link_from_attributes
from page_loader.url import is_same_domain

HTML_RESOURCE_TAGS = ("img", "script", "link")


def parsing_page(html_doc, url):
    soup = BeautifulSoup(html_doc, "html.parser")
    html_resources = []

    for element in soup.find_all(HTML_RESOURCE_TAGS):
        element_src = get_link_from_attributes(element.name, element.attrs)
        if element_src and is_same_domain(element_src, url):
            html_resources.append([element, element_src])
    return soup, html_resources
