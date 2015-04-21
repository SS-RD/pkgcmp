'''
Parse CLI options
'''
# Import python libs
import os
import copy
import argparse
# Import pkgcmp libs
import pkgcmp.scan
# Import third party libs
import yaml

DEFAULTS = {}


def parse():
    '''
    Parse!!
    '''
    parser = argparse.ArgumentParser(description='The pkgcmp map generator')
    parser.add_argument(
            '--config',
            dest='config',
            default='/etc/pkgcmp/pkgcmp',
            help='The location of the pkgcmp config file')
    opts = parser.parse_args().__dict__
    conf = config(opts['config'])
    for key in opts:
        if opts[key] is not None:
            conf[key] = opts[key]
    return conf


def config(cfn):
    '''
    Read in the config file
    '''
    ret = copy.copy(DEFAULTS)
    if os.path.isfile(cfn):
        with open(cfn, 'r') as cfp:
            conf = yaml.safe_load(cfp)
            print(conf)
            ret.update(conf)
    return ret


class PkgCmp:
    '''
    Build and run the application
    '''
    def __init__(self):
        self.opts = parse()
        self.scan = pkgcmp.scan.Scanner(self.opts)

    def run(self):
        self.scan.run()
