---
name: cli-forge-quorum
metadata:
  author: clement
description: Generate a Byzantine-fault-tolerant multi-agent orchestration using the REC-Quorum pattern (Reflect/Execute/Control with adaptive quorums, tickets pré-signés, leaderless execute, view-change timeouts). Use when a brigade-style orchestrator has stalled on a single-leader bottleneck, when deterministic decision quality is required (SLA/compliance/incident-response), when the team has > 5 agents with parallelism, or when operators mention 'BFT agents', 'REC-Quorum', 'deterministic consensus', 'threshold signatures', 'quorum adaptatif', 'view-change', 'leaderless execute', 'Byzantine orchestration'. Upgrade path from cli-forge-chef when Brigade stalls or requires formal audit trail.
---

# cli-forge-quorum — REC-Quorum Orchestration (BFT-grade)

Generates a multi-agent orchestration with **Byzantine fault tolerance**, **adaptive quorum sizing** per task criticality, and **view-change timeouts** to eliminate single-leader bottlenecks.

The pattern comes from applying distributed-systems research (PBFT, HotStuff, Mir-BFT, Mercury, BFTBrain) to LLM agent dispatch. Empirically validated by [arxiv 2511.15755](https://arxiv.org/abs/2511.15755) — multi-agent orchestration raises actionable-recommendation rate from 1.7% to 100% with zero variance across 348 trials.

## When to use this skill (triage)

| Situation | Use |
|---|---|
| First multi-agent sprint, 2-5 workers, dev repo | **`cli-forge-chef`** (Brigade pattern, lighter) |
| Brigade stalled 30+ min on leader bottleneck | **`cli-forge-quorum`** (view-change, leaderless) |
| Compliance audit / SLA / incident response | **`cli-forge-quorum`** (signed trail + DQ metric) |
| > 10 parallel agents | **`cli-forge-quorum`** (Mir-BFT-style scaling) |
| Variable criticality (trivial-to-critical tasks mixed) | **`cli-forge-quorum`** (adaptive N) |
| "Just automate my git workflow" | **`cli-forge-chef`** |

**Key test** : if stalling the leader would cost > 1h of wasted sprint time, you need REC-Quorum. If the leader can stall and be manually unblocked in < 15 min, Brigade is enough.

## Architecture — three phases, each gated

```
Phase 0 — Reflect    → plan signé + tickets commis (Chef + 2 Sous-Chefs plan)
Phase 1 — Execute    → leaderless, tickets pré-signés, contre-chef-inter auto-approve
Phase 2 — Control    → f+1 validateurs indépendants signent le résultat
```

Each phase emits a **signed certificate** (hash canonique + signatures). Without the certificate, no transition to the next phase. A failing phase triggers **view-change** (backup takes over) or **escalation** (human in the loop).

### Phase details

Read `references/rec-phases.md` for the complete specification of each phase, including timeouts, hash-canonical voting, and view-change protocol.

### Leaderless Execute — eliminating the Chef bottleneck

Read `references/leaderless-execute.md`. Core idea: at Phase 0, the Chef signs a **ticket** per commis stating "commis-X is authorized to Edit files matching scope S in normal zones". During Execute, the contre-chef-inter validates tickets against edits — no round-trip to the Chef. The Chef sleeps until Phase 2 or escalation.

### Adaptive quorum sizing

Read `references/quorum-sizing.md`. A task classifier maps incoming requests to N:

| Criticality | N | Tolerates | Example |
|---|---|---|---|
| trivial | 1 | nothing | format comment, rename var |
| routine | 3 | 1 crash | standard feature implementation |
| sensitive | 5 | 1 Byzantine | security-adjacent code, dependencies |
| critical | 7 | 2 Byzantine | auth, crypto, financial transactions |

**Cost model**: N=7 → 7× LLM cost. Document this in every sprint plan so operators don't casually pick critical.

## Visualization — Petri Nets / CWN, not PERT

Read `references/petri-cwn-templates.md`. PERT cannot model loops, tokens, or conditional gates — all of which REC-Quorum has. Colored Workflow Nets (van der Aalst) natively model:
- tokens = certificates with signatures (token color = signer set)
- AND-split / AND-join for fan-out quorum
- guarded transitions for k-of-n thresholds
- soundness analysis for free (no deadlock, no dead tasks)

For live dashboards: `bpmn-js` with token simulation plugin, or Renew/WoPeD for formal analysis.

## BFT primitives (pointers, not implementations)

Read `references/bft-primitives.md`. Do not re-implement consensus. Pick from:
- **HotStuff-lite** for leader-based BFT with linear complexity and pipelining
- **Mir-BFT** / **Arma** for multi-leader horizontal scaling
- **Mercury** for low-latency dual-mode BFT (optimistic vs Byzantine path)
- **BFTBrain** if workload varies enough to justify RL-based protocol swapping

For threshold signatures: BLS (short sigs, aggregatable) or Schnorr MuSig2 (more battle-tested).

## Upgrade path from Brigade

Read `references/upgrade-from-brigade.md`. A working `cli-forge-chef` brigade can migrate to REC-Quorum incrementally:

1. Keep the Chef for Phase 0 (planning) only
2. Add tickets pré-signés as part of the Chef's output
3. Split Sous-Chefs into Plan-validators (Phase 0) vs Control-validators (Phase 2)
4. Add the contre-chef-inter (already generated by `cli-forge-chef` at tier ≥ M)
5. Add per-phase timeouts with view-change
6. Migrate shared-state.md to shared-state.jsonl (append-only signed log)

Each step is independently deployable and testable.

## Generation workflow

### Phase 1 — Assess the project

```bash
# Does this project really need REC-Quorum?
# Run the triage decision tree
```

1. Does the workload have > 5 parallel agents? → continue
2. Is decision quality SLA required? → continue
3. Has a Brigade attempt stalled before? → continue
4. Is a threshold-signatures library available in the project language? → continue
5. Can the operator budget 2× LLM cost for a critical sprint? → continue

If any answer is "no" that matters to the use case, **stop** and suggest `cli-forge-chef` instead.

### Phase 2 — Gather inputs

- Project root + branch model (same as cli-forge-chef)
- Criticality classification for each expected task type
- Available primitives (threshold sig lib? consensus lib?)
- Target observability (Petri animation? BPMN dashboard? raw logs only?)
- Compliance needs (audit trail? SOC2? HIPAA?)

### Phase 3 — Generate the artifacts

Produce at minimum:

1. **`{project}/.claude/rec-quorum/orchestrator-{session}.md`** — main orchestrator prompt (replaces Chef role)
2. **`{project}/.claude/rec-quorum/plan-validator-{role}-{session}.md`** — Phase 0 validator prompts (scope, secu)
3. **`{project}/.claude/rec-quorum/control-validator-{role}-{session}.md`** — Phase 2 validator prompts (tests, security, contracts, policy, perf)
4. **`{project}/.claude/rec-quorum/apply-pane-{session}.md`** — apply pane prompt (Phase 2 mutations coordinator, see `references/apply-quorum-rec-q.md`)
5. **`{project}/.claude/rec-quorum/ticket-template.json`** — canonical ticket schema
6. **`{project}/.claude/rec-quorum/shared-state.jsonl`** — bootstrap the append-only log
7. **`{project}/.claude/rec-quorum/certificates/.gitkeep`** — directory for Phase-transition signed certificates (Q8)
8. **`{project}/.claude/rec-quorum/plans/.gitkeep`** — directory for apply plan artefacts (apply-quorum)
9. **`~/.config/tmuxinator/{session}.yml`** — windows for orchestrator + plan-validators + control-validators + apply pane + commis + ccheck + contre-chef-inter
10. **`{project}/.claude/rec-quorum/petri-net.cpn` or `.bpmn`** — workflow model for the sprint
11. **`{project}/.claude/settings.local.json`** — root permissions (see Reused artefacts below)
12. **`{project}/scripts/brigade-setup-worktrees.sh`** — idempotent worktree + per-pane permissions setup (reused from `cli-forge-chef/references/brigade-setup-worktrees.sh`, extended for REC-Q's role list)

### Reused artefacts (imported from `cli-forge-chef`)

Do not re-invent these. Import the chef versions verbatim and, where needed, extend:

| Artefact (chef source) | REC-Q use |
|---|---|
| `cli-forge-chef/references/ccheck-prompt-template.md` | Mandatory ccheck window (G24) |
| `cli-forge-chef/references/contre-chef-inter-prompt-template.md` | Phase 1 ticket verifier (see `references/leaderless-execute.md`) |
| `cli-forge-chef/references/tmuxinator-template.md` | Base structure — uses `--append-system-prompt-file` (G34-safe), no wrapper script, `brigade-setup-worktrees.sh` in `on_project_start` |
| `cli-forge-chef/references/brigade-setup-worktrees.sh` | Idempotent setup, no SIGPIPE (G35), one branch per agent (G36) |
| `cli-forge-chef/references/permissions-template.md` | Per-worktree `settings.local.json` for standalone panes (gate, apply, maitre). Teammates inherit the root (G32) — so the root `settings.local.json` must carry the strictest deny list |
| `cli-forge-chef/references/maitre-dhotel.md` | Post-merge watchdog, unchanged |
| `cli-forge-chef/references/gotchas-chef.md` | Base gotchas — read alongside `references/gotchas-quorum.md` |
| `cli-forge-chef/references/apply-quorum.md` | Lighter apply protocol for dev sprints; REC-Q uses `references/apply-quorum-rec-q.md` instead |

**Never generate `scripts/brigade-launch-agent.sh`** — it's the obsolete wrapper superseded by `--append-system-prompt-file` (see `references/anti-patterns.md` §22).

### Phase 4 — Hard gates before launch

Before running `tmuxinator start {session}`:

1. **Petri net soundness**: run a soundness check (Renew, WoPeD, or a custom reachability check). If the net has deadlocks or dead transitions, **stop**. (`gotchas-quorum.md` Q10)
2. **Ticket schema valid**: validate `ticket-template.json` against JSON Schema.
3. **N validators spawned**: count Agent blocks in orchestrator prompt. Must equal `floor(N/2) + 1` at minimum for Control, 2 for Plan.
4. **Timeouts set**: every phase must have a timeout. Missing timeout = guaranteed stall. (`anti-patterns.md` §11)
5. **Contre-chef-inter present**: inherit from `cli-forge-chef` §2.6b — mandatory at tier ≥ M.
6. **Cost estimate printed**: LLM calls × N = predicted cost. Operator must confirm. (`anti-patterns.md` §17)
7. **Native flag used, no wrapper script**: `! grep -q '\$(cat ' ~/.config/tmuxinator/{session}.yml` AND `! test -f {project}/scripts/brigade-launch-agent.sh` AND `grep -qc 'append-system-prompt-file' ~/.config/tmuxinator/{session}.yml`. Reject legacy wrapper generation. (`anti-patterns.md` §18, §22)
8. **Setup script executable and idempotent**: `test -x {project}/scripts/brigade-setup-worktrees.sh` AND `! grep -q 'pipefail' $_` AND `! grep -q 'worktree add.*| head' ~/.config/tmuxinator/{session}.yml`. (`anti-patterns.md` §19)
9. **One branch per agent worktree**: `git branch --list 'wt/*' | wc -l` equals the count of non-commis agent panes; `{base_branch}-{commis_name}` branches exist for each commis. (`anti-patterns.md` §20)
10. **Trust prompt auto-accept scheduled**: `grep -q 'Down Enter' ~/.config/tmuxinator/{session}.yml` AND the line contains `&` so it doesn't block on sleep. (`anti-patterns.md` §21)
11. **Root settings.local.json denies destructive Bash**: `grep -c 'Bash(tofu apply\|Bash(helm upgrade\|Bash(kubectl apply\|Bash(gh release\|Bash(git push --force' {project}/.claude/settings.local.json | (read n; [[ $n -ge 5 ]])`. Teammates inherit the root — strict deny list here is the only line of defence. (`gotchas-quorum.md` Q4)
12. **Apply pane permissions allow infra tools, deny push**: `test -f {project}-wt-apply/.claude/settings.local.json` AND it allows `tofu:*` / `helm:*` / `kubectl:*` AND denies `git push:*` / `git commit:*`. (`apply-quorum-rec-q.md`)
13. **Phase-transition certificate dirs present**: `test -d {project}/.claude/rec-quorum/certificates/` AND `test -d {project}/.claude/rec-quorum/plans/`. (`gotchas-quorum.md` Q8)
14. **Orchestrator prompt strips Brigade classification logic**: `! grep -iE 'classify|decide.*zone|check.*sensitive' {project}/.claude/rec-quorum/orchestrator-{session}.md` in the Phase 1 section. (`gotchas-quorum.md` Q7, `anti-patterns.md` §10)
15. **Control validators are distinct**: diff each pair of `control-validator-*.md` prompts — any two literally identical up to `{role}` substitution fails the gate. (`gotchas-quorum.md` Q6, `anti-patterns.md` §15)

If any gate fails, do NOT proceed. Fix generation first.

## Reference index

| File | Content |
|---|---|
| `references/rec-phases.md` | Phase 0 / 1 / 2 specs with timeouts, hash-canonical voting, view-change |
| `references/leaderless-execute.md` | Tickets pré-signés, contre-chef-inter as verifier, budget enforcement |
| `references/quorum-sizing.md` | Criticality classifier, N mapping, cost model, heterogeneous quorums |
| `references/bft-primitives.md` | Pointers to HotStuff-lite, Mir-BFT, Mercury, BFTBrain, threshold sigs |
| `references/petri-cwn-templates.md` | Workflow modelling with Petri / Colored Workflow Nets, soundness analysis |
| `references/upgrade-from-brigade.md` | Six incremental migration steps from `cli-forge-chef` |
| `references/apply-quorum-rec-q.md` | Phase 2 apply quorum for `tofu apply` / `helm upgrade` / `kubectl apply` / `gh release create` / feature-branch force-push |
| `references/gotchas-quorum.md` | REC-Q-specific gotchas Q1-Q10, plus cross-reference map to `cli-forge-chef/references/gotchas-chef.md` G1-G38 |
| `references/anti-patterns.md` | 22 patterns to refuse (architecture + launch-time bugs) |

## Anti-patterns to refuse

Read `references/anti-patterns.md`. Never generate:

- **Same quorum for all tasks** — trivial tasks at N=5 waste 5× cost; critical at N=1 = no safety
- **Majority vote on free text** — two agents write "looks good" with different wording; nothing reproducible. Always hash canonical form first
- **Reflect + Execute fused** — "the planner also executes" loses the planning gate, reintroduces leader bottleneck
- **No Control phase** ("ça marche en dev") — this is the phase that produces the audit trail; skipping it breaks compliance
- **Per-operation threshold sigs with 7 signers on every Edit** — overhead explodes, cache invalidation every write; batch at phase boundaries only
- **Human-in-the-loop as default** — REC-Q should auto-resolve > 98% of cases; humans only for attested escalations

## Relationship to cli-forge-chef

`cli-forge-chef` remains the right tool for dev workflows. `cli-forge-quorum` is a **higher-rigor, higher-cost** pattern for when Brigade is insufficient. The two skills share several templates:

- `contre-chef-inter-prompt-template.md` (lives in `cli-forge-chef/references/`, reused here)
- `tmuxinator-template.md` (base structure, adapted for N validators)
- `shared-state` concept (extended to `.jsonl` append-only in REC-Q)

`cli-forge-quorum` imports these via path references, not duplication. See `references/upgrade-from-brigade.md` for the exact reuse map.

## Cost honesty section

Before generating, print to the operator:

```
REC-Quorum cost estimate for this sprint:
  Task mix:     T trivial, R routine, S sensitive, C critical
  Quorum sizes: 1×T + 3×R + 5×S + 7×C agent-calls per task
  Base cost:    $X at N=1 (Brigade equivalent)
  REC-Q cost:   $Y (about 2-3× for a typical dev sprint)
  Cost rationale: a Brigade sprint stalled for 45 min wastes > $Y anyway.
  Ship anyway? [y/N]
```

Do not hide the cost. Operators who pay 2-3× and still choose REC-Q do so because stall-recovery is worth more.

## Completion criteria

A generation is "done" when:
- All hard gates pass
- Operator confirmed the cost estimate
- Petri net is sound
- One end-to-end test task flows through Phase 0 → 1 → 2 and produces a signed certificate
- `tmuxinator doctor` reports clean
