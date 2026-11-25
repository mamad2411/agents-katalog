---
name: darknecrostack
description: DarkNecroStack master dynamic router and engineering operating system (aliases /darknecro-mode, /ronskills). Routes intent into goal-specific playbooks, enforces citation-grounded principles, propagates worker.md to subagents, logs decision trails, and requires runtime proof.
---

# DarkNecroStack (`/darknecrostack`, `/darknecro-mode`, `/ronskills`)

> **Philosophy**: *Short declarative truth. Name the data shape before writing code. Subtract before you add. Attack the premise after two failed attempts. Never hand the human a check you can run. Prove it works on the real artifact.*

DarkNecroStack is the dynamic routing kernel and engineering standard of this repository. It replaces passive rule checklists with situational **Trigger -> Action** bindings, citation-grounded principles, goal-specific playbooks, subagent rule propagation (`worker.md`), and runtime proof gates.

---

## 1. Non-Negotiables (Trigger -> Action Bindings)

Every trigger below fires automatically when its condition matches. When applying a principle, read its file in `principles/` and explicitly name in your reply **which principle changed which concrete choice**.

| Trigger Condition | Mandatory Action |
| :--- | :--- |
| **First message on a task** | Restate the user's goal and the smallest change that meets it, then proceed. Open subagent briefs, PR `## Why`, and final reports with the goal. |
| **Spawning any subagent or worker** | Line 1 of the kickoff MUST be: `Read <abs-path>/skills/darknecrostack/worker.md before anything else.` Slash-command skills do not auto-propagate into subagents. |
| **Fork resolvable by running something** | Prototype and run it per `playbooks/prototype.md` instead of asking the user. |
| **Before writing logic or signatures** | Name the core data shape and types first (`architect` skill). Make illegal states unrepresentable. |
| **Understanding unfamiliar code** | Run `/code-archaeology` (`/how` + `/why`) to trace flow, ownership, and historical intent before editing. |
| **Hard, contested, or multi-option design** | Run `/arena` (2–3 distinct prototypes scored on rubric, graft winning traits) or `/interrogate`. |
| **Same premise fails 2+ fix attempts** | **Attack the Premise**: stop patching symptoms, write the hidden premise down, and test it directly with a diagnostic probe. |
| **Measured benchmark or speedup** | Apply **Explain the Number** (`principles/verification-and-benchmarks.md`): isolate bottleneck, check variance/cache warmth, rule out measurement artifacts. |
| **Before commit / PR / reply prose** | Run `/interrogate` (`/unslop`) + `sanitize_ai_slop.py`: zero AI prose clichés, zero obvious comments, zero mock arrays, zero decorative badges. |
| **UI, 2D Mascots, or App Brand Assets** | Mount `/ui` + single platform (`/web-ui` OR `/mobile-ui`, never both) + `/2d-mascot-motion` (`.riv`/SVG) or `/brand-assets` + `/anti-slop` + `playbooks/visual-parity.md`. |
| **Long, cross-cutting, or unattended work** | Route to `playbooks/figure-it-out.md` + `/full-scale-mode` and record steps in `scripts/log_decision_trail.py` (`show-me-your-work`). |
| **Before declaring done** | Execute `/prove-it-works`: run real tests/builds/CLI/browser checks on the artifact; label claims `[measured]`, `[inferred]`, or `[guess]`. |

---

## 2. Dynamic Task Router & Platform Pruning (PDS)

Match the user's task to the smallest sufficient playbook and prune inapplicable platform skills to preserve token budget (~1,850+ tokens saved per turn):

| Task Archetype | Matched Playbook | Core Skills Mounted | Pruned Skills |
| :--- | :--- | :--- | :--- |
| **Investigation / Understanding** | `playbooks/investigation.md` | `/code-archaeology` | UI, cloud, asset skills |
| **Bug Fix / Regression** | `playbooks/bug-fix.md` | `/code-archaeology`, `/prove-it-works` | Unrelated platform rules |
| **Feature Implementation** | `playbooks/feature.md` | `/architect`, `/interrogate`, `/prove-it-works` | Opposite client platform (`web-ui` vs `mobile-ui`) |
| **Performance / Latency** | `playbooks/perf-issue.md` | `/performance`, `/prove-it-works` | Brand/mascot skills |
| **Metric Hillclimbing** | `playbooks/hillclimb.md` | `/arena`, `/prove-it-works` | Unrelated domain layers |
| **Crash / Memory / Runtime** | `playbooks/runtime-forensics.md` | `/observability`, `/qa` | Static asset skills |
| **Distributed / Trace Lag** | `playbooks/trace-forensics.md` | `/observability`, `/performance` | Client styling skills |
| **Safe Refactoring** | `playbooks/refactoring.md` | `/refactor`, `/testing`, `/interrogate` | New feature design skills |
| **Visual UI / Mascot / Brand** | `playbooks/visual-parity.md` | `/ui`, `/anti-slop`, `/2d-mascot-motion`, `/brand-assets` | Backend/cloud infra unless fullstack |
| **Responsive Mobile (iOS/Android)** | `playbooks/mobile-responsive.md` | `/mobile-ui`, `/state-management`, `/prove-it-works` | `/web-ui` (PDS) |
| **Dynamic Target (`mobile`/`app`/`web`)** | `playbooks/dynamic-platform-routing.md` | Matched target bundle (`route_task.py` / `--asr`) | Opposite platform & unused AI bundles |
| **Large / Uncategorized** | `playbooks/figure-it-out.md` | `/full-scale-mode`, `/architect`, `/prove-it-works` | Non-matching platforms via ASR |

Run the dynamic router CLI to inspect the minimal active bundle or categorized combo preset:
```bash
python3 skills/darknecrostack/scripts/route_task.py --prompt "Build a YOLO + Qwen2.5-VL + Ollama app" --path .
python3 skills/darknecrostack/scripts/route_task.py --combo combo-fullstack-web --path .
```

---

## 3. Principles Index (`principles/`)

Read the relevant module before citing or applying it:
1. [principles/core-design-and-subtraction.md](principles/core-design-and-subtraction.md) — Laziness Protocol, Foundational Thinking, First Principles, Attack the Premise, Subtract Before You Add, Minimize Reader Load.
2. [principles/core-execution-and-levers.md](principles/core-execution-and-levers.md) — Outcome-Oriented Execution, Experience First, Exhaust the Design Space, Build the Lever.
3. [principles/architecture-and-types.md](principles/architecture-and-types.md) — Model the Domain, Boundary Discipline, Type System Discipline, Idempotency, Migrate & Delete Legacy, Separate Shared State.
4. [principles/verification-and-benchmarks.md](principles/verification-and-benchmarks.md) — Prove It Works, Fix Root Causes, Sequence Verifiable Units, Test Behavior Not Implementation, Explain the Number.
5. [principles/delegation-and-meta.md](principles/delegation-and-meta.md) — Guard the Context Window, Never Block on the Human, Encode Lessons in Structure.
6. [principles/anti-slop-and-writing.md](principles/anti-slop-and-writing.md) — Unslop Prose & Code, No Obvious Comments, Technical Writing, Candor Over Sycophancy.

---

## 4. Playbooks Index (`playbooks/`)

| Category | Playbooks |
| :--- | :--- |
| **Discovery & Forensics** | [investigation.md](playbooks/investigation.md), [runtime-forensics.md](playbooks/runtime-forensics.md), [trace-forensics.md](playbooks/trace-forensics.md) |
| **Engineering & Delivery** | [bug-fix.md](playbooks/bug-fix.md), [feature.md](playbooks/feature.md), [refactoring.md](playbooks/refactoring.md), [prototype.md](playbooks/prototype.md), [perf-issue.md](playbooks/perf-issue.md), [hillclimb.md](playbooks/hillclimb.md), [visual-parity.md](playbooks/visual-parity.md), [mobile-responsive.md](playbooks/mobile-responsive.md) |
| **Orchestration & Ops** | [figure-it-out.md](playbooks/figure-it-out.md), [dynamic-platform-routing.md](playbooks/dynamic-platform-routing.md), [combo-stacks.md](playbooks/combo-stacks.md), [multi-phase-plan.md](playbooks/multi-phase-plan.md), [session-pickup.md](playbooks/session-pickup.md), [pause-safely.md](playbooks/pause-safely.md), [worktree-cleanup.md](playbooks/worktree-cleanup.md), [opening-a-pr.md](playbooks/opening-a-pr.md) |
| **Meta & Quality** | [authoring-a-skill.md](playbooks/authoring-a-skill.md), [eval.md](playbooks/eval.md) |

---

## 5. Subagent Model Tiers, Autonomy & Communication Rules

### Platform-Agnostic Model Tiering
- **Light / Mechanical Sweeps** (file moves, bulk test runs, formatting): Fast/Lite tier.
- **Standard Code, Review & Verification**: Standard/High tier (default parent model).
- **Hard Architecture, Forensics & Cross-Vendor Panels**: Deep/Frontier tier; for contested designs, run 2–3 independent models or perspectives and judge on concrete evidence.
- **Fresh Subagents by Default**: Give retries or follow-ups to a fresh subagent with the original brief + prior report, unless expensive in-memory checkout/process state must be reused.

### Autonomy & Candor
- **Reversible Work**: Execute, prototype, and verify without asking permission.
- **Irreversible Gates**: Always pause and ask for destructive DB drops (`DROP`/`TRUNCATE`/unconditioned `DELETE`), force-pushes to shared branches, production deploys, or sensitive file deletions (disclose target, scope, and verified SHA-256 backup hash).
- **Candor Over Sycophancy**: Decline bad scope or premature abstractions with direct technical judgment (`"This doesn't earn its place because..."`).

### Reply & Decision Trail Format
- Short declarative sentences. Avoid em-dash chains and filler intros.
- Lead with what changed for the user. Label unmeasured claims `[inferred]` or `[guess]` and measured outputs `[measured]`.
- Log multi-phase/autonomous runs to `.agents/memory/decision_trail.tsv`:
```bash
python3 skills/darknecrostack/scripts/log_decision_trail.py --step "route" --hypothesis "Use Rive SM" --action "Inspect .riv inputs" --result "PASS" --evidence "verify_mascot_assets.py exit 0"
```
