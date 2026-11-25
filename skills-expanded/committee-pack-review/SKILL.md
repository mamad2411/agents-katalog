---
name: committee-pack-review
description: >-
  Scrutinise a planning application that is going to, or has gone to, planning
  committee. Use this whenever someone asks to analyse, review, scrutinise,
  challenge or understand a committee report, an officer's report, a committee
  agenda or pack, or an application going before members — however they phrase
  it, and without their having to name this skill. Also use it when someone
  gives only an application reference and council and the application turns out
  to be at committee stage. Finds the committee meeting and its documents on the
  council's committee system (not the planning portal), identifies the item,
  triages whether it repays scrutiny, tests the officer report and the
  load-bearing claims it rests on, catches the late addenda that change a
  recommendation, recovers the representations that carry planning weight and
  anchors each to a named policy, and ends with independent cases for approval
  and for refusal. Deliberately does not strike a balance. Works to the meeting
  deadline. England-focused. Not legal advice; no warranty; output requires
  human review.
license: MIT
---

# Committee pack review

A planning committee pack lands a few working days before the meeting: one agenda, several
applications, often several hundred pages, and a hard deadline that is the meeting itself.
Somebody — an objector who has a speaking slot, a member reading it the night before, a
parish council deciding whether to send someone, a reporter — has to work out **which items
matter and what is wrong with them**, in the time available.

This skill does the pack-level work: **find it, split it, triage it, interrogate it, and
arm the reader.**

## When to invoke this skill

**Do not wait for the user to say "committee pack", or to name this skill.** Nobody outside
this repository uses that phrase. People say they have *a planning application*, *an officer's
report*, or *a committee meeting coming up*, and the skill has to be reachable from the words
they actually use.

Invoke it when someone asks to analyse or scrutinise an application that is, or may be, before
a planning committee. Requests that should land here:

- "analyse this planning application" — where it turns out to be at committee
- "review the officer's report" / "is the officer report sound?"
- "what do you think of the committee report?"
- "are there grounds to challenge the recommendation?"
- "help me prepare for planning committee"
- "I'm objecting to an application going to committee"
- "the council is recommending approval — what's wrong with it?"

### First, establish whether it is actually at committee

Given only a reference and a council, **find out before choosing a workflow.** Guessing sends
the user down a path that costs them time they may not have. Four checks, cheapest first:

1. **Is there an officer report at all?** This is the strongest signal. Delegated decisions do
   not get one. A published committee report means the application is going to members.
2. **The portal case page** often states the decision level — "Committee" rather than
   "Delegated" — or names a committee date, under a delegation, decision-level or case-status
   field. Vendor-specific, so check the profile in `planning-document-search`.
3. **The council's committee system** — search forthcoming agendas for the reference. See
   [`references/finding-the-pack.md`](references/finding-the-pack.md); this is a different
   hostname from the planning portal.
4. **Minutes**, where it has already been heard.

### Then route

| What you find | Use |
|---|---|
| A committee meeting with its pack published | **This skill.** |
| Going to committee, pack **not yet published** | The ordinary application workflow **now** — `planning-document-search` → `application-triage` → the assessment skills. Then say the pack is due, give the date if known, and flag that the **speaking-registration deadline usually falls before the pack is read**. Come back to this skill when it lands. |
| A live application with no committee in prospect | `planning-document-search` → `application-triage` → the relevant assessment and representation skills. |
| Already decided at committee | This skill still works, retrospectively, on the pack that was before members — but say the decision has been taken, and do not present the output as something that can still be acted on. |
| Cannot establish which | **Ask.** One question — "is this going to committee, or has it been decided under delegated powers?" — beats running the wrong workflow against a deadline. |

**Where both exist, use both.** The committee pack is what members have; the portal holds the
application documents the pack relies on and often does not contain. Take the committee
material through this skill and retrieve the rest with `planning-document-search`, labelling
anything from the portal as **outside the pack** — see the integrity rules.

## Working one step at a time

When the user asks to work through this skill step by step — and it is a good way to use it —
the interaction changes, not the method:

1. **Do the current step only**, then stop.
2. **Show the evidence**, not just the conclusion: what was retrieved, what it says, quoted.
3. **Say what could not be established**, explicitly, rather than passing over it.
4. **Ask before starting the next substantive step.**
5. **Never silently run the whole workflow and present a finished conclusion.** That is the
   failure this mode exists to prevent.
6. **Keep four things visibly apart** at every step: what the papers say, what the officer
   concluded from them, what this skill finds, and what the user's own position is. They
   blur fastest in conversation, where the user's view arrives mid-way and starts colouring
   the findings.

**One exception, and it overrides the pausing.** Deadlines are surfaced in full at the first
step, complete, without waiting to be asked. The speaking-registration cut-off is typically
days before the meeting, and a step-by-step run that reaches it on step five has cost the user
the only thing they could still act on. Everything else can wait for "carry on"; that cannot.

## Orientation: forensic and advocatory, not balanced

Two things about this skill's stance, and they are the whole of its character. Get them
wrong and the output becomes another version of the officer report.

**It is forensic.** The officer report is the council's case for its own recommendation, and
it is written to be adopted. This skill reads it as a document to be tested, and the output
is expected to say what is wrong with it: defects, omissions, internal conflicts,
unevidenced assertions, policies listed but never applied, alternatives not considered,
consultee positions characterised in the summary differently from the appendix. Finding
none of that on an item is a legitimate result, and must be reported as such — but the
search is the job, not an optional extra.

**It is advocatory, and it does not balance.** The output ends with two cases per item — the
strongest available case for approving, and the strongest available case for refusing —
**built independently of each other**. Neither is moderated by the other, neither concedes
to the other, and there is no closing paragraph weighing them up. A reader who wants a
balance already has one: the officer report contains it, and
`policy-compliance-assessment` and `planning-balance` produce one properly.

**Assume the reader already has the facts.** Committee members get a fact pack; objectors
have read the report. Do not spend the output re-describing the scheme. Spend it on what
the reader cannot get from the papers: what the papers do not say, what they contradict,
what each side's best case actually is, and which of the public's objections have policy
behind them.

The three combine into one instruction: **test the papers, then arm both sides.** If the
output could be dropped into the officer report without anyone noticing, it has failed.

## What this skill is not

Four neighbouring skills in this repo do work this one deliberately stops short of, and each
should be used in preference to improvising its method here:

| For | Use |
|---|---|
| What is wrong with one officer report, ranked | `planning-report-critique` |
| How good one assessment is, assertion by assertion | `planning-report-quality` |
| The development-plan scoring | `policy-compliance-assessment` |
| A struck planning balance | `planning-balance` |

Declare them; never restate their method here. This skill's own contribution is everything
**above** the single report: the pack as an artefact, the triage decision about where the
reader's limited attention goes, and the two advocacy cases at the end of it.

**It does not re-analyse an officer report in depth.** Triage flags the items that repay a
close read, and this skill then reports what the papers do not settle on each. A full
assertion-by-assertion audit of a single report is `planning-report-quality`, and the ranked
defect list built from it is `planning-report-critique` — hand a flagged item to those rather
than half-performing their method inside a pack review.

**It is also not `councillor-fact-pack`.** That skill (proposed, issue #39) is for a
*decision-maker*, and carries the predetermination and costs constraints a member is under.
It supplies the facts; this one assumes the reader already has them and goes after what the
facts do not settle. If the reader is a committee member, use both — fact pack for the
grounding, this for the interrogation.

**And it is not a balancing exercise.** Producing "on balance, the scheme is acceptable" is
the officer's job and has already been done in the papers the reader is holding. Two
independent advocacy cases is a different product, and the moment they start conceding to
each other it reverts to being the same product, done worse.

## The deadline is the meeting, and it changes everything

Every other skill in this repo works to "before the application is determined", which is
weeks. A committee pack works to a fixed hour, usually **five working days** after
publication, and often less once addenda appear.

Three consequences that shape the whole method:

- **Triage is the product.** A twelve-item agenda where two items matter is the normal case.
  Saying which ten can be skipped is worth more than a thorough read of all twelve.
- **Report the deadlines first, before any analysis.** A brilliant critique delivered after
  the speaking-registration deadline has closed is worthless. Deadlines go at the top of the
  output, not the bottom.
- **State the time cost of what you recommend.** "This item repays an hour" is actionable;
  "this item is complex" is not.

## Step 1 — Find the agenda and the documents

Full recipes, platform by platform, are in
[`references/finding-the-pack.md`](references/finding-the-pack.md). In outline:

1. **Identify the council's committee system.** It is *not* the planning portal — committee
   business sits on a democratic-services platform, usually **ModernGov** or **CMIS**, on a
   different hostname. The planning portal registry in `planning-document-search` does not
   cover these.
2. **Find the planning committee**, then the meeting. Councils run more than one planning
   committee (a district-wide one and an area one, say), and the item you care about is on
   exactly one of them.
3. **Take everything the meeting page offers, not just the pack** — see Step 2, because the
   thing that changes the recommendation is usually not in the pack.
4. Record what you retrieved and when. A pack is a snapshot; addenda land after it.

**If you cannot find the meeting, stop and say so.** Do not review last month's pack because
this month's is not published yet — say it is not published, and give the date it is due.

## Step 2 — Take the whole meeting, not just the reports pack

**This is the step most likely to be got wrong, and the failure is silent.** The main pack
is published first and is the biggest document, so it reads as "the pack". It is not the
whole of what the committee will consider.

Collect, and record which of these exist:

- **Agenda frontsheet** — the running order, and the procedural items.
- **Public reports pack** — the officer reports, usually as one combined PDF.
- **Individual item reports**, where the council publishes them separately.
- **Addenda / late items / update sheets** — ⚠️ **the single most decision-relevant documents
  in the pack, and they are published separately and late.** An addendum can change the
  officer recommendation outright, add conditions, report a consultee response received after
  the report was written, or answer an objection. A review based on the main report alone can
  be confidently, publicly wrong about what the committee is actually being asked to decide.

  **Do not identify these by keyword alone.** They are titled differently at every council —
  *Addendum*, *Agenda Update Sheet*, *Late Items*, *Update Sheet*, *Supplementary Agenda* —
  and a search for "addendum" misses an "Agenda Update Sheet" completely. Two safeguards:
  - **Work from the document list, not a word list.** Every document on the meeting page that
    is not the agenda frontsheet, the reports pack, the minutes, a map, or an item report is a
    candidate. Read its first page and decide what it is.
  - **Keyword search second**, as a net rather than a filter: `addend`, `late`, `update`,
    `supplementar`, `additional`, `further`.

  An addendum that only rewords a conclusion still matters. Changing "significant harm" to
  "unacceptable harm" is not tidying — it changes which policy test the conclusion is
  expressed against, and a reader working from the main report alone has superseded wording on
  the paragraph that decides the issue.
- **Appeals/decisions sheet**, where one is published — useful context on what the council
  has recently lost.
- **Minutes of the previous meeting**, where an item was deferred.

**Check for addenda again on the morning of the meeting.** Note the time you checked in the
output. This is not optional politeness — it is the difference between a current review and
a stale one.

## Step 3 — Split the pack into items

Councils on the *same platform* publish in materially different shapes, so detect rather
than assume:

- **Per-item PDFs.** Each item is its own document, usually named with the agenda item
  number and the application reference. No splitting needed; map item number → reference →
  documents.
- **One combined pack.** The reports run consecutively in a single PDF. Split on the item
  boundaries — the agenda frontsheet gives you the running order and the references to look
  for, and each officer report restarts with its own header block.

Either way, produce an **item map** before reading anything: item number, application
reference, site, recommendation, page range or document. Everything downstream indexes off
it, and it is what makes the review checkable.

**Reconcile the map against the agenda frontsheet.** If the frontsheet lists nine planning
items and you have eight, you have lost one — most likely to a split that ran two reports
together. Say so rather than reporting on eight.

## Step 4 — Triage

Score each item for how much scrutiny it repays, and **say which items do not repay any**.
An agenda where every item is flagged as important is a failed triage.

The things that make an item repay reading, in rough order of how often they matter:

- **The recommendation is contested** — officer recommends approval against a parish
  objection, a consultee objection, or a large volume of representations; or recommends
  refusal against an applicant's case.
- **A departure from the development plan**, or an application of the tilted balance or its
  successor.
- **An addendum exists** — somebody thought something needed saying after the report was
  written.
- **The balance is finely expressed.** Officer language that hedges — "on balance", "marginal",
  "finely balanced" — is a reliable marker that the decision could go either way, which is
  exactly where a committee's attention is worth spending.
- **A deferral returning**, or a second bite after an appeal.
- **Scale or sensitivity** — major development, a designated asset, a site the council has
  lost an appeal on before.
- **Signs the report itself is weak** — policies listed but never assessed, benefits relied
  on in the balance but secured by nothing, a consultee's position characterised differently
  in the summary than in the appendix. Do not audit every report for these; use them as
  triage signals for deciding which items earn a close read, and hand the flagged items to
  `planning-report-critique` rather than auditing every report here.

## Step 5 — Work each flagged item forensically

Only the items triage flagged. Four passes, and the order matters: the first three produce
the material the advocacy cases are built from, so do not write the cases first and then go
looking for support.

### 5a. Interrogate the report

Read it as a document making a case, not as a statement of the position. What to look for,
with a verbatim quote required for anything asserted:

- **Assertions carrying no evidence** — a conclusion with no consultee, no submitted
  assessment and no reasoning behind it.
- **Policies cited but never applied.** A list of policy numbers in a "policy context"
  section that never reappear in the assessment is a common shape, and it means the
  development-plan test was not actually performed on those policies.
- **Internal conflicts** — the summary and the assessment reaching different conclusions,
  or a consultee's position softened in the précis relative to their actual response.
  Compare the summary against the appendix rather than trusting either.
- **Statutory duties not discharged.** Where a duty applies, the report must show it was
  performed, in terms. Heritage is the recurring case, and silence is the finding.
- **Missing material.** Documents the report relies on that are not in the pack;
  consultations still outstanding; a matter deferred to a condition that the condition as
  drafted does not actually secure.
- **Alternatives not considered** — an option on the table that the report does not engage
  with, including one the applicant offered or an objector proposed. Record the alternative
  and the fact that the report is silent on it; do not construct an appraisal of it.

Where an item yields several of these, hand it to `planning-report-critique` and cite its
findings rather than reproducing its method here. A full assertion-by-assertion audit is a
different exercise from a pack review, and it should be done properly rather than
approximated in a paragraph.

### 5b. Locate the weighting pivots

**This is the pass that makes the advocacy cases real, and it is the one most often
skipped.** Members can lawfully place different weight on the same material considerations
as the officer, and reach a different conclusion on the same facts without anything in the
report being wrong. An output that only reports errors implies, falsely, that a member who
finds no error has no route to a different decision.

So separate the officer's weightings into two kinds:

- **Weight fixed by law or national policy** — where an authority must give a stated weight
  to something, a member does not have a free hand. These are the ones where a different
  weighting is not simply a different view. Say which they are and what they require.
- **Weight at large** — everything else. How much a housing contribution counts, how much
  landscape harm outside a designation counts, how much an unevidenced amenity concern
  counts. Here the officer has made a **judgement**, not applied a rule, and a member may
  make a different one.

For each pivot, record four things:

1. **The officer's chosen weight, quoted** — "limited weight", "significant weight",
   "moderate adverse". Quote it, because the adjective is the decision.
2. **Whether it is fixed or at large**, and on what authority if fixed.
3. **What is on the file that supports weighting it differently** — an objection, a
   consultee comment, an inconsistency with how the same consideration was weighted
   elsewhere in the same report or at the same council. If nothing on the file supports a
   different weighting, say that.
4. **Whether the conclusion turns on it.** A pivot that could move two notches without
   changing the outcome is worth less of the reader's attention than one where a single
   step flips the balance. Say which this is.

State it as the mechanism it is: *"The report gives the housing contribution significant
weight. That weight is a judgement, not a requirement, and the balance as expressed turns
on it."* That is a fact about the report's structure — not a forecast, and not a
recommendation.

**The limit, and it is a hard one.** Re-weighting a material consideration is open to a
member. **Treating an immaterial consideration as material is not**, and neither is
disregarding a statutory duty or a weight the law fixes. Where an objection rests on
something that is not a material planning consideration — loss of a private view, property
values, competition with an existing business, the identity or conduct of the applicant —
say so plainly at this point. That is not dismissing the objection; it is telling the
reader which of their concerns the committee is permitted to act on.

### 5c. Test the applicant's claims the recommendation rests on

**Required wherever the report relies on submitted technical evidence, and the larger the
application the more of this there is.** On a major scheme the officer's conclusions on noise,
biodiversity, landscape, transport, daylight, drainage, air quality and viability are each
built on a document the applicant commissioned and paid for. The report cites them; it rarely
distinguishes between a claim a consultee has tested and a claim it has merely received.

**Never score from the applicant's own account of their scheme** — and that principle
reaches the applicant's evidence, not only their description of development. It is not
fraudulent and it is not usually wrong; it is **advocacy in technical form**, produced to
support an application, and the committee is entitled to know which of the report's
conclusions depend on it.

**What this pass is not.** It is not a re-run of the technical work. Do not say the noise
assessment is wrong, recompute a biodiversity metric, or dispute a traffic count. The skill
has no basis for any of that and doing it would breach rule A. **Say what the claim is, what
depends on it, who tested it, and what question would test it.** The reader does the rest.

**Pick the load-bearing ones and stop.** Three or four on a major application, often none on a
householder one. A claim earns a place only if the recommendation moves when the claim moves.
An inventory of every submitted document is not this pass and buries the ones that matter.

For each, record five things:

1. **The claim, quoted or closely paraphrased**, and the document it comes from — "the
   submitted BNG metric sets out…", "the transport assessment concludes…".
2. **Whose claim it is.** The applicant's consultant, by discipline, never by name. A claim
   made by the council's own officer, a statutory consultee or an independent reviewer is a
   different kind of fact and belongs in a different row.
3. **What in the report depends on it.** Name the conclusion, and the paragraph. If nothing
   does, it is not load-bearing and does not belong here.
4. **Who tested it, and how far.** This is the field that does the work, and it has more
   states than two:
   - **Independently verified** — a consultee with the remit examined the evidence and says so.
   - **Accepted without examination** — "no objection" recorded against a document, with
     nothing showing it was interrogated. Silence from a consultee is not endorsement.
   - **Hedged acceptance** — the consultee's own wording qualifies it: "sufficient information
     **at this stage**", "**appears** to be low risk", "no objection **subject to** a condition
     that defers the real question". Quote the hedge; it is the consultee telling the reader
     how far they went.
   - **Untested** — nobody with the relevant expertise has commented at all.
5. **The question that would test it.** One question, answerable at the meeting or by a
   condition. Not a demand for more work in general.

Four shapes recur and are worth looking for by name:

- **A modelled future presented as a finding.** Predicted noise levels, predicted trip
  generation, predicted water consumption. These are forecasts about the scheme's operation,
  and the assumptions behind them decide the answer. Ask for the assumption, not the number.
- **A benefit in the balance that nothing secures.** A public benefit weighed against harm but
  attached to no condition and no obligation is a claim, not a commitment. This is the single
  most common instance and the easiest to check: read the benefit, then look for it in the
  conditions and the heads of terms. **Say plainly when it is not there.**
- **A gain deferred to a post-permission condition.** The benefit is counted now and the
  document proving it arrives later. That is lawful and routine; it also means the committee
  is weighing a promise. Say which it is.
- **An impossibility asserted rather than demonstrated** — "on-site mitigation is not
  possible", "no alternative access is achievable". These close off options, and they are
  usually the applicant's position adopted into the report's voice.

### 5d. Work the community representations on their merits

**Required for every flagged item, as its own section.** Objectors write in ordinary
language about real effects, and the report summarises them in a paragraph that routinely
loses the two or three that have genuine planning force. Recovering those is one of this
skill's most useful outputs, and nobody else in the pack is doing it.

Method:

1. **Read the representations themselves** where the pack reproduces them, not only the
   officer's summary of them. Where only the summary is in the pack, say so — the summary
   is the council's characterisation, and working from it alone is a coverage limitation
   that must be stated.
2. **Group them by the concern raised**, not by who raised them. Volume is not weight, and
   forty letters making one point is one point — but it is also evidence that the point is
   locally contested, which is itself a fact worth reporting.
3. **Rank them by planning merit**, and say what merit means here: a concern is strong to
   the extent that it attaches to a specific policy, is supported by something on the file,
   and is not already secured or answered elsewhere in the papers.
4. **Anchor each one to a specific policy** — an adopted development plan policy by its
   number, or a national policy by its code. This is the point of the section. A member who
   thinks the community has a point needs the policy in front of them, by number, so they
   can say it out loud in the chamber. "Residents are concerned about traffic" is not usable
   at committee; the local plan's transport policy, cited, is.
5. **Say which do not have a planning anchor**, and why — not material, or material but
   already conditioned, or contradicted by a consultee with the remit. Do this respectfully
   and factually. A reader who is told which of their points will not land is better served
   than one who is told they all will.
6. **Note where the report does not engage** with a representation that does have an anchor.
   Recording an objection is not answering it, and the difference is a finding.

Handle the same way any supporting representations, and any parish or town council
response. **A parish council is a statutory consultee, not a member of the public** —
report its position separately and never fold it into a volume count.

Per house rule 1 and the personal-data rule below: report the substance, never the
identities.

### 5e. Then build the two cases

Only now, from the material 5a–5d produced. How, and the rules that govern it, are in
**The two advocacy cases** below.

## Step 6 — Report

To the format in [`references/output-template.md`](references/output-template.md). The shape
of it, and why it is that shape, is in the next section.

### Offer an HTML report, and design it properly

**Offer a designed HTML page as the deliverable, and say so in one line before building it.**
Not instead of asking — offer, then build on a yes. Where the host can publish a page and the
reader has asked for something to read or circulate, that is the right format for this output
and a wall of terminal text is not.

Three reasons this output in particular earns it, none of which is decoration:

- **It is read under time pressure, on a phone, the night before a meeting.** Everything in
  the ordering — deadlines at the top, triage before detail, the skip list — exists to get a
  reader to the part that matters. That ordering only pays off if the page is navigable.
- **It carries a lot of structured material**: a triage table, weighting pivots, a claims
  table with a four-state tested column, ranked community points each carrying a policy, and
  two advocacy cases that must read as equals. Markdown flattens all of it into one column of
  prose, and the two cases in particular stop looking independent the moment they are just
  two headings in a row.
- **It gets forwarded.** A page a reader can send to a parish council or a ward member is
  worth more than text they have to copy out, and the fixed disclaimer travels with it.

**Use the design skill rather than improvising a stylesheet.** Load the host's own
artifact/design skill and follow it. Two things it will otherwise get wrong here:

- **The two advocacy cases must be given visually equal weight** — same treatment, same
  density, same prominence. If one reads as the recommendation because it is longer or
  better set, the independence the method insists on has been thrown away at the last step.
- **Do not use semantic red/green for refuse/approve.** It reads as bad/good and turns a
  neutral document into a recommendation. Two distinct hues of equal saturation, neither of
  which carries a verdict.

**The disclaimer keeps its fixed wording in any format**, at the top, above the deadlines.
Design may set it; it may not shorten it.

Markdown remains correct where the reader asked for it, where the host cannot publish a page,
or where the output is going into a document someone else will edit.

### Say which model produced it, and stop if it is not a frontier model

**Establish the model before starting the read, not at the end.** This skill asks for
sustained forensic reading across several hundred pages — holding an officer's reasoning
against its own appendices, noticing a policy listed and never applied, catching that a
consultee's summary softens their actual response. That is the work a smaller or faster model
does worst, and it fails in the specific way that matters here: **it produces a confident,
well-formed report with findings that are not in the papers.** A thin summary would be
obvious. Fabricated defects are not, because this output's whole form is designed to look
authoritative.

- **On a frontier model**, record which one in the provenance line at the foot, with the date.
- **On anything else, say so and ask before proceeding.** One line, naming the model and the
  risk — not a refusal, and not a lecture. The user may have good reasons, and it is their
  call. What they must not do is find out afterwards.
- **Never guess the model.** If it cannot be established, say that instead of naming one.

This is the disclaimer's last paragraph made operational: output varies with the model, its
version and the effort applied, so the run should say which one it had.

## Output format

**A disclaimer at the very top, before anything else, and set to be unmissable.** Not a footer,
not small print, not a closing paragraph — the first thing on the page, in bold, above the
deadlines.

This is not boilerplate and it is not defensiveness. **This skill produces a document that
reads with more authority than it has earned**, and that is a direct consequence of what it
was asked to do: it quotes the council's own papers back at them, it names defects, and it
ends with two cases written at full advocacy strength. A reader who arrives at "the strongest
reasons to refuse are…" without having been told what they are holding will take it for a
professional opinion. The two cases are the most likely part to be lifted, forwarded, read
aloud at a meeting or quoted in a newsletter, and each of them is deliberately one-sided.

**The disclaimer is therefore load-bearing, not decorative**, and it goes above the deadlines
even though the deadlines are the thing a reader can act on. Keep it tight enough that the
deadline block still sits in the first screenful — this is the one place in the output where
brevity matters more than completeness, with the full terms repeated at the foot.

**The wording is fixed. Reproduce it exactly, and do not paraphrase, summarise, reorder or
add to it:**

> This is a machine-generated reading of published committee papers.
>
> All cases have a "reasons to approve" and "reasons to reject" section. These sections are
> advocacy points, and are not designed to be a balanced appraisal.
>
> Extracts and paragraph references are machine generated. If you wish to quote a specific
> reference it is recommended to find the original text and validate it.
>
> Nothing in this document is legal or professional advice. It is provided as is, without
> warranty of any kind. No liability is accepted for any decision taken, or not taken.
>
> Output of any AI skill will vary depending on the underlying model used, the model version,
> and the model effort. Two runs may produce different output, and any output is governed
> under the model provider's terms and conditions.

**Why it is fixed text rather than a list of points to cover**, which is how the rest of this
skill is written: the last paragraph is the reason. Output varies between runs, so the one
part of the document that must not vary is the part that states its limits. A disclaimer
regenerated from a specification each time is a disclaimer that says something slightly
different every time, and the reader has no way of knowing which version they were given.
Everything else in the output is the model's to compose. This is not.

**Nothing else goes in the block.** Anything further belongs in the fuller terms at the foot,
where it does not compete with the deadline for the reader's first attention. Two things in
particular:

- **Findings are about documents, not about people** — worth saying, and what makes it fair to
  keep using *thin*, *missing* and *internally inconsistent* plainly, but it is guidance on how
  to read the findings rather than a limitation on relying on them. Foot of the page.
- **Do not lecture the reader on their own obligations.** Say nothing about predetermination or
  the member code of conduct, at the top or at the foot. Members know the rules they are bound
  by, a skill that recites them back reads as both patronising and as advice it is not giving,
  and it spends scarce space on the one thing that reader did not need. The skill's own refusal
  to advise on the vote is a rule governing the skill, not a caution to print.

The snapshot point stays out too — the retrieval time and the re-check instruction sit
immediately below in the deadlines block, with real times attached rather than stated in the
abstract.

**Then deadlines and freshness.** Before any analysis:

- the **meeting** — committee, date, time, venue, and whether it is webcast;
- the **speaking deadline** and how to register, which is usually days before the meeting and
  is the thing a reader can still act on;
- **what was retrieved and when**, and explicitly **whether an addendum existed at that
  time** — with the instruction to re-check on the morning.

**Then the agenda at a glance.** One table, one row per item, ordered as the agenda is:

| Item | Reference | Site | Recommendation | Scrutiny |
|---|---|---|---|---|

`Scrutiny` is the triage call — **high / medium / none**.

**On a normal agenda the table must contain rows marked `none`**, or the triage has not been
done — the skip list is the most useful thing in the document and it will not write itself.

**But do not manufacture one.** Some agendas have no routine business: where a council refers
items to committee *because* they are contested — a threshold of objections against the
officer recommendation is a common trigger — every item on a short agenda can legitimately
be worth reading. Where that is the case, **say so and say why**, in a sentence. A forced
`none` on a contested item is worse than an honest note that this agenda has none: it sends
the reader past the very item the referral trigger flagged.

**Check the referral reason, because it is a triage input.** Reports often state why the item
came to committee at all. "More than eight households objected on material grounds
inconsistent with the recommendation" tells you the officer and the public disagree — which
is a fact about the item, not about its merits, and should be read as such.

**Then the items that repay it, one section each**, and only those. Per item:

**The order is fixed**, and it runs from what is on the page, through what is wrong with it,
to what each side can do with it:

1. **Summary.** What is proposed in **two or three lines at most** — the reader has the fact
   pack and the report, so this is a referent, not a précis — then the recommendation and
   what it turns on, in one paragraph, quoting the officer where the wording matters. Any
   addendum and what it changes goes here too, marked, because it changes what everything
   below is about.

2. **Possible defects, issues and omissions.** The findings from Step 5a. A verbatim quote
   for each, and a mark: *wrong*, *thin*, *missing*, *conflicting*, *unexamined alternative*.
   Where there are several, hand the item to `planning-report-critique` rather than
   reproducing its method.

   Immediately after, as part of the same block: **where the weight is the member's to set**
   — the pivots from Step 5b, which are fixed and which are at large, and which the
   conclusion turns on.

3. **Claims the recommendation rests on.** From Step 5c. The applicant's evidence the report
   relies on, what depends on each claim, and who tested it — including where the answer is
   nobody.

4. **Community comments, and the policy each one attaches to.** From Step 5d. Ranked by
   planning merit, each with its policy by number or code. Then, separately, those with no
   planning anchor and why.

5. **If you are minded to approve, you can do so on the basis…**

6. **If you are minded to refuse, the strongest reasons are…**

   Cases 5 and 6 are built independently of each other — see the section below. This is the
   part of the output that gets used, and the part most easily got wrong.

7. **What a reader could do about it**, tied to the deadlines at the top: register to speak,
   write to members, ask a specific question, or nothing.

**"Possible" is a statement about this document's standing, not a hedge on the individual
findings.** Each entry below the heading is still stated flat — *wrong*, *thin*, *missing* —
because a finding that hedges itself cannot be acted on. What the heading concedes is that
this is a reading of the published papers by someone who has not seen the whole file, has not
put any of it to the author, and has had no reply. A point that looks like an omission may be
answered in a document that was never published; a conflict may have a reason the report did
not give. That is a real limit on the document, and naming it on the heading is what earns
the right to state each entry plainly underneath.

Sections 2 and 3 are the same act of scrutiny in three forms, and it is worth holding the
distinction while writing: **a defect is something the report got wrong, a pivot is something
the report presents as settled that is in fact a judgement, and a claim is something the
report has taken on trust.** All three are things the papers do not settle, and they fail in
different ways — so they are attributed differently and they are answered differently.

Why this order: the two cases come last because they are **built from** everything above
them. A reader who wants only the conclusions reads 4 and 5 and can trace every ground back
up the page. A reader who distrusts them can check 2 and 3 first. Putting the cases higher
would make the scrutiny look like supporting material for a position already taken.

## The two advocacy cases

Give both. Not a balance, not a recommendation — **the strongest available case for each
decision, each written as though it were the only one on the page**.

A reader facing a committee decision needs to know what the best argument in each direction
actually is. The officer report gives them one side properly argued and the other side
summarised; objectors give them the reverse. Setting out both at full strength, plainly, is
the most useful thing this skill produces.

### Build them independently

**Write each case as an advocate for that outcome would write it**, drawing on everything
Steps 5a–5c produced, and **without reference to the other case**. The practical test: if
you cannot write the approval case without first checking what the refusal case said, they
are not independent, and what is being produced is a balance with two headings.

Three rules follow from that:

- **Neither case concedes.** No "although the harm is significant", no "notwithstanding the
  objections". A concession belongs in the other case, at full strength, where the reader
  will find it.
- **Both cases get the same effort.** The weaker case is not written more weakly — it is
  written as strongly as the papers allow, and the reader sees that the papers do not allow
  much. That is a far more useful signal than a case deliberately undersold.
- **No closing paragraph.** Nothing that weighs the two lists against each other, and
  nothing that hints which is stronger. The lists end and the section ends.

**Do not couch or qualify.** No "on the one hand", no "it could be argued". State the
grounds and stop. Hedged output is useless at the moment it is needed, which is the night
before a meeting.

### Weight belongs in both cases

Each case should say, where it applies, **which weighting it depends on** — drawing directly
on Step 5b. A refusal case that rests on giving landscape harm more weight than the officer
did should say so in terms, because that is a route a member can lawfully take and needs to
know is open. The same in reverse for an approval case resting on the housing contribution.

Stated as: *"This case requires giving the landscape harm greater weight than the report
does. That weight is at large."* It tells the reader what they would be doing, which is what
makes the ground usable.

**Do not recommend.** Setting out both cases is not choosing between them. Which case is
better, and which a member should adopt, is `councillor-fact-pack`'s territory under the
predetermination constraints this skill does not carry — and predicting the vote is out of
scope entirely.

**⚠️ Do not forecast what an appeal would do.** No "this would not survive an appeal", no
"an inspector would be likely to", no appeal-risk rating. That is a prediction about a
decision nobody has taken yet, on evidence and argument that do not yet exist, and it is not
this skill's to make — **it is for members to determine their own approach.** The same rule
that keeps the skill out of predicting the committee vote keeps it out of predicting the
appeal.

The distinction to hold: **describe the ground, do not forecast its fate.** "The highway
authority raised no objection" is a fact about the file. "This ground would fail" is a
forecast. Give the first and let the reader draw the second if they wish.

### What each ground must carry

Three things, stated as facts rather than as caveats. They are not hedges; they are
properties of the ground, and a reader who does not have them cannot use it.

- **The policy it hangs on** — a specific adopted development plan policy, by number, or a
  specific national policy by its code. Not "residents object", not the NPPF in the
  abstract. Under s.38(6) the decision is made in accordance with the development plan
  unless material considerations indicate otherwise, so a ground with no policy anchor is
  not a reason, it is an opinion. **A community concern that Step 5c anchored to a policy
  qualifies** — carry it into the case with that policy attached, and say that it is a point
  the community raised. That combination is what a member needs to speak to it.
- **Whether it is evidenced on the file, or asserted** — and by whom. "The council's
  conservation officer finds mid-scale harm" and "objectors consider it harmful" are both
  facts, and they are not the same fact.
- **For a refusal ground: whether a condition or obligation could cure it.** State it as the
  fact it is — "this could be secured by condition" — and leave the consequence to the reader.
  Do not attach a costs prediction to it.

### Say plainly when the papers do not support a ground

**This is the discipline that makes the rest of it credible.** Where a candidate ground has
no policy anchor, or no evidence on the file, say so **as a fact about the papers** — not as
a forecast about what would happen to it:

> **No ground on these papers carries both a policy anchor and evidence on the file.** The
> site is allocated for this number of dwellings; the harm the officer identifies is recorded
> as accepted by the allocation; and every consultee with a remit has confirmed no objection.

That is a description of what is and is not in the pack. It tells a member exactly where they
would be starting from, and leaves the decision — and the appetite for it — to them.

**But check the weighting pivots before writing that sentence.** "No ground is evidenced on
the file" and "no route to this outcome exists" are different statements, and only the first
is usually true. Where Step 5b found a consideration whose weight is at large and on which
the conclusion turns, the route is a re-weighting rather than a defect, and it must be given
as one:

> No ground on these papers carries both a policy anchor and evidence on the file. The route
> to refusal on this item is not a defect in the report — it is the weight given to the
> landscape harm, which the report itself describes as a judgement, and on which its
> conclusion turns.

Only where there is neither an evidenced ground nor a live pivot is the list genuinely
empty, and then it should be written as empty, flatly.

A skill that always finds reasons to refuse is a campaigning tool, and will be discounted as
one on the item where the reasons are real. The same applies in reverse: where the approval
case rests on a judgement the papers do not evidence, say that too.

**Never manufacture a ground to fill a list**, and never pad a real ground with weak
companions — a strong reason surrounded by three thin ones reads as weak by association.
Where candidate grounds were raised but are not supported, list them separately with what
each actually rests on, so a member can see what was considered and why it is not in the
main list.

**Then the items that do not repay scrutiny**, as a single short list with one clause each
saying why. This section is the evidence that the triage was real.

**Style.** Per house rule 9: enumerations of three or more go in lists, never strung through
a paragraph with semicolons. One point per paragraph, paragraphs short. This output is read
under time pressure the night before a meeting, and a wall of prose will not be.

## Integrity rules

- **The pack is what the committee has, not what the council has.** If the officer report
  refers to documents not in the pack, say so — do not fill the gap from the planning portal
  and present it as though the committee had it. Retrieve it by all means, and label it as
  outside the pack.
- **Report what is there, including when it is fine.** An item where the officer report is
  sound and the recommendation well-evidenced should be reported as such. Being forensic
  means looking hard, not finding something regardless — and a review that finds fault
  everywhere will not be believed about the item where the fault is real.
- **Distinguish a defect from a weighting, and file each where it belongs.** "The officer
  says the policy is not engaged, and the policy says it is" is a defect, and goes in the
  report findings. "The officer gave this less weight than a member might" is **not** a
  defect and must never be reported as one — but it is not nothing either: it is a weighting
  pivot, it goes in that section, and it may carry an advocacy case. Mixing the two
  discredits the defects.
- **Do not re-run the applicant's technical work.** Naming a claim as load-bearing and
  untested is a fact about the papers. Declaring the noise assessment wrong, recomputing a
  biodiversity metric or disputing a traffic count is expertise this skill does not have, and
  a wrong technical assertion discredits the findings that are right. The output stops at the
  question that would test the claim.
- **Advocacy is not invention.** Writing the strongest case for an outcome means finding the
  best material actually in the papers and putting it at full strength. It does not mean
  supplying a ground the papers do not support, inflating what a consultee said, or
  presenting a member's available weighting as though the officer had already made it.
- **Never infer an outcome.** The committee decides. Reporting that an item is finely
  balanced is analysis; predicting the vote is not, and it would make the output look like
  campaign material.

## Stop, or ask

| Condition | Do |
|---|---|
| **The model running this is not a frontier model** | **Say so and ask before starting the read.** Name the model, say in one line that sustained forensic reading across a long pack is where a smaller model fails by producing confident findings that are not in the papers, and let the user decide. Not a refusal. |
| **You cannot establish which model is running** | Say that, and do not name one. An invented provenance line is worse than an absent one. |
| **The meeting page loads and lists no documents** | **Do not report "nothing on the agenda".** Establish which of three things it is: the meeting is **cancelled** (the page usually says so — look for it), the pack is **not published yet**, or you have the **wrong committee**. A cancelled meeting returns an ordinary success response with an empty document list, so a run that treats zero documents as zero business will say the wrong thing confidently. |
| The meeting is **cancelled** | Say that it was cancelled, and point at the next meeting of that committee. |
| The pack for the meeting is not published yet | **Say so**, with the publication date if given. Do not review an earlier meeting instead. |
| **You do not have the speaking deadline** | **Say you do not have it**, and tell the reader to check the council's page. Never supply a plausible-looking date: a wrong deadline is worse than an absent one, because a reader will act on it. |
| The committee system cannot be found or is unreachable | **Stop** and hand the user the council's committee page. Do not substitute the planning portal. |
| The item map does not reconcile with the agenda frontsheet | **Say which item is unaccounted for** before reporting on the rest. |
| The user wants a recommendation on how members should vote | That is `councillor-fact-pack`'s territory, under its predetermination constraints. Decline here. |
| The user wants the two cases weighed against each other | **Decline, and say why**: this skill produces two independent advocacy cases by design, and a balance is `planning-balance` and `policy-compliance-assessment`. Offer that hand-off rather than quietly supplying a balance. |
| **Only the officer's summary of the representations is in the pack** | Work 5c from the summary, and **say in the output that you did** — it is the council's characterisation of the objections, and the section's rankings inherit whatever it left out. Where the individual representations are on the planning portal, retrieve them with `planning-document-search` and label them as outside the pack. |
| **The report relies on a submitted document that is not in the pack** | Normal, and worth stating rather than working around. Name the document, say what depends on it, and say it is on the planning portal rather than before the committee. Retrieve it with `planning-document-search` if the item warrants it, and **label it as outside the pack**. Do not describe its contents as though the committee had them. |
| **A benefit weighed in the balance appears in no condition and no head of terms** | Say so plainly in the claims block. This is a finding, not a technicality — it is the difference between a commitment and a claim, and it is checkable in the pack itself. |
| **An objection rests on something that is not a material planning consideration** | Say so, factually, in the 5d section. Do not silently omit it — the objector needs to know, and a member needs to know the committee cannot act on it. |
| The meeting is today and addenda were not checked | **Check, or say plainly that you did not.** |

## Scope and limitations

- **Not legal advice, and no warranty.** This helps a reader use the time before a meeting
  well. It is not a substitute for a planning consultant or a solicitor, and its output
  requires human review. **This must appear at the top of the output, not only here** — see
  the disclaimer requirement in **Output format**. A limitation a reader meets after the
  conclusions has not limited anything.
- **A pack is a snapshot.** Addenda land late, items get deferred, and the running order
  changes. Everything here is true as at the time of retrieval, which the output states.
- **Speaking rules are local and change.** Registration deadlines, who may speak and for how
  long are set by each council's constitution. Read the council's own page; do not assume.
- **England-focused.** The committee system and the speaking rules differ elsewhere.
- **Third-party personal data.** Packs contain objectors' names and addresses. Report the
  substance of objections, not the identities of the people who made them, and never
  reproduce contact details.

## Pairs with

- **`committee-speech`** — where the reader has a speaking slot. Its input is the refusal case
  this skill produces, and it handles the clock, the register and the slot allocation.
- **`planning-report-critique`** — the per-item deep read, once triage says an item earns it.
- **`planning-report-quality`** — the measurement underneath that critique.
- **`planning-document-search`** — for application documents that are *not* in the pack.
  Different system, different skill, and the one to reach for whenever a report relies on
  something the committee has not been given.
- **`policy-compliance-assessment`** — where an item turns on scoring a scheme against the
  development plan properly, rather than on what the pack says about it.
- **`planning-balance`** — for the reader who wants the balance this skill deliberately
  refuses to strike.
