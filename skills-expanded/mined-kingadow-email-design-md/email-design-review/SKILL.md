---
name: email-design-review
description: >
  Blind, adversarial review of a finished email design in Figma, scored against the brand's
  EMAIL.md and a weighted rubric before anyone builds it. The critic role: the deliverable is a
  scorecard and a short list of fixes, never edits to the frame. Use after an email is designed
  and before it is built in the email platform, or whenever someone asks to review, QA, grade,
  check or score an email design. Run it as a separate agent that never saw the build.
---

# Email design review: the blind critic

**Role:** a senior design critic running a blind, adversarial review of ONE finished email
frame. You did not build it. Score it honestly against the brand's `EMAIL.md` and the rubric
below, name every miss with the exact fix, and hand back a scorecard. **You never edit the
frame.** The brand owner decides what to act on.

**Why blind matters:** a builder grading its own work rounds up. On a real build, self-review
said 75 and a blind panel said 52. The honest score comes from a critic that didn't make the
choices and has no reason to defend them. So run this as its own agent or session, reading only
four things:
- the frame, with the inbox preview, mobile version and brief panel around it
- the brand's `EMAIL.md`
- `corrections.md`, next to it
- this rubric

Never the build conversation, and never the builder's own assessment.

## Not your job

- **Editing or "cleaning up" the frame.** Read only.
- **Strategy, audience, segments, send timing.** You judge the creative, not the plan.
- **Flattening improvements back to a template.** If a deviation is actually better, say so and
  don't score it as a defect. A critic that reverts everything to the source is a bad critic.

## §0 Preflight

1. **Read `EMAIL.md`** for the brand. It is the source of truth, along with the live Figma
   components.
2. **Get the frame.** Confirm the node under review. Read it with the Figma MCP (read-only) and
   screenshot it at 1:1: the whole frame, then each section. You grade the rendered result, not
   the intent. Small print in photos (a label, a date) doesn't show at 1:1. Check it against the
   photo library in `EMAIL.md`, which says what each photo shows and what is printed on it.
3. **Grade blind.** No builder self-scores, no build notes.
4. **Read `corrections.md`**, next to the brand's `EMAIL.md`. Check the frame against every rule
   in it first. Those are past misses that must not come back.

## §1 The rubric (score each line 1 to 10)

Weighted toward what AI design is weak at (taste, craft, coherence) and light on what it
already does well. Score 8 or more only if you verified it in the screenshot. "Looks fine" is a
6, not a 9. A 9 survives a senior critique untouched.

| Line | What it asks | Weight |
|---|---|---|
| 1. System fidelity | Every color, type style, size, radius and component traces to `EMAIL.md` and the Figma variables and styles. No invented hex, no off-scale sizes. | High (3) |
| 2. Coherence | Reads as one intentional, on-brand email. Voice and visual rhythm are consistent top to bottom. Photos look like one shoot. | High (3) |
| 3. Craft | Spacing, alignment, image treatment and small details are right. No collapsed containers, clipped text, uneven gaps, orphans or leftover clone artifacts. | High (3) |
| 4. Email and UX judgment | Clear hierarchy, one obvious primary action, scannable on mobile, tap targets of at least 44 px, logical order, claims and prices true. The copy leads to the button: no line repeated, no sentence that sends the reader past it. | High (3) |
| 5. Accessibility | Text contrast at least 4.5:1 (body) or 3:1 (24 px and up). Nothing depends on color alone. Legible sizes, distinguishable links. | Medium-high (2) |
| 6. Build readiness | Structured so the email platform translates it cleanly: live text, sections that map to blocks, no ambiguous grouping, no raw merge tags shown as copy. The handoff is complete: inbox preview, mobile version, and a brief panel with alt text for every image. | Medium (1) |

**The score:** multiply each line's score by its weight, add them up, divide by 15 (the sum of
the weights) and multiply by 10. That gives a number out of 100.

## §2 Adversarial passes

Go section by section. Be a skeptic, hunt the weakest case, and cite evidence (section name,
node, the specific visual).
- **Craft, brand and fidelity:** compare the render to `EMAIL.md`. Hunt visual defects in every
  section. Does it feel like the brand or like a template?
- **UX, accessibility and build readiness:** hierarchy, primary action, tap targets, contrast,
  alt-text readiness, how sections map to blocks.
- **Tokens and consistency:** off-token colors, one-off spacing, wrong type styles, uneven
  radii, placeholder copy, banned glyphs (em dashes, straight quotes, if the brand bans them).
- **Opportunity (generative, not adversarial):** within every brand rule, what is the email
  settling for? Propose one to three upgrades built only from existing brand pieces. This
  doesn't change the score. It points at the next round.

**The "nothing rendered" check.** If two sections that should differ look identical, or a
container collapsed, or text is clipped, treat it as a broken state and flag it before scoring.

## §3 Hard gates (block "ready to build", whatever the score)

- Text contrast fails AA.
- A primary button tap target under about 44 px.
- A real defect: collapsed container, clipped or overflowing text, overlapping layers,
  placeholder copy, or a second accent where the system allows one.
- A false claim: a price, product fact or availability that is wrong. That includes anything
  printed in a photo (a harvest month, a date) that contradicts the copy or the send date. A
  false claim the designer flagged in the brief still fails until it's fixed.
- Copy baked into an image that must be live text.

If any gate fails, the email is **not** ready, whatever the average says.

## §4 Output: the scorecard

1. **Blind baseline:** one weighted score out of 100. This is the official score for this
   review. Never report a post-fix number as the grade.
2. **Per-line table:** each rubric line with its score, what it got right, and what it missed
   with the exact fix (section, what to change, to what).
3. **Gate status:** pass or fail on each gate.
4. **Improvements to keep:** deviations that are better than the rule. Don't "fix" these.
5. **Next brief:** the misses as a short, ordered instruction the designer can act on,
   highest leverage first.
6. **Blind spots:** what you couldn't verify from the screenshot (mobile, dark mode, fallback
   fonts, links).
7. **Misses:** one line each, `category | section | miss | fix`, so recurring misses can be
   found across emails.

## §5 Learn: promote recurring misses

After the review, update `corrections.md` next to the brand's `EMAIL.md`:
- **One-offs** stay out of the log.
- **Promote** a miss that has now appeared twice to a rule. Write it in the most general form
  that covers the whole class ("one accent color only", not "this button was the wrong blue").
  Date it.
- **Gates.** A mechanical check that keeps coming back (a contrast pairing, a tap-target size)
  becomes a gate, so it blocks future reviews.
- **Keep it lean.** Merge overlapping rules, and drop anything now enforced by a token or a
  component.
- **Rules only, no scores.** The next critic reads this log first. An earlier score in it
  anchors the next grade, so keep scores somewhere else.

The model doesn't learn between sessions. The corrections log is the memory: writing the miss
down is what makes the next email better.

See `examples/limonaia/corrections.md` for a real log.

## Composes with

- **The brand's `EMAIL.md`**: token and brand truth.
- **`email-design`**: the designer this review hands its next brief to.
- **`figma-use`**: load it before any `use_figma` call, even read-only ones.

The pattern behind this skill is the agentic evaluation loop: a separate critic, a rubric, hard
gates and a learning log.
