from __future__ import annotations

import re
from dataclasses import replace
from typing import Iterable, List, Optional

from .models import InferencePacket, Relationship, SemanticDelta, SemanticState


class ToknzEngine:
    """Deterministic baseline semantic/context processor.

    The baseline intentionally stays model-agnostic and dependency-free. More advanced
    semantic resolvers can replace or extend the extraction hooks without changing the
    SemanticState / InferencePacket contract.
    """

    CHANGE_MARKERS = ("now", "changed", "updated", "instead", "but", "however", "back online", "offline")
    CONSTRAINT_MARKERS = {
        "safe": "safety-sensitive",
        "risk": "risk-sensitive",
        "must": "hard-requirement",
        "cannot": "prohibited-action-present",
        "don't": "negative-constraint-present",
        "do not": "negative-constraint-present",
        "immediate": "time-sensitive",
        "now": "time-sensitive",
        "final": "completion-oriented",
    }

    def __init__(self, max_active_context: int = 8, max_persistent_context: int = 32):
        self.state = SemanticState()
        self.max_active_context = max_active_context
        self.max_persistent_context = max_persistent_context
        self.turn = 0

    def process(self, text: str, retrieved_context: Optional[Iterable[str]] = None) -> InferencePacket:
        text = self._normalize(text)
        if not text:
            raise ValueError("TOKNZ requires non-empty input")

        prior = self.state
        self.turn += 1

        sentences = self._sentences(text)
        retrieved = [self._normalize(x) for x in (retrieved_context or []) if self._normalize(x)]
        objective = prior.objective or self._resolve_objective(text)
        constraints = self._stable_unique(prior.constraints + self._extract_constraints(text))
        entities = self._stable_unique(prior.entities + self._extract_entities(text))
        concepts = self._stable_unique(prior.concepts + self._extract_concepts(text))
        relationships = self._merge_relationships(prior.relationships, self._extract_relationships(text))

        delta = self._resolve_delta(prior, sentences)
        persistent = self._stable_unique(prior.persistent_context + sentences + retrieved)[-self.max_persistent_context :]
        active = self._select_active_context(text, persistent)
        knowns = self._stable_unique(prior.knowns + sentences)
        unknowns = self._resolve_unknowns(text, prior.unknowns)
        conflicts = self._resolve_conflicts(text, prior.conflicts)

        provenance = dict(prior.provenance)
        for item in sentences:
            provenance[item] = f"turn:{self.turn}:input"
        for item in retrieved:
            provenance[item] = f"turn:{self.turn}:retrieved"

        self.state = SemanticState(
            objective=objective,
            entities=entities,
            concepts=concepts,
            relationships=relationships,
            constraints=constraints,
            assumptions=list(prior.assumptions),
            knowns=knowns,
            unknowns=unknowns,
            conflicts=conflicts,
            active_context=active,
            persistent_context=persistent,
            provenance=provenance,
        )

        return InferencePacket(
            state=self.state,
            delta=delta,
            context=active,
            handoff=self._compile_handoff(self.state, delta),
        )

    def _resolve_objective(self, text: str) -> str:
        first = self._sentences(text)[0]
        lowered = text.lower()
        if any(x in lowered for x in ("plan", "create", "build", "design")):
            return first
        if any(x in lowered for x in ("identify", "analyze", "assess", "evaluate")):
            return first
        return f"Maintain and advance the active task state: {first}"

    def _extract_constraints(self, text: str) -> List[str]:
        lowered = text.lower()
        return [label for marker, label in self.CONSTRAINT_MARKERS.items() if marker in lowered]

    def _extract_entities(self, text: str) -> List[str]:
        # Deterministic baseline: named-like tokens, identifiers, and quantities with units.
        candidates = re.findall(r"\b(?:[A-Z][A-Za-z0-9_-]{2,}|[A-Za-z]+[-_][A-Za-z0-9_-]+|\d+(?:\.\d+)?\s?(?:hours?|days?|%|MW|GW))\b", text)
        return self._stable_unique(candidates)

    def _extract_concepts(self, text: str) -> List[str]:
        stop = {"the", "and", "that", "this", "with", "from", "what", "have", "into", "our", "but", "are", "for", "now"}
        words = re.findall(r"[A-Za-z][A-Za-z-]{3,}", text.lower())
        freq = {}
        for word in words:
            if word not in stop:
                freq[word] = freq.get(word, 0) + 1
        return [word for word, _ in sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:12]]

    def _extract_relationships(self, text: str) -> List[Relationship]:
        relationships: List[Relationship] = []
        patterns = [
            (r"\b(.{2,50}?)\s+is\s+(.{2,60}?)(?:[.;]|$)", "is"),
            (r"\b(.{2,50}?)\s+causes?\s+(.{2,60}?)(?:[.;]|$)", "causes"),
            (r"\b(.{2,50}?)\s+requires?\s+(.{2,60}?)(?:[.;]|$)", "requires"),
        ]
        for pattern, predicate in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                subject = match.group(1).strip(" ,")
                obj = match.group(2).strip(" ,")
                if 1 < len(subject.split()) <= 8 and 1 <= len(obj.split()) <= 10:
                    relationships.append(Relationship(subject, predicate, obj))
        return relationships

    def _resolve_delta(self, prior: SemanticState, sentences: List[str]) -> SemanticDelta:
        if not prior.persistent_context:
            return SemanticDelta(added=list(sentences))

        prior_norm = {self._canonical(x): x for x in prior.persistent_context}
        added, changed, reaffirmed = [], [], []
        for sentence in sentences:
            key = self._canonical(sentence)
            if key in prior_norm:
                reaffirmed.append(sentence)
            elif any(marker in sentence.lower() for marker in self.CHANGE_MARKERS):
                changed.append(sentence)
            else:
                added.append(sentence)

        unresolved = []
        for sentence in sentences:
            if "?" in sentence or any(x in sentence.lower() for x in ("unknown", "unclear", "uncertain", "not sure")):
                unresolved.append(sentence)
        return SemanticDelta(added=added, changed=changed, reaffirmed=reaffirmed, unresolved=unresolved)

    def _resolve_unknowns(self, text: str, prior: List[str]) -> List[str]:
        unknowns = list(prior)
        for sentence in self._sentences(text):
            if "?" in sentence or any(x in sentence.lower() for x in ("unknown", "unclear", "uncertain", "not sure")):
                unknowns.append(sentence)
        return self._stable_unique(unknowns)

    def _resolve_conflicts(self, text: str, prior: List[str]) -> List[str]:
        conflicts = list(prior)
        lowered = text.lower()
        if any(x in lowered for x in ("conflict", "contradict", "inconsistent", "but", "however")):
            conflicts.extend([s for s in self._sentences(text) if any(x in s.lower() for x in ("but", "however", "conflict", "contradict", "inconsistent"))])
        return self._stable_unique(conflicts)

    def _select_active_context(self, text: str, persistent: List[str]) -> List[str]:
        query_terms = set(re.findall(r"[a-z0-9]+", text.lower()))

        def score(item: str) -> tuple[int, int]:
            terms = set(re.findall(r"[a-z0-9]+", item.lower()))
            overlap = len(query_terms & terms)
            recency = persistent.index(item)
            return overlap, recency

        ranked = sorted(persistent, key=score, reverse=True)
        return ranked[: self.max_active_context]

    def _compile_handoff(self, state: SemanticState, delta: SemanticDelta) -> str:
        context = "\n".join(f"- {x}" for x in state.active_context) or "- none"
        constraints = ", ".join(state.constraints) or "none"
        unknowns = "\n".join(f"- {x}" for x in state.unknowns[-5:]) or "- none"
        conflicts = "\n".join(f"- {x}" for x in state.conflicts[-5:]) or "- none"
        changes = delta.changed + delta.added
        change_text = "\n".join(f"- {x}" for x in changes) or "- no material new state"
        return (
            "TOKNZ INFERENCE PACKET\n\n"
            f"OBJECTIVE:\n{state.objective}\n\n"
            f"CONSTRAINTS:\n{constraints}\n\n"
            f"CURRENT DELTA:\n{change_text}\n\n"
            f"ACTIVE CONTEXT:\n{context}\n\n"
            f"UNKNOWNS:\n{unknowns}\n\n"
            f"CONFLICTS:\n{conflicts}\n\n"
            "INFERENCE CONTRACT:\n"
            "Continue from the resolved semantic state. Preserve constraints and unresolved conflicts. "
            "Do not reconstruct irrelevant history unless required by the objective."
        )

    @staticmethod
    def _merge_relationships(existing: List[Relationship], incoming: List[Relationship]) -> List[Relationship]:
        seen = {(r.subject.lower(), r.predicate.lower(), r.object.lower()) for r in existing}
        result = list(existing)
        for rel in incoming:
            key = (rel.subject.lower(), rel.predicate.lower(), rel.object.lower())
            if key not in seen:
                seen.add(key)
                result.append(rel)
        return result

    @staticmethod
    def _sentences(text: str) -> List[str]:
        return [x.strip() for x in re.split(r"(?<=[.!?])\s+|\n+", text) if x.strip()]

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", (text or "").strip())

    @staticmethod
    def _canonical(text: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

    @staticmethod
    def _stable_unique(items: Iterable[str]) -> List[str]:
        seen, result = set(), []
        for item in items:
            key = item.lower().strip()
            if key and key not in seen:
                seen.add(key)
                result.append(item)
        return result
