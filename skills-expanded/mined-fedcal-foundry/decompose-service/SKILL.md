---
name: decompose-service
description: Decide whether to extract a service from a monolith or leave it in place, using measured coupling and cohesion, data ownership, transactional boundaries and team topology rather than fashion. Includes the hard do-not-split gates that stop a decomposition before it starts, and the extraction sequence when a split is genuinely justified. Use before any "let's make it a microservice" conversation.
user-invocable: true
argument-hint: "<candidate-module> [--since 12.months]"
metadata:
  foundry.vertical: dev
  foundry.io: "codebase + git history -> review.v1 + adr.v1 (+ plan.v1 if splitting)"
license: Apache-2.0
---

# Decompose (or do not decompose) a service

**The default answer is no.** A monolith with clean internal boundaries is strictly easier to
operate than the same boundaries stretched over a network, because in-process calls do not
partition, do not time out, and do not need tracing to debug. The burden of proof is entirely on
the split.

This skill exists to make that proof measurable. You will produce numbers, then decide, then
record the decision as an ADR. "It feels too big" is not an input.

## Step 0 — What actually forces a split

A split is justified only by a need that **cannot** be met inside one deployable. There are
exactly five, and each must come with a measurement:

| Legitimate driver | Evidence required |
|---|---|
| Independent scaling | one component's resource curve diverges: e.g. it needs 8× the CPU at peak while the rest idles, measured, not assumed |
| Independent failure isolation | a failure in that component currently takes the whole process down, with incident references |
| Independent deployment cadence | the component changes ≥ 5× more often than the rest, or is blocked by the rest's release train, measured from git |
| Independent data lifecycle or residency | a legal or contractual requirement to store/process the data elsewhere (cite the clause) |
| Independent team ownership at scale | ≥ 2 teams contend for the same code and merge/coordination cost is documented |

Reasons that are **not** drivers, however often they are offered: reuse (a library solves that),
"we want to use another language" (rarely worth a network boundary), "the repo is big" (split the
modules, not the process), "microservices are best practice", team preference, and hiring appeal.

## Step 1 — Measure before you argue

Run the measurements in `references/metrics.md`. The four that decide most cases:

1. **Co-change coupling** — how often two candidate modules appear in the same commit over 12
   months. This is the single best predictor of whether a boundary is real.
2. **Structural coupling** — cross-module import/call counts, and instability
   `I = Ce / (Ca + Ce)`.
3. **Data ownership** — which modules write which tables. Two writers to one table means the
   boundary does not exist yet.
4. **Transactional span** — how many candidate modules a single database transaction touches.

Record the raw numbers in the `review.v1` `metrics` object. A recommendation without them is an
opinion with a template around it.

## Step 2 — The do-not-split gates

**If any one of these holds, the answer is: do not split.** Not "split carefully" — do not split.
Fix the gate first; then re-run this skill.

| # | Gate | Threshold | Why it is fatal |
|---|---|---|---|
| G1 | No driver from Step 0 with a measurement | — | You would pay every distributed-systems cost for no benefit |
| G2 | Co-change coupling between the candidate and the rest | **≥ 30%** of the candidate's commits also touch the rest, over 12 months | Every feature becomes a two-repo, two-deploy, ordered release |
| G3 | A business invariant must hold atomically across the boundary and the business refuses any convergence window | window = 0 | You would need a distributed transaction; you will instead get silent inconsistency |
| G4 | Both sides write the same table(s) | ≥ 1 shared writable table | A shared database is not a boundary; it is a boundary-shaped decoration |
| G5 | No bounded context backs the boundary — the candidate has no distinct ubiquitous language | — | You are splitting on layers or on nouns, and the seam will move within a year |
| G6 | No single owning team with on-call capacity | owner count ≠ 1 | An unowned service is an outage waiting for a volunteer |
| G7 | The split introduces a synchronous call on a hot path | > 1 added network hop per user request, or fan-out > 5 | Latency and availability both degrade multiplicatively |
| G8 | No distributed tracing, no correlation ids, no per-service SLO, no centralised logs | any missing | The first cross-service bug will be undebuggable |
| G9 | No independent deployment pipeline and no independent database migration path | either missing | You will ship a distributed monolith |
| G10 | Organisation scale below the pain threshold | < ~5 engineers on the system, or < 1 deploy/week | You do not have the problem microservices solve, and you will acquire the problems they cause |
| G11 | The motivation is reuse, language choice or repository size | — | Solved by a library, a sidecar, or a directory, respectively |
| G12 | The candidate has no independent read path — every query joins across the boundary | ≥ 1 join per typical read | You will replace joins with N+1 network calls |

Write the gate evaluation into the ADR as a table, including the gates that passed. A reader in
two years needs to see that G3 was checked, not infer it.

## Step 3 — If no gate fires, still do the cheap thing first

Even when a split is justified, do **not** start with a new repository and a new pipeline.
Do this instead, in order, and stop as soon as the original pain disappears:

1. **Modular monolith.** Move the code behind an explicit in-process port. One package, one
   public interface, everything else package-private.
2. **Add a fitness function** that fails the build on a boundary violation. Without this the
   boundary erodes in weeks:
   ```bash
   # forbid inbound imports into the module's internals
   grep -rn --include=*.java -E "import com\.acme\.orders\.internal\." src/main/java \
     | grep -v "^src/main/java/com/acme/orders/" && exit 1 || exit 0
   ```
   Prefer a real rule engine where one exists (ArchUnit for JVM,
   `eslint-plugin-boundaries` for TS, `import-linter` for Python) — the grep is the fallback.
3. **Split the data ownership before the process.** Give the module its own schema, revoke the
   other modules' write grants, and replace their writes with calls to the port. This is where
   almost all real difficulty lives, and it is fully reversible while still in one process.
4. **Run it for at least one quarter.** Measure co-change again. If G2 now fires, the boundary
   was wrong and you have just saved yourself a distributed rewrite.
5. **Only then extract the process**, using the strangler pattern in
   `references/extraction-playbook.md`.

Most cases stop at step 2 or 3, and that is a success, not a failure of nerve.

## Step 4 — Sizing a boundary that is genuinely separate

If you do split, size it by the invariants and the team, never by lines of code:

- One service = one bounded context, or a coherent subset of one. **Never** two contexts.
- One service = exactly one owning team. A team may own several services; a service may not be
  owned by several teams (Conway's law is a constraint, not an observation).
- The service must be independently deployable **and** independently rollback-able, including its
  database migrations.
- The service must be able to serve its primary read path without a synchronous call to another
  service. If it cannot, the data it needs belongs to it, or the boundary is wrong.
- Cross-service synchronous chain depth ≤ 2. Deeper, and your availability is the product of too
  many nines.

## Step 5 — Record and plan

- `review.v1` to `.foundry/blackboard/<wave>/decompose-service.json`, `dimension: "decomposition"`,
  `verdict: pass` (do not split, keep as is), `pass-with-comments` (modularise in place) or
  `block` (a gate fires and someone is already building the split). Put every measurement in
  `metrics`.
- `adr.v1` via the `write-adr` skill. The options are always at least: *keep and modularise in
  place*, *extract now*, and *extract after the data ownership split*.
- If extracting, `plan.v1` with one wave per stage of `references/extraction-playbook.md` and a
  machine-checkable `gate` on each — for example wave "data-ownership" gates on
  `SELECT grantee FROM information_schema.role_table_grants` returning exactly one writer.
  Use `superpowers:writing-plans` if installed.

## Step 6 — Define the reversal criteria up front

Every split gets a written condition under which it is merged back. Without one, nobody ever
undoes a bad split; they just add a fourth service to work around it. Reasonable conditions:

- co-change between the two services exceeds 30% again three months after extraction;
- more than 20% of changes require an ordered deploy of both;
- p99 of the primary user journey regresses by more than the budget in the ADR.

Put these in the ADR under "Exit path if we are wrong", with the query that measures each.

## Quality gate

- [ ] All four measurements from Step 1 run, with commands and raw output recorded.
- [ ] All twelve gates evaluated explicitly, pass or fail, with the observed number.
- [ ] At least one driver from Step 0 with a measurement, or the recommendation is "do not split".
- [ ] `review.v1.metrics` contains the numbers, not prose.
- [ ] ADR written with ≥ 3 options including "keep and modularise in place".
- [ ] If splitting: fitness function exists **and is in CI** before any extraction work starts.
- [ ] Reversal criteria written with the query that measures each.
- [ ] Artifacts validated with `contract_validate`.

## Progressive disclosure

| File | Load when |
|---|---|
| `references/metrics.md` | running Step 1 — the actual commands and scripts |
| `references/extraction-playbook.md` | a gate-free split was approved and you are sequencing the work |

## What this skill deliberately does not cover

- **Where the boundaries are.** That is `domain-modeler`. This skill evaluates a *candidate*
  boundary; it does not discover one.
- **Integration mechanics of the resulting seam.** Outbox, saga, retries, DLQ:
  `integration-architect`. Wire protocol: `protocol-engineer`.
- **Infrastructure to run more services.** Pipelines, service mesh, autoscaling, cost:
  `foundry-ops` and `foundry-economics`.
- **Database physical design and migration tooling** beyond ownership and write grants.
- **Monorepo vs polyrepo.** A repository layout question, not an architecture question, and
  entirely independent of whether you split the runtime.
- **Serverless/function granularity.** Same gates apply, but the operational model differs enough
  that it needs its own analysis.
- **Organisational change.** This skill will tell you the team topology does not support a split;
  it will not tell you how to reorganise a company.
