#!/usr/bin/env python3

import json
from plumbum import local, cli
from card import UnitCard

class Compiler(cli.Application):

    def main(self, *filenames):
        for file in filenames:
            ucard = UnitCard(file)
            file = local.path(file)
            ucard.save((local.cwd / file.basename).with_suffix('.pdf'))


if __name__ == '__main__':
    Compiler.run()
