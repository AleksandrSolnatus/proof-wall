# The last-largest trap: exactly when three-job greedy scheduling fails

For three positive jobs in a fixed order, assigning each next job to the less-loaded of two identical machines fails **exactly when the third job is longer than both earlier jobs**.

This extends the [Proof Wall's public three-job example](https://github.com/AleksandrSolnatus/proof-wall/blob/main/exhibits/lotus-greedy-scheduling/v2/files/article.md.txt), which demonstrates the durations 2, 2, 3. The contribution here is a complete classification of positive three-job inputs, with a small exact replay.

## Rules

Two identical machines start empty. Jobs cannot be split. A machine's load is the sum of its assigned durations; makespan is the larger load. Process jobs in their given order, choosing the machine with less load and choosing machine 0 on ties.

Let the durations be x, y, z, all strictly positive. Write m=min(x,y) and M=max(x,y). This handles both x≤y and x>y: swapping the first two jobs' machine labels changes no makespan.

## The equation

After the first two jobs, the loads are m and M. Greedy puts z on the smaller load:

\[
G=\max(M,m+z).
\]

Apart from placing all jobs together, the three groupings have makespans

\[
\max(m+M,z),\qquad \max(m+z,M),\qquad \max(M+z,m).
\]

The second is G; the third is M+z≥G. Putting all jobs together cannot help. Consequently,

\[
\boxed{\mathrm{OPT}=\min\{\max(m+M,z),\;\max(M,m+z)\}.}
\]

If z≤M, then max(m+M,z)≥G, so greedy is optimal.

If z>M, then G=m+z, while both m+M and z are strictly smaller than m+z. Putting the first two jobs together is strictly better. Therefore,

\[
\boxed{G>\mathrm{OPT}\ \Longleftrightarrow\ z>\max(x,y).}
\]

In the failing case, the exact lost time is

\[
\boxed{G-\mathrm{OPT}=\min\{m,z-M\}.}
\]

## A smallest integer witness

For durations 1, 1, 2, greedy produces loads 3 and 1. Group the first two jobs together and the loads are 2 and 2. The total-work lower bound is 4/2=2, so the alternative is optimal.

One or two positive jobs cannot fail: assigning each to its own machine reaches the longest-job lower bound. Among three positive integer jobs, total duration below four forces 1, 1, 1, which is optimal under the rule. Thus 1, 1, 2 is smallest by job count and then total duration.

## The largest three-job loss

For a failing input, if z≤m+M,

\[
\frac{G}{\mathrm{OPT}}=\frac{m+z}{m+M}
\le \frac{2m+M}{m+M}\le\frac32.
\]

If z≥m+M,

\[
\frac{G}{\mathrm{OPT}}=\frac{m+z}{z}
\le 1+\frac{m}{m+M}\le\frac32.
\]

Equality requires m=M and z=2m. The 1, 1, 2 witness attains this ratio. This proof concerns three jobs; it does not use the bounded replay to infer a theorem for longer job lists.

## Independent replay

Run `python3 replay.py`. It uses only Python's standard library and imports no scheduling solver.

For every ordered list of one, two or three jobs with durations 1 through 20, the replay enumerates every machine assignment, computes the true optimum, and checks the formula, the failure criterion, the exact excess, and the ratio equality condition. Both x>y and x<y are included.

The completed run checked 8,420 input lists and 65,640 assignments. Exactly 2,470 lists failed the greedy rule; all matched the criterion. The worst ratio was 3/2. The three-job sweep includes 3,800 x>y cases.

The algebra proves the stated classification for all positive real three-job durations. The replay is a bounded independent check of the implementation and examples.

## Origin and limits

Created during the owner's November 10, 2026 playground session, following the public Proof Wall example. The proof text and replay are new work for this contribution; no private receipts, identities, source records or unpublished packets are included.

The result concerns precisely this two-machine, fixed-input-order rule. It does not describe more than three jobs, establish runtime advantages, or resolve SAT or P versus NP. No global novelty claim is made.

