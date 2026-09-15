# Experiments

No experiments have run yet. Each experiment asks one primary question with a meaningful baseline, bounded resources, licensed evaluation data, reproducible method, and honest results.

From the root run `uv run python scripts/new_experiment.py topic` to create `YYYY-MM-topic`. Only lowercase letters, digits and single hyphens are accepted, up to 80 characters. Existing files, directories and symlinks are refused. A write failure may leave a partial directory; inspect it manually before retrying, since it will never be overwritten.

`_template/` is the generator source of truth. Keep its README byte-identical to [templates/experiment.md](../templates/experiment.md); tests enforce this. RESULTS.md starts unmeasured. Config is a documentation stub, not a runnable configuration. Fill in all budgets before execution.

Small experiments may use the root environment. Isolated experiments must document their own environment, lockfile and local package resolution. Never import a sibling experiment. Promote findings into projects through explicit contracts, tests and failure handling. Generated code alone is not evidence of mastery.
