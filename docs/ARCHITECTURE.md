# TOKNZ Architecture

TOKNZ is a semantic/context-processing layer for inference AI.

Its architectural boundary is intentionally narrow:

```text
Sources / memory / retrieval / stream
                ↓
              TOKNZ
semantic state + context resolution
                ↓
        inference system
```

## Design principles

1. **State before inference** — downstream inference receives a resolved semantic state rather than unbounded raw history.
2. **Meaning before compression** — context may be compressed only after objectives, constraints, relationships, unknowns, and conflicts have been resolved.
3. **Delta before replay** — subsequent turns evolve prior state by explicit changes instead of reconstructing the entire task.
4. **Persistent state != active context** — TOKNZ may retain more state than any one inference call should receive.
5. **Unknowns remain unknown** — missing or conflicting information is represented rather than silently completed.
6. **Model-agnostic contract** — TOKNZ owns semantic/context state; downstream providers own inference.
7. **Pluggable resolution** — deterministic rules, embedding models, classifiers, LLM resolvers, or domain resolvers may all implement semantic extraction behind the same data contract.

## Runtime stages

```text
1. Normalize input
2. Resolve objective
3. Resolve semantic objects
4. Bind constraints
5. Resolve relationships
6. Compare against prior SemanticState
7. Produce SemanticDelta
8. Merge persistent context
9. Preserve unknowns/conflicts
10. Select objective-relative active context
11. Compile InferencePacket
```

## State ownership

TOKNZ owns:

- semantic continuity,
- objective continuity,
- constraint continuity,
- current/persistent context separation,
- delta representation,
- unresolved-state preservation,
- inference packet construction.

TOKNZ does not inherently own:

- long-term storage,
- source retrieval,
- model reasoning,
- tool execution,
- authorization,
- or downstream action.

Those systems may integrate with TOKNZ through bounded inputs and outputs.

## Baseline implementation

`ToknzEngine` is deliberately dependency-free. It is not presented as a frontier semantic parser. It establishes the runtime contract and regression baseline:

```python
text + prior SemanticState + optional retrieved_context
    -> SemanticState
    -> SemanticDelta
    -> InferencePacket
```

Production implementations can replace the extraction/resolution functions without changing the public state contract.

## Compatibility with original TOKNZ

The original `TOKNZ_Py_Demo` remains valid as a lightweight predecessor. Its `TaskState`, delta handling, context compression, constraints, and handoff logic map directly into the expanded architecture.

The expansion changes the category from *pre-reasoning context compression* to *semantic/context processing for inference AI* while preserving the original principle:

> Construct the task state once, then evolve it.
