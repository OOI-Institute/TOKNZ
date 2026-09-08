from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Relationship:
    subject: str
    predicate: str
    object: str
    confidence: float = 1.0
    provenance: str = "input"


@dataclass
class SemanticState:
    objective: str = ""
    entities: List[str] = field(default_factory=list)
    aliases: Dict[str, str] = field(default_factory=dict)
    concepts: List[str] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    task_boundaries: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)
    artifact_intent: str = ""
    execution_intent: str = ""
    output_intent: str = ""
    assumptions: List[str] = field(default_factory=list)
    knowns: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    evidence_context: List[str] = field(default_factory=list)
    relevance_context: List[str] = field(default_factory=list)
    uncertainty_context: List[str] = field(default_factory=list)
    temporal_context: List[str] = field(default_factory=list)
    active_context: List[str] = field(default_factory=list)
    persistent_context: List[str] = field(default_factory=list)
    provenance: Dict[str, str] = field(default_factory=dict)


@dataclass
class SemanticDelta:
    added: List[str] = field(default_factory=list)
    changed: List[str] = field(default_factory=list)
    removed: List[str] = field(default_factory=list)
    reaffirmed: List[str] = field(default_factory=list)
    superseded: List[str] = field(default_factory=list)
    unresolved: List[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not any(
            (
                self.added,
                self.changed,
                self.removed,
                self.reaffirmed,
                self.superseded,
                self.unresolved,
            )
        )


@dataclass
class InferencePacket:
    state: SemanticState
    delta: SemanticDelta
    context: List[str]
    handoff: str
