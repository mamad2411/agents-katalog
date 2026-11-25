---
name: pm-strategy-memo
description: Draft leadership-grade strategy memos using Minto Pyramid (single governing thought → 3-5 supporting arguments → evidence) with a Working Backwards stress-test and a fresh-Claude reader-test before finalizing. Designed for product strategy memos, exec alignment docs, decision memos, positioning memos, and any document that must move a leadership team to a decision. Triggers on "strategy memo", "leadership memo", "exec doc", "alignment doc", "decision memo", "positioning memo", "exec memo", "memo to leadership", "draft a memo", or when the user has a brief, transcript, or thesis and wants to turn it into a memo executives would read. Composes downstream of `interviewer` (context-gather) and `extract-insights` (turn a transcript into a brief) — both from the multiplai-research plugin — and `pm-jtbd-synthesis` / `pm-persona-codifier` (when the memo needs to reference discovery evidence or personas).
---

# pm-strategy-memo

Turn a brief, a thesis, or a pile of context into a memo a leadership team will actually decide on. This is **a decision-forcing artifact**, not an info dump. Every paragraph either moves the reader toward the decision or earns its keep by pre-empting an objection.

The skill enforces three things most strategy memos fail at:
1. **Single governing thought.** One sentence at the top that the entire memo defends. Most memos drift across 3-4 competing claims and lose the reader.
2. **Pyramid discipline.** Supporting arguments under the governing thought; evidence under each argument. No floating paragraphs.
3. **Adversarial pre-flight.** The memo passes a Working Backwards stress-test and a fresh-reader test *before* the user sees it.

## Arguments

| Arg | Description | Default |
|-----|-------------|---------|
| **source** | File path (brief, transcript, prior memo), `--from-conversation`, or stated thesis | *(required)* |
| `--audience` | Who reads it: `leadership`, `board`, `team`, `cross-functional` | ask |
| `--length` | `short` (~600 words / 1 page), `standard` (~1200 words / 2-3 pages), `long` (~2500 words / 4-5 pages) | `standard` |
| `--skip-reader-test` | Skip the fresh-Claude reader test (NOT recommended) | `false` |

## Workflow

This is a 5-step process. Do not skip the stress-test or reader-test — they're what separate a memo from a draft.

### Step 1 — Context gather (5 questions, asked together)

If `--from-conversation`, infer from context. Otherwise, ask:

1. **Primary audience.** Who reads this? Name them or describe their role. Multiple audiences = multiple memos in disguise.
2. **What do they currently believe?** Their starting position. The memo's job is to move them from this to a new position.
3. **What you need them to do after reading.** Explicit ask — approve, decide between options, change a stance, prepare for a follow-up. If there is no ask, this is not a memo; it's a status update. Push back.
4. **Anticipated objections.** What will they push back on? List 3-5. The memo must pre-empt these.
5. **Hard constraints.** Length, register (formal/informal), things you can/can't say, deadline.

After answers come in, restate them back in one paragraph for the user to confirm before drafting. If anything is fuzzy, push back — do not draft on top of fuzzy context.

### Step 2 — Pyramid build

See `references/minto-pyramid.md` for canon. Apply these gates strictly:

1. **Force a single governing thought.** One sentence. Subject-verb-object. No "ands." If you can't write it in one sentence, the memo isn't ready.
   - **Test:** Read the governing thought to someone who hasn't read the memo. Can they restate it back accurately? If not, simplify.
2. **3-5 supporting arguments under it.** Each is a complete claim, not a topic. ("We should reframe our positioning as data-product-factory" is an argument. "Positioning" is a topic.)
3. **Evidence under each argument.** Numbers, customer quotes, prior decisions, competitive data, logical proof. Each piece of evidence is tagged with source.
4. **MECE check:** are the supporting arguments mutually exclusive and collectively exhaustive? If two arguments overlap, merge them. If a key counter-argument has no parallel argument, you're cherry-picking.

Output of step 2: a one-page pyramid sketch, in this format:

```
GOVERNING THOUGHT: [one sentence]

  Argument 1: [claim]
    - Evidence: [...]
    - Evidence: [...]
  Argument 2: [claim]
    - ...
  Argument 3: [claim]
    - ...
```

**Confirm the pyramid with the user before drafting.** This is the highest-leverage check — fixing structure costs nothing here and costs everything once prose is written.

### Step 3 — Section-by-section draft

Apply the `doc-coauthoring` pattern (stolen from the Anthropic skills repo, see `references/section-coauthoring.md` for the local version):

For each section (which corresponds to one argument in the pyramid):
1. **Brainstorm 5-10 ways to make the point.** Different angles, different evidence orderings, different opening hooks. Don't draft yet.
2. **Surface the brainstorm to the user. Let them curate** — pick 1-2 angles, reject the rest, add anything missing.
3. **Draft the section in chosen voice.** Tight prose. No filler. Concrete > abstract. Specifics > generalities.
4. **Cross-reference the anticipated objections** (from Step 1). Does this section pre-empt the relevant one? If not, address it explicitly or move it to its own section.

Memo structure (default):

```markdown
# [Memo Title — 6 words max, states the ask, not the topic]

**Date:** YYYY-MM-DD
**Audience:** [from Step 1]
**Ask:** [what you need them to do, one sentence]

## TL;DR

[The governing thought + the ask, restated in 2-3 sentences. The reader who only reads this section should be able to make the decision.]

## The Argument

[3-5 short paragraphs, one per supporting argument. Each paragraph leads with the claim, then the evidence. No section headers between them in a SHORT memo. For STANDARD or LONG, each argument gets its own H2.]

## Objections (anticipated and addressed)

[For each of the 3-5 anticipated objections from Step 1: state the objection in steelmanned form, then address it. If you can't address an objection in 3 sentences, the objection is real and the memo needs to acknowledge the tension rather than hide it.]

## What I Need From You

[The ask, restated concretely. Decisions to make, by when, what happens next.]

## Appendix (optional)

[Supporting detail too dense for the main body. Methodology, data tables, competitive analysis, prior decision history. Keep main body lean; push depth here.]
```

LONG memos may add: a "Background" section between TL;DR and Argument, an "Alternatives Considered" section before Objections, and a "Decision Log" entry at the bottom recording the meeting outcome.

### Step 4 — Working Backwards stress-test

See `references/working-backwards-stress-test.md` for the full pattern. The short version:

1. Generate the 10 hardest questions a skeptical exec at this audience would ask. Be adversarial — not "what would help them?" but "what would they use to dismiss this?"
2. For each question, locate where the memo pre-answers it. If it doesn't, decide: revise the memo, accept the gap (and add it to Open Questions), or note it as a known-unaddressed in the Objections section.
3. Grade each question: ANSWERED / PARTIAL / NOT ADDRESSED. Aim for 8+ ANSWERED.
4. If &lt; 6 are answered, the memo isn't ready. Revise before reader-test.

Surface the stress-test grid to the user. Two reasons: (a) they may know answers you don't, (b) they should see the test and the gaps before the memo ships.

### Step 5 — Fresh-Claude reader test

Unless `--skip-reader-test true`, run a reader test. See `references/reader-test-pattern.md` for the exact pattern.

Method: spawn a sub-agent (using the Agent tool with `subagent_type: general-purpose`) with no context. Give it ONLY the memo. Ask three questions:

1. **What is this memo asking the reader to do?** (Tests whether the ask is clear.)
2. **Summarize the argument in three sentences.** (Tests whether the governing thought is intelligible.)
3. **What is the strongest objection a reader would have, and does the memo address it?** (Tests whether the memo is robust.)

Compare the sub-agent's answers to the intended ask, governing thought, and addressed objections. Any divergence is a memo defect, not a reader defect.

If the sub-agent gets the ask wrong: revise the TL;DR and What I Need From You sections.
If the sub-agent restates a different governing thought: revise the opening of The Argument.
If the sub-agent surfaces an objection the memo doesn't address: add it to Objections or acknowledge the gap.

After revision, run the reader-test ONE more time. If it still fails, escalate to the user — don't keep revising blindly.

## Output Location

Write the final memo to `strategy-memo-<slug>-YYYY-MM-DD.md` under `./INBOX/` if it exists, else the current directory (or ask the user where).

If the memo went through significant revision, also write `strategy-memo-<slug>-YYYY-MM-DD-method.md` (same location) containing:
- The pyramid sketch
- The stress-test grid (10 questions + grades)
- The reader-test transcript (sub-agent's 3 answers + your read)

This second file is for the user's reference; they can delete it if not needed.

## Rules

1. **No memo without an ask.** If the user can't articulate what they need the reader to do, this is not a memo. Push back and route them to `extract-insights` or `pm-strategy-memo --length short` later when the ask is clear.

2. **One governing thought.** If you find yourself writing "and also," "additionally," or "another reason" in the TL;DR, the memo has multiple governing thoughts. Pick one.

3. **Steelman objections.** When stating an anticipated objection, state it as the smartest version of the critique. Knocking down a strawman makes the memo look defensive.

4. **No throat-clearing.** Cut "It is important to note that," "In recent times," "As you know," "I think it's worth considering" etc. Lead with the claim.

5. **Evidence > vibes.** Every load-bearing claim needs a source. "Customers want trust" is vibes. "5 of 6 customers interviewed in Q2 asked for visible scoring logic before committing — see `INBOX/jtbd-synthesis-2026-05-19.md` cluster 3" is evidence.

6. **The Objections section is where memos earn their keep.** A memo that acknowledges 4 hard objections and addresses them is more credible than a memo that has zero objections. Hide nothing.

7. **Reader-test is not optional.** Skip it only when the user explicitly passes `--skip-reader-test true` and acknowledges the risk.

8. **Output to `./INBOX/` if it exists, else the current directory** (or wherever the user specifies). In a curated workspace, write only to `INBOX/` and let the user promote.

9. **Match the audience's altitude.** A board memo and a team memo differ in what they assume the reader already knows. Don't write up or down — match.

10. **If the brief is thin, surface it.** "I can draft this from the brief but Section 3 will rest on a single quote — recommend more discovery before this memo goes out" is the honest output when warranted.

## Composing With Other Skills

- **Upstream** (both require the **multiplai-research** plugin): `interviewer` for the context gather if the user is stuck on Step 1; `extract-insights` to turn a transcript into a brief if no brief exists yet.
- **Sideways**: `pm-jtbd-synthesis` and `pm-persona-codifier` provide the evidence base that fills Step 3 sections.
- **Downstream**: A locked strategy memo is the input for `pm-pr-faq` (when the strategy implies a launch narrative). (A PRD skill and a roadmap skill are planned but not yet shipped.)
