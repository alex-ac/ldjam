#!/usr/bin/env python3

import sys
import yaml
import logging
import requests
import os

from datetime import datetime
from argparse import ArgumentParser

from bot import Bot
from config import Config
from storage import Storage

def parse_args(argv=None):
    parser = ArgumentParser(description='Run game bot.')
    parser.add_argument('--config', '-c',
                        default='bot.yaml',
                        help='Configuration file.')
    parser.add_argument('--write-default',
                        default=False,
                        action='store_true',
                        help='Write default cofig file.')
    parser.add_argument('--log-level',
                        default=None,
                        help='Specify log level.')
    return parser.parse_args(argv)

def run(argv=None):
    args = parse_args(argv)

    if args.write_default:
        with open(args.config, 'w') as f:
            f.write(Config().save())
        return

    with open(args.config) as f:
        config = Config.load(f.read())

    if args.log_level:
        config.log_level = log_level

    logging.basicConfig(level=config.log_level)

    try:
        with open(config.storage_file) as f:
            storage = Storage.load(f.read())
    except IOError:
        storage = Storage()

    try:
        Bot(config.telegram_token, storage).run()
    except:
        with open(config.storage_file, 'w') as f:
            f.write(storage.save())
        raise

if __name__ == '__main__':
    sys.exit(run())
