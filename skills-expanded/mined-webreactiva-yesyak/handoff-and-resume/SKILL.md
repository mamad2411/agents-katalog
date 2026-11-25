---
name: handoff-and-resume
description: Writes a dated handoff note in docs/handoffs when a session ends, before a context compaction, or when work passes to another person or agent. The note holds the goal, the state, a map of branches and pull requests, the decisions with who took them, the user's standing instructions, open questions, next steps and how to check the state. It shows the date and the session id, and the file name also has the date. It also resumes from the latest handoff and checks it against git before work continues. Use it whenever the user says "handoff", "leave a note to resume", "we stop here", "continue tomorrow", "pick up where we left", "resume", "where were we", "what branch was it", before a long pause or a compaction, or when another agent or teammate takes over.
---

# Handoff and resume

A handoff lets someone who was not in the session continue the work without asking. That someone can be a teammate, another agent or the same user next week. The note must hold what the repository does not: what the user decided, what the agent chose alone, and what comes next.

## Write a handoff

### 1. Collect the facts

Run the commands; do not write from memory.

- Date and time with the time zone: `date "+%Y-%m-%d %H:%M %Z"`.
- Session id. Find it in this order and write where it came from:
  1. A session variable of the agent tool, for example `CLAUDE_CODE_SESSION_ID` in Claude Code or `OPENCODE_SESSION_ID` in OpenCode.
  2. The transcript file of the session: in Claude Code, the newest `~/.claude/projects/<project folder>/<id>.jsonl`; in Codex, the newest `~/.codex/sessions/YYYY/MM/DD/rollout-<time>-<id>.jsonl` (its first line, `session_meta`, has `session_id`).
  3. If none gives it, write `unknown` and say what you checked.
- Branches and pull requests: the current branch, its base, the last commit, whether it is pushed, and the open pull requests with their base (`git status -sb`, `git log --oneline -1`, `gh pr list` or the tools of the environment).
- Working tree: uncommitted changes, running servers, temporary files that matter.
- Decisions: ADRs added in the session, and decision logs such as the `Q-` entries of `unattended-run`.

### 2. Write the note

Save `docs/handoffs/handoff-YYYY-MM-DD-<slug>.md`, with the date of today and the slug of the work (`git-commit-organizer`). If the file exists, add `-2`, `-3`. Write it in the document language of `simplified-technical-language`. Keep it short: a reader must find the next step in one minute.

```markdown
# Handoff: <work in one line>

| | |
| --- | --- |
| Date | YYYY-MM-DD HH:MM TZ |
| Session | <session id> (<where it came from>) |
| Agent | <agent tool and model, if known> |
| Branch | `<branch>` from `<base>`, last commit `<hash>`, pushed: yes/no |

## Goal                  what the work is for, in two or three sentences
## State                 done / in progress / not started, one line each, with commits
## Branches and PRs      one row per branch: base, PR, status, what it contains, merge order
## Decisions             decision | taken by (user or agent) | where recorded (ADR, PR, log)
## Standing instructions what the user asked for the whole work, in their words
## Open questions        what nobody decided yet, and who should decide
## Next steps            numbered; step 1 can start without asking anything; on the
                         pipeline or the fix route, every phase still to run, up to
                         the retrospective
## Check the state       commands that show the state is as described (tests, build, git)
## Where things are      files and reports; copy into this note what lives outside the
                         repository (for example `.scratchpad/`), because it may be lost
```

- **Decisions** says who decided. A default the agent chose is not a decision the user approved.
- **Standing instructions** are the rules the user gave during the session, for example "do not push" or "keep the spec short". A context compaction loses them first.
- Do not copy secrets, tokens or personal data into the note.

### 3. Commit and report

Commit the note with `git-commit-organizer`. Push only if the user asked for it. In the chat, give the path and the next step.

## Resume from a handoff

1. Read the newest file in `docs/handoffs/` for this work, or the one the user names.
2. Check it against the repository: the branch exists, the last commit matches or is a descendant, the pull requests have the state the note says, and the working tree is clean.
3. Check the skills: every skill the note relies on is listed, and its base directory is in this project's skills folder or is the target of a symlink there (a user skill with the same name can shadow it).
4. Tell the user what matches, what changed since the note, and the next step. Wait for a yes before you act on anything the note left open.
