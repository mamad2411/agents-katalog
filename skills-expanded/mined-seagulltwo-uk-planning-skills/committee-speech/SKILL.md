---
name: committee-speech
description: >-
  Write the speech you will actually stand up and deliver at a UK planning
  committee, against an application. Use this whenever someone is speaking, or
  might speak, at a planning committee and needs the words — "write my
  three-minute committee speech", "we have two objector slots, split the
  points", "I'm speaking against this application on Thursday", "what do I say
  to the councillors", "help me with my deputation", "how do I object in
  person". Takes the grounds already assembled by the other skills in this repo
  and turns them into timed, speakable objector speeches that move a committee
  toward refusal, deferral, or approval on tighter conditions — selecting the few
  points that can change a vote, framing each as the decision members are
  actually taking, and sequencing them across the speakers without overlap.
  Objector-side by design, and says so. Will not manufacture grounds that are
  not there. England-focused. Not legal advice; no warranty; output requires
  human review.
license: MIT
---

# Committee speech

Somebody has a slot. It is two, three or four minutes, it happens once, and it is heard by
members who may not have read the papers closely. This skill writes what they say.

**A committee speech is a different instrument from a written objection.** The objection is read
at leisure by the case officer, who is paid to read it. The speech is heard once, aloud, under a
clock, by people deciding a dozen items in an evening. So the job is not to compress the
objection. It is to **select** the few points that can move a vote, **frame** each as the
decision the committee is actually taking, and **sequence** them across the available speakers
without repetition.

Adapted from a skill contributed by **JH** — see `CHANGELOG.md`. The speech craft in it is
theirs.

## Scope: this writes objector speeches, and says so

**This skill argues one side.** It is for the person standing up to oppose an application, and
it is written as their advocate. That is a deliberate choice and it is declared here rather than
disguised, because the rest of this repo is careful about neutrality and a reader is entitled to
know where the posture changes.

It is legitimate for the same reason `policy-representation` is: **an objector is a party**, and
writing a party's case at their instruction is not the same act as an analysis skill quietly
taking a side. What would not be legitimate is pretending the output is balanced. It is not.

**The integrity constraint survives the advocacy, and it is the whole of the skill's value:**

- **It will not manufacture a ground.** If the evidence does not support one, it does not get a
  sentence. A speaker who makes a point their own papers do not support has handed the officer a
  correction to make in the reply, in front of the members they were trying to persuade.
- **It will say when the honest ask is not refusal.** Sometimes the realistic outcome is
  deferral, or conditions, and the skill says so rather than writing a refusal demand that the
  committee cannot grant. `planning-balance` is the skill that answers this properly — run it
  where the answer is genuinely in doubt. Telling a user their case is weaker than they think is
  a service; it is also the only way the strong points stay credible.
- **It concedes what is settled**, early and plainly, because that is what buys the right to be
  believed on the rest.

**If you are speaking in support**, the mechanics below all transfer — the clock, the register,
the speaker allocation, the ask in the final two sentences. The stage gateways and the framing
assume you are arguing against, so use them as scaffolding rather than as written, and say
plainly that is what you are doing.

## When to invoke this skill

Whenever someone is about to speak, or is deciding whether to. Nobody says "committee speech
builder" — they say:

- "write my three-minute speech for planning committee"
- "I'm speaking against this on Thursday, what do I say?"
- "we've got two objector slots, how do we split it?"
- "what do I say to the councillors?"
- "help me with my deputation"
- "how do I object in person?"
- "the parish council has a slot — what should our rep say?"

**Do not write the speech first.** The grounds come from elsewhere; this skill turns them into
words. See the next section.

## Where the material comes from

**Compose with the written case. Do not re-derive it.** Speeches built from a fresh analysis
drift from — or contradict — the objection already on file, and the case officer will notice
and say so in the reply. Read what exists, then select from it.

| What you need | Where it comes from |
|---|---|
| **The strongest grounds, already anchored to policy** | `committee-pack-review` — its "if you are minded to refuse" case is exactly this input, each ground carrying its policy and whether it is evidenced or asserted |
| The officer's recommendation and what it turns on | `committee-pack-review` |
| The committee, the slots, the minutes, the registration deadline | `committee-pack-review`, which finds the committee system — see also [`references/council-rules.md`](references/council-rules.md) |
| Any late update sheet | `committee-pack-review` |
| Which considerations are engaged at all | `application-triage` |
| The adopted development plan and how the scheme scores against it | `policy-compliance-assessment` |
| Technical evidence on one ground | the topic skills — `ecological-`, `transport-`, `heritage-`, `flood-`, `noise-representation` |
| The written objection this speech must not contradict | `policy-representation` |
| **Whether refusal is the realistic ask at all** | `planning-balance` — run it where the honest answer matters, which is before promising a speaker that refusal is winnable |
| Current framework policy and its wording | `national-planning-policy` — **verify before citing**; do not quote policy from memory |
| Documents the pack relies on but does not contain | `planning-document-search` |

**If none of that exists yet, stop and build it first.** A speech is the last thing to write, not
the first. Run `committee-pack-review` if the item is at committee — it produces the ranked,
policy-anchored grounds this skill selects from — and come back.

## Gather these before writing

Ask if they are not supplied. Guessing any of them costs the speaker their slot or their
credibility:

- **The reference, site, proposal and stage** — outline, reserved matters, full/householder, or
  an appeal item. **The stage decides what the committee may lawfully consider**, and it governs
  everything else. See [`references/stage-modules.md`](references/stage-modules.md).
- **Which committee, how many objector slots, and how long each gets.** From the council's
  constitution and committee procedure rules — never from assumption, and never from another
  council. They vary by council and by committee tier.
- **The registration deadline, and how to register.** Usually days before the meeting.
  ⚠️ **Never supply a plausible-looking deadline.** A wrong one is acted on; an absent one is
  checked. If you do not have it, say so and send the user to the council's page.
- **The officer's recommendation**, if published — it decides which way the argument runs.
- **Whether the report and agenda are published** — they set out the balance, the conditions and
  the s.106 the speech should engage with.
- **Who is actually speaking.** One confident speaker or a full slate. This governs how the
  material is split, and whether it is split at all.

## Operating principles

1. **Credibility over volume.** One overstated or wrong point, spoken aloud and unchallenged,
   discredits everything around it — and members remember it. Concede what is genuinely settled
   and spend the credibility you save on the points that matter.

2. **Frame every point as the decision the committee is taking.** Members are not marking an
   essay; they are applying a test. Name the test, then show where the scheme fails it. *"This is
   over-development"* is weak. *"Your own design panel called this over-development, and design
   is the very matter you are approving tonight"* is not.

3. **Weight is the currency.** Where nothing compels refusal — which is the usual case — the
   committee is weighing material considerations. Give each point its correct weight and show
   the balance tipping. Get the vocabulary right; see **Planning weight** below.

4. **Time is the hard constraint.** A speaker who overruns is cut off mid-sentence, often before
   the ask. Write to the clock, and put the ask where it will always be reached.

5. **Speak to reach a vote.** End every speaker on a clear ask — refuse, defer, or impose these
   conditions — because a member has to *move* something, and you want to hand them the motion.

6. **Respect the room. Do not lecture it.** Members are experienced decision-makers, and being
   told their own law and duties — *"you cannot"*, *"you must"*, statute quoted back at them,
   appeal costs spelled out as a warning — reads as preaching and puts backs up, which is the
   last thing an objector can afford. Make the same points as help rather than instruction: *"as
   you know, the principle is not in question tonight"*; *"you are, of course, free to take a
   different view from your officer"*. Keep the tone collaborative and let the evidence — above
   all **the council's own advisers** — carry the argument. Any reminder that reasons must be
   recorded for a decision against the officer belongs as a light aside, never as a threat.

## The process

### 1. Fix the stage and its test

Everything follows from it, because the stage decides what members may lawfully consider. Read
the matching module in [`references/stage-modules.md`](references/stage-modules.md) and lift its
test into the opening frame.

**The commonest and most expensive error is arguing at the wrong stage** — re-opening the
principle at reserved matters, where it is settled, or treating landscape harm as decisive at
outline where an unmet-need gateway has engaged a pro-development balance. A speaker who does
this is corrected by the officer in the reply and loses the room.

### 2. Fix the speaking budget

From the constitution: which committee, how many objector slots, how many minutes each. Convert
to a word budget — see **Write to the clock**. This decides how many speeches exist and what
fits in them.

**Do not pad to fill the time.** A tight speech that finishes early is fine. An overrun is not.

### 3. Allocate across the speakers

Give each speaker a distinct job so nothing repeats and the slate runs as one argument:

- **Speaker 1 — the frame.** What, if anything, compels refusal; the light against-the-officer
  aside if it is warranted; and the opening of the balance, which is usually the heaviest ground.
- **Speaker 2 — the heaviest grounds in detail.** Often heritage, design or landscape.
- **Speaker 3 — the remainder, then the fallbacks.** Amenity, safety, ecology; then the case for
  deferral; then the conditions to impose if members are minded to grant.

**One slot only?** Compress into a single speech in the same order, cutting from the bottom —
conditions first, then deferral — until it fits.

**A parish or town council representative usually has their own slot**, and it is a different
kind of speech. The parish is a **statutory consultee**, not a member of the public, and its
standing is the point: it speaks for the settlement and its response is already on the file.
Give it the ground where that standing counts most — local character, cumulative effect,
infrastructure, what the parish said at consultation and whether the report engaged with it —
and do not spend it duplicating an objector.

⚠️ **Never let a later speaker claim an earlier speaker's point with "I".** Three different
people are speaking. Speaker 3 refers back as *"as my first speaker said"* or *"the point
already made"*, never *"the point I raised"*. Getting this wrong makes the slate look
ghost-written, and it is an easy tell.

### 4. Build each speech to the standard shape

This order, running on into later speakers where the budget requires:

**a. What, if anything, compels refusal.** State the narrow category of things that *require*
refusal at this stage and apply it honestly. **Usually nothing strictly compels refusal — say so
plainly.** It buys credibility and it correctly reframes the decision as a matter of weight,
which is the ground the objector can actually win on. Where something does compel refusal — a
mandatory policy bites, a reserved matter departs from the outline permission, a statutory bar —
lead with it, hard.

**b. The against-the-officer aside, if it is warranted.** Where members would be departing from
the recommendation, they carry a duty: proper regard to professional advice, and documented
reasons. Frame it to whichever way the recommendation runs. **Keep it light** — principle 6 —
and do not assert a cooling-off period unless the constitution actually contains one. Many do
not.

**c. The grounds where the balance points to refusal.** The heart of it. For each: name it, give
it its weight, tie it to a named development-plan or framework policy, and show the balance
tipping. **Anchor to independent evidence wherever it exists** — the council's own consultees,
its design panel, its conservation or landscape officer. Members discount an objector's opinion.
They do not discount their own advisers.

**d. Emerging-plan weight, where it arises.** If the applicant leans on a draft allocation: the
**adopted** plan carries full statutory weight under s.38(6); an **emerging** plan carries only
what its stage, its unresolved objections and its consistency with the framework allow. This
cuts both ways and is often decisive at outline. Verify the current framework wording through
`national-planning-policy` before citing it.

**e. Deferral, if time permits.** What is not before the committee that should be: contested
evidence, missing technical information, a site visit, unresolved s.106 heads of terms.
**Deferral is a real objector win and a much lower bar than refusal.**

**f. Conditions, if time permits.** A short list of precise, necessary, enforceable conditions
that would make the scheme least harmful — each tied to a reserved matter, a policy or an
existing condition, and each meeting the six tests. This gives members a constructive route and
seeds the motion if they are minded to grant.

### 5. Check for a late update sheet on the morning

**A speech written to the published report can be obsolete before it is delivered**, and unlike
a written objection there is no chance to correct it. Late items and update sheets are published
separately, often on the morning of the meeting, and can change the recommendation, add
conditions, or answer the objection the speech is built on.

`committee-pack-review` treats these as the most decision-relevant documents in a pack. For a
speaker the practical answer is narrower:

- **Check on the morning**, and say in the deliverable that this needs doing.
- **If nothing has moved**, deliver as written.
- **If the recommendation or a condition has moved, do not rewrite under pressure.** Keep the
  speech and add **one opening sentence** acknowledging the change — *"I've seen this morning's
  update, and my point on drainage still stands because…"*. A speaker reading a hastily rewritten
  script performs worse than one who has practised theirs and adapts a sentence.
- **If the update answers a ground outright, cut that ground** and let the speech run short.
  Arguing against something the council has already conceded wastes the slot and the credibility.

### 6. Quality checks

Run **Quality checks** below before anything is delivered.

## Write to the clock

Speaking pace for a nervous member of the public reading aloud is **130–150 words per minute**.
Budget conservatively so nobody is cut off:

| Slot | Word budget |
|---|---|
| 2 minutes | 260–280 words |
| 3 minutes | 380–410 words |
| 4 minutes | 490–520 words |

**State the word count and the target time in the deliverable** so the speaker can pace
themselves and practise against a clock.

**Put the ask in the final two sentences of every speech.** It is the one place that is always
reached. If the council allows less time than expected, cut from the least essential sentence
upward — never from the ask.

**Write for the ear, not the page.** Short sentences. One idea per sentence. Say *"the church"*,
not *"the Grade I-listed Church of St Mary Magdalene (List Entry 1234567)"*. Quote a policy's
words rather than its number, unless the number itself lands — *"your own design panel called it
over-development"* beats *"contrary to Policy DP26(c)(iv)"*. Open to the Chair and members, close
with thanks.

**No bullet lists inside spoken text.** Nobody speaks in bullets, and a speaker reading one
sounds like they are reading one.

## Cite instruments in full once, then short

The first spoken mention of any instrument — a section of an Act, an article of the
constitution, a development-plan or framework policy, a condition, a Part of the Building
Regulations — carries its source in full, so a member who has not read the papers can place it:
*"Section 38(6) of the Planning and Compulsory Purchase Act 2004"*, *"Policy DP26 of the
[district] Local Plan"*, *"condition 25 of the outline permission"*. After that, drop to the
short form. Repeating the full title turns a speech into a citation list and buries the point.

**Apply this per speech, in the order the room hears it.** A written "how to use" note or header
is not heard, so it does not consume the first mention. Where several speakers share an
instrument, the first to raise it names it in full; later speakers use the short form and
attribute it back rather than re-citing.

## Planning weight — say it accurately

Members apply weight, so misusing the vocabulary is expensive: it is the error an officer can
correct in the reply, in front of the room.

**Verify every weight direction and every policy citation against the framework edition in force
at the decision date, through `national-planning-policy`.** That skill holds the edition
register and the verify-before-citing protocol precisely so individual skills do not carry their
own copies to go stale. Do not quote framework policy from memory, and do not lift a weight
direction from an older objection without rechecking it.

Two things that do not change, and are worth knowing cold:

- **Harm to a designated heritage asset is a matter of considerable importance and weight.** That
  is the statutory duty under ss.66 and 72 of the Planning (Listed Buildings and Conservation
  Areas) Act 1990, as the courts have construed it. It is statute, not policy, so it does not
  move when the framework is rewritten.
- **Development-plan conflict carries full weight through s.38(6)** — the decision is made in
  accordance with the plan unless material considerations indicate otherwise. **Name the specific
  policies.** "Contrary to the local plan" is not a ground; a numbered policy is.

⚠️ **Framework vocabulary changes between editions, and the abolished terms are the ones people
repeat.** A phrase carried over from an old objection, or from guidance drafted against a
superseded edition, is exactly the error that gets corrected aloud. Check the current wording,
every time, rather than trusting a form of words that sounded right last year.

**If a point cannot be tied to a policy or an independent source, it is probably too weak to
spend a speaker's seconds on.** Say so, and drop it.

## Output

**Plain, speakable prose, formatted to be read aloud from paper.** A speaker stands at a lectern
with a printout, so the deliverable is optimised for that: generous line spacing, no bullets
inside the spoken text, nothing that requires scrolling or a second screen.

Structure:

- **A short header** — site, reference, committee, date, and the speaking budget (slots ×
  minutes). This is written matter, not spoken.
- **The registration deadline and how to register**, prominently, at the top — or a plain
  statement that it was not established and must be checked.
- **A one-line reminder to check for a late update sheet on the morning.**
- **Each speech under its own heading** — *Speaker N — [role]* — with its **word count and target
  time** noted.
- **A short "how to use" note** where the slate is meant to be adapted, setting out the decision
  sequence (4a–4f) so the reader can cut it down themselves.

Offer it as plain text where the user wants to paste it into an email to Democratic Services,
which is how many councils require the text to be submitted in advance.

## Quality checks

Before delivering, confirm every one:

1. **Timing.** Each speech is inside its word budget, and the ask sits in the final two
   sentences.
2. **Stage discipline.** Nothing argues a matter foreclosed at this stage. The applicable test
   is named and correctly stated.
3. **No cross-speaker "I".** No speaker claims another's point in the first person.
4. **Weights verified.** Every weight direction and policy citation checked against the current
   framework edition through `national-planning-policy` — not carried over from an older
   document. Every ground tied to a named policy or an independent source.
5. **Quotations verified.** Every quoted phrase — design panel, consultee, the applicant's own
   documents, a policy — checked against its source. Reuse the written objection's verified
   quotations. **Never paraphrase a quotation into something the source does not say.**
6. **Council facts correct.** Committee, slot count, time limit, registration deadline and the
   against-the-officer rule all match that council's current constitution. Not another
   council's, and not an assumption.
7. **Consistent with the written case.** Nothing contradicts the objection already on file.
8. **No overstatement.** Concessions are present and honest. Every "this requires refusal" claim
   is real.
9. **Citations oriented.** First spoken mention of each instrument in full, every later mention
   short.
10. **Respectful register.** No lecturing members on their own law or duties. No "you must" or
    "you cannot". No statute quoted at them. No appeal-cost warnings dressed as reminders.
11. **Update sheet flagged.** The deliverable tells the speaker to check on the morning.

## Stop, or ask

| Condition | Do |
|---|---|
| **No written case or analysis exists yet** | **Stop.** Run `committee-pack-review` (if it is at committee) or `application-triage` → the topic skills first. A speech written from a cold read of the application will contradict the objection on file. |
| **You do not have the registration deadline** | **Say so** and send the user to the council's page. Never supply a plausible date — a wrong one is acted on. |
| **You do not have the slot count or time limit** | Ask, or find the constitution. Do not default to three minutes because it is common. |
| **The grounds do not support refusal** | **Say so**, and write to the realistic ask — deferral, or conditions. Run `planning-balance` where it is genuinely in doubt. Do not write a refusal demand the committee cannot grant. |
| **The user wants a point included that the evidence does not support** | Say why it will not survive the officer's reply, and offer the strongest version that is supportable. It remains their speech and their call. |
| **The user is speaking in support** | The mechanics transfer; the framing does not. Say that, and adapt rather than pretending the skill is neutral. |
| **The meeting is today and the update sheet has not been checked** | **Check, or say plainly that you did not.** |
| **The item has been deferred or withdrawn** | Say so before writing anything. |

## Scope and limitations

- **Objector-side by design**, and stated as such above. Not a balanced appraisal, and not
  presented as one.
- **Not legal advice**, no warranty, and output requires human review before it is delivered.
- **Speaking rules are local and change.** Slots, minutes, registration deadlines and who may
  speak are set by each council's constitution. Read it; do not assume.
- **A speech is a snapshot.** Late items land after it is written — see step 5.
- **England-focused.** Committee procedure differs elsewhere.
- **Third-party personal data.** Name your own speakers if they consent. Report the substance of
  other people's objections, never their names or addresses.

## Pairs with

- **`committee-pack-review`** — run it first. Its refusal case is this skill's input.
- **`application-triage`** — which considerations are engaged, where the item is not at committee
  yet.
- **`policy-compliance-assessment`** — the adopted development plan and how the scheme scores.
- **`policy-representation`** — the written objection this speech must not contradict.
- **`planning-balance`** — whether the assembled case supports refusal, deferral or conditions.
  This skill writes the ask; that one tests whether it is the right ask.
- **`national-planning-policy`** — the framework edition register. Verify before citing.
- **`planning-document-search`** — documents the pack relies on but does not contain.
