# TOKNZ Architecture

TOKNZ is a standalone semantic and context-processing module for inference AI.

Its public boundary is intentionally narrow:

```text
Sources / memory / retrieval / stream
                ↓
              TOKNZ
semantic parsing + alignment
context reconstruction + continuity
delta resolution + normalization
relevance selection + inference compilation
                ↓
       Canonical Semantic State
                ↓
        InferencePacket
                ↓
        inference system
```

## Canonical responsibility

TOKNZ determines:

- what the active information means,
- which entities and concepts exist,
- which aliases resolve to the same identity,
- how entities and concepts relate,
- what dependencies exist,
- what objective is active,
- which constraints and task boundaries apply,
- which risks and permission signals are present,
- which domain/context is active,
- whether the request implies artifact, execution, or informational output,
- what is known, unknown, assumed, conflicting, or uncertain,
- what evidence, relevance, and temporal partitions matter,
- what prior semantic state persists,
- what changed since the prior state,
- and which bounded state should reach inference.

## Capability tree

```text
TOKNZ
├─ Semantic Parsing + Alignment
│  ├─ objective / goal resolution
│  ├─ entity extraction
│  ├─ entity identity + alias resolution
│  ├─ concept extraction
│  ├─ relationship extraction + typing
│  ├─ dependency identification
│  ├─ constraint binding
│  ├─ risk identification
│  ├─ permission-signal extraction
│  ├─ task-boundary resolution
│  ├─ domain/context resolution
│  ├─ artifact intent
│  ├─ execution intent
│  ├─ output intent
│  ├─ evidence partitioning
│  ├─ relevance partitioning
│  ├─ uncertainty partitioning
│  ├─ temporal/timeline partitioning
│  └─ canonical semantic framing
│
├─ Semantic State Resolution
│  ├─ knowns
│  ├─ unknowns
│  ├─ assumptions
│  ├─ conflicts
│  ├─ relationships / dependencies
│  └─ active objective
│
├─ Context Processing
│  ├─ prior semantic-state recall
│  ├─ relevant-history reconstruction
│  ├─ active-context reconstruction
│  ├─ persistent-context retention
│  ├─ retrieved-context integration
│  └─ irrelevant-context suppression
│
├─ Temporal / Delta Processing
│  ├─ added
│  ├─ changed
│  ├─ removed
│  ├─ superseded
│  ├─ reaffirmed
│  └─ unresolved
│
├─ Semantic Normalization
│  ├─ canonical terminology
│  ├─ duplicate resolution
│  ├─ identity normalization
│  ├─ relationship normalization
│  └─ constraint normalization
│
└─ Inference Context Compilation
   ├─ objective-relative state selection
   ├─ required constraint/boundary preservation
   ├─ uncertainty/conflict preservation
   ├─ redundant-context reduction
   └─ bounded inference packet
```

## Design principles

1. **Meaning before inference** — raw input is resolved into semantic state first.
2. **Meaning before compression** — context reduction must not discard objectives, constraints, relationships, boundaries, uncertainty, or conflict.
3. **State continuity** — prior state is reused rather than rebuilt every turn.
4. **Explicit deltas** — new input updates prior state through represented change.
5. **Persistent state != active context** — TOKNZ may retain more state than a single inference call needs.
6. **Unknowns remain unknown** — uncertainty is represented rather than silently promoted to fact.
7. **Boundaries persist** — constraints, permissions, and scope survive context reduction.
8. **Model-agnostic contract** — TOKNZ owns semantic/context preparation; downstream systems own inference and action.
9. **Pluggable resolution** — deterministic rules, learned models, LLMs, embeddings, or domain resolvers may implement extraction behind the same public contract.

## Baseline implementation

`ToknzEngine` is a dependency-free reference implementation designed to establish the public API and testable MVP behavior:

```python
text + prior SemanticState + optional retrieved_context
    -> semantic/context resolution
    -> SemanticState
    -> SemanticDelta
    -> InferencePacket
```

The baseline is intentionally replaceable. Production users can swap individual extraction/resolution functions with stronger learned components while preserving the public data model.

## Public state boundary

TOKNZ owns:

- semantic-state preparation,
- semantic continuity,
- objective and constraint continuity,
- entity/relationship/dependency representation,
- active vs persistent context separation,
- delta representation,
- unresolved-state preservation,
- inference packet construction.

TOKNZ does not inherently own:

- long-term storage,
- source retrieval,
- proprietary knowledge bases,
- planning/orchestration systems,
- model reasoning,
- tool execution,
- authorization decisions,
- external action,
- or private runtime infrastructure.

Those systems may integrate through bounded public inputs and outputs.

## Standalone architecture rule

The repository defines TOKNZ only. Public code and documentation must remain independent of any parent platform, private runtime, internal subsystem naming, or proprietary architecture lineage.

> **Construct semantic state once, then evolve it.**
