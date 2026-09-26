# Integrated projects — planned

No projects are implemented or activated. Use evidence from focused experiments; do not import their runtime code. Add project source, tests, evals and decisions only when needed. Shared code extraction needs two compatible consumers and a recorded decision.

| Project | Goal and progression | Activation / completion evidence |
|---|---|---|
| 01 Research/RAG agent | Retrieval → hybrid → reranking → evals → agent → state → tracing → MCP → routing | Activate after retrieval evidence; require reproducible benchmark, citations, eval set, tracing and documented failures |
| 02 Distributed recursive reasoning | Baseline → single-process → bounded recursion → durable recovery → distribution → MCP/A2A → validation | First select useful task/users, evaluation set and budget; require termination/resource limits, cancellation, injected-failure recovery, baseline comparison, MCP server/client, two agents, cross-framework case and security model |
| 03 Local AI platform | Simple inference → compatible endpoint → quantization → serving benchmark → routing | Select hardware/task/budget first; require repeatable startup, hardware requirements, TTFT/throughput and quality comparison, capacity/failure notes |
| 04 AI Frontier Radar | Discover → normalize → deduplicate → classify → score → analyze → store → report → decide | Begin with useful manual reports; require traceable primary sources, deduplication checks and justified experiment decisions; never auto-install/run discoveries |

The goal is to turn demonstrated understanding into useful systems. For Project 02, test whether each added mechanism improves the chosen task against a credible simpler baseline. Claims of an advance must meet the [evidence requirements](../ARCHITECTURE.md#evidence-required-for-an-advance), including repeated measurements, component comparisons, failure analysis and reproducibility. No breakthrough or general superiority is claimed.

Project 02 follows the full [architecture progression](../ARCHITECTURE.md#project-02--distributed-recursive-reasoning-framework). Its concrete task, users, deployment environment and hardware budget remain open. These are integration destinations, not simultaneous commitments.
