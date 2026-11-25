---
name: analyze
description: Build a developer character profile (persona card) from the user's local coding-agent history — Claude Code, Codex CLI and Gemini CLI transcripts, session titles, and auto-memory files, with projects worked on in several agents merged into one profile. Use when the user asks to analyze their agent or Claude Code history or past sessions, asks what kind of developer they are, says "analyze me", "build my persona", "karakterimi çıkar", "geçmişimi analiz et", or runs /devpersona:analyze. Not for generating improvement suggestions — that is devpersona:advise. Not for raw numbers only — that is devpersona:stats.
---

# Persona analysis

Turn the user's local coding-agent history into an evidence-backed developer character card.
One shared adapter reads Claude Code, Codex CLI and Gemini CLI, so a project worked on in
more than one agent appears once, with the agents named.
All of this runs locally: transcripts are read from disk, nothing is uploaded anywhere.

**Language rule: write every user-facing output in the language the user is speaking with you.**

## Step 1 — Scan

Create the output directory `~/.claude/persona/` if it does not exist, then run the
scanner and load its output:

```
node "${CLAUDE_PLUGIN_ROOT}/scripts/scan.mjs" --out "<home>/.claude/persona/stats.json"
```

(Replace `<home>` with the user's real home directory — expand it yourself;
do not pass a literal `~` or `<home>` to the script.)

Add `--agent claude-code|codex|gemini-cli` to narrow, or `--days 90` to bound the window.

Read the JSON. If `node` is missing, stop and tell the user Node.js 18+ is required.
If `totals.humanPrompts` is 0, stop and say there is no history to analyze yet. Check
`source.agents` — which agents were actually found — and name them in the report, because a
profile built from one agent describes only part of how the user works.

## Step 2 — Gather qualitative evidence

Numbers alone don't make a character. For the **top 3 projects by `humanPrompts`**:

1. **Auto-memory files** — `memoryFiles` holds absolute paths; read each one. These are
   distilled facts from past chats: the highest-quality evidence available. Read all of
   them for the top projects. (Only Claude Code writes these, so they may be empty.)
2. **Prompt samples** — run:
   ```
   node "${CLAUDE_PLUGIN_ROOT}/scripts/scan.mjs" --prompts <project> --limit 30
   ```
   Pass the project's `label` or its `key` (the working directory). This prints truncated
   first/last human prompts of that project; IDE-injected messages are already filtered out. Use them to judge
   tone, prompt style, and how the user directs an agent — never quote more than a
   short fragment back, and never quote anything that looks sensitive (names, keys, URLs).
3. **Session titles** — `sessionTitles` in the JSON summarize what each session was about.

## Step 3 — Synthesize the character card

Produce a card with exactly these sections. Every claim must cite evidence
(a number from the JSON, a memory file, or an observed prompt pattern).
No horoscope material: if the data doesn't support a trait, leave it out.

```markdown
# Developer persona — <date>

## Identity
Stack, domains, project types. (from languages, commands, memory files)

## Working style
Session rhythm (peak hours/days, activeDays), session length, iteration style,
planning vs diving in, how errors are handled (errors/toolCalls ratio, denials).

## Communication style
Prompt length (avgPromptChars), language mix (turkishPromptRatio), tone,
how precisely tasks are specified, correction patterns.

## Strengths
2–4 traits the evidence clearly supports.

## Risk patterns
2–4 honest, kindly-worded risks (e.g. giant sessions, high error rate,
repeated manual routines, never writing tests). Each with its evidence.

## Signature moves
1–3 memorable, specific habits that make this developer recognizable.
```

## Step 4 — Save and present

1. Write the card to `~/.claude/persona/persona.md` (the scan JSON is already at
   `~/.claude/persona/stats.json` from Step 1).
2. Show the full card in chat.
3. Close with one line: everything was computed locally, and
   `/devpersona:advise` turns this card into concrete suggestions.
