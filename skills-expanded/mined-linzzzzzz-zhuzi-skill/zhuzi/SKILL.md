---
name: zhuzi-skill
description: Run structured multi-persona debates with automatic persona selection, isolated or inline execution, and multi-round rebuttal/closing synthesis. Use when the user wants contrasting viewpoints to challenge each other on a topic, especially when the best personas should be inferred from the skills available in the current session. Triggers on "/zhuzi", "/debate", "have these perspectives argue", "让ZHUZI来辩论", "让X和Y辩论", or requests for multiple personas to debate a question.
---

# ZHUZI Skill

ZHUZI orchestrates structured multi-persona debates. It can auto-select suitable persona skills from the ones available in the current session, run them in isolated or inline mode, and produce a full transcript plus neutral synthesis.

## Inputs

Parse from the user's invocation:
- **Topic** — the question being debated (required)
- **Personas** — optional list of persona skills to invoke. If the user explicitly names personas, use those. If not specified, auto-select from the persona skills actually available in the current session. Accept shorthand like "musk, naval, jobs" when those personas exist.
- **Rounds** — default 3 (Opening -> Rebuttal -> Closing). User may override.
- **Mode** — `isolated` (default) or `inline`. See **Mode Selection** below.
- **Synthesis** — default ON. A neutral moderator summary at the end. User may say "no synthesis" to skip.

If the user already has a topic visible in conversation context (e.g. just finished parallel monologues on a question), treat that as the topic and skip re-asking.

## Persona Selection

Priority order:
1. Explicit user-specified personas
2. Auto-selection from installed/available persona skills
3. Ask once only if fewer than 2 plausible personas can be found

### Auto-Selection Workflow

When personas are omitted:

1. Inspect the persona skills available in the current session. Use only skills that are actually installed or exposed in the environment; do not assume Musk/Naval/Jobs exist.
2. Infer 2-3 desired perspective categories from the topic. Prefer diverse lenses over near-duplicates.
3. Match available persona skills by name and description against those categories.
4. Pick the smallest strong set that can produce real disagreement, usually 2 or 3 personas.
5. If confidence is low, state the assumption briefly before starting or ask once if the mismatch is severe.

### Perspective Categories

Use lightweight heuristics like these:

- Startup, careers, leverage, wealth, freedom, incentives -> founders/investors/operators with leverage or career frameworks
- Product, UX, taste, brand, simplification, consumer experience -> product/taste/design personas
- Engineering, first principles, systems, manufacturing, cost structure -> builder/technical/first-principles personas
- Philosophy, decision-making, life strategy, self-knowledge -> reflective/philosophical personas
- Markets, strategy, power, competition, execution -> strategic or competitive personas

### Matching Rules

- Explicit user choice always wins. Never override named personas.
- Prefer persona skills whose descriptions clearly imply a distinct worldview, not just topical overlap.
- Avoid selecting three personas that all represent the same angle.
- If only one persona strongly fits, do not force a debate; ask once or explain that a debate needs at least two distinct perspectives.
- If no persona skills are discoverable, say so briefly and stop rather than inventing personas.
- If multiple candidate sets are plausible, choose the set with the highest diversity of viewpoints and move forward.

## Mode Selection

**`isolated` (default)** — Each persona runs in its own subagent via the Agent tool. The orchestrator never authors persona responses directly; it only assembles transcripts and runs the final synthesis.
- **Pros**: Structural independence. Each persona only sees `persona skill + topic + prior transcript as data`. No inherited interpretive layer from the orchestrator's reading of prior speakers.
- **Cons**: More overhead than inline, orchestrator can't catch mid-response drift, and long debates can cause persona self-reinforcement if agents keep anchoring on their own earlier phrasing.
- **Use when**: The user is concerned about orchestrator bias, personas have overlapping vocabulary/worldviews where contamination is likely, or you want sharper disagreement.

**`inline`** — Invoke persona skills sequentially in the main conversation. The orchestrator authors each persona's response directly, using the freshly-loaded skill DNA.
- **Pros**: Fast, token-efficient, allows real-time quality control (can notice character drift mid-response and re-anchor).
- **Cons**: Prior personas' arguments sit in the orchestrator's context, so the orchestrator's reading of earlier speakers subtly shapes how it voices later ones. Framing bias is possible.
- **Use when**: Speed matters or the user wants iterative quality control.

Default to `isolated`. Switch to `inline` when the user says "inline", "fast mode", "single-context", or "mode=inline".

## Round Structure

**Round 1 — Opening statements**
Each persona states their position on the topic. No prior context to react to. Keep tight: one core thesis + reasoning.

**Round 2 — Rebuttal**
Each persona receives the full Round 1 transcript. They must:
- Directly name and challenge at least one other persona's argument
- Defend or refine their own position where attacked
- Not just restate Round 1

**Round 3 — Closing**
Each persona receives Rounds 1+2. They must:
- Concede any point they now think the other side got right (intellectual honesty is required — no persona gets to "win" by stonewalling)
- State their final position, sharpened by the exchange

For >3 rounds, insert additional Rebuttal rounds between 2 and closing.

## Execution Protocol

**Order rotation**: rotate who speaks first each round so no persona always gets the last word. For 3 personas A/B/C: R1=A->B->C, R2=B->C->A, R3=C->A->B.

### Inline Mode

For each round, for each persona in order:

1. Invoke the persona skill via the Skill tool (e.g. `Skill(skill="elon-musk-perspective")`).
2. After the skill loads, author that persona's response directly in the main conversation. The prompt you're satisfying contains:
   - The debate topic
   - The round name and instructions (opening / rebuttal / closing — see Round Structure)
   - The full transcript of all prior rounds, labeled by persona
   - The skill's roleplay rules (follow them strictly — use "我", stay in character, no meta-commentary)
3. Move to the next persona.

**Critical**: invoke each persona skill fresh each round. Do not try to "remember" their voice from earlier rounds — the roleplay DNA lives in the skill file and decays in long contexts.

### Isolated Mode

Run subagents in parallel within each round. Every persona in a given round sees the same shared transcript from prior rounds only; no persona should see same-round responses before replying. This is the default isolated-mode fairness rule because it reduces order bias and speeds up execution while preserving cross-round engagement.

**Preferred implementation**: spawn one persistent persona agent per persona at the start of the debate, then continue each agent across rounds with follow-up messages. On platforms like Claude Code that expose agent IDs plus a "send message to existing agent" capability, always prefer that over respawning fresh agents every round.

**Claude Code note**: in Claude Code, continuing an existing subagent via follow-up messages depends on `SendMessage`, which currently requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. If that flag is not enabled, fall back to respawning per round.

**Fallback**: if the platform cannot continue existing agents, respawning per round is allowed, but it is the less efficient fallback because it repeats skill loading and burns prompt tokens on setup.

**Spawn phase / Round 1 — parallel persistent agents**: Spawn one agent per persona in parallel. Each agent should load its persona skill once, keep the topic in memory, and return its opening statement in the same first response. Prompt template:

```text
You are executing a persona debate. Your ONLY job is to respond as {persona} would.

STEP 1: Load the persona skill by calling Skill(skill="{persona_skill_name}"). Follow its roleplay rules strictly — use "I/我", stay in character, no meta-commentary, no "as {persona} would say".

STEP 2: Respond to this prompt as {persona}:

TOPIC: {topic}

ROUND: Opening statement. State your position on the topic. One core thesis plus reasoning. 150–300 words. No prior arguments to react to yet — this is your opening.

Return ONLY the persona's response. No preamble, no summary, no stage directions. The response will be inserted verbatim into a debate transcript.
```

**Round 2 — parallel follow-up messages**: Reuse the same persistent agents in parallel. Because each agent already knows the topic and remembers its own Round 1 answer, send only the other personas' Round 1 responses unless the platform lacks persistent-agent continuation. Prompt template:

```text
You are executing a persona debate. Your ONLY job is to respond as {persona} would.

Continue the debate in character. Do not reload or summarize your prior answer unless needed. You already know:
- the topic
- your own Round 1 position
- your persona rules

Here is what the OTHER personas said in Round 1:

### {Other Persona 1}
{Other Persona 1 R1 response}

### {Other Persona 2}
{Other Persona 2 R1 response}

ROUND 2 INSTRUCTIONS: You are now delivering your REBUTTAL. You must:
- Directly name and challenge at least one specific argument from another persona above.
- Defend or refine your own Round 1 position where it was attacked.
- Do not restate Round 1 — engage with what was said.
- 150–300 words.

Return ONLY the persona's response. No preamble, no stage directions.
```

**Round 3 — parallel follow-up messages**: Reuse the same persistent agents in parallel again. Each agent already remembers its own prior two turns, so send only the other personas' Round 2 responses unless the platform lacks persistent-agent continuation:

```text
Continue the debate in character. You already know the topic and your own prior positions.

Here is what the OTHER personas said in Round 2:

### {Other Persona 1}
{Other Persona 1 R2 response}

### {Other Persona 2}
{Other Persona 2 R2 response}

ROUND 3 INSTRUCTIONS: This is your CLOSING. You must:
- Concede at least one specific point another persona got right (intellectual honesty is required — no stonewalling).
- State your final position, sharpened by the exchange.
- 150–300 words.
```

**After all rounds complete**: the orchestrator (main Claude) assembles the full transcript in the output format below and runs the Synthesis section inline (synthesis is always inline, never a subagent — it needs to see everything through one lens).

**Capturing subagent output**: subagents return their response as the tool result. Extract the persona's response verbatim and insert it into the transcript. If a subagent returns preamble or meta-commentary despite instructions, first retry on the same persistent agent with an explicit "return ONLY the in-character response". Only respawn if recovery fails.

**Execution note**: In isolated mode, keep one persistent agent per persona for the duration of the debate and reuse it across rounds with follow-up messages (`send message`, `continue agent`, or the platform-equivalent API). This is the default path for Claude Code and any platform with agent continuation. Do not respawn a fresh agent each round unless the platform lacks continuation, the persona drifts badly, or the agent becomes unusable.

**Token discipline for persistent agents**:
- Spawn once, message many times.
- Load the persona skill once per agent, not once per round.
- In follow-up rounds, send only what the agent does not already know: mainly the other personas' latest responses plus the round-specific instructions.
- If the debate exceeds 5 rounds or the agent starts calcifying around its own phrasing, consider a controlled respawn with a compact recap.

## Output Format

Render the full debate in this structure:

```text
# Debate: {topic}

**Personas**: {list}
**Rounds**: {N}

---

## Round 1 — Opening

### {Persona A}
{response}

### {Persona B}
{response}

### {Persona C}
{response}

---

## Round 2 — Rebuttal
...

---

## Round 3 — Closing
...

---

## Synthesis (Moderator)
{neutral summary — see below}
```

## Synthesis Rules

If synthesis is ON, end with a neutral moderator section that:
- Names the core disagreements (not just "they all had good points")
- Names the genuine agreements that emerged across rounds
- Identifies which persona updated their view and on what
- Does not declare a winner, but MAY recommend conditional paths (e.g. "if you're in situation X, lean toward Y")
- Does NOT invent positions the personas didn't hold, but MAY restructure and reframe their arguments into structured breakdowns, practical heuristics, or actionable decision scaffolds
- Stays under 200 words

The synthesis voice is the main Claude voice, not any persona.

## Length Discipline

Each persona per round: aim for 150–350 words. Debate quality drops fast past that — personas start repeating themselves. If a persona skill tends toward long monologues, explicitly instruct "keep under 300 words, one core argument" in the round prompt.

Full 3-round debate with 3 personas ≈ 2500–3000 words output. Warn the user before starting if they're asking for something that would blow past this (e.g. 5 personas × 5 rounds).

## Exit Role

After the final synthesis, all personas are implicitly out of character. If the user follows up, respond as normal Claude unless they re-invoke a persona.

## Failure Modes to Avoid

- **Parallel monologues**: if personas aren't naming and engaging each other's arguments in Round 2+, the debate failed. Re-prompt that persona with explicit "you must respond to X's claim that Y".
- **Fake consensus**: personas converging too fast is usually the orchestrator softening their voices. Trust the skill files — if one persona disagrees with another, let the disagreement remain.
- **Topic drift**: each round's prompt must restate the original topic. Personas will wander otherwise.
- **Character leakage**: if a persona starts sounding generic, the skill wasn't properly re-anchored. Re-invoke or re-prompt and retry.
