



from shlex import split
import inspect


class Command:
    def __init__(self, funct, names: tuple or list, does):
        self.funct = funct
        self.names = names or [funct.__name__]
        self.args = inspect.getfullargspec(funct)
        self.does = does
        self.help_msg = self.usage

    def run(self, *args, **kwargs):
        try:
            return [0, self.funct(args, kwargs)]
        except Exception as e:
            return [1, e]

    def set_help_msg(self, msg, show_aliases=False, show_usage=False):
        if show_aliases:
            self.help_msg = self.usage if show_usage else ""+"\nNames: "+" | ".join(self.names)+msg
        else:
            self.help_msg = self.usage if show_usage else ""+msg

    @property
    def usage(self, name: str=None):
        if not name:
            name = self.name
        params = "|"
        if not self.params:
            params = "| this command does not take any parameters"
        for param in self.params:
            params += f" <{param}>  "

        return f"| {name}: {self.does}"+"\n"+params

    @property
    def params(self):
        return inspect.signature(self.funct).parameters

    @property
    def name(self):
        return self.names[0]


class Commands(dict):
    class CommandExists(ValueError):
        pass

    class NoSuchCommand(KeyError):
        pass

    class NoValidInput(TypeError):
        pass

    def __init__(self, *, register_help_command=True, register_exit_command=True, register_aliases_command=True):
        self.commands_no_aliases = []
        if register_help_command:
            self.__add_command(
                Command(self.__help_command, ["help"], "prints out available commands, and their arguments")
            )
        if register_aliases_command:
            self.__add_command(
                Command(self.__aliases, ["names","alternate","aliases"], "returns all names for a given command")
            )
        if register_exit_command:
            self.__add_command(
                Command(exit, ["exit"], "exits the program using exit()")
            )
        super().__init__()

    def __add_command(self, command):
        for name in command.names:
            if name in self:
                raise self.CommandExists(
                    f"Name or alias assigned to function {command.funct.__name__} is duplicate: {name}"
                )
            else:
                self[name] = command
        self.commands_no_aliases.append(command.names[0])

    def add_command(self, *names, does="No information provided for this command"):
        def inner_fn(funct):
            self.__add_command(Command(funct, names, does))
            return funct
        return inner_fn

    def __help_command(self, command=None):
        if command:
            print(self[command].help_msg)
        else:
            print("List of available commands: ")
            for command in self.commands_no_aliases:
                print(self[command].usage, end="\n"*2)

    def __aliases(self, command):
        try:
            if self[command]:
                pass
        except self.NoSuchCommand:
            return 1
        print(f"Registered aliases for {command}")
        print(", ".join(self[command].names))

    def execute(self, user_input):
        try:
            command, kwargs = self.parse(user_input)
        except SyntaxError as e:
            return [1, e, user_input]
        except self.NoValidInput as e:
            return [3, e, user_input]
        if command[0] in self.keys():
            return 0, self[command[0]].funct(*command[1:],**kwargs), command[0], command[1:], kwargs
        else:
            return 2, self.NoSuchCommand(f"{command[0]} is not a command!"), command[0], command[1:], kwargs

    def execute_no_parse(self, cmd: str, *args, **kwargs):
        if cmd=="":
            return 3, self.NoValidInput("No valid input was received"), cmd, args, kwargs
        if cmd in self.keys():
            return 0, self[cmd](args, kwargs), cmd, args, kwargs

    @classmethod
    def parse(cls, value=None):
        if not value:
            raise cls.NoValidInput(
                "No valid input was received"
            )
        args = []
        kwargs = {}
        for argument in split(value):
            if "=" in argument:
                if argument=="=":
                    raise SyntaxError(
                        "Value must not be separated with spaces: x=y not x = y"
                    )
                a, b = argument.split("=")
                if b[0]=="#" and b[1:].isnumeric():
                    kwargs[a]=int(b[1:])
                elif [b for check in ["[", "(", ")", "]"] if (check in b)]:
                    if (b[0] == "[" and b[-1] == "]") or (b[0] == "(" and b[-1] == ")"):
                        kwargs[a]=b.replace("[", "").replace("(", "").replace("]", "").replace(")", "").split(",")
                else:
                    kwargs[a]=b
            elif [argument for check in ["[","(",")","]"] if(check in argument)]:
                if (argument[0]=="[" and argument[-1]=="]") or (argument[0]=="(" and argument[-1]==")"):
                    args.append(argument.replace("[","").replace("(","").replace("]","").replace(")","").split(","))
                else:
                    raise SyntaxError(
                        "Improperly formatted list argument! Should look like: [value1,value2,etc.]"
                    )

            elif argument[0]=="#" and argument[1:].isnumeric() and kwargs=={}:
                args.append(int(argument[1:]))
            else:
                if kwargs=={}:
                    args.append(argument)
                else:
                    raise SyntaxError(
                        "positional argument follows keyword argument"
                    )

        return [args, kwargs]


if __name__=="__main__":
    COMMANDMODULE = Commands()

    @COMMANDMODULE.add_command("hi","hello", does="prints hello world")
    def hi():
        print("Hello world!")

    @COMMANDMODULE.add_command("echo","repeat","print", does="prints any passed arguments")
    def echo(*args):
        for x in args:
            print(str(x))

    @COMMANDMODULE.add_command("echotwice","saytwice", does="prints any passed arguments, but twice")
    def echotwice(*args):
        print(args)
        for x in args:
            print(str(x),str(x),sep="\n")

    @COMMANDMODULE.add_command("add", does="returns the sum of all passed arguments (integers required)")
    def add(a, b, *args):
        return sum((a,b,*args))

    print(COMMANDMODULE["echotwice"].args)
    print(inspect.signature(echotwice).parameters.values())

    for arg in inspect.signature(add).parameters.values():
        print(f"<{arg}> | {arg.kind}")

    try:
        while True:
            print(COMMANDMODULE.execute(input(">>> ")))

    except KeyboardInterrupt:
        # Code here runs when CTRL+C is pressed, or when KeyboardInterrupt is thrown as an error.
        pass

    finally:
        # Code here runs on normal program exit/keyboard interrupt. Keyboard interrupt will call both this
        # and the above except statement.
        pass
