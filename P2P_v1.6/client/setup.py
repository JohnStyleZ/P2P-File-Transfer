from setuptools import setup

APP = ['Client.py']
DATA_FILES = []
OPTIONS = {
 'iconfile':'logo.icns',
 'argv_emulation': True,
 'packages': ['cffi','cryptography','pyqrcode','pyotp'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
