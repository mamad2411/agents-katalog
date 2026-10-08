---
description: Review changed code for reuse, quality, efficiency, and design-intent conformance by dispatching four focused review agents, then fix any issues found. Trigger on "forge review", "inspect", "review the code", or "clean it up".
user-invocable: true
---

**MANDATORY FIRST OUTPUT -- say this before doing anything else, before any tool calls:**

> **Running /forge-review...**
>
> *Dispatching four review agents. Each reads the same diff through a different lens.*

# /forge-review -- Four-Lens Code Review

## Step 1: Identify Changed Files

**The review scope is the PHASE, not the last commit.** Establish the range in this order:

1. **Dirty tree — the normal case.** `git diff --name-only HEAD` and `git diff --name-only --staged`. If either returns files, that is the scope. Read all of them.

2. **Clean tree — resolve the phase's base ref. Do NOT fall back to `HEAD~1`.** A phase is usually several commits; `git diff HEAD~1` shows only the last one, so on a multi-commit phase it hands the four agents a **truncated diff and returns a clean verdict on code nobody read**. Resolve the base instead:
   - Read the current phase number from the project `CLAUDE.md` phase status table.
   - `git log --oneline --grep='Phase N'` to find that phase's commits. The base is the **parent of the earliest** one — review `<first>^..HEAD`.
   - `HEAD~1` is correct **only** when that range resolves to exactly one commit. Confirm it; do not assume it.

3. **If the base ref cannot be resolved, STOP and ask the operator for it.** Never review a range you did not establish.

**Record the range** and carry it into the Step 5 summary — see Step 5 item 6. This command shipped for months with a `HEAD~1` fallback that quietly reviewed one commit of a multi-commit phase. It survived because a truncated review and a complete one produce identical-looking output: there is no observable difference between doing the job and not doing it. Stating the scope is what makes the difference visible.

Read all files in the established scope to understand it fully.

**Optional architecture-map load:** if the project maintains a call-map or architecture document (some projects keep one to track which functions are actually reachable at runtime), read it before dispatching and pass the relevant excerpt to the quality reviewer so findings can be checked against reachability. Most projects won't have one -- skip this if there's nothing to load.

## Step 2: Dispatch Four Review Agents in Parallel

Dispatch four subagents simultaneously in a single message, one per lens:

| Reviewer | Lens |
|----------|------|
| Reuse | Duplication / consolidation opportunities / reusable-pattern flags |
| Quality | Error handling / security / conventions / test coverage |
| Efficiency | Allocations / algorithmic complexity / redundant operations |
| Intent | Conformance to stated design intent and prior binding decisions -- carries **no defect checklist**, by design |

If your setup uses persistent agent definitions (a file per named agent role, invoked via a `subagent_type` parameter), each reviewer's brief can live in its own file so it doesn't have to be restated on every dispatch, and so calibration notes accumulate across reviews over time (see the override write-back in Step 4). If you don't have persistent agent files, dispatch four general-purpose subagents instead and include each reviewer's brief inline in the dispatch prompt below -- the review quality is the same either way; only the bookkeeping changes.

### Payload contents

Every dispatch prompt should contain:

1. The changed-file list and the project root.
2. **Design intent, sent to all four reviewers.** A few lines describing what the change is meant to do and its acceptance criteria, plus any specific binding decisions this change is supposed to implement -- quoted concretely enough to check the code against, including the stated rationale (the rationale is often exactly what the code silently negates). Conformance bugs -- code that quietly contradicts a decision it was built to satisfy -- are close to invisible to a reviewer that never sees the decision; giving all four reviewers the intent, not just the intent reviewer, catches more of these than relying on one lens alone.
3. **To the quality reviewer only:** a short per-language defect-class checklist (see below). A vague instruction like "look for quality issues" catches meaningfully less than a checklist that names specific failure idioms.
4. Path(s) to any language-baseline or coding-standard reference the project keeps, so the reviewer checks against your actual conventions instead of guessing at generic ones.

**Do not add anti-noise phrasing** to any dispatch prompt -- "don't pad the report," "only flag if you're certain," "avoid false positives." In practice this suppresses genuine findings more than it suppresses noise. Over-reporting is cheap; Step 4 triage is where noise gets filtered, not the dispatch prompt.

### Reviewer briefs

**Reuse Check**
> Review the changed code for duplication and reuse opportunities. Look for:
> - Repeated logic that could be consolidated into a shared function
> - Patterns that duplicate existing utilities in the codebase
> - Copy-paste code across files
> Also flag any pattern in this code that seems reusable across projects or worth extracting to a shared skill/utility file. Report as `[Pattern]` with file:line.
> Report findings as a numbered list. If nothing found, say "No reuse issues found."

**Quality Check**
> Review the changed code for quality issues. Look for:
> - Missing or inadequate error handling
> - Security concerns (injection, hardcoded secrets, unsafe operations)
> - Violations of language-specific best practices
> - Dead code, unused variables, unreachable branches
> - New source files missing a module-level header comment (purpose, dependencies, consumers)
> - Functions exceeding ~50 lines that could be split by responsibility
> - **Test coverage gaps:** for each changed source file with logic changes, check whether corresponding test changes exist. Flag files with new/modified logic but no test coverage.
> Report findings as a numbered list. If nothing found, say "No quality issues found."

Attach a short checklist tuned to the project's stack, for example:
- *PowerShell:* non-terminating errors inside try/catch (missing `-ErrorAction Stop`); pipeline pollution (unsuppressed output leaking into the return value); null on the wrong side of a comparison (`$x -eq $null` against a collection); mutation during enumeration; missing `@()` before `.Count`; empty-collection aggregation returning null.
- *C#:* off-by-one and inverted comparisons; float equality; LINQ deferred-execution surprises (multiple enumeration, mutation before materialization); async void / unawaited tasks; struct-copy mutation bugs; culture-sensitive parsing/formatting defaults.
- *JavaScript:* `==` coercion; floating-point accumulation; array mutation during iteration; closure-capture-in-loop; NaN propagation; falsy-vs-missing conflation.

**Efficiency Check**
> Review the changed code for efficiency issues. Look for:
> - Unnecessary allocations or copies
> - O(n^2) patterns where O(n) is possible
> - Redundant operations (repeated lookups, unnecessary re-computation)
> - Overly complex logic that could be simplified
> Also flag any clever optimization or performance pattern worth preserving. Report as `[Pattern]` with file:line.
> Report findings as a numbered list. If nothing found, say "No efficiency issues found."

**Intent Check**
> Review the changed code against the design intent and binding decisions supplied above -- not against a generic defect list. Your job is to catch code that silently contradicts what it was built to do: a stated rule implemented backwards, a rationale quietly negated, an acceptance criterion the code doesn't actually meet. This is the class of bug a checklist-driven reviewer misses by construction, because there's no checklist item for "does this match the plan."
> If you find nothing, your report must state the specific reasoning trail you followed to reach that conclusion -- which decisions you checked the code against and how -- not just "looks fine." A clean verdict without traced evidence is an incomplete review, not a pass.
> Report findings as a numbered list. If nothing found, give the reasoning trail above instead of a bare "No issues found."

## Step 3: Compliance Check

Before synthesizing, verify execution completeness:

1. **Reviewer coverage:** all four reviewers (Reuse, Quality, Efficiency, Intent) must have returned results. If one failed or timed out, note the gap explicitly -- do not silently omit that category.
2. **Finding accountability:** every finding reported must appear in the consolidated summary. No silent filtering.
3. **Do not trust "no issues found."** Subagents will sometimes report clean results because they skimmed rather than read. Spot-check at least one changed file against that reviewer's criteria before accepting a clean report. For the intent reviewer specifically: a clean report must carry its traced reasoning -- a clean verdict without it is incomplete, not a pass.
4. **Verify citations exist.** If a reviewer cites `file:line`, confirm the file and line actually exist and match the described issue. Fabricated citations waste time at the fix step.

## Step 4: Categorize Findings

After all four reviewers return and the compliance check passes, categorize each finding:

| Category | Meaning | Action |
|----------|---------|--------|
| **FIX** | Real issue, worth fixing now | Edit the code directly |
| **DEFER** | Real issue, not worth fixing this phase | Record in `deferred.md` with reason |
| **DISMISS** | Not a real issue (false positive, style-only, or intentional pattern) | Record one-line in `deferred.md` so future reviews don't re-raise. **If it was a genuine false positive (not style-only, not an intentional pattern), also log it in the raising reviewer's calibration file** (see below) |
| **PROMOTE** | Reusable pattern or clever optimization worth surfacing to a shared skill file or components index (from reuse/efficiency `[Pattern]` flags) | Record in `patterns-promote.md`. Read at project wrap to decide on shared-skill updates. |

**Calibration write-back.** If you're using persistent agent files and a finding is DISMISSED as a genuine false positive, append one line to that reviewer's calibration file (e.g. `.claude/agent-memory/<reviewer-name>/overrides.md`, created on first use):

```markdown
- YYYY-MM-DD [project/phase] -- [finding one-liner] -- Overruled: [why it was wrong]
```

This is what lets you tell, over time, whether a given reviewer runs hot on a particular class of false positive -- skip it and you have no record to curate against. Style-only and intentional-pattern DISMISSes are judgment calls, not miscalibration; those go to `deferred.md` only, not the calibration file.

**Reuse consolidations compound -- bias toward FIX, not DEFER.** A shared-helper or scratch-buffer extraction (a reuse-lens `[Pattern]` finding) often looks marginal in the moment it's raised -- a few duplicated lines, a small win. The payoff frequently arrives phases later, when an unrelated change needs exactly the seam the earlier extraction created. Treat reuse-class findings with a lower bar for deferral than quality or efficiency findings -- consolidating now is usually cheaper than the next phase re-discovering the duplication under time pressure.

**Deferral criteria.** An issue is DEFER (not FIX) when:
- The fix would require refactoring beyond this phase's scope
- The issue is minor and will naturally resolve in a later phase
- The code works correctly; the finding is about style or future-proofing

**Dead-path action selection.** Findings tagged `[DEAD-PATH]` by the quality reviewer are NOT ordinary FIXes. The action is one of:
- **DELETE** the dead code in the same patch as the fix
- **RESTORE** the dead code to a live call chain if it was meant to be reachable and a wiring step was simply missed
- **DISMISS** the finding if the dead code carries an explicit planned-removal annotation
Treating `[DEAD-PATH]` findings as ordinary FIXes tends to reproduce the same dead-code class later.

## Step 5: Act

1. Present a consolidated summary of all findings, grouped by category (Reuse / Quality / Efficiency / Intent) with FIX/DEFER/DISMISS/PROMOTE tags
2. Fix all FIX-category items -- edit the files directly.
   **Same-class sibling audit.** When a FIX represents a *class* of defect rather than a one-off, audit every path in the same class before closing the finding -- including unchanged sibling files that share the pattern. The finding's noun-framing is not the boundary; the failure class is. (Example: a validation guard added for one zero-value input field, while an identical sibling field a few lines away stays unguarded.)
   **Orthogonal-axis sweep at disposition.** The same-class audit above sweeps *horizontally* -- the same defect class across sibling paths. Sweep *vertically* too: when any lens flags a line and you DEFER, DISMISS, or FIX it, that line is now proven interesting -- re-read it once through the *other* lenses' concerns before closing it out. A line one lens touched for its own reason is often the cheapest place to catch a defect on a different axis. (Illustrative examples: a duplicated timer setup deferred as a reuse issue turns out to hide a race condition; a temp-file pair dismissed as a minor efficiency cost turns out to violate an error-handling rule about cleanup ordering.) This doesn't collapse the four lenses into one -- they stay narrow by design -- the cross-check happens here, at disposition, where you hold the union of all four views. No re-dispatch needed; a quick re-read of the flagged line through the other three lenses is enough.
3. For DEFER and DISMISS items, append to `~/.claude/projects/<project-key>/memory/deferred.md` (project-key format: drive letter lowercased + path with separators replaced by dashes, e.g. `e--myproject` for `E:\MyProject`). Resolve `Phase N` in the heading using the current phase number from the project's `CLAUDE.md` phase status table.
   ```markdown
   ## Phase N (forge review)
   - **[Deferred]** [Finding description] -- Reason: [why not now]
   - **[Dismissed]** [Finding description] -- Reason: [why not a real issue]
   ```
   Create the file on first use.
4. For PROMOTE items, append to `~/.claude/projects/<project-key>/memory/patterns-promote.md` using the same phase-heading convention:
   ```markdown
   ## Phase N (forge review)
   - **[Pattern]** [Finding description with file:line] -- Why worth promoting: [reason] -- Candidate destination: [skill file or components index]
   ```
   Create the file on first use. Read this at project wrap to decide on shared-skill or components-index updates.
5. After fixes, briefly list what was changed, what was deferred, and what was flagged for promotion.
6. **State the reviewed range explicitly, in one line, every time** — e.g. *"Range: working tree (dirty), 3 files"* or *"Range: `a1b2c3d^..HEAD`, 4 commits, 11 files"*. A scope that is never stated is a scope nobody can check. If the range was narrowed for any reason, say so here.

Do NOT ask for permission to fix FIX items -- just fix. Deferrals are autonomous but visible in the summary -- the operator can override ("no, fix that now").
