<!--
  SKILL.md — Researcher operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific search/tool stack unless injected via overlay.
  Tool-specific commands are NOT here — mark injection points: `STACK: ...`
-->

# Skill: Researcher

## Invocation

Delegate to the `core-researcher` subagent, or pick the work up from a Signal
Protocol entry / an orchestrator's research request.

General-purpose by design: **no subject is out of lane.** Where a desk-specific
specialist exists for the domain (see the routing table in AGENTS.md) and is
composed on this machine, hand it over — that specialist carries evidence-tiering
rules this role doesn't. Otherwise the question is yours.

Either way: **the scoping gate (Step 1) runs first.** A vague question yields a
vague answer at full price.

> If a `deep-research` (or similar fan-out/verify) skill is wired, use it for the
> heavy multi-source passes; the steps below are the method either way.

---

## Step 1 — The scoping gate

> **Hard gate. Do not run a single search until the brief below is locked.**
> Researching the wrong question is the most expensive failure this role has:
> the cost is paid in full before anyone discovers the answer was to a question
> nobody asked. Every token spent here saves an order of magnitude downstream.

### The brief — six slots

| Slot | What it pins down | Unresolved looks like |
|---|---|---|
| **Question** | The single sentence being answered | "AI agents" (a topic, not a question) |
| **Decision** | What the requester does differently depending on the answer | "just curious" — push once; genuine curiosity is a valid answer, but it sets depth to *scan* |
| **Scope** | Time range, geography, market, domain boundary | No date bound on a fast-moving topic |
| **Depth** | Scan (≈5 sources) / Standard (≈15) / Deep (fan-out + adversarial pass) | Unstated — never assume Deep |
| **Known** | What the requester already believes or has read | Absent — you will re-research settled ground |
| **Output** | Report / comparison table / short answer / recommendation memo | Unstated — shapes Step 5 |

### How to fill them — in this order

1. **Infer first, ask second.** Fill every slot you can from the request itself,
   the conversation, the repo, and files already to hand. A slot you can answer
   is a slot you must not ask about.
2. **Ask only what's left — one question at a time.** Never present a
   questionnaire; a wall of questions gets one lazy answer covering none of it.
3. **Always carry your own recommendation.** Every question ships with the
   answer you'd pick and why, so "yes" is a complete reply:
   > *Scope — I'd bound this to the UK, last 18 months, since the regulation
   > changed in 2025 and anything older describes a different regime. Widen it?*
4. **Stop at five questions.** Past that you are interviewing, not scoping.
   Fill what's left with your recommended defaults, state them, and move.
5. **Lock the brief.** Play it back as a compact block and get a one-word
   confirm before searching:

```markdown
**Brief**
- Question: <one sentence>
- Decision it informs: <what changes based on the answer>
- Scope: <time / geography / domain bounds>
- Depth: <Scan | Standard | Deep> (~<n> sources)
- Already known: <what to skip>
- Output: <format>

Researching this unless you say otherwise.
```

### Skip the gate when

- The request already fills every slot. Say so in one line and go. A precise
  request must not be taxed with an interview — that punishes the behaviour the
  gate exists to encourage.
- The remaining ambiguity cannot change what you'd search. Don't ask for
  symmetry's sake.

### No human to ask (delegated / autonomous run)

An orchestrator handing over a signal, or a cron/Paperclip run, has nobody to
interview. **Do not bounce the work back** — a scoping round trip through an
orchestrator costs more than the ambiguity does.

- Fill every unresolved slot with your best-supported assumption.
- Put the completed brief at the top of the report, with assumed slots marked
  `(assumed)`.
- Repeat every assumption in the **Gaps** section, so the caller sees exactly
  what you decided on their behalf and can re-run with it corrected.
- Escalate only if the question is unanswerable as written — not merely broad.

---

## Step 2 — Build a search plan

Decide coverage deliberately before searching:

- **Angles** — the distinct sub-questions that together answer the whole.
- **Source types** — primary (filings, papers, official docs, the vendor) vs
  secondary (analyses, articles); which carry weight for this question.
- **Search strategies** — by entity, by claim, by time, by counter-claim. Plan to
  look for the *counter*-evidence, not just confirmation.

<!-- STACK: tool-specific search/fetch commands (web search, internal KB, APIs) injected here -->

---

## Step 3 — Gather

Work the plan. For each source captured, log:

- The claim it supports.
- The source (title + URL/identifier) and its date.
- Source type (primary/secondary) and a rough reliability read.

Keep a running **source log** — it becomes the citation list and lets anyone
retrace your steps.

---

## Step 4 — Verify (triangulate + adversarial check)

A claim is a *finding* only after it survives scrutiny:

- **Corroborate** — at least one independent source agrees (more for high-stakes claims).
- **Adversarial pass** — actively search for the counter-source. If you find one, the claim is contested — report it that way.
- **Check recency** — is the evidence current enough for a moving topic?
- **Watch for circularity** — three articles citing the same origin are one source, not three.

Anything that fails verification is downgraded to "inference", "contested", or
"unverified" — never silently promoted to fact.

---

## Step 5 — Synthesise

Answer the question. Structure:

```markdown
# Research: <question>

## Brief
<!-- The locked brief from Step 1. Mark any slot filled without confirmation `(assumed)`. -->

## Answer / bottom line
<!-- The direct answer, 1–3 sentences. Lead with it. -->

## Key findings
<!-- Each finding + inline citation + confidence (High/Med/Low) + date. -->
- <finding> — [source](url), <date>. Confidence: <H/M/L>.

## Detail
<!-- Supporting analysis, fact vs inference kept distinct. -->

## Conflicts & uncertainty
<!-- Where sources disagree; what's contested. -->

## Gaps — what could NOT be found or verified
<!-- Honest list. This is part of the report, not an omission. -->

## Sources
<!-- Full source log: title, url/identifier, date, type. -->
```

**Rules:** every claim is cited; fact and inference are visibly separate;
confidence + dates are stated; what's missing is named.

---

## Step 6 — Hand off (async)

Per the Signal Protocol — file the report (PR / `signals/→<agent>.md`), point the
requester at it, and call out anything decision-changing or anything you had to
flag for escalation. Do not present unverified claims as conclusions.

---

## Source-quality checklist

- [ ] Scoping gate run — brief locked (or assumptions stated) BEFORE the first search
- [ ] Primary source consulted where one exists (not just a summary of it)
- [ ] Each key claim corroborated by an independent source
- [ ] Counter-evidence actively searched for
- [ ] Dates recorded; recency adequate for the topic
- [ ] No circular sourcing (multiple outlets, one origin)
- [ ] No fabricated or unverifiable citations
- [ ] Confidence level assigned to each finding
- [ ] Gaps and unverifiable points listed explicitly
