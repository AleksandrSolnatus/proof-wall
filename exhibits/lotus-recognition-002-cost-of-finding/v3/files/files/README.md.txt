# LOTUS — Recognition 002

Private experimental continuation. Start with `LOTUS-RECOGNITION-002-REPORT.md`.
No network, dependencies, installation, repository writes, deployment or merge.
Requires Node.js (tested 24.22.1) and Python 3 (tested 3.12.14).

The original v1 protocol was frozen before results. `AMENDMENT-001.md` explains
the separate stricter old-parent control. Sources and historical baseline bytes
remain unchanged. No universal speedup or claim about P versus NP is made.

## Reproduce

Run from this directory. Write new outputs to new directories to keep receipts.

```sh
node baseline/research/rising-tide-001/space/test_demo.mjs
node test_recognizer.mjs
node run.mjs /tmp/lotus-recognition-main
python3 audit.py /tmp/lotus-recognition-main
node run_strict.mjs /tmp/lotus-recognition-strict
python3 audit.py /tmp/lotus-recognition-strict
node replay_saved.mjs results/runs
node replay_saved.mjs results/strict-runs
python3 verify_packet.py
```

`run_strict.mjs` deliberately enumerates possible misleading fixtures and may
take several minutes. This generator overhead is outside service work. The
saved-input replay avoids repeating generation and fully reruns the learners.
`python3 analyze.py` reconstructs `results/analysis.json` and `comparisons.csv`
from the included receipts and independently checks unique strict parents.

Each compressed receipt contains raw ordered problems, separately labeled
generator metadata, all four policy traces with certificates and cumulative
cost categories, retained-inverse snapshots, and discovered parent/edit edges.
Generator metadata is never passed to the learner. The baseline is a source
snapshot, not a replacement for or audit of the original five-archive packet.

## Preserved evidence

- `BASELINE_SOURCE.json`: PR and exact Git blob provenance.
- `baseline/`: unmodified baseline solver, tests and mathematical limitations.
- `PROTOCOL.md`: policies, grid, cost model and exclusions.
- `results/runs/`: 540 original sequences and summary.
- `results/strict-runs/`: 54 additional controlled old-parent sequences.
- `results/independent-audit.json`, `strict-independent-audit.json`: independent
  Python certificate, inverse, relationship and ledger-sum checks.
- `results/reproducibility.json`: full main regeneration, byte-identical receipts.
- `results/strict-replay.json`: full strict policy replay from saved raw problems.
- `results/comparisons.csv`: all per-policy totals and cost categories.
- `MANIFEST.json`: SHA-256 integrity manifest for the packet's other files.

No new license is granted here. Existing research rights and privacy remain.
