import logging
import os

import requests
from progress.bar import Bar

from page_loader.html import parsing_page
from page_loader.logger import create_logger
from page_loader.resources import change_resource_link
from page_loader.storage import mk_dir, save_file, save_page
from page_loader.url import (create_full_source_url, get_source_new_filename,
                             normalize_url_name)

DEFAULT_TIMEOUT = 1


def download(url, save_path, loglevel="INFO"):
    create_logger(loglevel)
    logging.debug(f"Start with {url} to save in {save_path}")
    url_file_name = normalize_url_name(url)
    url_save_path = os.path.join(save_path, url_file_name + ".html")
    url_save_dir_name = os.path.join(save_path, f"{url_file_name}_files")

    html_doc = download_page(url)
    soup, html_resources = parsing_page(html_doc, url)
    if html_resources:
        download_resources(html_resources, url, url_save_dir_name)
    save_page(soup.prettify(), url_save_path)
    logging.info(f"Page was successfully downloaded into '{url_save_path}'")
    return url_save_path


def download_file_from_url(file_url):
    r = requests.get(file_url, stream=True, timeout=DEFAULT_TIMEOUT)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        logging.info(f"Status code of {file_url} is {r.status_code}")
    return r


def download_page(url):
    r = requests.get(url, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    logging.debug(f"Downloaded page {url}")
    return r.text


def download_resources(resources, original_url, save_dir_path):
    mk_dir(save_dir_path)
    resources = remove_double_from_the_list(resources)
    logging.debug(f"Found {len(resources)} unique resources to download")
    with Bar("Downloading resources", max=len(resources)) as bar:
        for resource in resources:
            soup_item, source_link = resource
            resource_link = create_full_source_url(source_link, original_url)
            source_new_filename = get_source_new_filename(
                source_link, original_url
            )
            file_obj = download_file_from_url(resource_link)
            save_file(file_obj, source_new_filename, save_dir_path)
            change_resource_link(soup_item, source_new_filename, save_dir_path)
            bar.next()


def remove_double_from_the_list(items):
    """
    >>> remove_double_from_the_list([[1,2], [1,2], [3,4]])
    [[1, 2], [3, 4]]
    """
    new_item = []
    for item in items:
        if item not in new_item:
            new_item.append(item)
    return new_item
