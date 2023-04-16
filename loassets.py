import logging

import fire

from command import Command

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    fire.Fire(Command)
