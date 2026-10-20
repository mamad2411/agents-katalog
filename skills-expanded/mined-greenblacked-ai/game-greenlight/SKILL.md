---
name: game-greenlight
description: "Turn a game concept into a chosen idea before any design document exists. Writes a one-page pitch (fantasy, target player, three comparables, why now), reads feasibility against team, time, money, platform and technical risk, and builds a risk register naming the one assumption most likely to sink it. Sizes the smallest prototype that can test that assumption — not a vertical slice, which proves polish rather than risk — and writes go, no-go and pivot criteria before the prototype is built, so the result cannot be rationalised afterward. Use whenever someone has a game concept and needs a pitch, a feasibility read, a greenlight decision, or a prototype defined — \"should we build this\", \"is this idea feasible\", \"what should the prototype prove\". Not for the spec once chosen (game-design-doc), building it (game-builder), or recording a decision already made (decision-record)."
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Game Greenlight

A go, no-go or pivot decision gets made once, in writing, against criteria set before the prototype existed to argue for itself — not twice, once informally over the weeks the prototype was fun to work on and once formally to ratify what everyone already believed.

Almost every greenlight that goes wrong goes wrong before the prototype starts, for one of two reasons. The first is testing the wrong thing: a team builds a beautiful vertical slice that proves they can make good art and never touches the one assumption the whole pitch actually depends on, so a good demo ships a bad decision. The second is testing at the wrong time: the kill criteria get written after the prototype is played, once everyone already has a favourite outcome, which turns a decision into a justification. This skill exists to put the order right — pitch, feasibility, the one riskiest question, the criteria — before a line of prototype code exists, so the decision the team reaches is the one the evidence actually supports.

## Scope

Use for: writing the pitch for a game concept; reading feasibility against team, time, money, platform and technical risk; building a risk register and naming the single riskiest assumption; deciding what a prototype needs to prove and how small it can be while still proving it; writing go, no-go and pivot criteria in advance; and making the call once the prototype exists.

Do not use for: writing the feature specification once an idea has been chosen — that is `game-design-doc`, which starts exactly where this skill ends. Building the prototype or the game itself, including the playable build that answers the riskiest question, is `game-builder`; this skill decides what the build has to prove, not how to make it. Recording a decision already taken, with the options that lost and why, is `decision-record` in the manager plugin — reach for it if the team wants the greenlight call written up as a durable artefact after the fact, not for making the call itself. Choosing or comparing external vendors, engines or tools is `vendor-evaluation`, also in manager. Tuning numbers inside a game that already exists is `game-balance`.

## Scale and game type

Scale here means what the work requires rather than a headcount or a budget: indie/A is one small team wearing every hat; AA adds specialised roles, several platforms and a publisher's milestones; AAA adds many specialised disciplines, external studios and a simultaneous multi-platform launch.

| | Indie/A | AA | AAA |
| --- | --- | --- | --- |
| Who decides (step 7) | The team self-greenlights; the call is a conversation, written down by whoever made it | The pitch goes to a publisher, and the criteria in step 5 are what the pitch meeting actually asks for money against | A stage-gate process: several named gates, each with its own written criteria, reviewed by people who did not build the prototype |
| Pitch formality (step 1) | A page, sometimes a paragraph, sometimes just said aloud and then written down | A real pitch deck built to what the publisher's process expects | A formal pitch document per gate, often rewritten for each one |
| Prototype budget (step 4) | Days to a couple of weeks, self-funded | A budgeted milestone with a deadline the publisher set | A funded pre-production phase, sometimes with more than one riskiest question run in parallel by different teams |

Feasibility (step 2) carries the most weight for a small team betting its only runway on one idea, and for a AAA stage gate where the tech-risk axis alone can decide the gate. The riskiest-question step matters most wherever the genre's core loop is unproven — a new mechanic, a new market, or a technical approach the team has not shipped before; it matters least for a sequel or a well-understood genre entry, where the open question is usually content and scope rather than whether the game can be fun at all.

## Workflow

### 1. Write the pitch before judging it

One page, four parts: the core fantasy in one sentence, the target player and why they would choose this over what they already play, three comparables in the shape "plays like X, but Y", and why this team can make it now. Writing the pitch before reading feasibility is deliberate — feasibility read against an idea nobody has stated cleanly ends up feasible for the version of the idea in the reader's head, which is rarely the version being pitched.

Read `references/pitch-and-feasibility.md` for the shape of each part and what it protects against.

### 2. Read feasibility against what the team actually has

Score the pitch against team, time, money, platform and technical risk — not against how good the idea sounds. A pitch can be excellent and still infeasible for this team at this moment, and saying so before the prototype starts is the whole point of doing this step first.

| Axis | The honest question |
| --- | --- |
| Team | Does anyone here know how to make this kind of game, or is the team learning the genre and the idea at once |
| Time | What is the actual deadline, and does the prototype fit inside a fraction of it |
| Money | What does a no-go cost against what a go costs, and can the team survive either |
| Platform | Does the target platform's constraints (input, screen, store rules) shape the core loop, or was the loop designed first and the platform assumed |
| Technical risk | Is there a piece of this — netcode, procedural generation, a simulation scale — nobody on the team has built before |

`references/pitch-and-feasibility.md` has the full matrix and a worked read against a real pitch.

### 3. Build the risk register and find the one question

List every assumption the pitch depends on to be true — "players will understand the mechanic without a tutorial", "the art style is cheap enough to produce at the needed volume", "the netcode model scales to sixty-four players". For each, rate how likely it is to be wrong and how much it costs the project if it is. The assumption with the worst combination is the riskiest question, and it is usually not the one that is easiest or most fun to test.

Read `references/prototype-question.md` for how to run the register and for worked examples across a few genres of what the riskiest question actually turns out to be.

### 4. Choose what the prototype tests — not a vertical slice

The prototype exists to answer the one question from step 3, and nothing else. A vertical slice — a small polished piece representative of the whole game — answers "can this team produce at this quality bar", which is rarely the riskiest thing about a new idea and is expensive to build before anyone knows whether the core assumption holds. Build the smallest thing that could prove the riskiest assumption false, in the ugliest form that still tests it honestly.

A netcode-risk pitch gets two boxes talking over a real network before either box gets art. A fun-risk pitch gets the loop in grey boxes before a single asset. A market-risk pitch sometimes needs no code at all — a landing page or a handful of interviews answers it faster than a build does. Say out loud which question is being tested and what a build with no bearing on that question would look like, so scope creep toward a demo is visible while it is still happening.

### 5. Write kill criteria before the prototype exists

For each of go, no-go and pivot, write the observable result that produces it — a number, a session behaviour, a specific failure — before anyone has played the prototype, and say how it will be observed: the method (a session count, a measured number, a behaviour watched for), the observer (the team, or players from the target audience in step 1), and the threshold that separates the outcomes. "We'll know it when we see it" is not a criterion; it is a decision deferred to whoever is most persuasive after the fact. A criterion written once the result is in is not a criterion, it is a description of what already happened wearing the shape of one.

Write where the criteria live — a pinned note, the pitch deck, the stage-gate document — and who signs them before the prototype starts. Read `references/kill-criteria.md` for the shape of a good criterion, examples of criteria that quietly failed to constrain anything, and how a pivot differs from a no-go dressed up to avoid saying it.

### 6. Build the prototype

Hand `game-builder` a prototype brief, not just the question. It carries what the earlier steps already wrote, by reference rather than rewritten:

- **The riskiest question** — the falsifiable assumption from step 3, and the one the build exists to answer.
- **Scope and non-goals** — the smallest-test scope from step 4 and its list of what the prototype will not include.
- **Platform and input** — only where step 2 found they shape the core loop, so the test runs on the input it will ship with.
- **Budget** — the time and people the prototype gets, from the scale table above.
- **The criteria** — step 5's method, observer, threshold, and the go, no-go and pivot results.

That brief is the approved direction: the builder builds to it rather than reopening concept choice, and comes back to this skill if the brief leaves a major design decision open. What returns is evidence against each criterion, labelled by kind — a build or automated smoke check, the developer's own self-playtest, or observation of intended players — with any criterion it could not test marked unverified or blocked, and what is missing. The call stays here, at step 7. This skill does not build; it decides what has to be true for the build to mean anything.

### 7. Make the call against what was written, not against how it feels

Read the prototype's result against the criteria from step 5, one criterion at a time, not against team morale or how much fun the prototype was to make. Check each criterion's evidence is the kind it named: build success establishes only that the project built, an executed smoke check supports only the runtime behaviour it exercised and asserted, and a developer's self-playtest shows what the builder found. None stands in for intended players when the criterion is about them. A criterion with unverified or blocked evidence is not met, and it is not a go — name the missing evidence and the test that would supply it, and wait for that test rather than deciding without it. A result that lands ambiguously between the written thresholds is itself a finding — usually that the test was underpowered, or that it tested the wrong thing — and the answer is to go back to step 4 and run a sharper test, not to let the mood in the room break the tie.

### 8. Hand off

A go goes to `game-design-doc` to turn the chosen idea into a feature specification the team can build from. A pivot returns to step 1 with the revised idea, carrying forward what the prototype disproved so the new pitch does not repeat it. A no-go stops here; if the decision needs a durable record for a publisher or a future team, that write-up is `decision-record`.

## Anti-patterns

**The vertical slice standing in for a risk test.** It proves the team can hit a quality bar, which is rarely what the pitch is actually betting on, and it costs far more than the test that would have answered the real question.

**Kill criteria written after the prototype is played.** A number picked to match the result it is describing is not a criterion. Write it before, or the exercise only produces the illusion of rigour.

**Testing the safe assumption instead of the risky one.** Building the part everyone already agrees will work is comfortable and proves nothing; the riskiest question is often the one nobody wants to test first.

**Silence as a go.** A prototype that nobody formally rejects becomes the game by default, without anyone having actually decided that it should. Make the call and write it down, in every direction including go.

**Falling for the pitch before reading feasibility.** An idea judged only on how exciting it is skips the question of whether this team, at this time, can actually make it — which is the question feasibility exists to answer honestly.

**Overriding the criteria on sunk cost.** Weeks of work invested in the prototype are not evidence about whether the idea is good; they are a reason the call gets harder to make honestly, which is exactly why the criteria were written down first.

## References

- `references/pitch-and-feasibility.md` — read at steps 1 and 2: the four-part pitch shape and what each part protects against, and the full feasibility matrix with a worked read.
- `references/prototype-question.md` — read at step 3: how to run the risk register, score an assumption's likelihood against its cost, and worked examples of the riskiest question across a few genres.
- `references/kill-criteria.md` — read at step 5: what makes a criterion a real constraint rather than decoration, examples of criteria that failed to constrain anything, and how a pivot differs from an undeclared no-go.
