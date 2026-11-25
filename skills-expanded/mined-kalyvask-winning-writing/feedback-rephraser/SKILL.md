---
name: feedback-rephraser
description: Rewrites blunt downward or peer feedback as "what I like plus what I would like," focused on the work rather than the person, ideally phrased as a question. Use whenever the user is drafting a performance review, a Slack message to a report, a 1:1 talking point, an HR conversation script, a peer-review comment, or any line where they're tempted to criticize a colleague directly. Triggers on "give feedback to," "tell my report," "perf review line," "stop doing X," "you don't / you're not / you should stop," "smile more," "speak up more," "interrupt less," "less blunt," "burning out," "running late."
---

# Feedback rephraser

Source: `points/performance-review-rules.md` (reframing kit) and `points/core-rules.md` (say what you like + what you would like).

## Why this exists

Blunt feedback feels honest to the giver and burns trust with the receiver. The receiver hears *"you are bad at X"* even when the giver meant *"the work needs Y."* The fix is mechanical: lead with what you LIKE, then what you WOULD LIKE, anchored to the WORK, phrased as a QUESTION where possible.

The principle generalizes across every channel — annual review, Slack DM, 1:1 talking point, peer review comment, HR script. Same rewrite, same rules.

## What to detect

Catch any sentence that does one or more of:

- Addresses a personal trait, not a behavior in the work (*"you don't smile enough," "you're intellectually intimidating," "you're too blunt"*)
- Tells the person to *stop* something without naming what to do instead (*"stop interrupting," "stop being late"*)
- Uses *you are* / *you're too* / *you don't* as the load-bearing verb
- Speculates about the person's emotional state (*"you're burning out," "you don't care"*)
- Mentions personal context the writer hasn't been invited to discuss (*"because of your divorce," "since the baby was born"*)
- Phrases a complaint as a declaration when a question would land softer (*"this isn't working"*)

## The five-move reframe

Every rewrite uses some combination of these moves:

1. **Open with what you LIKE** — at least one named, specific thing.
2. **Re-aim at the WORK** — not their personality, not their emotional state. The deliverable, the meeting, the client interaction.
3. **Convert "stop X" to "I'd love to see more Y"** — frame the positive behavior, not the prohibition.
4. **Phrase as a question** — *"can we talk about how to..."*, *"is it time to..."*, *"worth thinking about whether..."*
5. **Cut all psychoanalysis** — never speculate about why. If you suspect a personal reason, that's a separate, private conversation.

## Reframing table

The patterns that show up most often. Detect any of these constructions and rewrite them.

| Blunt | Reframe |
|---|---|
| *"You don't smile enough."* | *"I noticed in client meetings your enthusiasm for the subject doesn't always show in your face. Worth thinking about whether the room can read what you feel."* |
| *"You're intellectually intimidating."* | *"We all know how smart you are. You have more influence when you add a little self-deprecating humor — it makes you accessible."* |
| *"Stop cutting off your colleagues."* | *"I love a lot of the ideas you share. Give the room more space to get there too."* |
| *"You're not speaking up enough."* | *"In the moments you've contributed, we've all benefited. I'd love to see more."* |
| *"You're too blunt."* | *"I appreciate your candor. To borrow from Mary Poppins, a spoonful of sugar helps the medicine go down."* |
| *"Stop asking so many questions."* | *"I hired you because you're smart. I trust you to figure more things out on your own."* |
| *"I'm sick of you being late on deliverables."* | *"I'd rather you be on time at 90% than late at 100%. Can we talk about how to meet our deadlines?"* |
| *"You're burning out."* | *"I'm concerned about whether you can sustain this pace. Is it time to take a break?"* |
| *"You're disorganized."* | *"Your ideas land best when the writeup is structured. Would a doc template help, or is it more about prioritizing the time?"* |
| *"You don't care about quality."* | *"I noticed the last two ship reviews skipped the checklist. What would make running it the default for you?"* |
| *"This isn't working."* | *"I want to find a version of this that works for both of us. Tell me where it's hardest from where you sit."* |
| *"You're not a team player."* | *"Your output is strong solo. The team benefits when you bring others in earlier — what's the smallest version of that you could try this sprint?"* |
| *"Your divorce is affecting your work."* | Cut entirely from any written feedback. Have a private conversation. *"It's been a tough quarter. Tell me what I can do."* |

## Output format

Two passes, same shape as style-tells.

### Pass 1 — Inventory

```
Blunt phrasings found: N
```

For each occurrence, return:

```
Line N: "the original blunt sentence"
  Detected: trait-attack | stop-without-replacement | psychoanalysis | declared-not-asked | personal-context
  Reframe: "the rewritten sentence"
  Why this lands better: one sentence
```

### Pass 2 — Clean draft

The full text with every blunt line rewritten. No commentary in this section, just the clean text.

If the text is a written review, also flag any line that introduces bad news the writer has not raised before. The rephrase doesn't fix an ambush — the writer needs to discuss it with the person first.

## When NOT to soften

Some feedback should stay sharp. Do not reframe if any of these apply:

- The behavior is a **fireable offense** (harassment, theft, lying to customers) — sharp written record is the point.
- The user is **documenting** rather than coaching — legal / HR context where understatement creates risk.
- The receiver is the user themselves writing a **self-critique** — self-reframing into corporate-speak is often the user dodging their own assessment.
- The user explicitly says *"I want this to be blunt"* or *"this is HR documentation."*

When in doubt, ask the user which context this is in.

## What this skill is not

- **Not a politeness layer.** The reframes are tighter, not softer. They cut filler, replace personality attacks with work-focused asks, and convert declarations into questions. The receiver gets *more* signal, not less.
- **Not a yes-and machine.** If the feedback is wrong on the merits, the reframe won't save it. Flag that and tell the user the underlying claim needs work first.
- **Not for upward feedback in hierarchical cultures** where the issue isn't phrasing but channel — those need a different surface (skip-level, anonymous survey, exit interview), not a rewritten sentence.

## The litmus test

Read the reframe aloud. Would you say it to the person across a coffee table without flinching? If yes, ship. If it still reads like a manager who's annoyed, you stopped at "what I would like" without first naming "what I like." Loop back to move 1.
