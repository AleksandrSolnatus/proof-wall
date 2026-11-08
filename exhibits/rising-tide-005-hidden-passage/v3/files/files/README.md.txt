# MATH / RISING TIDE 005 — The Hidden Passage

**Executed 7 November 2026. Finite experiment, not a proposal.**

This joins a mathematically genuine four-coordinate routing world with moving a
fixed obstacle off the travel plane, adjacency without direct entry, the
observability of W, and computation that naturally leaves reusable work.

## Reproduce

```bash
python3 experiment.py
```

Requires Python 3.10+ standard library only. Creates deterministic `results.json`,
`wall_sweep.csv`, `adjacency_sweep.csv`, `query_ledger.csv`. Outputs are overwritten
on replay; use a disposable copy if preserving archived bytes. No network or
installation is involved. The program prints exact test counts and an approximate
elapsed runtime; elapsed runtime is omitted from canonical JSON for byte-for-byte replay.

## Files

- `PROOF.md` — exact mathematical statements, proof arguments, counterexamples.
- `REPORT.md` — data, what happened, unresolved questions, interpretations.
- `experiment.py` — complete runnable source, algorithm, controls and test oracles.
- `results.json` — structured results.
- `wall_sweep.csv` — sixteen closed-form-versus-computed routes.
- `adjacency_sweep.csv` — sixty distinct hypothetical resource cases.
- `query_ledger.csv` — 560 real routing questions with cumulative work counters.
- `run_receipt.txt` — successful recorded run.
- `MANIFEST.sha256` — byte hashes of included files.

Built on our Traffic Puddle 001 / 002 and adjacency notes, earlier W-pressure
work, and Rising Tide 003B. The earlier experiments were not retested or
replaced. This packet is not published to Proof Wall or Carryforward, and was
not automatically placed into Toy Bin.

**What the work does not claim:** physical 4D, a real traffic capacity result,
actual knowledge transfer, or a new general P-vs-NP breakthrough.
