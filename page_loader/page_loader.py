import os
import shutil
import requests

from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup


def download(url, save_path):
    url_parse_result = urlparse(url)
    url_domain_changed = url_parse_result.netloc.replace(".", "-")
    url_path_changed = url_parse_result.path.replace("/", "-")
    url_file_name = url_domain_changed + url_path_changed
    url_save_path = os.path.join(save_path, url_file_name + ".html")
    url_save_dir_name = os.path.join(save_path, f"{url_file_name}_files")
    mk_dir(url_save_dir_name)
    html_doc = download_page(url)
    soup = BeautifulSoup(html_doc, "html.parser")
    for link in soup.find_all("img"):
        link_src = link.get("src")
        if is_same_domain(link_src):
            new_link_src = urlparse(link_src).path
            new_link_src = (
                f"{url_domain_changed}{new_link_src.replace('/', '-')}"
            )
            new_link_src_with_dir = f"{url_save_dir_name}/{new_link_src}"
            download_file_from_url(
                link_src,
                url_save_dir_name,
                new_link_src_with_dir,
                page_url=url,
            )
            link["src"] = f"{url_file_name}_files/{new_link_src}"
    html_doc_new = soup.prettify()
    save_page(html_doc_new, url_save_path)
    return url_save_path


def is_same_domain(file_url):
    if not urlparse(file_url).netloc:
        return True


def mk_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def save_page(html, path):
    print(html)
    with open(path, "w") as text_file:
        text_file.write(html)


def download_file_from_url(file_url, save_path, file_name, page_url):
    save_path_with_file_name = os.path.join(save_path, file_name)
    file_url_parse = urlparse(file_url)
    if not file_url_parse.netloc:
        file_url = urljoin(page_url, file_url)
    if not os.path.exists(save_path_with_file_name):
        r = requests.get(file_url, stream=True)
        with open(save_path_with_file_name, "wb") as file:
            shutil.copyfileobj(r.raw, file)


def download_page(url):
    r = requests.get(url)
    return r.text
