import logging
import os
import shutil
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar

from page_loader.exceptions import BadStatusCodeException
from page_loader.logger import create_logger
from page_loader.tools import mk_dir, remove_double_from_the_list, save_page

HTML_RESOURCES = {"img": "src", "script": "src", "link": "href"}
ERROR_STATUS_CODE = (404, 500)
TEXT_FILE_EXTENSION = (".css", ".js", ".html")


def download(url, save_path, loglevel="INFO"):
    create_logger(loglevel)
    logging.debug(f"Start with {url} to save in {save_path}")

    # create the necessary variables
    url_domain_changed = urlparse(url).netloc.replace(".", "-")
    url_path_changed = urlparse(url).path.replace("/", "-")
    if url_path_changed == "-":
        url_path_changed = ""
    url_file_name = url_domain_changed + url_path_changed
    url_save_path = os.path.join(save_path, url_file_name + ".html")
    url_save_dir_name = os.path.join(save_path, f"{url_file_name}_files")

    html_doc = download_page(url)
    soup = BeautifulSoup(html_doc, "html.parser")
    all_html_resources = []
    for tag, attr in HTML_RESOURCES.items():
        new_soup, resources = change_html(
            tag,
            attr,
            soup,
            url,
            url_save_dir_name,
            url_domain_changed,
            url_file_name,
        )
        all_html_resources.extend(resources)
    all_html_resources = remove_double_from_the_list(all_html_resources)
    logging.debug(
        f"Found {len(all_html_resources)} unique resources to download"
    )
    mk_dir(url_save_dir_name)
    download_resources(all_html_resources)
    html_doc_new = new_soup.prettify()
    save_page(html_doc_new, url_save_path)
    logging.info(f"Page was successfully downloaded into '{url_save_path}'")
    return url_save_path


def change_html(
    tag,
    attr,
    soup,
    url,
    url_save_dir_name,
    url_domain_changed,
    url_file_name,
):
    resources = []
    for el in soup.find_all(tag):
        el_src = el.get(attr)
        if el_src is not None and is_same_domain(el_src, url):
            new_el_src = str(urlparse(el_src).path)
            new_el_src = new_el_src.replace("/", "-").replace("'", "")
            new_el_src = url_domain_changed + new_el_src
            if "." not in new_el_src:
                new_el_src = f"{new_el_src}.html"
            new_el_src_with_dir = f"{url_save_dir_name}/{new_el_src}"
            resources.append(
                {
                    "file_url": el_src,
                    "save_file_path": new_el_src_with_dir,
                    "page_url": url,
                }
            )
            el[attr] = f"{url_file_name}_files/{new_el_src}"
    return soup, resources


def is_same_domain(file_url, url):
    if not urlparse(file_url).netloc:
        return True
    if urlparse(file_url).netloc == urlparse(url).netloc:
        return True


def download_file_from_url(file_url, save_file_path, page_url):
    file_url_parse = urlparse(file_url)
    if not file_url_parse.netloc:
        file_url = urljoin(page_url, file_url)
    if os.path.exists(save_file_path):
        logging.debug(f"{save_file_path} is already exists")
    r = requests.get(file_url, stream=True)
    if r.status_code not in ERROR_STATUS_CODE:
        with open(save_file_path, "wb") as file:
            if file_url.endswith(TEXT_FILE_EXTENSION):
                file.write(r.content)
            else:
                shutil.copyfileobj(r.raw, file)
            logging.debug(f"Saved file into {save_file_path}")
    else:
        logging.info(f"Status code of {file_url} is {r.status_code}")


def download_page(url):
    r = requests.get(url, timeout=1)
    if r.status_code in ERROR_STATUS_CODE:
        raise BadStatusCodeException(
            f"Error {r.status_code} when loading the page"
        )
    logging.debug(f"Downloaded page {url}")
    return r.text


def download_resources(resources):
    with Bar("Downloading resources", max=len(resources)) as bar:
        for resource in resources:
            download_file_from_url(**resource)
            bar.next()
