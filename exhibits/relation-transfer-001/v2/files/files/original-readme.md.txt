# RELATION-TRANSFER-001 — private offline reproduction

Start with `RELATION-TRANSFER-001-REPORT.md`. This archive contains unmodified relevant source files at pinned private GitHub commits, original fixture/demo evidence, the explicit adapter, independent binding/truth-table checks, and execution results. It is a focused snapshot, not a full checkout or deployed integration. No network or third-party packages are required for reproduction.

Requirements: Node.js 22.13+ and Python 3. Tested here with Node v24.22.1 and Python 3.12.14. Run from this directory:

```bash
python3 verify_snapshot.py
node upstream/rulebench/tests/relation-capsule.mjs
PYTHONPATH=upstream/lotus-garden python3 -m unittest discover -s upstream/lotus-garden/tests -p 'test_relation_pollen*.py' -v
python3 run.py --out results/reproduction
```

The last command exports the real Lotus fixture, invokes actual Rulebench discovery, translates both capsules, invokes the unmodified independent Lotus checker, compares actual satisfying assignments, exercises rejection and moderation gates, and writes full inputs and results. Every database is temporary. Owner approval is simulated only on disposable local records. No service is started, no live submission is touched, and no credential is needed. Timing, UUIDs, and timestamps vary; the generated proof/proposal contents and logical outcomes are reproducible.

`results/run-002/` is the final recorded run. `run-001/` preserves the earlier run before adding six binding-tamper tests and the direct-target discovery control. The initial Python import-path mistake is retained in `results/lotus-initial-import-error.txt`; the corrected run and all final tests passed. Relevant upstream tests passed, but the full repository suites were not run from this focused snapshot.

The schema-gap probes intentionally document acceptance defects, rather than asserting that the original implementations reject everything. Inspect `summary.json` and the report before using these formats. The adapter handles only the common one-step/fixed-source subset. It is not an automatic approval or trust mechanism.
