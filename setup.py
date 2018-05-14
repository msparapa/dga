from setuptools import setup

setup(
    name='dga',
    version='0.1a',
    packages=['optim', 'optim.problem', 'optim.algorithms', 'optim.algorithms.geneticalgorithm'],
    url='https://github.com/msparapa/dga',
    license='MIT',
    author='Michael Sparapany',
    author_email='msparapa@purdue.edu',
    description='A discrete genetic algorithm.',
    python_requires='>=3'
)
