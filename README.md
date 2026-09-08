# TOKNZ

**Semantic & Context Processing for Inference AI**

TOKNZ is a model-agnostic semantic/context-processing system that converts raw or evolving information into a canonical semantic state before downstream inference.

TOKNZ resolves **what the task means, what matters now, what changed, what persists, what conflicts, what is unknown, and what the inference system actually needs.**

> Raw information does not go directly to inference. TOKNZ parses, partitions, aligns, reconstructs, normalizes, and compiles semantic state first.

## Core architecture

```text
CURRENT INPUT
+ PRIOR SEMANTIC STATE
+ OPTIONAL RETRIEVED / SYSTEM CONTEXT
        ↓
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
        ↓
CANONICAL SEMANTIC STATE
        ↓
BOUNDED INFERENCE PACKET
        ↓
MODEL / AGENT / ROBOT / WORKFLOW
```

## PSA capability integration

TOKNZ now contains the complete semantic parsing/alignment capability lineage previously treated as PSA. PSA is **not a separate runtime layer** in this repository.

Those capabilities are implemented inside TOKNZ as:

- semantic partitioning,
- semantic alignment,
- objective/goal extraction,
- entity and alias resolution,
- relationship and dependency mapping,
- constraint/risk/permission extraction,
- task and context boundary resolution,
- evidence/relevance/uncertainty partitioning,
- temporal/timeline partitioning,
- artifact/execution/output intent resolution,
- canonical semantic framing.

TOKNZ then extends those capabilities with persistent semantic-state recall, active-context reconstruction, delta processing, state normalization, and bounded inference compilation.

## What TOKNZ is

TOKNZ is the semantic-state layer between information and inference.

It can sit between memory/retrieval and inference, or operate directly on streaming and multi-turn input:

```text
Memory / Retrieval / Input
          ↓
        TOKNZ
semantic + contextual resolution
          ↓
      Inference
```

Memory answers **what can be recalled**. TOKNZ answers **what the active information means together and what semantic/context state should be active now**.

## What TOKNZ is not

TOKNZ is not primarily:

- a foundation model,
- a chatbot,
- a vector database,
- a RAG replacement,
- an agent framework,
- a long-term memory store,
- or a text compressor.

Compression is a mechanism inside TOKNZ, not its defining category.

## Core objects

### `SemanticState`

The canonical persistent representation includes:

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

```text
added
changed
removed
reaffirmed
superseded
unresolved
```

### `InferencePacket`

The bounded packet handed to downstream inference contains the canonical state, current delta, selected active context, and a model-neutral inference contract.

## Minimal usage

```python
from toknz import ToknzEngine

engine = ToknzEngine()
packet = engine.process(
    "Plan a safe six-hour stabilization response. Two substations are offline."
)

print(packet.state.objective)
print(packet.state.risks)
print(packet.delta.added)
print(packet.context)
```

Subsequent turns evolve the existing state rather than rebuilding it:

```python
packet = engine.process("One substation is now back online, but load is still rising.")
```

## Repository layout

```text
src/toknz/       semantic/context runtime
tests/           deterministic regression tests
examples/        model-agnostic usage examples
docs/            architecture and evaluation notes
TOKNZ_Py_Demo    original lightweight model demo
*.pdf            original demonstrations/research artifacts
```

The existing demo and PDFs remain preserved as the historical/minimal implementation baseline.

## Evaluation direction

TOKNZ should be evaluated on semantic preservation, objective/constraint retention, alias and relationship resolution, delta accuracy, conflict/unknown preservation, context sufficiency, state drift, inference quality, and context/token efficiency.

Large efficiency claims from earlier demonstrations remain historical repo baselines until reproduced under documented benchmark methodology.

## Legacy material

- `TOKNZ_Py_Demo` — original lightweight continuous-state demo
- `TOKNZ_5Turn_Demo.pdf` — five-turn demonstration
- `TOKNZ_Comparison.pdf` — behavioral comparison
- `toknz_insight.pdf` — original system insight

These artifacts are not removed or invalidated. They represent the first working expression of the same principle: **construct state once, then evolve it.**

## License

See `LICENSE`.
