---
name: android-bug-hunting-dispatcher
description: >
  Systematic bug hunt across an Android (or KMP) codebase. Dispatches a focused set of
  specialist sub-agents — each targeting a specific class of defect (coroutine/Flow misuse,
  lifecycle leaks, Compose correctness, main-thread violations, resource leaks, KMP-specific
  defects) — and aggregates their findings into a single severity-ranked report with concrete
  fixes. Use this skill whenever the user asks to "find bugs", "hunt bugs", "audit for bugs",
  "look for defects", "find issues", "check for problems", or any phrasing that asks for
  defect detection in an Android/Kotlin/KMP codebase. Trigger even on casual phrasings like
  "what's wrong with my app", "are there any bugs in here", "anything sketchy in this code",
  or "give my Android project a once-over for bugs". This is the entry point — prefer it
  over invoking individual specialist skills directly unless the user has narrowed the scope.
---

# Android Bug Hunt — Dispatcher

## Purpose

This is a **bug-finding** skill, not a code-review skill. The goal is to surface concrete,
runtime-affecting defects with high signal-to-noise — crashes, leaks, races, ANRs,
broken behaviour — not stylistic or architectural commentary.

The dispatcher fans out to specialist skills, each of which knows one class of bug deeply.
The dispatcher's job is to:

1. Scope the hunt to what's relevant for *this* codebase.
2. Run the right specialists in parallel.
3. Aggregate, deduplicate, and rank findings.
4. Produce a single report ordered by severity.

---

## Step 0 — Locate and characterize the project

Identify the project root and what's in it. The result of this step decides which specialists
to dispatch.

```bash
# Module list and build config
find . -name "build.gradle.kts" -o -name "build.gradle" | sort
cat settings.gradle.kts 2>/dev/null || cat settings.gradle 2>/dev/null
cat gradle/libs.versions.toml 2>/dev/null

# Source tree shape
find . -path "*/src/*/kotlin/*" -o -path "*/src/*/java/*" \
  | sed 's|.*/src/\([^/]*\)/.*|\1|' | sort -u

# Key signals for which specialists to dispatch
grep -rE "@Composable" --include="*.kt" -l | head -5            # Compose in use?
grep -rE "kotlinx\.coroutines|Flow<|StateFlow|SharedFlow" \
  --include="*.kt" -l | head -5                                  # Coroutines/Flow in use?
grep -rE "expect (class|fun|object|interface|val|var)" \
  --include="*.kt" -l | head -5                                  # KMP in use?
ls -d */src/commonMain 2>/dev/null                                # KMP source sets?
grep -rE "Room|@Dao|@Entity|@Database" --include="*.kt" -l | head -5
grep -rE "Retrofit|OkHttp|HttpClient" --include="*.kt" -l | head -5
```

Build a small profile of the project:

| Signal | Dispatch |
|---|---|
| Coroutines/Flow used anywhere | `android-bug-hunting-coroutine-and-flow-defects` (almost always) |
| Activities/Fragments/Services exist | `android-bug-hunting-lifecycle-leak-hunter` |
| `@Composable` functions exist | `android-bug-hunting-compose-correctness` |
| Room, Retrofit, file I/O, or `SharedPreferences.commit` references | `android-bug-hunting-main-thread-violations` |
| `Cursor`, `InputStream`, `OutputStream`, OkHttp `Response`, `TypedArray` references | `android-bug-hunting-resource-leaks` |
| `commonMain` source set or `expect`/`actual` declarations | `android-bug-hunting-kmp-defects` |

If the user has narrowed the scope ("just look for memory leaks", "compose only"), dispatch
only those specialists.

---

## Step 1 — Dispatch specialists in parallel

Spawn each relevant specialist **in the same turn**. Each receives:

1. The shared project profile from Step 0.
2. The path to its dedicated SKILL.md.
3. A workspace path for findings: `<workspace>/findings-<specialist-slug>.md`.
4. Instruction to Read the shared Bug Report Format (see Step 2).

### Specialist prompt template

```
You are a specialist bug hunter focused exclusively on **{SPECIALIST_FOCUS}**.

Read your detailed playbook at {SPECIALIST_SKILL_PATH}/SKILL.md and follow it.

## Shared project profile
{PROJECT_PROFILE_FROM_STEP_0}

## Output format
Before writing findings, Read:
`.claude/skills/android-bug-hunting-dispatcher/references/report-format.md`
It defines the finding template plus the Severity, Effort, and Confidence rubrics.
Every finding must use that exact format.

Write findings to: {WORKSPACE}/findings-{SPECIALIST_SLUG}.md
```

---

## Step 2 — Shared Bug Report Format

The canonical finding template, plus the Severity / Effort / Confidence rubrics, lives in:

`.claude/skills/android-bug-hunting-dispatcher/references/report-format.md`

Every specialist Reads that file before writing findings. The dispatcher relies on the format for aggregation in Step 3.

---

## Step 3 — Aggregate and rank

Once all specialists have written their findings:

1. **Read every `findings-*.md`.**
2. **Deduplicate.** If two specialists flag the same root cause from different angles
   (e.g. android-bug-hunting-lifecycle-leak-hunter flags a Fragment holding a binding past `onDestroyView`,
   and android-bug-hunting-compose-correctness flags the same Fragment for a related state issue), unify
   them into one finding that cites both perspectives.
3. **Renumber.** Assign global IDs `BUG-001`, `BUG-002`, … in final severity order.
4. **Sort.** Critical first, then High, Medium, Low. Within a severity tier, sort by
   Confidence (High first), then Effort (Trivial first — quick wins surface first).

---

## Step 4 — Produce the final report

Write to `<workspace>/android-bug-hunt-report.md` using this structure:

```markdown
# Android Bug Hunt — Report

## Summary
- Total findings: N
- Critical: X · High: Y · Medium: Z · Low: W
- Specialists run: <list>
- Files scanned: <count>

## Quick-win table
A compact table of all findings ordered as in Step 3, columns:
ID · Severity · Category · Location · Effort · Confidence · Title

## Findings (full detail)
Every BUG-NNN in full format as defined above, in sorted order.

## Specialists that found nothing
List any specialists that ran and produced zero findings — this is information.

## Notes and limitations
- Anything the hunt could not check (e.g. "no test sources scanned",
  "native code not analyzed", "obfuscated module skipped").
- Any findings where confidence is Low and the user should weigh in.
```

Present the report to the user. If there are more than ~25 findings, also produce a
top-10 executive list at the top so the urgent items are immediately visible.

---

## Notes

- This skill is for **finding bugs**, not for reviewing architecture or style. If the
  user asked for a review, prefer the `android-review` skill instead. If they ask for
  both, run both and combine — but keep the two reports separate so the bug hunt's
  signal-to-noise stays high.
- For very large codebases, scope to a directory or module if the user named one.
- A finding without `file:line` evidence does not belong in the report. Discard
  speculation that a specialist could not anchor to source.
