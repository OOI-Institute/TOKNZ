# TOKNZ

**Semantic & Context Processing for Inference AI**

TOKNZ is a model-agnostic semantic/context-processing system that prepares bounded, decision-ready state for downstream inference.

Instead of forcing every model, agent, robot, or workflow to reinterpret raw history from scratch, TOKNZ resolves the active semantic state: **what the task means, what matters now, what changed, what persists, what conflicts, and what the inference system actually needs.**

> Raw information does not go directly to inference. TOKNZ resolves meaning and context first, then compiles a bounded inference packet.

## Core flow

```text
CURRENT INPUT
+ PRIOR SEMANTIC STATE
+ OPTIONAL RETRIEVED / SYSTEM CONTEXT
        ↓
SEMANTIC RESOLUTION
entities · concepts · relationships · objectives
constraints · assumptions · knowns · unknowns
        ↓
CONTEXT RESOLUTION
active · persistent · superseded · conflicting · irrelevant
        ↓
DELTA RESOLUTION
added · changed · removed · reaffirmed · unresolved
        ↓
SEMANTIC STATE
        ↓
INFERENCE PACKET COMPILER
        ↓
MODEL / AGENT / ROBOT / WORKFLOW
```

## What TOKNZ is

TOKNZ is a semantic/context layer for inference systems. It can sit between memory/retrieval and inference, or operate directly on streaming/multi-turn input.

It is designed to:

- reconstruct persistent semantic state across turns,
- preserve objectives and constraints,
- track explicit state changes,
- resolve relationships and dependencies,
- separate persistent context from currently active context,
- preserve conflicts and unknowns rather than silently flattening them,
- reduce irrelevant context before inference,
- compile model-neutral inference packets.

## What TOKNZ is not

TOKNZ is not primarily:

- a foundation model,
- a chatbot,
- a vector database,
- a RAG replacement,
- an agent framework,
- a long-term memory store,
- or a text compressor.

Compression remains useful, but it is a mechanism inside the broader semantic/context-processing system.

## Minimal usage

```python
from toknz import ToknzEngine

engine = ToknzEngine()
packet = engine.process("Plan a safe six-hour stabilization response for the grid event.")

print(packet.state.objective)
print(packet.delta.added)
print(packet.context)
```

Subsequent turns evolve the existing state rather than rebuilding it:

```python
packet = engine.process("One substation is back online, but load is still rising.")
```

## Core objects

### `SemanticState`

The persistent internal representation of the active task/world meaning:

```text
objective
entities
concepts
relationships
constraints
assumptions
knowns
unknowns
conflicts
active_context
persistent_context
provenance
```

### `SemanticDelta`

What changed relative to the prior state:

```text
added
changed
removed
reaffirmed
unresolved
```

### `InferencePacket`

The bounded state handed to downstream inference:

```text
semantic state
current delta
selected context
constraints
unknowns/conflicts
handoff instruction
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

The original demo and PDFs remain part of the repository as the historical/minimal implementation baseline.

## Relationship to memory and RAG

A useful separation is:

```text
Memory / Retrieval
        ↓
TOKNZ
semantic + contextual resolution
        ↓
Inference
```

Memory answers **what can be recalled**. TOKNZ answers **what the active information means together and what should be active for this inference call**.

## Evaluation direction

TOKNZ should be evaluated on more than token count. Primary metrics include:

- semantic preservation,
- objective retention,
- constraint retention,
- delta accuracy,
- conflict/unknown preservation,
- context sufficiency,
- state drift,
- inference quality,
- and token/context efficiency.

Large efficiency claims from earlier demonstrations should be treated as historical repo baselines until reproduced under a documented benchmark methodology.

## Legacy material

The repository preserves the established work:

- `TOKNZ_Py_Demo` — original lightweight continuous-state demo
- `TOKNZ_5Turn_Demo.pdf` — five-turn demonstration
- `TOKNZ_Comparison.pdf` — behavioral comparison
- `toknz_insight.pdf` — original system insight

These artifacts are not removed or invalidated by the semantic-context expansion. They represent the first working expression of the same core principle: **construct state once, then evolve it.**

## License

See `LICENSE`.
