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


def test_unknowns_and_conflicts_are_preserved():
    engine = ToknzEngine()
    packet = engine.process(
        "Pressure is reported stable, but sensor B reports an inconsistent drop. The cause is unclear?"
    )

    assert packet.state.conflicts
    assert packet.state.unknowns
    assert "CONFLICTS" in packet.handoff
    assert "UNKNOWNS" in packet.handoff


def test_empty_input_rejected():
    engine = ToknzEngine()
    try:
        engine.process("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("empty input should raise ValueError")
