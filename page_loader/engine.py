import logging
import os
import shutil
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from page_loader.tools import get_loglevel, mk_dir, save_page

HTML_RESOURCES = {"img": "src", "script": "src", "link": "href"}


def download(url, save_path, loglevel="INFO"):
    logging.basicConfig(
        format="%(asctime)s - %(message)s", level=get_loglevel(loglevel)
    )
    logging.info(f"Start with {url} to save in {save_path}")
    url_values = prepare_url(url, save_path)
    html_doc = download_page(url)
    soup = BeautifulSoup(html_doc, "html.parser")
    all_html_resources = []
    for tag, attr in HTML_RESOURCES.items():
        new_soup, resources = change_html(tag, attr, soup, url_values)
        all_html_resources.extend(resources)
    download_resources(all_html_resources)
    html_doc_new = new_soup.prettify()
    save_page(html_doc_new, url_values["url_save_path"])
    logging.info(f"Finish with {url} to save in {save_path}")
    return url_values["url_save_path"]


def prepare_url(url, save_path):
    url_parse_result = urlparse(url)
    url_domain_changed = url_parse_result.netloc.replace(".", "-")
    url_path_changed = url_parse_result.path.replace("/", "-")
    if url_path_changed == "-":
        url_path_changed = ""
    url_file_name = url_domain_changed + url_path_changed
    url_save_path = os.path.join(save_path, url_file_name + ".html")
    url_save_dir_name = os.path.join(save_path, f"{url_file_name}_files")
    mk_dir(url_save_dir_name)
    return {
        "url_parse_result": url_parse_result,
        "url_domain_changed": url_domain_changed,
        "url_path_changed": url_path_changed,
        "url_file_name": url_file_name,
        "url_save_path": url_save_path,
        "url": url,
        "url_save_dir_name": url_save_dir_name,
    }


def change_html(tag, attr, soup, url_values):
    resources = []
    for el in soup.find_all(tag):
        el_src = el.get(attr)
        if is_same_domain(el_src, url_values["url"]):
            new_el_src = str(urlparse(el_src).path)
            new_el_src = new_el_src.replace("/", "-").replace("'", "")
            new_el_src = url_values["url_domain_changed"] + new_el_src
            if not new_el_src.endswith((".css", ".js", ".png")):
                new_el_src = f"{new_el_src}.html"
            new_el_src_with_dir = (
                f"{url_values['url_save_dir_name']}/{new_el_src}"
            )
            resources.append(
                {
                    "file_url": el_src,
                    "save_path": url_values["url_save_dir_name"],
                    "file_name": new_el_src_with_dir,
                    "page_url": url_values["url"],
                }
            )
            el[attr] = f"{url_values['url_file_name']}_files/{new_el_src}"
    return soup, resources


def is_same_domain(file_url, url):
    if not urlparse(file_url).netloc:
        return True
    if urlparse(file_url).netloc == urlparse(url).netloc:
        return True


def download_file_from_url(file_url, save_path, file_name, page_url):
    save_path_with_file_name = os.path.join(save_path, file_name)
    file_url_parse = urlparse(file_url)
    if not file_url_parse.netloc:
        file_url = urljoin(page_url, file_url)
    if not os.path.exists(save_path_with_file_name):
        r = requests.get(file_url, stream=True)
        print(save_path_with_file_name)
        if r.status_code != "404":
            with open(save_path_with_file_name, "wb") as file:
                if file_url.endswith((".css", ".js", ".html")):
                    file.write(r.content)
                else:
                    shutil.copyfileobj(r.raw, file)
                logging.info("save file %s" % save_path_with_file_name)
        else:
            logging.info("status code of %s is 404" % file_url)
    else:
        logging.info("%s is already exists" % save_path_with_file_name)


def download_page(url):
    logging.debug("download page %s" % url)
    r = requests.get(url)
    return r.text


def download_resources(resources):
    for resource in resources:
        download_file_from_url(**resource)
