import os
import tempfile

import requests_mock
from page_loader.page_loader import download

from tests.fixtures.html_response import original_reponse, changed_html

TEST_URL = "https://ru.hexlet.io/courses"
TEST_URL_FILE_NAME = "ru-hexlet-io-courses.html"
TEST_URL_DIR_NAME = "ru-hexlet-io-courses_files"
TEST_URL_PNG_FILE_NAME = "ru-hexlet-io-assets-professions-nodejs.png"
TEST_URL_JS_FILE_NAME = "ru-hexlet-io-packs-js-runtime.js"
TEST_URL_CSS_FILE_NAME = "ru-hexlet-io-assets-application.css"
TEST_FULL_URL_PNG_FILE = "https://ru.hexlet.io/assets/professions/nodejs.png"
TEST_FULL_URL_JS_FILE = "https://ru.hexlet.io/packs/js/runtime.js"
TEST_FULL_URL_CSS_FILE = "https://ru.hexlet.io/assets/application.css"


def test_page_loader():
    with requests_mock.Mocker() as m, tempfile.TemporaryDirectory() as tmpdirname:
        m.get(TEST_URL, text=original_reponse)
        m.get(TEST_FULL_URL_PNG_FILE, text="1")
        m.get(TEST_FULL_URL_JS_FILE, text="1")
        m.get(TEST_FULL_URL_CSS_FILE, text="1")
        file_path = download(TEST_URL, tmpdirname)
        assert file_path == os.path.join(tmpdirname, TEST_URL_FILE_NAME)
        assert open(file_path, "r").read() == changed_html


def test_page_loader_change_original_html():
    with requests_mock.Mocker() as m, tempfile.TemporaryDirectory() as tmpdirname:
        m.get(TEST_URL, text=original_reponse)
        m.get(TEST_FULL_URL_PNG_FILE, text="1")
        m.get(TEST_FULL_URL_JS_FILE, text="1")
        m.get(TEST_FULL_URL_CSS_FILE, text="1")
        file_path = download(TEST_URL, tmpdirname)
        response = open(file_path, "r").read()
        assert response == changed_html


def test_page_loader_download_files():
    with requests_mock.Mocker() as m, tempfile.TemporaryDirectory() as tmpdirname:
        m.get(TEST_URL, text=original_reponse)
        m.get(TEST_FULL_URL_PNG_FILE, text="1")
        m.get(TEST_FULL_URL_JS_FILE, text="1")
        m.get(TEST_FULL_URL_CSS_FILE, text="1")
        file_path = download(TEST_URL, tmpdirname)
        assert True == os.path.exists(
            os.path.join(tmpdirname, TEST_URL_DIR_NAME)
        )
        assert True == os.path.exists(
            os.path.join(tmpdirname, TEST_URL_DIR_NAME, TEST_URL_PNG_FILE_NAME)
        )
        assert True == os.path.exists(
            os.path.join(tmpdirname, TEST_URL_DIR_NAME, TEST_URL_JS_FILE_NAME)
        )
        assert True == os.path.exists(
            os.path.join(tmpdirname, TEST_URL_DIR_NAME, TEST_URL_CSS_FILE_NAME)
        )
