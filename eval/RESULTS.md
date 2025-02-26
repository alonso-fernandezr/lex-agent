# Retrieval Eval Results

Measures the retriever config in `chains.py` (`search_type="similarity_score_threshold"`, `k=10`, `score_threshold=0.3`) against a small, human-verified golden QA set. Eval-only — no production code changed.

## Method

- 18 candidate chunks sampled from the ingested corpus (`chroma_db_legal_bot_part1`, 1006 chunks), filtered by a cheap heuristic (`eval/chunk_sampling.py`) for likely-self-contained, non-fragment text and a minimum length (to exclude ~27 short non-legal "greeting" entries seeded in the corpus for small talk).
- One candidate question drafted per chunk by `gpt-4o-mini` (`eval/qa_generation.py`), then manually reviewed against a 3-point checklist: the answer is explicit in the chunk, the chunk is self-contained (or at least the answer-bearing portion of it is), and the question isn't answerable by other chunks. 4 of 22 initial candidates were rejected and replaced on this basis; the final 18 all passed review.
- Each question run through the retriever in isolation (`eval/retrieval_eval.py`) — no LLM generation involved, this measures retrieval only.
- Scoring matches on exact `page_content` string equality — the pinned `langchain-chroma` version doesn't expose a stable chunk id on retrieval, so the retrieved chunk's text is the only reliable identity signal.

## Results

| Metric | Value |
|---|---|
| Recall@10 | 94.4% (17/18) |
| MRR | 0.789 |
| 95% CI (Wilson) on Recall@10 | 74.2% – 99.0% |

**n=18 is a directional signal, not a precise estimate** — the confidence interval above spans ~25 points. This sample size was a deliberate choice (see PR description / issue #15 discussion): cheap enough to fully human-verify each item, sized to catch a gross retrieval failure, not to pin down whether true recall is 90% or 98%.

## Failure analysis

**One miss** (question: *"What topics are included in the Eleventh Schedule under Article 243G?"*) — the retriever's top 10 never surfaced the actual Eleventh Schedule chunk. Instead it returned content from the Fifth, Sixth, and Seventh Schedules plus other Article 243-series provisions. This looks like a real, specific weakness: the Constitution has several structurally similar numbered schedules (lists of topics/subjects), and a generically-phrased "what topics are in Schedule X" question doesn't discriminate well between them at the embedding level.

**One near-miss** (question about the Rajasthan Colonisation Act) — retrieved, but at rank 9, just inside the `k=10` cutoff. A slightly harder phrasing of the same question would plausibly drop below the threshold or outside `k=10` entirely.

## Scope

No changes to `chains.py`/`prompts.py`/`lawglance_main.py`. No parameter sweep over `k`/`score_threshold` in this PR — reported at the current config only, per the staged plan; a sweep is a reasonable follow-up if there's interest.
