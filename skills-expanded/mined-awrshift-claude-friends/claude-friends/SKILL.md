---
name: claude-friends
description: "Ask AIs from other families to review something before you commit to it. User-triggered, never automatic. Fires when the user signals uncertainty or asks for another perspective: 'ask a friend', 'second opinion', 'sanity check', 'cross-check', 'am I missing something', 'stress-test this', 'critique this', 'devil's advocate', 'poke holes in this' (one reviewer); 'this is important', 'high-stakes', 'run a full review', 'ask everyone', 'check before I send', 'before publishing', 'boardroom debate', 'don't let me ship something dumb' (the whole table in parallel); 'help me choose', 'brainstorm options', 'I have several paths', 'compare these approaches', 'diverge and converge' (multi-round round-table); 'ask Gemini', 'ask Opus', 'ask GPT' (a named reviewer). Reviewers come from different model families (Gemini, an isolated Claude with no parent context, optionally GPT) so they do not share blind spots; their findings are input, never a vote. Not for factual lookups — use WebSearch."
allowed-tools: Bash, Read, Glob, Grep, Task, Write
---

# Claude Friends

Claude doesn't decide alone. On the calls that matter, it asks its friends — AIs from other families who think differently and catch the blind spots Claude can't see from the inside. Three styles, picked automatically by what the user typed. Different model families (Gemini + an isolated Claude with fresh eyes; optional OpenAI GPT) catch different blind spots than one model alone. It's not "second-guess yourself" — it's "ask people you trust before you ship."

## When to invoke

Four trigger conditions. If any of them fires, pick the matching style below.

1. User has two or more viable paths to choose between (architecture options, technology choice, content angle) — use Round-Table Discussion.
2. High-stakes design decision (ADR, architecture, launch copy, anything where rollback costs something real) — use Boardroom Debate as the default.
3. User stuck on the same problem after two or more attempts (failed fix, failed retry, about to add another flag or condition) — use Devil's Advocate.
4. Non-trivial proposal awaiting user approval (new module, refactor plan, multi-step migration) — use Devil's Advocate or Boardroom Debate depending on stakes.

If none of these fires, don't invoke the skill. A single-model answer is enough for routine work.

Out of scope: factual lookups like "what's the latest X version" or "is Y still free". Use Claude Code's native WebSearch for those. This skill is for critique and adversarial validation, not fact retrieval.

## The three review styles

### 1. Devil's Advocate (single critique)

Trigger phrases: "sanity check this", "am I missing something", "stress-test this", "critique this", "give me a second opinion".

Two implementations. Claude picks based on context.

(a) Gemini second-opinion. Different model family entirely. Use when the claim is about tech or the external world, or when you want a perspective trained on different data.

(b) idea-validator subagent. Isolated Claude Opus with no parent conversation context. Use when you need to stress-test your own reasoning chain without inherited bias from the parent framing.

Model for (a): `gemini-3.5-flash` with an adversarial reviewer system prompt. Latency 10-20 seconds. Cost around 1 cent.

Model for (b): Claude Opus subagent, fixed-format output (Verdict, top 3 concerns, hidden assumptions, what to verify, counterargument). Latency 10-30 seconds. Cost around 3-5 cents.

Decision rule:
- Tech or external claim: pick Gemini. Different training distribution catches different errors.
- Internal reasoning chain: pick idea-validator. Same model family but no parent context.
- Not sure: default to Gemini for breadth, idea-validator for depth.

Example (Gemini):
```python
Bash("python3 ~/.claude/skills/claude-friends/scripts/gemini.py second-opinion @prompt.md --save out.md")
```

Example (Opus subagent):
```python
Agent(
  subagent_type="idea-validator",
  description="Validate <design name>",
  prompt="<self-contained design / decision / plan as artifact>"
)
```

### 2. Boardroom Debate (dual validation, the headline pattern)

Trigger phrases: "run a full review", "this is important", "give me two independent opinions", "boardroom debate", "high-stakes review".

Tool: parallel call to both Gemini second-opinion and the idea-validator Opus subagent, in the same message.

Same message is non-negotiable. If you call them sequentially, the second reviewer sees the first reviewer's framing in tool results. Independence destroyed. You get two echoes instead of two minds.

Protocol:

0. Pre-flight check. Verify `~/.claude/agents/idea-validator.md` exists before attempting Boardroom Debate. If it's missing, tell the user: "Boardroom Debate needs the idea-validator subagent. Install with: `curl -sL https://raw.githubusercontent.com/awrshift/claude-friends/main/agents/idea-validator.md -o ~/.claude/agents/idea-validator.md`". Then fall back to Devil's Advocate (single Gemini critique) for the current call.

1. Claude writes one self-contained artifact describing the design, decision, or plan. Paste content inline. Never use `@file:` references in the artifact text — Gemini Flash silently hallucinates if `@file:` fails to load. Session #199 incident: a 14 KB audit plan sent via `@file:` came back as a plausible review citing audit IDs D1, F2, C4 that did not exist in the source.

2. One message with two tool calls:
   ```python
   Bash("python3 ~/.claude/skills/claude-friends/scripts/gemini.py second-opinion @prompt.md --save gemini-out.md")
   Agent(subagent_type="idea-validator", prompt="<same artifact pasted inline>")
   ```

3. Read both outputs. Build an acceptance ledger:

   | Concern | Gemini says | Opus says | My evaluation | Action |
   |---|---|---|---|---|

4. Three outcome classes per row:
   - Both agree: high signal, address it.
   - One raises it, the other silent: medium signal. Evaluate whether the silent one had enough context to notice.
   - They disagree: highest-value finding. Different model perspectives surfaced different things. Investigate which is right and why.

5. Present the ledger to the user with critical evaluation. Don't forward output as-is. Show where you accept, where you push back, where reviewers diverge and which side you take.

6. Claude makes the final decision. The skill is not voting between two AIs. Two opinions are input, not majority rule.

When to use: ADR drafts, architecture decisions, multi-step plans (three or more dependent stages), new patterns before codifying, hypothesis falsification, prompt design for core logic, launch copy for public release, anything where rollback cost is meaningful.

Real evidence (Session #201 ADR sprint, 2026-05-25): 6 dual-validations covered 8 architecture decisions. Every validation found at least one load-bearing problem the proposing agent had missed. Examples: BullMQ `limiter` semantics misread (caps execution, not enqueue, silent 2-hour SSE stall). LLM "deterministic at temp=0.2" myth (both validators independently flagged non-determinism). Indefinite retention plan would have violated GDPR storage limitation. Pre-call `SELECT SUM` plan had a TOCTOU race plus 500ms × 50 calls burst stall. Total overhead: roughly 4% of session time. Issues caught would have cost an entire ADR rewrite or a production incident.

Latency: 15-30 seconds parallel. Cost: 5-8 cents per full review.

### 3. Round-Table Discussion (3-round brainstorm)

Trigger phrases: "help me choose between", "brainstorm options", "we have several paths", "diverge then converge", "multi-round brainstorm".

Tool: structured 3-round protocol between Claude and Gemini, with one mandatory user check-in mid-flow.

Process:

```
Phase 0    Gather context (what exists, constraints, goal)
Phase 0.5  GROUND — dual web-check (Claude WebSearch + Flash --grounded in parallel)
R1         DIVERGE — Gemini proposes 7+ ideas, challenges Claude's framing
R1.5       VERIFY (if R1 introduced new tech) — Flash checks new claims
R2         DEEPEN — kill weak ideas down to 3 with concrete arguments
           MANDATORY USER CHECK-IN — present 2-3 survivors, ask for preference
R3         CONVERGE — Gemini picks ONE primary action, secondary, kill list
Phase 3.5  FACT-CHECK — verify all R3 claims (dual: Claude + Flash)
Phase 4    Synthesize — summary table, final recommendation, kill list
```

Use when: two or more viable paths, technology choice, strategy decision, before committing to an architecture with multiple defensible options.

Full protocol with prompt templates per phase is in `references/round-table.md`.

Latency: 5-10 minutes (multi-turn, includes user check-in). Cost: about 25 cents.

## Style Router

Decision tree, top-down:

1. High-stakes design decision (ADR, architecture, launch copy, anything with meaningful rollback cost): Boardroom Debate as default.
2. Two or more viable paths to choose between with no clear winner: Round-Table Discussion.
3. Stuck on a problem, need critique on a non-trivial proposal, want a sanity check: Devil's Advocate.
   - Pick Gemini if the claim is about tech, the external world, or anything with a different training distribution.
   - Pick idea-validator if you need to stress-test your own reasoning chain without inherited bias.

Out of router: factual lookups (current version, price, statistic, recent event) belong to Claude Code's WebSearch, not this skill.

## Critical Evaluation Rule

Reviewer output is input for the decision. It is not the decision.

After every reviewer call:

1. Challenge each recommendation. Is this a fact or speculation?
2. Check for missing context. The reviewer doesn't see your codebase, your prior decisions, your constraints.
3. Verify numbers. Predictions like "90% speedup" are estimates, not measurements.
4. Look for blind spots: implementation complexity, side effects, code the reviewer can't see.
5. Present critically. Use a table: reviewer said, my evaluation, reason, action.

Workflow: reviewer recommends, Claude evaluates critically, Claude presents both to the user, the user decides.

Anti-patterns:
- Forwarding reviewer output as-is.
- Accepting all recommendations without questioning.
- Treating reviewer confidence as a proxy for correctness.
- Skipping critical evaluation because the reviewer is Opus, or Gemini, or "smart".

Full anti-pattern examples are in `references/critical-evaluation.md`.

## Own thinking first, reviewer second

Before invoking any review style, Claude must have:

1. Done its own deep research (read relevant files, prior decisions, source material).
2. Formed its own proposal with rationale, trade-offs, and open questions.
3. Shown the proposal to the user.

Only then invoke the reviewer to critique that proposal.

Why: if Claude goes to Gemini without a thought-through position, it's easy to accept Gemini's recommendation uncritically. Gemini lacks codebase context and can confidently suggest something wrong. The reviewer validates your thinking, it doesn't seed new ideas.

Trigger sequence:
- User asks a complex question. Claude researches, synthesizes its own answer.
- Claude shows the user the answer with reasoning.
- If stakes are high (per "When to invoke"), Claude offers to cross-check via a review style.
- User approves. Claude invokes the chosen style.
- Reviewer returns. Claude evaluates critically and presents the ledger.
- User decides.

Skipping steps 1-3 and asking Gemini first is the anti-pattern. Codified Session #142 after the L4.1 topic clusterer where this exact mistake was caught.

## Cost rules

| Style | Cost per call | When justified |
|---|---|---|
| Devil's Advocate (Gemini) | ~$0.01 | Non-trivial decisions, prompt before finalizing, stuck after 2+ attempts |
| Devil's Advocate (Opus subagent) | ~$0.03-0.05 | Reasoning chain stress-test, fresh adversarial perspective |
| Boardroom Debate (parallel both) | ~$0.05-0.08 | High-stakes: ADR, architecture, launch copy, anything with rollback cost |
| Round-Table Discussion (3-round) | ~$0.25 | Multi-path strategy decisions, technology choice, before committing to architecture |

Rule of thumb: cost of validating is less than cost of being wrong times probability of wrong.

Real cost reality (Session #201 ADR sprint): 8 decisions, 6 dual-validations (some batched), about 60 seconds overhead each. Total: 6 minutes. The ADR took about 3 hours. Validation overhead was around 4% of session time. Caught 6+ load-bearing issues. Obvious ROI for ADR-class work.

## Anti-patterns

1. Sequential parallel calls. Running Gemini then Opus destroys independence. Same message, two tool calls. See `references/dual-validation.md`.

2. `@file:` references in Gemini prompts. Gemini Flash silently hallucinates content when `@file:` fails to load. Always paste content inline. Always verify identifiers in the response match your input. Scan for 2-3 IDs and throw out the response if even one doesn't match. Codified Session #199 (2026-05-24) after the 14 KB audit plan incident.

3. Asking Gemini before forming your own opinion. Turns Gemini into a seed for the decision instead of a validator. Codified Session #142 (2026-05-16) on the L4.1 topic clusterer.

4. Boardroom Debate for trivial things. Burns tokens on stylistic preferences (file naming, format choices, code style with project rules). Save dual validation for genuinely high-stakes moments.

5. Accepting reviewer output as-is. Same Critical Evaluation Rule applies. Output is input for decisions, not the decision. Two opinions are not a majority rule.

6. Using `gemini think` for code review. Claude subagents (via Task tool) can read files and follow imports. Gemini cannot. Use Claude subagent for file-aware code review. Use Gemini for independent reasoning without codebase access.

## CLI Reference

For direct invocation when Claude needs custom params.

```bash
GEMINI=~/.claude/skills/claude-friends/scripts/gemini.py

# Web-grounded ask (used internally by Round-Table Phase 0.5 + 3.5 for tech verification.
# Not a user-facing review style. For factual lookups, use Claude Code's native WebSearch.)
python3 $GEMINI ask "Verify these technologies: A, B, C" --grounded

# Devil's Advocate, single critique
python3 $GEMINI second-opinion @prompt.txt --save out.md

# Boardroom Debate, paired with Agent call to idea-validator in same Claude message
python3 $GEMINI second-opinion @prompt.txt --save gemini-out.md

# Deep reasoning
python3 $GEMINI think "Design a caching strategy for 10M users"

# Visual review (screenshots)
python3 $GEMINI second-opinion @prompt.txt --image our.png --image ref.png --save review.md

# Structured extraction
python3 $GEMINI extract "Parse this invoice..." --json-mode
```

| Command | Default Model | Use When |
|---|---|---|
| `ask` | `gemini-3.5-flash` | Quick questions, research with `--grounded` |
| `second-opinion` | `gemini-3.5-flash` (adversarial system prompt) | Devil's Advocate, Boardroom Debate (paired with Opus) |
| `think` | `gemini-3.5-flash` (high thinking) | Complex reasoning, architecture sketch |
| `extract` | `gemini-3.5-flash` (JSON mode) | Structured extraction from unstructured text |

Legacy: `gemini-3.1-pro-preview` available via `-m` flag for pure-math reasoning (ARC-AGI-style) where Flash 3.5 falls short. Post-audit 2026-05-20, Flash 3.5 beat Pro by 5 findings, ran 22% faster, cost 33% less, produced 0 factual errors. Pro retained only as legacy fallback.

## Setup

The plugin marketplace install (`/plugin marketplace add awrshift/claude-friends`) copies all skill files and the `idea-validator` subagent into the right places — but it cannot configure your API key or Python environment. Three manual steps remain:

1. Get a Gemini API key at [aistudio.google.com](https://aistudio.google.com). Click "Create API Key".
2. Store the key so any shell finds it — `mkdir -p ~/.gemini && printf '%s' 'your_key_here' > ~/.gemini/api_key && chmod 600 ~/.gemini/api_key`. (`gemini.py` reads `GOOGLE_API_KEY` first, then this file. A bare `GOOGLE_API_KEY=...` in `~/.env` does NOT work — nothing sources it in a fresh non-interactive shell.)
3. Run `pip install google-genai`.

If you install the skill manually (without the plugin marketplace), also copy the subagent into place so Boardroom Debate can find it:

```bash
mkdir -p ~/.claude/agents
curl -sL https://raw.githubusercontent.com/awrshift/claude-friends/main/agents/idea-validator.md \
  -o ~/.claude/agents/idea-validator.md
```

## Multimodal: images and video

Pass `--image` (repeatable) or `--video` (URL or local file) to any text command.

```bash
# Compare two designs visually
python3 $GEMINI second-opinion "compare designs, score 1-10" --image ours.png --image ref.png --save review.md

# YouTube video analysis
python3 $GEMINI ask "summarize this video" --video https://youtube.com/watch?v=ID
```

Supported images: PNG, JPEG, WebP, GIF, max about 20 MB total. Gemini 3.x is natively multimodal. Use cases: design review, visual QA, screenshot diff, accessibility audit.

## Parallel execution

When you have multiple independent aspects to validate, run them concurrently.

```bash
python3 $GEMINI second-opinion @aspect1.txt --save r1.md &
python3 $GEMINI second-opinion @aspect2.txt --save r2.md &
python3 $GEMINI second-opinion @aspect3.txt --save r3.md &
wait
```

Useful for multi-axis review like security plus performance plus readability in parallel.

## References

Read on demand.

- `references/round-table.md` — Full 3-round brainstorm protocol with phase-by-phase prompt templates.
- `references/dual-validation.md` — Parallel call protocol, acceptance ledger format, three outcome classes.
- `references/decision-framework.md` — When to use Gemini vs Claude subagents vs Opus subagent.
- `references/critical-evaluation.md` — Why reviewer output is not the decision, with anti-pattern examples.
- `references/models.md` — Gemini model specs, pricing, thinking levels, deprecation table.
- `references/parameters.md` — Complete CLI argument reference.
- `references/third-family-gpt.md` — **OPT-IN.** Add OpenAI GPT as a third reviewer family for the highest-stakes Boardroom Debates (needs a paid OpenAI key; the default two-family flow needs nothing extra).

## Migrating from skill-gemini or skill-brainstorm

If you previously installed `awrshift/skill-gemini` or `awrshift/skill-brainstorm`:

1. Uninstall: `/plugin marketplace remove awrshift/skill-gemini` (and/or `awrshift/skill-brainstorm`).
2. Install: `/plugin marketplace add awrshift/claude-friends`.
3. All previous CLI commands work unchanged: `gemini.py ask`, `second-opinion`, `think`, `extract`, `--grounded`, `--image` behave identically. Point to `~/.claude/skills/claude-friends/scripts/gemini.py` instead of `~/.claude/skills/gemini/gemini.py`.
4. New capabilities: Boardroom Debate (parallel dual validation with idea-validator subagent), Round-Table Discussion (was skill-brainstorm), Style Router (Claude picks based on user phrasing), Critical Evaluation Rule (explicit anti-patterns).

`awrshift/skill-brainstorm` is archived with a pointer to this skill (functionality fully merged).

`awrshift/skill-gemini` was renamed to `awrshift/claude-friends` (GitHub redirect handles old install URLs).

## Why two model families

If both reviewers come from the same lab, they share training distribution, the same blind spots, similar reasoning failure modes. Two echoes, not two minds.

Gemini (Google) has different training data, different reasoning patterns, different post-training feedback loops than Claude (Anthropic). Where Claude misses, Gemini sometimes catches. Where Gemini misses, Claude catches.

The isolated Opus subagent is the same family as the parent Claude, but without inherited context. It can't anchor on the parent's framing or be primed by prior conversation. Fresh adversarial perspective on the artifact.

Boardroom Debate uses both because:
- Gemini catches what Anthropic-family models miss (external optics, different training distribution).
- The Opus subagent catches what's wrong with your own reasoning chain (internal logic without parent bias).

Single reviewer is one angle. Two reviewers from different families are two angles, not two voices.

Evidence: Phase D experiment A433. Same Gemini model with a basic prompt scored 50%. Same model with a prompt that Gemini itself had stress-tested scored 75-80%. The model wasn't the bottleneck. The prompt was. A different model family caught the prompt's blind spots Claude couldn't see from inside.
