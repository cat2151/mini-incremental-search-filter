from distutils.core import setup
import py2exe

option = {
    'bundle_files':1,
    'optimize': 2,
    'excludes' : ['_gtkagg', '_ssl', '_tkagg', 'bsddb', 'curses', 'doctest', 'email', 'pdb', 'pyreadline', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl', 'Tkconstants'],
     'dist_dir': './miniIncrementalSearchFilter',
}
setup(
    options = {'py2exe': option},
    windows=['miniIncrementalSearchFilter.py'],
    zipfile = 'lib\\libs.zip',
    )
