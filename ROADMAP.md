# Roadmap

Phases are evidence gates, not calendar promises or mandatory tool checklists. Evaluation, privacy, security, observability, and cost control begin with the first experiment. Most learning work below is planned; the first lexical retrieval diagnostic is active.

## Progress and learning discipline

The core goal is demonstrated engineering ability and useful systems. The distributed recursive reasoning framework is a major integration destination; use the [architecture evidence requirements](ARCHITECTURE.md#evidence-required-for-an-advance) to judge proposed advances.

For each learning cycle: define one question → implement the simplest baseline → make one deliberate change → measure and stress it → explain the result → record a decision. Set a finite budget and finish the evidence record before expanding scope. Update SKILLS.md only with linked evidence; a failed hypothesis can still demonstrate understanding.

Bootstrap tooling exists locally. The [lexical retrieval diagnostic](experiments/2026-09-lexical-retrieval-baseline/README.md) has an implementation and measured results; owner understanding review is pending. No integrated project has been completed. Local checks, committed files, and remote validation must be reported separately.

## Phase 0 — Bootstrap

- Goal: Package, templates, CI, experiment lifecycle.
- Artifact: Usable repository.
- Exit evidence: Setup, tests, lint, format, typing and temporary generation pass. All required files are committed and setup works from a clean checkout. Verify remote CI after an explicitly approved push; local success alone does not establish remote readiness.

## Phase 1 — Retrieval + RAG

- Goal: BM25/sparse, dense, hybrid, RRF, reranking, metadata filters, chunking, query rewriting, evaluation, context selection, agentic retrieval.
- Artifact: Reproducible retrieval comparison.
- Exit evidence: Compare baseline and variants on held-out queries; report Recall@k, MRR, latency, failures and uncertainty.

## Phase 2 — Agent engineering

- Goal: Raw loop, structured outputs, tool calling, state, memory, context, retries, checkpoints, human approval; LangGraph and OpenAI Agents SDK comparison.
- Artifact: Bounded agent and comparison report.
- Exit evidence: Evaluate same task set against a fixed workflow; test retries, stop conditions and approval enforcement.

## Phase 3 — Interoperability

- Goal: MCP server/client, tools/resources/prompts, transport, consent; A2A and cross-framework communication.
- Artifact: Local interoperability demo and threat model.
- Exit evidence: Test supported contracts, denied actions and failures; demonstrate a cross-framework exchange after MCP baseline.

## Phase 4 — Evals / observability / security

- Goal: Golden data, deterministic graders, LLM judge, retrieval metrics, trajectories, tracing, latency/cost, injection, permissions, sandboxing, audit logging.
- Artifact: Regression and adversarial suite.
- Exit evidence: Publish repeatable grader methodology and observed failure rates with sanitized traces.

## Phase 5 — Automation

- Goal: n8n, webhooks, schedules, events, approval, MCP integration, Frontier Radar MVP.
- Artifact: Auditable workflow.
- Exit evidence: Exercise success, duplicate events, denial and recovery; measure latency and cost.

## Phase 6 — Open models + inference

- Goal: Loading, quantization, vLLM, SGLang comparison, TTFT, throughput, batching, KV/prefix cache, serving and compatible endpoint.
- Artifact: Local serving benchmark.
- Exit evidence: Record hardware, repeated latency/throughput/quality results and capacity failures.

## Phase 7 — Fine-tuning / post-training

- Goal: Transformers, PEFT, LoRA/QLoRA, SFT, TRL, preferences, synthetic data.
- Artifact: Baseline-versus-tuned evaluation.
- Exit evidence: Document licensed data splits and compare held-out quality, runtime, memory and regressions.

## Phase 8 — Multi-agent / frontier

- Goal: Supervisor/worker, planner/executor, router/specialists, critic/reviewer, parallel agents, swarms, learned orchestration.
- Artifact: Bounded systems experiments.
- Exit evidence: Compare identical held-out tasks against simpler baselines; test budget, cancellation and recovery invariants.

## Phase 9 — Multimodal / physical AI

- Goal: Document AI, vision, voice, computer use, VLM/VLA, NVIDIA/robotics ecosystem.
- Artifact: Selected scoped prototype.
- Exit evidence: Choose a task and budget first; publish baseline quality, failure analysis and action boundaries.

## Systems progression

[Project 02 architecture](ARCHITECTURE.md#project-02--distributed-recursive-reasoning-framework): select a useful task → deterministic/single-agent baseline → single-process executor → bounded recursion → durable local recovery → distributed fault injection → independent MCP/A2A integrations → product validation. Before every stage define measurable exit criteria and finite budgets. Target users, deployment environment, and hardware budget remain open.

## Initial practical backlog

- [ ] Retrieval: tiny public evaluation corpus; sparse/BM25 baseline; dense retrieval; Qdrant hybrid; compare sparse/dense/hybrid; reranking; Recall@k/MRR/latency.
- [ ] First agent: raw tool loop; structured outputs; errors; LangGraph comparison; checkpoints; human approval; trace a run.
- [ ] Evals/context: golden dataset; deterministic grader; secondary LLM judge; context selection; context-size measurement; Langfuse or equivalent tracing.
- [ ] MCP: local server; safe read-only tool; resource; client; approved write test; threat model; compatible client integration. A2A follows MCP understanding.

First active experiment: [2026-09-lexical-retrieval-baseline](experiments/2026-09-lexical-retrieval-baseline/README.md), the sparse first step toward the hybrid-search comparison. Dense retrieval, Qdrant, and reranking remain deferred. Set data, time, request/token, spending and resource budgets before starting. Each claim of mastery requires mechanism explanation, a predicted/reproduced failure, a deliberate modification, and honest assistance disclosure.
