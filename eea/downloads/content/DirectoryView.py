""" Custom Filesystem Directory View
"""
import logging
import os

from Products.CMFCore import DirectoryView, FSFile
from Products.CMFCore.DirectoryView import createDirectoryView
from eea.downloads.config import PROJECTNAME

logger = logging.getLogger('eea.downloads')

class DirectoryInformation(DirectoryView.DirectoryInformation):
    """ Custom Directoy Information
    """
    def _changed(self):
        mtime=0
        filelist=[]
        try:
            mtime = os.stat(self._filepath)[8]
            if not self.use_dir_mtime:
                # some Windows directories don't change mtime
                # when a file is added to or deleted from them :-(
                # So keep a list of files as well, and see if that
                # changes
                os.path.walk(self._filepath, self._walker, filelist)
                filelist.sort()
        except:
            logger.exception("Error checking for directory modification")

        if mtime != self._v_last_read or filelist != self._v_last_filelist:
            self._v_last_read = mtime
            self._v_last_filelist = filelist

            return 1
        return 0

def registerDirectory(filepath):
    """ Register file-system directory
    """
    return DirectoryView._dirreg.registerDirectoryByKey(filepath, PROJECTNAME)

#
# Monkey patch DirectoryRegistry
#
def wrapper(func):
    def registerDirectoryByKey(self, filepath, reg_key, subdirs=1,
                                   ignore=DirectoryView.ignore):
        if 'eea.downloads' in reg_key:
            info = DirectoryInformation(filepath, reg_key, ignore)
            self._directories[reg_key] = info
            if subdirs:
                for entry in info.getSubdirs():
                    entry_filepath = os.path.join(filepath, entry)
                    entry_reg_key = '/'.join((reg_key, entry))
                    self.registerDirectoryByKey(entry_filepath, entry_reg_key,
                                                subdirs, ignore)
        else:
            return func(self, filepath, reg_key, subdirs, ignore)

    return registerDirectoryByKey

DirectoryView.DirectoryRegistry.registerDirectoryByKey = wrapper(
    DirectoryView.DirectoryRegistry.registerDirectoryByKey)

DirectoryView.registerFileExtension('epub', FSFile.FSFile)

__all__ = [
    createDirectoryView.__name__,
    registerDirectory.__name__,
]
