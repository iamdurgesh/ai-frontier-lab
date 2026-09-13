"""Report local tooling and credential presence, never credential values."""

import platform
import shutil
import subprocess
from pathlib import Path

from frontier_lab.config import Settings


def main() -> None:
    """Inspect the current environment without starting services or making API calls."""
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    for name in ("uv", "docker"):
        executable = shutil.which(name)
        version = "unavailable (optional)" if name == "docker" else "unavailable"
        if executable:
            try:
                result = subprocess.run(
                    [executable, "--version"], capture_output=True, text=True, timeout=5, check=True
                )
                version = result.stdout.strip()
            except (OSError, subprocess.SubprocessError):
                version = "installed; version check failed"
        print(f"{name}: {version}")
    print(f".env exists: {Path('.env').is_file()}")
    settings = Settings()
    for key in type(settings).model_fields:
        print(f"{key.upper()} CONFIGURED: {bool(getattr(settings, key))}")


if __name__ == "__main__":
    main()
