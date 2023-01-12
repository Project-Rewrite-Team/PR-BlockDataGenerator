import colorama as color
from shutil import copy
from os import path
from os import getcwd
from os import makedirs
from .logger import log


def make_new_file(copy_file_path: str, new_file_name: str, new_file_path: str, replace_keywords: dict):
    """
    Makes a new file and replaces keywords with strings provided.

    :param copy_file_path: Location of the file to be copied.
    :param new_file_name: Name of the copy.
    :param new_file_path: Locatino to copy to.
    :param replace_keywords: A dictionary of keywords to replace.
    :return:
    """
    makedirs(new_file_path, exist_ok=True)
    copy(copy_file_path, path.join(new_file_path, new_file_name))
    with open(path.join(new_file_path, new_file_name), 'r') as file:
        file_data = file.read()
    for key in replace_keywords.keys():
        file_data = file_data.replace(key, str(replace_keywords[key]))
    with open(path.join(new_file_path, new_file_name), 'w') as file:
        file.write(file_data)


if __name__ == "__main__":
    _copy_file_path = path.join(getcwd(), "Default", "assets", "blockstates", "default.json")
    _new_file_path = path.join(getcwd(), "Generated", "projectrewrite", "assets", "blockstates")
    _new_file_name = "testfile.json"
    _replace_keywords = {
        "<01>": "projectrewrite:blocks/layered_sandstone",
        "<02>": "projectrewrite:blocks/layered_sandstone_top"
    }
    make_new_file(_copy_file_path, _new_file_name, _new_file_path, _replace_keywords)
