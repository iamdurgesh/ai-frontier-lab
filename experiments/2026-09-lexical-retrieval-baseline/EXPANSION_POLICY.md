# Expansion only after an empty result

Date: 2026-10-27. AI-assisted follow-up; owner understanding review remains pending.

## Question and hypothesis

Can expanding only after an empty BM25 result retain the previous recovery gain without damaging a correct ambiguous-word match? Hypothesis: yes for those two controlled cases, but it cannot fix a wrong nonempty result. This tests a policy, not a new retrieval algorithm or semantic model.

## Method and limits

Reuse the two synthetic documents and explicit mapping from expansion.py, without modifying that historical diagnostic. Compare `never`, `always`, and `on_empty` on three co-designed cases at k=1, k1=1.2, b=0.75. Relevance labels specify intended meanings: `restore` means checkpoint recovery; `resume` means a career document; `restore resume` is labeled checkpoint recovery. These deliberately short, ambiguous examples are not independently curated evaluation data.

Budget: nine policy evaluations, at most eighteen underlying searches per run, no network, services, model downloads, or new dependencies. Each fallback permits at most two searches and skips a second search when no new vocabulary is added. This bounds calls, not wall-clock time or memory. Use a 10-second subprocess timeout for validation runs; stop on test failure. No timing benchmark. API cost is zero; local compute cost is not measured.

Input text is data, never executed. The runner reads local source files and writes a new explicit output file. It refuses existing outputs. Exact source hashes, documents, configuration, per-case scores, relevance metrics, and actual search counts are recorded. Recall@1 and reciprocal rank@1 are identical here because each query has one relevant document.

## Reproduce

From repository root, choose a fresh output path:

```bash
.venv/bin/pytest tests experiments/2026-09-lexical-retrieval-baseline -q
.venv/bin/python experiments/2026-09-lexical-retrieval-baseline/expansion_policy.py --output /tmp/expansion-policy-new.json
```

Tests invoke the runner with a 10-second timeout. The CLI itself does not impose a deadline. With uv installed, `uv run python` and `uv run pytest` are alternatives.

## Understanding check

Explain why a nonempty result is not evidence of relevance. Predict the tradeoff from adding a score threshold before changing the code; raw BM25 scores are not calibrated confidence probabilities. No skill rating is advanced by this implementation.

## Decision and next investigation

Keep all three policies as diagnostic comparisons. Do not enable fallback by default in a product based on these examples. Independently curated queries with explicit intent and no-answer cases are needed before broader quality comparisons; dense and hybrid retrieval remain planned. The existing corpus and historical evidence are preserved.

## Measured results

[Evidence](policy-results-2026-10-27.json), measured locally on 2026-10-27:

| Case | Never: Recall@1 | Always: Recall@1 | On empty: Recall@1 |
|---|---|---|---|
| Lexical miss | 0 | 1 | 1 |
| Ambiguous career query | 1 | 0 | 1 |
| Wrong nonempty result | 0 | 1 | 0 |

The fallback performed two searches for the lexical miss and one for each other case. Ten searches were performed across all nine evaluations. The hypothesis held on these constructed examples only; this is not evidence of general superiority.

Validation: 44 tests passed across bootstrap and this experiment. Repository lint, format checks, configured typing, and explicit typing of expansion_policy.py passed. Tests verify bounded calls, unchanged-query short-circuiting, invalid-policy rejection, deterministic evidence, and overwrite refusal. Remote CI was not run.
