import tempfile
from pathlib import Path

import pytest
import requests

from page_loader.engine import download
from page_loader.exceptions import StorageErrorException

TEST_URL = "https://ru.hexlet.io/courses"
TEST_URL_FILE_NAME = "ru-hexlet-io-courses.html"
TEST_URL_DIR_NAME = "ru-hexlet-io-courses_files"
TEST_URL_PNG_FILE_NAME = "ru-hexlet-io-assets-professions-nodejs.png"
TEST_URL_JS_FILE_NAME = "ru-hexlet-io-packs-js-runtime.js"
TEST_URL_CSS_FILE_NAME = "ru-hexlet-io-assets-application.css"
TEST_FULL_URL_PNG_FILE = "https://ru.hexlet.io/assets/professions/nodejs.png"
TEST_FULL_URL_JS_FILE = "https://ru.hexlet.io/packs/js/runtime.js"
TEST_FULL_URL_CSS_FILE = "https://ru.hexlet.io/assets/application.css"
TEST_UNREACHABLE_URL = "https://10.0.0.0"
TEST_NOT_EXISTS_PATH = "111111"

TEST_DATA_DIR = Path(__file__).resolve().parent.joinpath("fixtures")
TEST_PNG_FILE = Path(TEST_DATA_DIR).joinpath("nodejs.png")
TEST_JS_FILE = Path(TEST_DATA_DIR).joinpath("runtime.js")
TEST_CSS_FILE = Path(TEST_DATA_DIR).joinpath("application.css")


ORIGINAL_RESPONSE_PATH = Path(TEST_DATA_DIR).joinpath("original_response.txt")
CHANGED_RESPONSE_PATH = Path(TEST_DATA_DIR).joinpath("changed_html.txt")


@pytest.fixture()
def tmpdirname():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_page_loader_base_functional(tmpdirname, requests_mock):
    original_reponse = Path(ORIGINAL_RESPONSE_PATH).read_text()
    changed_html = Path(CHANGED_RESPONSE_PATH).read_text()
    requests_mock.get(TEST_URL, text=original_reponse)
    requests_mock.get(
        TEST_FULL_URL_PNG_FILE, content=Path(TEST_PNG_FILE).read_bytes()
    )
    requests_mock.get(
        TEST_FULL_URL_JS_FILE, content=Path(TEST_JS_FILE).read_bytes()
    )
    requests_mock.get(
        TEST_FULL_URL_CSS_FILE, content=Path(TEST_CSS_FILE).read_bytes()
    )
    file_path = download(TEST_URL, tmpdirname)
    response = Path(file_path).read_text()
    assert Path(file_path) == Path(tmpdirname).joinpath(TEST_URL_FILE_NAME)
    assert response == changed_html
    assert Path(tmpdirname).joinpath(TEST_URL_DIR_NAME).exists()
    assert (
        Path(tmpdirname)
        .joinpath(TEST_URL_DIR_NAME, TEST_URL_PNG_FILE_NAME)
        .exists()
    )
    assert (
        Path(tmpdirname)
        .joinpath(TEST_URL_DIR_NAME, TEST_URL_JS_FILE_NAME)
        .exists()
    )

    assert (
        Path(tmpdirname)
        .joinpath(TEST_URL_DIR_NAME, TEST_URL_CSS_FILE_NAME)
        .exists()
    )
    assert (
        Path(TEST_PNG_FILE).read_bytes()
        == Path(tmpdirname)
        .joinpath(TEST_URL_DIR_NAME, TEST_URL_PNG_FILE_NAME)
        .read_bytes()
    )
    assert (
        Path(TEST_JS_FILE).read_bytes()
        == Path(tmpdirname)
        .joinpath(TEST_URL_DIR_NAME, TEST_URL_JS_FILE_NAME)
        .read_bytes()
    )
    assert (
        Path(TEST_CSS_FILE).read_bytes()
        == Path(tmpdirname)
        .joinpath(TEST_URL_DIR_NAME, TEST_URL_CSS_FILE_NAME)
        .read_bytes()
    )


def test_page_loader_bad_site(tmpdirname, requests_mock):
    requests_mock.get(TEST_URL, text="Not Found", status_code=500)
    with pytest.raises(requests.exceptions.HTTPError):
        download(TEST_URL, tmpdirname)
    assert not Path(tmpdirname).joinpath(TEST_URL_DIR_NAME).exists()
    assert (
        not Path(tmpdirname)
        .joinpath(TEST_URL_DIR_NAME, TEST_URL_PNG_FILE_NAME)
        .exists()
    )
    assert (
        not Path(tmpdirname)
        .joinpath(TEST_URL_DIR_NAME, TEST_URL_JS_FILE_NAME)
        .exists()
    )
    assert (
        not Path(tmpdirname)
        .joinpath(TEST_URL_DIR_NAME, TEST_URL_CSS_FILE_NAME)
        .exists()
    )


def test_page_loader_unreachable_site(tmpdirname):
    with pytest.raises(requests.exceptions.ConnectTimeout):
        download(TEST_UNREACHABLE_URL, tmpdirname)


def test_storage_errors(requests_mock):
    requests_mock.get(TEST_URL)
    with pytest.raises(StorageErrorException):
        download(TEST_URL, TEST_NOT_EXISTS_PATH)
