---
name: script-over-instruction-decomposition
description: When designing or refactoring a rule, skill, or sub-agent prompt, decompose its procedure into a deterministic script tier and a prose tier — encode every deterministic step as an executable script under scripts/, leave only judgement/branching/gates in prose.
category: Rule-Management
---

# Script Over Instruction Decomposition Skill

> **Skill ID:** `script-over-instruction-decomposition`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Encode the principle: **scripts are more deterministic than instructions.**
Any agent-facing procedure — rule, skill, sub-agent prompt, README,
checklist — is replayed by a probabilistic language model and may drift
in subtle ways. A script is replayed by an interpreter and either
succeeds identically or fails loudly.

This skill operationalizes the decomposition: for any procedure, split
its steps into a **deterministic tier** (becomes a script) and a
**judgement tier** (stays as prose). The script ships inside the host
skill's `scripts/` folder. Prose collapses to invocation + branching +
gates.

## Prerequisites

| Requirement | Minimum |
|---|---|
| Shell | PowerShell 5.1+ OR Bash 4+ OR Python 3.7+ (per host skill's language choice) |
| Edit access | Write access to the host skill / rule directory |

## When to Apply

Apply this skill when:

- Designing a NEW rule or skill that contains multi-step mechanical work.
- Refactoring an EXISTING rule/skill whose prose contains a long bash
  recipe, multi-file mutation sequence, or repeated-across-sessions
  verification pattern.
- Reviewing an agent prompt that hand-codes a deterministic procedure
  the agent could instead invoke via one script call.

Do NOT apply when:

- The procedure is genuinely one-shot exploration / triage requiring
  judgement.
- The procedure is a single shell command (a script is overhead).
- The host artifact is purely conceptual (architecture rationale,
  trade-off discussion).

## Adoption Note — Why the Prose Tier Lives in a Skill, Not a Rule

The judgement / branching / gate tier that survives decomposition must
still be authored *somewhere*. Prefer the **Agent Skills** format
([agentskills.io](https://agentskills.io), Anthropic-originated,
multi-vendor adopted) over a vendor-specific rule file
(`.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, `AGENTS.md`,
`CLAUDE.md`, `.windsurfrules`, etc.):

- Skills are the **open standard**: one `SKILL.md` is consumable by
  every conformant runtime.
- Rules are **vendor-locked**: a `.mdc` rule is invisible to Copilot;
  a `CLAUDE.md` is invisible to Cursor; etc.

So the full preference chain is:

1. **Script** (interpreter-replayed; deterministic).
2. **Skill prose** (LLM-replayed; portable across runtimes).
3. **Rule / instruction file** (LLM-replayed; vendor-locked) — only
   when a vendor-specific surface is genuinely required (e.g.,
   Permanent Operating Reminders that must fire at every boot of a
   specific runtime).

When converting an existing rule into a skill, delegate to
[`rule-to-skill-industrialization`](../rule-to-skill-industrialization/SKILL.md);
that skill in turn delegates back here for the tier-decomposition pass.

## The Determinism Hierarchy

For any agent-facing procedure, classify each step into one tier:

| Tier | Encoding | When to choose |
|---|---|---|
| **A. Script (executable)** | `.ps1` / `.py` / `.bash` under `scripts/` | Deterministic mechanical work — file mutations, deployments, idempotent verifications, byte-level assertions, multi-step orchestrations. |
| **B. Script-invoking prose** | Markdown with a one-liner `python3 scripts/foo.py --bar` | The procedure exists as a script; prose tells the agent which script to run and when. |
| **C. Pure prose** | Markdown checklist or rule | Genuine judgement, branching on user intent, adversarial gates ("ASK BEFORE destructive op"), one-shot exploration / triage. |

When a procedure straddles tiers, split it: mechanics → A; gate → C;
Tier B prose threads them.

## Mandatory Categories (MUST be Tier A)

These categories MUST be encoded as scripts, never as prose recipes:

- **Multi-step file mutations** — write A, edit B, symlink C as one
  atomic operation.
- **Idempotent deployment / installation** — symlink creation, config
  fan-out from a canonical SSOT, mirrored backups.
- **Byte-level / JSON-shape verifications** — assertions like "file
  must JSON-equal target" or "all keys in alphabetical order".
- **Determinism-critical sequences** — operations whose correctness
  depends on exact ordering or exact intermediate state.
- **Repeated-across-sessions recipes** — anything the agent runs
  verbatim more than once across sessions (safety stash patterns,
  pre-commit verifications, environment hydration).

## Appropriate-for-Prose Categories (SHOULD be Tier C)

These SHOULD remain in prose:

- **Decision trees that branch on user intent** — "if user wants X
  then A, if Y then B."
- **Exploration / triage steps that require judgement** — "inspect the
  diff and classify each file by concern."
- **Adversarial / safety gates** — "before any destructive operation,
  ASK the user and WAIT for explicit confirmation."
- **Pedagogical explanations** — flag-by-flag breakdowns of a command,
  rationale for an architectural choice.
- **One-shot bootstrap steps that vary per machine** — the script
  cannot run yet because the script is itself the artefact being
  installed.

## Step-by-Step Procedure

### Step 1 — Identify the Host Artifact

Locate the rule, skill, or sub-agent prompt whose procedure is being
decomposed. Confirm its `scripts/` folder exists (create if not).

### Step 2 — Audit the Procedure for Tiers

Read the procedure top-to-bottom. For each numbered step:

- Mark **A** if it is deterministic mechanical work.
- Mark **C** if it is judgement / branching / gate / explanation.
- Mark **A+C** if it mixes both (will need to be split).

### Step 3 — Extract the Tier-A Core into a Script

Group consecutive Tier-A steps into a single script under
`scripts/<verb-noun>.{ps1|py|bash}`. The script MUST:

- Be **idempotent** — safe to re-run.
- Be **deterministic** — same input → same output.
- Fail **loudly** on unexpected state — never silently skip.
- Take parameters via flags / args, not hard-coded paths.
- Print a one-line summary per side-effect (created, updated, skipped).
- Obey the host project's language mandate (default PowerShell per
  `script-management-rules.md`; Python only with documented
  justification; Bash uses `.bash` extension).

### Step 4 — Trim the Prose to Tier B + C

Replace the extracted Tier-A prose with:

- **One-line invocation** (Tier B) — `python3 scripts/foo.py --bar`.
- **Preserved Tier C** — judgement, branching, gates, explanations.
- **Optional fallback** — the original manual recipe, labelled
  "Bootstrap / Audit / Rollback Fallback", referencing the script as
  the canonical path.

### Step 5 — Verify Script Independence

Confirm the script runs end-to-end on a fresh checkout with only the
prerequisites listed in the host skill. No reliance on agent state.

### Step 6 — Commit Atomically

Per
[`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md),
the extraction is one atomic commit. Message pattern:

```text
refactor(<host-skill>): extract <verb-noun> into scripts/<file>

Tier-A core of <procedure> was previously prose; replayed
non-deterministically per session. Extracting into an idempotent script
makes the procedure replayable and self-verifying. Prose §<N> trimmed
to invocation + fallback-for-audit.
```

## Anti-Patterns to Reject

| Anti-pattern | Why bad |
|---|---|
| Inlining script body inside a fenced code block in `SKILL.md` | Violates No-Embedded-Script Mandate; SSOT duplication. |
| "Run this 5-step bash recipe" with no script equivalent | Agent re-derives the recipe each session; drift inevitable. |
| Splitting one script into "prose + 3-line script" | Tier-A leak into prose. Move all mechanics into the script. |
| Removing the manual fallback entirely | Bootstrap and audit need it; preserve as labelled fallback. |
| Bulk "convert everything" sweep | High churn, low context. Refactor opportunistically per session. |


## Consumer Discipline — Always Invoke, Never Re-derive

The script-first decomposition has TWO sides, and both MUST be honoured for the discipline to deliver determinism:

1. **Authoring side** (covered by `## Mandatory Categories`, `## Step-by-Step Procedure`, and `## Anti-Patterns to Reject` above): extract every Tier-A step into an executable script under `scripts/`.
2. **Consumer side** (this section): when an agent later EXECUTES a skill, it MUST invoke the existing script — not re-derive the Tier-A logic ad-hoc from the surrounding prose.

Re-derivation defeats the purpose of authoring the script. The prose around a script call is Tier-B/C only (judgement, branching, human-gates); the Tier-A mechanics live in `scripts/<x>` and are kept correct THERE.

### Consumer Pre-Flight (Mandatory)

Before executing any deterministic step described in a skill's prose, the consumer agent MUST:

1. **List the skill's scripts directory**:

    ```bash
    ls <skill-dir>/scripts/ 2>/dev/null
    ```

    (Use the in-process `glob` tool with `pattern: "scripts/**"` and `paths: "<skill-dir>"` as a §3 Pattern 2-safe alternative to bash `find`.)

2. **Match the prose step to a script.** Scan filenames + the top docstring/header of each candidate. If the skill's prose says *"register the skill in `agentskills.io/library.json`"*, look for `scripts/register-skill.*`, `scripts/agent-registration.*`, etc.

3. **Read the script's header, then invoke.** Before constructing the invocation, read the script's header/docstring (first 10–20 lines of the file) to understand its CLI contract — flags, positional args, env vars. Scripts document their usage at the top; this is more reliable than probing `--help` (which some scripts redirect through a pager or omit entirely). Only if the header is unclear or absent should you fall back to probing `--help` or `--usage`. The agent's transcript MUST show evidence of understanding the usage (either a header read or a `--help` call) before the real invocation for any script the agent has not read this session.

    **Scope pre-flight by script type.**
    - **Base/independent skill scripts**: SKILL.md documents the exact invocation. Trust the doc; read the script header only if the documented contract is ambiguous.
    - **Composer dependency scripts**: The dependency skill may evolve independently. Before invoking a dependency script you haven't read this session, read its header to catch any contract changes.

4. **Fall through to manual recipe only if NO script exists.** If `scripts/` is empty or no script matches the step, the prose recipe is the authoritative fallback (Tier B / C). Do NOT skip the pre-flight just because manual recipes are familiar.

### Forbidden Consumer Patterns

| Anti-pattern | Why bad |
|---|---|
| Re-typing a multi-step bash recipe inline when `scripts/<x>.sh` encodes the same recipe | Drift between consumer invocations and the script's evolving canonical form; the script's edge-case handling is bypassed. |
| Re-typing a Python loop / parser inline when `scripts/<x>.py` already does it | Same drift risk; parsing edge cases (encoding, BOM, line-ending) the script handles get reintroduced as bugs. |
| Reading the prose for "the algorithm" when a script encodes it | Prose around a Tier-A step is intentionally not the algorithm — it's the rationale + Tier-B branching. The algorithm is the script. |
| Skipping the `ls scripts/` pre-flight because the agent "remembers from a previous session that there's no script" | Skills evolve; scripts get added between sessions. Always probe fresh. |

### Verification

When reporting a skill execution done, the agent's tool transcript MUST show at least one invocation of each Tier-A step's owning script (or an explicit note that no script exists for that step and the manual fallback was used). If the transcript shows only inline bash/Python re-deriving the logic, the §3 (Mandatory Categories) contract has been violated at consumer time even if the authoring side was correct.

### Historical Example — Skill-Factory Agent Registration

The [`skill-factory`](../skill-factory/SKILL.md) skill ships dedicated registration scripts under `scripts/` for the agent-registration step (adding the new skill to the agent's discoverable index). An earlier consumer session executed the registration step by re-typing the registration commands inline from the prose rather than invoking the script — even though the prose explicitly pointed at the script. The output was correct but bypassed the script's idempotency check, env-var validation, and SSOT updates. The fix was free if the pre-flight (`ls .agents/skills/skill-factory/scripts/`) had been run before executing the step.

(Persisted as `permanent_discipline.consumer-always-invoke-never-rederive`.)

## Worked Example — MCP Consumer Symlink Deployment

The
[`mcp-cross-tool-config-sync`](../mcp-cross-tool-config-sync/SKILL.md)
skill originally documented its Phase 5 "Symlink Distribution" as a
five-step bash recipe (verify backup → `rm` → `ln -s` → verify →
`diff`). Each invocation rehydrated those steps from prose and ran them
per tool — error-prone, drift-prone, verbose.

The script-first refactor moved the entire deterministic core into
`scripts/generate-configs.py`:

- `deploy_symlink(link, target)` — idempotent, relative-path, skips
  silently when the consumer's parent dir is absent.
- `DEPLOY_TARGETS` map — single registration point for new tools.
- `--no-deploy` flag — generation-only mode for CI / dry-run.

Skill §9 prose was trimmed to "run the script; here's the fallback
manual pattern for bootstrap and audit." Adding a new tool means
appending one entry to a Python dict — no prose edit required.

See the upstream commit (`ai-suite-2` `c190f39`) and downstream sync
(`<private-config-repo>` `27f0e6e`) for the canonical refactor.

## Cross-References

- **[Script Management Rules](../../../ai-agent-rules/script-management-rules.md)** —
  canonical SSOT for script craftsmanship (headers, language priority,
  `Common-Utils.ps1` dot-sourcing).
- **[Scripting Language Selection Rules](../../../ai-agent-rules/scripting-language-selection-rules.md)** —
  PowerShell vs Bash vs Python decision matrix.
- **[Bash Scripting Rules](../../../ai-agent-rules/bash-scripting-rules.md)** —
  Bash-specific craftsmanship (`.bash` extension, shebang,
  `set -euo pipefail`).
- **[AI Rule Standardization Rules §4](../../../ai-agent-rules/ai-rule-standardization-rules.md)** —
  Script SSOT Mandate and No-Embedded-Script Mandate.
- **[Git Atomic Commit Construction](../git-atomic-commit-construction/SKILL.md)** —
  per-extraction commit discipline.
- **[Skill Factory](../skill-factory/SKILL.md)** — invokes this skill
  during §2.2.1 Tier Decomposition Mandate for every newly drafted
  skill.
- **[Rule to Skill Industrialization](../rule-to-skill-industrialization/SKILL.md)** —
  invokes this skill during Phase 4 to push deterministic recipes out
  of the blended prose and into scripts.

## Related Skills

- [`skill-cross-reference-audit`](../general/skill-cross-reference-audit/SKILL.md) — automated audit for skill graph issues (duplicates, missing bridges, missing frontmatter)
- [`script-template-extraction`](../script-template-extraction/SKILL.md) — companion base skill for template extraction; run `skill-cross-reference-audit` after extraction to verify the skill graph is clean
- [`skill-factory`](../skill-factory/SKILL.md) — consumes this skill during §2.2.1 Tier Decomposition Mandate for every newly drafted skill

## Traceability

Formalized after a session in which a configurations repository's MCP
consumer symlink (`User/mcp.json`) needed to be made portable across
machines. The refactor moved symlink creation from documented bash
steps into the generator script's `deploy_symlink` function and gated
on `link.parent.exists()` so the script is safe to run on machines
where each consumer is or is not installed.

User principle: *"I prefer script over skill instruction; scripts are
more deterministic than instruction (or its derivatives like rules,
skills, sub-agents, etc.)."* This skill is the operational form of
that principle.
