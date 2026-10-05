# AI Frontier Lab

A hands-on AI engineering lab for learning to turn unfamiliar AI capabilities into useful products with confidence.

**Master the principles. Practice winners. Monitor challengers.**

This single repository will connect focused experiments, evidence-backed technology decisions, and integrated projects—including a progressive distributed recursive multi-agent reasoning framework with MCP/A2A support.

Status: active learning/engineering lab with initial bootstrap tooling. The first offline lexical-retrieval diagnostic has measured results; owner understanding review is pending. No integrated project or reasoning framework is implemented. Experiments will vary in maturity.

- [Repository architecture](ARCHITECTURE.md): bootstrap tree, module boundaries, growth map, and framework progression.

The architecture defines the bootstrap checklist and repository boundaries. Future project directories and service stacks are activated when actual experiments need them.

## Core goal

Develop the ability to explain, build, evaluate, troubleshoot, and justify useful AI systems. Integrate existing capabilities confidently and create new architectures when experiments show a concrete need. The lab connects deliberate learning to working products; the distributed recursive reasoning framework is a major planned destination.

We aim for meaningful advances, including a potential breakthrough, through reproducible implementation and comparison. Progress means demonstrated understanding and useful measured outcomes. See the [architecture's evidence requirements](ARCHITECTURE.md#evidence-required-for-an-advance) before making improvement or novelty claims.

## Working principles

MASTER principles | PRACTICE evidence-backed tools | RADAR challengers

No notes without implementation where practical; no implementation without measurement where practical; no benchmark without methodology; no adoption without a written decision. Prefer official documentation and distinguish reproducible evidence from opinion. Never commit secrets or private data.

- Learn through focused implementation: one question, a falsifiable hypothesis, and a meaningful baseline.
- Demonstrate understanding: explain the mechanism, predict and reproduce a failure, and make a deliberate modification. Record AI assistance honestly.
- Follow DRY and KISS: keep clear responsibilities and add dependencies or abstractions only for demonstrated needs.
- Measure quality, reliability, latency, resource use, and cost where relevant; publish limitations and negative results alongside successes.
- Apply privacy, permission boundaries, and finite budgets from the first experiment. Assess deployment-specific obligations before deployment.
- Advance from experiments to integrated projects when tests and evidence justify the next step.

The learning scope covers RAG/search, agents, MCP/A2A, multi-agent systems, context engineering, evals, coding agents, automation, open models, inference, and fine-tuning. Multimodal and physical AI remain future tracks. Current focus: advanced retrieval, evaluation, agents, MCP, then A2A.

## Quick start

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first. Run from the repository root:

```bash
git clone <repo-url>
cd ai-frontier-lab
uv sync --locked
cp .env.example .env
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run python scripts/check_environment.py
```

Initial setup downloads Python 3.12 if needed and the locked dependencies. Baseline checks need no cloud credentials or services. Future cloud experiments may incur costs and require explicit credential configuration.

## Repository map

| Path | Purpose |
|---|---|
| `src/frontier_lab/` | Optional settings and opt-in logging |
| `tests/`, `scripts/` | Offline checks and safe experiment creation |
| [core](core/README.md) | Principle tracks and evidence index |
| [experiments](experiments/README.md) | Single-question investigations and canonical template |
| [projects](projects/README.md) | Planned integrated systems and activation gates |
| [benchmarks](benchmarks/README.md) | Reproducibility and measurement conventions |
| [tools](tools/README.md) | Evidence-backed tool comparisons |
| [frontier](frontier/README.md) | Primary-source monitoring and revisit triggers |
| `templates/` | Experiment, benchmark, review, and decision contracts |
| [datasets](datasets/README.md), [infra](infra/README.md) | Data policy and deferred services |

See [roadmap](ROADMAP.md), [skills evidence](SKILLS.md), [technology decisions](TECH_RADAR.md), [contributing](CONTRIBUTING.md), [security](SECURITY.md), and [change history](CHANGELOG.md). The existing MIT [license](LICENSE) applies.

## Start an experiment when ready

```bash
uv run python scripts/new_experiment.py hybrid-search-baseline
```

This creates `experiments/YYYY-MM-hybrid-search-baseline/` with planned, unmeasured documents. It does not execute an experiment. Fill in the hypothesis, baseline, evaluation data, budgets, and permitted actions before adding implementation. The active lexical baseline is linked below; create a new experiment only for a new question.

## Active experiment

[Lexical retrieval baseline](experiments/2026-09-lexical-retrieval-baseline/README.md): compare word overlap, BM25, and a length-normalization ablation on a small synthetic diagnostic. [Measured results](experiments/2026-09-lexical-retrieval-baseline/RESULTS.md) show the expected vocabulary-mismatch failures; they do not establish general retrieval quality. Next: work through the understanding check before broadening the dataset.
