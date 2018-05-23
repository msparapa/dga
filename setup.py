from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

modules = []
tests = []

setup(
    name='dga',
    version='0.1.3',
    packages=['dga'] + modules + tests,
    url='https://github.com/msparapa/dga',
    license='MIT',
    author='Michael Sparapany',
    author_email='msparapa@purdue.edu',
    description='A discrete genetic algorithm.',
    python_requires='>=3',
    install_requires=requirements,
    include_package_data=True
)
