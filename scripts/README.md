# Repository scripts

Run from repository root after `uv sync --locked`:

- `uv run python scripts/check_environment.py`: Python/platform, uv/Docker availability, .env presence and optional provider configuration booleans. It never calls model APIs or starts services.
- `uv run python scripts/new_experiment.py topic`: creates the current YYYY-MM-topic folder from experiments/_template/. Invalid names and existing targets fail with nonzero exit status. No experiment is run.

Generator tests create disposable experiments under pytest temporary directories; the repository remains free of fake experiments. Settings load .env relative to the working directory only when explicitly constructed. Logging is opt-in and callers must omit secrets and payloads.
