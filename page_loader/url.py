from urllib.parse import urljoin, urlparse


def normalize_url_name(url):
    """
    >>> normalize_url_name('https://ru.hexlet.io/courses')
    'ru-hexlet-io-courses'
    """
    url_domain_changed = urlparse(url).netloc.replace(".", "-")
    url_path_changed = urlparse(url).path.replace("/", "-")
    new_url_name = (url_domain_changed + url_path_changed).rstrip("-")
    return new_url_name


def is_same_domain(file_url, url):
    """
    >>> is_same_domain('/courses', 'https://ru.hexlet.io')
    True
    >>> is_same_domain('https://ru.hexlet.io/courses', 'https://ru.hexlet.io')
    True
    >>> is_same_domain('https://ru.hexlet.io/courses', 'https://hexlet.io')
    False
    """
    if not urlparse(file_url).netloc:
        return True
    if urlparse(file_url).netloc == urlparse(url).netloc:
        return True
    return False


def create_full_source_url(file_url, page_url):
    """
    Create a full url for the resource

    >>> create_full_source_url('/nodejs.png', 'https://ru.hexlet.io/')
    'https://ru.hexlet.io/nodejs.png'

    >>> create_full_source_url('https://hex.io/nodejs.png', 'https://hex.io/')
    'https://hex.io/nodejs.png'
    """
    full_source_url = file_url
    if not urlparse(full_source_url).netloc:
        full_source_url = urljoin(page_url, file_url)
    return full_source_url


def get_source_new_filename(source_link, original_url):
    """
    >>> get_source_new_filename('/ass/nodejs.png', 'https://ru.hex.io/co')
    'ru-hex-io-ass-nodejs.png'
    >>> get_source_new_filename('https://ru.hex.io/js/runtime.js', 'https://ru.hex.io/courses') # noqa: E501
    'ru-hex-io-js-runtime.js'
    >>> get_source_new_filename('/courses', 'https://ru.hex.io/courses')
    'ru-hex-io-courses.html'
    """
    netloc_url = urlparse(source_link).netloc.replace(".", "-")
    if not netloc_url:
        netloc_url = urlparse(original_url).netloc.replace(".", "-")
    source_link_path = urlparse(source_link).path
    source_link_without_slash = source_link_path.replace("/", "-")
    if "." not in source_link:
        source_link_without_slash = source_link_without_slash + ".html"
    return f"{netloc_url}{source_link_without_slash}"
