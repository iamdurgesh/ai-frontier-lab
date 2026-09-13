import importlib.util
import shutil
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("new_experiment", ROOT / "scripts/new_experiment.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@pytest.fixture
def root(tmp_path):
    shutil.copytree(ROOT / "experiments/_template", tmp_path / "experiments/_template")
    return tmp_path


def test_create_and_refuse_existing(root):
    target = module.create_experiment("retrieval-baseline", root, date(2026, 9, 13))
    assert target.name == "2026-09-retrieval-baseline"
    before = {p.name: p.read_bytes() for p in target.iterdir()}
    assert b"2026-09-13" in before["README.md"]
    assert b"<name>" not in before["README.md"]
    assert b"Not measured" in before["RESULTS.md"]
    with pytest.raises(FileExistsError):
        module.create_experiment("retrieval-baseline", root, date(2026, 9, 13))
    assert before == {p.name: p.read_bytes() for p in target.iterdir()}


@pytest.mark.parametrize(
    "slug", ["", "../escape", "/absolute", "a/b", "Bad", "a--b", "a-", "x" * 81]
)
def test_invalid_slug(root, slug):
    with pytest.raises(ValueError):
        module.create_experiment(slug, root)
    assert list((root / "experiments").iterdir()) == [root / "experiments/_template"]


@pytest.mark.parametrize("kind", ["file", "symlink"])
def test_existing_non_directory(root, kind):
    target = root / "experiments/2026-09-topic"
    if kind == "file":
        target.write_text("preserve")
    else:
        target.symlink_to(root / "missing")
    with pytest.raises(FileExistsError):
        module.create_experiment("topic", root, date(2026, 9, 13))


def test_template_sync():
    assert (ROOT / "templates/experiment.md").read_bytes() == (
        ROOT / "experiments/_template/README.md"
    ).read_bytes()


def test_missing_template_does_not_create_target(root):
    (root / "experiments/_template/RESULTS.md").unlink()
    with pytest.raises(FileNotFoundError):
        module.create_experiment("topic", root, date(2026, 9, 13))
    assert not (root / "experiments/2026-09-topic").exists()


def test_symlink_template_rejected(root):
    source = root / "experiments/_template/README.md"
    source.unlink()
    source.symlink_to(ROOT / "experiments/_template/README.md")
    with pytest.raises(ValueError, match="symlinks"):
        module.create_experiment("topic", root)


def test_cli_create_and_refuse_existing(root):
    import subprocess
    import sys

    (root / "scripts").mkdir()
    script = root / "scripts/new_experiment.py"
    shutil.copyfile(ROOT / "scripts/new_experiment.py", script)
    command = [sys.executable, str(script), "cli-smoke"]
    first = subprocess.run(command, capture_output=True, text=True)
    assert first.returncode == 0, first.stderr
    assert Path(first.stdout.strip()).is_dir()
    second = subprocess.run(command, capture_output=True, text=True)
    assert second.returncode == 1
    assert "Experiment not created" in second.stderr
