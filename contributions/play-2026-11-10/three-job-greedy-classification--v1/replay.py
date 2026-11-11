#!/usr/bin/env python3
"""Exact independent check of the public three-job classification.
No network, dependencies, private fixtures, or external solver imports.
"""
from itertools import product
from fractions import Fraction
from pathlib import Path
from hashlib import sha256
import json
import time

def list_schedule(jobs):
    assignment, loads = [], [0, 0]
    for p in jobs:
        machine = 0 if loads[0] <= loads[1] else 1
        loads[machine] += p
        assignment.append(machine)
    return assignment, loads, max(loads)

def evaluate(jobs, assignment):
    left = sum(p for p, machine in zip(jobs, assignment) if machine == 0)
    right = sum(p for p, machine in zip(jobs, assignment) if machine == 1)
    return [left, right], max(left, right)

def exhaustive(jobs):
    rows = []
    for assignment in product((0, 1), repeat=len(jobs)):
        loads, makespan = evaluate(jobs, assignment)
        rows.append({"assignment": list(assignment), "loads": loads, "makespan": makespan})
    return min(row["makespan"] for row in rows), rows

def verify():
    start = time.perf_counter()
    inputs, assignments, failures, swapped = 0, 0, 0, 0
    worst, first = Fraction(0, 1), None
    equality_cases = 0
    for length in (1, 2, 3):
        for jobs in product(range(1, 21), repeat=length):
            _, _, g = list_schedule(jobs)
            optimum, rows = exhaustive(jobs)
            inputs += 1
            assignments += len(rows)
            if length <= 2:
                assert g == optimum
            else:
                x,y,z = jobs
                m,M = min(x,y),max(x,y)
                swapped += x > y
                formula = min(max(m+M,z), max(M,m+z))
                assert optimum == formula, ("optimum",jobs)
                assert (g > optimum) == (z > M), ("failure",jobs)
                if z > M:
                    assert g-optimum == min(m,z-M), ("excess",jobs)
                ratio = Fraction(g, optimum)
                assert ratio <= Fraction(3,2)
                assert (ratio == Fraction(3,2)) == (m == M and z == 2*m)
                equality_cases += ratio == Fraction(3,2)
            if g > optimum:
                failures += 1
                if first is None:
                    first = list(jobs)
            worst = max(worst, Fraction(g, optimum))
    assert inputs == 8420
    assert assignments == 65640
    assert failures == 2470
    assert swapped == 3800
    assert first == [1,1,2]
    assert worst == Fraction(3,2)
    fixtures = []
    for jobs in ([1,1,2],[2,2,3],[5,2,6],[5,2,4]):
        optimum, rows = exhaustive(jobs)
        assignment, loads, g = list_schedule(jobs)
        fixtures.append({"jobs":jobs, "greedy_assignment":assignment,"greedy_loads":loads,
                         "greedy_makespan":g,"optimum":optimum,"all_assignments":rows})
    return {"status":"PASS","scope":{"job_counts":[1,2,3],"positive_integer_durations":[1,20],
            "machines":2,"ties":"machine 0"},"inputs_checked":inputs,
            "assignments_enumerated":assignments,"greedy_failures":failures,
            "ordered_triples_with_x_greater_y":swapped,"first_failure":first,
            "worst_ratio":str(worst),"ratio_equality_cases":equality_cases,
            "fixtures":fixtures,
            "proof_scope":"All positive real three-job durations; see article.md.",
            "replay_scope":"Only the explicit bounded integer domain above.",
            "elapsed_seconds":time.perf_counter()-start,
            "source_sha256":sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__ == "__main__":
    result = verify()
    (Path(__file__).resolve().parent/"results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:result[k] for k in ("status","inputs_checked","assignments_enumerated",
        "greedy_failures","ordered_triples_with_x_greater_y","worst_ratio","elapsed_seconds")},indent=2))

