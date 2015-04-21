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
# Import third party libs
import yaml

DEB_REPOS = [
        'debian_repo',
        'ubuntu_repo',
        ]


def reposync():
    '''
    Download the repo packages to be scanned
    '''
    dest = os.path.join(__opts__['cachedir'], 'debianpkg')
    if not os.path.isdir(dest):
        os.makedirs(dest)
    for repo in DEB_REPOS:
        cmd = 'rsync --links --hard-links --times --verbose --recursive --delay-updates --files-from :indices/files/typical.files rsync://{} {}'.format(__opts__[repo], dest)
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
    cmd = 'ar vx {0}'.format(path)
    subprocess.check_output(cmd, shell=True)
    cmd = 'tar xvf {}'.format(os.path.join(tmp, 'data.tar.*'))
    subprocess.check_output(cmd, shell=True)
    cmd = 'tar xvf {}'.format(os.path.join(tmp, 'control.tar.gz'))
    subprocess.check_output(cmd, shell=True)
    ret.update(yaml.safe_load(os.path.join(tmp, 'control')))
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
    dest = os.path.join(__opts__['cachedir'], 'debianpkg')
    for root, dirs, files in os.walk(dest):
        for fn_ in files:
            if fn_.endswith('.deb'):
                yield(os.path.join(root, fn_))
