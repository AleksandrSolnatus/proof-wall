# Lantern Walk — independent adversarial review

**Outcome: no mathematical defect found in the three requested claims.**

I tried the boundary cases r=1, endpoint-adjacent vertices, the two central vertices of the short path, odd versus even cycle lengths, and a deliberately misleading count-only ball comparison. I also wrote a separate checker that imports no code from the toy.

## All-windows family

The claimed histogram for P_(4r+2) versus C_(2r+2) disjoint P_(2r) is correct for every integer r≥1.

For a vertex at nearest-endpoint distance d in 0,…,r−1, the short path's opposite endpoint is 2r−1−d edges away, which is at least r. Its induced radius-r ball is therefore a path with root-to-end distances {d,r}, exactly as in the long path. Both graphs have two such roots for each d.

The long path has 2r+2 remaining roots. Their balls have endpoint distances {r,r}. A radius-r ball in C_(2r+2) omits the unique antipodal vertex and is precisely that same rooted path. Hence the cycle supplies exactly 2r+2 matching roots. This explicitly checks the point most likely to go wrong: the short path has no additional interior-root category.

At radius r+1 every cycle root sees a closed cycle. Every ball in the long path is still acyclic, so the histograms must differ. The construction fails at r=0 because it would use a two-cycle, which is not a simple undirected cycle; the article correctly requires r≥1.

An independent exhaustive root-fixing permutation matcher confirmed histogram equality at r=1,2,3, and separation at r+1 for r=1,2. It performed 16,522 permutation checks, including the separate guard below. It does not rely on the toy's endpoint-distance canonical key.

## Minimal n=6 collision

A separately written exhaustive enumerator used disjoint-set union for connectivity and explicit triples for triangle counts. It reproduced all 33,867 labelled graphs on 1–6 vertices.

There are no mixed-connectivity signature classes through five vertices. At six there is exactly one: sorted degrees (1,1,2,2,2,2), triangle count zero, with 360 connected and 45 disconnected graphs.

There is also a direct count sanity check. A connected graph with this degree sequence is P6, giving 6!/2=360 labelings. A disconnected triangle-free graph with this sequence must be C4 plus an edge, giving choose(6,4)×3=45 labelings. The finite enumeration, rather than this sanity check alone, excludes other signatures.

## Cycle threshold and summary guard

For C_(2m) versus two C_m, the article's first distinguishing radius floor(m/2) is correct. If m is even the smaller ball has fewer vertices at that radius; if m is odd it gains a closing edge. Earlier balls are exact rooted paths.

Count-only summaries are not general rooted-isomorphism tests. As an adversarial guard I built two five-vertex radius-one balls with the same root degree, vertex count, edge count, and distance-layer sizes: connect the root to all four others, then place P4 among the others in one ball and a triangle plus an isolated vertex among them in the other. The balls have three versus four triangles and are not isomorphic. The article already excludes this generalization; the guard reinforces that its qualifier is necessary.

## Implementation limits

The Python implementation's edge-order assumptions are satisfied by every generated fixture. Its path/cycle canonicalizer is exact on the promised connected maximum-degree-two domain. Optional future hardening would assert that maximum degree explicitly before constructing an endpoint-distance key; no current generated input violates it.

This review did not operate the browser interface or recheck its JavaScript comparison ledger. Those remain root's separate checks.

## Reproduce and identify

Run:
`python3 review-replay.py --target /path/to/lantern-walk`

The script independently repeats the full small-graph enumeration, exact permutation comparisons, and summary guard, then writes `review-results.json`. That receipt records SHA-256 hashes of the exact reviewed article and Python experiment. No private service records or account identifiers are included.

The separate checker passed. Its bounded tests support the stated implementation; the endpoint argument above supplies the all-r justification.

