import os
import imp
"""Deprecated since version 3.4: The imp package is pending deprecation in favor of importlib."""

def importFromURI(uri, absl=False):
    if not absl:
        uri = os.path.normpath(os.path.join(os.path.dirname(__file__), uri))
    path, fname = os.path.split(uri)
    mname, ext = os.path.splitext(fname)

    no_ext = os.path.join(path, mname)

    if os.path.exists(no_ext + '.pyc'):
        try:
            return imp.load_compiled(mname, no_ext + '.pyc')
        except:
            raise
    if os.path.exists(no_ext + '.py'):
        try:
            return imp.load_source(mname, no_ext + '.py')
        except:
            raise
    raise NameError('Script %s does not exist' % uri)
