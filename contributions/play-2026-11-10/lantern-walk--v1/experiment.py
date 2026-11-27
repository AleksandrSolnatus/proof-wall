#!/usr/bin/env python3
"""Lantern Walk: exact, dependency-free finite graph experiments.

Enumerates every labelled simple undirected graph on 1..6 vertices.
Checks the cycle family using an independent breadth-first traversal.
This program uses no SAT solver, heuristic graph matcher, or network.
"""
from collections import Counter, defaultdict, deque
from itertools import combinations
import json
from pathlib import Path


def adjacency(n, edges):
    rows = [set() for _ in range(n)]
    for a, b in edges:
        assert 0 <= a < n and 0 <= b < n and a != b
        rows[a].add(b)
        rows[b].add(a)
    return rows


def ball(rows, root, radius):
    distances = {root: 0}
    queue = deque([root])
    while queue:
        a = queue.popleft()
        if distances[a] == radius:
            continue
        for b in rows[a]:
            if b not in distances:
                distances[b] = distances[a] + 1
                queue.append(b)
    vertices = sorted(distances)
    edges = [(a, b) for a in vertices for b in rows[a] if a < b and b in distances]
    return {"vertices": vertices, "edges": edges,
            "distance_histogram": [sum(d == k for d in distances.values()) for k in range(radius + 1)]}


def cycle(n, offset=0):
    return sorted(tuple(sorted((offset + i, offset + (i + 1) % n))) for i in range(n))


def summary(n, edges):
    rows = adjacency(n, edges)
    seen = set()
    components = []
    for root in range(n):
        if root in seen:
            continue
        part = ball(rows, root, n)["vertices"]
        components.append(part)
        seen.update(part)
    return {"vertices": n, "edges": len(edges),
            "degrees": sorted(map(len, rows)),
            "triangles": sum(c in rows[a] and c in rows[b] for a, b in edges for c in range(b + 1, n)),
            "components": components, "connected": len(components) == 1}


def enumerate_small(max_n=6):
    report = []
    for n in range(1, max_n + 1):
        pairs = list(combinations(range(n), 2))
        groups = defaultdict(lambda: {False: 0, True: 0, "witnesses": {}})
        for mask in range(1 << len(pairs)):
            rows = [0] * n
            for i, (a, b) in enumerate(pairs):
                if mask >> i & 1:
                    rows[a] |= 1 << b
                    rows[b] |= 1 << a
            degrees = tuple(sorted(x.bit_count() for x in rows))
            triangles = sum((rows[a] & rows[b]).bit_count() for a, b in pairs if rows[a] >> b & 1) // 3
            seen = pending = 1
            while pending:
                bit = pending & -pending
                pending ^= bit
                new = rows[bit.bit_length() - 1] & ~seen
                seen |= new
                pending |= new
            connected = seen == (1 << n) - 1
            group = groups[degrees, triangles]
            group[connected] += 1
            group["witnesses"].setdefault(connected, mask)
        collisions = []
        for (degrees, triangles), group in sorted(groups.items()):
            if group[True] and group[False]:
                witnesses = {}
                for value in (True, False):
                    mask = group["witnesses"][value]
                    edges = [p for i, p in enumerate(pairs) if mask >> i & 1]
                    check = summary(n, edges)
                    assert check["connected"] == value
                    assert check["degrees"] == list(degrees)
                    assert check["triangles"] == triangles
                    witnesses[str(value).lower()] = {"edge_mask": mask, "edges": edges}
                collisions.append({"degrees": degrees, "triangles": triangles,
                    "connected_graphs": group[True], "disconnected_graphs": group[False],
                    "witnesses": witnesses})
        report.append({"n": n, "labelled_graphs": 1 << len(pairs),
            "shadow_classes": len(groups), "ambiguous_classes": len(collisions),
            "collisions": collisions})
    return report


def cycle_family():
    report = []
    for m in range(4, 17):
        n = 2 * m
        edges_a = cycle(n)
        edges_b = cycle(m) + cycle(m, m)
        a, b = adjacency(n, edges_a), adjacency(n, edges_b)
        s_a, s_b = summary(n, edges_a), summary(n, edges_b)
        for key in ("vertices", "edges", "degrees", "triangles"):
            assert s_a[key] == s_b[key]
        first_difference = None
        profiles = []
        for radius in range(m + 1):
            aa, bb = ball(a, 0, radius), ball(b, 0, radius)
            shadow_a = (len(aa["vertices"]), len(aa["edges"]), aa["distance_histogram"])
            shadow_b = (len(bb["vertices"]), len(bb["edges"]), bb["distance_histogram"])
            same = shadow_a == shadow_b
            if not same and first_difference is None:
                first_difference = radius
            profiles.append({"radius": radius, "same_ball_summary": same,
                "a": shadow_a, "b": shadow_b})
        assert first_difference == m // 2
        assert s_a["connected"] and not s_b["connected"]
        report.append({"m": m, "n": n, "first_distinguishing_radius": first_difference,
            "profiles": profiles})
    return report


def rooted_path_or_cycle(rows, root, radius):
    """Exact rooted isomorphism key for a connected max-degree-two ball."""
    region = ball(rows, root, radius)
    vertices = set(region["vertices"])
    local = {v: rows[v] & vertices for v in vertices}
    if len(vertices) == 1:
        return ("path", 0, 0)
    ends = [v for v in vertices if len(local[v]) == 1]
    if not ends:
        assert all(len(local[v]) == 2 for v in vertices)
        return ("cycle", len(vertices))
    assert len(ends) == 2
    distances = {root: 0}
    queue = deque([root])
    while queue:
        u = queue.popleft()
        for v in local[u]:
            if v not in distances:
                distances[v] = distances[u] + 1
                queue.append(v)
    return ("path", *sorted(distances[v] for v in ends))


def all_windows_family():
    """Even every local window can agree while connectivity differs."""
    report = []
    for radius in range(1, 9):
        n = 4 * radius + 2
        a = [(i, i + 1) for i in range(n - 1)]
        b = cycle(2 * radius + 2) + [(i, i + 1) for i in range(2 * radius + 2, n - 1)]
        rows_a, rows_b = adjacency(n, a), adjacency(n, b)
        ha = Counter(rooted_path_or_cycle(rows_a, root, radius) for root in range(n))
        hb = Counter(rooted_path_or_cycle(rows_b, root, radius) for root in range(n))
        assert ha == hb
        deeper_a = Counter(rooted_path_or_cycle(rows_a, root, radius + 1) for root in range(n))
        deeper_b = Counter(rooted_path_or_cycle(rows_b, root, radius + 1) for root in range(n))
        assert deeper_a != deeper_b
        sa, sb = summary(n, a), summary(n, b)
        for key in ("vertices", "edges", "degrees", "triangles"):
            assert sa[key] == sb[key]
        assert sa["connected"] and not sb["connected"]
        report.append({"radius": radius, "n": n, "edges_a": a, "edges_b": b,
            "exact_rooted_ball_histogram": [{"key": key, "count": count} for key, count in sorted(ha.items())],
            "histograms_equal": True, "next_radius_equal": False})
    return report


def run():
    small = enumerate_small()
    assert sum(row["labelled_graphs"] for row in small) == 33867
    assert [row["ambiguous_classes"] for row in small] == [0, 0, 0, 0, 0, 1]
    collision = small[-1]["collisions"][0]
    assert collision["connected_graphs"] == 360
    assert collision["disconnected_graphs"] == 45
    path = [(i, i + 1) for i in range(5)]
    broken = cycle(4) + [(4, 5)]
    a, b = summary(6, path), summary(6, broken)
    for key in ("vertices", "edges", "degrees", "triangles"):
        assert a[key] == b[key]
    assert a["connected"] and not b["connected"]
    return {"format": "lantern-walk-results/1", "status": "verified-finite-result",
        "enumeration": small, "minimum_witness": {"a": path, "b": broken, "summary_a": a, "summary_b": b},
        "cycle_family": cycle_family(), "all_windows_family": all_windows_family(),
        "limits": ["Simple, undirected, unweighted graphs only.",
                   "Exhaustive search stops at six vertices.",
                   "The interactive fixture family is C_(2m) versus two disjoint C_m, 4 <= m <= 16.",
                   "This does not establish a complexity lower bound or a P-versus-NP result."]}


if __name__ == "__main__":
    result = run()
    destination = Path(__file__).with_name("results.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: 33,867 labelled graphs; first connectivity collision at n=6; 13 cycle pairs and 8 all-windows pairs checked.")
