from toknz import ToknzEngine


engine = ToknzEngine()

turns = [
    "Plan a safe six-hour grid stabilization response. Two substations are offline and diesel delivery is delayed.",
    "One substation is now back online, but load is still rising.",
    "Water pressure is dropping in two zones, but the cause is unclear?",
]

for index, turn in enumerate(turns, start=1):
    packet = engine.process(turn)
    print(f"\nTURN {index}")
    print("Objective:", packet.state.objective)
    print("Added:", packet.delta.added)
    print("Changed:", packet.delta.changed)
    print("Constraints:", packet.state.constraints)
    print("Active context:", packet.context)
    print("\nHandoff:\n", packet.handoff)
