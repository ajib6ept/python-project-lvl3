import os
import tempfile

import requests_mock
from page_loader.page_loader import download

TEST_URL = "https://ru.hexlet.io/courses"
TEST_URL_FILE_NAME = "ru-hexlet-io-courses.html"


def test_page_loader():
    with requests_mock.Mocker() as m, tempfile.TemporaryDirectory() as tmpdirname:
        m.get(TEST_URL, text="resp")
        file_path = download(TEST_URL, tmpdirname)
        assert file_path == os.path.join(tmpdirname, TEST_URL_FILE_NAME)
        response = open(file_path, "r").read()
        assert response == "resp"
