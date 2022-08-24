import os

HTML_RESOURCES = {"img": "src", "script": "src", "link": "href"}


def get_link_from_attributes(tag_name, attrs):
    """
    getting the source from attributes

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


def change_resources_link(local_resources):
    """
    change the link to the resource in the soup
    """
    for resource in local_resources:
        soup_item, source_link, save_dir_path = resource
        base_name = os.path.basename(save_dir_path)
        soup_item.attrs[HTML_RESOURCES[soup_item.name]] = os.path.join(
            base_name, source_link
        )


def remove_double_from_the_list(items):
    """
    >>> remove_double_from_the_list([[1,2], [1,2], [3,4]])
    [[1, 2], [3, 4]]
    """
    new_item = []
    for item in items:
        if item not in new_item:
            new_item.append(item)
    return new_item
