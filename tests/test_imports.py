import subprocess
import sys


def test_imports_have_no_startup_side_effects(tmp_path):
    code = """
import logging
import socket
from unittest.mock import patch
before = list(logging.getLogger().handlers)
with patch.object(socket.socket, 'connect', side_effect=AssertionError('network')):
    with patch('pydantic_settings.BaseSettings.__init__', side_effect=AssertionError('settings')):
        import frontier_lab
        import frontier_lab.config
        import frontier_lab.logging
assert logging.getLogger().handlers == before
"""
    result = subprocess.run([sys.executable, "-c", code], cwd=tmp_path, capture_output=True)
    assert result.returncode == 0, result.stderr.decode()
    assert not result.stdout


def test_environment_report_masks_credentials():
    import os
    from pathlib import Path

    script = Path(__file__).resolve().parents[1] / "scripts/check_environment.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        env={**os.environ, "OPENAI_API_KEY": "dummy-do-not-display"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert "OPENAI_API_KEY CONFIGURED: True" in result.stdout
    assert "dummy-do-not-display" not in result.stdout + result.stderr
