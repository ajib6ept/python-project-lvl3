import logging
import os
import shutil

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar

from page_loader.logger import create_logger
from page_loader.resources import (change_resource_link,
                                   get_link_from_attributes)
from page_loader.tools import mk_dir, remove_double_from_the_list, save_page
from page_loader.url_utility import (create_full_source_url,
                                     create_normalize_url_name,
                                     create_source_new_filename,
                                     is_same_domain)

HTML_RESOURCE_TAGS = ("img", "script", "link")
DEFAULT_TIMEOUT = 1
TEXT_FILE_EXTENSION = (".css", ".js", ".html")


def download(url, save_path, loglevel="INFO"):
    create_logger(loglevel)
    logging.debug(f"Start with {url} to save in {save_path}")

    url_file_name = create_normalize_url_name(url)
    url_save_path = os.path.join(save_path, url_file_name + ".html")
    url_save_dir_name = os.path.join(save_path, f"{url_file_name}_files")

    html_doc = download_page(url)
    soup = BeautifulSoup(html_doc, "html.parser")
    html_resources = []

    for element in soup.find_all(HTML_RESOURCE_TAGS):
        element_src = get_link_from_attributes(element.name, element.attrs)
        if element_src and is_same_domain(element_src, url):
            html_resources.append([element, element_src])
    if html_resources:
        mk_dir(url_save_dir_name)
        html_resources = remove_double_from_the_list(html_resources)
        logging.debug(
            f"Found {len(html_resources)} unique resources to download"
        )
        download_resources(html_resources, url, url_save_dir_name)
    save_page(soup.prettify(), url_save_path)
    logging.info(f"Page was successfully downloaded into '{url_save_path}'")
    return url_save_path


def save_file(file_obj, source_new_filename, save_path_dir):
    full_save_path = os.path.join(save_path_dir, source_new_filename)
    with open(full_save_path, "wb") as file:
        if file_obj.url.endswith(TEXT_FILE_EXTENSION):
            file.write(file_obj.content)
        else:
            shutil.copyfileobj(file_obj.raw, file)
        logging.debug(f"Saved file into {full_save_path}")


def download_file_from_url(file_url):
    r = requests.get(file_url, stream=True, timeout=DEFAULT_TIMEOUT)
    if r.status_code <= 400:  # If the status code is not an error
        return r
    else:
        logging.info(f"Status code of {file_url} is {r.status_code}")


def download_page(url):
    r = requests.get(url, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    logging.debug(f"Downloaded page {url}")
    return r.text


def download_resources(resources, original_url, save_dir_path):
    with Bar("Downloading resources", max=len(resources)) as bar:
        for resource in resources:
            soup_item, source_link = resource
            resource_link = create_full_source_url(source_link, original_url)
            source_new_filename = create_source_new_filename(
                source_link, original_url
            )
            file_obj = download_file_from_url(resource_link)
            save_file(file_obj, source_new_filename, save_dir_path)
            change_resource_link(soup_item, source_new_filename, save_dir_path)
            bar.next()
