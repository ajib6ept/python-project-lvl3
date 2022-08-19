import os

HTML_RESOURCES = {"img": "src", "script": "src", "link": "href"}


def get_link_from_attributes(tag_name, attrs):  # noqa: E501
    """
    Getting the source from attributes

    >>> get_link_from_attributes('link', {'href': '/courses', 'rel': ['cano']})
    '/courses'
    >>> get_link_from_attributes('script', {'src': 'https://js.stipe.com/v3/'})
    'https://js.stipe.com/v3/'
    >>> get_link_from_attributes('img', {'src': '/nodejs.png', 'alt': 'И'})
    '/nodejs.png'
    >>> get_link_from_attributes('link', {'src': '/courses', 'rel': ['cano']})
    ''
    """
    if tag_name in HTML_RESOURCES.keys():
        return attrs.get(HTML_RESOURCES[tag_name], "")
    return ""


def change_resource_link(soup_item, source_link, save_dir_path):  # noqa: E501
    """
    change resource link in soup
    """
    base_name = os.path.basename(save_dir_path)
    soup_item.attrs[HTML_RESOURCES[soup_item.name]] = os.path.join(
        base_name, source_link
    )
