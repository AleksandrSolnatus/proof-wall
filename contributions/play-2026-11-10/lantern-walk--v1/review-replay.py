#!/usr/bin/env python3
"""Independent adversarial replay; imports no Lantern Walk implementation."""
from itertools import combinations, permutations
from collections import defaultdict, Counter
from pathlib import Path
from hashlib import sha256
import json, time, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--target", type=Path, required=True,
                    help="Directory containing the reviewed article.md and experiment.py")
TARGET = parser.parse_args().target

def components(n, edges):
    parent=list(range(n))
    def root(v):
        while parent[v] != v:
            v=parent[v]
        return v
    for a,b in edges:
        parent[root(a)] = root(b)
    return len({root(i) for i in range(n)})

def signature(n, edges):
    degrees=[0]*n
    es={frozenset((a,b)) for a,b in edges}
    for a,b in edges:
        degrees[a]+=1;degrees[b]+=1
    triangles=sum(all(frozenset(pair) in es for pair in combinations(triple,2))
                  for triple in combinations(range(n),3))
    return tuple(sorted(degrees)), triangles

def enumerate_domain():
    records=[]
    for n in range(1,7):
        possible=list(combinations(range(n),2))
        groups=defaultdict(lambda:[0,0])
        for mask in range(2**len(possible)):
            edges=[edge for i,edge in enumerate(possible) if mask & 2**i]
            groups[signature(n,edges)][components(n,edges)==1]+=1
        ambiguous=[{"degrees":k[0],"triangles":k[1],"disconnected":v[0],"connected":v[1]}
                   for k,v in groups.items() if all(v)]
        records.append({"n":n,"graphs":2**len(possible),"ambiguous":ambiguous})
    assert all(not r["ambiguous"] for r in records[:5])
    assert records[-1]["ambiguous"]==[{"degrees":(1,1,2,2,2,2),"triangles":0,"disconnected":45,"connected":360}]
    return records

def local_ball(n, edges, origin, radius):
    # Synchronous set expansion, independent of the target queue traversal.
    visible={origin}
    for _ in range(radius):
        visible=visible | {v for a,b in edges for u,v in ((a,b),(b,a)) if u in visible}
    ordered=[origin]+sorted(visible-{origin})
    mapping={old:new for new,old in enumerate(ordered)}
    induced={frozenset((mapping[a],mapping[b])) for a,b in edges if a in visible and b in visible}
    return len(ordered), induced

permutation_count=0
def canonical(n, edges, origin, radius):
    global permutation_count
    k,induced=local_ball(n,edges,origin,radius)
    best=None
    for order in permutations(range(1,k)):
        permutation_count += 1
        p=(0,*order)
        key=tuple(frozenset((p[a],p[b])) in induced for a,b in combinations(range(k),2))
        best=key if best is None or key < best else best
    return k,best

def path(n,offset=0):
    return [(i+offset,i+offset+1) for i in range(n-1)]
def cycle(n,offset=0):
    return path(n,offset)+[(offset,offset+n-1)]

def exact_windows():
    records=[]
    for r in (1,2,3):
        n=4*r+2
        a=path(n)
        b=cycle(2*r+2)+path(2*r,2*r+2)
        ah=Counter(canonical(n,a,i,r) for i in range(n))
        bh=Counter(canonical(n,b,i,r) for i in range(n))
        assert ah==bh
        assert components(n,a)==1 and components(n,b)==2
        assert signature(n,a)==signature(n,b)
        record={"r":r,"n":n,"rooted_histogram_equal":True,"rooted_types":len(ah),
                "rooted_type_counts":sorted(ah.values())}
        if r<=2:
            deeper_a=Counter(canonical(n,a,i,r+1) for i in range(n))
            deeper_b=Counter(canonical(n,b,i,r+1) for i in range(n))
            assert deeper_a!=deeper_b
            record["next_radius_equal"]=False
        records.append(record)
    # Counterexample to generalizing visible-count summaries into isomorphism:
    # root 0 joined to all four others; on others P4 vs K3 + isolated.
    # Both radius-one balls have n5,e7 and layer sizes1,4, but 3 vs4 triangles.
    a=[(0,i) for i in range(1,5)]+[(1,2),(2,3),(3,4)]
    b=[(0,i) for i in range(1,5)]+[(1,2),(1,3),(2,3)]
    assert len(a)==len(b)==7
    assert canonical(5,a,0,1)!=canonical(5,b,0,1)
    assert signature(5,a)[1]==3 and signature(5,b)[1]==4
    return records,{"same_vertices":5,"same_edges":7,"same_layer_sizes":[1,4],
                    "isomorphic":False,"a":a,"b":b,
                    "interpretation":"Supports article's explicit restriction of count summaries to generated cycle families."}

start=time.perf_counter()
small=enumerate_domain()
windows,guard=exact_windows()
report={"status":"PASS","method":"Independent DSU connectivity, triangle triples, and exhaustive root-fixing permutation canonicalization.",
        "source_hashes":{name:sha256((TARGET/name).read_bytes()).hexdigest() for name in ("article.md","experiment.py")},
        "enumeration":small,"rooted_checks":windows,"root_fixing_permutations":permutation_count,
        "general_summary_guard":guard,"elapsed_seconds":time.perf_counter()-start}
Path(__file__).with_name("review-results.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({k:report[k] for k in ("status","rooted_checks","root_fixing_permutations","elapsed_seconds")},indent=2))

