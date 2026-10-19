"""
test cli module
"""

import subprocess


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
