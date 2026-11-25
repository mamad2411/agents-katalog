---
name: rootcompact
description: Pre-compaction memory checkpoint. Use right before compacting a long session (context heavy, ~150k+) to curate durable knowledge into the project's long-term memory BEFORE the conversation is summarized away. Forces fact extraction, dedup against existing memory, protocol-correct writes, and an index update — then hands off to /compact. Does NOT run /compact itself (that's a user command).
triggers:
  - rootcompact
  - 루트컴팩트
  - 컴팩트 전에
  - 컴팩트 전에 저장
  - 기억하고 컴팩트
  - 정리하고 컴팩트
  - 저장하고 컴팩트
  - 컴팩트 준비
  - 컨텍스트 정리
  - 컨텍스트 꽉
  - context 꽉
  - context 정리
  - 기억할거 저장
  - 메모리 저장하고
  - compact 전에
  - before compact
  - save before compact
  - memory checkpoint
---

# rootcompact — Pre-Compaction Memory Checkpoint

Compaction summarizes the conversation and throws away the rest. Anything worth remembering across sessions must be written to durable memory **first**, or it's lost. This skill curates that memory write before you compact, so the next session starts informed instead of amnesiac.

## What this skill does NOT do

- **It does not run `/compact`.** Compaction is a user slash-command; the agent cannot emit a slash command, and there is no tool equivalent. This is the one hard wall: the skill measures context, saves memory, then tells you to press `/compact`. (Claude Code's own auto-compact still fires near the context limit independently.)
- **It does not auto-fire at a threshold.** A skill can't watch the counter and self-trigger. You invoke it (keyword or `/rootcompact`). Truly automatic firing needs a PreCompact hook in settings.json — out of scope here by design.
- **It CAN read the real context size.** Not via the `/context` command (the agent can't run that), but by reading the active session transcript `.jsonl` and summing the last turn's `usage` — equivalent to what `/context` shows (Step 0).

## Activation

Explicit: `/rootcompact`

Auto-triggers (when these phrases appear in the user message):
- "컴팩트 전에 저장", "기억하고 컴팩트", "정리하고 컴팩트"
- "컨텍스트 정리", "context 꽉", "기억할거 저장"
- "메모리 저장하고", "compact 전에", "save before compact"

## What's Different (vs a casual "save to memory")

| Casual save | rootcompact Mode |
|---|---|
| Dump whatever seems notable | Curate only **durable, cross-session** facts; drop ephemera |
| Create a new file each time | **Dedup first** — update existing file over creating a duplicate |
| Freeform note | **Protocol-correct**: frontmatter + correct `type` + `MEMORY.md` index line |
| "Saved." | Reports a table of what was written/updated/skipped, then green-lights compaction |
| Save then hope | Verifies index points at real files before declaring done |

## 7-Step Workflow

### 0. Measure context size, then gate on it
Read the **actual** current context size from the active session transcript and decide whether saving is warranted. The agent can't run `/context`, but the transcript records the same numbers `/context` displays.

Run this. It scopes to the **current project's** transcript dir (derived from cwd), not a global newest-file scan — a global scan would grab another concurrent session (e.g. a cmux/background session) and report the wrong number.

```bash
python3 - <<'PY'
import os, re, glob, json, unicodedata
cwd = os.getcwd()
# Claude Code names the transcript dir after cwd with every non-alphanumeric char → '-'.
# macOS returns paths in NFD (decomposed Hangul); Claude Code munges NFC. Try both, pick the dir that exists.
cands = [re.sub(r'[^a-zA-Z0-9]', '-', unicodedata.normalize(f, cwd)) for f in ('NFC', 'NFD')]
proj = next((os.path.expanduser(f'~/.claude/projects/{m}')
             for m in cands if os.path.isdir(os.path.expanduser(f'~/.claude/projects/{m}'))), None)
if not proj:
    print("NO_TRANSCRIPT"); raise SystemExit
files = glob.glob(f'{proj}/*.jsonl')
if not files:
    print("NO_TRANSCRIPT"); raise SystemExit
latest = max(files, key=os.path.getmtime)   # active session = most-recently-written in THIS project
last = None
with open(latest) as f:
    for line in f:
        try: o = json.loads(line)
        except Exception: continue
        u = (o.get('message') or {}).get('usage') or o.get('usage')
        if u and 'cache_read_input_tokens' in u:
            last = u
if last:
    total = (last.get('input_tokens', 0)
             + last.get('cache_creation_input_tokens', 0)
             + last.get('cache_read_input_tokens', 0))
    print(f"CONTEXT_TOKENS={total}")
else:
    print("NO_USAGE")
PY
```

`CONTEXT_TOKENS` ≈ current context occupancy. Gate the threshold (default **150,000**, adjustable if the user names a different number):

- **≥ threshold** → proceed to Step 1. State the reading: e.g. "현재 ~154k, 저장 진행할게요."
- **< threshold** → don't save reflexively. Report the number and ask:
  > 현재 컨텍스트 약 N k로 150k 아래예요. 그래도 지금 저장할까요?

  Proceed only if the user confirms.
- **`NO_TRANSCRIPT` / `NO_USAGE`** (measurement failed) → fall back to a heuristic read from conversation length, say it's an estimate, and proceed if the session is clearly long.

Never invent a token number — only report what the script returns.

### 1. Locate the memory system
Find where durable memory lives for THIS project, in priority order:
1. **Auto-memory dir** — a `memory/` directory containing `MEMORY.md` (e.g. `~/.claude/projects/<project-slug>/memory/`). This is the primary target. The format authority is the user's global `CLAUDE.md` memory protocol.
2. **OMC project memory** — `.omc/project-memory.json` / notepad, if the repo uses oh-my-claudecode.
3. **Repo docs** — only if neither exists and the user wants a tracked file (e.g. `DECISIONS.md`).

If no memory system is found, ask the user once which target to use; default to the auto-memory dir.

### 2. Extract candidate facts from the conversation
Scan the session for knowledge that will matter **next time**. Sort each candidate into one bucket (matching the global memory protocol):

- **user** — who the user is: role, expertise, stable preferences.
- **feedback** — how I should work: corrections and confirmed approaches. Include the **why** and **how to apply**.
- **project** — ongoing work, goals, constraints, decisions, current state, pending forks. Convert relative dates to absolute.
- **reference** — pointers to external resources: URLs, dashboards, tickets, file locations, account IDs.

### 3. Filter — what NOT to save
Drop a candidate if it is:
- Already recoverable from the repo, git history, or `CLAUDE.md`/`AGENTS.md` (code structure, past fixes, file trees).
- Only relevant to the current turn (scratch reasoning, transient tool output).
- A secret value. Record *where* a credential lives and how to fetch it — **never the value itself**.

If the user says "remember this" but it's repo-derivable, save instead **what was non-obvious about it** (the decision, the gotcha, the why).

### 4. Dedup against existing memory
Before writing, read the existing memory index and relevant files:
- If a file already covers the topic → **update it in place**, don't create a near-duplicate.
- If a recalled fact turned out wrong → delete/correct it.
- Link related memories with `[[other-name]]` in the body (liberal linking is fine; a link to a not-yet-written name marks a TODO, not an error).

### 5. Write — protocol-correct
For each kept fact, write one file (one fact per file) in the established format:

```markdown
---
name: <short-kebab-case-slug>
description: <one-line summary — used for relevance during recall>
metadata:
  type: user | feedback | project | reference
---

<the fact. For feedback/project, follow with **Why:** and **How to apply:** lines.
Link related memories with [[their-name]].>
```

Then add/refresh a **one-line pointer** in `MEMORY.md`:
`- [Title](file.md) — hook`
(One line per memory. Never put memory content into `MEMORY.md` itself — it's an index.)

Match whatever frontmatter the existing files in this project use (e.g. extra `metadata` fields). Mirror the local convention rather than imposing this template verbatim.

### 6. Report & hand off
Output a table of what was **written / updated / skipped (dup) / dropped (ephemeral)**. Then state plainly:

> 메모리 저장 완료. 이제 `/compact` 하셔도 됩니다.

Do not claim to have compacted. The user runs `/compact`.

## Anti-Patterns (forbidden in this mode)

1. **Compacting blindly** — letting the session compact with durable facts unsaved.
2. **Duplicate spam** — creating `topic-2.md` when `topic.md` already covers it. Update instead.
3. **Index drift** — writing a memory file but forgetting the `MEMORY.md` line, or leaving an index line pointing at a deleted file.
4. **Content in the index** — pasting the fact into `MEMORY.md` instead of a one-line pointer.
5. **Saving secrets** — writing a credential value instead of its location + fetch method.
6. **Hoarding ephemera** — saving transient reasoning or repo-derivable facts that bloat recall.
7. **Claiming the compact** — saying "compacted" when the skill only prepared memory.

## Output Format

```
[rootcompact — <project-slug>]

Memory target: <path/to/memory dir or system>

Saved / Updated:
- [created] <slug> (type) — <hook>
- [updated] <slug> (type) — <what changed>

Skipped:
- [dup] <topic> — already in <existing-slug>
- [dropped] <topic> — repo-derivable / ephemeral

Index: MEMORY.md updated (N lines touched), all pointers resolve ✓

→ 메모리 저장 완료. 이제 /compact 하세요.
```

## Termination Conditions

Exit rootcompact only when ALL of:
- Context weight gauged; if light, the user confirmed before saving.
- Memory target located (or chosen with the user).
- Durable facts extracted, bucketed, and filtered.
- Dedup pass done (updates preferred over new files).
- Files written in protocol-correct format; `MEMORY.md` index updated and every pointer resolves to a real file.
- Report table delivered and the user is told it's safe to `/compact`.

## Notes

- Derived from a recurring friction: on long sessions the user manually asks "기억할 거 메모리에 저장해줘" before every `/compact`. This skill makes that one keyword instead of a paragraph, and enforces the format so recall stays clean.
- Pairs with the global memory protocol in `~/.claude/CLAUDE.md` — this skill is the *write-before-compact* discipline; the protocol is the *format authority*.
- Keyword/manual trigger by design. For automatic firing at a token threshold, add a PreCompact hook separately (not part of this skill).
- Works in any project. Global skill. Adapts the write format to the project's existing memory convention.
