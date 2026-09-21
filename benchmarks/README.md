# Benchmarks

No results exist yet. Use [benchmark template](../templates/benchmark.md). Store small sanitized summaries and manifests here when reuse is demonstrated; keep experiment-specific evaluators and raw run artifacts with their experiment. Large/raw data belongs outside Git with a documented retrieval location and integrity identifier.

Record commit, date, hardware/OS/runtime/package/model/provider versions, licensed data and split, sample size, prompts/config, concurrency, warmup, metric definitions, repetitions, uncertainty, failures/timeouts, cost method and raw evidence paths. Compare like-for-like held-out tasks. Separate measurements, observations and interpretation; label vendor claims explicitly.

Metrics by task: retrieval Recall@k/Precision@k/MRR/nDCG, latency and index size; agents success, tool correctness, trajectory length, retries, interventions, wall time, tokens, cost/success and unsafe actions; inference TTFT, TPOT, tokens/requests per second, VRAM, batch/concurrency and failures; tuning baseline/tuned quality, loss where meaningful, runtime, memory, dataset size and inference regressions. No README/radar performance claim without evidence.
