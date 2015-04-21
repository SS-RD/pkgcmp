'''
Execute the full os scanning maddness!
'''
# Import pkgcmp libs
import pkgcmp.scanners
import pkgcmp.dbs


class Scanner:
    def __init__(self, opts):
        self.opts = opts
        self.scanners = pkgcmp.scanners.scanners(self.opts)
        self.dbs = pkgcmp.dbs.dbs(self.opts)
        self.db = self.opts.get('db', 'sqlite')

    def _distros(self):
        '''
        return a list of distros
        '''
        ret = set()
        for func in self.scanners:
            if '.' in func:
                mod, fun = func.split('.')
                ret.add(mod)
        return sorted(ret)

    def reposync(self):
        '''
        run all the plugin reposync funcs
        '''
        for func in self.scanners:
            if func.endswith('.reposync'):
                self.scanners[func]()

    def db_update(self, distro):
        '''
        Pass over each distro and update the core db with the data
        '''
        for path in self.scanners['{}.iterpkgs'.format(distro)]():
            data = self.scanners['{}.scanpkg'.format(distro)](path)
            self.dbs['{}.save_pkg'.format(self.db)](data)

    def init_db(self):
        '''
        Init the database if needed
        '''
        idb = '{}.init'.format(self.db)
        if idb in self.dbs:
            self.dbs[idb]()

    def run(self):
        '''
        Scan the packages!!!
        '''
        if not self.opts['skip_sync']:
            self.reposync()
        if not self.opts['skip_db_init']:
            self.init_db()
        for distro in self._distros():
            self.db_update(distro)
