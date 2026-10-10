"""
IBM Qiskit Fall Fest 2026 - Challenge 1: Predict the Output
-----------------------------------------------------------
Problem Statement - A quantum circuit can produce different measurement outcomes depending on the 
gates applied to a qubit. 
Your task is to predict the output of simple quantum circuits before executing them and then compare your 
prediction with the actual measurement results. 
 
Your Task - Using Qiskit: 
1. Create a single-qubit quantum circuit. 
2. Prepare the qubit in the initial state |0⟩. 
3. Construct and investigate the following circuits: 
a. Circuit A: Apply an X gate and measure. 
b. Circuit B: Apply two X gates and measure. 
c. Circuit C: Apply an H gate and measure. 
4. Before executing each circuit, predict the expected measurement outcome. 
5. Execute each circuit for 100 shots. 
6. Record the measurement results. 
7. Compare your predictions with the actual results. 
8. Display the results using a histogram. 
 
Think Before You Run - Before executing the circuits, predict: What will happen after applying one X 
gate? What will happen after applying two X gates? What do you expect after applying an H gate? Will 
Circuit C always produce the same measurement result? 
 
Design Constraints - Your circuit must: 
• Use exactly 1 qubit. 
• Include measurement. 
• Use only the gates introduced in the workshop. 
• Be created and executed using Qiskit. 
• Use 100 shots for each experiment. 
 
Submission - Your notebook must include: 
• The three quantum circuits. 
• Your prediction for each circuit. 
• Measurement results for 100 shots. 
• Histograms of the results. 
• A short comparison between your predictions and the actual results. 

Install:  pip install qiskit qiskit-aer matplotlib
Run:      python challenge_1.py
"""

import matplotlib
matplotlib.use("Agg")  # works without a display; remove if you want a pop-up window
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

SHOTS = 100


def build_circuits():
    """Create the three 1-qubit circuits (qubit starts in |0>)."""
    # Circuit A: X gate -> |1>
    qc_a = QuantumCircuit(1, 1, name="Circuit A (X)")
    qc_a.x(0)
    qc_a.measure(0, 0)

    # Circuit B: X then X -> back to |0>
    qc_b = QuantumCircuit(1, 1, name="Circuit B (X, X)")
    qc_b.x(0)
    qc_b.x(0)
    qc_b.measure(0, 0)

    # Circuit C: H gate -> equal superposition (|0> + |1>)/sqrt(2)
    qc_c = QuantumCircuit(1, 1, name="Circuit C (H)")
    qc_c.h(0)
    qc_c.measure(0, 0)

    return {"A": qc_a, "B": qc_b, "C": qc_c}


# Predictions made BEFORE running the circuits
PREDICTIONS = {
    "A": "X flips |0> to |1>, so every shot should give '1' (100% '1').",
    "B": "The second X flips the qubit back (X*X = I), so every shot should give '0' (100% '0').",
    "C": "H creates an equal superposition, so about 50% '0' and 50% '1'. "
         "Results are random, so it will NOT give the same result every time "
         "(expect something like 45-55 for each, not exactly 50/50).",
}


def main():
    circuits = build_circuits()
    simulator = AerSimulator()

    all_counts = {}

    for key, qc in circuits.items():
        print("=" * 60)
        print(qc.name)
        print(qc.draw(output="text"))
        print("Prediction:", PREDICTIONS[key])

        # Run for 100 shots
        job = simulator.run(qc, shots=SHOTS)
        counts = job.result().get_counts()
        all_counts[key] = counts
        print("Measured counts (100 shots):", dict(counts))

    # ---- Histograms ----
    for key, counts in all_counts.items():
        fig = plot_histogram(counts, title=circuits[key].name)
        fig.savefig(f"histogram_circuit_{key}.png", bbox_inches="tight")
        plt.close(fig)

    # Combined histogram
    fig = plot_histogram(
        list(all_counts.values()),
        legend=[circuits[k].name for k in all_counts],
        title="Challenge 1: All circuits (100 shots each)",
    )
    fig.savefig("histogram_all_circuits.png", bbox_inches="tight")
    plt.close(fig)
    print("\nSaved histograms: histogram_circuit_A/B/C.png and histogram_all_circuits.png")

    # ---- Prediction vs. actual ----
    print("\n" + "=" * 60)
    print("COMPARISON: PREDICTION vs ACTUAL")
    print("=" * 60)
    c = all_counts
    print(f"Circuit A: predicted all '1'        -> actual {dict(c['A'])}")
    print(f"Circuit B: predicted all '0'        -> actual {dict(c['B'])}")
    print(f"Circuit C: predicted ~50/50 random  -> actual {dict(c['C'])}")

    print(
        "\nConclusion:\n"
        "- A: One X gate flips |0> to |1>, so the result was deterministic: always 1.\n"
        "- B: Two X gates cancel out (X*X = identity), so the qubit returned to |0>: always 0.\n"
        "- C: The H gate puts the qubit in superposition, so measurement is probabilistic. "
        "Counts were close to 50/50 but not exactly equal, and they change from run to run. "
        "So Circuit C does NOT always give the same result, unlike A and B."
    )


if __name__ == "__main__":
    main()