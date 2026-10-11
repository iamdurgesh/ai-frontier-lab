# Results: lexical-retrieval-baseline

Measured on 2026-09-29. Experiment remains Running until owner understanding review.

## Measured results

Evidence: [raw artifact](results-2026-09-29.json), including source/data hashes, base commit, runtime environment, configuration, rankings, scores and all latency samples.

| Configuration | Overall Recall@3 | Overall MRR@3 | Lexical queries: Recall@3 / MRR@3 | Paraphrases: Recall@3 / MRR@3 |
|---|---|---|---|---|
| Word overlap | 0.6667 | 0.6667 | 1.0 / 1.0 | 0.0 / 0.0 |
| BM25, b=0.75 | 0.6667 | 0.6667 | 1.0 / 1.0 | 0.0 / 0.0 |
| BM25, b=0 | 0.6667 | 0.6667 | 1.0 / 1.0 | 0.0 / 0.0 |

Each configuration retrieved the relevant document first for all 8 lexical queries and returned no hits for the 4 deliberately disjoint-vocabulary paraphrases. All 20 repetitions per query had identical rankings. No execution errors occurred in this run; empty retrievals are relevance failures, not execution errors.

Search-only latency across 240 measurements per configuration:

| Configuration | Median milliseconds | Min–max milliseconds |
|---|---|---|
| overlap | 0.0051 | 0.0026–0.0081 |
| bm25 | 0.0065 | 0.0044–0.0096 |
| bm25_no_length_norm | 0.0065 | 0.0043–0.0097 |

Tiny timings are sensitive to scheduling, warmup and timer overhead. They are not capacity benchmarks or performance rankings. Repeated deterministic runs are not independent quality samples. API cost is zero; electricity/compute cost is not measured.

## Observations

`restore progress after crash` did not retrieve the checkpoint document because none of its words occur in that document. Changing length normalization did not improve aggregate fixture quality. A separate controlled unit test demonstrates the ranking change between equal-term-frequency documents of unequal length.

## Interpretation

The stated lexical/paraphrase hypothesis held on this intentionally constructed diagnostic. BM25 provided no measured aggregate quality gain over word overlap here. This does not establish equivalence on real data: the corpus is tiny, its query labels were co-designed, and no held-out evaluation was performed. No generalization, statistical significance or novelty is claimed.

## Unresolved questions

- Can the owner explain the formula, reproduce the failures and predict the ablation? Review is pending; no skill mastery is claimed.
- What useful retrieval task and independently curated dataset should drive the next comparison?
- Would query expansion or dense retrieval help those independent cases, and at what cost?

## Reproduction

Follow the commands in README.md, choosing a new output filename. Hashes identify the executable sources and fixture even while they remain uncommitted. Timings and timestamps vary; rankings and aggregate quality should reproduce.
