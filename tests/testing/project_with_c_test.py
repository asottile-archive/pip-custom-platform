from __future__ import absolute_import
from __future__ import unicode_literals

import subprocess


def test_project_with_c(tmpdir):
    """Make sure it is an installable C extension and produces the expected
    output.
    """
    venv = tmpdir.join('venv')
    subprocess.check_call(('virtualenv', venv.strpath))
    subprocess.check_call((
        'sh', '-c',
        '. {}/bin/activate && pip install testing/project_with_c'.format(
            venv.strpath,
        ),
    ))
    proc = subprocess.Popen(
        (
            'sh', '-c',
            '. {}/bin/activate && '
            'python -c "'
            'import project_with_c\n'
            'print(project_with_c.hello_world())"'.format(
                venv.strpath,
            )
        ),
        stdout=subprocess.PIPE,
    )
    out, _ = proc.communicate()
    assert proc.returncode == 0
    assert out == b'hello world\n'
