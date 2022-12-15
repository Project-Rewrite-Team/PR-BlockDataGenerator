import colorama as color
from shutil import copy
from os import path
from os import getcwd
from os import makedirs


class FileReplacer:
    def __log(*args, mixins=(), end="\n",sep="",flush=True, mixin_color=color.Fore.LIGHTCYAN_EX, fore_color=color.Fore.LIGHTWHITE_EX, level="none"):  # Overly complicated log functions, replaces mixins with colorful text!
        x = {"none":"", "warn":"[Warn] ","error":"[ERROR] "}
        if mixins:
            print(fore_color+(x[level] if level in x.keys() else "none")+(sep.join((str(x) for x in args)).format(*(mixin_color+mixin+fore_color for mixin in (str(x) for x in mixins)))), end=end+color.Fore.RESET, flush=flush)
        else:
            print(fore_color+(x[level] if level in x.keys() else "none")+(sep.join((str(x) for x in args))),end=end+color.Fore.RESET, flush=flush)

    def make_new_file(copyfilepath: str, newfilename: str, newfilepath: str, replacekeywords: dict):
        FileReplacer.__log("ensuring {} exists...",mixins=[newfilepath])
        makedirs(newfilepath, exist_ok=True)
        FileReplacer.__log("copying {} to {}",mixins=[copyfilepath,path.join(newfilepath+newfilename)])
        copy(copyfilepath, path.join(newfilepath, newfilename))
        FileReplacer.__log("replacing keywords in file...")
        with open(path.join(newfilepath, newfilename), 'r') as file:
            filedata = file.read()
        for key in replacekeywords.keys():
            filedata = filedata.replace(key, replacekeywords[key])
        FileReplacer.__log("writing changes to file...")
        with open(path.join(newfilepath, newfilename), 'w') as file:
            file.write(filedata)
        FileReplacer.__log("Success! All operations were completed successfully!",fore_color=color.Fore.GREEN)


if __name__ == "__main__":
    copyfilepath = path.join(getcwd(), "Default", "assets", "blockstates", "default.json")
    newfilepath = path.join(getcwd(), "Generated", "projectrewrite", "assets", "blockstates")
    filename = "testfile.json"
    replacekeywords = {
        "<01>": "projectrewrite:blocks/layered_sandstone",
        "<02>": "projectrewrite:blocks/layered_sandstone_top"
    }
    FileReplacer.make_new_file(copyfilepath, filename, newfilepath, replacekeywords)

