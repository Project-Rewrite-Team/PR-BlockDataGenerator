from shutil import copy
from os import path
from os import getcwd
from os import makedirs

class Colors:
    LIGHT_GRAY = "\033[0;37m"
    GREEN = "\033[0;32m"
    LIGHT_BLUE = "\033[1;34m"
    END = "\033[0m"

class FileReplacer:
    def make_new_file(copyfilepath: str, newfilename: str, newfilepath: str, replacekeywords: dict):
        print(f"{Colors.LIGHT_GRAY}Making sure {Colors.LIGHT_BLUE}{newfilepath}{Colors.LIGHT_GRAY} exists...{Colors.END}")
        makedirs(newfilepath, exist_ok=True)
        print(f"{Colors.LIGHT_GRAY}Copying {Colors.LIGHT_BLUE}{copyfilepath}{Colors.LIGHT_GRAY} to new directory...{Colors.END}")
        copy(copyfilepath, path.join(newfilepath, newfilename))
        
        print(f"{Colors.LIGHT_GRAY}Opening {Colors.LIGHT_BLUE}{path.join(newfilepath, newfilename)}{Colors.LIGHT_GRAY}...{Colors.END}")
        with open(path.join(newfilepath, newfilename), 'r') as file :
            filedata = file.read()

        print(f"{Colors.LIGHT_GRAY}Replacing keywords...{Colors.END}")
        for key in replacekeywords.keys():
            filedata = filedata.replace(key, replacekeywords[key])

        print(f"{Colors.LIGHT_GRAY}Merging changes...{Colors.END}")
        with open(path.join(newfilepath, newfilename), 'w') as file:
            file.write(filedata)
        print(f"{Colors.GREEN}Success! All operations were completed!{Colors.END}")
        


if __name__=="__main__":
    from Colors import Colors
    copyfilepath = path.join(getcwd(),"Default","assets","blockstates","pilaredblock.json")
    newfilepath = path.join(getcwd(),"Generated", "projectrewrite", "assets","blockstates")
    filename = "testfile.json"
    replacekeywords = {
        "<01>":"projectrewrite:blocks/layered_sandstone",
        "<02>":"projectrewrite:blocks/layered_sandstone_top"
    }
    FileReplacer.make_new_file(copyfilepath,filename,newfilepath,replacekeywords)

