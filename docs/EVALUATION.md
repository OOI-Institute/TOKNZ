# TOKNZ Evaluation

TOKNZ should be evaluated as a standalone semantic/context-processing module, not only as a token-reduction mechanism.

## Core metrics

- **Objective retention:** the active objective survives across turns.
- **Constraint retention:** explicit constraints persist until superseded.
- **Entity resolution:** important entities remain stable and distinguishable.
- **Alias resolution:** references to the same entity converge correctly.
- **Relationship preservation:** relevant relationships remain available to inference.
- **Dependency preservation:** task-relevant dependencies remain explicit.
- **Delta accuracy:** additions, changes, removals, reaffirmations, and supersessions are separated correctly.
- **Context sufficiency:** active context contains what downstream inference needs.
- **Context precision:** irrelevant persistent state is excluded from a given inference packet.
- **Conflict preservation:** contradictory information remains visible.
- **Unknown preservation:** unresolved state is not silently converted into fact.
- **Semantic drift:** state meaning remains stable unless evidence or input changes it.
- **Inference quality:** downstream results remain useful relative to full-context baselines.
- **Efficiency:** context/token reduction is measured only after quality constraints are satisfied.

## Benchmark structure

Each benchmark should compare at minimum:

1. full raw history,
2. naive recent-window truncation,
3. summary-memory baseline,
4. TOKNZ semantic state + bounded inference packet.

For stochastic model calls, report:

- model and version,
- temperature and decoding settings,
- trial count,
- seeds where available,
- prompt templates,
- raw outputs,
- scoring method,
- confidence intervals where appropriate.

## MVP regression requirements

A release should fail evaluation if it materially reduces:

- objective retention,
- constraint retention,
- entity/relationship consistency,
- conflict visibility,
- unknown visibility,
- or downstream outcome quality.

Compression or context reduction is never considered a success if semantic fidelity degrades materially.

## Suggested benchmark tasks

The MVP should include multi-turn tasks that exercise:

- entity renaming and aliases,
- changing constraints,
- conflicting facts,
- superseded state,
- retrieved context,
- dependency chains,
- evolving objectives,
- bounded context windows,
- and long-turn continuity.

## Reproducibility

Published benchmark claims should be backed by committed test inputs, scoring logic, model settings, and raw or machine-readable results where licensing permits.
