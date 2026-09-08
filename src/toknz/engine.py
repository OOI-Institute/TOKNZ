from __future__ import annotations

import re
from typing import Dict, Iterable, List, Optional

from .models import InferencePacket, Relationship, SemanticDelta, SemanticState


class ToknzEngine:
    """Dependency-free TOKNZ semantic/context processor.

    TOKNZ owns semantic parsing/alignment, semantic-state continuity, context
    reconstruction, delta resolution, normalization, and inference-packet
    compilation. The deterministic baseline is intentionally replaceable by
    stronger resolvers without changing the public SemanticState contract.
    """

    CHANGE_MARKERS = (
        "now", "changed", "updated", "instead", "but", "however",
        "back online", "offline", "no longer", "replaced", "became",
    )

    CONSTRAINT_MARKERS = {
        "safe": "safety-sensitive",
        "risk": "risk-sensitive",
        "must": "hard-requirement",
        "cannot": "prohibited-action-present",
        "can't": "prohibited-action-present",
        "don't": "negative-constraint-present",
        "do not": "negative-constraint-present",
        "avoid": "avoidance-constraint-present",
        "immediate": "time-sensitive",
        "now": "time-sensitive",
        "final": "completion-oriented",
    }

    DOMAIN_MARKERS = {
        "infrastructure": ("grid", "substation", "power", "water", "diesel", "utility"),
        "operations": ("plan", "schedule", "workflow", "response", "operations"),
        "safety": ("safe", "risk", "hazard", "unsafe"),
        "software": ("code", "api", "python", "repository", "software"),
        "robotics": ("robot", "robotic", "sensor", "actuator", "manipulator"),
        "research": ("hypothesis", "study", "experiment", "evidence", "research"),
    }

    ARTIFACT_MARKERS = {
        "report": "report",
        "document": "document",
        "diagram": "diagram",
        "dashboard": "dashboard",
        "code": "code",
        "script": "code",
        "plan": "plan",
        "table": "table",
        "presentation": "presentation",
    }

    EXECUTION_MARKERS = (
        "run", "execute", "send", "push", "deploy", "create", "build",
        "update", "modify", "write", "generate", "call", "move", "act",
    )

    PERMISSION_MARKERS = (
        "allowed", "authorized", "permission", "may", "can", "cannot",
        "can't", "must not", "do not", "only", "requires approval",
    )

    RISK_MARKERS = (
        "risk", "hazard", "unsafe", "failure", "danger", "harm",
        "critical", "outage", "collapse", "breach",
    )

    TEMPORAL_MARKERS = (
        "now", "today", "tomorrow", "yesterday", "currently", "previously",
        "before", "after", "later", "earlier", "hours", "days", "weeks",
        "timeline", "deadline", "until", "since",
    )

    UNCERTAINTY_MARKERS = (
        "unknown", "unclear", "uncertain", "not sure", "maybe", "possibly",
        "likely", "appears", "could", "might", "?",
    )

    EVIDENCE_MARKERS = (
        "evidence", "source", "data", "record", "report", "observed",
        "measurement", "sensor", "log", "document", "retrieved",
    )

    def __init__(self, max_active_context: int = 10, max_persistent_context: int = 48):
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
        entities = self._stable_unique(prior.entities + self._extract_entities(text))
        aliases = self._merge_aliases(prior.aliases, self._extract_aliases(text))
        concepts = self._stable_unique(prior.concepts + self._extract_concepts(text))
        relationships = self._merge_relationships(prior.relationships, self._extract_relationships(text))
        dependencies = self._stable_unique(prior.dependencies + self._extract_dependencies(text))
        constraints = self._stable_unique(prior.constraints + self._extract_constraints(text))
        risks = self._stable_unique(prior.risks + self._extract_risks(text))
        permissions = self._stable_unique(prior.permissions + self._extract_permissions(text))
        task_boundaries = self._stable_unique(prior.task_boundaries + self._extract_task_boundaries(text))
        domains = self._stable_unique(prior.domains + self._resolve_domains(text))
        artifact_intent = self._resolve_artifact_intent(text) or prior.artifact_intent
        execution_intent = self._resolve_execution_intent(text) or prior.execution_intent
        output_intent = self._resolve_output_intent(text) or prior.output_intent
        assumptions = self._stable_unique(prior.assumptions + self._extract_assumptions(text))

        delta = self._resolve_delta(prior, sentences)
        persistent = self._stable_unique(prior.persistent_context + sentences + retrieved)[-self.max_persistent_context :]
        active = self._select_active_context(text, persistent)

        knowns = self._stable_unique(prior.knowns + sentences + retrieved)
        unknowns = self._resolve_unknowns(text, prior.unknowns)
        conflicts = self._resolve_conflicts(text, prior.conflicts)

        evidence_context = self._stable_unique(
            prior.evidence_context + self._partition_evidence(sentences + retrieved)
        )
        uncertainty_context = self._stable_unique(
            prior.uncertainty_context + self._partition_uncertainty(sentences)
        )
        temporal_context = self._stable_unique(
            prior.temporal_context + self._partition_temporal(sentences)
        )
        relevance_context = list(active)

        provenance = dict(prior.provenance)
        for item in sentences:
            provenance[item] = f"turn:{self.turn}:input"
        for item in retrieved:
            provenance[item] = f"turn:{self.turn}:retrieved"

        self.state = SemanticState(
            objective=objective,
            entities=entities,
            aliases=aliases,
            concepts=concepts,
            relationships=relationships,
            dependencies=dependencies,
            constraints=constraints,
            risks=risks,
            permissions=permissions,
            task_boundaries=task_boundaries,
            domains=domains,
            artifact_intent=artifact_intent,
            execution_intent=execution_intent,
            output_intent=output_intent,
            assumptions=assumptions,
            knowns=knowns,
            unknowns=unknowns,
            conflicts=conflicts,
            evidence_context=evidence_context,
            relevance_context=relevance_context,
            uncertainty_context=uncertainty_context,
            temporal_context=temporal_context,
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

    # ------------------------------------------------------------------
    # Semantic parsing/alignment (absorbed PSA capability surface)
    # ------------------------------------------------------------------

    def _resolve_objective(self, text: str) -> str:
        first = self._sentences(text)[0]
        lowered = text.lower()
        if any(x in lowered for x in ("plan", "create", "build", "design", "update", "find")):
            return first
        if any(x in lowered for x in ("identify", "analyze", "assess", "evaluate", "explain")):
            return first
        return f"Maintain and advance the active task state: {first}"

    def _extract_entities(self, text: str) -> List[str]:
        candidates = re.findall(
            r"\b(?:[A-Z][A-Za-z0-9_-]{2,}|[A-Za-z]+[-_][A-Za-z0-9_-]+|\d+(?:\.\d+)?\s?(?:hours?|days?|weeks?|%|MW|GW))\b",
            text,
        )
        return self._stable_unique(candidates)

    def _extract_aliases(self, text: str) -> Dict[str, str]:
        aliases: Dict[str, str] = {}
        patterns = [
            r"\b([A-Z][A-Za-z0-9_-]+)\s*\((?:also known as|aka|formerly)\s+([^\)]+)\)",
            r"\b([A-Z][A-Za-z0-9_-]+)\s+(?:also known as|aka)\s+([A-Z][A-Za-z0-9_-]+)",
            r"\b([A-Z][A-Za-z0-9_-]+)\s*=\s*([A-Z][A-Za-z0-9_-]+)\b",
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                canonical = match.group(1).strip()
                alias = match.group(2).strip()
                aliases[alias] = canonical
        return aliases

    def _extract_concepts(self, text: str) -> List[str]:
        stop = {
            "the", "and", "that", "this", "with", "from", "what", "have",
            "into", "our", "but", "are", "for", "now", "should", "would",
        }
        words = re.findall(r"[A-Za-z][A-Za-z-]{3,}", text.lower())
        freq: Dict[str, int] = {}
        for word in words:
            if word not in stop:
                freq[word] = freq.get(word, 0) + 1
        return [word for word, _ in sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:16]]

    def _extract_relationships(self, text: str) -> List[Relationship]:
        relationships: List[Relationship] = []
        patterns = [
            (r"\b(.{2,50}?)\s+is\s+(.{2,60}?)(?:[.;]|$)", "is"),
            (r"\b(.{2,50}?)\s+causes?\s+(.{2,60}?)(?:[.;]|$)", "causes"),
            (r"\b(.{2,50}?)\s+requires?\s+(.{2,60}?)(?:[.;]|$)", "requires"),
            (r"\b(.{2,50}?)\s+depends on\s+(.{2,60}?)(?:[.;]|$)", "depends_on"),
            (r"\b(.{2,50}?)\s+belongs to\s+(.{2,60}?)(?:[.;]|$)", "belongs_to"),
            (r"\b(.{2,50}?)\s+affects?\s+(.{2,60}?)(?:[.;]|$)", "affects"),
        ]
        for pattern, predicate in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                subject = match.group(1).strip(" ,")
                obj = match.group(2).strip(" ,")
                if 1 < len(subject.split()) <= 8 and 1 <= len(obj.split()) <= 10:
                    relationships.append(Relationship(subject, predicate, obj))
        return relationships

    def _extract_dependencies(self, text: str) -> List[str]:
        result = []
        for sentence in self._sentences(text):
            lowered = sentence.lower()
            if any(x in lowered for x in ("depends on", "requires", "blocked by", "before", "after")):
                result.append(sentence)
        return result

    def _extract_constraints(self, text: str) -> List[str]:
        lowered = text.lower()
        return [label for marker, label in self.CONSTRAINT_MARKERS.items() if marker in lowered]

    def _extract_risks(self, text: str) -> List[str]:
        return [
            sentence for sentence in self._sentences(text)
            if any(marker in sentence.lower() for marker in self.RISK_MARKERS)
        ]

    def _extract_permissions(self, text: str) -> List[str]:
        return [
            sentence for sentence in self._sentences(text)
            if any(marker in sentence.lower() for marker in self.PERMISSION_MARKERS)
        ]

    def _extract_task_boundaries(self, text: str) -> List[str]:
        boundaries = []
        for sentence in self._sentences(text):
            lowered = sentence.lower()
            if any(x in lowered for x in ("only", "do not", "don't", "without", "within", "outside", "scope", "limit")):
                boundaries.append(sentence)
        return boundaries

    def _resolve_domains(self, text: str) -> List[str]:
        lowered = text.lower()
        domains = [
            domain for domain, markers in self.DOMAIN_MARKERS.items()
            if any(marker in lowered for marker in markers)
        ]
        return domains or ["general"]

    def _resolve_artifact_intent(self, text: str) -> str:
        lowered = text.lower()
        for marker, intent in self.ARTIFACT_MARKERS.items():
            if marker in lowered:
                return intent
        return ""

    def _resolve_execution_intent(self, text: str) -> str:
        lowered = text.lower()
        verbs = [marker for marker in self.EXECUTION_MARKERS if re.search(rf"\b{re.escape(marker)}\b", lowered)]
        return verbs[0] if verbs else ""

    def _resolve_output_intent(self, text: str) -> str:
        lowered = text.lower()
        if any(x in lowered for x in ("explain", "summarize", "describe", "answer")):
            return "informational"
        artifact = self._resolve_artifact_intent(text)
        if artifact:
            return f"artifact:{artifact}"
        if any(x in lowered for x in self.EXECUTION_MARKERS):
            return "execution"
        return ""

    def _extract_assumptions(self, text: str) -> List[str]:
        return [
            sentence for sentence in self._sentences(text)
            if any(x in sentence.lower() for x in ("assume", "assuming", "presume", "suppose"))
        ]

    # ------------------------------------------------------------------
    # Context, uncertainty, evidence, temporal, and delta processing
    # ------------------------------------------------------------------

    def _resolve_delta(self, prior: SemanticState, sentences: List[str]) -> SemanticDelta:
        if not prior.persistent_context:
            return SemanticDelta(added=list(sentences))

        prior_norm = {self._canonical(x): x for x in prior.persistent_context}
        added, changed, reaffirmed, superseded = [], [], [], []

        for sentence in sentences:
            key = self._canonical(sentence)
            lowered = sentence.lower()
            if key in prior_norm:
                reaffirmed.append(sentence)
            elif "no longer" in lowered or "instead" in lowered or "replaced" in lowered:
                superseded.append(sentence)
            elif any(marker in lowered for marker in self.CHANGE_MARKERS):
                changed.append(sentence)
            else:
                added.append(sentence)

        unresolved = self._partition_uncertainty(sentences)
        return SemanticDelta(
            added=added,
            changed=changed,
            reaffirmed=reaffirmed,
            superseded=superseded,
            unresolved=unresolved,
        )

    def _resolve_unknowns(self, text: str, prior: List[str]) -> List[str]:
        return self._stable_unique(prior + self._partition_uncertainty(self._sentences(text)))

    def _resolve_conflicts(self, text: str, prior: List[str]) -> List[str]:
        conflicts = list(prior)
        for sentence in self._sentences(text):
            if any(x in sentence.lower() for x in ("but", "however", "conflict", "contradict", "inconsistent", "despite")):
                conflicts.append(sentence)
        return self._stable_unique(conflicts)

    def _partition_evidence(self, items: List[str]) -> List[str]:
        return [item for item in items if any(marker in item.lower() for marker in self.EVIDENCE_MARKERS)]

    def _partition_uncertainty(self, items: List[str]) -> List[str]:
        return [item for item in items if any(marker in item.lower() for marker in self.UNCERTAINTY_MARKERS)]

    def _partition_temporal(self, items: List[str]) -> List[str]:
        return [item for item in items if any(marker in item.lower() for marker in self.TEMPORAL_MARKERS)]

    def _select_active_context(self, text: str, persistent: List[str]) -> List[str]:
        query_terms = set(re.findall(r"[a-z0-9]+", text.lower()))

        def score(item: str) -> tuple[int, int]:
            terms = set(re.findall(r"[a-z0-9]+", item.lower()))
            overlap = len(query_terms & terms)
            recency = persistent.index(item)
            return overlap, recency

        return sorted(persistent, key=score, reverse=True)[: self.max_active_context]

    # ------------------------------------------------------------------
    # Inference packet compilation
    # ------------------------------------------------------------------

    def _compile_handoff(self, state: SemanticState, delta: SemanticDelta) -> str:
        def lines(items: List[str], limit: int = 6) -> str:
            return "\n".join(f"- {x}" for x in items[-limit:]) or "- none"

        changes = delta.changed + delta.superseded + delta.added
        aliases = ", ".join(f"{a}→{c}" for a, c in state.aliases.items()) or "none"
        return (
            "TOKNZ INFERENCE PACKET\n\n"
            f"OBJECTIVE:\n{state.objective}\n\n"
            f"DOMAINS:\n{', '.join(state.domains) or 'general'}\n\n"
            f"INTENT:\nartifact={state.artifact_intent or 'none'}; "
            f"execution={state.execution_intent or 'none'}; output={state.output_intent or 'none'}\n\n"
            f"ALIASES:\n{aliases}\n\n"
            f"CONSTRAINTS:\n{lines(state.constraints)}\n\n"
            f"RISKS:\n{lines(state.risks)}\n\n"
            f"PERMISSIONS / BOUNDARIES:\n{lines(state.permissions + state.task_boundaries)}\n\n"
            f"CURRENT DELTA:\n{lines(changes)}\n\n"
            f"ACTIVE CONTEXT:\n{lines(state.active_context, 10)}\n\n"
            f"UNKNOWNS / UNCERTAINTY:\n{lines(state.unknowns + state.uncertainty_context)}\n\n"
            f"CONFLICTS:\n{lines(state.conflicts)}\n\n"
            "INFERENCE CONTRACT:\n"
            "Continue from the canonical TOKNZ semantic state. Preserve objective, constraints, "
            "relationships, permissions, boundaries, unknowns, conflicts, and temporal changes. "
            "Do not reconstruct irrelevant history unless required by the active objective."
        )

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _merge_aliases(existing: Dict[str, str], incoming: Dict[str, str]) -> Dict[str, str]:
        result = dict(existing)
        result.update(incoming)
        return result

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
