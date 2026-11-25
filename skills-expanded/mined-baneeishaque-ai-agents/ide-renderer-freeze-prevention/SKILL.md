---
name: ide-renderer-freeze-prevention
description: Industrial protocol for preventing VS Code / Anti Gravity / Eclipse renderer freezes caused by unbounded bash output, chained shell calls, recursive tree walks, multi-path arguments, large heredocs, inverted-match assumptions, and large Edit/Create tool operations. Owns the ten recurring freeze patterns, the eleven-item per-call self-audit checklist, and the recovery protocol after a freeze occurs.
version: 1.0.0
---

# IDE Renderer Freeze Prevention Skill (v1)

> **Skill ID:** `ide-renderer-freeze-prevention`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

The VS Code / Anti Gravity renderer (and similar Electron-based IDE chat surfaces) freezes under unbounded terminal scrollback load — typically when a single `bash` tool call emits thousands of lines, when the cumulative session scrollback grows past the renderer's debounce budget, or when the `edit` / `create` tools issue a large file mutation that the diff renderer cannot draw in time.

This skill is the **SSOT** for the bash-call-shape and tool-shape disciplines that eliminate the freeze. It owns:

- The **ten recurring freeze patterns** observed across sessions (catalogued from real incidents).
- The **eleven-item per-call self-audit checklist** every agent applies BEFORE issuing a bash / edit / create tool call.
- The **recovery protocol** after a freeze occurs.

## Composition Rationale

This skill is **atomic**. It does not compose other skills. It IS composed by:

- [`skill-factory`](../skill-factory/SKILL.md) §4 — every skill-creation session enforces the checklist on its own bash calls.
- [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) §5 — owns the *redirect-to-`scratch/`* mitigation when a call's upper output bound is unprovable (one of this skill's mitigations).

## Related Skills

- [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) — companion mitigation: when this skill's self-audit flags an unbounded call, redirect the output to `scratch/<purpose>-output.txt` and inspect via `view`.
- [`untracked-scratch-triage`](../untracked-scratch-triage/SKILL.md) — disposal of the `scratch/` artifacts the mitigation produces.

## Source Rules

| Rule File | Scope Incorporated |
| --- | --- |
| AGENTS.md Permanent Operating Reminder §1 | One command per bash call |
| AGENTS.md Permanent Operating Reminder §2 | Edit/Create tool large-operation ban |
| AGENTS.md Permanent Operating Reminder §3 | Heredoc hygiene + sentinel collisions |
| AGENTS.md Permanent Operating Reminder §4 | Bounded output + cumulative scrollback |

***

## 1. When to Apply

Apply this skill on **every** bash / edit / create tool call — it is the per-call gate, not a one-time setup.

Apply with extra rigor:

- During skill authoring (skill-factory) — most freezes happen here because of heredoc-heavy content writes.
- During codebase exploration in unfamiliar trees — recursive walks blow up on unexpected build artifacts / `node_modules` / fsevents churn.
- After any prior freeze in the session — the renderer's drain window persists; further unbounded calls compound.

## 2. Prerequisites

None. This skill governs every tool call from the moment the session starts.

***

## 3. The Ten Recurring Freeze Patterns

| # | Pattern | Why it freezes | Mitigation |
|---|---|---|---|
| 1 | Chained commands in one bash call: `A; B`, `A && B`, `A \| B` chained for purposes OTHER than necessary piping | Each segment adds to a single call's output; one bad segment unbounds the whole call. AGENTS.md §1 requires independent shell calls. | **One command per `bash` call.** Pipes are allowed only when they are the natural shape (e.g., `grep \| head`); never chain unrelated commands. |
| 2 | Bash `grep -r` / `find` over a directory tree | Walks unknown numbers of files (fsevents, indexer churn, build artifacts) → unbounded output. | Use the **`grep` tool** (in-process, has `head_limit`, no shell, no TTY drain). Reserve bash `grep` for single-file or known-small inputs. |
| 3 | One command with many path arguments (e.g., `grep regex file1 file2 ... file6`) | Cumulative match volume across paths is unpredictable; one noisy file unbounds the whole call. | One file (or one narrow directory) per call. Iterate at the agent level, not in shell. |
| 4 | Large heredoc writes (one `cat > file <<EOF ... EOF` with > ~80 lines of body) | The heredoc body is rendered in the bash-call transcript before the file write completes; cumulative scrollback spikes. AGENTS.md §3 also flags heredoc-sentinel collisions. | Split into multiple ≤ ~50-line `cat >> file <<EOF` appends; or write via Python `pathlib.Path.write_text()`; never one giant blast. |
| 5 | **Inverted match assumption** — trusting the optimistic-case output size (e.g., "this grep will return zero hits") when the pessimistic-case upper bound is unprovable. The optimistic case never freezes; the pessimistic case does. | A reasoning failure, not a syntactic one. Decisions made on "it'll probably be small" routinely violate the bounded-output rule. | **Default to the pessimistic case.** If the upper bound cannot be proven small, redirect to `scratch/` (see [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md)) or pipe to `head` *before* invocation. Apply Pattern 2 (use the `grep` tool with `head_limit`) whenever the question is "are there matches?" rather than "show me all matches". |
| 6 | **Edit / Create tool on large or many-line operations** | AGENTS.md §2 documents that the `edit` and `create` tools hang the renderer on large operations; any post-freeze `edit` / `create` calls during the drain window are themselves reported as failures. | For multi-line content edits, use **bash heredoc appends** (Pattern 4 sizing) or **Python `pathlib.Path.read_text() / write_text()`** for surgical insertions. Never the `edit` tool for > ~30-line changes. |
| 7 | **Parallel-batch cumulative scrollback** — issuing several content-heavy tool calls (`view` with wide ranges, multi-file reads, `bash` with multi-line output) in a SINGLE response so they execute in parallel | The renderer must draw every batch member's output in one debounce window. Two ~150-line `view`s + a directory listing = a single ~310-line render the renderer cannot split. Per-call output looks fine; cumulative-per-batch output freezes. | **Sum the worst-case output of every call in the batch** during §5 self-audit and treat it as ONE call's budget. Never batch two content-heavy reads (> 50 lines each) in the same response — serialize across turns so the renderer drains between batches. Targeted `view_range` over full-file `view`; ask one focused question per round. |
| 8 | **Cross-turn drain-window carryover** — the first call of a new turn that follows a heavy prior turn (≥ 5 sequential bash/edit calls, or any turn with a Python heredoc + multiple file mutations) | The renderer's debounce / drain budget does NOT reset at turn boundaries. A user saying "continue" does not give the renderer time to drain. The first new-turn call lands on top of unflushed buffer pressure and freezes even though it would have been safe in isolation. | **First call of every new turn after a heavy turn MUST be a trivial probe** (`pwd`, `ls`, `git status --short`) — confirms the renderer has drained before any content-heavy call. Same gate as §6 step 3, applied prophylactically across turn boundaries. |
| 9 | **Within-turn cumulative scrollback** — many small bounded calls in the SAME turn (e.g., 10+ sequential `pwd`/`grep`/`view` calls) whose individual outputs are all tiny but whose per-turn sum exceeds the renderer's per-turn draw budget | Pattern 7 covers parallel batches; this covers SERIAL accumulation within one turn. Each call passes §5 items 1–9 in isolation; the turn as a whole still freezes. | **Budget the WHOLE turn, not just each call.** If a turn already contains ≥ ~8 content-emitting calls, end the turn (yield to the user / split into a checkpoint) before issuing the next call. Trivial probes (`pwd`) don't count. |
| 10 | **Session-aggregate lifetime ceiling** — the cumulative tool-call count across the ENTIRE session (≥ ~50 substantive calls, or any session that has been compaction-summarized) saturates the chat-document size the renderer can hold, causing a hard hang that requires OS force-quit and persists across window restarts because the chat document persists | Per-call and per-turn hygiene cannot mitigate this; the buffer is the chat document itself, not the live scrollback. Symptom: even a `pwd` freezes. | **Structural session-handoff.** When a session approaches the ceiling, stop and hand off to a fresh session via a written brief (pending tasks + on-disk state to verify). Do NOT try to finish "one more thing"; the next tool call may be the one that requires force-quit. |

## 4. Universal Discipline

- **Bound the output size of every single call** (AGENTS.md §4): pipe to `wc -l`, `head`, or `> scratch/...` whenever the upper bound is unknown.
- **Bound cumulative scrollback across the session** (AGENTS.md §4): even small-output calls add up; prefer one `view` of a written file over many `echo` / `cat` calls.
- **Built-in tools beat bash CLI** for grep / glob / view (tool-preferences rule): they respect bounding and avoid the shell entirely.

## 5. Self-Audit Checklist (Before Every Tool Call)

1. Does this call contain `;`, `&&`, or chained commands NOT required by a pipe? → split.
2. Does this call use `grep -r` / `find -type` over a tree? → switch to the `grep` / `glob` tools.
3. Does this call pass more than ONE path argument? → split per path.
4. Is the heredoc body > 50 lines? → split into appends.
5. Could the output exceed ~200 lines? → redirect to `scratch/` or pipe to `head`.
6. Am I assuming this call will return small output without a *provable* upper bound? → treat as pessimistic; apply (2) or (5).
7. Am I about to use the `edit` or `create` tool on a > ~30-line change? → use bash heredoc / Python `write_text` instead.
8. Am I batching this call in parallel with other content-heavy calls in the same response? → sum the worst-case outputs across the batch; if the sum exceeds the single-call budget (§3 Pattern 7), serialize across turns instead.
9. Is this the FIRST call of a new turn that follows a heavy prior turn (≥ 5 sequential bash/edit calls, or any turn with a Python heredoc + multiple file mutations)? → fire a trivial probe (`pwd` / `ls` / `git status --short`) FIRST to confirm renderer drain before this call.
10. Has the CURRENT turn already emitted ≥ ~8 content-producing tool calls? → end the turn (yield to user / checkpoint) before issuing this one; per-call hygiene cannot offset per-turn cumulative scrollback (§3 Pattern 9).
11. Has the SESSION already issued ≥ ~50 substantive tool calls, or been compaction-summarized? → stop and hand off to a fresh session via written brief (§3 Pattern 10); the next call may require OS force-quit.

If any answer is yes, restructure before invoking.

## 6. Recovery Protocol (After a Freeze Occurs)

When a freeze symptom is observed (user reports IDE unresponsive, prior call output truncated, subsequent calls fail):

1. **Stop issuing tool calls.** Wait for the user's acknowledgement before continuing.
2. **Acknowledge the violation** by mapping the offending call to one of the §3 patterns. Do not rationalize; cite the pattern number.
3. **Resume with one small bounded call** — typically a `read_bash` on the most recent shellId (to recover the truncated output) OR a single targeted `view` / built-in `grep` with `head_limit`.
4. **Document the incident** if it reveals a new pattern not already in §3 — propose an addition to §3 in the next turn.

***

## 7. Pitfalls

### 7.1 The Optimistic-Case Fallacy

Most freezes happen because the agent reasoned "this query will probably return nothing / very few results". The reasoning is correct in the optimistic case and irrelevant in the pessimistic case. Always size the mitigation to the pessimistic case.

### 7.2 The Drain-Window Trap

After a freeze, the renderer continues to drain for several seconds. Any tool call issued during the drain window is reported as failed even when the underlying operation succeeded. The fix is to stop and wait, not to retry.

### 7.3 The Edit-Tool Ladder

A common pattern: the `edit` tool fails (per Pattern 6), so the agent retries with `create`, which fails, so it retries with a longer `edit`. Each retry adds to the freeze. Break the ladder immediately on the first failure and switch to bash heredoc / Python `write_text`.

### 7.4 The Skill-Authoring Heredoc Cliff

Skill-authoring sessions are over-represented in freeze incidents because the natural way to write a multi-section markdown file is one big heredoc. Resist this — split every SKILL.md into ≤50-line `cat >> file <<EOF` appends from the start, even if the final file is small. The discipline costs nothing on small files and saves the session on large ones.

### 7.5 The Parallel-Batch Fallacy

Per-call self-audit (§5 items 1–7) sizes each call individually. Item 8 exists because a batch of three calls, each individually within budget, can still exceed the renderer's per-debounce-window draw budget when issued in parallel. The fallacy: "each one is fine, so the batch is fine." Reality: the renderer must draw all batch outputs together. **Symptom signature**: a freeze that happens on a response whose individual `bash` / `view` calls would each have been safe in isolation. **Discipline**: serialize content-heavy reads across response turns, even when the parallel-tool-calling rule encourages batching for efficiency. Efficiency yields to the §4 cumulative-scrollback ceiling.

### 7.6 The Cross-Turn Drain-Window Trap

§7.2 covers drain within a single freeze (don't retry during the drain window). The same drain budget also applies **across turn boundaries**. After a heavy prior turn, the user saying "continue" or asking the next question does NOT reset the renderer's drain timer — the buffer pressure carries forward. The first call of the new turn lands on top of unflushed scrollback and freezes, even though it would have been safe in a clean session.

**Signature**: a freeze on what would otherwise be a trivially safe call, immediately after a heavy authoring turn (many sequential mutations).

**Discipline**: treat the start of every turn following a heavy turn as if recovering from a freeze. Fire a trivial probe (`pwd`, `ls`, `git status --short`) as the first call to confirm renderer health, then proceed with the real work. The probe costs one round-trip and reveals drain-window carryover before it causes damage.

***

### 7.7 The Within-Turn Cumulative Trap

§7.5 catches parallel batches in one response; this trap is its serial twin. A turn that issues ten sequential `pwd` / `grep` / `view` calls — each individually trivial — still accumulates ten render events into the same per-turn draw budget. The §5 per-call audit passes every time, yet the turn as a whole freezes.

**Signature**: a freeze deep inside a turn that has been making small, well-shaped calls for several minutes.

**Discipline**: budget the turn, not just the call. Once a turn crosses ~8 content-emitting calls, end the turn — yield to the user, checkpoint, or split. Trivial probes (`pwd`) don't count toward the budget but also don't reset it.

### 7.8 The Session-Aggregate Ceiling

The §3 patterns 1–9 all govern per-call or per-turn hygiene. Pattern 10 governs the **chat document itself**: across a long session (≥ ~50 substantive tool calls, or any session that has been compaction-summarized), the document size the renderer must hold saturates. The hang is hard — even `pwd` freezes — and survives window restarts because the chat document persists on disk and is rehydrated on reopen.

**Signature**: every tool call freezes regardless of shape; quitting and reopening VS Code does not recover.

**Discipline**: this cannot be mitigated by per-call or per-turn discipline. The only fix is **structural session-handoff** — stop issuing calls, write a hand-off brief (pending tasks + on-disk state to verify), and start a fresh session. Trying to finish "one more thing" is what forces the OS-level force-quit.

***

### 7.9 The Author-Forgets-Their-Own-Skill Trap

A meta-pitfall observed during the very turn that promoted Patterns 9 and 10 into this skill: the authoring agent issued a bash `grep` with FOUR path arguments — a textbook §3 Pattern 3 violation — and froze the renderer. The pattern had been in the skill for months; the agent had just spent the turn editing the skill; recency of authorship did NOT translate to internalization on the next call.

**Signature**: a freeze on a tool call whose offending shape is exactly what the agent just finished documenting.

**Discipline**: after any edit to §3 or §5, (a) the FIRST verification call must explicitly re-read the rule it is about to exercise; (b) any multi-file sweep must use the `grep` tool (per-file iteration) or N separate bash calls — never one bash `grep` with multiple path arguments; (c) **for the REMAINDER of the authoring session, the `edit` and `create` tools are forbidden** — all file mutations must use Python `pathlib.Path.read_text() / write_text()` regardless of size, because §7.9 has been observed to recur within the same session even after the agent acknowledged it. Authoring momentum is not internalization, and a single acknowledgement is not internalization either.

### 7.10 The Heredoc-Markdown-Body Trap

Embedding markdown content (especially fenced code blocks and `### N.M` heading-looking lines) inside a `python3 - <<'SENTINEL'` heredoc — as part of a Python triple-quoted string literal that will later be written to a `.md` file — has produced full IDE freezes even when the outer heredoc sentinel was unique. This is the natural extension of Pitfall 7.4 (Skill-Authoring Heredoc Cliff) to the specific case where the heredoc's body is *itself* markdown destined for a skill doc.

**Mandatory safe pattern.** Two-stage write:

1. Write the markdown body to a scratch file via a SINGLE clean heredoc whose sentinel does not appear anywhere in the body: `cat > /tmp/section.md <<'BODY_SENTINEL_UNIQUE'` … `BODY_SENTINEL_UNIQUE`.
2. Splice it with a tiny Python (or `awk`/`sed` for trivial inserts) that reads `/tmp/section.md` via `Path(...).read_text()` and uses LITERAL `find()` / `replace()` — never a regex that has to scan for heading boundaries inside the body.

**Forbidden.** A single `python3 - <<'SENTINEL'` whose body contains a Python triple-quoted string carrying both fenced code blocks and `### N.M` heading-looking lines.

Cross-reference: `memories/repo/heredoc-with-markdown-body-freeze.md` (incident record, 2026-05-31).

***

## 8. Acceptance Criteria

This skill is correctly applied when:

1. Every bash / edit / create tool call has passed the §5 eleven-item checklist.
2. No session-wide cumulative scrollback growth attributable to repeated small-output calls when one `view` would suffice.
3. After any freeze, the §6 recovery protocol was followed before further tool calls.

***

## 9. Composition by Higher-Level Skills

| Composer | Role |
|---|---|
| [`skill-factory`](../skill-factory/SKILL.md) §4 | Enforces the §5 checklist on every bash call made during skill creation; cites this skill as the SSOT for the patterns and checklist. |
| [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) | Provides the `scratch/`-redirect mitigation referenced in Pattern 5 and checklist item 5; the scratch skill exists in part to give this skill a place to send unbounded output. |

***

## 10. Traceability

- **Origin**: 2026-05-31 — two consecutive renderer freezes during a skills-documentation session (incident 1: large heredoc; incident 2: chained `grep -rnE … ; echo "exit=$?"` with multi-path arguments and inverted-match assumption). The post-incident analysis catalogued patterns 1–6 and the seven-item checklist; originally lodged in `repo-scratch-output-capture` §8 as a session-local addendum, then extracted to this dedicated atomic skill once it became clear the discipline applied to every bash call session-wide, not just to scratch-capture-adjacent work.
- **Pattern 7 added**: 2026-05-31 (same day, post-extraction) — a freeze occurred during the post-extraction completeness audit of THIS skill itself. Two ~150-line `view` ranges (skill-factory body) batched in parallel with a directory listing in one response. Each individual call was within budget; their cumulative parallel render was not. The §6 recovery protocol was followed; the incident catalogued the missing pattern and produced §3 row 7 + §5 checklist item 8 + §7.5 pitfall. Persisted as `permanent_discipline.freeze-7-parallel-batch-cumulative-scrollback`.
- **Pattern 8 added**: 2026-05-31 (same day, immediately after Pattern 7 was catalogued) — a freeze occurred on the FIRST call of a new turn that followed a heavy prior turn (~10 sequential bash + Python + sed mutations). The single grep was small, bounded, single-file, anchored regex — passed every §5 self-audit item 1–8. The freeze proved drain-window carryover across turn boundaries. Discipline added as §3 row 8 + §5 checklist item 9 + §7.6 pitfall. Persisted as `permanent_discipline.freeze-8-cross-turn-drain-window`.
- **Pattern 9 added**: 2026-05-31 — within-turn cumulative scrollback freeze observed after ~10 sequential small bounded calls in a single turn; each individually passed §5 items 1–9 but the turn's aggregate render exceeded budget. Discipline added as §3 row 9 + §5 checklist item 10 + §7.7 pitfall. Persisted as `permanent_discipline.freeze-9-within-turn-cumulative-scrollback`.
- **Pattern 10 added**: 2026-05-31 — session-aggregate lifetime ceiling reached after a compaction-summarized session accumulated ~50+ substantive tool calls; the chat document itself saturated the renderer, causing a hard hang that required OS force-quit and persisted across window restarts because the chat document is rehydrated on reopen. Per-call and per-turn hygiene cannot mitigate; the only fix is structural session-handoff to a fresh session via a written brief. Discipline added as §3 row 10 + §5 checklist item 11 + §7.8 pitfall. Persisted as `permanent_discipline.freeze-10-session-aggregate-lifetime-ceiling`.
- **Meta-pitfall §7.9 added**: 2026-05-31 — immediately after Patterns 9 and 10 were promoted to this skill, the authoring agent violated §3 Pattern 3 (multi-path bash `grep` across 4 files) on the next verification call and froze the renderer. Captured as §7.9 "The Author-Forgets-Their-Own-Skill Trap". Recency of authorship does not equal internalization; post-edit verification must explicitly re-read the rule it exercises.
- **Meta-pitfall §7.9 RECURRED**: 2026-05-31 — within the SAME authoring run that produced §7.9, the agent violated Pattern 6 by using the `create` tool on a ~60-line AGENTS.md bridge file. Quantifies the meta-pitfall: a single re-read after editing §3/§5 is INSUFFICIENT; the §5 self-audit must be re-applied to every file-mutating call for the remainder of the authoring session, not just the immediately-next call.
- **Meta-pitfall §7.9 RECURRED a third time**: 2026-05-31 — agent used the `edit` tool on a ~10-line block in `skill-factory/SKILL.md` during a content-heavy turn (4 prior calls) and froze the renderer. Even sub-30-line `edit` calls compound with Pattern 9 (within-turn cumulative) into a freeze. Strengthened discipline: **after any §3/§5 edit, the agent MUST switch tool-class to Python `pathlib.Path.read_text() / write_text()` for ALL file mutations for the remainder of the authoring session** — not just the immediately-next call, and not just for > ~30-line changes. The `edit` and `create` tools are forbidden in any turn that mutates a skill the agent just edited.
- **Generated via**: [`skill-factory`](../skill-factory/SKILL.md)
