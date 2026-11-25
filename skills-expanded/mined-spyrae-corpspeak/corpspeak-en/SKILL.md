---
name: corpspeak-en
description: "A joke translator between blunt speech and corporate English. Four modes: blunt to corporate, corporate to blunt (decoder), bullshit density detector, and batch translation of whole emails and threads. Use when the user asks to 'translate this to corporate', 'how do I say this at work', 'what did they actually mean', 'decode this email', 'how much of this is filler', 'corporate speak', or 'corporate bullshit'. For Russian text use corpspeak-ru instead. Do NOT use for: writing a real business email that has to land well, stripping AI slop from text (that is deslop-en), editing copy for publication, or genuinely defusing a live conflict."
version: 1.0.0
license: MIT
---

# Corpspeak EN - the corporate translator

A joke two-way translator: blunt speech into corporate English and back.

The Russian version is `corpspeak-ru`. They are not translations of each other. Russian and English corporate speak fail in different ways and need different idioms.

**The core.** Every utterance carries three layers:

- **proposition** - what was actually said
- **affect** - how annoyed the speaker is
- **implicature** - what is meant but left unsaid

Corporatization keeps the proposition intact, launders the affect through grammar, and buries the implicature. The decoder runs it backwards: it digs out the implicature and puts the affect back.

The comedy comes from **precision**, not density. A translation lands when the original thought is fully recoverable but the output reads like a slide. If the proposition is gone, that is not a translation, it is filler.

---

## Six moves

The generative core. Works on any input, including the ones no dictionary lists.

| # | Move | Mechanism | Example |
|---|------|-----------|---------|
| 1 | **Agent deletion** | remove whoever is at fault | "I forgot" → "it wasn't captured in the tracker" |
| 2 | **Nominalization** | verb becomes noun | "everything broke" → "we're seeing service degradation" |
| 3 | **Hedging** | strip the certainty | "no" → "that feels like a heavy lift for this cycle" |
| 4 | **Parking** | defer the conflict instead of resolving it | "you're wrong" → "let's take this offline" |
| 5 | **Jargon substitution** | plain word becomes business word | "no time" → "I don't have the bandwidth" |
| 6 | **Positive reframe** | failure becomes opportunity | "we blew the quarter" → "the quarter surfaced great learnings" |

Moves stack. The higher the intensity, the more of them land on one sentence.

---

## Intensity scale (1-3)

Default is **2**. If the user names no level, use the second.

**Level 1 - polite.** Ordinary workplace courtesy, no jargon, legible to anyone.
> "I don't know yet, let me find out and get back to you."

**Level 2 - standard corporate.** Jargon, hedging, passive voice. Recognizable but still functional.
> "I don't have visibility into that. Let me check with the owner and come back with an update."

**Level 3 - the BigTech slide.** Maximum density, frameworks, workstreams, process references. Meaning is at the edge but still recoverable.
> "Team, I don't have full visibility on this one. I'd suggest we park it as a separate workstream, prioritize it in the next planning cycle, and I'll circle back with an update once I've synced with the domain owner."

**The level 3 rule:** density rises, the proposition survives. Word salad with no proposition is not funny, it is just empty.

---

## Mode 1: BLUNT → CORPORATE (primary)

Triggers: "translate this to corporate", "how do I say this at work", "make this presentable".

**Steps:**

1. Extract the proposition: what the speaker actually claims or demands.
2. Read the affect: irritation, despair, contempt, exhaustion, indifference. Affect decides which moves fire.
3. Identify the target, if there is one. "You're an idiot" and "this code is idiotic" translate differently: the first goes to "I have questions about the decision-making process", the second to "this module needs refactoring before handover".
4. Stack the moves per intensity level.
5. Check reversibility: can the original thought be recovered from the output?

**Output:** one line at the requested level. If no level was named, give three variants marked 1/2/3.

```
Input:  fuck if I know

1 → I'm not sure, let me check.
2 → I don't have visibility into that, it sits outside my area.
3 → Team, I don't have full visibility here. I'd suggest routing this
    to the domain owner and circling back with an update.
```

```
Input:  I don't give a shit, do whatever you want

1 → I don't have a preference, your call.
2 → I don't hold a strong view here, I'll defer to the team.
3 → No blockers from my side. I think this decision is best made at
    the team level - you're closer to the context.
```

```
Input:  who the hell wrote this, nobody can maintain it

1 → This code is hard to maintain, worth a look together.
2 → I have some concerns about the maintainability of this module.
    Worth walking through it with the author.
3 → The review surfaced some maintainability risk in this module.
    I'd suggest we capture it as tech debt and prioritize it in the
    upcoming planning cycle.
```

---

## Mode 2: CORPORATE → BLUNT (decoder)

Triggers: "what did they actually mean", "decode this", "translate from corporate".

**Steps:**

1. Find the hedge and work out what it is covering.
2. Restore the agent: who is the real subject in the agentless sentence.
3. Unwind nominalizations back into verbs.
4. Dig out the implicature: what they meant but did not say.
5. Put the affect back into plain speech.

**Output:** the blunt version plus one "Bottom line" about what is actually wanted.

```
Input:  Let's circle back on this after planning
Output: Never.
Bottom line: the question is closed, there will be no discussion.
```

```
Input:  Interesting idea, let me think about how we'd implement it
Output: No.
Bottom line: a refusal, but with nothing in writing.
```

```
Input:  There are some nuances to how this works
Output: It doesn't work.
Bottom line: you're expected to figure it out and not ask in public.
```

```
Input:  I'd like to sync to level-set expectations
Output: You did the wrong thing.
Bottom line: prepare to explain yourself, and not over email.
```

---

## Mode 3: bullshit detector

Triggers: "how much of this is filler", "is this bullshit", "break down this email".

**The metric.** `Bullshit Density = sentences with no new fact / total sentences × 100%`

A sentence carries a fact if it contains at least one of: a number, a date, a name, a concrete action with a subject, or a checkable claim. Everything else is connective tissue.

| BD | Diagnosis |
|----|-----------|
| 0-20% | a normal working email |
| 20-50% | standard corporate, survivable |
| 50-80% | filler email, the real content is one paragraph |
| 80%+ | cover-your-ass, the facts are missing on purpose |

**Output:**

```
Bullshit Density: NN%  [diagnosis]

What was actually said:
- [fact 1]
- [fact 2]

Red flags:
- "[quote]" → [what it means]

Bottom line: [what they want from you]
```

---

## Mode 4: batch

Triggers: a whole email, a thread, a long message.

1. Keep the structure: subject, greeting, paragraph breaks, sign-off.
2. Translate by paragraph, not by sentence, or the connective logic dies.
3. Never touch names, numbers, dates, system names, or links. They are the anchors the comedy hangs on.
4. Do not normalize length. The corporate version runs 2-3x longer than the original, and that is part of the joke. The reverse runs 5x shorter.
5. In a thread, preserve who is replying to whom.

If the user names no direction and the input is obviously corporate, run the decoder (mode 2). That is almost always what they want.

---

## Lexicon: register calibration

Not a lookup table. Apply the moves to the actual sentence first; come here to catch the tone. Extended version in `references/lexicon.md`.

**Not knowing**

| Direct | Corporate |
|---|---|
| fuck if I know | I don't have visibility into that |
| how would I know | I'm not the right owner for this one |
| nobody knows how this works | the documentation could use a refresh |

**Saying no**

| Direct | Corporate |
|---|---|
| no | that feels like a heavy lift for this cycle |
| that's nonsense | I'd want to pressure-test the assumptions here |
| you're wrong | I have a slightly different read on this |
| I'm against it | I'd like to register a dissenting view |

**Pushback**

| Direct | Corporate |
|---|---|
| stop moving the date | I'd like to lock a firm date |
| you promised and didn't deliver | I'm seeing a gap against what we agreed on [date] |
| did you even read what I sent | my earlier note may have gotten buried in the thread |

**Bad news**

| Direct | Corporate |
|---|---|
| everything is broken | we're seeing degraded service |
| we won't make it | there's timeline risk, we should revisit scope |
| I screwed up | a gap was introduced during implementation |
| we're all getting fired | the org is being restructured for efficiency |

**Indifference and scope defence**

| Direct | Corporate |
|---|---|
| I don't care, do whatever | no blockers from my side, I'll defer to the team |
| figure it out yourselves | I'll let your team take ownership on this |
| not my job | that sits outside the current scope |
| I don't have time | I don't have the bandwidth this sprint |

**Register markers.** Nouns: bandwidth, scope, ownership, visibility, alignment, blocker, learnings, workstream, appetite, lift, signal. Verbs: circle back, sync, align, socialize, action, unpack, park, escalate, level-set, double-click, loop in, take offline. Cushions: "just to level-set", "help me understand", "I want to make sure I'm tracking", "from my side", "as a next step", "I'll follow up with an update".

One or two markers per sentence. More than that reads as parody rather than translation.

**Standing euphemisms (for the decoder)**

| Written | Means |
|---|---|
| let's circle back on this | never |
| interesting idea | no |
| there are some nuances here | it doesn't work |
| this needs further exploration | nobody has looked at it |
| we should sync on this | you did the wrong thing, and not over email |
| a decision was made following discussion | decided without you |
| as part of an efficiency initiative | layoffs |
| we've heard your feedback | nothing will change |
| aggressive timeline | impossible timeline |
| we're operating with high ambiguity | nobody knows what's happening |
| let's not escalate this | don't tell my manager |
| great question | I don't know |
| we're working on it | we haven't started |
| per my last email | read the thing I already sent you |
| just following up on this | you have been ignoring me |
| with all due respect | with no respect whatsoever |
| for visibility | I am creating a paper trail |
| adding [name] for awareness | I am telling your manager |

---

## What kills the joke

| Mistake | Symptom | Fix |
|---|---|---|
| Lost proposition | the original thought can't be recovered | put the specifics back |
| Merely polite | "I'm not sure" instead of corporate | add moves 2, 4, 5 |
| Collapse | every angry input yields "let's sync on this" | hold the concrete object: code, deadline, person, process |
| Lost target | "you're an idiot" and "this code is idiotic" come out the same | step 3 of mode 1 |
| Profanity in corporate output | any obscene root survives | zero exceptions, mode 1 output is always clean |
| Empty level 3 | word salad with no meaning | density rises, proposition stays |
| Explaining the joke | "here I applied agent deletion" | return the result only |

---

## Output Format

Always return **the translation only**, with no breakdown of the moves. Explain the mechanism only when asked.

```
Mode 1 (level named):     one line
Mode 1 (no level named):  three lines, marked 1 / 2 / 3
Mode 2:                   blunt version + "Bottom line" row
Mode 3:                   the metric block (template above)
Mode 4:                   the whole document, structure preserved
```

---

## Smoke test

Run this after editing the skill. If an output collapses into a generic phrase, the collapse guard is broken - fix step 3 of mode 1.

```
input:  this deadline is fantasy, we physically cannot ship by then
output: The current estimate doesn't line up with the release date.
        I'd suggest we either cut scope or move it a sprint.

input:  this crap fell over in prod again, third time this week
output: Flagging a third incident on this service this week. I'd
        suggest we treat it as systemic rather than one-off.

input:  Team, I suggest we revisit this after the planning cycle
output: Never.
        Bottom line: the question is closed, there will be no discussion.
```

## Boundaries

The skill is a joke and takes profanity as input. That is linguistic material, not abuse.

What it does not do:

- write abusive messages aimed at a named living person; the decoder returns meaning, not ammunition
- translate a real business email that actually has to be sent
- genuinely strip filler from text (that needs an editor, not a translator)
