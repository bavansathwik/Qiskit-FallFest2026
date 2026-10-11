"""
IBM Qiskit Fall Fest 2026 - Challenge 4: Quantum Correlation Switch
-------------------------------------------------------------------
Part A (correlated)  : H(q0) -> CX(q0,q1)          => (|00> + |11>)/sqrt(2)
Part B (opposite)    : H(q0) -> CX(q0,q1) -> X(q1) => (|01> + |10>)/sqrt(2)

The X gate on qubit 1 is the "switch": without it the qubits agree,
with it they disagree. Only gates from the workshop are used: H, CX, X.

Install:  pip install qiskit qiskit-aer matplotlib pylatexenc
Run:      python challenge_4.py
"""

import matplotlib
matplotlib.use("Agg")  # remove this line to get pop-up windows instead of saved PNGs
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

SHOTS = 100
sim = AerSimulator()


def correlation_circuit(opposite: bool) -> QuantumCircuit:
    """Build the 2-qubit circuit. opposite=False -> Part A, True -> Part B."""
    name = "Part B: opposite (01/10)" if opposite else "Part A: correlated (00/11)"
    qc = QuantumCircuit(2, 2, name=name)
    qc.h(0)             # gate 1: superposition on qubit 0
    qc.cx(0, 1)         # gate 2: entangle -> Bell state
    if opposite:
        qc.x(1)         # gate 3: the switch, flips qubit 1
    qc.measure([0, 1], [0, 1])
    return qc


qc_a = correlation_circuit(opposite=False)   # 2 gates before measurement
qc_b = correlation_circuit(opposite=True)    # 3 gates before measurement

PREDICTIONS = {
    qc_a.name: "Only 00 and 11 appear, ~50% each. 01 and 10 should NOT appear "
               "(so not all four outcomes show up).",
    qc_b.name: "Only 01 and 10 appear, ~50% each. 00 and 11 should NOT appear "
               "(so not all four outcomes show up).",
}

# ---------------- Run ----------------
results = {}
for qc in (qc_a, qc_b):
    print("=" * 66)
    print(qc.name)
    print(qc.draw(output="text"))
    print("Prediction:", PREDICTIONS[qc.name])
    counts = dict(sim.run(qc, shots=SHOTS).result().get_counts())
    results[qc.name] = counts
    print(f"Measured counts (100 shots): {counts}")

# ---------------- Histograms ----------------
for tag, qc in (("A", qc_a), ("B", qc_b)):
    fig = plot_histogram(results[qc.name], title=qc.name)
    fig.savefig(f"histogram_part_{tag}.png", bbox_inches="tight")
    plt.close(fig)

fig = plot_histogram(
    list(results.values()),
    legend=["Part A: correlated", "Part B: opposite"],
    title="Challenge 4: Quantum Correlation Switch (100 shots each)",
)
fig.savefig("histogram_comparison.png", bbox_inches="tight")
plt.close(fig)
print("\nSaved: histogram_part_A.png, histogram_part_B.png, histogram_comparison.png")

# ---------------- Comparison ----------------
a, b = results[qc_a.name], results[qc_b.name]
print("\n" + "=" * 66)
print("COMPARISON")
print("=" * 66)
print(f"Part A: 00={a.get('00', 0)}, 11={a.get('11', 0)}, 01={a.get('01', 0)}, 10={a.get('10', 0)}")
print(f"Part B: 00={b.get('00', 0)}, 11={b.get('11', 0)}, 01={b.get('01', 0)}, 10={b.get('10', 0)}")

print("""
Explanation:
- Dominant outcomes in Part A: 00 and 11 (about 50% each). The qubits always agree.
- Dominant outcomes in Part B: 01 and 10 (about 50% each). The qubits always differ.
- What changed: the only difference is one extra X gate on qubit 1, placed after
  the CNOT and before measurement.
- Why the relationship changed: H puts qubit 0 in superposition and CX entangles
  the qubits, giving the Bell state (|00> + |11>)/sqrt(2); measuring one qubit
  fixes the other to the same value. The X gate flips every qubit-1 value
  (|00> -> |01>, |11> -> |10>), turning the state into (|01> + |10>)/sqrt(2).
  The entanglement is untouched, but 'equal' becomes 'opposite'.
- Not all four outcomes appear: entanglement allows only two of the four
  results in each circuit, so the other two have (ideally) zero probability.
  Each qubit alone is still random, but the pair is perfectly correlated.
  Counts are not exactly 50/50 because 100 shots is a small random sample.

Note: Qiskit prints bits as q1 q0, so '01' means q1=0, q0=1.
""")