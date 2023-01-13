# Various needed imports

from havenselph.utilities import log
from havenselph.utilities import Template, BlockTools
import colorama as color
from pickle import load
from pickle import dump
from os import makedirs
from os import path
from os import getcwd
from shutil import rmtree
from os import abort
from PyCommandsTool import Commands


class AutoGen:
    class NameSpaceNotSet(Exception):
        pass

    def __init__(self):
        self.USE_CUSTOM_DIRECTORY = False
        self.CUSTOM_DIRECTORY = None
        self.NAMESPACE_DATA = None
        self.REPLACEMENTS = {}
        self.ORE_COPY = {
            "copper": (5, 2),
            "lapis": (9, 4),
            "redstone": (5, 4),
            "nether_gold": (6, 2)
        }

    @property
    def NAMESPACE(self):
        if self.NAMESPACE_DATA:
            return self.NAMESPACE_DATA
        else:
            log("You must set a namespace, enter one now:")
            self.NAMESPACE_DATA = input(">>> ")
            log("Namespace set to: {}", mixins=[self.NAMESPACE_DATA])
            return self.NAMESPACE_DATA

    def save_data(self):
        log("Saving data...")
        with open("data.agn", 'wb') as file:
            dump(vars(self), file)
        log("Data was saved.", fore_color=color.Fore.GREEN)

    def load_data(self):
        try:
            log("Attempting to load data...")
            with open("data.agn", 'rb') as file:
                self.__dict__.update(load(file))
        except FileNotFoundError:
            return 1
        except Exception as er:
            log("An exception was encountered:\n{}\nPlease report this to our GitHub or Discord!", mixins=[repr(er)],
                fore_color=color.Fore.RED, mixin_color=color.Fore.LIGHTRED_EX, level="error")
            return 1
        log("Data was loaded.", fore_color=color.Fore.GREEN)

    def target_directory(self):
        if not self.USE_CUSTOM_DIRECTORY or not self.CUSTOM_DIRECTORY or not path.exists(self.CUSTOM_DIRECTORY):
            return path.join(getcwd(), "Generated")
        else:
            return path.join(self.CUSTOM_DIRECTORY)


# Global variables
a = AutoGen()
a.load_data()

COMMANDMODULE = Commands(register_help_command=False, register_aliases_command=False)


# Script Functions
def run(_input: str):
    try:
        COMMANDMODULE.execute(_input)

    except COMMANDMODULE.NoSuchCommand:
        log("{} was not recognized as a command!", mixins=COMMANDMODULE.parse(_input)[0])

    except COMMANDMODULE.ParseError as er:
        log(er)

    except Exception as er:
        log(er)


# Main Commands
@COMMANDMODULE.add_command("help", "about", does="Shows information about given command, or lists all commands.")
def help_command(command=None):
    if command:
        args = []
        for param in COMMANDMODULE[command].params:
            args.append(f"<{param}>")
        log("{}: " + COMMANDMODULE[command].does + "\nArgs: {}", mixins=[command, " ".join(args or ["no arguments"])])
        if COMMANDMODULE[command].help_msg != COMMANDMODULE[command].usage:
            log(COMMANDMODULE[command].help_msg)
    else:
        print("List of available commands: ")
        for cmd in COMMANDMODULE.commands_no_aliases:
            args = []
            for param in COMMANDMODULE[cmd].params:
                args.append(f"<{param}>")
            log("{}: " + COMMANDMODULE[cmd].does + "\nArgs: {}", mixins=[cmd, " ".join(args or ["no arguments"])],
                end="\n\n")


@COMMANDMODULE.add_command("aliases", "names", does="Shows all names pointing to a given command.")
def aliases(command):
    if COMMANDMODULE[command]:
        log("Registered aliases for {}:", mixins=[command])
        for i, name in enumerate(COMMANDMODULE[command].names):
            if i == len(COMMANDMODULE[command].names) - 1:
                log(name, fore_color=color.Fore.LIGHTCYAN_EX)
                continue
            log("{}, ", mixins=[name], end="", flush=False)


@COMMANDMODULE.add_command("dump", "savedump", does="Dumps save data to the terminal, mainly used for debugging code.")
def save_dump():
    log(a.__dict__)


@COMMANDMODULE.add_command("deletesavedinformation", does="Deletes ALL saved information, there is NO going back!")
def delete_save(confirm=None):
    if confirm == "confirm":
        if input("FINAL CHANCE: are you really sure? y/n: ") == "y":
            log("Saved information deleted.")
            global a
            a = AutoGen()
            a.save_data()
        else:
            log("Deletion aborted.")
    else:
        log("You must type: {}", mixins=["deletesavedinformation confirm"])


@COMMANDMODULE.add_command("setcustomdirectory", "setdir",
                           does="Sets path for generated files to be created at, use help on this command to learn more.")
def setcustomdirectory(dirpath, use=False, create=False):
    if path.exists(dirpath):
        a.CUSTOM_DIRECTORY = dirpath
        a.USE_CUSTOM_DIRECTORY = use
        log("Custom directory path set as {}\nUse: {}", mixins=[dirpath, use])
    elif not path.exists(dirpath) and create:
        makedirs(dirpath, exist_ok=True)
        a.CUSTOM_DIRECTORY = dirpath
        a.USE_CUSTOM_DIRECTORY = use
        log("Custom directory path set to created directory: {}\nUse: {}", mixins=[dirpath, use])


@COMMANDMODULE.add_command("setnamespace", "namespace", does="Shows or sets current namespace.")
def setnamespace(namespace=None):
    if namespace:
        a.NAMESPACE_DATA = namespace
        log("Set namespace to: {}", mixins=[namespace])
    else:
        # noinspection
        log("Current namespace: {}", mixins=[a.NAMESPACE_DATA or "No namespace has been set!"])


@COMMANDMODULE.add_command("newreplacement", "newrp",
                           does="Registers a new replacement token, use 'help newrp' for more info.")
def new_replacement(token, value):
    log("Creating new token: {} --> {}", mixins=["%" + token, value])
    a.REPLACEMENTS.update({"%" + token: value})


@COMMANDMODULE.add_command("deletereplacement", "delrp",
                           does="Deletes an existing replacement token, create one using: 'newrp'")
def del_replacement(token):
    a.REPLACEMENTS["%" + token] = None
    print(a.REPLACEMENTS[token])


@COMMANDMODULE.add_command("showreplacements", "showrp",
                           does="Shows all replacement tokens, create some using: 'newrp'")
def show_replacements():
    if not a.REPLACEMENTS:
        log("No replacement tokens have been set. Set one using {}", mixins=["newrp <token>"])
        return 0
    log("Showing all tokens and their replacements:\n{} --> {}", mixins=["token", "replacement"])
    for token in a.REPLACEMENTS.keys():
        log("{} --> {}", mixins=[token, a.REPLACEMENTS[token]])


@COMMANDMODULE.add_command("resetreplacements", does="Deletes all replacement tokens. NO GOING BACK")
def reset_replacements():
    log("Are you sure? There is no going back:")
    if input("type 'yes' >>> ") == "yes":
        a.REPLACEMENTS = {}
    else:
        log("Deletion aborted.")


@COMMANDMODULE.add_command("deletegenerated", "cleargenerated", does="Clears files within custom directory or default directory. WILL DELETE FILES NOT MADE BY THE PROGRAM!")
def delete_generated(override: bool=False):
    if a.USE_CUSTOM_DIRECTORY:
        log("You are using a custom directory, it is recommended that you manually delete files instead to avoid deleting important files! You have been warned!", level="warn")

    if not override:
        log("You are about to delete ALL files within: {}\nAre you sure you want to do this? Type {}", mixins=[a.target_directory(), "yes"], fore_color=color.Fore.RED, mixin_color=color.Fore.WHITE, level="warn")
        if not input(">>> ").lower()=="yes":
            log("Input did not match {}, aborting.", mixins=["yes"])
            return
    try:
        rmtree(a.target_directory())
        log("All files deleted!")
    except WindowsError:
        log("No file was found at path location.")


@COMMANDMODULE.add_command("generatefromfile", "fromfile",
                           does="Runs a file as input to this terminal, allowing auto generation of hundreds of blocks in one command!")
def generatefromfile(filename="generate.ags"):
    try:
        with open(path.join(getcwd(), filename), "r") as file:
            log("Running commands from {}", mixins=[filename])
            for line in file:
                if line == "\n":
                    continue
                elif line[0] == "#" or line[0:2] == "//":
                    continue
                run(line)
    except FileNotFoundError:
        log("No such file or directory: {}", mixins=[filename], fore_color=color.Fore.RED, mixin_color=color.Fore.RED,
            level="error")


@COMMANDMODULE.add_command("newdb","newdefaultblock", does="Generates a default block. Pass a second variable to set what it drops.")
def default_block(block_name: str, dropped_item: str=None):
    BlockTools.NewBlock.generic(a.target_directory(), a.NAMESPACE, block_name, dropped_item)


@COMMANDMODULE.add_command("newpb", "newpillarblock", does="Generates a pillar block, these behave like logs. Pass a second variable to set what it drops.")
def pillar_block(block_name: str, dropped_item: str=None):
    BlockTools.NewBlock.pillar(a.target_directory(), a.NAMESPACE, block_name, dropped_item)


@COMMANDMODULE.add_command("newwb", "newwoodblock", does="Generates a pillar block with no end block, this behaves like wood blocks. Pass a second variable to set what it drops.")
def wood_block(block_name: str, dropped_item: str, texture_name: str=None):
    BlockTools.NewBlock.pillar(a.target_directory(), a.NAMESPACE, block_name, dropped_item, texture_name)


@COMMANDMODULE.add_command("newob", "neworeblock", does="Generates an ore block. Pass 'copyof=<ore>' to copy their drop settings.")
def ore_block(block_name: str, dropped_ore: str, copyof: str=None, max_min_dropped: list or tuple=(0,0)):
    if copyof in a.ORE_COPY.keys():
        max_dropped, min_dropped = a.ORE_COPY[copyof]

    if max_min_dropped != (0,0) or copyof not in a.ORE_COPY.keys():
        max_dropped, min_dropped = max_min_dropped

    # noinspection PyUnboundLocalVariable
    if (max_dropped, min_dropped) != (0, 0):
        BlockTools.NewBlock.ore(a.target_directory(), a.NAMESPACE, block_name, dropped_ore, max_dropped, min_dropped)
    else:
        BlockTools.NewBlock.ore(a.target_directory(), a.NAMESPACE, block_name, dropped_ore)


@COMMANDMODULE.add_command("newolt", "neworeloottable", does="Overwrites an ore's loot_table, useful for overwriting minecraft blocks or even previously generated ones.")
def ore_loot_table(block_name: str, dropped_ore, copyof: str=None, max_min_dropped: list or tuple=(0,0)):
    if copyof in a.ORE_COPY.keys():
        max_dropped, min_dropped = a.ORE_COPY[copyof]

    if max_min_dropped != (0,0) or copyof not in a.ORE_COPY.keys():
        max_dropped, min_dropped = max_min_dropped

    # noinspection PyUnboundLocalVariable
    if (max_dropped, min_dropped) != (0, 0):
        _loot_table = Template.LootTable.Blocks.custom_ore(a.NAMESPACE, block_name, dropped_ore, max_dropped, min_dropped)
    else:
        _loot_table = Template.LootTable.Blocks.ore(a.NAMESPACE, block_name, dropped_ore)
    BlockTools.make_file(a.target_directory(), a.NAMESPACE, block_name, "ltb", _loot_table)


@COMMANDMODULE.add_command("newsap", "newsapling", does="Generates a sapling.")
def sapling(block_name: str):
    BlockTools.NewBlock.sapling(a.target_directory(), a.NAMESPACE, block_name)


@COMMANDMODULE.add_command("newlvs", "newleaves", does="Generates a leaves block.")
def leaves(block_name: str, sapling_name: str, stick_name="minecraft:stick"):
    BlockTools.NewBlock.leaves(a.target_directory(), a.NAMESPACE, block_name, sapling_name, stick_name)


# Help Messages
COMMANDMODULE["setdir"].set_help_msg("""
This command allows you to set a custom path for generated files to be sent to,
by default they go to "Generated/" within this scripts parent directory.
If you set a custom directory, say to a project file so the scripts are
automatically generated in their final place, make sure you set it to the
"<yourprojectfile>/src/main/resources/" directory, it will not create a
"/Generated" directory, so use with caution. I recommend that you create a 
directory just for generated files as to not overwrite any you don't want to,
because there is NOT an undo function.
Command example:
setdir "D:\\Projects\\Modding\\Minecraft\\chameleons\\src\\main\\resources\\Generated" use=True create=True
""")
COMMANDMODULE["fromfile"].set_help_msg("""
This command works like a scripting language, once you understand our commands,
you can automatically generate everything almost immediately! Below is and ex-
ample of how to use the scripting language:

    -----------------------------------------------    
    FILENAME: generate.ags | CONTENTS:
    // This can be used as a comment!
    /* This too!
    */ Sadly it doesn't work like this though, yet!!!!

    # Python comments work as well!

    # Let's make a pillar block:
    newpillarblock layered_sandstone cobbled_layered_sandstone
    newpillarblock yucca_palm_logs
    newpillarblock yucca_palm_stripped_logs
    -----------------------------------------------

It really is as simple as that! Anything you can type in this console,
you can type in a .ags file and it will run just as if you typed it out
in the console! 
By default, this command targets "generate.ags" but you can change this
by passing a file name, ex:
fromfile myscript.ags
    """)
COMMANDMODULE["setnamespace"].set_help_msg("""
This command sets the namespace for the current project. This is the
name that goes before a blockname, ex:
    minecraft:dirt
    minecraft:grass_block
    projectrewrite:layered_sandstone
    projectrewrite:cobbled_layered_sandstone
This is the default name it will put before a block name if you don't
provide one. It is also the name of the directory it will create inside
of whatever the parent directory is. For instance, if your namespace
was "coolnamespace" and your directory was "Generated/" it would generate
a file structure as such:
    Generated/coolnamespace/assets/...
    Generated/coolnamespace/data/...
Pair this with "setcustomdirectory" to automatically output all generated
files to your project directory! Learn more with: "help setdir"
""")
COMMANDMODULE["newrp"].set_help_msg("""
Replacement tokens are how you make the workflow way easier! Isn't it annoying
writing out a namespace/really long block name over and over? Well... It doesn't
have to be! Take this scenario for instance:
    newpb yucca_palm_log
    newpb yucca_palm_wood
    newpb yucca_palm_stripped_log
    newpb yucca_palm_stripped_wood
    newpb yucca_palm_planks
It's kind of annoying having to write 'yucca_palm' every single time, isn't it?
Lets fix that by running the following command:
    newrp yp yucca_palm
Now the following lines will be exactly the same as the above ones:
    newpb %yp_log
    newpb %yp_wood
    newpb %yp_stripped_log
    newpb %yp_stripped_wood
    newpb %yp_planks
Isn't that way easier? You can also replace namespaces with tokens:
    newrp pr projectrewrite
    newpb %pr:log <--> newpb projectrewrite:log
""")

# Input loop
try:
    while True:
        run(input(">>> "))

except KeyboardInterrupt:
    a.save_data()

except IOError:  # this error is weirdly thrown when using exit() on pycharm.
    a.save_data()
    abort()
