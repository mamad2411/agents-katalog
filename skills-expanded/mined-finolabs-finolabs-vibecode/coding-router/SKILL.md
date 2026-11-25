---
name: coding-router
description: Route coding work by depth (MIN, NORMAL, DEEP), gates, proof and workflow (Spec Kit, another pack, none) before substantive edits. Use when starting, resuming or redirecting a feature, fix or refactor, brainstorming code before building, before a Spec Kit story skips speckit-tasks, or when fixes fail on one invariant.
---

# Coding router

The entry point for coding work in any repository. It sets the depth, the gates and the proof the work needs, and picks the workflow path that carries it: Spec Kit, another workflow skill pack, or none, which has a procedure of its own. The other skills in this plugin own the details it points to. Work that is not code but carries comparable risk (queries on live data, infrastructure configuration, dashboards and reports, predictions and forecasts) reads [references/non-code-work.md](references/non-code-work.md) beside this skill.
**Advisory (agent judgment):** When the coordinator starts work on a task in a session the user started by hand, run `python3 -I <this skill folder>/scripts/record.py task --id <id>`; the script validates the task id.

## 1. Inspect before acting

Read the goal and acceptance criteria, the scoped instructions (`AGENTS.md`, `CLAUDE.md`, a constitution), ownership and the current diff, accepted artifacts and decisions, open failures and findings, and the proof already gathered. Expose conflicts between sources; a newer source does not win by being newer. A missing source pauses only the work that depends on it.
Keep a short receipt: source, task, workflow path, depth, gaps, evidence limits. A receipt is a record, not proof.
Once the task is known, name or rename the session in the title format the session-start rules give (`tidy` "Titles" when they are not in context), and again when the phase changes (planning to implementation to review). Advisory (agent judgment).

Done when the workflow path and the depth can be chosen without guessing.

## 2. Pick the workflow path

Pick the path here, before loading or invoking any generic process skill, including one that another skill asks for. Check what the repository and this session actually provide (the skill files, not only a folder name), then read the one adapter that fits, in this order:

| First match | Adapter |
| --- | --- |
| The repository uses Spec Kit | [speckit.md](references/workflows/speckit.md) |
| The repository's or the user's scoped instructions adopt a workflow pack, or the pack is installed for this repository: mattpocock/skills | [mattpocock.md](references/workflows/mattpocock.md) |
| The same, for obra/superpowers | [superpowers.md](references/workflows/superpowers.md) |
| Nothing above | [none.md](references/workflows/none.md) |

A pack installed only for the user, with no instruction adopting it, supplies tools, not a workflow: follow none.md and let its tools carry the steps they fit. When two packs qualify and nothing chooses between them, ask the user the one question that decides it. Every adapter keeps the depth, gates and proof below; it decides only which skill carries each step. To support another workflow, add `references/workflows/<name>.md` with the same parts (detect, steps, what yields, gaps) and a row here.
A request that is only a review, with no change to make, goes to `review-gate`, plus `security-review-gate` when its triggers hit and `ui-review-gate` when it touches user-facing UI, on every path.
Decide the depth and the next activity yourself by observed fit and the adapter, or ask the user the one question that decides it (advisory, agent judgment).

Done when you can name the workflow path, the phase and the next activity.

## 3. Choose the depth

- **MIN**: a bounded, reversible seam with known consumers and no unexplained failure, blocking finding, or contract, security, privacy, permission, runtime, dependency or migration risk. Work serially: no optional new spec, plan or interview, no implementation children, no broad reruns. Required acceptance, checks and specialist gates still apply. A no-runtime-impact text edit needs its applicable checks, not a new reviewer per edit; text that changes instructions, executable configuration, auth or data is not automatically harmless.
- **NORMAL**: understood behavior and integration.
- **DEEP**: consequential uncertainty, unknown consumers, sensitive boundaries or irreversible effects. Also: logic that combines several calculations whose errors compound, a prediction or forecast, and user input that is itself ambiguous.

Depth sets effort inside the chosen path and decides its optional ceremony, whatever a workflow skill's own trigger says; in a Spec Kit repository it bypasses nothing except through the Spec Kit depth gate. Upgrade before dependent work. Downgrade only future ceremony when evidence allows, never acceptance, gates, findings or failure counters. File count alone does not set depth.
Record the receipt with `python3 -I <this skill's folder>/scripts/record.py router --depth <MIN|NORMAL|DEEP> --trigger <trigger>`. The command only prints the receipt; when the user has turned usage metrics on, the plugin's hook records it with the session. The trigger names what set the depth, one of `none`, `contract`, `security`, `privacy`, `permission`, `migration`, `dependency`, `uncertainty`, `consumers`, `irreversible`, `calculation`, `prediction`, `input`.
When the work goes into a pull request, its body carries the same depth and trigger as one `fnl-router` marker line, written when you open it and updated before merge if the depth changed: [references/pr-marker.md](references/pr-marker.md) gives the format and the `ui=` suffix (enforcer: `merge_check.py`).

Done when the depth and its reason are in the receipt, the command above has run, and a pull request's body carries the marker line.

## 4. Work, then gate
**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged.

These hold on every path:
- A spec or plan asks the user the decisions the user can settle and records the answers as settled decisions with the date; only what the user cannot settle yet stays open, as [references/decisions.md](references/decisions.md) says. Enforcer: agent judgment, advisory.
- A behavior change starts from a genuine red: a test or reproducer that fails for the reason the change addresses. The change is the smallest that turns it green (see "Proportion").
- Invoke `checks` before you report work as done, fixed or passing, and before you accept a delegated run: fresh targeted runs against each acceptance criterion. Advisory (agent judgment).
- Every pull request needs a posted code review and a posted security review before merge (`review-gate` "Pull requests"); `security-review-gate` runs in full when its triggers hit.
- A change that touches user-facing UI (components, pages, templates, styles, design tokens, interface copy) also runs `ui-review-gate` beside both reviews, never instead of them. Advisory (agent judgment).
- Delegation to other agents follows the `delegate` skill. When you hold two or more independent tasks with clear acceptance tests, apply its "Keep or hand off" before you start the first, even if you expect to do them all yourself. Within one task, budget root and children before spawning: MIN has no implementation children (handing a whole task to another agent under `delegate` is a delegation, not a child); otherwise at most two lightweight children, one nesting level and one heavy job at a time, unless a stricter cap applies.
  Independent tasks run in parallel up to the repository's limit in `delegate` (default 3), each under these per-task caps.
- Commits follow `commit-messages`, and so does every branch: creating, syncing, merging and deleting it (`commit-messages` "Branches"). The main checkout stays on the default branch; each branch gets its own worktree (advisory). Versions, tags and changelogs follow `versioning`.
- Long sessions, handovers and titles follow `tidy`.

## Proportion

Build what the acceptance criteria require at the stage the product is at now. Every changed hunk traces to an acceptance criterion; a hunk that does not is removed or justified. Set this limit in the brief and the plan, where it costs nothing, rather than after the work is written.
- **Over-engineering** looks like: an abstraction with one use, options or flags nobody asked for, defensive checks for cases that cannot happen, a compatibility shim with no consumer, an extra layer, retries or fallbacks before a real failure, comments or documents longer than the code, and scale or performance work (optimizing, hardening, load tests) beyond the stage the product has reached. Three similar lines beat a premature abstraction.
- **Over-testing** looks like: tests for unchanged code or plain declarations, mocks around what can be tested directly, and running tests after every edit or running the whole suite. Tests cover new or changed behavior and its traced consumers, with one regression test per fixed defect. Run them at checkpoints (the end of a seam, after a fix); while fixing a failure, rerun only that test, then the targeted set once. The full suite stays the owner's call (`checks`).

## Checkpoint: stop repeated local fixes

After two failed corrections of the same invariant, stop before a third. Also stop when the next fix reaches a third layer; when each fix's targeted test is green while the end-to-end gate stays red; when the proposed fix adds another flag, retry, debounce, timeout or state copy; or when no shared authority, revision or epoch can prove the invariant. Then run the read-only architecture checkpoint in [references/checkpoint.md](references/checkpoint.md).
