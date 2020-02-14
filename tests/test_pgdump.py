import pytest
import subprocess

from pgbackup import pgdump

url = "postgres://bob@psqlserver:5432/db_one"

def test_dump_calls_pgdump(mocker):
    """
    Utilize pgdump with the database URL
    """
    mocker.patch('subprocess.Popen')
    assert pgdump.dump(url)
    subprocess.Popen.assert_called_with(['pg_dump', url], stdout = subprocess.PIPE)


def test_dump_catches_filenotfound(mocker):
    """
    pgdump returns a user-friendly error, when the tool isn't installed.
    """
    mocker.patch('subprocess.Popen', side_effect=OSError('no such file'))
    with pytest.raises(SystemExit):
        pgdump.dump(url)
    