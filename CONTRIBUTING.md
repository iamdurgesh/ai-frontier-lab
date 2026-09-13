# Contributing

Read README.md and ARCHITECTURE.md. If local agent context is installed, also read the root AGENTS.md pointer. Use Python 3.12 and `uv sync --locked`.

Create a focused branch and a single-hypothesis experiment with `uv run python scripts/new_experiment.py topic`. Define the question, baseline, data provenance, held-out split, budgets, stop conditions, and security boundaries before running it. Record assistance honestly. Explain a mechanism, reproduce a predicted failure, and make a deliberate modification before claiming understanding.

Run `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, and `uv run mypy`. Optional local hooks: `uv run pre-commit install`; run all hooks with `uv run pre-commit run --all-files`. Hooks use the locked root environment.

Use small commits such as `chore(repo): bootstrap frontier lab` or `exp(rag): compare retrieval baselines`. PRs describe behavior, evidence, validation, and limitations. A completed experiment has reproducible code, measured results, conclusion, and a justified radar decision.

Root runtime dependencies: pydantic provides masked credential values; pydantic-settings loads optional configuration. Hatchling builds the src package. pytest tests bootstrap behavior; Ruff handles lint/format/import order; mypy checks reusable code; pre-commit runs the same local checks. No HTTP client, agent SDK, CLI framework, async test plugin, or service client is needed yet. Versions resolve into uv.lock; update deliberately and rerun checks.

Small experiments may use the root environment. Heavy/conflicting/GPU stacks get their own pyproject.toml and lockfile or container. Document exact run commands and local frontier_lab dependency resolution. Do not import sibling experiments/projects. Root CI selects only offline bootstrap tests; explicitly activate other suites.

Implementation references checked at bootstrap: [uv project configuration](https://docs.astral.sh/uv/concepts/projects/config/) and [Pydantic settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/). Recheck APIs when changing dependencies.
