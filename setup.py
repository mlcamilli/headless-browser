from setuptools import setup, find_packages
import re

requires = [
    'PyVirtualDisplay==0.2',
    'selenium==2.53.2',
]

__version__ = ''
with open('trackmaven_drf/__init__.py', 'r') as fd:
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

if not __version__:
    raise RuntimeError('Cannot find version information')


setup(
    name='headless-browser',
    author="Matt Camilli",
    author_email="mlcamilli@gmail.com",
    version=__version__,
    url="https://github.com/mlcamilli/headless-browser",
    install_requires=requires,
    packages=find_packages(exclude=['tests']),
)
