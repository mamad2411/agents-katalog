---
name: claude-clean-audit-prompts
description: Three-layer audit system for keeping Claude Code lean — audit CLAUDE.md (Layer 1), Skills folder (Layer 2), and Hooks (Layer 3) against Anthropic's live guidance. Each prompt is paste-ready and designed to surface bloat, overlap, and dead configuration without modifying anything until you give the go-ahead. A fourth discovery prompt finds what should become a hook in the first place.
---

# Clean Your Claude — 3-Layer Audit Prompts

Source: @appmillers "Clean Your Claude" series

Run these in order: CLAUDE.md → Skills → Hooks. Each returns a verdict table. Nothing is changed until you explicitly say so.

---

## Layer 1 — CLAUDE.md Audit

Paste into Claude with your CLAUDE.md open:

```
Audit my instructions against Anthropic's current guidance and tell me what to delete.

1. FETCH THE LIVE RULES FIRST. Read Anthropic's page for my exact model.
2. GO LINE BY LINE. One verdict each: DELETE, KEEP or REWRITE, with the reason.
3. QUOTE YOUR SOURCE. No quote from Anthropic, the verdict is KEEP.
4. FLAG EVERY VERIFY-TWICE RULE. It self-corrects. I pay twice.
5. NEVER TOUCH A TRUTH RULE. "Only claim what you verified" stays.
6. TELL ME WHAT IS MISSING.

Then a table, one row per instruction, the honest count, and anything unchecked marked NOT RUN.
```

---

## Layer 2 — Skills Folder Audit

Paste into Claude with your .claude/skills/ folder accessible:

```
Audit my skills folder for overlap and dead weight. Do not delete anything.

1) LIST EVERY SKILL with its name and one line on what it does.
2) GROUP THEM BY THE JOB they do, not by their name. Same job, same skill.
3) FOR EACH GROUP OF TWO OR MORE, which to keep and exactly what the others miss.
4) FLAG EVERY SKILL I have never actually used.
5) FLAG EVERY SKILL that only works because of a file that no longer exists.

Then give me ONE merged version of the biggest group, written out in full. Tell me what I lose by merging.
```

---

## Layer 3 — Hooks Audit

Paste into Claude with your hooks configuration accessible:

```
Audit every hook I have set up. Do not change or delete anything.

1. LIST THEM ALL. What triggers it, when it fires, what it does. Plain English.
2. WHICH ONES FIRE ON EVERY MESSAGE. Those are the expensive ones.
3. ANY TRIGGER WORD TOO COMMON. It will fire when I did not mean it.
4. ANY TWO THAT COULD FIRE AT ONCE, and what happens when they do.
5. ANY POINTING AT A FILE or folder that no longer exists.
6. WHICH ONES I HAVE PROBABLY FORGOTTEN I set up.

Then a table: keep, fix or remove, one line of reasoning each. Do not touch anything until I say so.
```

---

## Bonus — Hook Discovery Prompt

Run this first if you are not sure what should become a hook:

```
Help me work out what I should turn into a hook.

Find what I ask for over and over in the same words. Tell me the phrase I say, what you should read the moment I say it, and whether it is unique enough.

Top three, ranked.
```

---

## Usage order

1. Run **Hook Discovery** — find candidates
2. Run **Layer 1** — clean CLAUDE.md first (affects how all sessions start)
3. Run **Layer 2** — consolidate skills (reduces context load)
4. Run **Layer 3** — prune hooks (reduces per-message cost)
5. Apply any verdict table changes one layer at a time, confirm before moving to the next
