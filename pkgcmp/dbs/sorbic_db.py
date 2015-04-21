'''
Store data in a sorbic database
'''
# Import sorbic libs
import sorbic.db


def save_pkg(pkg):
    '''
    Save the data for the given package
    '''
    db = sorbic.db.DB(__opts__['sorbic']['root'])
    key = '{}/{}'.format(pkg['distro'], pkg['name'])
    db.insert(key, pkg)
