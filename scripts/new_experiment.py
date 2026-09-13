"""Create one planned experiment from the canonical template without overwriting."""

import argparse
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def create_experiment(slug: str, root: Path = ROOT, today: date | None = None) -> Path:
    """Validate a slug and exclusively create its dated directory; refuse symlink roots."""
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or len(slug) > 80:
        raise ValueError("Use a lowercase alphanumeric slug with single hyphens (max 80).")
    day = today or date.today()
    experiments = root / "experiments"
    if experiments.is_symlink():
        raise ValueError("The experiments directory must not be a symlink.")
    template = experiments / "_template"
    if template.is_symlink():
        raise ValueError("The template must not be a symlink.")
    # Read and validate all inputs before reserving the destination.
    contents: dict[str, str] = {}
    for name in ("README.md", "RESULTS.md", "config.example.yaml"):
        source = template / name
        if source.is_symlink():
            raise ValueError("Template files must not be symlinks.")
        contents[name] = source.read_text(encoding="utf-8")
    target = experiments / f"{day:%Y-%m}-{slug}"
    target.mkdir()  # Atomic exclusive reservation; existing files/dirs/symlinks fail.
    for name, content in contents.items():
        (target / name).write_text(
            content.replace("<name>", slug).replace("<date>", day.isoformat()),
            encoding="utf-8",
        )
    return target


def main() -> None:
    """Parse a topic and report expected creation errors without a traceback."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    args = parser.parse_args()
    try:
        target = create_experiment(args.slug)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Experiment not created: {exc}\n")
    print(target)


if __name__ == "__main__":
    main()
