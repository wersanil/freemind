#!/usr/bin/env python3
"""
FreeMind - Cross-platform operating environment in Python
Inspired by the philosophy of GNU
"""

import os
import sys
import time
import subprocess
from datetime import datetime
import platform
import json
import importlib.util
from pathlib import Path

# Terminal setup for cross-platform compatibility
if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm-256color'

# Determine platform once for optimization
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"

# Try to import psutil
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

class FreeMind:
    """Main class of the system"""
    
    def __init__(self):
        self.version = "0.3.1"
        self.name = "FreeMind"
        self.commands = {}
        self.current_dir = os.path.expanduser("~")
        self.running = True
        self.has_terminal = sys.stdout.isatty()
        
        # Path setup for modules (commented out - module system disabled)
        # self.base_path = os.path.dirname(os.path.abspath(__file__))
        # self.modules_path = os.path.join(self.base_path, "modules")
        # self.loaded_modules = {}
        
        # Create modules folder if it doesn't exist (commented out)
        # os.makedirs(self.modules_path, exist_ok=True)
        # for category in ['games', 'utils', 'system']:
        #     os.makedirs(os.path.join(self.modules_path, category), exist_ok=True)
        
        # Color setup for Windows
        if IS_WINDOWS:
            os.system("color")
        
        self.init_commands()
        
    def init_commands(self):
        """Initialization of built-in commands"""
        self.commands = {
            # Main commands
            'help': self.cmd_help,
            'exit': self.cmd_exit,
            'quit': self.cmd_exit,
            'clear': self.cmd_clear,
            'reboot': self.cmd_reboot,
            'shutdown': self.cmd_shutdown,
            
            # File operations
            'ls': self.cmd_ls,
            'dir': self.cmd_ls,
            'pwd': self.cmd_pwd,
            'cd': self.cmd_cd,
            'mkdir': self.cmd_mkdir,
            'rm': self.cmd_rm,
            'del': self.cmd_rm,
            'cat': self.cmd_cat,
            'type': self.cmd_cat,
            'touch': self.cmd_touch,
            'edit': self.cmd_edit,
            
            # System information
            'date': self.cmd_date,
            'time': self.cmd_date,
            'sysinfo': self.cmd_sysinfo,
            'info': self.cmd_sysinfo,
            'whoami': self.cmd_whoami,
            'ps': self.cmd_ps,
            'neofetch': self.cmd_neofetch,
            'fetch': self.cmd_neofetch,
            
            # Applications
            'echo': self.cmd_echo,
            'calc': self.cmd_calc,
            'calcfig': self.cmd_calcfig,
            'weather': self.cmd_weather,
            
            # Module system (disabled)
            # 'modules': self.cmd_modules,
            # 'module': self.cmd_module,
            
            # Platform dependent
            'windows': self.cmd_windows,
            'linux': self.cmd_linux,
        }
        
    def colorize(self, text, color_code):
        """Adds color to text (cross-platform version)"""
        if not self.has_terminal:
            return text
            
        colors = {
            'red': '31',
            'green': '32',
            'yellow': '33',
            'blue': '34',
            'magenta': '35',
            'cyan': '36',
            'white': '37',
        }
        
        if color_code in colors:
            # Colors work differently in Windows
            if IS_WINDOWS:
                # Simple color emulation for Windows
                return text
            else:
                return f"\033[{colors[color_code]}m{text}\033[0m"
        return text
        
    def boot(self):
        """System boot"""
        self.clear_screen()
        self.show_boot_screen()
        time.sleep(1.5)
        self.clear_screen()
        self.main_loop()
        
    def show_boot_screen(self):
        """Shows loading screen"""
        os_name = "Windows" if IS_WINDOWS else "Linux"
        boot_screen = f"""
╔══════════════════════════════════════════════════════════╗
║                    {self.name} v{self.version}                       ║
║               "Freedom. Simplicity. Control"             ║
╠══════════════════════════════════════════════════════════╣
║   The system is ready to work!                           ║
╚══════════════════════════════════════════════════════════╝
        """
        print(boot_screen)
        
    def clear_screen(self):
        """Screen clearing (cross-platform)"""
        os.system('cls' if IS_WINDOWS else 'clear')
        
    def get_prompt(self):
        """Generates a command prompt"""
        try:
            user = os.getlogin()
        except:
            user = 'user'
        
        host = platform.node()
        dir_name = os.path.basename(self.current_dir) or '/'
        
        prompt = f"{self.colorize(user, 'green')}@{self.colorize(host, 'cyan')} "
        prompt += f"{self.colorize(dir_name, 'blue')}$ "
        return prompt
        
    def main_loop(self):
        """Main loop of the system"""
        print(f"\n{self.colorize('Welcome to ' + self.name + '!', 'yellow')}")
        print(f"{self.colorize('Type help for a list of commands', 'cyan')}\n")
        
        while self.running:
            try:
                command = input(self.get_prompt()).strip()
                if command:
                    self.execute_command(command)
            except KeyboardInterrupt:
                print("\nUse 'exit' to exit")
            except EOFError:
                break
                
    def execute_command(self, command_line):
        """Executes a command"""
        parts = command_line.split()
        if not parts:
            return
            
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd in self.commands:
            try:
                self.commands[cmd](args)
            except Exception as e:
                print(f"{self.colorize(f'Error: {e}', 'red')}")
        else:
            self.execute_system_command(command_line)
            
    def execute_system_command(self, command):
        """Executes a system command"""
        try:
            result = subprocess.run(command, shell=True, 
                                  capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"{self.colorize(f'Error: {result.stderr}', 'red')}")
        except Exception as e:
            print(f"{self.colorize(f'Command not found: {command}', 'red')}")
    
    # ===== MAIN COMMANDS =====
    
    def cmd_help(self, args):
        """Shows help"""
        print(f"\n{self.colorize('Available commands:', 'yellow')}")
        print("=" * 60)
        
        categories = {
            ' Files': ['ls', 'pwd', 'cd', 'mkdir', 'rm', 'cat', 'touch', 'edit'],
            ' System': ['sysinfo', 'whoami', 'date', 'ps', 'neofetch'],
            ' Control': ['clear', 'exit', 'reboot', 'shutdown'],
            ' Apps': ['calc', 'calcfig', 'weather', 'echo'],
            # ' Modules': ['modules', 'module'],
            ' Platform': ['windows', 'linux'],
        }
        
        for category, cmd_list in categories.items():
            print(f"\n{self.colorize(category, 'cyan')}")
            for cmd in sorted(cmd_list):
                if cmd in self.commands:
                    doc = self.commands[cmd].__doc__ or "No description"
                    print(f"  {cmd:10} - {doc}")
        print()
    
    # ===== FILE COMMANDS =====
    
    def cmd_ls(self, args):
        """Shows the contents of a directory"""
        path = args[0] if args else self.current_dir
        show_all = '-a' in args or '/a' in args
        
        try:
            items = os.listdir(path)
            if not show_all:
                items = [i for i in items if not i.startswith('.')]
            
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
            
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    print(self.colorize(f"{item}/", 'blue'))
                elif os.access(full_path, os.X_OK):
                    print(self.colorize(f"{item}*", 'green'))
                else:
                    print(item)
        except Exception as e:
            print(f"{self.colorize(f'Error: {e}', 'red')}")
    
    def cmd_pwd(self, args):
        """Shows the current directory"""
        print(self.colorize(self.current_dir, 'cyan'))
    
    def cmd_cd(self, args):
        """Changes directory"""
        path = args[0] if args else os.path.expanduser("~")
        try:
            os.chdir(path)
            self.current_dir = os.getcwd()
        except Exception as e:
            print(f"{self.colorize(f'Error: {e}', 'red')}")
    
    def cmd_mkdir(self, args):
        """Creates a directory"""
        if not args:
            print(f"{self.colorize('Specify the directory name', 'red')}")
            return
        try:
            os.mkdir(args[0])
            print(f"Directory '{args[0]}' created")
        except Exception as e:
            print(f"{self.colorize(f'Error: {e}', 'red')}")
    
    def cmd_rm(self, args):
        """Deletes a file or directory"""
        if not args:
            print(f"{self.colorize('Specify the file to delete', 'red')}")
            return
        
        for path in args:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"File '{path}' deleted")
                elif os.path.isdir(path):
                    os.rmdir(path)
                    print(f"Directory '{path}' deleted")
                else:
                    print(f"{self.colorize(f'{path} not found', 'red')}")
            except Exception as e:
                print(f"{self.colorize(f'Error: {e}', 'red')}")
    
    def cmd_cat(self, args):
        """Shows file content"""
        if not args:
            print(f"{self.colorize('Specify the file', 'red')}")
            return
        try:
            with open(args[0], 'r', encoding='utf-8') as f:
                print(f.read())
        except Exception as e:
            print(f"{self.colorize(f'Error: {e}', 'red')}")
    
    def cmd_touch(self, args):
        """Creates an empty file"""
        if not args:
            print(f"{self.colorize('Specify the file name', 'red')}")
            return
        for filename in args:
            try:
                with open(filename, 'a'):
                    os.utime(filename, None)
                print(f"File '{filename}' created")
            except Exception as e:
                print(f"{self.colorize(f'Error: {e}', 'red')}")
    
    def cmd_edit(self, args):
        """Simple text editor"""
        if not args:
            print(f"{self.colorize('Specify the file to edit', 'red')}")
            return
        
        filename = args[0]
        lines = []
        
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                print(f"Editing {filename} (:wq to save):")
            except:
                print(f"Could not read {filename}")
                return
        else:
            print(f"Creating {filename} (:wq to save):")
        
        new_lines = []
        line_num = 1
        
        for line in lines:
            print(f"{line_num:3d}| {line.rstrip()}")
            line_num += 1
        
        while True:
            try:
                user_input = input(f"{line_num:3d}| ")
                if user_input == ':wq':
                    break
                new_lines.append(user_input + '\n')
                line_num += 1
            except KeyboardInterrupt:
                print("\nSaving...")
                break
        
        if new_lines:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"File {filename} saved")
            except Exception as e:
                print(f"{self.colorize(f'Error: {e}', 'red')}")
    
    # ===== SYSTEM COMMANDS =====
    
    def cmd_date(self, args):
        """Shows date and time"""
        now = datetime.now()
        print(f"{self.colorize('Date:', 'yellow')} {now.strftime('%d.%m.%Y')}")
        print(f"{self.colorize('Time:', 'yellow')} {now.strftime('%H:%M:%S')}")
    
    def cmd_echo(self, args):
        """Outputs text"""
        print(' '.join(args))
    
    def cmd_whoami(self, args):
        """Shows username"""
        try:
            print(os.getlogin())
        except:
            print('user')
    
    def cmd_clear(self, args):
        """Clears screen"""
        self.clear_screen()
    
    def cmd_exit(self, args):
        """Exits the system"""
        print(f"\n{self.colorize('Session ended...', 'yellow')}")
        self.running = False
    
    def cmd_reboot(self, args):
        """Reboots the system"""
        print(f"\n{self.colorize('Rebooting...', 'yellow')}")
        time.sleep(1)
        self.clear_screen()
        self.boot()
    
    def cmd_shutdown(self, args):
        """Shuts down the system"""
        print(f"\n{self.colorize('Shutting down...', 'yellow')}")
        time.sleep(1)
        sys.exit(0)
    
    def cmd_sysinfo(self, args):
        """System information"""
        print(f"\n{self.colorize('=== SYSTEM INFORMATION ===', 'yellow')}")
        print(f"OS: {platform.system()} {platform.release()}")
        print(f"Host: {platform.node()}")
        print(f"User: {self.cmd_whoami([])}")
        print(f"Directory: {self.current_dir}")
        print(f"Python: {platform.python_version()}")
        
        if HAS_PSUTIL:
            try:
                print(f"\n{self.colorize('Hardware:', 'yellow')}")
                print(f"CPU: {psutil.cpu_count()} cores")
                print(f"CPU usage: {psutil.cpu_percent()}%")
                
                mem = psutil.virtual_memory()
                print(f"RAM: {mem.total / 1024**3:.1f}GB total, {mem.percent}% used")
                
                disk = psutil.disk_usage('/')
                print(f"Disk: {disk.total / 1024**3:.1f}GB total, {disk.percent}% used")
            except:
                pass
        else:
            print(f"\n{self.colorize('Install psutil for full information', 'yellow')}")
        print()
    
    def cmd_ps(self, args):
        """Shows processes"""
        if not HAS_PSUTIL:
            print(f"{self.colorize('Install psutil', 'yellow')}")
            return
        
        try:
            print(f"\n{'PID':>6} {'Name':20} {'CPU%':>6} {'MEM%':>6}")
            print("-" * 40)
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    print(f"{info['pid']:6} {info['name'][:20]:20} "
                          f"{info['cpu_percent'] or 0:6.1f} {info['memory_percent'] or 0:6.1f}")
                except:
                    pass
        except:
            print("Process information not available")
    
    # ===== APPLICATIONS =====
    
    def cmd_calc(self, args):
        """Simple calculator"""
        print(f"\n{self.colorize('Calculator (q - exit)', 'yellow')}")
        while True:
            try:
                expr = input("calc> ").strip()
                if expr.lower() == 'q':
                    break
                result = eval(expr)
                print(f"= {result}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")

    def cmd_calcfig(self, args):
        """Rectangle parameters calculator"""
        
        def to_int(value):
            if value is None:
                return None
            if isinstance(value, (int, float)):
                return int(value)
            try:
                return int(str(value))
            except (ValueError, TypeError):
                try:
                    return int(value.value)
                except AttributeError:
                    pass
                try:
                    return int(value.get())
                except (AttributeError, TypeError, ValueError):
                    pass
                return None

        d_int = None
        w_int = None
        
        if len(args) >= 2:
            d_int = to_int(args[0])
            w_int = to_int(args[1])
        
        if d_int is None or w_int is None:
            print("Enter rectangle parameters:")
            while True:
                try:
                    d_int = int(input("Length: "))
                    w_int = int(input("Width: "))
                    break
                except ValueError:
                    print("Error: enter an integer.")

        length, width = d_int, w_int

        perimeter = (length + width) * 2
        area = length * width

        line_len = 105
        print(f"{'RECTANGLE PARAMETERS'.center(line_len)}")
        line = "-" * line_len
        print(line)
        
        col1 = 20
        col2 = 15
        col3 = 35
        col4 = 30

        header = (f"|{'Length'.center(col1)}|"
                  f"{'Width'.center(col2)}|"
                  f"{'Perimeter'.center(col3)}|"
                  f"{'Area'.center(col4)}|")
        print(header)
        print(line)

        fmt_len = format(length, "20,.0f")
        fmt_wid = format(width, "15,.0f")
        fmt_per = format(perimeter, "35,.0f")
        fmt_are = format(area, "30,.0f")

        data_row = f"|{fmt_len}|{fmt_wid}|{fmt_per}|{fmt_are}|"
        print(data_row)
        print(line)
    
    def cmd_weather(self, args):
        """Demo weather"""
        print(f"\n{self.colorize('Weather:', 'yellow')}")
        print(f"Temperature: +15°C")
        print(f"Humidity: 65%")
        print(f"Wind: 3 m/s\n")
    
    # ===== PLATFORM DEPENDENT COMMANDS =====
    
    def cmd_windows(self, args):
        """Windows information"""
        if IS_WINDOWS:
            print(f"\n{self.colorize('Windows:', 'yellow')}")
            print(f"Version: {platform.version()}")
            print(f"Architecture: {platform.machine()}")
        else:
            print("This command is only available on Windows")
    
    def cmd_linux(self, args):
        """Linux information"""
        if IS_LINUX:
            print(f"\n{self.colorize('Linux:', 'yellow')}")
            try:
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('PRETTY_NAME='):
                            print(f"Distribution: {line.split('=')[1].strip().strip('\"')}")
            except:
                print(f"Kernel: {platform.release()}")
        else:
            print("This command is only available on Linux")
    
    # ===== MODULE SYSTEM (DISABLED) =====
    
    # Module system functions have been commented out
    # They will be reimplemented in a future version
    
    def cmd_neofetch(self, args):
        """Shows ASCII logo"""
        logo = f"""
{self.colorize('       ██╗██████╗ ███████╗███████╗', 'blue')}
{self.colorize('       ██║██╔══██╗██╔════╝██╔════╝', 'cyan')}
{self.colorize('       ██║██████╔╝█████╗  █████╗  ', 'green')}
{self.colorize('  ██   ██║██╔═══╝ ██╔══╝  ██╔══╝  ', 'yellow')}
{self.colorize('  ╚█████╔╝██║     ██║     ██║     ', 'red')}
{self.colorize('   ╚════╝ ╚═╝     ╚═╝     ╚═╝     ', 'magenta')}
{self.colorize('═══════════════════════════════════', 'white')}
{self.colorize('    OPEN KNOWLEDGE • FREE ACCESS   ', 'cyan')}
{self.colorize('═══════════════════════════════════', 'white')}

{self.colorize('User:', 'yellow')} {self.cmd_whoami([])}
{self.colorize('System:', 'yellow')} {platform.system()} {platform.release()}
{self.colorize('Python:', 'yellow')} {platform.python_version()}
        """
        print(logo)


# ===== EXTERNAL FUNCTIONS =====

def main():
    """Main function"""
    os_instance = FreeMind()
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            print("FreeMind - Operating environment in Python")
            print("\nUsage:")
            print("  python freemind.py     - System startup")
            print("  python freemind.py demo - Demo mode")
            return
        elif sys.argv[1] == 'demo':
            demo_mode()
            return
    
    try:
        os_instance.boot()
    except Exception as e:
        print(f"Critical error: {e}")
        input("Press Enter to exit...")

def demo_mode():
    """Demonstration mode"""
    print("\n" + "="*60)
    print("FreeMind DEMONSTRATION")
    print("="*60 + "\n")
    
    os_instance = FreeMind()
    os_instance.show_boot_screen()
    time.sleep(1)
    
    print(f"\n{os_instance.colorize('Available commands:', 'yellow')}")
    print("-" * 40)
    
    for i, cmd in enumerate(sorted(os_instance.commands.keys())[:15]):
        doc = os_instance.commands[cmd].__doc__ or "..."
        print(f"  {cmd:12} - {doc}")
    
    print("\n  ... and more")
    print(f"\n{os_instance.colorize('System information:', 'yellow')}")
    print("-" * 40)
    os_instance.cmd_sysinfo([])
    
    print(f"\n{os_instance.colorize('ASCII logo:', 'yellow')}")
    print("-" * 40)
    os_instance.cmd_neofetch([])
    
    print(f"\n{os_instance.colorize('To run the full version:', 'yellow')}")
    print("  python freemind.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
