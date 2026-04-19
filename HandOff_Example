Toknz HandOff Report (HO) — Public Version
Pre-Reasoning Output → Reasoning Layer Input

🧠 0. System Overview
Toknz is a pre-reasoning layer that prepares complex inputs for downstream reasoning systems.
This report represents the structured problem state after preprocessing and before answer generation.
Toknz does not generate answers.
It defines the problem space, constraints, and viable solution directions.

🎯 1. Active Request State
A normalized representation of the user’s request and its context.
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

🌐 2. Candidate Concept Space
Initial concepts and directions extracted from the input.
candidate_space:
  total_candidates: {{count}}

  concepts:
    - {{concept_1}}
    - {{concept_2}}
    - {{concept_3}}

🧩 3. Filtered Problem Structure
Concepts retained after relevance filtering and constraint alignment.
filtered_structure:
  retained_concepts: {{count}}

  concepts:
    - id: {{concept_id}}
      label: "{{concept}}"
      category: {{goal | constraint | action | risk}}
      relevance: {{0.0–1.0}}

🔗 4. Relationships & Dependencies
Key relationships between retained concepts.
relationships:
  - source: {{concept_A}}
    target: {{concept_B}}
    type: {{dependency | overlap | constraint | association}}
    strength: {{0.0–1.0}}

⚔️ 5. Trade-Offs & Constraints
Real-world tensions that impact decision-making.
tradeoffs:
  - elements: [{{A}}, {{B}}]
    type: "{{tradeoff_type}}"
    description: "{{description}}"
    impact_level: {{low | medium | high}}

constraints:
  - {{constraint_1}}
  - {{constraint_2}}

💡 6. Candidate Solution Paths
Structured hypotheses or solution directions derived from the filtered problem.
solution_paths:
  - id: {{path_id}}
    description: "{{approach}}"
    related_concepts: [{{concept_ids}}]
    confidence: {{0.0–1.0}}

📊 7. Feasibility Assessment
High-level evaluation of each solution path.
evaluation:
  - solution: "{{approach}}"
    feasibility: {{low | medium | high}}
    cost_impact: {{low | medium | high}}
    timeline: {{short | medium | long}}
    overall_rank: {{1..n}}

🧠 8. Key Insights
Important structural observations about the problem.
{{insight_1}}
{{insight_2}}
{{insight_3}}

🎯 9. Completion Criteria
Conditions a valid final answer should satisfy.
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

📦 10. Reasoning Layer Instructions
Guidance for downstream model or agent.
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

📏 11. Efficiency Metrics (Optional)
metrics:
  concept_reduction_ratio: {{value}}
  retained_concepts: {{count}}
  initial_concepts: {{count}}

  expected_impact:
    - reduced repetition
    - improved first-pass accuracy
    - lower total token usage in multi-turn scenarios
