from __future__ import absolute_import
from __future__ import unicode_literals

from pymonkey import make_entry_point

main = make_entry_point(('pip-custom-platform',), 'pip')

if __name__ == '__main__':
    exit(main())
