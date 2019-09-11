from setuptools import setup

APP = ['client.py']
DATA_FILES = []
OPTIONS = {
 'iconfile':'logo.icns',
 'argv_emulation': True,
 'packages': ['cffi','cryptography'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)