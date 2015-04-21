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

RED_REPOS = [
        'cent_repo',
        'fedora_repo',
        ]


def reposync():
    '''
    Download the repo packages to be scanned
    '''
    dest = os.path.join(__opts__['cachedir'], 'redpkg')
    if not os.path.isdir(dest):
        os.makedirs(dest)
    for repo in RED_REPOS:
        fdest = os.path.join(dest, repo)
        cmd = 'rsync --links --hard-links --times --verbose --recursive --delay-updates --files-from :indices/files/typical.files rsync://{} {}'.format(__opts__[repo], fdest)
        subprocess.check_output(cmd, shell=True)


def scanpkg(path):
    '''
    Extract a single package to a temporary location, scan the contents and return the content data
    '''
    ret = {}
    cmd = 'rpm -q -filebypkg -p {0}'.format(path)
    file_out = subprocess.check_output(cmd, shell=True)
    cmd = 'rpm -q -i -p {0}'.format(path)
    meta_out = subprocess.check_output(cmd, shell=True)
    ret.update(_parse_meta_out(meta_out))
    ret.update(_parse_file_out(file_out))
    return ret


def iterpkgs():
    '''
    Return a generator to iterate over the named packages
    '''
    dest = os.path.join(__opts__['cachedir'], 'redpkg')
    for repo in RED_REPOS:
        fdest = os.path.join(dest, repo)
        for root, dirs, files in os.walk(fdest):
            for fn_ in files:
                if fn_.endswith('.deb'):
                    yield(os.path.join(root, fn_))
