""" Main product initializer
"""
import os
from eea.downloads.content.DirectoryView import registerDirectory

def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
    dirpath = os.environ.get('EEADOWNLOADS_PATH')
    if dirpath:
        registerDirectory(dirpath)
