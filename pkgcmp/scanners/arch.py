'''
Scan an Arch Linux repo full of packages and create the data map
'''
# Download packages
# Extract packages, one at a time
# generate list of files in package
# Save package name, version distro and package list

# Import python libs
import os
import shutil
import tempfile
import subprocess


def _parse_pkginfo(path):
    '''
    Return the pkginfo as a dict
    '''
    ret = {}
    with open(path, 'r') as fp_:
        for line in fp_:
            line = line.strip()
            if line.startswith('#'):
                continue
            if not line.find('='):
                continue
            key, val = line.split('=')
            ret[key] = val
    return ret

def reposync():
    '''
    Download the repo packages to be scanned
    '''
    dest = os.path.join(__opts__['cachedir'], 'archpkg')
    if not os.path.isdir(dest):
        os.makedirs(dest)
    cmd = 'rsync -rtlvH --delete-after --delay-updates --safe-links --max-delete=1000 {0} {1}'.format(__opts__['arch_linux_mirror'], dest)
    subprocess.check_output(cmd, shell=True)


def scanpkg(path):
    '''
    Extract a single package to a temporary location, scan the contents and return the content data
    '''
    ret = {}
    files = []
    dirs = []
    tmp = tempfile.mkdtemp(__opts__['cachedir'])
    shutil.copy(path, tmp)
    orig = os.pwd()
    os.chdir(tmp)
    cmd = 'tar xvf {0}'.format(path)
    subprocess.check_output(cmd, shell=True)
    ret.update(_parse_pkginfo(os.path.join(tmp, '.PKGINFO')))
    ret['distro'] = 'arch'
    ret['name'] = ret['pkgname']
    ret['version'] = ret['pkgver']
    for root, dirs, files in os.walk(tmp):
        for fn_ in files:
            full = os.path.join(root, fn_)
            files.append(full[len(tmp):])
        for dn_ in dirs:
            full = os.path.join(root, dn_)
            dirs.append(full[len(tmp):])
    ret['files'] = files
    ret['dirs'] = dirs
    os.chdir(orig)
    shutil.rmtree(tmp)
    return ret


def iterpkgs():
    '''
    Return a generator to iterate over the named packages
    '''
    dest = os.path.join(__opts__['cachedir'], 'archpkg')
    for root, dirs, files in os.walk(dest):
        for fn_ in files:
            if fn_.endswith('.pkg.tar.xz'):
                yield(os.path.join(root, fn_))
