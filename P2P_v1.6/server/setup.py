from setuptools import setup

APP = ['Server.py']
DATA_FILES = ['buffer.py','otp.py','QRcode.py']
OPTIONS = {
 'iconfile':'logo.icns',
 'argv_emulation': True,
 'packages': ['cffi','cryptography','pyotp','pyqrcode'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
