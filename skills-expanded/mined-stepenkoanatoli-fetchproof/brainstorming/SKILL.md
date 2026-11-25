---
name: brainstorming
description: Turn a request into a design the user has approved before any implementation, or review existing work with fresh eyes for better ideas. Use this before creating features, building components, adding functionality, modifying behavior, or starting a new project — including tasks that look too small to need it. Also use it when asked to review a diff or change for improvement ideas, or when the user asked for something to be built, left its shape open, and wants it made meaningfully better. Covers classifying the task (spike, bounded, architectural), clarifying questions, comparing approaches, design approval, written specs, fresh-eyes review, and ranked improvement ideas.
metadata:
  version: "3.0"
---

# Brainstorming

This skill does two jobs that share one discipline: think before building, and tell the user what you actually know.

1. **Design** — turn a request into a design the user approves before implementation starts.
2. **Review and Expand** — look at existing work with fresh eyes and produce ranked, costed ideas for making it better.

Read the request and the current state of the project, then name which mode you are in so the user can correct you.

## Working principles

These apply in every mode. They exist because the most expensive mistakes in design work are not bad ideas; they are confident statements that were never checked.

- **Approval comes before implementation.** The user cannot correct a plan they never saw. The size of the design scales with the task. The approval step does not.
- **Separate observed from inferred from assumed.** "The handler lives in `api/orders.py`" is something you read. "This is probably called from the checkout flow" is an inference. "Users will want to export this" is an assumption. Label them, especially the assumptions, so the user can reject the ones that are wrong.
- **Do not fill gaps with invention.** If you do not know a constraint, a user need, or how a piece of the codebase behaves, say so or ask. A guess presented as a fact costs more to unwind than a question costs to ask.
- **Do not pad lists.** If a mode asks for five ideas and you have three that clear the bar, give three and say the bar is why. Weak ideas hide strong ones and spend the user's attention.
- **Do not claim work you did not do.** "I checked the tests" means you opened them. "I ran it" means you ran it. If something is untested, say untested.
- **Recommend, and own the recommendation.** Lead with your pick and your reasons. Present the trade-offs fairly, including the case against your pick. The user is choosing; you are informing the choice.
- **Say when there is nothing to do.** A change that is already in good shape, or a request with nothing open to brainstorm, is a legitimate finding. Report it and stop.

## Choosing a mode

| Situation | Mode |
|---|---|
| The user wants something built or changed and it has not been built yet | **Design** |
| The user wants a review of an existing change or diff for better ideas | **Review** |
| The user asked for something to be built, left its shape open, and wants it made better | **Expand** |

If the request is to investigate, fix, or change one specific behavior and the user did not ask for ideas, Review and Expand do not apply. Use Design and classify the task.

---

## Mode 1: Design

### The approval gate

Do not write code meant to be kept, scaffold a project, invoke an implementation skill, or take any implementation action until you have told the user what you intend to do and they have approved it.

This applies to every path below. A todo list, a one-function utility, a config change — the design may be two sentences in chat, but present it and wait. Small tasks are where unexamined assumptions waste the most work, because nobody thought they were worth examining.

### Classify first

Before your first question, classify the request and say the classification out loud so the user can override it.

**Spike** — a feasibility question ("can we…", "is it possible…", "quick and dirty is fine") whose output is an answer, not code to keep.
- Present the question and what you will try, in two or three sentences. A nod is enough.
- Investigate as cheaply as correctness allows.
- Report findings as a recommendation. Label anything you built as throwaway. Keeping it is a new request and gets its own classification.

**Bounded** — a well-scoped change to a flow that already exists in this repo: a new flag, a small endpoint, a one-file fix.
- The test is concrete: can you open the code you are changing? If there is no existing flow to read, the task is not bounded, however familiar the kind of application is.
- Ask the clarifying questions that matter. Present a short design in chat: approach, files touched, how it will be tested. Then stop and wait for an explicit yes.
- No spec file, no plan document.

**Architectural** — new projects, new subsystems, changes that restructure how components fit together, or changes to interfaces other code depends on.
- Follow the full process: context, questions, two or three approaches, a sectioned design, a written spec, then an implementation plan.

Two rules govern classification:
- **When in doubt, take the heavier path.** Reaching for a lighter label to skip work is itself the doubt.
- **The ratchet is one-way.** Hidden complexity discovered mid-task upgrades the path. Stop, say what you found, and step up. Nothing downgrades mid-task, and each task gets its own classification and its own approval. Approval of a spike does not cover the change that follows it.

### Checklists

If you keep a task list, add each item for your path and complete them in order.

**Spike**
1. Explore project context — enough to frame the probe.
2. Present the question and probe plan — two or three sentences.
3. Get approval.
4. Investigate — as cheaply as correctness allows.
5. Report findings as a recommendation; label anything built as throwaway.

**Bounded**
1. Explore project context — files, docs, recent commits.
2. Ask the clarifying questions that matter, one at a time.
3. Present a short design in chat — approach, files touched, testing.
4. Get approval — stop and wait for an explicit yes.
5. Implement using the normal development workflow. No plan document.

**Architectural**
1. Explore project context — files, docs, recent commits.
2. Ask clarifying questions, one at a time — purpose, constraints, success criteria.
3. Propose two or three approaches with trade-offs and a recommendation.
4. Present the design in sections scaled to complexity; get approval after each section.
5. Write the design spec and commit it.
6. Self-review the spec and fix issues inline.
7. Ask the user to review the written spec.
8. Transition to an implementation plan.

### Working the design

**Understanding the idea**
- Read the project before asking about it. Files, docs, and recent commits answer many questions; do not spend the user's time on ones you could have answered yourself.
- If the request describes several independent subsystems, say so immediately and help decompose it before asking detailed questions.
- Ask one question at a time. Offer multiple choice where you can. Focus on purpose, constraints, and success criteria.
- State the assumptions you are carrying. The user can only correct what they can see.

**Exploring approaches**
- Propose two or three genuinely different approaches, not one approach with cosmetic variants.
- Lead with your recommendation and explain why. Include the strongest argument against it.
- Cut anything the current goal does not need. If a capability is "nice to have later," leave it out and say that you left it out.

**Presenting the design**
- Scale each section to its complexity. A simple section is a sentence; a hard one gets a paragraph and a diagram if that helps.
- Ask after each section whether it looks right so far.
- Cover architecture, components, data flow, error handling, and testing.
- Prefer smaller units with a clear purpose and well-defined interfaces.

**Working in an existing codebase**
- Explore the current structure before proposing changes.
- Follow existing patterns. If you intend to deviate, say so and say why.
- Include only targeted improvements that serve the current goal.

### After the design (architectural path only)

**Write the spec.** Use the repo's existing location for design documents if it has one. Otherwise use `docs/specs/YYYY-MM-DD-<slug>-design.md`. Commit it if the repo is under version control and the user has not asked you not to. Tell the user the exact path.

**Self-review the spec** before handing it over:
- Placeholders — any "TBD," "TODO," or bracketed gaps.
- Internal consistency — does section four contradict section two.
- Scope — did anything creep in that the goal does not need.
- Ambiguity — could a reasonable implementer read a sentence two ways.

Fix issues inline and tell the user what you changed.

**User review gate.** Ask, in roughly these words: "The spec is written at `<path>`. Please review it and tell me what you would change before I create the implementation plan." Then wait.

**Transition.** Once the spec is approved, invoke a planning skill if one is available in this environment. If none is, write the implementation plan yourself and get approval for it before starting implementation.

### Visual aids

Offer a visual (mockup, diagram, side-by-side comparison) only when a specific question is clearer shown than told, and only if the environment can actually display it. Offer it as its own message at the moment it would help, not upfront. Keep everything that is not genuinely visual in text.

---

## Mode 2: Review

Use this when asked to look at an existing change or diff with fresh eyes.

- Read the full diff and enough of the surrounding architecture to understand what the change touches. Do not edit files.
- Ask: considering the whole change, what would improve its overall design, architecture, simplicity, cleanliness, or behavior? What larger change would shake things up in a good way? What has not been considered? Which earlier hint of an idea would actually make a difference?
- Produce a few concrete recommendations — typically three to five, fewer if fewer are real. For each, give:
  - What the idea is
  - Expected impact
  - Rough effort
  - Trade-offs
  - What it rests on — something you read in the diff, something in the surrounding code, or an inference you have not verified
- Rank them and highlight the strongest one or two, with reasons.
- If the change is already in good shape and you see nothing worth its cost, say exactly that. A clean report is a valid outcome, not a failure to find something.

---

## Mode 3: Expand

Use this only when the user asked for something to be built and left its shape to you. If the request was to investigate, fix, or change a specific behavior, say there is nothing in scope to brainstorm and stop.

- Do not change anything.
- If the product has a real surface, use it: run it, open it, click through it. If you cannot (no display, no runtime, no access), say so plainly. Do not describe an experience you did not have.
- Brainstorm at least five concrete ways it could be meaningfully better — deeper where it is shallow, more delightful where it is flat, more worth returning to where it is forgettable. If fewer than five clear the "meaningfully better" bar, give the ones that do and say so.
- Stay inside the request's own meaning. A different product is out of bounds, however appealing.
- For each idea, give:
  - What it is
  - Why a demanding user would notice it
  - Rough cost
- Rank by value for cost. Name the top two. For the first, describe exactly what building it would involve — components, files, order of work — so the next pass can start without re-deriving it.

---

## Red flags

Thought → Reality

- "This is too simple to need a design." → Simple means a short design, not no design. Two sentences in chat, then approval.
- "I'll call it bounded and skip the spec." → Reaching for a label to skip work is the doubt. Take the heavier path.
- "The design is obvious, I'll start while they read it." → The gate is the approval, not the design's length. Present, then stop.
- "I understand this kind of app, so it's bounded." → Bounded measures the repo, not your familiarity. No existing flow means architectural.
- "The spike works, so I'll keep the code." → A spike's output is an answer. Keeping the code is a new request.
- "It grew, but I'm almost done." → Hidden complexity upgrades the path. Stop and say so.
- "They approved the spike, so the follow-up is approved too." → Each task gets its own classification and approval.
- "I need five ideas, so I'll add two weak ones." → Weak ideas hide strong ones. Give what is real and explain the shortfall.
- "It almost certainly works; I'll say I tested it." → Say what you actually ran. Untested is untested.
- "The user probably wants X." → Ask, or state it as an assumption they can reject. Do not build on it silently.
- "I couldn't run it, but I can describe how it probably feels." → Report that you could not use it. Base ideas on what you could read.
