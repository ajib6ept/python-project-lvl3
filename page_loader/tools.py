import os


def mk_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def save_page(html, path):
    with open(path, "w") as text_file:
        text_file.write(html)
