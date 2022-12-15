# Various needed imports
from havenselph.utilities.filereplacerold import FileReplacer
import colorama as color
from pickle import load
from pickle import dump
from os import makedirs
from os import path
from os import getcwd
from os import listdir
from os import abort

# Get and register pycommands module
from havenselph.utilities.pycommands import Commands

COMMANDMODULE = Commands(register_help_command=False, register_aliases_command=False)


def log(*args, mixins=(), end="\n", sep="", flush=True, mixin_color=color.Fore.LIGHTCYAN_EX,
        fore_color=color.Fore.LIGHTWHITE_EX,
        level="none"):  # Overly complicated log functions, replaces mixins with colorful text!
    x = {"none": "", "warn": "[Warn] ", "error": "[ERROR] "}
    if mixins:
        print(fore_color + (x[level] if level in x.keys() else "none") + (sep.join((str(x) for x in args)).format(
            *(mixin_color + mixin + fore_color for mixin in (str(x) for x in mixins)))), end=end + color.Fore.RESET,
              flush=flush)
    else:
        print(fore_color + (x[level] if level in x.keys() else "none") + (sep.join((str(x) for x in args))),
              end=end + color.Fore.RESET, flush=flush)


def run(command):
    try:
        out = COMMANDMODULE.execute(command)
        if out[0] == 0:
            pass
        elif out[0] == 1:
            log("Error: "+str(out[1]), fore_color=color.Fore.RED)
        elif out[0] == 2:
            if out[1] == "Argument does not refer to any registered command.":
                log("{} could not be found, type {} for a list of all commands.", mixins=[out[3][0], "help"],
                    fore_color=color.Fore.RED, mixin_color=color.Fore.YELLOW)
            else:
                log("{} was not recognized as a valid command, type {} for a list of all commands.",
                    mixins=[out[2], "help"], fore_color=color.Fore.RED, mixin_color=color.Fore.YELLOW)
        elif out[0] == 3:
            log("You must enter a command, enter {} for a list of all valid commands.", mixins=["help"],
                fore_color=color.Fore.RED, mixin_color=color.Fore.YELLOW)
    except a.NameSpaceNotSet:
        log("You must set a namespace before using this command! Do so by typing {}", mixins=["namespace"], fore_color=color.Fore.RED)
    except Exception as er:
        user_input = COMMANDMODULE.parse(command)
        log("An exception was encountered while running the command: \n{0}\nInput: {1}({2}, {4})\nSave: {3}\nPlease report this issue on our Discord, or GitHub, thanks!",
            mixins=[repr(er), user_input[0][0], " ".join(user_input[0][1:]), vars(a), user_input[1] or ""], fore_color=color.Fore.RED,
            mixin_color=color.Fore.YELLOW)
    else:
        return out
    finally:
        return 1


class AutoGen:
    class NameSpaceNotSet(Exception):  # Need this for a couple of things.
        pass

    def __init__(self):
        self.USE_CUSTOM_DIRECTORY = False
        self.CUSTOM_DIRECTORY = None
        self.NAMESPACE = None
        self.REPLACEMENTS = {}
        self.TEMPLATES = {}
        self.get_files()
        self.ORE_COPY = {
            "copper": ["5", "2"],
            "lapis": ["9", "4"],
            "redstone": ["5", "4"],
            "nether_gold": ["6", "2"]
        }

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
                self.get_files()
        except FileNotFoundError:
            pass
        except Exception as er:
            log("An exception was encountered:\n{}\nPlease report this to our GitHub or Discord!", mixins=[repr(er)],
                fore_color=color.Fore.RED, mixin_color=color.Fore.LIGHTRED_EX, level="error")
            return 1
        log("Data was loaded.", fore_color=color.Fore.GREEN)

    def get_files(self):
        for file in listdir(path.join(getcwd(), "Default", "assets", "blockstates")):
            self.TEMPLATES.update({
                f"blockstates/" + file.replace(".json",
                                               ""): f"{path.join(getcwd(), 'Default', 'assets', 'blockstates', file)}"
            })
        for file in listdir(path.join(getcwd(), "Default", "assets", "models", "block")):
            self.TEMPLATES.update({
                f"models/block/" + file.replace(".json",
                                                ""): f"{path.join(getcwd(), 'Default', 'assets', 'models', 'block', file)}"
            })
        for file in listdir(path.join(getcwd(), "Default", "assets", "models", "item")):
            self.TEMPLATES.update({
                f"models/item/" + file.replace(".json",
                                               ""): f"{path.join(getcwd(), 'Default', 'assets', 'models', 'item', file)}"
            })
        for file in listdir(path.join(getcwd(), "Default", "data", "loot_tables", "blocks")):
            self.TEMPLATES.update({
                f"loot_tables/blocks/" + file.replace(".json",
                                                      ""): f"{path.join(getcwd(), 'Default', 'data', 'loot_tables', 'blocks', file)}"
            })


# Global variables
a = AutoGen()  # Permanent save system! loads data automatically
a.load_data()


def target_directory(*filepath):
    # A way to use the custom directory, if enabled and path exists, or use the generated directory
    # without a ton of if statements, I'm sure there's a more pythonic way, but I don't really care.
    #
    # Just in case you were thinking it, no, this is not a big impact on speed, Python handles this
    # extremely fast.
    if not a.USE_CUSTOM_DIRECTORY or not a.CUSTOM_DIRECTORY or not path.exists(a.CUSTOM_DIRECTORY):
        return path.join(getcwd(), "Generated", *filepath)
    else:
        return path.join(a.CUSTOM_DIRECTORY, *filepath)


def make_replacements(string: str):
    if a.REPLACEMENTS:
        for key, value in a.REPLACEMENTS.items():
            string = string.replace(key, value)
    return string


def arg_replace(*args, add_namespace_if_needed=True):
    def do_replacement(arg):
        if not arg:
            return arg
        arg = make_replacements("block/"+arg)
        if ":" not in arg and add_namespace_if_needed:
            arg = a.NAMESPACE + ":" + arg
        return arg
    if len(args)>1:
        return (do_replacement(arg) for arg in args)
    else:
        return do_replacement(*args)


def nonblock(name: str):
    return name.replace("block/", "")


@COMMANDMODULE.add_command("echo", "say",
                           does="Repeats any arguments sent to it. Could be useful within a script file.")
def echo(*args):
    for arg in args:
        log(make_replacements(arg))


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


@COMMANDMODULE.add_command("setnamespace", "namespace", does="Shows or sets current namespace.")
def setnamespace(namespace=None):
    if namespace:
        a.NAMESPACE = namespace
        log("Set namespace to: {}", mixins=[namespace])
    else:
        log("Current namespace: {}", mixins=[a.NAMESPACE or "No namespace has been set!"])


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


# Generation commands:
@COMMANDMODULE.add_command("rawnewfile", does="Use help on this command to learn about how to use it.")
def new_file(template, target: list or tuple, file_name, *replacements, file_ext=".json"):
    replace = {}
    for i, rp in enumerate(replacements):  # This is stupid IK, but it auto generates replacements for me!!!
        replace.update({f"<0{i+1}>" if i+1<10 else f"<{i+1}>":rp})
    FileReplacer.make_new_file(
        copyfilepath=a.TEMPLATES[template],
        newfilepath=target_directory(target[0], a.NAMESPACE, target[1]),
        newfilename=file_name+file_ext,
        replacekeywords=replace
    )
    return 0


@COMMANDMODULE.add_command("pillarblock", "newpb",does="Generates a pillar block. Pillar blocks are blocks that behave like logs, deepslate, etc.")
def pillarblock(block_name, dropped_block=None):
    if not a.NAMESPACE:
        log("You must set a namespace first, use {}", mixins=["setnamespace <name>"])
        return 1
    block_name, dropped_block = arg_replace(block_name, dropped_block)
    file_name = nonblock(block_name.split(":")[1])
    new_file("blockstates/pillaredblock", ["assets", "blockstates"], file_name, block_name + "_horizontal", block_name, block_name + "_horizontal")
    new_file("models/block/pillaredblock", ["assets", path.join("models", "block")], file_name, block_name, block_name + "_top")
    new_file("models/block/pillaredblock_horizontal", ["assets", path.join("models", "block")], file_name + "_horizontal", block_name, block_name + "_top")
    new_file("models/item/default", ["assets", path.join("models", "item")], file_name, block_name)
    if dropped_block:
        new_file("loot_tables/blocks/stone_like", ["data", path.join("loot_tables", "blocks")], file_name, nonblock(block_name), nonblock(dropped_block))
    else:
        new_file("loot_tables/blocks/drops_self", ["data", path.join("loot_tables", "blocks")], file_name, nonblock(block_name))


@COMMANDMODULE.add_command("genericblock", "newgb",
                           does="Generates a generic block. These are blocks that behave like dirt, planks, etc.")
def genericblock(block_name, dropped_block=None):
    if not a.NAMESPACE:
        log("You must set a namespace first, use {}", mixins=["setnamespace <name>"])
        return 1
    block_name, dropped_block = arg_replace(block_name, dropped_block)
    file_name = nonblock(block_name.split(":")[1])
    new_file("blockstates/default", ["assets", "blockstates"], file_name, block_name)
    new_file("models/block/default", ["assets", path.join("models", "block")], file_name, block_name)
    new_file("models/item/default", ["assets", path.join("models", "item")], file_name, block_name)
    if dropped_block:
        new_file("loot_tables/blocks/stone_like", ["data", path.join("loot_tables", "blocks")], file_name, nonblock(block_name), nonblock(dropped_block))
    else:
        new_file("loot_tables/blocks/drops_self", ["data", path.join("loot_tables", "blocks")], file_name, nonblock(block_name))


@COMMANDMODULE.add_command("oreblock", "newob", "newore",
                           does="Generates a new ore block. These are blocks that behave like iron_ore, diamond_ore, etc.")
def oreblock(block_name, dropped_item, copyof=None, maxdropped=None, mindropped=None):
    if not maxdropped and copyof:
        maxdropped = a.ORE_COPY[copyof][0]
    if not mindropped and copyof:
        mindropped = a.ORE_COPY[copyof][1]
    if not a.NAMESPACE:
        log("You must set a namespace first, use {}", mixins=["setnamespace <name>"])
        return 1
    block_name, dropped_block = arg_replace(block_name, dropped_item)
    file_name = nonblock(block_name.split(":")[1])
    new_file("blockstates/default", ["assets", "blockstates"], file_name, block_name)
    new_file("models/block/default", ["assets", path.join("models", "block")], file_name, block_name)
    new_file("models/item/default", ["assets", path.join("models", "item")], file_name, block_name)
    if mindropped and maxdropped:
        new_file("loot_tables/blocks/customore", ["data", path.join("loot_tables", "blocks")], file_name, nonblock(block_name), nonblock(block_name), maxdropped, mindropped)
    else:
        new_file("loot_tables/blocks/ore", ["data", path.join("loot_tables", "blocks")], file_name, nonblock(block_name), nonblock(block_name))

@COMMANDMODULE.add_command("oreloottable", "newolt",
                           does="Generates a new ore loottable. This can be used to overwrite minecraft ores as well! Just set your namespace to minecraft.")
def oreloottable(block_name, dropped_item, copyof=None, maxdropped=None, mindropped=None):
    if not maxdropped and copyof:
        maxdropped = a.ORE_COPY[copyof][0]
    if not mindropped and copyof:
        mindropped = a.ORE_COPY[copyof][1]
    if not a.NAMESPACE:
        log("You must set a namespace first, use {}", mixins=["setnamespace <name>"])
        return 1
    block_name, dropped_item = arg_replace(block_name, dropped_item)
    file_name = nonblock(block_name.split(":")[1])
    if mindropped and maxdropped:
        new_file("loot_tables/blocks/customore", ["data", path.join("loot_tables", "blocks")], file_name, nonblock(block_name), nonblock(block_name), maxdropped, mindropped)
    else:
        new_file("loot_tables/blocks/ore", ["data", path.join("loot_tables", "blocks")], file_name, nonblock(block_name), nonblock(block_name))

@COMMANDMODULE.add_command("sign", "newsign",
                           does="Generates a sign block.")
def sign(block_name):
    if not a.NAMESPACE:
        log("You must set a namespace first, use {}", mixins=["setnamespace <name>"])
        return 1
    block_name = arg_replace(block_name)
    file_name = nonblock(block_name.split(":")[1])
    new_file("blockstates/default", ["assets", "blockstates"], file_name, block_name)
    new_file("blockstates/default", ["assets", "blockstates"], file_name.replace("_sign","_wall_sign"), block_name)
    new_file("models/block/sign", ["assets", path.join("models", "block")], file_name, block_name.replace("_sign", "_planks"))
    new_file("models/item/asitem", ["assets", path.join("models", "item")], file_name, block_name)
    new_file("loot_tables/blocks/drops_self", ["data", path.join("loot_tables", "blocks")], file_name, nonblock(block_name))


@COMMANDMODULE.add_command("sapling", "newsap",
                           does="Generates a sapling.")
def sapling(block_name):
    if not a.NAMESPACE:
        log("You must set a namespace first, use {}", mixins=["setnamespace <name>"])
        return 1
    block_name = arg_replace(block_name)
    file_name = nonblock(block_name.split(":")[1])
    new_file("blockstates/default", ["assets", "blockstates"], file_name, block_name)
    new_file("models/block/sapling", ["assets", path.join("models", "block")], file_name, block_name)
    new_file("models/item/asitem", ["assets", path.join("models", "item")], file_name, block_name)
    new_file("loot_tables/blocks/drops_self", ["data", path.join("loot_tables", "blocks")], file_name, nonblock(block_name))


@COMMANDMODULE.add_command("leaves", "newleaves",
                           does="Generates a sapling.")
def leaves(block_name, dropped_sapling):
    if not a.NAMESPACE:
        log("You must set a namespace first, use {}", mixins=["setnamespace <name>"])
        return 1
    block_name, dropped_block = arg_replace(block_name, dropped_sapling)
    file_name = nonblock(block_name.split(":")[1])
    new_file("blockstates/default", ["assets", "blockstates"], file_name, block_name)
    new_file("models/block/leaves", ["assets", path.join("models", "block")], file_name, block_name)
    new_file("models/item/default", ["assets", path.join("models", "item")], file_name, block_name)
    new_file("loot_tables/blocks/leaves", ["data", path.join("loot_tables", "blocks")], file_name, nonblock(block_name), nonblock(dropped_sapling))


# Set help messages for commands:
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
COMMANDMODULE["rawnewfile"].set_help_msg("""
This command is how all the block commands are internally generated, so you can manually create a block
of any type using any .json templates you may have! If you are going to use this command, it is highly
recommended that you use "fromfile" with this, and write a script so you don't have to do this more than
once. Keep in mind that replacement tokens *DO NOT* work with this command. That is for internal reasons.

Below is some example code to help you understand how it works:

    -----------------------------------------------    
    FILENAME: generate.ags | CONTENTS:
    namespace projectrewrite
    
    // Manually create a block state for yucca palm logs (The / is for a continue line, you would not use that in 
    // code, it's just necessary for making this readable)!
    newfile blockstates/pillaredblock [assets blockstates] yucca_palm_log projectrewrite:yucca_palm_log_horizontal /
    projectrewrite:yucca_palm_log projectrewrite:yucca_palm_log_horizontal
    
    // This command automatically does the above and the rest required for a block:
    newpb yucca_palm_log
    -----------------------------------------------
""")
new_block_help = """
*This is a generic help message for all block commands*

These commands generate blocks when provided with the above arguments. Don't
forget about replacement tokens! These are completely compatible so
"newpb %pr:%blck"
could be the same as:
"newpb projectrewrite:layered_cobbled_sandstone"
if you had set the tokens properly! Tokens are a very useful tool for streamlining
this process, happy coding!
"""
COMMANDMODULE["newpb"].set_help_msg(new_block_help)
COMMANDMODULE["newgb"].set_help_msg(new_block_help)
COMMANDMODULE["newob"].set_help_msg(new_block_help)
COMMANDMODULE["newsign"].set_help_msg(new_block_help)
COMMANDMODULE["newsap"].set_help_msg(new_block_help)
COMMANDMODULE["newleaves"].set_help_msg(new_block_help)
COMMANDMODULE["newolt"].set_help_msg("""
This is used to manually generate a loottable for an oreblock! If you want,
you can even overwrite minecraft ore loottables by setting your namespace
to minecraft, then generating a loottable for a minecraft ore! Example:

namespace minecraft
newolt emerald_ore emerald copy_of=copper maxdropped=12

Don't forget to set your namespace back back though!
""")


try:
    while True:
        # Sends input to function defined above, I do it this way so generatefromfile can use the EXACT same input loop.
        last = run(input(f"{color.Fore.LIGHTBLACK_EX}>>> {color.Fore.RESET}"))
except KeyboardInterrupt as e:
    log(e)
finally:
    a.save_data()
    # Technically not needed, but pycharm (what I use for this project) has a bit of an issue
    # with how it handles exit(), this causes an I/O error to be thrown each time you close
    # the tool and I hate seeing that. This is the only solution AFAIK, below is the Stack
    # Overflow question that enlightened me on this annoying bug:
    #
    # https://stackoverflow.com/questions/62173114/using-exit-i-get-valueerror-i-o-operation-on-closed-file
    abort()
