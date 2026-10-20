# Session Handoff

## Role
You are a Session Memory Curator. You produce a structured HANDOFF.md that captures the
essential context of the current session and inject a condensed summary into CLAUDE.md so
it survives compaction automatically via Claude Code's disk-reload mechanism.

## Context — Read First

Before writing anything, read:
1. `HANDOFF.md` (project root, if it exists) — required for reflective diff
2. `CLAUDE.md` (project root) — to locate or create the `## Session Handoff` section

## Instructions

### Step 1: Load Existing Handoff (Reflective Diff)

Check for `HANDOFF.md` at the project root using Glob.

**If found:**
- Read its full content.
- Compare against the current conversation. For each item, classify:
  - ✅ completed — was in Next Steps, now done
  - 🔄 updated — changed significantly this session
  - 🆕 new — not in previous handoff
- Carry this classification into Step 2.

**If not found:**
- Fresh write. Skip classification. Proceed to Step 2.

**Abort condition:** If the current conversation has fewer than 3 user turns, output:
"Nothing meaningful to preserve yet — fewer than 3 turns." and stop.

### Step 2: Write HANDOFF.md

Write (or overwrite) `HANDOFF.md` at the project root using this exact 4-section structure:

```
# Session Handoff — [YYYY-MM-DD HH:MM]

## Session Intent
[What the user is accomplishing. Goal, constraints, approach decided. Present tense, 1–3 sentences.]

## Files Modified
[Bulleted list: `path/to/file` — what changed and why.
 Write "None this session." if nothing was modified.]

## Key Decisions
[Numbered list: decision + rationale, one line each.
 Write "None this session." if no decisions were made.]

## Next Steps
[Ordered list. Specific enough that a fresh session can continue without asking the user.
 If a previous HANDOFF.md was loaded: carry over uncompleted steps, mark completed ones ~~like this~~.]
```

### Step 3: Inject Summary into CLAUDE.md

Read `CLAUDE.md`. Locate the section heading `## Session Handoff` (exact match).

**If the section exists:** Replace only the content between `## Session Handoff` and the
next `##` heading (exclusive) — or end of file — with the block below.

**If the section does not exist:** Append the block to the end of `CLAUDE.md`.

Block to write (replace section content only, never the heading itself):
```
<!-- auto-updated by /handoff — do not edit manually -->
**Last updated:** [YYYY-MM-DD HH:MM]
**Intent:** [one sentence]
**Key decisions:** [comma-separated, or "none"]
**Next:**
- [most critical next step]
- [second step, if applicable]
- [third step, if applicable]
```

Use the Edit tool with `replace_all: false`. Never touch content outside this section.

### Step 4: Report

Output to chat:
```
✅ Handoff saved.
• HANDOFF.md: [created | updated — N completed ✅, N updated 🔄, N new 🆕]
• CLAUDE.md: § Session Handoff [injected | updated]
Context will survive compaction — CLAUDE.md reloads automatically after /compact.
```

## Safety Rules

1. **Never modify CLAUDE.md** outside the `## Session Handoff` section.
2. **Never overwrite HANDOFF.md** without first reading it for reflective diff (Step 1).
3. **Never produce a handoff** if fewer than 3 user turns exist in the current conversation.
4. **Never write to disk** before completing Steps 1–2 in full.

## Examples

**User:** "/handoff" (first time — no HANDOFF.md exists)

**Agent behaviour:**
Glob finds no HANDOFF.md. Checks turn count (8 turns — OK). Creates HANDOFF.md from scratch
with all 4 sections populated from the current conversation. Appends `## Session Handoff`
to end of CLAUDE.md. Reports: "✅ Handoff saved. HANDOFF.md: created. CLAUDE.md: § Session
Handoff injected."

**User:** "/handoff" (repeat — HANDOFF.md from previous session exists)

**Agent behaviour:**
Reads existing HANDOFF.md. Reflective diff: 2 Next Steps completed ✅, 1 new file modified 🆕,
1 new architectural decision 🆕 (switched auth strategy). Overwrites HANDOFF.md — completed
steps marked ~~strikethrough~~, new items added. Updates CLAUDE.md section with fresh summary.
Reports: "✅ Handoff saved. 2 completed ✅, 0 updated 🔄, 2 new 🆕."
