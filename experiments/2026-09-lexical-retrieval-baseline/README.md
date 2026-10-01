# Experiment: lexical-retrieval-baseline

## Status

Running: implementation and automated checks exist; owner understanding review is pending. This is the sparse first step toward the planned retrieval comparison. Dense, hybrid, vector databases, and reranking are deferred.

## Date

2026-09-29

## Principle and intended product use

Understand lexical ranking, term frequency, inverse document frequency, document length normalization, and retrieval evaluation before adding agentic retrieval. The intended application direction is a research/RAG system; no specific customer use case has been chosen.

## Time/resource budget and stop conditions

This run is limited to 8 documents, 12 queries, 3 configurations, one warmup and 20 timed repetitions per query (756 search calls total), with concurrency 1. No API requests, paid calls, model downloads, or services. Stop if tests fail, rankings vary across repetitions, labels are invalid, or the run exceeds 60 seconds. Dataset size is fixed; expanding it requires a new experiment decision. Compute/electricity cost is not measured. No memory cap is implemented; this tiny fixture is not a resource-isolation test.

## Question

How do word overlap and BM25 behave on exact-word queries versus paraphrases with no matching vocabulary?

## Hypothesis

Both methods will retrieve the labeled document within the top three for the deliberately lexical queries, and neither will retrieve the paraphrase targets when there is no token overlap. BM25's scoring differs from overlap, but an aggregate quality improvement is not assumed. Removing length normalization should affect a controlled unequal-length example; this is verified separately by a unit test.

## Why this matters

A visible lexical failure provides a concrete reason to investigate query expansion or dense retrieval later. Metric correctness and reproducibility come before a larger stack.

## Technology

Python 3.12, standard library only. pytest is already available in the root development environment. No new dependencies. The experiment implementation stays local to this directory.

## Baseline

Count distinct query tokens shared with each document. Compare with positive-IDF BM25, k1=1.2 and b=0.75; ablate document length normalization with b=0. All methods use the same tokenizer, k=3 and deterministic document-ID tie breaking. Zero-score documents are excluded, so an unknown query returns no results.

The exact BM25 variant is:

```text
idf(t) = ln(1 + (N - df(t) + 0.5) / (df(t) + 0.5))
score(d,q) = sum over distinct query tokens t:
  idf(t) * tf(t,d) * (k1 + 1)
  / (tf(t,d) + k1 * (1 - b + b * len(d) / average_length))
```

The added 1 inside the logarithm makes IDF positive; this differs from the unsmoothed log-odds variant. Query term repetition is ignored. No stemming, stopword removal, synonym expansion, embeddings, or token learning is used.

## Environment

The root environment supplies Python and test tooling. The runner records runtime/platform, base Git commit, and SHA-256 hashes of the corpus and executable source. The base commit alone may not contain the uncommitted experiment. Hardware model, available RAM and power usage are not collected; latency is diagnostic only.

## Setup

From repository root with uv installed:

```bash
uv sync --locked
uv run pytest experiments/2026-09-lexical-retrieval-baseline -q
uv run python experiments/2026-09-lexical-retrieval-baseline/run.py --output /tmp/lexical-results.json
```

Use a new output filename for each run: existing files are refused. The current workstation lacks uv on PATH; validation used the existing `.venv/bin/python` and `.venv/bin/pytest` directly. Installing uv remains a bootstrap setup item.

`config.example.yaml` documents fixed runner settings; it is not loaded. Change the explicit configuration in run.py deliberately and record new source hashes. Root pytest selects bootstrap tests only; select this experiment explicitly as shown above.

## Method

`fixture.json` is an AI-authored synthetic English teaching fixture, created for this experiment under the repository MIT license. It contains 8 short documents, 8 lexical queries, and 4 deliberately difficult paraphrases with one binary relevance label each. No external corpus, private data or personal data is included.

Corpus, queries, and labels were co-designed and visible during implementation. There is no train/test split or held-out quality claim. Parameters are fixed, not tuned on these examples. Future quality comparisons require independently curated evaluation cases and a development/evaluation separation.

Warm up each query once, then record all 20 search-only durations using a monotonic clock. Index construction and file IO are excluded. Rankings must be identical across repetitions. Timing repetitions are not independent quality observations. No statistical significance or population confidence interval is claimed.

## Metrics

Recall@3 = number of relevant documents retrieved in the first three / number of relevant documents. Reciprocal rank@3 = inverse rank of the first relevant hit within the first three, or zero. MRR@3 averages that per-query value. Report lexical and paraphrase subsets separately as well as their combined mean. Raw per-query rankings, scores and latency samples are retained.

Success means reproducible execution, correct metric behavior, and documented lexical limitations. No minimum quality gain is required to call this diagnostic informative.

## Results

See [RESULTS.md](RESULTS.md) and the measured artifact it references. Never infer general superiority from this fixture.

## Failure cases

Expected: paraphrases with no token overlap return no documents. Punctuation is discarded, word order is ignored, repeated query tokens do not add weight, and there is no meaning-based matching. Ties depend on document IDs. These are explicit design limitations.

## Cost

API requests and API cost: zero by construction. Local compute/electricity cost: not measured.

## Security/privacy considerations

The runner reads local fixture/source files and the Git commit ID, then writes only the explicitly requested new output file. No network or tool execution from corpus text. Dataset text is data, not executable instructions. This experiment does not test prompt injection or certify deployment compliance.

## Understanding check

Implementation, fixture, labels and initial analysis were AI-assisted. They do not establish the owner's mastery. Before advancing the skill rating:

1. Explain why a rare word can outweigh a common word and why repeated occurrences saturate.
2. Hand-calculate the two-document example in test_hand_calculated_bm25.
3. Predict the result of `restore progress after crash`, run it, and explain the failure.
4. Predict how b=0 changes the controlled long/short-document example; verify with the test.
5. Make a deliberate change, such as token normalization, and record both an improvement and a possible regression on new examples.

## Conclusion

The expected lexical successes and paraphrase failures were observed. BM25 did not improve aggregate quality on this fixture. Owner understanding review remains pending; implementation is not proof of understanding.

## Revisit trigger

After understanding review, construct a broader licensed corpus and independent evaluation queries before comparing dense or hybrid retrieval. Keep the lexical baseline and record whether added complexity improves the chosen task.

## Radar decision

ASSESS: no framework, model, or retrieval service adopted from this diagnostic.

## Official references

Reviewed 2026-09-29: [Introduction to Information Retrieval — Okapi BM25](https://nlp.stanford.edu/IR-book/html/htmledition/okapi-bm25-a-non-binary-model-1.html), by Manning, Raghavan and Schütze. The local formula above specifies the exact positive-IDF variant used.
