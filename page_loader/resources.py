import os

from bs4 import BeautifulSoup

from page_loader.url import is_same_domain

HTML_RESOURCES = {"img": "src", "script": "src", "link": "href"}
HTML_RESOURCE_TAGS = ("img", "script", "link")


def parse_page(html_doc, url):
    soup = BeautifulSoup(html_doc, "html.parser")
    html_resources = []

    for element in soup.find_all(HTML_RESOURCE_TAGS):
        element_src = get_link_from_attributes(element.name, element.attrs)
        if element_src and is_same_domain(element_src, url):
            html_resources.append((element, element_src))
    return soup, html_resources


def get_link_from_attributes(tag_name, attrs):
    """
    getting the source from attributes

    >>> get_link_from_attributes('link', {'href': '/courses', 'rel': ['cano']})
    '/courses'
    >>> get_link_from_attributes('script', {'src': 'https://js.stipe.com/v3/'})
    'https://js.stipe.com/v3/'
    >>> get_link_from_attributes('img', {'src': '/nodejs.png', 'alt': 'И'})
    '/nodejs.png'
    >>> get_link_from_attributes('link', {'src': '/courses', 'rel': ['cano']})
    ''
    """
    if tag_name in HTML_RESOURCES.keys():
        return attrs.get(HTML_RESOURCES[tag_name], "")
    return ""


def change_resources_link(soup_item, source_link, save_dir_path):
    """
    change the link to the resource in the soup
    """
    base_name = os.path.basename(save_dir_path)
    soup_item.attrs[HTML_RESOURCES[soup_item.name]] = os.path.join(
        base_name, source_link
    )


def remove_double_from_the_list(items):
    """
    >>> remove_double_from_the_list([(1,2), (1,2), (3,4)])
    [(1, 2), (3, 4)]
    """
    return list(set(items))
