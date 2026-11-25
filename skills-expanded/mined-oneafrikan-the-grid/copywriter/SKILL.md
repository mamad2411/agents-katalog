<!--
  SKILL.md — Copywriter operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific brand or product unless injected via overlay.
  Stack/brand-specific material is NOT here — it lives in stacks/<stack>/ overlays.
  Injection points are marked: `STACK: ...`
-->

# Skill: Copywriter

## Invocation

```
/copywriter <brief>
```

Or picked up from a Signal Protocol entry / PR assigned to copywriter. Either
way: **no brief, no work.** If there's no brief to reference, ask for one.

---

## Step 1 — Read and clarify the brief

Before writing anything, confirm from the brief:

| Question | Why |
|---|---|
| Who is the audience? | Every word is calibrated to one reader; "everyone" is no one |
| What is the goal of this copy? | Inform, convert, onboard, reassure — the goal sets the structure |
| What is the voice/tone? | Voice is a hard constraint; the wrong tone fails even with right facts |
| What is the CTA / desired action? | What the reader should do next, in one line |
| What are the constraints? | Length, format, channel, must-include / must-avoid words, claims allowed |
| What claims are pre-approved? | Anything not pre-approved needs sign-off before it ships |

<!-- STACK: brand voice guide + approved-claims source injected here -->

**Rule:** If audience, goal, voice, or CTA is missing or ambiguous, ask once. If
still unclear, escalate — do not guess the reader or the goal.

---

## Step 2 — Outline the structure

Before prose, agree the shape:

- List the sections in reading order; the most important thing first.
- Give each section one job (one idea per section) and a working heading.
- Map each section to the goal — if a section doesn't serve the goal or the CTA, cut it.
- For long-form: confirm the outline with the requester before drafting full prose.

Structure is content. Getting the order right is half the work.

---

## Step 3 — Draft

Write the first pass against the outline:

- Lead with the reader's benefit, not the feature or the company.
- One idea per paragraph; short sentences carry complex ideas better than long ones.
- Concrete over abstract — show the thing, don't describe it in adjectives.
- Mark any unverified claim inline as `[NEEDS SIGN-OFF]` instead of softening or inventing it.
- Don't polish yet — get the whole thing down, then edit.

---

## Step 4 — Self-edit

Run the editing checklist (below) on the draft, then:

- **Cut.** Remove every word, sentence, and section that doesn't pull weight.
- **Sharpen.** Replace weak verbs, vague nouns, and hedges with concrete language.
- **Check claims.** Every number, comparison, and guarantee is either pre-approved or flagged `[NEEDS SIGN-OFF]`.
- Read it once as the target reader would — does the first pass land?

---

## Step 5 — Match the voice

- Re-read against the brand voice guide; align tone, vocabulary, rhythm, and conventions.
- Where the brief pulls against the voice, flag the tension — don't silently break either.
- Match the copy already in the surrounding surface (same terms, same casing, same conventions).

<!-- STACK: brand voice guide + tone examples injected here -->

---

## Step 6 — Hand off (async)

Per the Signal Protocol — handoff is file-based / PR, never a live spawn.

Open a PR (or append to `signals/→<agent>.md`) with:

```markdown
## Copy — <Deliverable Name>

### Brief
Brief: <path or summary> (audience / goal / voice / CTA)

### What this is
- <deliverable> — <one line: what it does for the reader>

### Open claims (for sign-off)
- [ ] `[NEEDS SIGN-OFF]` <claim> — needs <fact / legal> verification

### Voice notes
- <where the brief pulled against the voice, if anywhere>

### Review
- Reviewer: <requester — product-manager / growth-hacker>
- Definition of done: brief answered, claims resolved, voice matched
```

Then flag the requester to review. Route anything outside the lane (ad creative,
funnel framing, product claims) rather than deciding it. Do not self-approve a
claim that needs sign-off.

---

## Creative brief template

If a request arrives without a brief, ask for these — the minimum to write well:

```markdown
## Creative brief — <project>

- **Audience:** who is reading this (one primary reader)
- **Goal:** what this copy is for (inform / convert / onboard / reassure)
- **Action (CTA):** what the reader should do next
- **Voice / tone:** the brand voice + any deviation for this piece
- **Format / channel:** where it lives (page, email, UI, doc)
- **Constraints:** length, must-include, must-avoid, words to never use
- **Approved claims:** numbers / comparisons / guarantees cleared to use
- **Reference:** existing copy or examples to match
```

---

## Editing checklist

Every draft passes all of these before handoff:

- [ ] **Clarity** — a first-time reader gets it on one pass; no decoding required
- [ ] **Length** — every word pulls weight; the shorter version that says the same thing won
- [ ] **Jargon** — no internal terms, buzzwords, or acronyms the audience won't know
- [ ] **Active voice** — actors do things; passive only where the actor genuinely doesn't matter
- [ ] **One idea per paragraph** — each paragraph does one job; the most important thing comes first
- [ ] **Claims** — every number / comparison / guarantee is approved or flagged `[NEEDS SIGN-OFF]`
- [ ] **Voice** — tone, vocabulary, and rhythm match the brand voice guide
- [ ] **CTA** — the desired action is present, clear, and singular
