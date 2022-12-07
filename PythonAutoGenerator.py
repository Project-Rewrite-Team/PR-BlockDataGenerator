from havenselph.utilities.PyCommands import Commands
from havenselph.utilities.Colors import Colors
import havenselph.utilities.FileReplacer as FileReplacer
from pickle import load
from pickle import dump
from os import path
from os import getcwd

print("\033[2J\033[H")

# Workaround for F-Strings
BRACKETS = "{}"


# Initialize pycommands
_NOT_FOUND = f"{Colors.RED}{BRACKETS}{Colors.LIGHT_GRAY} was not found! Type {Colors.RED}help <command>{Colors.LIGHT_GRAY} for available commands/info on them!{Colors.END}"
_ARG_MISMATCH = f"{Colors.RED}{BRACKETS}{Colors.LIGHT_GRAY} takes {Colors.RED}{BRACKETS}{Colors.LIGHT_GRAY} argument(s), but {Colors.RED}{BRACKETS}{Colors.LIGHT_GRAY} were passed!{Colors.END}"
COMMANDMODULE = Commands(_NOT_FOUND, _ARG_MISMATCH)

# Global variables
NAMESPACE = None

# Will come in a future update!
USECUSTOMDIRECTORY = False
CUSTOMDIRECTORY = None

# Attempt to load saved vars
try:
    with open('save.pag', 'rb') as file:
        NAMESPACE, USECUSTOMDIRECTORY, CUSTOMDIRECTORY = load(file)
except TypeError as e:
    print("Error loading saved namespace! If this is your first time using the program, you can ignore this error.")
    print(e)
except FileNotFoundError:
    pass
except Exception as e:
    print(e)
    
# Internal functions for use in commands
def genericRegisterWithItem(blockname):
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "assets", "blockstates", "default.json"),
        newfilepath=path.join(getcwd(), "Generated", "assets", NAMESPACE, "blockstates"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{blockname}",
        }
    )
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "assets", "models", "item", "default.json"),
        newfilepath=path.join(getcwd(), "Generated", "assets", NAMESPACE, "model", "item"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:item/{blockname}",
        }
    )


# Add all commands to be used
@COMMANDMODULE.add_command("help <command>")
def help():
    for c in COMMANDMODULE.keys():
        print(COMMANDMODULE)

@COMMANDMODULE.add_command("save")
def save():
    with open('save.pag', 'wb') as file:
        dump([NAMESPACE, USECUSTOMDIRECTORY, CUSTOMDIRECTORY], file)
    print(f"{Colors.GREEN}Save complete!{Colors.END}")

@COMMANDMODULE.add_command("exit", aliases=["quit"])
def exit():
    raise KeyboardInterrupt

@COMMANDMODULE.add_command("say", aliases=["print","repeat","echo"])
def say(*args):
    return '\n'.join(args) if (len(args)>1) else args[0]
    
@COMMANDMODULE.add_command("setnamespace <name>", aliases=["newnamespace"])
def setnamespace(name=None):
    global NAMESPACE
    if name:
        NAMESPACE = name
        return f"{Colors.LIGHT_GRAY}Namespace set to {Colors.GREEN}{name}{Colors.LIGHT_GRAY}!{Colors.END}"
    else:
        return f"{Colors.LIGHT_GRAY}You must pass a namespace!{Colors.END}"

@COMMANDMODULE.add_command("namespace")
def namespace():
    return f"Current namespace is {Colors.GREEN}{NAMESPACE}{Colors.END}."

@COMMANDMODULE.add_command("togglecustomdirectory")
def togglecustomdirectory():
    global USECUSTOMDIRECTORY
    if USECUSTOMDIRECTORY:
        USECUSTOMDIRECTORY = False
    else:
        if CUSTOMDIRECTORY:
            USECUSTOMDIRECTORY = True
        else:
            return f"You must set a custom directory, use {Colors.RED}setcustomdirectory <path>{Colors.END}!"

@COMMANDMODULE.add_command("clearscreen", aliases=["clear","cls","clr"])
def clearscreen():
    return "\033[2J\033[H"

@COMMANDMODULE.add_command("newpillarblock <blockname>", aliases=["pillarblock","addpillarblock","generatepillarblock"])
def newpillarblock(blockname, dropped_block=None):
    if not NAMESPACE:
        return f"{Colors.LIGHT_GRAY}You need to set a namespace: {Colors.RED}setnamespace <namespace>{Colors.END}"
    if not dropped_block:
        FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "data", "loot_tables", "blocks", "drops_self.json"),
        newfilepath=path.join(getcwd(), "Generated", "data", NAMESPACE, "loot_tables", "blocks"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{blockname}",
        }
    )
    else:
        FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "data", "loot_tables", "blocks", "stone_like.json"),
        newfilepath=path.join(getcwd(), "Generated", "data", NAMESPACE, "loot_tables", "blocks"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{blockname}",
            "<02>":dropped_block
        }
    )
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "assets", "blockstates", "pillaredblock.json"),
        newfilepath=path.join(getcwd(), "Generated", "assets", NAMESPACE, "blockstates"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{blockname}",
        }
    )
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "assets", "models", "block", "pillaredblock.json"),
        newfilepath=path.join(getcwd(), "Generated", "assets", NAMESPACE, "models", "block"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{blockname}",
            "<02>":f"{NAMESPACE}:block/{blockname}_top"
        }
    )
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "assets", "models", "block", "pillaredblock_horizontal.json"),
        newfilepath=path.join(getcwd(), "Generated", "assets", NAMESPACE, "models", "block"),
        newfilename=blockname+"_horizontal.json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{blockname}",
            "<02>":f"{NAMESPACE}:block/{blockname}_top"
        }
    )
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "assets", "models", "item", "pillaredblock.json"),
        newfilepath=path.join(getcwd(), "Generated", "assets", NAMESPACE, "models", "item"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{blockname}",
        }
    )

@COMMANDMODULE.add_command("sign <signname>")
def sign(blockname):
    if not NAMESPACE:
        return f"{Colors.LIGHT_GRAY}You need to set a namespace: {Colors.RED}setnamespace <namespace>{Colors.END}"
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "assets", "blockstates", "sign.json"),
        newfilepath=path.join(getcwd(), "Generated", "assets", NAMESPACE, "blockstates"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{blockname}",
        }
    )
    newblockname = blockname.split("_")
    newblockname.insert(2, "wall")
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "assets", "blockstates", "wall_sign.json"),
        newfilepath=path.join(getcwd(), "Generated", "assets", NAMESPACE, "blockstates"),
        newfilename="_".join(newblockname)+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{blockname}",
        }
    )
    newblockname = blockname.split("_")
    newblockname[2] = "planks"
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "assets", "models", "block", "sign.json"),
        newfilepath=path.join(getcwd(), "Generated", "assets", NAMESPACE, "models", "block"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{'_'.join(newblockname)}",
        }
    )
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "assets", "models", "item", "default.json"),
        newfilepath=path.join(getcwd(), "Generated", "assets", NAMESPACE, "models", "item"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:item/{blockname}",
        }
    )
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "data", "loot_tables", "blocks", "drops_self.json"),
        newfilepath=path.join(getcwd(), "Generated", "data", NAMESPACE, "loot_tables", "blocks"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:item/{blockname}",
        }
    )
    

@COMMANDMODULE.add_command("leaves <sapling>")
def leaves(blockname, sapling):
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "data", "loot_tables", "blocks", "leaves.json"),
        newfilepath=path.join(getcwd(), "Generated", "data", NAMESPACE, "loot_tables", "blocks"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{blockname}",
            "<02>":sapling
        }
    )
    FileReplacer.FileReplacer.make_new_file(
        copyfilepath=path.join(getcwd(), "Default", "assets", "models", "block", "leaves.json"),
        newfilepath=path.join(getcwd(), "Generated", "assets", NAMESPACE, "models", "block"),
        newfilename=blockname+".json",
        replacekeywords= {
            "<01>":f"{NAMESPACE}:block/{blockname}",
        }
    )
    genericRegisterWithItem(blockname)
    

try:
    print(f"{Colors.LIGHT_GRAY}Welcome to the autogenerator, type {Colors.GREEN}help <command>{Colors.LIGHT_GRAY} for available commands/info on them!"+Colors.END)
    while True:
        last = COMMANDMODULE.execute(input(Colors.GREEN+'>>> '+Colors.END))
        if last[0]:
            # pass
            print(last[2] or "", end="\n")
        else:
            print(last[1])
except (KeyboardInterrupt) as e:
    save()