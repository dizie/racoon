import platform
import sys

GD_WIN32 = 'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win32.zip'
GD_WIN64 = 'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip'
GD_MAC = 'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-macos.tar.gz'
GD_LIN32 = 'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux32.tar.gz'
GD_LIN64 = 'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz'

PJS_WIN = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip'
PJS_MAC = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip'
PJS_LIN32 = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2'
PJS_LIN64 = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-i686.tar.bz2'


def main():
    os = platform.system()
    is_64bit = sys.maxsize > 2**32


if __name__ == "__main__":
    main()
