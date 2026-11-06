# Rising Tide 003B

Start with **RISING-TIDE-003B-REPORT.md**.

This packet contains the corrected finite strict-expansion argument, a fresh-binary comparison on the original fixed graph, and an exact changing-graph experiment using integer midpoint-support counts.

Run with Python 3.10 or newer:

```sh
python3 experiment.py
```

Only the Python standard library is required. The command regenerates results.json in this folder. It runs the original 128 matrix comparisons, six restricted frontier transitions, 4,608 exhaustive graph-edit cases, and 529 dynamic query instances checked separately for three methods.

- **experiment.py:** final implementation and fixed fixtures.
- **results.json:** final measured work ledgers, complete graph versions and queries, edit traces, checks, and source hash.
- **PROTOCOL.md:** assumptions, cost definitions, predetermined choices, and disclosed changes after the pilot.
- **RISING-TIDE-003B-REPORT.md:** conclusions, proofs, comparison tables, counterexample, limitations, and references.
- **development/pilot_experiment.py** and **development/pilot_results.json:** preserved pilot, using the earlier bookkeeping. Do not combine its numbers with the final measurements.
- **SHA256SUMS.txt:** hashes of packet members other than itself.

The counters are declared work-event counts, not timings. The original handoff was read and independently reimplemented; its original executable is not part of this packet. No original user files were modified.
