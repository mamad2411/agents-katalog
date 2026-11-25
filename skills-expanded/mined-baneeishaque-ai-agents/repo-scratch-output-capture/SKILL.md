---
name: repo-scratch-output-capture
description: Redirect stdout and stderr of probes, builds, installs, and any long-running diagnostic command into a repo-root `scratch/` folder (gitignored) instead of suppressing output or writing to `/tmp`. Keeps the terminal clean while preserving complete, inspectable output co-located with the artifact under investigation.
category: Code Hygiene & Maintenance
---

# Repo Scratch Output Capture Skill (v1)

> **Skill ID:** `repo-scratch-output-capture`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base

## 1. When to Apply

Apply this skill whenever a command's output is too verbose for the terminal but MUST be
preserved for inspection (success verdict, failure trace, install log, probe result). Specifically:

- Capability probes (DB version, network reach, schema introspection).
- Package installers (`pip`, `npm`, `cargo`, `apt`, `brew`).
- Long builds whose interesting signal is the last 20 lines.
- Any command that runs unattended and may fail silently.

Do NOT apply for:

- Commands whose output is itself the deliverable (those go to the user directly).
- One-line commands whose output already fits the terminal.

## 2. Core Doctrine

| Forbidden | Required |
| --- | --- |
| `cmd > /dev/null 2>&1` (silent failure invisible) | `cmd > scratch/cmd.out 2> scratch/cmd.err` |
| `cmd > /tmp/x.log` (lost on reboot, not co-located with the artifact) | `cmd > <repo-root>/scratch/x.out` |
| Writing to the CWD's containing repo when the artifact lives in another repo | Resolve `<artifact-repo-root>/scratch/` first; write there |
| Adding `scratch/` only to `.git/info/exclude` (local-only) | Add `scratch/` to committed `.gitignore` (team-wide) |

**Rationale:** A suppressed failure is a debugging time-bomb. `/tmp` divorces the trace from the
artifact. `scratch/` next to the artifact is discoverable by every contributor and survives
reboots while staying out of version control.

## 3. Naming & Layout

Artifacts are organized **per-session** under a scratch root that is
gitignored. The session folder is named by the current opencode session ID
(`ses_` prefix omitted), e.g. `scratch/<session-id>/`:

```text
<repo-root>/
├── .gitignore              # contains line: scratch/
└── scratch/                # gitignored
    └── <session-id>/        # ses_ prefix omitted (e.g. <session-id>)
        ├── <purpose>_<ts>.out      # captured stdout
        ├── <purpose>_<ts>.err      # captured stderr
        └── <purpose>_<ref-slug>_<ref-sha>.<ext>  # artifact captured at a git ref
```

- `<purpose>` is a short lowercase-kebab slug describing the command
  (`probe-multi`, `pip-install`, `gradle-build`).
- Always pair `.out` + `.err` siblings — many tools split signal unpredictably
  between the two streams.
- **Naming and session-folder resolution are delegated to the
  [`scratch-artifact-naming`](../general/file/scratch-artifact-naming/SKILL.md)
  base skill** — never re-derive the `<purpose>_<ts>` / `_<ref-slug>_<sha>`
  forms yourself. Run its `resolve-scratch-path.py` and append the extension.
- Sub-folders permitted for multi-step workflows
  (`scratch/<session-id>/<step>.out`).

## 4. Operational Logic

### 4.1 Ensure-and-Capture Pattern

Idempotent one-liner pattern:

```bash
REPO="$(git rev-parse --show-toplevel)"
SCRATCH_ROOT="$REPO/scratch"
mkdir -p "$SCRATCH_ROOT"
grep -qxF 'scratch/' "$REPO/.gitignore" 2>/dev/null \
    || echo 'scratch/' >> "$REPO/.gitignore"

SESSION_DIR="$(python3 "$REPO/.agents/skills/general/file/scratch-artifact-naming/scripts/resolve-scratch-path.py" \
    --repo "$REPO" --purpose my-command | xargs dirname)"

my-command --with --args \
    > "$SESSION_DIR/my-command.out" \
    2> "$SESSION_DIR/my-command.err"
echo "Exit: $?  See $SESSION_DIR/my-command.{out,err}"
```

The **session-dir + naming** part MUST come from
[`scratch-artifact-naming`](../general/file/scratch-artifact-naming/SKILL.md) —
run its `resolve-scratch-path.py` (which also creates the dir) instead of
computing the path by hand. Use the bundled script
[`scripts/ensure-scratch-gitignored.py`](scripts/ensure-scratch-gitignored.py)
to perform the setup and emit the absolute session-scoped scratch path on
stdout:

```bash
REPO="$(git rev-parse --show-toplevel)"
python3 "$REPO/.agents/skills/repo-scratch-output-capture/scripts/ensure-scratch-gitignored.py" >/dev/null
STEM="$(python3 "$REPO/.agents/skills/general/file/scratch-artifact-naming/scripts/resolve-scratch-path.py" \
    --repo "$REPO" --purpose my-command)"
my-command > "$STEM.out" 2> "$STEM.err"
echo "Exit: $?  See $STEM.{out,err}"
```

### 4.2 Inspection Protocol

After the command exits:

1. Check exit code immediately (`echo $?`).
2. If non-zero: `tail -30 scratch/<purpose>.err` first (usually has the failure summary), then `.out`.
3. If zero but result uncertain: `grep <verdict> scratch/<purpose>.out`; check `.err` for warnings.

### 4.3 Cleanup

The `scratch/` folder is ephemeral by design — delete contents freely.
Do NOT commit scratch files. If a captured file is valuable enough to keep, move it to a tracked
location.

For triage of files that accidentally became untracked elsewhere (NOT in `scratch/`), see
[`untracked-scratch-triage`](../untracked-scratch-triage/SKILL.md). That skill DISPOSES of unclear
leftovers; this skill PRODUCES intentional captures — the two are SSOTs for different lifecycle phases.

## 5. Composition

This skill is a base primitive consumed by:

- [`scratch-artifact-naming`](../general/file/scratch-artifact-naming/SKILL.md) —
  **delegate target** for the session folder + naming; this skill composes it
  (via its `resolve-scratch-path.py`) instead of owning the formulas itself.
- [`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md) — probe output goes
  to `scratch/probe-*.out|err`.
- [`mise-tool-management`](../mise-tool-management/SKILL.md) — every `mise install`,
  `mise trust`, and `mise ls` invocation is captured to `scratch/mise-*.{out,err}` so
  deprecation warnings emitted on stderr (e.g., `mise WARN  deprecated [ubi]: …`) are
  not lost to terminal scroll-back.
- Any future probe / installer / build wrapper that needs to keep the terminal clean while preserving
  output for audit.

## 6. Prohibited Behaviors

- Writing scratch output to `/tmp/` (loss-on-reboot, no co-location).
- Suppressing stderr with `2>/dev/null` for any command whose failure matters.
- Committing files under `scratch/`.
- Putting `scratch/` in `.git/info/exclude` only (team members hit the same problem next session).
- Reusing `scratch/` as a build-output cache (use `target/`, `build/`, `dist/` for those).

## 7. Cross-References

- Anti-overlap: [`untracked-scratch-triage`](../untracked-scratch-triage/SKILL.md) — disposal of
  unclear untracked files (this skill produces intentional captures).
- Companion: [`gitignore-rules`](../gitignore-rules/SKILL.md) — for authoring the ignore entry
  correctly across nested repos / submodules.

## 8. IDE-Renderer Freeze Hazards — SSOT Pointer

The ten recurring freeze patterns, the eleven-item per-call self-audit checklist, and the post-freeze recovery protocol are owned by [`ide-renderer-freeze-prevention`](../ide-renderer-freeze-prevention/SKILL.md) (extracted from this skill on 2026-05-31 once it became clear the discipline applied to every bash call session-wide, not just to scratch-capture-adjacent work).

This skill remains the SSOT for **one** of that skill's mitigations: when its self-audit flags a call whose upper output bound is unprovable, redirect the output to `scratch/<purpose>-output.txt` per §3–§4 above. See [`ide-renderer-freeze-prevention`](../ide-renderer-freeze-prevention/SKILL.md) Pattern 5 and checklist item 5 for the trigger.
