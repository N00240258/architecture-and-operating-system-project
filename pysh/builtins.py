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
import time
import psutil
from pysh.colors import BLUE, GREEN, RESET

sortKey = ""


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

def builtin_cd(args, homeDir):
    if args != []:
        if os.path.isdir(args[0]):
            os.chdir(args[0])
        else:
            print("Please enter a valid directory")
    else:
        os.chdir(homeDir)

def builtin_cat(args):
    for file in args:
        if args != []:
            filename = file
            filepath = os.getcwd() + "/" + filename

            if os.path.isfile(filepath):
                print(f"-----{filename}-----")
                with open(filepath,"r") as f:
                    for i, line in enumerate(f, 1):
                        print(f"{i}: {line}")
            else:
                print(f"{file} not found")
        else:
            print("Please enter valid file")
            break

def builtin_head(args):
    if args[0].isdigit():
        numLines = int(args[0])
    else:
        numLines = 10
    
    for file in args:
        i = 0
        if args != [] and args != args[0]:
            filename = file
            filepath = os.getcwd() + "/" + filename

            if os.path.isfile(filepath):
                print(f"-----{filename}-----")
                with open(filepath,"r") as f:
                    for i, line in enumerate(f, 1):
                        print(f"{i}: {line}")
                        if i >= numLines:
                            break
            else:
                print(f"{file} not found")
        elif args[0].isdigit():
            continue
        else:
            print("Please enter valid file")
            break

def builtin_wc(args):
    for file in args:
        numLines = 0
        numWords = 0
        numChars = 0

        if args != [] and args != args[0]:
            filename = file
            filepath = os.getcwd() + "/" + filename

            if os.path.isfile(filepath):
                print(f"-----{filename}-----")
                with open(filepath,"r") as f:
                    for line in f:
                        numLines += 1 
                        words = line.split()
                        numWords += len(words)
                        for char in line:
                            numChars += 1
                    print(f"In the file '{file}' there are: \n")
                    print(f"{numLines} lines")
                    print(f"{numWords} words")
                    print(f"{numChars} characters")
            else:
                print(f"{file} not found")
        else:
            print("Please enter valid file")
            break

def builtin_sysinfo(args):
    while True:
        data = []
        cols = {
            "pid"     :"PID"    ,
            "user"    :"User"   ,
            "virt"    :"Virt"   ,
            "res"     :"Res"    ,
            "shr"     :"Shr"    ,
            "cpu"     :"%CPU"   ,
            "mem"     :"%MEM"   ,
            "time"    :"Time"   ,
            "process" :"Process",
        }

        for proc in psutil.process_iter([]):
            mem = proc.memory_info()
            cputimes = proc.cpu_times()
            row = {
                "pid"     : proc.pid, 
                "user"    : proc.username(), 
                "virt"    : mem.vms, 
                "res"     : mem.rss ,
                "shr"     : mem.shared, 
                "cpu"     : round(proc.cpu_percent()/100, 2), 
                "mem"     : round(proc.memory_percent(), 3), 
                "time"    : cputimes.user, 
                "process" : proc.name()
            }

            data.append(row)

        global sortKey
        if args != []:
            if args[0] == "--sort":
                if row.get(str(args[1])) != -1:
                    sortKey = str(args[1]).lower()
        else:
            sortKey = "virt"

        os.system('cls||clear')

        systemVirtMem = psutil.virtual_memory()
        print(f"Total Physical Memory: {systemVirtMem.total}")
        print(f"Memory Used          : {systemVirtMem.used}")
        print(f"Memory Free          : {systemVirtMem.free}")
        print(f"Memory Percentage    : {systemVirtMem.percent}")
        print()

        systemSwapMem = psutil.swap_memory()
        print(f"Total Swap Memory    : {systemSwapMem.total}")
        print(f"Memory Used          : {systemSwapMem.used}")
        print(f"Memory Free          : {systemSwapMem.free}")
        print(f"Memory Percentage    : {systemSwapMem.percent}")
        print()

        print(f"Total Core count     : {psutil.cpu_count()}")
        print(f"CPU usage per core   : {psutil.cpu_percent(percpu=True)}")
        print(f"CPU usage            : {psutil.cpu_percent()}")
        print()
        
        data.sort(reverse=True, key=sortFunc)
        data.insert(0, cols)
        for lines in data[0]:
                print(str(data[0][lines]).ljust(15), end="")
        print()
        
        for i in range(10):
            for lines in data[i+1]:
                print(str(data[i+1][lines]).ljust(15), end="")
                #print(lines)
                #print(f"{lines}: {data[i][lines]}")
            print()

        
        time.sleep(2)

def sortFunc(e):
    return e[sortKey]