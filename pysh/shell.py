"""
pysh — A minimal shell built in Python.

This is the main module. It runs the shell loop:
  1. Display a prompt
  2. Read a line of input
  3. Parse it into a command and arguments
  4. Execute the command
  5. Repeat
"""

import grp
import os
import subprocess
import psutil


from pysh.builtins import builtin_exit, builtin_pwd, builtin_sum, builtin_procinfo, builtin_cd, builtin_cat, builtin_head, builtin_wc, builtin_sysinfo, builtin_download
from pysh.colors import BLUE, GREEN, RESET

homeDir = os.getcwd()

helpList = [
            "pwd - Displays current directory",
            "cd - Change directory or return to home directory"
            "help - Displays a list of all commands",
            "procpid - Gets the current process ID",
            "procinfo - Displays some information about the process",
            "cat - Reads the content of a file",
            "wc - Displays how many words, lines and characters are in a file",
            "head - Displays a specified amount of lines of a line starting from the beginning",
            "sysinfo - Displays info of the system",
            "download - Downloads files from a given link. --status to show information on current downloads",
            "exit - Exits the shell",
            ]

def prompt():
    """Return the shell prompt string showing the current directory."""
    cwd = os.getcwd()
    user = os.environ.get("USER")
    group = grp.getgrgid(os.getgid()).gr_name

    return f"{GREEN}{user}@{group}{RESET}:{BLUE}{cwd}{RESET}$ "


def parse(line):
    """
    Parse a line of input into a command name and a list of arguments.

    Example:
        parse("echo hello world") returns ("echo", ["hello", "world"])
        parse("") returns (None, [])
    """
    parts = line.strip().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def execute(command, args):
    """
    Execute a command with the given arguments.

    First checks if the command is a built-in. If not, tries to run it
    as an external program using subprocess.
    """

    # TODO: Add your own built-in commands here
    
    if command == "pwd":
        builtin_pwd(args)
    elif command == "help":
        for command in helpList:
            print(command)
    elif command == "sum":
        builtin_sum(args)
    elif command == "cd":
        builtin_cd(args, homeDir)

    elif command == "procpid":
        proc = psutil.Process(os.getpid())
        print(proc.pid)
    elif command == "procinfo":
        builtin_procinfo(args)

    elif command == "exit":
        builtin_exit(args)

    elif command == "cat":
        builtin_cat(args)
    elif command == "wc":
        builtin_wc(args)

    elif command == "head":
        builtin_head(args)
    elif command == "sysinfo":
        builtin_sysinfo(args)

    elif command == "download":
        builtin_download(args)
    else:
        # Run external commands as a child process.
        # subprocess.run will search for the command on the system PATH,
        # run it, and wait for it to finish before returning.
        try:
            subprocess.run([command] + args)
        except FileNotFoundError:
            print(f"pysh: {command}: command not found")


def main():
    """Entry point for the shell."""

    print(
        r"""
 __
 \ \
  \ \
  / /
 /_/   ______
      /_____/"""
    )

    print()
    print("Welcome to pysh! Type 'help' to see available commands.\n")

    while True:
        try:
            line = input(prompt())
            commands = line.split("&&")
            for i in range(len(commands)):
                command, args = parse(commands[i])

                # If the user just pressed Enter, show the prompt again
                if command is None:
                    continue

                execute(command, args)

        except EOFError:
            # Ctrl+D — exit the shell
            print("\nGoodbye!")
            break

        except KeyboardInterrupt:
            # Ctrl+C — don't exit, just move to a new line
            print()
            continue

        except SystemExit:
            # The exit command was called
            break

# https://docs.python.org/3/library/readline.html