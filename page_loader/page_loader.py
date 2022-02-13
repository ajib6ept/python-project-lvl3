import os
import shutil
import requests

from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup

HTML_RESOURCES = {"img": "src", "script": "src", "link": "href"}


def download(url, save_path):
    url_values = prepare_url(url, save_path)
    html_doc = download_page(url)
    soup = BeautifulSoup(html_doc, "html.parser")
    for tag, attr in HTML_RESOURCES.items():
        new_soup = change_html(tag, attr, soup, url_values)
    html_doc_new = new_soup.prettify()
    save_page(html_doc_new, url_values["url_save_path"])
    return url_values["url_save_path"]


def prepare_url(url, save_path):
    url_parse_result = urlparse(url)
    url_domain_changed = url_parse_result.netloc.replace(".", "-")
    url_path_changed = url_parse_result.path.replace("/", "-")
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
    for el in soup.find_all(tag):
        el_src = el.get(attr)
        if is_same_domain(el_src, url_values["url"]):
            new_el_src = urlparse(el_src).path
            new_el_src = new_el_src.replace("/", "-")
            new_el_src = url_values["url_domain_changed"] + new_el_src
            if not new_el_src.endswith((".css", ".js", ".png")):
                new_el_src = f"{new_el_src}.html"
            new_el_src_with_dir = (
                f"{url_values['url_save_dir_name']}/{new_el_src}"
            )
            download_file_from_url(
                el_src,
                url_values["url_save_dir_name"],
                new_el_src_with_dir,
                page_url=url_values["url"],
            )
            el[attr] = f"{url_values['url_file_name']}_files/{new_el_src}"
    return soup


def is_same_domain(file_url, url):
    if not urlparse(file_url).netloc:
        return True
    if urlparse(file_url).netloc == urlparse(url).netloc:
        return True


def mk_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def save_page(html, path):
    with open(path, "w") as text_file:
        text_file.write(html)


def download_file_from_url(file_url, save_path, file_name, page_url):
    save_path_with_file_name = os.path.join(save_path, file_name)
    file_url_parse = urlparse(file_url)
    if not file_url_parse.netloc:
        file_url = urljoin(page_url, file_url)
    if not os.path.exists(save_path_with_file_name):
        r = requests.get(file_url, stream=True)
        if r.status_code != "404":
            with open(save_path_with_file_name, "wb") as file:
                if file_url.endswith((".css", ".js", ".html")):
                    file.write(r.content)
                else:
                    shutil.copyfileobj(r.raw, file)


def download_page(url):
    r = requests.get(url)
    return r.text
