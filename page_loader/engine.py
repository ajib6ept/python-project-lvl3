import logging
import os

import requests
from progress.bar import Bar

from page_loader.logger import create_logger
from page_loader.resources import (change_resources_link, parse_page,
                                   remove_double_from_the_list)
from page_loader.storage import mk_dir, save_file
from page_loader.url import (get_abs_source_url, get_source_filename,
                             normalize_name)

DEFAULT_TIMEOUT = 1


def download(url, save_path, loglevel="INFO"):
    create_logger(loglevel)
    logging.debug(f"Start with {url} to save in {save_path}")

    url_save_path = os.path.join(save_path, f"{normalize_name(url)}.html")
    url_save_dir_name = os.path.join(save_path, f"{normalize_name(url)}_files")

    html_doc = download_page(url)
    new_html_doc, html_resources = parse_page(html_doc, url)

    if html_resources:
        mk_dir(url_save_dir_name)
        html_resources = remove_double_from_the_list(html_resources)
        logging.debug(
            f"Found {len(html_resources)} unique resources to download"
        )

        bar = Bar("Downloading resources", max=len(html_resources))
        for resource in html_resources:
            html_obj, source_link = resource
            source_new_filename = get_source_filename(source_link, url)
            try:
                download_resource(
                    source_link,
                    url,
                    source_new_filename,
                    url_save_dir_name,
                )
            except Exception:
                logging.warning(
                    f"Failed to download and save the resource {source_link}"
                )
            else:
                change_resources_link(
                    html_obj, source_new_filename, url_save_dir_name
                )
            bar.next()
        bar.finish()

    save_file(new_html_doc.prettify(), url_save_path, "")
    logging.info(f"Page was successfully downloaded into '{url_save_path}'")
    return url_save_path


def download_file_from_url(file_url):
    r = requests.get(file_url, stream=True, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    logging.debug(f"Downloaded file {file_url}")
    return r


def download_page(url):
    r = requests.get(url, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    logging.debug(f"Downloaded page {url}")
    return r.text


def download_resource(source_link, url, source_new_filename, save_dir_path):
    resource_link = get_abs_source_url(source_link, url)
    file_obj = download_file_from_url(resource_link)
    save_file(file_obj, source_new_filename, save_dir_path)
