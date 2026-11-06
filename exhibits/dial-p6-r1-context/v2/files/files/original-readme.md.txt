# P6-R1 authoritative execution folder

This folder is the authoritative execution record for the **single authorized P6-R1 v1.0 run on 2026-10-01 (America/Phoenix)**.

## Outcome

**Survives this particular sensitivity check.**  
S07 add-one p = `0.036594817`; S25 = `0.033479833`; governing max = `0.036594817`. Both are below the frozen 0.05 weakening gate.

## Inspect in this order

1. `results/P6_R1_REPORT.md` — measured result and interpretation.
2. `preflight/PRE_SAMPLING_MANIFEST.json` — frozen implementation/input identities before random draws.
3. `preflight/P6_R1_PREFLIGHT.json` — deterministic preflight checks.
4. `implementation/run_p6_r1.py` — frozen executor.
5. `results/P6_R1_RESULTS.json` — complete statistical result and distribution counts.
6. `raw/P6_R1_T_S07.csv.gz`, `raw/P6_R1_T_S25.csv.gz` — 200,000 accepted T values each.
7. `results/POSTRUN_VERIFICATION.json` — reconciliation of raw ledgers to results.
8. `receipts/CLEANUP_RECEIPT.md` — closure record.
9. `MANIFEST.sha256` — final artifact hashes (manifest excludes itself).

`source/original/corpus_masked.json` is the byte-identical raw source. `source/working/eligible_S07.json` and `eligible_S25.json` are explicitly transformed working inputs. `reference/` preserves the governing P6-R1 protocol, execution wrapper, and untouched P-6 baseline references. The ZIP of this folder is transport only; it is not a second authoritative version.
