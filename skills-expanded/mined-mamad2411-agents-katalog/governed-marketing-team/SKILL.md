---
name: governed-marketing-team
description: Run marketing work through a governed multi-agent structure — one orchestrator that routes and packs context, six single-remit specialists that only draft, one brand reviewer that gates every draft against evidence, three hard gates (human publish, proof-row claims, no-context-no-start), and a set of versioned context files that every specialist reads and only the context manager writes. Use when setting up or running a Claude-based marketing team, when AI-drafted marketing content keeps shipping unverified claims or off-voice copy, when specialists (human or agent) are publishing directly, or when asked to "govern", "add a review gate", or "stop AI content from going out unchecked". Distinct from `forge-marketing-team` (role switching, no governance) and `marketing-org-operating-model` (org design / build-buy-automate).
---

# Governed Marketing Team

Source: uploaded infographic "CLAUDE — The Governed Marketing Team:
Orchestrator + Specialists + Reviewer + Gates + Context" (prosp). The
infographic is a structure, not a tool; this skill turns it into an
operating procedure that runs inside Claude Code with this repo's agents.

## The core idea

Most AI marketing setups fail in one of five ways (the infographic's
"What it prevents" column):

1. An unverified claim ships.
2. A badge / award / certification with no date gets used.
3. A specialist publishes directly.
4. A decision on voice is made silently.
5. A quarter gets spread across four channels with no strategy.

Every rule below exists to block one of these. If a rule does not map to
one of the five, it is optional.

## The five layers

| # | Layer | Role | Count |
|---|---|---|---|
| 1 | Routing | Orchestrator | 1 |
| 2 | Working | Specialists | 6 |
| 3 | Gate | Brand reviewer | 1 |
| 4 | Control | Gates | 3 |
| 5 | Foundation | Context files | 5 + health report |

### 1. Orchestrator — the routing layer

The orchestrator is the only thing the human talks to. It:

- Restates the job in one sentence before doing anything.
- Splits two deliverables into two orders (never one order with two outputs).
- Names why that specialist, in one line.
- Assembles the **minimum** context packet — only the files that specialist needs.
- Writes the definition of done (format, channel, length, what "pass" means).
- **Fails closed on missing context**: if a required file is absent or stale, it stops and names the file.
- Grants only the named tools to each specialist.
- Routes every draft to the reviewer.
- **Never writes deliverable content itself.**

In Claude Code: the main session is the orchestrator. Specialists are
sub-agents (`Agent` tool) with a restricted `tools` list.

### 2. Specialists — the working layer (6)

| Specialist | Remit | Does NOT decide | Repo agent / skill to use |
|---|---|---|---|
| Strategist | Quarter plan, channel choice, pillar weighting | Voice, copy | `content-strategy`, `growth-operating-framework` |
| Context manager | Maintains the context files — **the only writer** | What the strategy is | `memory-keeper` pattern |
| Content & repurposing | Long-form drafts, repurposing into formats | Which channel ships it | `content-script-writer`, `content-repurpose` |
| Social & distribution | Channel-native posts, scheduling proposals | Publishing (human does) | `content-hook-writer`, `carousel-writer`, `content-manager` |
| Research & analytics | Read-only research, performance reads | Anything that ships | `agentic-researcher`, `content-analyst` |
| Email & lifecycle | Sequences, newsletters, nurture | Send (human does) | `copywriting`, `email-drafter` |

Rules for every specialist: one remit each, one context packet each, one
line stating what they do not decide, **draft only**.

### 3. Brand reviewer — the gate layer

Use the `brand-reviewer` agent (`.claude/agents/brand-reviewer.md`). It checks:

- **Brief**: does it do the job asked (against the orchestrator's definition of done)?
- **Channel**: does it fit the format (length, structure, platform norms)?
- **Claims**: every claim traceable to a row in `proof.md`.
- **Facts**: checked against the source, not memory.
- Returns **pass or fail with evidence** — specific failures, never general notes.
- **Never reviews its own work.**
- Logs a revision event on every fail.
- **No partial credit on claims** — one unproven claim fails the draft.

### 4. Gates — the control layer (3)

| Gate | Rule | Enforcement in Claude Code |
|---|---|---|
| G1 Publish | No publish without a human. Every specialist output is a draft. | `content-publisher` only after explicit human approval; no specialist gets a publish/send tool |
| G2 Proof | No claim without a proof row. Block until verified. | Reviewer fails any sentence with a number, superlative, award or customer name not in `proof.md` |
| G3 Context | No context, no start. Name the missing file and ask. | Orchestrator checks `health-report.md` before routing |

### 5. Context files — the foundation layer

Templates in `context-templates/`. Copy to the project (suggested
`docs/marketing-context/`) and fill in.

| File | Contents | Read by |
|---|---|---|
| `voice.md` | Tone, vocabulary, sentence rules, examples | Every specialist |
| `proof.md` | One row per claim: claim, source, date, expiry | Every specialist + reviewer |
| `pillars.md` | 3–5 content pillars with weighting | Strategist, content, social |
| `banned.md` | Banned words, claims, competitors, topics | Every specialist + reviewer |
| `last-quarter.md` | The numbers a strategy cannot be set without | Strategist, analytics |
| `health-report.md` | Gaps per file, staleness past 90 days, which gaps block this week | Orchestrator |

## Who talks to what (access matrix)

| Actor | May talk to / read | May write |
|---|---|---|
| Human | Orchestrator only | Approvals, final publish |
| Orchestrator | Everything (to route) | Orders, definitions of done — never content |
| Specialists | Their context packet only | Drafts only |
| Research | Read-only everywhere | Research notes |
| Context manager | All context files | **The only writer** of context files |
| Reviewer | Output only — **not the specialist's reasoning** | Pass/fail report, revision log |

The reviewer sees the output, not the reasoning, so it cannot be talked
into a pass by a plausible chain of thought.

## The run loop

1. **Orchestrator routes** — sets the job and packs the context.
2. **Specialists draft** — in parallel where orders are independent.
3. **Reviewer gates** — checks, verifies, requests changes (loop to 2 on fail).
4. **Human approves** — signs off and publishes.
5. **Context improves** — context manager updates files for next time (new proof rows, voice decisions made explicit, health report refreshed).

## Honest limits (read before adopting)

- **Six specialists is overkill below ~3 channels.** A solo operator should
  start with orchestrator + 2 specialists (content, social) + reviewer + all
  three gates. The gates and `proof.md` deliver most of the value; the
  specialist count is the cheapest thing to cut.
- **An LLM reviewing an LLM has correlated blind spots.** That is why G2 is
  mechanical (claim ↔ proof row) rather than judgement-based. Do not let the
  reviewer "judge" a claim plausible — it either has a row or it fails.
- **The system is only as good as `proof.md`.** An empty proof file means
  every factual draft fails. That is the intended behaviour, not a bug.
- **Regulated sectors** (healthcare/medtech — see `medtech-brand-strategy`,
  `anthropic-skills:medtech-market-access-greece`): add a G2b gate for
  regulatory claims (indications, CE/MDR status, efficacy) with a named
  human regulatory reviewer. The brand reviewer is not a regulatory reviewer.

## Commands and agents

- `/governed-marketing [job]` — runs the full loop for one job.
- `brand-reviewer` agent — the gate.
- Templates: `context-templates/*.md`.
