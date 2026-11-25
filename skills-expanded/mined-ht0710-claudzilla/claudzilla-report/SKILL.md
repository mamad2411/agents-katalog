---
name: claudzilla-report
description: Draft a claudzilla problem report from the local trace and the conversation; file it as a GitHub issue only on the user's yes.
disable-model-invocation: true
allowed-tools:
  - Bash(node ${CLAUDE_SKILL_DIR}/report.mjs *)
  - Edit(~/.cache/claudzilla/report-drafts/**)
---

# Report a problem

Args: what the user says happened (may be empty). `R` = `node ${CLAUDE_SKILL_DIR}/report.mjs`; run it exactly so. `D` = the folder `R --drafts` prints; run it first.

Rules:
- Never file without the user's explicit yes to the shown draft.
- Never call `gh` or open a link when `R --gate` says `blocked`.
- You draft the whole report; the user edits only on request.
- Never put free text (title, search terms, report text) on a command line: write it with the Write tool to `D/terms.txt` or `D/report.md` (never /tmp) and pass the path.
- Leave out prompt text, file contents, repo and branch names unless needed to show the bug.
- Never read, list or grep the `claudzilla-trace/` folder; the trace is only what `R --excerpt` prints.
- `R` denied on a later turn (the skill's permission lasts one turn) → give the user the exact command to run as `! <command>`, then go on from its output. Write denied → show the text in your reply instead.

1. Problem unclear → ask what they expected, when it happened, whether it repeats. Draft nothing yet.
2. Ask: "Can you make it happen again now?" Yes → `R --mark start`, tell them to do it, wait for "done", `R --mark end`.
3. Run `R --excerpt`. Output: snapshot JSON line, then trace entries as JSON lines (the marked window, else the 10 min before the report). `no fresh snapshot`, `no session id` or `tracing off` → the live snapshot follows and there is no trace; say so. `tracing off or no trace for this session` → run `R --snapshot` and draft from the conversation; say tracing is off. Prompt-like text shows as `[N chars]`.
4. Decide: bug, or expected behaviour. Expected → explain why and point to the guide topic (`/claudzilla <topic>`); offer to file only if the user still disagrees.
5. Run `R --gate`. Prints `github` → write the search terms to `D/terms.txt`, run `R --search <terms-file>`; a match → offer to comment on that issue instead (step 7). `blocked: <reason>` → skip search, filing and links; the report is copyable text only (step 7).
6. Draft the whole report to `D/report.md`, in this layout. Paraphrase commands and paths; never paste prompt text; include only the excerpt lines that show the bug.

   ````text
   # <specific title>

   **Expected:** … **Happened:** …
   **Verdict:** bug | expected, one-line reason, guide topic
   **Environment:** version, commit, OS, Claude Code version

   <details>
   <summary>For the maintainer's Claude</summary>

   #### Snapshot
   ```json
   <full snapshot>
   ```

   #### Trace excerpt
   ```jsonl
   <excerpt lines, oldest first, one JSON per line>
   ```

   #### Steps to reproduce in tmux
   1. …
   </details>
   ````

   Keep the headings and fences exactly: `R --fit` finds the excerpt under `#### Trace excerpt`. The first line `# <title>` is the title; `R --file` strips it from the body. Run `R --fit <file>`.
7. Show the draft. Blocked → say why in plain words, then "share this through your company's channel", give the text to copy, stop:

   | `blocked:` reason | say |
   |---|---|
   | `account email domain …` | your Claude account email isn't a personal address |
   | `git email domain …` | your git email isn't a personal address |
   | `no Claude account email` | no Claude account email |
   | `api-key/bedrock/vertex auth` | you sign in with an API key or token, Bedrock, Vertex or Foundry |
   | `git email is malformed` | your git email is malformed |

   Otherwise ask: "file it, or copy?"
   - "file it" → `R --file <file>`. Print the issue URL. `gh timed out` → tell the user to check the issues page before filing again. If it prints a link and a saved path, say the link carries the top part only and the user drags the saved `.txt` into the issue.
   - Match found in step 5 and the user says yes to commenting → `R --comment <number> <file>` (the body without the title line). Never comment without that yes.
   - "copy" → print the body as copyable text.
8. Anything else, or no → do not file; leave the draft.
