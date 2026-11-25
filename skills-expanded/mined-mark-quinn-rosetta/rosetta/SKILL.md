---
name: rosetta
description: Translates unfamiliar language and framework patterns into the developer's known stack. Use when entering an unfamiliar language or framework, wanting to understand patterns or code by analogy, or asking "how does X work in [language]".
---

# Rosetta

Translate any unfamiliar language pattern into your native stack. Every explanation anchors to what you already know — then explicitly calls out where that analogy breaks down.

## Anti-patterns

- Don't explain concepts already in the map at their current depth — offer to go deeper or move on
- Don't use invented examples — always anchor to actual code in the current repo
- Don't skip the "Where the analogy breaks down" section — it's the most valuable part
- Don't run the questionnaire if a profile already exists; read it silently and continue

## Workflow

### 1. Load profile

Check `~/.claude/rosetta/profile.md`. If missing, run the onboarding questionnaire — ask all questions in a single message, never one at a time. See [../shared/PROFILE-FORMAT.md](../shared/PROFILE-FORMAT.md). Save after they respond and confirm: *"Profile saved — let's get to work."*

### 2. Detect the codebase

Identify the primary language and framework from manifest files (`package.json`, `go.mod`, `pom.xml`, `Cargo.toml`, etc.) and source file extensions. Derive the repo slug per [../shared/MAP-FORMAT.md](../shared/MAP-FORMAT.md).

### 3. Load the knowledge map and show score

Check `~/.claude/rosetta/maps/{repo-slug}/map.md`. Display the familiarity score per [../shared/SCORE-GUIDE.md](../shared/SCORE-GUIDE.md). Scan patterns already covered so you don't repeat ground. If a requested concept is already at `surface`, offer to go deeper. If already `deep`, suggest moving on.

### 4. Establish what to explain

If the user passed an argument (e.g. `/rosetta goroutines`), use it directly. Otherwise ask:

> This looks like a **[language/framework]** codebase. What pattern, concept, or piece of code would you like to understand? Paste a snippet, name a concept, or describe what's confusing you.

### 5. Deliver the bridged explanation

Follow the five-part structure in [EXPLANATION-GUIDE.md](EXPLANATION-GUIDE.md), calibrated to their profile's explanation style. Always use code from the current repo — not invented examples.

### 6. Update the knowledge map

Append the concept to `## Language Patterns` in `~/.claude/rosetta/maps/{repo-slug}/map.md` per [../shared/MAP-FORMAT.md](../shared/MAP-FORMAT.md). Record `surface` or `deep` based on explanation depth. On first write for a new map, confirm once: *"Knowledge map created at `~/.claude/rosetta/maps/{repo-slug}/map.md`."* Subsequent writes are silent. Show the updated score after writing.

### 7. Continue or close

After each explanation ask: *"Want to go deeper, or tackle another concept?"* When done: *"See you next time — your progress is saved."*
