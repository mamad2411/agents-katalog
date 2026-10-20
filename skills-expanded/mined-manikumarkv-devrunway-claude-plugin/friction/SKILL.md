---
name: friction
description: Append a single friction-log entry to docs/quality/FRICTION-LOG.md. Use when devrunway should have caught something and didn't, or did something it shouldn't have. Optimised for 20-second capture. Usage — /friction [one-line description]
argument-hint: "[optional one-line description]"
arguments:
  - name: description
    description: "Optional — short title for the friction. If omitted, you'll be asked interactively."
user-invocable: true
effort: low
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(date *)
  - Bash(ls *)
  - Bash(mkdir *)
  - Bash(grep *)
  - Bash(wc *)
---

# /friction — quick capture for the dogfood log

The whole point of this skill is **speed**. If logging takes more than 30 seconds, the user stops doing it.

---

## Step 1 — Find or create the log file

```bash
mkdir -p docs/quality
test -f docs/quality/FRICTION-LOG.md || cat > docs/quality/FRICTION-LOG.md <<'EOF'
# Friction Log

Append-only log of devrunway frictions. See entry format in docs/quality/FRICTION-LOG.md template at https://github.com/manikumarkv/devrunway-claude-plugin

## Entries

EOF
```

If the file already exists, leave it. If it doesn't, scaffold the minimal header above and continue.

---

## Step 2 — Collect the four fields

If `$ARGUMENTS[0]` is non-empty, use it as the **title**. Otherwise, ask:

> What happened? (one sentence)

Then ask, in order:

> What did you expect?
> Which skill/agent? (path, e.g. `layers/backend/node-express/nodejs-standards`, or skip)
> Type? (skill-gap | hook-fp | hook-fn | pipeline | ux | other)
> Severity? (low | medium | high — default medium)

Allow `skip` or empty for the skill/agent field. Default severity to `medium` if user just hits Enter.

Don't ask follow-up clarifications. The point is volume. The user can edit the entry later if needed.

---

## Step 3 — Generate the entry ID and append

The entry ID is `F-YYYY-MM-DD-NN` where `NN` is the zero-padded count of entries already logged today.

```bash
TODAY=$(date +%Y-%m-%d)
if [ -f docs/quality/FRICTION-LOG.md ]; then
  COUNT=$(grep -c "^## F-$TODAY-" docs/quality/FRICTION-LOG.md || true)
else
  COUNT=0
fi
NEXT=$(printf "%02d" $((COUNT + 1)))
ID="F-$TODAY-$NEXT"
```

Append this block to the end of the file (use the Edit tool with `old_string` matching the end-of-file marker, or simply Read the file and Write it back with the new block appended):

```markdown
## F-YYYY-MM-DD-NN — <title>
**What happened:** <what>
**Expected:** <expected>
**Skill/agent:** <skill or "—">
**Type:** <type>
**Severity:** <severity>
**Status:** open
```

---

## Step 4 — Confirm

Print one line and stop:

```
✓ Appended F-YYYY-MM-DD-NN to docs/quality/FRICTION-LOG.md
```

Do NOT print the full entry back. Do NOT ask follow-up questions. Do NOT suggest fixes. The user is in the middle of doing something else.

---

## Hard rules

- Total interaction: 4 questions, 1 confirmation line. No more.
- Never auto-classify the type for the user — they decide.
- Never edit existing entries via this command; it's append-only. Use `/friction-review` to manage history.
- If the user types `skip` at any field, write a `—` for that field and move on.
- If the user types `cancel` at any point, abort with no file changes.
