# TOKNZ Architecture

TOKNZ is a semantic and context-processing system for inference AI.

Its job is to transform raw/evolving information into a canonical semantic state before downstream inference.

```text
Sources / memory / retrieval / stream
                ↓
              TOKNZ
semantic parsing + alignment
context reconstruction + continuity
delta resolution + normalization
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
- which entities/concepts exist,
- which aliases resolve to the same identity,
- how entities/concepts relate,
- what dependencies exist,
- what objective is active,
- which constraints and task boundaries apply,
- which risks and permission/authority signals are present,
- which domain/context is active,
- whether the request implies artifact, execution, or informational output,
- what is known, unknown, assumed, conflicting, or uncertain,
- what evidence/time/relevance partitions matter,
- what prior semantic state persists,
- what changed since the prior state,
- and which bounded state should reach inference.

## Unified TOKNZ capability tree

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
│  ├─ permission / authority-signal extraction
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

## PSA integration

The semantic parsing/alignment capability set previously referred to as **PSA** is fully absorbed into TOKNZ.

PSA is not a separate stage or runtime component here.

Historically:

```text
PSA
= parse, partition, align, and structure meaning

TOKNZ
= preserve, reconstruct, normalize, and update semantic context
```

The current architecture combines both responsibilities:

```text
Input
  ↓
TOKNZ
semantic parsing + semantic alignment
+ semantic-state continuity
+ context reconstruction
+ delta resolution
+ inference compilation
  ↓
Inference
```

## Design principles

1. **Meaning before inference** — raw information is resolved into semantic state first.
2. **Meaning before compression** — compression cannot discard objective, constraints, relationships, boundaries, uncertainty, or conflict.
3. **State before replay** — prior state is reused rather than reconstructed every turn.
4. **Delta before full history** — subsequent input updates semantic state explicitly.
5. **Persistent state != active context** — TOKNZ may remember more than one inference call requires.
6. **Unknowns remain unknown** — uncertainty is represented, not silently promoted to fact.
7. **Boundaries persist** — constraints, permissions, and scope survive context reduction.
8. **Model-agnostic contract** — TOKNZ owns semantic state; downstream systems own inference/action.
9. **Pluggable resolution** — deterministic, learned, LLM, embedding, or domain-specific resolvers can implement the same contract.

## Baseline implementation

`ToknzEngine` is a deterministic, dependency-free reference implementation. It is not presented as a frontier semantic parser. It exists to define a concrete runtime contract and testable behavior:

```python
text + prior SemanticState + optional retrieved_context
    -> semantic parsing/alignment
    -> SemanticState
    -> SemanticDelta
    -> InferencePacket
```

Stronger semantic resolvers may replace individual extraction functions without changing the public data model.

## State ownership boundary

TOKNZ owns semantic/context state preparation. It does not inherently own long-term storage, source retrieval, downstream reasoning, tool execution, authorization decisions, or external action. Those systems can integrate through bounded inputs and outputs.

## Compatibility with original TOKNZ

The original `TOKNZ_Py_Demo` remains a valid lightweight predecessor. Its task state, delta handling, context compression, constraints, and handoff logic map directly into the expanded architecture.

The current architecture preserves the original principle:

> **Construct semantic state once, then evolve it.**
