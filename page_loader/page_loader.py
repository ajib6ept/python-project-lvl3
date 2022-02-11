import os
import requests


def download(url, save_path):
    url_file_name = url.split("://")[1].replace(".", "-").replace("/", "-")
    url_save_path = os.path.join(save_path, url_file_name + ".html")
    r = requests.get(url)
    with open(url_save_path, "w") as file:
        file.write(r.text)
    return url_save_path
