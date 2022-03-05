from setuptools import setup, Extension
import os

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

long_description = '''A simple discrete genetic algorithm.'''

modules = ['dga']
tests = ['dga.tests']

dir_setup = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_setup, 'dga', 'release.py')) as f:
    exec(f.read())

setup(
    name='dga',
    version=__version__,
    description=long_description,
    long_description=long_description,
    packages=modules + tests,
    url='https://github.com/msparapa/dga',
    license='MIT',
    author='Michael Sparapany',
    author_email='msparapany@gmail.com',
    python_requires='>=3.5',
    install_requires=requirements,
)
