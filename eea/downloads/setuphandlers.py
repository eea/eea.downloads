""" Various setup
"""
import os
from eea.downloads.config import PROJECTNAME
from eea.downloads.content.DirectoryView import createDirectoryView

def setupVarious(context):
    """ Do some various setup.
    """
    if context.readDataFile('eea.downloads.txt') is None:
        return

    site = context.getSite()
    dirname = os.environ.get('EEADOWNLOADS_NAME')
    if dirname and dirname not in site.objectIds():
        createDirectoryView(site, PROJECTNAME, dirname)
