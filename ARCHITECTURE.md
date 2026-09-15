# AI Frontier Lab — Repository Architecture

Status: design contract for creator-agent bootstrap; no runtime implementation is claimed.

## Purpose and learning strategy

Become an engineer who can turn unfamiliar AI capabilities into useful products with confidence, integrate existing systems, and create new architectures where evidence justifies them.

**MASTER THE PRINCIPLES. PRACTICE WINNERS. MONITOR CHALLENGERS.**

- **MASTER:** durable mechanisms, reasoning about tradeoffs, implementation ability, and failure analysis.
- **PRACTICE:** tools selected against actual requirements and comparative evidence. Winners are contextual and revisable.
- **RADAR:** emerging approaches with a problem statement and a trigger for investigation. Popularity alone does not warrant adoption.

These are learning categories, not three sequential stages. The separate ADOPT / TRIAL / ASSESS / HOLD / IGNORE lifecycle records technology decisions.

Use one repository initially. A new tool does not warrant a new repository or a new project. Experiments answer questions; projects integrate capabilities into useful systems. Dependency isolation does not require repository separation.

## Bootstrap creation checklist

The creator agent must read this document and the local creator specification in `.agent-context/` (when available). This tree governs bootstrap scope; the specification governs file content. Preserve existing files and owner instructions. Do not implement the experiments or frameworks during bootstrap.

```text
ai-frontier-lab/
├── README.md
├── ARCHITECTURE.md                       # This contract; preserve and link
├── ROADMAP.md
├── SKILLS.md
├── TECH_RADAR.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── .gitignore
├── .env.example
├── .python-version
├── pyproject.toml
├── uv.lock
├── .pre-commit-config.yaml
├── .github/
│   ├── workflows/ci.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── experiment.yml
│   │   └── technology-review.yml
│   └── pull_request_template.md
├── src/frontier_lab/
│   ├── __init__.py
│   ├── config.py                          # Optional credentials; no import side effects
│   └── logging.py                         # Minimal logging; do not log secrets/payloads
├── tests/
│   ├── test_imports.py
│   ├── test_config.py
│   └── test_new_experiment.py              # Safe creation and existing-target refusal
├── core/README.md                         # Principle tracks and evidence links
├── experiments/
│   ├── README.md
│   └── _template/
│       ├── README.md
│       ├── RESULTS.md                     # Explicitly unmeasured
│       └── config.example.yaml
├── projects/README.md                     # Integrated project goals and activation gates
├── benchmarks/README.md                   # Methodology and result storage conventions
├── tools/README.md                        # Tool selection and comparison index
├── frontier/
│   ├── README.md
│   └── watchlist.md
├── templates/
│   ├── experiment.md
│   ├── tool-review.md
│   ├── benchmark.md
│   ├── paper-review.md
│   └── architecture-decision-record.md
├── datasets/README.md                     # Provenance, licensing, storage policy
├── infra/README.md                        # Deferred service plan
└── scripts/
    ├── README.md
    ├── check_environment.py
    └── new_experiment.py
```

Do not add an empty `utils` package, service stack, framework abstractions, or directories for every future topic. Add runtime dependencies only for implemented bootstrap behavior. Keep the two experiment template representations consistent and designate `experiments/_template/` as the generator's source of truth.

Agent instructions, communication rules, and the creator workflow live locally in `.agent-context/`, with a root `AGENTS.md` discovery pointer. Both are excluded via `.git/info/exclude` and are not part of a fresh clone. Root `SKILLS.md` tracks learning evidence; it is project documentation.

## Directory responsibilities and boundaries

| Location | Owns | Boundary |
|---|---|---|
| `core/` | Explanations of principles, small worked examples, links to evidence | No duplicate experiment implementations or vendor tutorial dumps |
| `experiments/` | One primary hypothesis, baseline, runnable code, local tests, results, conclusion | Independent runs; no imports from another experiment |
| `projects/` | Useful integrated systems, project-specific source, tests, evaluation, design decisions | No runtime imports from experiment directories or sibling projects |
| `src/frontier_lab/` | Small, proven shared code with stable responsibilities | Must not import projects or experiments; no speculative universal agent framework |
| `benchmarks/` | Reusable evaluation methodology, manifests, small sanitized result artifacts | Experiment-specific evaluators remain with their experiment until reuse is demonstrated |
| `tools/` | Evidence-backed tool reviews and integration notes | Tool-specific trials execute under `experiments/` |
| `frontier/` | Signals, primary-source references, review dates, revisit triggers | Monitoring never auto-installs or executes discovered code |
| `datasets/` | Dataset manifests, small approved fixtures, provenance | No private data, large weights, or unlicensed redistribution |
| `infra/` | Explicitly activated local service configurations | No implicit services or network calls on package import |
| `templates/` | Review and decision contracts | No invented conclusions or metrics |

Allowed runtime dependency direction:

```text
experiment code ──→ frontier_lab shared code ──→ justified third-party dependencies
project code ─────→ frontier_lab shared code
project application ──→ project domain/contracts
project adapters ─────→ project domain/contracts + provider/protocol SDKs
project entry point ──→ application + configured adapters
```

Keep application policy independent of provider and transport SDKs when an actual project needs that separation. Do not build these layers at bootstrap. Promote shared code only after at least two concrete consumers demonstrate compatible needs, with tests and a recorded extraction decision.

Small experiments may use the root environment. Conflicting, heavy, or GPU-dependent work gets a local `pyproject.toml` and lockfile or a documented container. Document exact run commands and how any dependency on `frontier_lab` resolves locally. Root CI runs offline baseline checks; project/experiment checks are explicitly selected and do not silently require paid APIs or GPUs.

## Growth map — create only when activated

```text
core/
  model-foundations/        # Training/inference, embeddings, sampling, generalization
  experimental-design/      # Baselines, held-out data, leakage, repeated trials, uncertainty
  distributed-systems/      # Concurrency, delivery, idempotency, partial failure, recovery
  reasoning-orchestration/  # Decomposition, bounded recursion, aggregation, termination
  rag/ agents/ context-engineering/ evals/ security/
  mcp/ a2a/ inference/ finetuning/
experiments/YYYY-MM-question-slug/
  README.md  RESULTS.md  config.example.yaml
  [implementation, tests, and environment files appropriate to the question]
projects/
  01-research-rag-agent/
  02-distributed-reasoning-framework/
  03-local-ai-platform/
  04-ai-frontier-radar/
frontier/weekly/YYYY-WXX.md
frontier/papers/
infra/compose.yaml          # Only when a selected experiment requires services
```

The four projects are planned integration destinations, not four simultaneous commitments. Add project-specific `src/`, `tests/`, `evals/`, and `docs/decisions/` as needed. Framework code initially belongs to Project 02; a later decision may promote a reusable package within this repository. A separate repository is not a prerequisite.

## Project 02 — Distributed recursive reasoning framework

Intended capability: execute bounded reasoning tasks across workers, allow controlled recursive delegation, integrate tools through MCP and remote agents through A2A, and recover predictably from failures. This is a design direction to validate, not a claim that multi-agent reasoning is better by default.

### Logical responsibilities

| Component | Responsibility and boundary |
|---|---|
| Task contracts | Task/run/parent IDs, input/output schemas, status, errors, deadlines, cancellation, artifact references, schema versions |
| Orchestrator | Plan/delegate/aggregate; determine completion; enforce recursion depth, fan-out, total work, time, and spending limits |
| Scheduler/executor | Dispatch bounded work, apply backpressure, manage concurrency, retries, and worker availability |
| Worker | Execute one assigned task with scoped capabilities; report outcome and usage; cooperate with cancellation |
| State store | Persist lifecycle transitions and recoverable execution state; define deduplication and ownership semantics |
| Model adapter | Expose required model behavior and usage without scattering provider SDK calls |
| MCP adapter | Integrate external tool/resource capabilities with explicit authorization and untrusted-output handling |
| A2A adapter | Map remote agent interactions to internal contracts; keep protocol-version details at the boundary |
| Policy boundary | Check tool actions and delegation against permissions, budgets, and approval requirements |
| Evaluation and telemetry | Record sanitized events, task outcomes, failures, latency, and usage for comparison and debugging |

The internal domain must not be defined by a specific protocol SDK. Confirm current official MCP/A2A behavior when implementing adapters. Do not presume either protocol supplies the framework's scheduling, durable execution, or security policy.

### Evidence-gated progression

1. **Deterministic workflow baseline:** define a useful task and held-out cases; measure a fixed workflow and, where relevant, a single-agent implementation.
2. **Single-process executor:** explicit task lifecycle, fake workers for deterministic testing, bounded tool access, observable failure outcomes.
3. **Bounded recursive delegation:** parent-child tracking, depth/fan-out limits, shared budget accounting, aggregation, and termination under adversarial decomposition.
4. **Durable local execution:** checkpoint/restart behavior, idempotency keys, duplicate handling, cancellation propagation, and exhausted-retry outcomes.
5. **Distributed execution:** begin with multiple local processes; inject worker crashes, delays, duplicate delivery, and disconnections. Specify delivery semantics and recovery behavior. Do not assume exactly-once effects.
6. **Protocol integration:** add and test MCP capabilities and A2A remote-agent interoperability independently, then combine them in an end-to-end task with scoped permissions.
7. **Product validation:** compare quality, reliability, latency, cost, and operational complexity with the original baseline on the same held-out tasks. Record whether the architecture earns adoption for this use case.

Before each stage, define measurable exit criteria and a finite experiment budget. No default numerical quality threshold is invented before the task and evaluation set exist. Safety invariants include bounded work, permission enforcement, visible terminal failure states, and prevention or explicit reconciliation of duplicate side effects. Record the limits of cancellation for in-flight external actions.

Select a concrete useful task before beginning Project 02. The creator agent must leave that selection open rather than invent the owner's target users, deployment environment, or hardware budget.

## Experiment and learning contract

Every experiment records:

- Question, hypothesis, simplest meaningful baseline, and the principle being learned.
- Intended practical use and the decision this evidence will inform.
- Data provenance, evaluation split, reproducible environment, and relevant model/configuration identifiers.
- Time, request/token, spending, and resource budgets; stop conditions.
- Measurements, repeated trials where relevant, failures, uncertainty, and raw evidence location.
- Security/privacy boundaries, permitted actions, and data sent to external services.
- Conclusion, limitations, adoption decision where applicable, and revisit trigger.
- Understanding evidence: explain the mechanism, predict a failure, reproduce it, and make a deliberate modification. Record assistance honestly; generated code alone does not establish mastery.

A finished experiment may supply evidence to a project. Integrating it requires project tests, explicit contracts, documented dependencies, and appropriate failure handling. A successful demo alone is insufficient to call a component production-ready.

Security, privacy, evaluation, observability, and cost control begin with the first experiment. Record intended use and data flows; deployment-specific GDPR/DSGVO and EU AI Act applicability must be assessed against current authoritative requirements before a real product deployment. The lab architecture itself does not certify compliance.

## Creator-agent handoff

Assignment:

> Read the root README and ARCHITECTURE.md, plus the local creator specification when available. Bootstrap only the architecture's creation checklist. Preserve existing owner instructions and work. Implement the minimal package, experiment generator, offline tests, and CI; create concise indexes and templates. Record future projects and principles in the roadmap without implementing them or creating their future directory trees. Validate the bootstrap commands and generator behavior. Report created files, checks performed, failures, and remaining manual setup honestly. Do not start an AI experiment, install service stacks, or call paid models.

Bootstrap is complete when the documented setup works without cloud credentials, tests/lint pass, a temporary experiment can be generated safely, and a reader can distinguish current implementation from planned architecture. The first proposed learning experiment remains a retrieval baseline; its execution requires a subsequent assignment.
