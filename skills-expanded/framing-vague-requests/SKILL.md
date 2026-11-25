---
name: framing-vague-requests
description: Turn a vague or ambiguous request into executable work — establish the facts, ask the right questions (and only those), present options with a recommendation, get explicit agreement before executing. Independent of project, language, and domain.
---

# Framing a vague request

A badly framed task is lost before the first line: you will quickly produce something clean that doesn't answer the question. Framing is not paperwork — it's the moment where most of the value is decided.

## 1. Detect that the request is vague

Treat as vague any request where one of these signals appears:
- **A goal without an observable criterion**: "improve", "clean up", "make it more robust", "modernize". Improved by what measure, visible where?
- **A solution given in place of a problem**: "add a cache" may be the right answer to a slowness problem — or not. Climb back up to the problem before executing the proposed solution.
- **A scope without an edge**: you can't say what is explicitly EXCLUDED from the request.
- **Terms that admit several readings**: "the users", "the payment module", "the old system" — which ones, exactly?
- **A gap between the request and what you see in the code**: the request describes a state of the system that doesn't match what exists.

If no signal appears — the request is precise, bounded, verifiable — **don't inflict framing on it**. Execute. Framing a clear request wastes everyone's time.

## 2. Establish the factual map BEFORE asking questions

**Never ask a question the system can answer.** Before any question to the requester, go read what exists: what the code does today, what is already wired, what is dead, what the real usages are. Every question whose answer was readable in the code chips away at your credibility and the requester's time — and exposes you to a from-memory answer, often wrong, that you will then execute.

**Open with the map, not with a choice.** First present the factual state of things: "here's what exists, here's how it's wired, here's what is dead or has drifted". No options at this stage, no recommendation — facts. Two effects: the requester corrects your understanding BEFORE you build on it, and half the questions answer themselves once the facts are laid out.

**Flag the gaps between the story and the reality.** If the request assumes something the code contradicts ("button X" that doesn't exist, "the old behavior" that never was that), say it first. Building on a false story produces disposable work, even when executed perfectly.

## 3. Ask the right questions — and only those

**Prioritize: the problem before the solution, the what before the how.** The questions that matter, in order:
1. **What problem** does this request solve? What triggered the request now?
2. **What does "successful" look like**? What will be observably different?
3. **What is OUT of scope**? The excluded edge is more informative than the included content.
4. **What constraints** are non-negotiable — deadline, compatibility, things that must absolutely not break?

Implementation questions (which mechanism, which structure) come after, and you can often answer them yourself.

**Few questions, closed when possible.** Two or three questions per exchange at most, phrased so they can be answered in one sentence. A ten-point questionnaire won't be filled in — it will be skimmed, and you'll take a fatigue "yes" for a ruling.

**Distinguish what blocks from what can wait.** Ask now only the questions whose answer changes the direction of the work. Ambiguities that only affect execution details are settled by a reasonable default — announced, so it can be contested.

**Adapt the language to the requester.** With a non-specialist, every technical question comes with a translation into concrete consequences: not "should we invalidate the cache?" but "if someone changes X, do the others need to see it immediately, or is within a minute acceptable?". A question the requester doesn't understand produces a random answer — which you will then execute.

## 4. Propose: options with a recommendation

**Never a neutral menu.** Presenting three options without an opinion is offloading your work onto the requester. For each decision: the viable options (two or three, not seven), each one's trade-off in one sentence, and **your recommendation, argued**. The requester decides all the better when reacting to a position rather than exploring a space.

**Don't force a premature binary choice.** The inverse of the neutral menu is also a fault: reducing an open space too early to "A or B?" locks the discussion into a frame you chose alone. If the space is still wide, stay at the factual-map stage and let the requester express what matters to them before carving out options.

**Size the proposal to the problem, then show the edge.** Propose the scope that solves the problem properly — neither the minimal band-aid that will let the problem come back to life, nor the maximal project that drowns the request. And make the edge explicit: "this includes A and B; this excludes C, which I'm noting for later". What you noticed along the way that exceeds the request gets **flagged** — it doesn't invite itself into the scope.

**Put a price on what you propose.** Even roughly: small / medium / large, reversible / hard to undo, risky / harmless. A requester who says yes without perceiving the cost hasn't really said yes.

## 5. Lock the agreement before executing

**Restate the contract in three lines.** Before executing: the chosen goal, the scope (included AND excluded), the success criteria. If the requester corrects the restatement, the framing has just paid for itself — that's exactly the misunderstanding you would have discovered at delivery.

**An asked question waits for its answer.** If you raised a doubt or flagged a problem, stop there. Asking a question and then executing your own answer right away is not asking — it's announcing. The requester's apparent enthusiasm for the whole doesn't count as a ruling on the specific point you raised.

**Agreement on the plan is not a blank check.** If during execution you discover the plan rests on a false assumption, or that the real cost is nothing like what was announced, come back to the requester with the new fact. Executing a plan that reality has invalidated, "because it was agreed", betrays the agreement instead of honoring it.

**Record the decisions.** Every ruling made (scope excluded, option discarded, default accepted) is noted somewhere the next session — you, someone else, later — will find it. A lost decision will be re-debated, and sometimes re-decided the other way without anyone noticing.
