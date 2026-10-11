"""
IBM Qiskit Fall Fest 2026 - Challenge 2: Make the Quantum Coin Biased
---------------------------------------------------------------------
Idea: a Hadamard gives a fair coin (50/50). To bias it we rotate the qubit
only PART of the way from |0> to |1> using an RY(theta) gate:

    RY(theta)|0> = cos(theta/2)|0> + sin(theta/2)|1>
    P(0) = cos^2(theta/2),   P(1) = sin^2(theta/2)

Install:  pip install qiskit qiskit-aer matplotlib pylatexenc
Run:      python challenge_2.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # remove this line to get pop-up windows instead of saved PNGs
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

SHOTS = 100
sim = AerSimulator()


def run(qc):
    return dict(sim.run(qc, shots=SHOTS).result().get_counts())


def predict(theta):
    p0 = float(np.cos(theta / 2) ** 2)
    return p0, 1 - p0


# ---------------------------------------------------------------
# Main circuits (each uses exactly 1 qubit and only 1-3 gates)
# ---------------------------------------------------------------

# Circuit 1 (0 more likely): RY(pi/3)  ->  P(0)=75%, P(1)=25%
theta1 = np.pi / 3
qc1 = QuantumCircuit(1, 1, name="Circuit 1: RY(pi/3)")
qc1.ry(theta1, 0)
qc1.measure(0, 0)

# Circuit 2 (1 more likely): RY(2pi/3) ->  P(0)=25%, P(1)=75%
theta2 = 2 * np.pi / 3
qc2 = QuantumCircuit(1, 1, name="Circuit 2: RY(2pi/3)")
qc2.ry(theta2, 0)
qc2.measure(0, 0)

# Circuit 3 (workshop-gates-only alternative): H, T, H
# H -> T adds a phase -> H converts that phase into a probability difference
# P(0) = cos^2(pi/8) ~ 85.4%, P(1) ~ 14.6%
qc3 = QuantumCircuit(1, 1, name="Circuit 3: H-T-H")
qc3.h(0)
qc3.t(0)
qc3.h(0)
qc3.measure(0, 0)

circuits = [
    (qc1, predict(theta1)),
    (qc2, predict(theta2)),
    (qc3, (float(np.cos(np.pi / 8) ** 2), float(np.sin(np.pi / 8) ** 2))),
]

all_counts = []
print("=" * 64)
for qc, (p0, p1) in circuits:
    print(qc.name)
    print(qc.draw(output="text"))
    print(f"Prediction: P(0) = {p0:.1%}, P(1) = {p1:.1%}")
    counts = run(qc)
    all_counts.append(counts)
    print(f"Measured (100 shots): {counts}")
    print(f"  -> 0: {counts.get('0', 0)}%   1: {counts.get('1', 0)}%")
    fig = plot_histogram(counts, title=qc.name)
    fig.savefig(f"histogram_{qc.name.split(':')[0].replace(' ', '_').lower()}.png",
                bbox_inches="tight")
    plt.close(fig)
    print("=" * 64)

# Bonus: compare the "0-biased" and "1-biased" circuits side by side
fig = plot_histogram(
    all_counts[:2],
    legend=["0 favoured: RY(pi/3)", "1 favoured: RY(2pi/3)"],
    title="Bonus: opposite biases (100 shots)",
)
fig.savefig("histogram_bonus_comparison.png", bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------
# Different degrees of bias: sweep theta
# ---------------------------------------------------------------
print("\nDEGREES OF BIAS (single RY gate)")
print(f"{'theta':>10} | {'pred P(0)':>9} | {'meas 0':>6} | {'meas 1':>6}")
sweep_counts, sweep_labels = [], []
for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:  # theta = frac * pi
    theta = frac * np.pi
    qc = QuantumCircuit(1, 1)
    qc.ry(theta, 0)
    qc.measure(0, 0)
    counts = run(qc)
    sweep_counts.append(counts)
    sweep_labels.append(f"theta={frac:g}pi")
    print(f"{frac:>8g}pi | {predict(theta)[0]:>9.1%} | "
          f"{counts.get('0', 0):>6} | {counts.get('1', 0):>6}")

fig = plot_histogram(sweep_counts, legend=sweep_labels,
                     title="Degrees of bias: RY(theta) sweep", figsize=(11, 6))
fig.savefig("histogram_bias_sweep.png", bbox_inches="tight")
plt.close(fig)

print("\nSaved histograms as PNG files in the current folder.")

# ---------------------------------------------------------------
# Explanation + Challenge Question (put this in the LAST notebook cell)
# ---------------------------------------------------------------
EXPLANATION = """
Explanation:
The Hadamard gate transforms the initial state |0⟩ into an equal superposition of 
|0⟩ and |1⟩, giving each outcome a 50% measurement probability. The RY(θ) rotation gate
changes the amplitudes of these states according to cos(θ/2) and sin(θ/2), respectively.
Since measurement probabilities are the squares of the amplitudes, changing θ changes
the probability of obtaining 0 or 1. Phase gates such as T can also influence 
measurement probabilities when combined with other gates, such as the Hadamard gate,
through quantum interference.


Challenge Question: How can quantum gates change the probability of obtaining
0 or 1 when a qubit is measured?
Answer: A qubit's state is a combination of |0> and |1> with amplitudes, and
the measurement probability of each outcome is the square of its amplitude.
Quantum gates are rotations that change those amplitudes. Gates like X flip
them completely (0 <-> 1), H spreads them equally (50/50), and rotation gates
such as RY(theta) set any split we want. Phase gates (S, T) don't change the
probabilities by themselves, but combined with H they change how amplitudes
interfere, which also shifts the probabilities. So by choosing which gates
and angles to apply before measuring, we control the chance of seeing 0 or 1.
"""
print(EXPLANATION)