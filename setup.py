from setuptools import find_packages, setup

setup(
    name='lib',
    packages=find_packages(),
    version='0.1.25',
    description='Serializer/Deserializer',
    author='Me',
    license='MIT',
    python_requires='>=3.8',
)

import os
from pathlib import Path

home = str(Path.home())

os.system('rm -rf ~/lib')
os.system('mkdir ~/lib')
os.system('cp -a . ~/lib')
os.system('chmod +x ~/lib/lib/redump.py')
with open(home + '/.bashrc', 'a') as file:
    file.write("alias redump='" + "~/lib/lib/redump.py'")

