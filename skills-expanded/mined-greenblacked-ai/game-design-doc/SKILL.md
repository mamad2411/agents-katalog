---
name: game-design-doc
description: "Turn a game idea or a design chat into an implementation-ready feature specification the whole team can build from — designers, programmers, artists, animators, UI, producers, QA and analysts. Writes out of scope before scope, marks every statement as a confirmed decision, assumption, recommendation or open question, keeps must, should and may distinct, makes acceptance criteria testable by a stranger, and pulls analytics, save/load and multiplayer forward from the sections teams find late. Use whenever someone says \"write a design doc for this feature\", \"spec out this mechanic\", \"we need a GDD\", \"feature spec\", or \"turn this design chat into something the team can build\". Not for building or prototyping the game itself (game-builder), a decision already taken (decision-record), READMEs and architecture overviews (technical-docs), or a publishable article (write-technical-article)."
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Game Design Doc

A feature specification is finished when a programmer, an artist, a UI designer and a QA engineer can each open it, find the part written for them, and start work without asking the author a question the document should have answered — and when nobody has to guess which sentences were decided and which were guessed.

Two failures produce most of the rework. The first is a document written for one discipline: it describes the fantasy and the fiction in detail, and says nothing about states, parameters, failure paths or what a build has to do to be accepted, so every other discipline invents its own answer and three of them conflict. The second is flattening certainty: a designer's guess, a recommendation and a decision the studio actually took all appear in the same voice, so a team builds for three weeks on an assumption that nobody ever agreed to, and discovers it in review. Everything below exists to prevent those two, and to pull forward the three sections teams reliably discover late — analytics, save and load, and multiplayer — because each of them is cheap while the feature is a document and expensive once it is code.

## Scope

Use for: turning a game idea, a pitch, a design conversation or a chat log into an implementation-ready feature specification; specifying one feature or system — a progression track, a shop, a boss encounter, matchmaking entry, a daily reward, a crafting loop — before anyone builds it; reviewing an existing design document for the sections and the marked statements it is missing; and separating what a meeting actually decided from what it assumed.

Do not use for: designing and building a playable game, choosing the engine or tuning game feel — that is `game-builder`, which makes the thing, where this specifies it before anyone does. Capturing a single decision and the alternatives that lost, after the decision is taken, is `decision-record` in the manager plugin. READMEs, onboarding guides and architecture overviews for software with a named reader and a Diátaxis mode are `technical-docs` in the coding plugin. A publishable article is `write-technical-article` in the career plugin. Choosing the numbers this document parameterises is `game-balance`. Save schema versioning and migration is `game-save-system`, and the authority model is `game-netcode`: name what the feature needs from each here, and cede the mechanics to them.

## Scale and game type

Scale here means what the work requires rather than a headcount or a budget: indie/A is one small team wearing every hat; AA adds specialised roles, several platforms and a publisher's milestones; AAA adds many specialised disciplines, external studios and a simultaneous multi-platform launch.

| | Indie/A | AA | AAA |
| --- | --- | --- | --- |
| Readers (step 1) | Often you and one or two teammates, so several of the eight roles are the same person | Each reader in step 1 is a different person, and the discipline read in step 9 is a real review meeting | Each reader is a different team, some external, and the spec earns sign-off from a discipline lead per team |
| Formality | Keep all twenty sections, but let several honestly read "not applicable" | Circulate a full draft for the step 9 read before build starts | The same review runs across studios and time zones, so open-question owners and dates have to survive without you in the room |

Narrative and story-driven games lean hardest on the user flow and states-and-transitions sections, because that is where branching lives. Competitive multiplayer and live-service games lean hardest on the analytics events and multiplayer behaviour in step 7, because the economy and matchmaking decisions in `game-balance` and `game-netcode` depend on what this document commits to measuring.

## Workflow

### 1. Name the readers before you write a section

The specification serves eight readers, and the list is the point — a spec only a designer can read has failed, however good the design is.

| Reader | The question they open it to answer | Section that has to answer it |
| --- | --- | --- |
| Game designer | What is the feature, and what is it for | Purpose, player experience goal, gameplay rules |
| Programmer | What states exist, what transitions are legal, what is configurable | States and transitions, parameters and configuration, technical dependencies |
| Artist | What has to be drawn or modelled, at what fidelity, in what states | Visual requirements, states and transitions |
| Animator | What moves, on what trigger, for how long, and what interrupts it | States and transitions, visual requirements |
| UI and UX designer | What the player sees and touches, and where the flow branches | User flow, UI requirements |
| Producer | What is in, what is out, what it depends on, what is still unresolved | Scope, out of scope, technical dependencies, open questions |
| QA engineer | How the build is proved to work, and what a failure looks like | Acceptance criteria, QA scenarios, edge cases, error handling |
| Analyst | What the feature emits, and what question those events answer | Analytics events |

Write the reader's name against any section you are tempted to skip. A section with no reader is one you can drop; a reader with no section is the person who will be blocked.

### 2. Write Out of scope before Scope

It is the section skipped most often and the one that costs most when it is missing, because a reviewer's first question is always what the feature is *not*, and every unanswered version of that question becomes somebody's optimistic assumption.

List every adjacent thing a reasonable reader could assume is included, and for each say which of these it is:

- **Out for this release**, with the milestone where it is expected instead. This is a deferral and it needs a name, not a shrug.
- **Out permanently**, with the reason. "Never" is a stronger promise than "not yet" and it lets a programmer design differently.
- **Owned by another feature or another spec**, named. This is where a boundary gets settled in one line rather than in a meeting.

Then write Scope. Writing it second is easier, because the boundary is already drawn.

### 3. Mark every statement as one of four kinds

A specification carries four kinds of sentence, and conflating them is how a team builds the wrong thing for three weeks. Mark each one inline, at the statement, rather than by grouping paragraphs — the mark has to survive a reader who copies one line into a task.

- **Confirmed decision.** Agreed by whoever has the authority to agree it. Build against it.
- **Assumption.** Taken as true so the document could continue, and not yet checked. It has an owner and a date by which it becomes a decision or an open question.
- **Recommendation.** The author's proposal, still open to being overruled. It names the alternative it beat.
- **Open question.** No answer yet, with the person who can give one and the date the answer is needed.

The tell that this is being done badly is a document where everything is a confirmed decision. First drafts are not like that.

### 4. Use the modal verbs precisely, and only these

| Verb | Obligation | A reader who ignores it |
| --- | --- | --- |
| must | Required. The build is wrong without it | Ships a defect |
| should | Expected, but a justified exception is allowed | Owes a written reason |
| may | Permitted, at the implementer's discretion | Is doing nothing wrong |
| cannot | Prohibited, and enforced by the system | Ships an exploit |
| only when | The single condition under which the thing is permitted | Widens a rule silently |
| except when | The single carve-out from a rule stated above | Breaks the carve-out case |

Blurring them is not a style problem. A "should" read as a "must" produces work nobody asked for; a "must" written as a "should" produces a missing feature that passed review. Cut narrative description entirely: a specification is not a pitch and not a story, and a paragraph of mood sitting where a rule belongs is read as decoration and skipped by the people who needed the rule.

`references/statement-discipline.md` — read it at steps 3 and 4: the notation for the four statement kinds, the modal verbs with worked before-and-after rewrites, and the phrases that look like requirements and are not.

### 5. Work through the twenty sections, in this order

1. Purpose — 2. Player experience goal — 3. Scope — 4. Out of scope — 5. User flow — 6. Gameplay rules — 7. States and transitions — 8. Parameters and configuration — 9. UI requirements — 10. Visual requirements — 11. Audio requirements — 12. Technical dependencies — 13. Analytics events — 14. Save and load behaviour — 15. Multiplayer behaviour — 16. Edge cases — 17. Error handling — 18. Acceptance criteria — 19. QA scenarios — 20. Open questions.

The order is load-bearing rather than tidy. Intent comes before boundary so the boundary can be argued against something; the boundary comes before the flow so the flow does not wander outside it; rules and states come before the discipline-facing sections so art, UI and audio are specified against states that exist; and acceptance criteria come last among the substantive sections because they can only test what the earlier sections committed to.

Keep every section, including the ones that do not apply. A section reading "Not applicable: this feature is single-player only, and stores nothing persistent — confirmed decision" is information. A missing section is indistinguishable from a forgotten one, and a reader cannot tell which.

`references/feature-spec-template.md` — read it at this step and keep it open while drafting: the full twenty-section template, with what each section has to contain, the discipline it unblocks, and the failure that follows when it is thin.

### 6. Write acceptance criteria someone who did not write the spec can test

Every criterion is a statement a QA engineer with no access to the author can mark as passed or failed. If marking it requires the author's taste, it is not a criterion.

Badly:

> The dash should feel responsive and the cooldown should be obvious to the player.

Well:

> - The dash must begin on the frame the input is received; input-to-first-animation-frame latency must be under 100 ms at 60 fps on the minimum-spec device. [decision]
> - The cooldown indicator must be visible for the full cooldown duration and must read as complete within 100 ms of the ability becoming usable again. [decision]
> - Dash must be unavailable while the cooldown is active, except when the player is in the tutorial, where cooldown is zero. [decision]

The second version is longer, and that is the whole cost. It is testable by a stranger, it names the device, and it exposes a carve-out that the adjective version hid.

Adjectives that cannot be acceptance criteria on their own: responsive, smooth, intuitive, juicy, satisfying, clear, fun, polished. Each is a real goal — put it in the player experience goal section, where it belongs, and convert it here into a number, a duration, a count, a visible state or an observable ordering.

### 7. Specify analytics, save and load, and multiplayer now, not later

These three are discovered late on almost every feature, and each costs rework out of proportion to the sentence that would have prevented it.

- **Analytics events.** Instrumenting after launch loses the baseline permanently: there is no way to compare the feature against the weeks before anyone measured, so the first question the feature raises cannot be answered. For each event name the trigger, the properties, the type and range of each property, and the question the event exists to answer. An event that answers no question is cost with no payoff, and a question with no event is a decision that will be made on opinion.
- **Save and load behaviour.** A feature that touches persistent state changes the save schema, and that change is a migration for every player who already has a file. Name here exactly what the feature persists, what it must restore on load, what happens when the field is absent because the save predates the feature, and what happens if the game is closed mid-flow. Hand the schema version, the migration step and the write policy to `game-save-system`; do not design them here.
- **Multiplayer behaviour.** A feature designed single-player-first often cannot be made authoritative later, because the whole implementation assumes the client can decide. State whether the feature exists in multiplayer at all, what each player sees of another player using it, what the server has to validate, and what happens when a player disconnects mid-flow. The authority model, prediction and reconciliation belong to `game-netcode` — name the requirement, cede the mechanism.

### 8. Leave the open questions in, with an owner and a date

Open questions are a first-class section, not an admission of failure. A first draft with no open questions is almost always hiding assumptions that were resolved by the author quietly, and those are the ones that surface as rework.

Each open question carries the question, why it blocks or does not block a start, the person who can answer it, and the date the answer is needed. A question with no owner is a note; a question with no date never closes. When one is answered, move it into the relevant section as a confirmed decision and leave a line in Open questions saying what it became, so a reader who remembered the question can find its answer.

### 9. Read the draft once per discipline before you circulate it

Read it as each of the eight readers in step 1, one pass each, asking only their question:

- **Programmer.** Is there any behaviour here I would have to invent? Every invention is a decision made by the person with the least context.
- **Artist and animator.** Is every state that appears in section 7 something I can see, and does every visual asset named have a state that uses it?
- **UI designer.** Can I draw the flow without guessing what happens on the branch nobody wrote down?
- **QA.** Is every acceptance criterion falsifiable, and does every edge case say what the correct behaviour is rather than that the case exists?
- **Producer.** If half of this is cut, which half, and does the spec make that obvious?
- **Analyst.** Does every event answer a question somebody asked?

Fix what each pass finds before circulating. A review cycle spent on gaps the author could have found is the most expensive kind of review.

## Anti-patterns

**Narrative where a rule belongs.** A paragraph of fiction reads as flavour, so the people who needed the rule skip it, and the rule is never implemented.

**Writing "should" and meaning "must".** The reviewer approves it, the programmer treats it as optional, and the missing behaviour is found in QA by someone who cannot tell whether it is a bug.

**Skipping Out of scope because the scope seems obvious.** It is obvious to the author. Every reader fills the gap differently, and the versions conflict in integration rather than in review.

**Acceptance criteria written as adjectives.** "Feels responsive" cannot be failed by anyone except the author, which makes the author the bottleneck on every build.

**Marking an assumption as a decision.** It is the single most expensive error in this document, because nothing downstream distinguishes them and the cost lands weeks later as a rebuild rather than a conversation.

**Deferring the analytics section to after launch.** The baseline cannot be collected retroactively, so the feature's first evaluation is anecdote.

**Specifying a persistent feature without a save section.** The save schema changes anyway; the only question is whether it changes by design or in a hotfix.

**Designing single-player and adding multiplayer later.** Authority cannot be retrofitted onto an implementation that assumed the client decides, so the late version is a rewrite.

**A first draft with no open questions.** The questions exist; they have been answered privately by the author, which is the same as answering them at random.

**Parameters described in prose.** A tuning value buried in a sentence is invisible to the person tuning it, so it gets hard-coded, and the balance pass has to find it in the source.

**One document for the whole game.** A hundred-page design bible is read once. A feature specification is read by someone about to build that feature, which is why it is scoped to a feature.

## References

- `references/feature-spec-template.md` — read at step 5 and keep open while drafting: the full twenty-section template in order, with what each section has to contain, who it unblocks, and the failure that follows when it is thin or missing.
- `references/statement-discipline.md` — read at steps 3 and 4: the four statement kinds and how to mark them inline, the six modal verbs with the obligation each carries, before-and-after rewrites, and the phrasings that look like requirements without being testable.
