```markdown
# TOKNZ Hand-Off Report (HO) — Public Reference Format

**Pre-Reasoning Output → Reasoning Layer Input**

🧠 **0. System Overview**  
TOKNZ is a pre-reasoning layer that prepares complex, multi-turn inputs for downstream reasoning systems (LLMs or agents).  
This report represents the **structured problem state** after deterministic preprocessing and before answer generation.  

TOKNZ does **not** generate answers. It defines the problem space, constraints, relationships, and viable solution directions so the reasoning layer operates inside a stable, bounded system state.

---

🎯 **1. Active Request State**  
A normalized representation of the user’s request and its context.

```yaml
active_state:
  request_summary: "{{summarized_request}}"
  objective_type: "{{plan | explanation | roadmap | decision | design}}"

  domains:
    - {{domain_1}}
    - {{domain_2}}

  key_constraints:
    - {{constraint_1}}
    - {{constraint_2}}

  relevant_context:
    - {{context_signal_1}}
    - {{context_signal_2}}

  confidence: {{0.0–1.0}}
```

---

🌐 **2. Candidate Concept Space**  
Initial concepts and directions extracted from the input.

```yaml
candidate_space:
  total_candidates: {{count}}

  concepts:
    - {{concept_1}}
    - {{concept_2}}
    - {{concept_3}}
```

---

🧩 **3. Filtered Problem Structure**  
Concepts retained after relevance filtering and constraint alignment.

```yaml
filtered_structure:
  retained_concepts: {{count}}

  concepts:
    - id: {{concept_id}}
      label: "{{concept}}"
      category: {{goal | constraint | action | risk}}
      relevance: {{0.0–1.0}}
```

---

🔗 **4. Relationships & Dependencies**  
Key relationships between retained concepts.

```yaml
relationships:
  - source: {{concept_A}}
    target: {{concept_B}}
    type: {{dependency | overlap | constraint | association}}
    strength: {{0.0–1.0}}
```

---

⚔️ **5. Trade-Offs & Constraints**  
Real-world tensions that impact decision-making.

```yaml
tradeoffs:
  - elements: [{{A}}, {{B}}]
    type: "{{tradeoff_type}}"
    description: "{{description}}"
    impact_level: {{low | medium | high}}

constraints:
  - {{constraint_1}}
  - {{constraint_2}}
```

---

💡 **6. Candidate Solution Paths**  
Structured hypotheses or solution directions derived from the filtered problem.

```yaml
solution_paths:
  - id: {{path_id}}
    description: "{{approach}}"
    related_concepts: [{{concept_ids}}]
    confidence: {{0.0–1.0}}
```

---

📊 **7. Feasibility Assessment**  
High-level evaluation of each solution path.

```yaml
evaluation:
  - solution: "{{approach}}"
    feasibility: {{low | medium | high}}
    cost_impact: {{low | medium | high}}
    timeline: {{short | medium | long}}
    overall_rank: {{1..n}}
```

---

🧠 **8. Key Insights**  
Important structural observations about the problem.

{{insight_1}}  
{{insight_2}}  
{{insight_3}}

---

🎯 **9. Completion Criteria**  
Conditions a valid final answer should satisfy.

```yaml
completion_requirements:
  must:
    - address core objective
    - respect constraints
    - account for trade-offs
    - produce actionable output

  should_not:
    - introduce unrelated domains
    - ignore constraints
    - provide non-executable recommendations
```

---

📦 **10. Reasoning Layer Instructions**  
Guidance for downstream model or agent.

```yaml
handoff_instructions:
  focus:
    - highest-ranked solution paths
    - critical constraints
    - key trade-offs

  approach:
    - avoid reinterpreting the problem
    - build directly on structured inputs
    - prioritize clarity and execution

  output_style:
    - concise
    - structured
    - decision-oriented
```

---

📏 **11. Efficiency Metrics (Optional)**

```yaml
metrics:
  concept_reduction_ratio: {{value}}
  retained_concepts: {{count}}
  initial_concepts: {{count}}

  expected_impact:
    - reduced repetition
    - improved first-pass accuracy
    - lower total token usage in multi-turn scenarios
```

---

## Concrete Example: Turn 1 QI Demo (Redacted)

**Active Request State**  
```yaml
active_state:
  request_summary: "Build a Quality Improvement (QI) project proposal focused on improving patient education interpretability and discharge understanding at REDACTED NETWORK Health"
  objective_type: "design"
  domains:
    - Quality Improvement
    - Patient Education
    - Health Literacy
    - Discharge Planning
  key_constraints:
    - Redact all network names to ***REDACTED NETWORK***
    - Target 6th-grade reading level with conversational tone
    - Use only approved sources (Elsevier ClinicalKey, UpToDate)
    - No clinical decision-making or new medical advice
    - Policy-compliant formatting (≤20 words/sentence, active voice, etc.)
  relevant_context:
    - PDSA framework required
    - Patient satisfaction and safer transitions are primary goals
  confidence: 0.95
```

**Filtered Problem Structure** (excerpt)  
- id: `patient_understanding` → category: `goal` → relevance: 1.0  
- id: `health_literacy_policy` → category: `constraint` → relevance: 1.0  
- id: `discharge_education` → category: `action` → relevance: 0.98  

**Key Insights**  
1. This is a communication/interpretability gap, not a clinical-care gap.  
2. All outputs must remain education-only and route through Patient Education Specialist review.  
3. The system state must preserve redaction and policy rules as immutable invariants.

**Reasoning Layer Instructions** (excerpt)  
- Focus on building the cleaned, redacted QI document structure.  
- Do not re-explain the background on every future turn — treat this as the persistent system state.  
- Maintain exact redaction rules and health-literacy constraints across all subsequent turns.

---

## How to Use This Hand-Off (Example)

```python
# Example Python wrapper (public reference)
from tok.nz import StateManager  # or your own integration

# Your closed TOKNZ engine produces the handoff
handoff = tok.nz.generate_hand_off(chat_history)   # proprietary engine

# Downstream LLM receives a clean, bounded prompt
prompt = f"""You are now reasoning inside this pre-processed problem state:

{handoff.render_markdown()}

Follow the handoff instructions exactly. Do not reinterpret the request or re-explain the background."""
```

---

**This is the public reference format.**  
It demonstrates the exact interface between TOKNZ’s pre-reasoning layer and any downstream reasoning system.  

**Production TOKNZ** (full constraint engine, versioned state, enterprise security, audit logs, and multi-LLM routing) is available via OOI Institute licensing.

See the full 4-turn QI demo in action: [4_TURN_DEMO.pdf](https://github.com/OOI-Institute/TOKNZ/blob/main/4_TURN_DEMO.pdf)
```
