---
name: refresh-codemap
preamble-tier: 2
version: 1.0.0
description: |
  Regenerates the project codemap files (hotfiles.md, recent.md) from git
  history. Run weekly or before starting major architectural work to keep
  the SessionStart-injected codemap fresh. Triggers on user prompts like
  "refresh codemap", "update hotfiles", "regenerate codemap", "what's been
  hot lately", "what changed this month", "rebuild project map", or after
  significant rebases / merges that may have shifted the change-frequency
  picture. Does NOT regenerate overview.md — that's hand-curated and should
  only be edited when the architecture genuinely changes.
---

# Refresh Codemap

Regenerates the auto-generated portions of the project codemap.

## Step 1 — Verify we're in a project with a codemap

```bash
test -d .codemap || { echo "No .codemap/ in current directory tree"; exit 1; }
```

If no `.codemap/`, the project hasn't been bootstrapped yet. Tell the user
to run codemap bootstrap manually (write `.codemap/overview.md` and create
the directory) before this skill can help.

## Step 2 — Regenerate hotfiles.md

```bash
cd "$(git rev-parse --show-toplevel)" || exit 1

cat > .codemap/hotfiles.md << 'EOF'
# Hot Files — <project name>

Top files by 90-day change frequency. **Where 80% of recent activity happens =
where 80% of new bugs hide.** Extra care when touching anything in this list.

Generated: <YYYY-MM-DD>

| Changes | File |
|---|---|
EOF

git log --since="90 days ago" --name-only --pretty=format: 2>/dev/null \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -20 \
  | awk '{printf "| %s | `%s` |\n", $1, $2}' \
  >> .codemap/hotfiles.md
```

After regeneration:

1. Read the new hotfiles.md
2. Manually annotate each row with what the file is (1 line per file). Use
   your knowledge of the project + the file's purpose. Do NOT auto-generate
   these — LLM-written file descriptions are usually generic and miss the
   load-bearing role.
3. Below the table, write a "Patterns to notice" paragraph: what cluster of
   files is hot? What does that imply about current direction?
4. Below that, a "When designing changes" reminder block.

The user audits the annotations before committing. The auto-generated table
is the data; the annotations are the judgment.

## Step 3 — Regenerate recent.md

```bash
cd "$(git rev-parse --show-toplevel)" || exit 1

git log --since="30 days ago" --pretty="format:%ad|%s" --date=short 2>/dev/null
```

Use the output to write a NEW `.codemap/recent.md` that summarizes:

1. **Dominant theme** — what's the cluster of recent commits about? (Marketplace
   rollout? Satellite work? Frontend redesign?) State it in one sentence.
2. **Milestones completed** — if commits follow a milestone pattern, list them
   in a table.
3. **Other notable recent work** — non-theme commits worth flagging.
4. **What this implies** — actionable guidance for "if you're about to touch
   X, do Y first." This is the most valuable section.
5. **What's NOT in flight** — what would be off-direction or out-of-scope to
   propose right now.

Style: terse, judgment-laden, action-oriented. Not a commit log replay.

## Step 4 — Verify the codemap hook still fires

```bash
bash ~/.claude/hooks/inject-project-codemap.sh | jq -e '.hookSpecificOutput.hookEventName == "SessionStart"' \
  && echo "✓ codemap hook valid"
```

Report total injected size:

```bash
chars=$(~/.claude/hooks/inject-project-codemap.sh | jq -r '.hookSpecificOutput.additionalContext' | wc -c | tr -d ' ')
echo "Codemap injection: $chars chars (~$((chars / 4)) tokens)"
```

If injection size exceeds ~6000 tokens, suggest the user trim overview.md
or split hotfiles into a top-10 instead of top-20.

## Step 5 — Commit (if user wants)

The codemap is gitignored by default — see if `.gitignore` already has
`.codemap/` listed. If not, ask the user whether they want it committed
(useful for team sharing) or kept local (keeps repo clean).

## When NOT to use this skill

- The user just wants to look at git log — that's a simple bash query, not a
  full regeneration.
- The user wants to update overview.md — that's a hand-curation task, not
  this skill. Open the file and edit it directly.
- No `.codemap/` exists yet — that's a bootstrap task, not a refresh task.

## Relationship to Serena MCP

The codemap covers what Serena does NOT: architectural narrative, git-derived
heat maps, recent activity summaries. Serena handles structural queries
(find_symbol, find_references, get_symbol_overview) — those don't go in the
codemap because they're answered live by Serena. Don't try to capture
Serena's domain in the codemap; you'll just create staleness.
