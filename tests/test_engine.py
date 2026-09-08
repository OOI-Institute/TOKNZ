from toknz import ToknzEngine


def test_state_persists_and_delta_changes():
    engine = ToknzEngine()
    first = engine.process(
        "Plan a safe grid stabilization response. Two substations are offline and diesel delivery is delayed."
    )
    second = engine.process(
        "One substation is now back online, but load is still rising."
    )

    assert first.state.objective
    assert "safety-sensitive" in second.state.constraints
    assert second.delta.changed
    assert any("back online" in item.lower() for item in second.delta.changed)
    assert any("substation" in item.lower() for item in second.state.persistent_context)


def test_psa_capabilities_are_native_toknz_state():
    engine = ToknzEngine()
    packet = engine.process(
        "Build a safety report for GridCore aka GC. GridCore depends on Substation-A. "
        "Only operators may execute changes. Sensor data shows outage risk, but the cause is unclear?"
    )

    state = packet.state
    assert state.entities
    assert state.aliases
    assert state.relationships
    assert state.dependencies
    assert state.constraints
    assert state.risks
    assert state.permissions or state.task_boundaries
    assert state.domains
    assert state.artifact_intent == "report"
    assert state.execution_intent
    assert state.output_intent
    assert state.unknowns
    assert state.conflicts
    assert state.evidence_context
    assert state.uncertainty_context


def test_retrieved_context_is_persistent_but_bounded_for_inference():
    engine = ToknzEngine(max_active_context=2)
    packet = engine.process(
        "Assess the current incident risk.",
        retrieved_context=[
            "Maintenance record: substation A failed last winter.",
            "Policy: load shedding requires operator approval.",
            "Weather: ambient temperature is falling.",
        ],
    )

    assert len(packet.context) == 2
    assert len(packet.state.persistent_context) >= 3
    assert any("retrieved" in source for source in packet.state.provenance.values())
    assert packet.state.evidence_context


def test_unknowns_conflicts_and_temporal_context_are_preserved():
    engine = ToknzEngine()
    packet = engine.process(
        "Pressure is reported stable, but sensor B reports an inconsistent drop now. The cause is unclear?"
    )

    assert packet.state.conflicts
    assert packet.state.unknowns
    assert packet.state.temporal_context
    assert "CONFLICTS" in packet.handoff
    assert "UNKNOWNS" in packet.handoff


def test_superseded_delta_is_explicit():
    engine = ToknzEngine()
    engine.process("Use Route A for the workflow.")
    packet = engine.process("Use Route B instead; Route A is no longer active.")
    assert packet.delta.superseded


def test_empty_input_rejected():
    engine = ToknzEngine()
    try:
        engine.process("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("empty input should raise ValueError")
