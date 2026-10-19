"""
test cli module
"""

import subprocess

import pytest

from bis_fetcher import get_version
from bis_fetcher.__cli__ import main


def capture(command: list[str]) -> tuple[bytes, bytes, int]:
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_cli() -> None:
    """Test cli module"""
    command = ["bis_fetcher"]
    _out, _err, exitcode = capture(command)
    assert exitcode == 0


def test_main_in_process(capsys) -> None:
    """No arguments prints the about line; --version prints the version and exits 0."""
    main([])
    assert get_version() in capsys.readouterr().out
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert capsys.readouterr().out.strip() == f"bis_fetcher {get_version()}"
