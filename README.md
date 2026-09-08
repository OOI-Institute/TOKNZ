# TOKNZ

**Semantic & Context Processing for Inference AI**

TOKNZ is a standalone, model-agnostic semantic/context-processing module for AI and ML systems.

It converts raw or evolving input into a **canonical semantic state** and a **bounded inference packet** so downstream models, agents, applications, and pipelines can reason from resolved context instead of repeatedly reconstructing it from raw history.

> TOKNZ makes context machine-ready before inference.

## Core flow

```text
CURRENT INPUT
+ PRIOR SEMANTIC STATE
+ OPTIONAL RETRIEVED / SYSTEM CONTEXT
        ↓
      TOKNZ
        ↓
semantic parsing + alignment
context reconstruction + continuity
delta resolution + normalization
relevance selection + inference compilation
        ↓
CANONICAL SEMANTIC STATE
        ↓
BOUNDED INFERENCE PACKET
        ↓
MODEL / AGENT / ML PIPELINE / APPLICATION
```

## What TOKNZ resolves

```text
TOKNZ
├─ objective resolution
├─ entity extraction
├─ alias resolution
├─ concept extraction
├─ relationship extraction + typing
├─ dependency identification
├─ constraint binding
├─ risk identification
├─ permission / authority-signal extraction
├─ task-boundary resolution
├─ domain/context resolution
├─ artifact intent
├─ execution intent
├─ output intent
├─ evidence partitioning
├─ relevance partitioning
├─ uncertainty partitioning
├─ temporal / timeline partitioning
├─ knowns / unknowns / conflicts
├─ prior semantic-state recall
├─ active-context reconstruction
├─ persistent-context retention
├─ retrieved-context integration
├─ delta resolution
├─ semantic normalization
└─ inference-context compilation
```

## Core objects

### `SemanticState`

Persistent, structured representation of the active meaning:

```text
objective
entities
aliases
concepts
relationships
dependencies
constraints
risks
permissions
task_boundaries
domains
artifact_intent
execution_intent
output_intent
knowns
unknowns
conflicts
assumptions
evidence_context
relevance_context
uncertainty_context
temporal_context
active_context
persistent_context
provenance
```

### `SemanticDelta`

Explicit change relative to prior state:

```text
added
changed
removed
reaffirmed
superseded
unresolved
```

### `InferencePacket`

A bounded package for downstream inference containing:

- canonical semantic state,
- current semantic delta,
- selected active context,
- unresolved uncertainty/conflicts,
- model-neutral handoff instructions.

## Minimal usage

```python
from toknz import ToknzEngine

engine = ToknzEngine()

packet = engine.process(
    "Plan a six-hour stabilization response. Two substations are offline."
)

print(packet.state.objective)
print(packet.state.entities)
print(packet.delta.added)
print(packet.context)
```

State evolves across turns:

```python
packet = engine.process(
    "One substation is now back online, but load is still rising."
)
```

Retrieved or application context can be injected without changing the public contract:

```python
packet = engine.process(
    "Assess the updated situation.",
    retrieved_context=[
        "Maintenance record: substation A failed last winter.",
        "Policy: load shedding requires operator approval.",
    ],
)
```

## Installation

```bash
pip install -e .
```

Python 3.10+ is required.

## MVP scope

This repository intentionally contains only the standalone TOKNZ module:

```text
src/toknz/       runtime + public data model
tests/           deterministic regression tests
examples/        model-agnostic examples
docs/            public architecture + evaluation docs
```

TOKNZ does not require or expose any proprietary orchestration platform, private knowledge system, internal runtime, or company-specific architecture. It is designed to be independently embedded into AI/ML products.

See [`docs/MVP_SCOPE.md`](docs/MVP_SCOPE.md) for the public product boundary.

## What TOKNZ is not

TOKNZ is not itself:

- a foundation model,
- a chatbot,
- a vector database,
- a RAG system,
- an agent framework,
- a long-term storage engine,
- an authorization engine,
- or an execution runtime.

Those systems can integrate with TOKNZ through normal inputs and outputs.

## Design goal

Memory and retrieval answer **what information is available**.

TOKNZ answers:

> **What does the active information mean together, what changed, what still matters, and what should reach inference now?**

## Evaluation

TOKNZ should be evaluated on:

- semantic preservation,
- objective retention,
- constraint retention,
- entity/alias/relationship resolution,
- delta accuracy,
- context precision and sufficiency,
- conflict/unknown preservation,
- semantic drift,
- downstream inference quality,
- context/token efficiency.

See [`docs/EVALUATION.md`](docs/EVALUATION.md).

## License

Apache-2.0. See `LICENSE`.
