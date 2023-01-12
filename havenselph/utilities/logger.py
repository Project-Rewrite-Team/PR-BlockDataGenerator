import colorama as color

x = {"none": "", "warn": "[Warn] ", "error": "[ERROR] "}


def log(*args, mixins=(), end="\n", sep="", flush=True, mixin_color=color.Fore.LIGHTCYAN_EX,
        fore_color=color.Fore.LIGHTWHITE_EX,
        level="none"):
    if mixins:
        print(fore_color + (x[level] if level in x.keys() else "none") + (sep.join((str(key) for key in args)).format(
            *(mixin_color + mixin + fore_color for mixin in (str(value) for value in mixins)))), end=end + color.Fore.RESET,
              flush=flush)
    else:
        print(fore_color + (x[level] if level in x.keys() else "none") + (sep.join((str(key) for key in args))),
              end=end + color.Fore.RESET, flush=flush)
