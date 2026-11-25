---
name: voice-update
description: Update `context/voice-and-style.md` or `context/about-me.md` from one of three sources. Manual (user dictates a single new rule, sample, or career fact). Memory (batch pull from Claude Code's auto-memory in `~/.claude/projects/<slug>/memory/`). Sent-mail (analyze the last 20-50 sent Gmail messages and propose updates from observed patterns). Always proposes diffs and requires per-file approval; never auto-writes. Use when the user says "save this to my voice file," "remember this style," "consolidate my voice," "update from memory," "read my sent mail," "voice from sent mail," "what does my voice actually look like," "voice-update," or "/voice-update." Pass --source manual|memory|sent-mail.
---

# Voice update

Source of truth: `context/voice-and-style.md` and `context/about-me.md`. This skill is the only writer to those files; every update flows through it.

## What this skill does

Three sources behind one skill. Each source pulls voice / identity information from a different upstream, but all flow into the same downstream (proposed diffs to the two context files):

| Source | Reads | Use when |
|---|---|---|
| **manual** | One dictated rule, paragraph, or fact from the user | User just noticed something about their voice and wants to capture it now |
| **memory** | Claude Code auto-memory dir (`~/.claude/projects/<slug>/memory/`) | Periodic batch pull — what has Claude learned about my style across recent sessions? |
| **sent-mail** | Last 20-50 sent Gmail messages via the connected Gmail MCP | Audit voice files against ground truth — how do you *actually* write vs how you claim to |

`--source` is required. There is no default — the three sources have different scopes and contracts, and picking automatically would hide the trade-off.

## How to invoke

```
/voice-update --source manual "save this rule: I never use 'leverage' as a verb"
/voice-update --source memory
/voice-update --source sent-mail
/voice-update --source sent-mail last 2 weeks
```

## Universal rules (apply to all three sources)

These rules govern every voice-update operation, regardless of source.

### Routing

| If the input is about... | Update this file | Section |
|---|---|---|
| A word the user uses | `voice-and-style.md` | Words I like |
| A word the user doesn't use | `voice-and-style.md` | Banned words |
| A sentence rhythm or structure | `voice-and-style.md` | Sentence structure |
| An AI tell to flag | `voice-and-style.md` | AI tells |
| A sample paragraph the user likes | `voice-and-style.md` | Sample paragraphs |
| A target length or format | `voice-and-style.md` | Length targets / Format preferences |
| A posture / register preference | `voice-and-style.md` | Posture |
| New job, project, paper, credential | `about-me.md` | Trajectory / Public output |
| Where they live, lived, hobbies, languages | `about-me.md` | Identity / How I think |
| A specific belief, thesis, or focus | `about-me.md` | Primary focus / Public output |
| What Claude should know about them | `about-me.md` | What you (Claude) should know |

### Merge philosophy

1. **Preserve old content** — never delete a rule, sample, or fact without explicit user approval.
2. **Add new info in the right section** — don't dump at the end of the file.
3. **Flag contradictions** — surface them; let the user pick which version is canonical.
4. **Don't paraphrase** — use the user's exact words for samples, quotes, and banned words.
5. **One concept per commit** — don't batch unrelated additions. The user reviews each.

### What NOT to do

- Do NOT auto-write. Every change goes through diff + approval.
- Do NOT auto-learn from drafts. Auto-learning from a Coach output would reinforce AI-tells the model rationalized away. Manual + sent-mail are the only legitimate signal paths.
- Do NOT delete existing content without explicit approval.
- Do NOT route style notes to about-me.md or career notes to voice-and-style.md.

---

## Source 1 — manual

The user dictates one thing. The skill writes it.

### Inputs

One of:

1. **A paragraph the user wrote** that they liked — a positive sample for `voice-and-style.md`
2. **A rewrite of a Coach output** — captures both the bad pattern (for AI tells / banned words) and the good rewrite (for sample paragraphs)
3. **A general style note** — "I never use 'leverage,'" "I prefer first person," "I don't use semicolons"
4. **A career fact** — new job, new project, new credential, new public output (routes to `about-me.md`)
5. **An identity fact** — where they grew up, formative experience, hobby, distinctive trait (also `about-me.md`)

If the input is ambiguous, ask one clarifying question before proceeding.

### Process

1. **Identify the target file** via the routing table above
2. **Read the current file** in full
3. **Identify the right section** (don't append blindly)
4. **Compose the diff** with 3-5 lines of surrounding context plus the addition
5. **Show the diff** — clearly label what's being added or flagged for contradiction
6. **Ask for approval**
7. **On approval, write** via Edit tool (preserves existing content)
8. **Echo back the change** in 1-2 sentences. If the change has implications for other files (e.g., a new banned word should also live in `points/banned-jargon.md`), suggest the follow-up but don't do it without approval.

### Example

**User:** "save this to my voice file: I never use 'leverage' as a verb. I'd rather say 'use' or just rewrite the sentence."

**Skill:**

1. Reads `context/voice-and-style.md`
2. Identifies "Banned words" section
3. Proposes diff:
   ```diff
     ## Banned words
     - synergy, drive, deliverables, utilize
   + - leverage (as a verb) — use "use" or rewrite the sentence
     - "at the intersection of"
   ```
4. Asks "OK to write?"
5. On yes, writes; suggests adding to `points/banned-jargon.md` too.

---

## Source 2 — memory

Bridge Claude Code's auto-memory to the context files.

Claude Code's auto-memory captures cross-conversation feedback as files like `feedback_writing_style.md` and `feedback_pm_framing.md` under `~/.claude/projects/<slug>/memory/`. The winning-writing context files are read by every Coach run. The two don't talk to each other — so insights from a session about email writing might never make it into the voice file the next session reads. This source closes that loop.

### Where to find auto-memory

- macOS / Linux: `~/.claude/projects/<project-slug>/memory/`
- Windows: `%USERPROFILE%\.claude\projects\<project-slug>\memory\`

The project slug is derived from the working-directory path. List `~/.claude/projects/` and match the slug. Every memory directory has a `MEMORY.md` index — read that first.

If you can't find the path, ask. Don't guess and read the wrong files.

### Process

1. **Find the memory dir** — ask the user if you don't know it
2. **Read `MEMORY.md`** (the index)
3. **Filter to writing-relevant memories** — file names matching `feedback_writing*`, `feedback_pm*`, `feedback_tone*`, `voice*`, `style*`, plus identity memories not already in `about-me.md`
4. **Read each relevant memory in full** — actual content, not just the hook
5. **Read current `context/voice-and-style.md` and `context/about-me.md`** in full
6. **Identify gaps** — for each memory, ask: is this insight already in the file? If yes, skip. If no, candidate for merge.
7. **Group candidates by target file** per the routing table above
8. **Propose merges per file** — one diff per file with all candidates grouped. Cite the source memory inline for each addition (e.g., `(from feedback_writing_style.md, line 14)`). Flag contradictions.
9. **Ask for approval per file** — user can approve voice-and-style.md but reject about-me.md, or vice versa. Don't bundle.
10. **On approval, write each file**
11. **Suggest pruning** — for any auto-memory now superseded, suggest removing it from auto-memory to keep the index lean (don't auto-delete; user prunes)

### Additional rules for this source

- Cite the source memory for every addition (verifiability). If the user prefers a clean voice file without citations, drop them after the diff is approved.
- Do NOT read auto-memory files outside the writing-relevant filter unless the user explicitly broadens scope.
- Do NOT modify or delete auto-memory files. This skill only reads them.

### When auto-memory has nothing new

Say so plainly. "I read 7 writing-related memories; all 7 are already reflected in your context files. Nothing to consolidate." That's a successful run.

---

## Source 3 — sent-mail

The user's actual voice lives in their sent folder, not in the context files. This source reads the last 20-50 sent messages, surfaces recurring patterns (openers, signoffs, sentence rhythm, words used and avoided, length, formality), and proposes diffs to bring the context files in line with how the user actually writes.

### Why this source exists

Two failure modes the manual / memory sources don't catch:

1. **Aspirational voice ≠ actual voice.** The user wrote `context/voice-and-style.md` six months ago describing how they want to write. Their last 20 sent emails show how they actually write. The Coach reads the file, not the inbox, so it drifts.
2. **Banned-word drift.** A word the user once banned creeps back into their sent mail. Either the rule is wrong (revise it) or the user is regressing (flag it).

Auto-learning from drafts is intentionally not supported — drafts reflect aspirational voice. But sent mail is ground truth: messages the user actually sent and stands behind.

### Inputs

Optional arguments:
- **Time window** — default `last 30 days`. Accept "last week," "last 3 months," "since [date]."
- **Count cap** — default `20 messages`. Cap at 50 to keep token cost bounded.
- **Filter** — default: exclude `to:` matches that look automated (no-reply, notifications@, billing@), exclude one-line replies under 30 words.
- **Recipient archetype** — optional. "Only emails to investors / professors / friends / colleagues." Different archetypes pull different voice registers.

With no args, use defaults and ask whether to narrow before fetching.

### Process

1. **Confirm scope before fetching.** "I'll pull your last 20 sent messages from the past 30 days, excluding one-liners and auto-replies. Sound right?"
2. **Fetch via the Gmail MCP.** Query `from:me` in sent. Fetch message bodies, not just headers. For replies, fetch only the user's portion (skip quoted threads).
3. **Read the current voice files** in full.
4. **Analyze. Look for:**
   - **Opener moves** — how the first sentence starts. "Hi NAME," vs no greeting, BLUF first vs throat-clearing first, time references.
   - **Signoffs** — if "Best" appears in 18 of 20, that's the user's actual default; flag if the file claims otherwise.
   - **Sentence rhythm** — average length, max/min, runs of short sentences.
   - **Words the user actually uses** — confirmations against "Words I like"; candidates for addition if frequent and absent.
   - **Banned-word violations** — quote the sentence.
   - **AI-tell drift** — em-dashes, "delve," "navigate the complexities."
   - **Length** — actual median word count vs file's target.
   - **Format moves** — contractions, fragments, parentheticals, lists.
   - **Recipient adjustments** — does the user write differently to investors vs friends?

5. **Produce the audit report** with three sections:
   - **Confirmations** — patterns matching the file. "File says: no semicolons. Sent: 0/20 ✓"
   - **Drift candidates** — file rules that don't match sent mail. "File says: 'Best' is bland. Sent: 'Best' in 18/20."
   - **New patterns** — recurring sent-mail moves not in the file.

6. **For each drift and new pattern, propose a diff.** Group by file. Per-diff approval, not batched.

7. **On approval, write each file** preserving existing content.

8. **Echo back what changed and propose next read date.** "Updated voice-and-style.md with 3 patterns. Suggest re-running in 4-6 weeks."

### Privacy rules for this source

- Reads sent mail in the user's own session; nothing leaves the local environment except the model's analysis.
- The model sees message bodies in-context to analyze patterns; does not store them outside the session.
- Anonymize any cited recipient by role (`"a senior partner"`), never by name.
- Do NOT analyze drafts in the Drafts folder — those are aspirational, not actual.
- Cap count low if the user wants extra caution. Support `--no-quotes` to suppress example sentences in the audit.

### Cadence

Once per 4-6 weeks. More often overweights short-term tone shifts. Sensible cadences:

- **Weekly:** light touch, catches drift early
- **After a major writing project:** captures patterns from intensive use
- **When the user notices Coach is missing a known preference:** targeted fix

This source is not auto-scheduled. The user invokes it.

---

## Relationship between sources

- **manual** is for one-off, in-the-moment additions ("save this rule")
- **memory** is for periodic batch updates from auto-memory
- **sent-mail** is for periodic audits against ground truth

They compose. After a sent-mail run surfaces three drift candidates, the user might approve two via the audit and capture a fourth (a follow-up thought) via manual. After memory consolidation pulls in new banned words from feedback memories, sent-mail next month verifies they actually held.

Same merge philosophy across all three. Different triggers, different scopes.
