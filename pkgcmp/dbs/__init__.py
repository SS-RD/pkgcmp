'''
Load the dbs interface
'''
# Import python libs
import os
# Import salt libs
import salt.loader

BASE_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
TAG = 'dbs'


def dbs(opts):
    '''
    Return the scnners loader funcs
    '''
    return salt.loader.LazyLoader(
            salt.loader._module_dirs(
                opts,
                TAG,
                TAG,
                base_path=BASE_PATH),
            opts,
            pack={},
            tag=TAG)
