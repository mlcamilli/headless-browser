from setuptools import setup, find_packages

requires = [
    'PyVirtualDisplay==0.2',
    'selenium==2.53.2',
]

__version__ = '0.0.2'


setup(
    name='headless-browser',
    author="Matt Camilli",
    author_email="mlcamilli@gmail.com",
    version=__version__,
    url="https://github.com/mlcamilli/headless-browser",
    install_requires=requires,
    packages=find_packages(exclude=['tests']),
)
