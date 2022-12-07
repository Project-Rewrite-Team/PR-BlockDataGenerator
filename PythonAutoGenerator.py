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
NOT_FOUND = f"{Colors.RED}{BRACKETS}{Colors.LIGHT_GRAY} was not found! Type {Colors.RED}help <command>{Colors.LIGHT_GRAY} for available commands/info on them!{Colors.END}"
ARG_MISMATCH = f"{Colors.RED}{BRACKETS}{Colors.LIGHT_GRAY} takes {Colors.RED}{BRACKETS}{Colors.LIGHT_GRAY} argument(s), but {Colors.RED}{BRACKETS}{Colors.LIGHT_GRAY} were passed!{Colors.END}"
COMMANDMODULE = Commands(NOT_FOUND, ARG_MISMATCH)

# Global variables
NAMESPACE = None

# Attempt to load saved namespace
try:
    with open('save.pag', 'rb') as file:
        NAMESPACE = load(file)
except TypeError as e:
    print("Error loading saved namespace! If this is your first time using the program, you can ignore this error.")
    print(e)
    
# Internal functions for use in commands
# ...


# Add all commands to be used
@COMMANDMODULE.add_command("help <command>")
def help():
    for c in COMMANDMODULE.keys():
        print(COMMANDMODULE)

@COMMANDMODULE.add_command("save")
def save():
    with open('save.pag', 'wb') as file:
        dump(NAMESPACE, file)
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

@COMMANDMODULE.add_command("clearscreen", aliases=["clear","cls","clr"])
def clearscreen():
    return "\033[2J\033[H"

@COMMANDMODULE.add_command("newpillarblock <blockname>", aliases=["pillarblock","addpillarblock","generatepillarblock"])
def newpillarblock(blockname):
    if not NAMESPACE:
        return f"{Colors.LIGHT_GRAY}You need to set a namespace: {Colors.RED}setnamespace <namespace>{Colors.END}"
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