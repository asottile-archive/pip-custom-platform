from __future__ import absolute_import
from __future__ import unicode_literals

import contextlib
import os
import shutil
import tempfile


@contextlib.contextmanager
def tmpdir():
    """Contextmanager to create a temporary directory.  It will be cleaned up
    afterwards.
    """
    tempdir = tempfile.mkdtemp()
    try:
        yield tempdir
    finally:
        shutil.rmtree(tempdir)


def mkdirp(path):
    try:
        os.makedirs(path)
    except OSError:
        if os.path.isdir(path):
            return
        else:
            raise
