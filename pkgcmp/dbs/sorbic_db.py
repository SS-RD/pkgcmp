'''
Store data in a sorbic database
'''
# Import python libs
import os
# Import sorbic libs
import sorbic.db

__virtualname__ = 'sorbic'


def __virtual__():
    return __virtualname__


def save_pkg(pkg):
    '''
    Save the data for the given package
    '''
    db = sorbic.db.DB(os.path.join(__opts__['cachedir'], 'sorbic'))
    key = '{}/{}'.format(pkg['distro'], pkg['name'])
    db.insert(key, pkg)
