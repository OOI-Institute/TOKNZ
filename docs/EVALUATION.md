# TOKNZ Evaluation

TOKNZ should be evaluated as a semantic/context-processing system, not only as a token-reduction mechanism.

## Core metrics

- **Objective retention:** active objective survives across turns.
- **Constraint retention:** explicit constraints persist until superseded.
- **Delta accuracy:** additions/changes/reaffirmations are correctly separated.
- **Context sufficiency:** active context contains what downstream inference needs.
- **Context precision:** irrelevant persistent state is excluded from a given inference packet.
- **Conflict preservation:** contradictory information remains visible.
- **Unknown preservation:** unresolved state is not silently converted into fact.
- **Semantic drift:** state meaning remains stable unless evidence/input changes it.
- **Inference quality:** downstream results are at least as useful as full-history baselines.
- **Efficiency:** token/context reduction is measured only after quality constraints are satisfied.

## Benchmark structure

Each benchmark should compare at minimum:

1. full raw history,
2. naive recent-window truncation,
3. summary-memory baseline,
4. TOKNZ semantic state + bounded inference packet.

For stochastic model calls, report model/version, temperature, trial count, seeds where available, prompt templates, raw outputs, scoring method, and confidence intervals.

## Historical efficiency claims

Earlier repository demonstrations reported substantial context/token savings across long-horizon scenarios. Those results remain part of TOKNZ's development history, but large numerical claims should be considered **historical baselines** until reproduced under the benchmark methodology above with raw artifacts committed to `benchmarks/`.

## Regression requirement

New TOKNZ versions should not improve compression by losing task meaning. A release should fail evaluation if it materially reduces:

- objective retention,
- constraint retention,
- conflict visibility,
- unknown visibility,
- or downstream outcome quality.
