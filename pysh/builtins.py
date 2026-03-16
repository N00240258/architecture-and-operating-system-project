"""
Built-in commands for pysh.

Built-in commands are handled directly by the shell, rather than by
running an external program. For example, 'cd' must be a built-in
because changing directory needs to affect the shell process itself.

Each built-in is a function that takes a list of string arguments.
Look at builtin_pwd below as a complete example to follow.
"""

import os
import sys
import grp
import psutil
from pysh.colors import BLUE, GREEN, RESET


# ---------------------------------------------------------------------------
# Example built-in: pwd
# ---------------------------------------------------------------------------


def builtin_pwd(args):
    """
    Print the current working directory.

    Uses os.getcwd() which asks the operating system for the current
    working directory of this process.

    Example usage:
        pysh /home/student $ pwd
        /home/student
    """
    print(os.getcwd())


# ---------------------------------------------------------------------------
# Example built-in: exit
# ---------------------------------------------------------------------------


def builtin_exit(args):
    """
    Exit the shell.

    Raises SystemExit which is caught by the main loop in shell.py
    to break out of the loop cleanly.
    """
    sys.exit(0)

# ---------------------------------------------------------------------------
# TODO: Implement the remaining built-in commands below.
#       Each function receives a list of string arguments.
#       Look at builtin_pwd above as an example to follow.
# ---------------------------------------------------------------------------

def builtin_sum(args):
    sum = 0
    for num in args:
        sum += int(num)
    print(sum)

def builtin_procinfo(args):
    if args == []:
        print("Please insert a PID")
    elif int(args) == psutil.Process(os.getpid()):
        print("Please enter valid PID")
    else:
        proc = psutil.Process(int(args))
        #print(proc.pid)
        print(f"Process name: {proc.name()}")
        print(f"Process status: {proc.status()}")
        print(f"Process CPU usage: {proc.cpu_percent()}%")
        print(f"Process run time: {proc.cpu_times().user}s")
        mem = proc.memory_info()
        print(f"Process physical ram usage: {mem.rss}")
        print(f"Process virtual ram usage: {mem.vms}")

def builtin_cd(args):
    if args != []:
        os.chdir(args[0])
    else:
        os.chdir(os.getcwd())
