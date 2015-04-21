'''
Load the scanners interface
'''
# Import python libs
import os
# Import salt libs
import salt.loader

BASE_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

def scanners(opts):
    '''
    Return the scnners loader funcs
    '''
    return salt.loader.LazyLoader(
            salt.loader._module_dirs(
                opts,
                'scanners',
                'scanners',
                base_path=BASE_PATH),
            opts,
            pack={},
            tag='scanners')
