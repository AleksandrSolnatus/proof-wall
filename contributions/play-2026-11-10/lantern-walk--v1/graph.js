(function (root) {
  'use strict';
  function cycle(n, offset = 0) {
    return Array.from({length: n}, (_, i) => [offset + i, offset + (i + 1) % n]);
  }
  function adjacency(n, edges) {
    const a = Array.from({length: n}, () => []);
    for (const [u, v] of edges) { a[u].push(v); a[v].push(u); }
    return a;
  }
  function ball(n, edges, origin, radius) {
    const a = adjacency(n, edges), distance = Array(n).fill(-1), q = [origin];
    distance[origin] = 0;
    for (let at = 0; at < q.length; at++) {
      const u = q[at];
      if (distance[u] === radius) continue;
      for (const v of a[u]) if (distance[v] < 0) { distance[v] = distance[u] + 1; q.push(v); }
    }
    return {vertices: q.slice().sort((a,b) => a-b),
      edges: edges.filter(([a,b]) => distance[a] >= 0 && distance[b] >= 0), distance};
  }
  function summary(n, edges) {
    const a = adjacency(n, edges), seen = new Set(), components = [];
    for (let i=0; i<n; i++) if (!seen.has(i)) {
      const c=ball(n, edges, i, n).vertices; c.forEach(v=>seen.add(v)); components.push(c);
    }
    let triangles=0;
    for (let i=0;i<n;i++) for(let j=i+1;j<n;j++) for(let k=j+1;k<n;k++)
      if(a[i].includes(j)&&a[j].includes(k)&&a[k].includes(i)) triangles++;
    return {vertices:n, edges:edges.length, degrees:a.map(x=>x.length).sort((a,b)=>a-b), triangles, components};
  }
  function pair(m) { return {n:2*m, a:cycle(2*m), b:cycle(m).concat(cycle(m,m))}; }
  const api={cycle, adjacency, ball, summary, pair};
  if(typeof module !== 'undefined' && module.exports) module.exports=api;
  else root.LanternGraph=api;
})(typeof window !== 'undefined' ? window : this);
