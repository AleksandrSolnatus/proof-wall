# Stone 003B research packet

Start with `STONE-003B-WHEN-THE-PIECES-RECONNECT.md`, then `METHOD-AND-PROOF.md`.
`SUMMARY.json` contains machine-readable headline results.

Requirements: Python 3.10 or later; standard library only. No network, account,
package installation, or external data is needed to reproduce the experiments.

Verify archived bytes BEFORE running scripts that rewrite outputs:

```sh
sha256sum -c MANIFEST.sha256
python test_engine.py
python independent_check.py
```

Regenerate experiments (timings change):

```sh
python run_experiments.py
python independent_check.py
```

Each suite can be run separately, for example:

```sh
python run_experiments.py --suites replay chains
```

Repeat the final benchmarks separately when execution time limits apply:

```sh
python benchmark.py --case 0
python benchmark.py --case 1
python benchmark.py --case 2
python benchmark.py --case 3
python build_report.py
```

These write per-case files to `benchmarks/` and aggregate them in `benchmark.json`.
Case indexes: original replay, 64-region chain, 5x5 grid, selected random-cross case.
The full 4-case benchmark also runs with `python benchmark.py` where permitted.
The report builder expects all seven suite JSONs and all four final benchmark cases.

Table budget: 262,144 assignments in one dense combination. A budget stop carries
no count and is not UNSAT. This is not a total-memory/time guarantee. Sources and
caches are retained, and the cache has no eviction policy. The baseline BDD also
has no global resource cap. Use these as bounded research programs, not a service
for untrusted or unrestricted large inputs.

All inputs and full seeds are in the result JSONs. The independent checker does
not import the tested algorithms. It validates counts, not benchmark timings.

`original/math_stone_003/` preserves the parent packet, whose 156 checks were rerun.
`history/` preserves pilot timing evidence and a timeout log; those are not the
final benchmark source. See `RESEARCH-LOG.md` for the distinction.

All SHA-256 checksums are integrity receipts, not external signatures or proofs.
