---
name: cli-audit-hanoi
description: "Audit the ordering and layering of install/config/build steps using the Tower of Hanoi model: stable-and-expensive at the bottom, volatile-and-cheap on top, no step before its prerequisite, minimal redone work per change, and no responsibility displaced to a higher layer. Applies to Dockerfiles (layer cache, image size), Ansible playbooks and roles (task order, handler restarts, idempotence), Kubernetes manifests (apply order, CRD/RBAC sequencing), Rust workspaces and build systems (crate layering, incremental compile), CI job ordering, and cross-layer stacks. Use when the user says 'hanoi', 'ordre d'install', 'layer order', 'layer caching', 'Dockerfile cache', 'ça rebuild tout', 'build lent', 'image trop grosse', 'restart storm', 'apply order', 'sync waves', 'incremental build', 'reorder steps', 'ordering audit', 'blast radius', or 'displaced responsibility'. Do not use for call-graph cycles (cli-audit-tangle), CI pipeline redesign (cli-forge-pipeline), or benchmarking gains (cli-forge-perf)."
---

# Hanoi Audit

Audit the *order* of operations, not the operations themselves. The same
steps, intelligently stacked, produce something concise, clean, and fast;
badly stacked, they produce rebuild storms, restart loops, and bloat.

Model: a Tower of Hanoi. Each step is a disk. Disk size = stability ×
redo cost. Touching a disk forces every disk above it to be redone.
And in a multi-techno stack, the towers themselves stack: code → build
→ image → orchestrator → config management. A move skipped in a lower
tower reappears in every tower above it.

Read `../gotchas.md` before producing output — the conservation law
applies doubly here: a reorder is only justified by measured rework, never
by aesthetics.

## The Three Laws

1. **Big disk first (stability ordering).** Order steps by change
   frequency and redo cost: stable and expensive at the bottom, volatile
   and cheap on top. Every inversion — a frequently-edited step sitting
   below a costly stable one — taxes each edit with the full stack above.
2. **No move before its prerequisite (topological legality).** A step
   never executes before what it depends on. Crashloop-until-ready and
   "run it twice" are retry-based ordering: a Law 2 violation with a
   costume on.
3. **Count the moves (economy).** Hanoi has a known minimum (2^n - 1).
   Code has one too: one change should redo only itself and what truly
   depends on it. Every extra restart, cache invalidation, re-download,
   or recompile is a wasted move.
4. **Conservation of responsibility (multi-techno displacement).** A
   capability the code does not provide does not disappear — it is
   compensated above, per tool and per environment, with weaker
   guarantees: shell instead of types, retries instead of contracts.
   No config reload in the app → checksum rollouts in kube and restart
   handlers in Ansible. No dependency retry in the app → `wait-for-it`
   in the entrypoint, an initContainer, and an Ansible `until` loop:
   the same missing move, paid three times.

## Workflow

1. **Inventory** ordering-sensitive artifacts under the target path:
   Dockerfile/Containerfile, compose files, Kubernetes manifests
   (kustomize/Helm), Ansible playbooks and roles, CI YAML, build
   definitions (Cargo workspace, Makefile, package.json scripts), and
   long-lived documents. List what was found and what was skipped.
2. **Build each stack.** For each artifact, list steps in execution
   order. Annotate each step with:
   - change frequency — measured, not guessed: `git log --since=6.months
     --name-only` for file-level heat, `git log -L` for line ranges
     inside a Dockerfile or playbook;
   - redo cost — duration, download size, restart impact, image weight.
3. **Detect violations** per law, using `references/domains.md` for the
   canonical stack and anti-patterns of each domain.
4. **Trace displaced responsibilities (multi-techno).** For every
   compensation found in Docker/kube/Ansible — entrypoint `sed`,
   `wait-for-it`, initContainer sleep, `preStop` sleep, probes that grep
   logs, `until` loops around app start — identify the missing
   capability in the layer below using `references/displacement.md`.
   Count how many layers compensate for the same gap: two or more is a
   confirmed finding. Propose the fix at the source, or, when the
   source is out of reach (vendor binary, frozen legacy), consolidation
   into exactly one layer.
5. **Measure blast radius.** For the 2-3 most frequently changed inputs,
   count what gets redone today versus after the proposed reorder. This
   number is the finding; without it, there is no finding.
6. **Propose the reordered stack**: before/after stack diagram, patch
   sketch, expected win (build time, cache-hit rate, image size, restart
   count, first-apply success). Mark semantic risks explicitly — some
   orders encode real constraints; a reorder must be behavior-preserving
   or flagged `NEEDS-REVIEW`. A non-trivial reorder is a hypothesis
   until measured: shape it as an optimization card
   (`../shared/optimization-card.md`) — evidence, invariants, validation
   method, risk, owner.

## Scoring

Score each artifact 0-10 per law:

| Law | What drags the score down |
|---|---|
| Stability | inversions, weighted by change frequency × redo cost above them |
| Legality | prerequisite violations, races, retry-based ordering |
| Economy | wasted moves per typical change: restarts, invalidations, re-downloads, recompiles |
| Displacement (repo-level) | responsibilities compensated above their natural layer, weighted by how many layers pay for the same gap |

Findings carry tier and confidence per `../shared/triage.md` so
`cli-cycle` can aggregate them without re-parsing prose.

Report shape — findings first:

```markdown
## Verdict
[one line per artifact: score triple + the single worst inversion]

## Inversions (ranked by frequency × redo cost)
| # | Artifact | Step out of place | Law | Blast radius today | After reorder |

## Reordered stacks
[before/after diagram + patch sketch per artifact worth fixing]

## Displaced responsibilities
| Missing capability | Natural layer | Compensations found (layer: file) | Fix at source / consolidation |

## Points à vérifier
[semantic risks, unmeasured costs, NEEDS-REVIEW]
```

Rank fixes by gain ÷ effort. If the blast radius barely moves, say so and
recommend leaving the file alone — churn is a cost, not a deliverable.

## The Signature Inversion

The most common finding across all domains is the same disk misplaced:
**a small volatile piece at the bottom of the tower.**

- Docker: `COPY . .` before dependency install.
- Rust: a daily-edited `utils` crate every other crate depends on.
- Ansible: an inline restart after each config file instead of one
  notified handler.
- Kubernetes: a ConfigMap applied after the workload that mounts it.
- Text: the conclusion the reader needs, buried on page four.
- Multi-techno: the same wait-for-db in `entrypoint.sh`, an
  initContainer, and an Ansible `until` loop — one missing retry in
  code, paid three times.

Name it when you see it — the pattern transfers across domains, and the
fix is always the same: move the volatile piece up, or split it so the
stable part can sink.

## Read References On Demand

- `references/domains.md` — canonical stacks, anti-patterns, and quick
  checks per domain: container images, Ansible, Kubernetes, Rust/build
  systems, CI, text.
- `references/displacement.md` — the cross-layer catalog: missing
  capability in code → compensations you will find in Docker, kube.yml,
  and Ansible → fix at source, plus what is legitimate platform work
  and must not be flagged.

## Relationship With Other cli-* Skills

| Situation | Better handoff |
|---|---|
| Call-graph cycles, god functions, dead code | `cli-audit-tangle` |
| Full CI/CD pipeline redesign | `cli-forge-pipeline` |
| Benchmarking the claimed speed-up | `cli-forge-perf` |
| Migrating the deployment itself | `cli-forge-oci-rootless`, `cli-forge-infra` |
| Ordering information in an outbound message | `cli-forge-plume` |
| Run under the full project review | `cli-cycle` — emit `.claude/cli-audit-hanoi.json` per `../shared/result-schema.md` for orchestrator aggregation |

Recommend, do not auto-run.

## Guardrails

- Measured rework is the only force that justifies a reorder. No
  "cleaner", no "best practice", no reordering files the user did not
  put in scope.
- Never propose a reorder that changes behavior silently: config written
  before its package exists, tasks whose order encodes a state timeline,
  K8s resources with real readiness dependencies. Verify or flag.
- Respect existing conventions (file names, YAML style, task naming) —
  this audit moves steps, it does not restyle them.
- If git history is unavailable, say the frequency column is estimated
  and lower confidence accordingly.
