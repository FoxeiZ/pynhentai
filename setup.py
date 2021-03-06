from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pynhentai',  # How you named your package folder (MyLib)
    packages=['pynhentai'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='gpl-3.0',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Lightweight async lib for nhentai',  # Give a short description about your library
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Foxeiz',  # Type in your name
    author_email='57582539+FoxeiZ@users.noreply.github.com',  # Type in your E-Mail
    url='https://github.com/FoxeiZ/pynhentai',  # Provide either the link to your github or to your website
    download_url='https://github.com/FoxeiZ/pynhentai/archive/v0.1.tar.gz',
    keywords=['nhentai', 'anime'],  # Keywords that define your package best
    install_requires=[
        'aiohttp',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Multimedia',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  # Again, pick a license
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
