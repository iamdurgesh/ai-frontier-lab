# Controlled query-expansion follow-up

Date: 2026-10-19. AI-assisted implementation; owner understanding review remains pending.

## Question and hypothesis

Can an explicit vocabulary mapping recover a lexical miss while also introducing an incorrect match for an ambiguous word? This is the deliberate-modification follow-up to the existing lexical diagnostic, not a broader retrieval benchmark.

Hypothesis: expanding `restore` to include `checkpoint` retrieves the checkpoint document; expanding `resume` with the same term incorrectly favors that document over a career document. The career interpretation is an explicit relevance label, not something the system can infer from this single-word query.

## Method and budget

Use two new synthetic documents and two queries, co-designed with the mapping. Original fixture, retrieval implementation, runner and historical results remain unchanged. No held-out evaluation or generalization claim. Text and labels are AI-authored for this repository under its MIT license.

Compare unchanged BM25 defaults (k1=1.2, b=0.75) at k=1 with and without one-hop expansion. Original terms are retained, normalized additions are deduplicated, and added terms are never expanded recursively. Mapping keys must be normalized tokens. No new dependencies, model downloads, external services, or API calls.

One evidence run performs four searches. Stop on test failure or execution beyond 10 seconds. Tests use temporary output files; the runner refuses existing output paths. No latency/capacity or memory-isolation claim. API cost is zero by construction; electricity is unmeasured.

## Reproduce

From the repository root:

```bash
.venv/bin/pytest tests experiments/2026-09-lexical-retrieval-baseline -q
.venv/bin/python experiments/2026-09-lexical-retrieval-baseline/expansion.py --output /tmp/query-expansion-new.json
```

Use a fresh output filename. With uv installed, `uv run python` and `uv run pytest` may be used instead. The JSON captures exact source hashes, documents, expansion configuration, scores, and per-query Recall@1 and reciprocal rank@1. This deterministic diagnostic does not measure runtime performance.

## Interpretation boundaries

Expansion uses an explicit hand-authored mapping, not learned semantic understanding. The new checkpoint term can outweigh the original ambiguous term under document-length normalization. Inspect both cases separately; an average can hide a gain canceled by a regression. Do not adopt unconditional expansion based on this fixture. Independently curated queries and context-sensitive disambiguation remain future investigations.

The runner reads local source files and writes one explicit new artifact. Corpus text is never executed. No private data or network access is involved.

## Understanding check

Explain why adding a term can change the top result even while retaining the original term. Predict the effect of removing only the `resume` mapping, then test it on a separate output artifact. Owner answers and modifications have not been recorded.

## Measured outcome

[Evidence artifact](expansion-results-2026-10-19.json): the recovery case changed from no hit to the correct top hit (Recall@1: 0 → 1). The ambiguous career case changed from the correct top hit to the checkpoint document (Recall@1: 1 → 0). Reciprocal rank@1 changed identically. This confirms both predicted behaviors on the constructed examples only.

Validation: 36 tests passed across bootstrap and the lexical experiment. Repository lint, formatting, configured typing, and an explicit typing check of expansion.py passed. No remote CI was run. Decision: retain expansion as a teaching diagnostic; no general retrieval adoption claim. Revisit with independent, context-bearing queries before integration.
