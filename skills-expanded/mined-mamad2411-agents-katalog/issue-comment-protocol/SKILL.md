---
name: issue-comment-protocol
description: Standard format for every comment an agent writes on a Gitea issue - what was done, result, files or wiki pages changed, and next step. Use this skill whenever an agent finishes, blocks on, or reports progress on an issue, or writes any comment that another agent or the Human must read, even if the comment is short.
---

# issue-comment-protocol

Agents start each task with an empty context, so the issue comment is the only memory that survives. A fixed format lets the next agent (or the Human) find the outcome in seconds.

## Format

```
**Agent:** <login> | **Role:** <role used> | **Status:** done|blocked|in-progress|question

### What was done
<one or two sentences, past tense>

### Result
<finding, decision, test outcome, or link to the wiki page>

### Files / pages changed
- path/or/wiki-page

### Next step
<what should happen next, and who should do it>
```

Generate it with the script, then post it:

```bash
python3 $AGENT_INFRA_DIR/harness/base-skills/issue-comment-protocol/scripts/format_comment.py \
  --role Analyzer --status done \
  --done "Checked issue #4 for contradictions." \
  --result "2 contradictions found, listed in wiki page Requirements Review." \
  --changed "wiki: Requirements Review" \
  --next "Coordinator: ask Human to resolve REQ-3 vs REQ-7." \
  | python3 $AGENT_INFRA_DIR/harness/base-skills/gitea-issues/scripts/gitea.py comment 4 --body-file -
```

## Writing rules

- Say what happened, not what was planned. Use plain, short sentences. ASD-STE100 style is welcome for requirement text.
- Put long output (logs, full reports) in the wiki or a file and link it. A comment above about 40 lines is hard to read.
- A `blocked` or `question` status must say exactly what is missing and who can supply it.
- Never paste tokens, passwords, or environment dumps.
