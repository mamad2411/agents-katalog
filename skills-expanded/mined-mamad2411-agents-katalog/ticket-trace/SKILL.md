---
name: ticket-trace
description: Two-way traceability between commits and tickets. (A) When committing any change, make sure the commit message carries the ticket / work-item number — derive it from the user's words, the branch name, or the current task, ask if unknown (a commit-msg hook is bundled but install it only on explicit request). (B) When the user asks WHY code is the way it is — "why was this changed", "who decided this", "is this hardcode intentional", "ทำไมถึงแก้อันนี้", "มีเหตุผลป่าว" — trace the line through git blame/log to the commit, extract the ticket number from the message, fetch the ticket from the tracker (Azure DevOps, GitHub Issues, JIRA), INCLUDING downloading and reading attached images (requirements often live only in an annotated screenshot), and answer with commit + ticket evidence. Trigger on any commit request in a ticketed repo, on "install commit hook", and on any why-is-this-code-like-this / change-archaeology question — even when the user doesn't mention tickets.
effort: max
---

# Ticket Trace

Two operations that share one idea: **a commit message is the join key between code and the reason for the code.** Writing commits without a ticket number breaks the chain; answering "why" questions without following the chain to the ticket produces guesses.

## The chain

```
code line → git blame/log → commit → ticket number in message → ticket in tracker → reason (text + ATTACHED IMAGES)
```

Real example that motivated this skill: a hardcoded label looked like a naming bug. `git log -S "Vehicles"` → commit `e40eb36 "fix 5887"` → ADO ticket #5887 → the description was **one annotated screenshot** saying "Rename Auto to Vehicles / Hide Breakbulk". The hardcode was an explicit requirement. Without opening the image, the answer would have been wrong.

## Operation A — Commit with a ticket number

Every commit in a ticketed repo must reference its ticket. Resolve the number in this order, and say which source you used:

1. **User said it** — "this is for 6084" → use it.
2. **Branch name** — `bug/6084-cargo-labels`, `feature/4242-x` → extract the number.
3. **Session context** — the task you're working on came from a ticket discussed earlier.
4. **Recent log convention** — check `git log --oneline -5` to match the repo's format (`fix 5887`, `feat: ... (#6084)`).
5. **None of the above** → **ask the user** ("Which ticket is this for?"). Do not invent a number, and do not commit without one — a wrong ticket is worse than no commit, because it plants false evidence for future archaeology.

Match the repo's existing message style; don't impose a new one. Skip the requirement for `Merge`/`Revert`/`fixup!` commits.

### Optional: enforcement hook

The skill itself is the enforcement — follow the resolution order above on every commit. A git hook exists as an **opt-in extra**: install it ONLY when the user explicitly asks for hard enforcement ("install the hook", "reject commits without tickets"). Do not install it proactively — it affects every committer and every tool that touches the repo.

```bash
cp <skill-dir>/scripts/commit-msg <repo>/.git/hooks/commit-msg
chmod +x <repo>/.git/hooks/commit-msg   # not needed on Windows
```

The hook rejects commits whose message has no ticket reference (default pattern `(#|\b)[0-9]{3,6}\b`, override with `git config ticket.pattern '<regex>'`; bypass once with `--no-verify`). It must not clobber an existing `commit-msg` hook — if one exists, show it to the user and merge manually.

### Auto commit-log (daily-state `## Log`)

Separately, dev-workflows ships a **PreToolUse hook** (`hooks/commit-log.py`, registered in `hooks/hooks.json`) that fires on every `git commit` and echoes the commit message into that repo's `daily-state.md` `## Log` (via `daily-state.py log`). It is **active automatically when the plugin is enabled** — no install step, "just works" for everyone — and **never blocks a commit** (best-effort; any failure is swallowed). This is the running-worklog half of the chain: the ticket number keeps a commit traceable to its *reason*; the daily-state `## Log` keeps a human-readable record of *what happened when*, at the repo root, independent of git history. The two are complementary — the commit-log hook does **not** check or enforce the ticket number (that is this skill's job, above).

## Operation B — Answer "why was this changed?"

When the user questions a piece of code (a weird label, a hardcode, a removed feature, a magic number), do NOT answer from the code alone. Walk the chain:

1. **Pin the code** — find the exact file/line(s) the question is about.
2. **Find the commit(s)** — pick the right tool:
   - `git log -S "<literal>" -- <file>` — when the text was added/removed (best for hardcodes/labels)
   - `git log -L <start>,<end>:<file>` — history of a line range
   - `git blame -w -C <file> -L <n>,<n>` — who last touched the line
   Follow renames with `--follow` if the file moved.
3. **Extract ticket references** from the commit message (`fix 5887`, `(#6084)`, `JIRA-123`). If the message has none, try the merge commit / PR that brought it in (`git log --merges --ancestry-path <sha>..HEAD | tail`), then the PR description.
4. **Fetch the ticket from the tracker.** For Azure DevOps read [references/ado.md](references/ado.md). For GitHub use `gh issue view <n> --comments`. For JIRA use the REST API with the user's configured auth.
5. **Read the attachments.** If the description references an image, **download it with the same auth and read it through `read-picture`** (load that skill via your harness's mechanism, kind `requirement`, which answers from the project's picture record when this attachment has already been read for the same question and opens the image when it has not) — annotated screenshots frequently ARE the requirement, and skipping them flips the conclusion. Read the comments too; decisions often live in the last comment, not the description.
6. **Answer with evidence**, in this shape:
   - **Verdict first** — intentional (requirement) / bug / unknown.
   - The chain: `file:line` → commit sha + message → ticket id + title + state.
   - What the ticket actually says (quote or describe the annotation), and what that means for the user's question ("don't 'fix' it" / "safe to change").
   - Link the ticket URL so the user can verify.

### Traps

- **The description may be only an image.** An empty-looking HTML body with an `<img src=".../_apis/wit/attachments/...">` is the whole spec. Download and read it — never report "description is empty".
- **Several commits touch the same line.** The newest one isn't always the reason; `-S` on the exact string finds the one that introduced it.
- **Ticket numbers vs other numbers.** `fix 5887` is a ticket; `v2.0.1` and `#region` are not. Sanity-check the id by fetching it — a 404 means you parsed the wrong thing.
- **Closed ticket ≠ fully implemented.** Compare what the ticket asked against the code; surface gaps as findings ("the ticket also says hide X, but X still renders").
- **No ticket found anywhere** — say so plainly and fall back to commit message, PR, and asking the author. Don't speculate dressed as evidence.

## If the output is requested as a document

The default output is an evidence-chain answer in chat — no diagrams. But if
the user asks for the trace as a Markdown report file, follow the diagram
convention in `references/diagram-convention.md` (the
overview diagram is the chain itself: `file:line` → commit → ticket, as a
`flowchart TD`).

## When NOT to use

Pure code-mechanics questions ("what does this function do") need no ticket. Turning findings into new tickets is `ado-backlog`/`github-backlog`. Auditing label wording against a system of record is `naming-audit` (but when naming-audit flags a suspicious hardcode, THIS skill answers whether it was intentional).
