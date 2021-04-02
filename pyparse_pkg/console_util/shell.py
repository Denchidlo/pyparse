import os
from pathlib import Path

home = str(Path.home())

os.system('rm -rf ~/lib')
os.system('mkdir ~/lib')
os.system('cp -a . ~/lib')
os.system('chmod +x ~/lib/main.py')
with open(home + '/.bashrc', 'a') as file:
    file.write("alias redump='" + "~/lib/main.py'")
