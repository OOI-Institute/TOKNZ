# TOKNZ MVP Scope

This repository is the public, standalone MVP of TOKNZ.

## Included

The MVP includes only the functionality required to demonstrate TOKNZ as a reusable AI/ML component:

- semantic-state data models,
- deterministic baseline semantic extraction,
- entity/concept/relationship/dependency handling,
- objective and constraint continuity,
- risk/permission/task-boundary signals,
- known/unknown/conflict preservation,
- active vs persistent context handling,
- retrieved-context integration,
- semantic delta tracking,
- model-neutral inference packet compilation,
- regression tests,
- model-agnostic usage examples.

## Excluded

This repository intentionally excludes:

- proprietary orchestration systems,
- private company architectures,
- private knowledge bases or datasets,
- internal subsystem naming,
- private safety/governance runtimes,
- proprietary planning or routing systems,
- private agent or robotics infrastructure,
- product-specific connectors,
- non-public research artifacts,
- internal benchmarks or confidential performance data.

## Integration model

TOKNZ is designed to be embedded as a commodity-style module:

```text
Application / Retrieval / Memory
             ↓
           TOKNZ
             ↓
      Inference Provider
             ↓
 Application / Agent / Pipeline
```

Integrators may replace the baseline extractors with their own classifiers, LLMs, embeddings, domain parsers, or learned semantic models while keeping the public `SemanticState`, `SemanticDelta`, and `InferencePacket` contracts.

## Public API rule

A feature belongs in this repository when it can be explained and used as an independent semantic/context-processing capability without relying on knowledge of any private parent system.

If a feature requires proprietary runtime context, company-specific terminology, internal architecture, or confidential data to make sense, it does not belong in the public MVP.
