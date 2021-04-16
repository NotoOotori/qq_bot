from os import path

import nonebot

from config import *


def main():
    nonebot.init()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'src', 'plugins'),
        'src.plugins'
    )
    nonebot.run(host=HOST, port=PORT)

if __name__ == '__main__':
    main()
