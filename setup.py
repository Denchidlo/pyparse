from setuptools import find_packages, setup

setup(
    name='lib',
    packages=find_packages(include=['lib']),
    version='0.1.0',
    description='Serializer/Deserializer',
    author='Me',
    license='MIT',
    python_requires='>=3.8',
)
