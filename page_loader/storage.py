import logging
import os

from page_loader.exceptions import StorageErrorException

TEXT_FILE_EXTENSION = (".css", ".js", ".html")


def save_file(file_obj, source_new_filename, save_path_dir, file_type=".html"):
    full_save_path = os.path.join(save_path_dir, source_new_filename)
    with open(full_save_path, "wb") as file:
        if file_obj.url.endswith(TEXT_FILE_EXTENSION):
            file.write(file_obj.content)
        else:
            for chunk in file_obj.iter_content(chunk_size=128):
                file.write(chunk)
        logging.debug(f"Saved file into {full_save_path}")


def mk_dir(dir_path):
    if not os.path.exists(dir_path):
        parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
        if os.path.exists(parent_path):
            os.mkdir(dir_path)
            logging.debug(f"Successfully created directory {dir_path}")
        else:
            raise StorageErrorException
    else:
        logging.debug(f"{dir_path} is already exists")


def save_page(html, path):
    with open(path, "w") as text_file:
        text_file.write(html)
    logging.debug(f"Successfully saved page in {path}")
