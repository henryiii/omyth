#!/usr/bin/env python3

import json
from plumbum import local, cli
from card import UnitCard

class Compiler(cli.Application):

    def main(self, *filenames):
        for file in filenames:
            ucard = UnitCard(file)
            print(ucard)
            

if __name__ == '__main__':
    Compiler.run()
