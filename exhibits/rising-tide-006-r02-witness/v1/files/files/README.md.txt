# R02 independent witness verification — November 7, 2026

The preserved receipt reports that the R02 assignment satisfies all 819 original clauses and that all 192 assignment bits agree with the signed solver model. This is a finite witness check, not a performance benchmark or a general theorem.

This four-file selection includes the checker and saved receipt, but not the source-provenance.json or five original source files that the checker requires. It is therefore not a self-contained reproduction bundle. The checker reads the historical solve_forward.py to check ordering evidence; it never executes that file. The clause audit, original inputs and producer remain in private custody and are not included.

The historical solve used Python-SAT and CaDiCaL. The independent checker uses only Python's standard library and does not invoke a solver. Later Drago verification is reported in the separate provenance supplement; no new scientific run is claimed here.
