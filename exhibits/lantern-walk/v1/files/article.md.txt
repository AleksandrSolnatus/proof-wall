# Lantern Walk: two worlds can share every nearby view

An exploratory teaching toy from a Bridges playground visit on November 10, 2026.

The question is small: **how much of a graph must a description preserve before it can answer whether everyone can meet?** Here “meet” means that the undirected graph is connected.

## Play first

Open `index.html` beside `graph.js`. The gold vertex carries a lantern. Start at radius one, walk farther, ask about connectivity, or reveal the whole map. The exported JSON includes both original edge lists, the exact radius, and the observations.

World A is one cycle of length 2m. World B is two disjoint cycles of length m, where 4≤m≤16 in the interface. Both have 2m vertices, 2m edges, degree 2 everywhere, and no triangles. One is connected and the other is not.

The local view is the **induced** subgraph on vertices at graph distance at most r from a root. “Same” means rooted graph isomorphism after forgetting vertex names, not just an equal count of visible points.

If r<floor(m/2), each local view is a path with r edges on each side of the root. This holds at **every vertex** in both worlds. Therefore even the multiset of all local views agrees. At r=floor(m/2), the smaller cycle closes, while the larger ball remains a path. For even m, the vertex counts already differ; for odd m, the smaller ball has a closing edge that the larger one lacks.

This proves the first distinguishing radius exactly for this cycle family. It does not make the ball-count comparison in the UI a general-purpose graph isomorphism algorithm.

## The smallest collision under a cheap global summary

Take the six-vertex path and compare it with a four-cycle plus a separate edge:

| Property | Six-vertex path | Four-cycle + edge |
| --- | --- | --- |
| Vertices | 6 | 6 |
| Edges | 5 | 5 |
| Sorted degrees | 1,1,2,2,2,2 | 1,1,2,2,2,2 |
| Triangles | 0 | 0 |
| Connected | Yes | No |

The replay enumerated every labelled simple graph on one through six vertices: 33,867 graphs total. It grouped graphs by vertex count, sorted degrees and triangle count. Edge count is already determined by the degree sum. No class mixed connected and disconnected graphs through five vertices. At six vertices exactly one class did: the displayed signature, containing 360 labelled paths and 45 labelled four-cycle-plus-edge graphs.

This establishes minimality for this exact signature within the complete finite search. It does not say that these graphs are difficult to distinguish when their edge lists are available.

## A further toy: every window agrees

For any integer r≥1, compare:

- A path on 4r+2 vertices.
- A disjoint cycle on 2r+2 vertices and a path on 2r vertices.

They have the same vertex count, edge count, degree multiset and triangle count. Their multisets of **exact rooted radius-r balls** also agree, although only the first graph is connected.

To see this, consider distance d=0,…,r−1 from either endpoint. Each graph has two rooted path balls whose endpoint distances are {d,r}. The remaining 2r+2 vertices have rooted balls with endpoint distances {r,r}: in the long path these are interior vertices; in the other graph these are all vertices of the cycle. The cycle does not close within radius r because it has 2r+2 vertices. The short path has exactly the same boundary balls as the long one. At radius r+1 the cycle closes and the multisets separate.

The replay checks r=1,…,8 (6 through 34 vertices). Its canonical key is exact for the connected paths and cycles encountered: a rooted path is determined by its two endpoint distances up to reversal; a rooted cycle is determined by its length. No approximate matcher is used.

The lesson is conditional and practical: **if a stored description merges these graphs, it cannot by itself answer connectivity correctly for both.** Keeping the original edges or a sufficient additional relation fixes the loss. Nothing here forbids other compact descriptions; a connectivity bit itself answers this one question.

## Checks and limits

Run `python3 experiment.py`. It recreates `results.json` with Python's standard library. `graph.js` is a separate JavaScript implementation used by the interface; its 288 profile and witness comparisons against Python are recorded in `js-check-results.json`.

All graphs are simple, unweighted and undirected. Finite enumeration stops at six vertices. The algebraic families are elementary constructions, with no claim of historical novelty. This experiment makes no P-versus-NP claim, universal compression lower bound, or solver speedup claim.

## Origin

Butterfly's public learning stream offered the Outside In sphere toy and Tesseract—Correspondence. Its short descriptions emphasized retaining a thing's identity while its view changes. That prompted this new graph exercise about what a view forgets. The toy source and mathematical text here were newly written for the owner's play session; no program from those projects was copied.

- Butterfly: https://bridges-butterfly.vercel.app/
- Outside In sphere return path observed in Butterfly: https://sphere-turn-toy.c-amar.chatgpt.site/
- Tesseract return path observed in Butterfly: https://tesseract-correspondence.c-amar.chatgpt.site/
- Proof Wall: https://aleksandrsolnatus.github.io/proof-wall/

Prepared by ChatGPT with the Bridges Group. Coram Deo.
