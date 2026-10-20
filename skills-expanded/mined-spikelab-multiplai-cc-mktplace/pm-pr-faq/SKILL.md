---
name: pm-pr-faq
description: Draft Amazon-style Working Backwards documents — a fictional press release dated at launch plus an internal FAQ. Forces clarity on customer benefit, target persona, and tradeoffs *before* the team commits to building. Includes an adversarial FAQ generator (if the user provides fewer than 10 hard questions, the skill generates the rest as a skeptical investor / exec) and a stress-test pass. Triggers on "pr/faq", "pr faq", "6-pager", "six-pager", "working backwards", "launch narrative", "investor memo", "future-state narrative", "press release for", "fictional press release", "Amazon-style memo", or when the user wants to pressure-test a not-yet-built initiative by writing as if it had already shipped. Composes downstream of `pm-strategy-memo` (when strategy implies a launch) and `pm-persona-codifier` (the PR's fictional customer is a persona).
---

# pm-pr-faq

Write a future-state launch document as if the thing is already shipping. The discipline is what matters: by forcing yourself to write the press release first, you discover whether the customer benefit is real, whether the persona is recognizable, and whether the tradeoffs are admittable in public. If those are weak, the document tells you to *not build* — which is the highest-leverage version of this artifact.

Two parts:
1. **Press Release (PR)** — 1 page, dated at the future launch date, in the voice and shape of a real press release.
2. **Internal FAQ** — 10-15 hard questions with honest answers, including the questions the team would rather not address.

## Arguments

| Arg | Description | Default |
|-----|-------------|---------|
| **source** | File path (strategy memo, brief, conversation), `--from-conversation`, or thesis | *(required)* |
| `--launch-date` | Future date the PR is dated at | ask |
| `--audience` | Who reads it: `internal`, `investors`, `customers`, `mixed` | `internal` |
| `--with-stress-test` | Run the adversarial stress-test pass | `true` |

## Workflow

5 steps. Don't skip Steps 3-4 — the adversarial FAQ generation and stress-test are where this artifact earns its keep.

### Step 1 — Context gather (5 questions, asked together)

If `--from-conversation`, infer from context. Otherwise, ask:

1. **What's the future state?** Describe the launched thing in 2-3 sentences. What does the customer see, hear, experience after launch?
2. **Launch date.** Concrete future date. "Q3" is not concrete; "September 15, 2026" is. Drives the framing — a 3-month-out launch reads differently from a 2-year-out vision.
3. **Primary customer / persona.** Who's the "you" in "you can now…"? If multiple personas are in scope, you need multiple PR-FAQs (or to pick one).
4. **Primary metric.** What number moves because of this launch? Concrete and measurable.
5. **Tradeoffs and known costs.** What does this REQUIRE giving up — features cut, costs incurred, customers excluded, scope narrowed? The FAQ stress-tests these; if you can't name them, the FAQ will surface them awkwardly.

After answers come in, restate them and ask the user to confirm before drafting.

### Step 2 — Draft the Press Release (PR)

See `references/working-backwards-canon.md` for full structure. Working from launch backwards forces clarity that solution-thinking doesn't.

**Structure (1 page max):**

```markdown
# [Product/Capability Name] — [Headline that states the benefit, not the feature]

**[Company]** — **[Future launch city, future launch date]** — [Subhead: who it's for and what they get, one sentence]

[**Summary paragraph (3-5 sentences):** the announcement, capable of standing alone if everything else were cut.]

[**Problem paragraph (3-5 sentences):** the state of the world before launch, from the customer's POV. What was broken. Specific. No "in today's fast-paced world" throat-clearing.]

[**Solution paragraph (3-5 sentences):** how the new thing works for the customer. Concrete capabilities, not platform abstractions. The reader should be able to picture using it.]

> "[Quote from a fictional but plausible customer. Names a specific outcome, in their voice.]" — [Fictional Customer Name, Title, Company]

> "[Quote from internal leader. States the strategic intent without marketing-speak.]" — [Real Leader Name, Real Title, Company]

**Getting started.** [3-4 sentences: how a real customer adopts this — sign up, what they do first, what they see in 24-48 hours. Concrete and frictionless.]
```

**Discipline rules for the PR:**

- **No buzzwords.** "AI-powered," "intelligent," "seamless," "world-class," "best-in-class," "next-generation" — all banned unless the user explicitly insists. They communicate nothing and tag the doc as marketing rather than product.
- **Customer voice in the customer quote.** Use the persona's language (from `pm-persona-codifier` output if available). The quote should sound like the persona, not like a press release writer impersonating the persona.
- **Specific over vague.** "Reduces forecast variance by 40%" beats "improves forecast accuracy." If the number is made up, mark it `[hypothetical metric]`.
- **The "Problem" paragraph is the truth-test.** If you can't write the problem paragraph in concrete, specific terms with a recognizable customer experience, the underlying initiative may not have a real problem to solve. Stop and surface the doubt to the user.

### Step 3 — Draft the Internal FAQ

Target: 10-15 questions. **Honest answers.** This is internal — it doesn't have to flatter the product.

Required question categories (at least 1 from each):

| Category | Example questions |
|----------|-------------------|
| **Customer / persona** | "Why would [persona] adopt this when they already use [incumbent]?" "What changes for [persona]'s daily workflow on day 1?" |
| **Differentiation** | "What can we do that [competitor] can't?" "Why now and not in 2 years when the tech is more mature?" |
| **Business** | "What's the unit economics?" "How does this affect our gross margin?" "Cannibalization risk?" |
| **Execution** | "What's the hardest engineering problem we're betting we can solve?" "Who owns this? What's the team shape?" |
| **Tradeoffs** | "What did we explicitly decide not to build?" "What customer segment are we ignoring?" |
| **Risk** | "What's the most likely way this fails?" "What's the worst-case scenario if our biggest assumption is wrong?" |
| **Reversibility** | "If this is a flop, how fast can we kill it?" "Type-1 or type-2 decision?" |

If the user provides fewer than 10 questions, **generate the rest adversarially** — see Step 4. Don't ask the user for more questions until you've generated adversarial candidates yourself, since the questions the user *wouldn't* think to ask are usually the most diagnostic.

### Step 4 — Adversarial FAQ pass

This is the part that separates this skill from "ChatGPT, write a PR-FAQ."

Switch posture. You are now:
- A skeptical investor on the board who has seen 5 of these launches fail
- A competitor reading this and looking for the gap
- A customer support lead who will get the angry emails when it doesn't work
- A senior engineer who has built systems like this and knows where the bodies are

From each posture, generate 2-3 questions the team would rather not answer. Add them to the FAQ. Answer them honestly.

**Adversarial answer discipline:**

- If the honest answer is "we don't know yet," say that. Don't paper over.
- If the honest answer is "we're betting that [X] is true, and if it's not, this fails," say that. Naming the bet is more credible than hiding it.
- If you can't answer honestly without revealing the initiative isn't ready, surface the doubt to the user. "FAQ question 7 doesn't have a good answer. This may indicate the initiative needs more discovery before this PR-FAQ ships."

### Step 5 — Stress-test pass

Take the completed PR + FAQ and re-read as **the strategic skeptic**. See `references/pr-faq-stress-test.md` for the pattern.

Five questions to score against:

1. **Does the customer benefit pop in the first paragraph?** If a reader skimmed only the summary paragraph, would they understand what the customer gets? PASS / FAIL.
2. **Is the persona recognizable?** Could a sales rep read this and identify which of their accounts maps to this persona? PASS / FAIL.
3. **Does the FAQ admit a real tradeoff?** Or are all answers self-congratulatory? Tradeoffs admitted: list them. If zero, FAIL — go back and add.
4. **What's the riskiest assumption?** Single sentence. If you can't name it, the doc is hiding it.
5. **Would this PR be embarrassing to ship if a competitor wrote a "Why X is Wrong" rebuttal the same day?** If yes, the claims are overstated. Tighten.

If any of 1, 2, 3 is FAIL, revise before delivering. Surface the stress-test grid to the user along with the final doc.

## Output

Write to `pr-faq-<slug>-YYYY-MM-DD.md` under `./INBOX/` if it exists, else the current directory (or ask the user where). Single file containing both PR and FAQ, in that order. Stress-test grid at the bottom under a "Method Notes" section.

```markdown
# PR-FAQ: [Slug]

**Drafted:** YYYY-MM-DD
**Launch date in PR:** [future date]
**Audience:** [internal / investors / mixed]
**Source brief:** [path or "from conversation"]

---

## Press Release

[full PR content per structure above]

---

## Internal FAQ

### Q1. [question]

[honest answer]

### Q2. [question]

...

(10-15 questions total, including adversarial ones)

---

## Method Notes

### Stress-Test Grid

| # | Test | Result | Notes |
|---|------|--------|-------|
| 1 | Customer benefit pops in summary | PASS / FAIL | ... |
| 2 | Persona is recognizable | PASS / FAIL | ... |
| 3 | FAQ admits real tradeoff | PASS / FAIL | tradeoffs: [list] |
| 4 | Riskiest assumption named | yes / no | assumption: [single sentence] |
| 5 | Survives competitor rebuttal | yes / no | ... |

### Open Questions / Known Gaps

[Anything the doc punts on, flagged honestly.]
```

## Rules

1. **Working backwards is the discipline.** The PR comes BEFORE the build, not after. If you find yourself reverse-engineering a PR from features already decided, the discipline is broken. Push back on the user; this artifact is for *not-yet-built* initiatives.

2. **The FAQ must include at least 3 questions the team would rather not answer.** If the FAQ is all soft-balls, the doc is theater. Adversarial questions are non-negotiable.

3. **No "AI-powered" / "intelligent" / "seamless" / "world-class."** These words obscure the actual capability. Replace with specifics or cut.

4. **The fictional customer quote must sound like a persona.** Not like a press release writer. Use language from `pm-persona-codifier` output if available; otherwise pull from interview transcripts.

5. **Made-up numbers get marked `[hypothetical metric]`.** Real numbers cite source. Don't smuggle aspiration in as fact.

6. **The "Problem" paragraph is load-bearing.** A weak problem paragraph means a weak initiative. Surface the weakness — don't paper over it.

7. **Output to `./INBOX/` if it exists, else the current directory** (or wherever the user specifies). In a curated workspace, write only to `INBOX/` and let the user promote.

8. **If the underlying initiative can't sustain a credible PR-FAQ, say so.** "This PR is dangerously thin in the Problem paragraph — recommend more discovery before committing to the launch narrative" is the honest output when warranted.

## Composing With Other Skills

- **Upstream**: `pm-strategy-memo` provides the strategic case for the launch; the PR-FAQ is the future-state translation of that case. `pm-persona-codifier` provides the persona for the fictional customer.
- **Sideways**: `interviewer` (requires the **multiplai-research** plugin) for the context gather if the user is stuck on what the future state actually is.
- **Downstream**: A locked PR-FAQ feeds product planning — the FAQ surfaces requirements and the PR sets experience targets. (A PRD skill and a roadmap skill that would consume it are planned but not yet shipped.)
