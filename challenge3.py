"""
IBM Qiskit Fall Fest 2026 - Challenge 3: Can you change the correlation?
------------------------------------------------------------------------
Original circuit : Bell state  H(q0) -> CX(q0, q1)   => (|00> + |11>)/sqrt(2)
Modified circuit : add ONE X gate on q1 after the CX => (|01> + |10>)/sqrt(2)

Install:  pip install qiskit qiskit-aer matplotlib pylatexenc
Run:      python challenge_3.py
"""

import matplotlib
matplotlib.use("Agg")  # remove this line to get pop-up windows instead of saved PNGs
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

SHOTS = 100
sim = AerSimulator()

# ---------------- Original circuit: Bell state ----------------
qc_orig = QuantumCircuit(2, 2, name="Original Bell circuit")
qc_orig.h(0)          # superposition on qubit 0
qc_orig.cx(0, 1)      # entangle qubit 1 with qubit 0
qc_orig.measure([0, 1], [0, 1])

# ---------------- Modified circuit: one extra X gate ----------------
qc_mod = QuantumCircuit(2, 2, name="Modified circuit (extra X on q1)")
qc_mod.h(0)
qc_mod.cx(0, 1)
qc_mod.x(1)           # <-- the single added gate: flips qubit 1
qc_mod.measure([0, 1], [0, 1])

# ---------------- Predictions (made before running) ----------------
PRED_ORIG = ("Only 00 and 11 appear, each about 50%. The qubits always "
             "agree; 01 and 10 should never appear.")
PRED_MOD = ("The X gate flips qubit 1, so the outcomes become 01 and 10, "
            "each about 50%. The qubits now always DISAGREE; 00 and 11 "
            "should never appear.")

# ---------------- Run ----------------
results = {}
for qc, pred in [(qc_orig, PRED_ORIG), (qc_mod, PRED_MOD)]:
    print("=" * 66)
    print(qc.name)
    print(qc.draw(output="text"))
    print("Prediction:", pred)
    counts = dict(sim.run(qc, shots=SHOTS).result().get_counts())
    results[qc.name] = counts
    print(f"Measured counts (100 shots): {counts}")

# ---------------- Histograms ----------------
for tag, qc in [("original", qc_orig), ("modified", qc_mod)]:
    fig = plot_histogram(results[qc.name], title=qc.name)
    fig.savefig(f"histogram_{tag}.png", bbox_inches="tight")
    plt.close(fig)

fig = plot_histogram(
    list(results.values()),
    legend=["Original (Bell)", "Modified (+X on q1)"],
    title="Challenge 3: original vs modified (100 shots each)",
)
fig.savefig("histogram_comparison.png", bbox_inches="tight")
plt.close(fig)
print("\nSaved: histogram_original.png, histogram_modified.png, histogram_comparison.png")

# ---------------- Comparison ----------------
o, m = results[qc_orig.name], results[qc_mod.name]
print("\n" + "=" * 66)
print("COMPARISON")
print("=" * 66)
print(f"Original : 00={o.get('00', 0)}, 11={o.get('11', 0)}, "
      f"01={o.get('01', 0)}, 10={o.get('10', 0)}")
print(f"Modified : 00={m.get('00', 0)}, 11={m.get('11', 0)}, "
      f"01={m.get('01', 0)}, 10={m.get('10', 0)}")

print("""
Explanation:
The original circuit makes the Bell state (|00> + |11>)/sqrt(2). The H gate puts
qubit 0 in superposition and the CNOT entangles qubit 1 with it, so the two
qubits always give the SAME result (00 or 11, roughly 50/50 each).

Adding a single X gate on qubit 1 after the CNOT flips that qubit's outcome:
|00> -> |01> and |11> -> |10>. The state becomes (|01> + |10>)/sqrt(2). The qubits
are still perfectly correlated and still entangled, but the correlation is now
OPPOSITE: they always give DIFFERENT results (01 or 10, roughly 50/50 each).
Each individual qubit is still random, but their relationship changed from
'always equal' to 'always opposite'. The prediction matched the result.
(Counts are not exactly 50/50 because of the random nature of 100 shots.)

Note: Qiskit prints bits as q1 q0, so '01' means q1=0, q0=1.
""")