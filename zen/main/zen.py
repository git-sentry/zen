#/usr/local/bin/python3

import os

from github3 import login

def main():
    git = login(token=os.environ['ZEN'])
    print(f'Hello, I am {git.me()}')

if __name__ == '__main__':
    main()
