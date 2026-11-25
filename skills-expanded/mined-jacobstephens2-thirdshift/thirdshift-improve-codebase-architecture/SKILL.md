---
name: thirdshift-improve-codebase-architecture
description: "Scan a codebase for deepening opportunities, take the top recommendation, and publish it to the issue tracker: as a plan when it is Strong, as an idea otherwise. Only for an Architecture review."
disable-model-invocation: false
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This is an **Architecture review**. It runs headless: nobody reads a report, picks a candidate or answers a question. Never open a browser, ask a question or wait for an answer. Every decision is yours, and each one is written down with its reason.

It changes nothing in the repository. Never commit, push, create a branch or open a pull request, and never edit `GLOSSARY.md` or an ADR: any change the refactor needs to them is work for a Ticket. The worktree is thrown away when the session ends, so a throwaway prototype in it is fine, and nothing in it survives. What the review produces is issues on the issue tracker.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Use the `thirdshift-codebase-design` skill for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion, and don't drift into "component," "service," "API," or "boundary."
- The domain language in `GLOSSARY.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.

The issue tracker and triage label vocabulary should have been provided to you. If `docs/agents/issue-tracker.md` is missing, fall back to the `gh` CLI. If `docs/agents/triage-labels.md` is missing, use the label names as written here, creating a label the tracker lacks (`gh label create`).

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the Session prompt named a focus (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Look up the focus area's terms in the relevant entries of the project's domain glossary (`GLOSSARY.md`) first. Follow the repository's domain-reading guidance and any separate domain-to-code index; search terms/symbols with `rg -n` and read bounded ranges before widening the scan. Check applicable coding standards and read ADRs in the area you're touching.

Read the open issues too, titles and bodies: Specs, Tickets and ideas alike, whatever their labels. They are what a candidate may already be covered by.

Then spawn a sub-agent to walk the codebase. Don't follow rigid heuristics; explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Take the top recommendation

Weigh the candidates in the session. Write no report file. For each candidate, settle:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: plain English description of what would change
- **Benefits**: explained in terms of locality and leverage, and how tests would improve
- **Recommendation strength**: one of `Strong`, `Worth exploring`, `Speculative`
- **Covered by**: the open issue that already covers it, if one does

A candidate is **Strong** only when all of these hold:

- The friction is real and you can point to it in the code.
- The deepening passes the deletion test.
- You can settle its whole design from the code, `GLOSSARY.md` and the ADRs. A candidate with a decision only a human can make is `Worth exploring` at most.
- It contradicts no ADR, or the friction is real enough to warrant reopening that ADR.

A candidate is **covered** when an open issue proposes the same deepening of the same modules, whether as a Spec, a Ticket or an idea. An issue that only touches the same files doesn't cover it.

Rank the candidates: which you'd tackle first and why. Then take the **top recommendation**:

1. The highest-ranked `Strong` candidate that no open issue covers. It becomes the plan: go on to step 3.
2. If there is none, the highest-ranked candidate of all. If an open issue covers it, file nothing: go to step 6 and name that issue. Otherwise it becomes an idea: go to step 5.

Every other candidate is dropped. Don't file it, and don't list it in the plan or the idea: the next Architecture review starts from the codebase as it is by then.

If the scan surfaced no candidate at all, file nothing, and say so plainly in place of the final line of step 6: there is no issue for it to name.

**Use GLOSSARY.md vocabulary for the domain, and the `thirdshift-codebase-design` skill's vocabulary for the architecture.** If `GLOSSARY.md` defines "Order," talk about "the Order intake module," not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only keep it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the report (e.g. a warning callout: _"contradicts ADR-0007, but worth reopening because…"_). Don't raise every theoretical refactor an ADR forbids.

Do NOT propose interfaces yet.

### 3. Settle the design

Only for a `Strong` top recommendation.

Map the decisions as a **design tree**: every decision branches into the decisions that hang off it. Walk it: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled. Settle the whole frontier yourself, then recompute it. Finding _facts_ is a lookup: when a decision needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it. The _decisions_ are yours too. For each one, write down what you decided and why. The design is settled when the frontier is empty: every branch of the design tree visited, nothing left silently assumed.

If a decision turns out to need a human, the candidate was not `Strong`: make it `Worth exploring` and take the top recommendation again, from step 2.

Side effects are recorded, never written:

- **Naming a deepened module after a concept not in `GLOSSARY.md`?** Record the term and its definition as work for a Ticket.
- **Sharpening a fuzzy term as you decide?** Record the sharper definition as work for a Ticket.
- **Reopening an ADR, or making a decision worth one?** Record the new or changed ADR as work for a Ticket. A decision is worth an ADR only when it is hard to reverse, surprising without context, and the result of a real trade-off.
- **Want to explore alternative interfaces for the deepened module?** Use the `thirdshift-codebase-design` skill and its design-it-twice parallel sub-agent pattern.

### 4. Publish the plan

Only for a `Strong` top recommendation whose design is settled.

Decide the plan's size. If one session, a single fresh context window, is enough for the whole change, the plan is a single **Ticket**. Otherwise it is a **Spec** with **Tickets**. Don't force a small refactor into a Spec.

- **A Spec with Tickets**: use the `thirdshift-to-spec` skill to publish the Spec, then the `thirdshift-to-tickets` skill to publish its Tickets as the Spec's sub-issues.
- **A single Ticket**: use the `thirdshift-to-tickets` skill to publish one standalone Ticket, with no parent.

The plan's top issue, the Spec or the single Ticket, is labelled `needs-triage` and nothing else. thirdshift marks it ready once the session has ended and the plan passes its checks; you never do. Tickets under a Spec are labelled `ready-for-agent`.

The plan's top issue carries, whichever shape it takes:

- **Every decision from step 3, each with its reason.** In a Spec, under Implementation Decisions and Testing Decisions. In a single Ticket, under a `## Decisions` heading added after the issue template's sections.
- **The report**: the candidate's card as Markdown with a Mermaid before/after diagram. In a Spec, under Further Notes. In a single Ticket, under an `## Architecture review` heading added last, after `## Decisions`. See [REPORT.md](REPORT.md) for the card.

The `GLOSSARY.md` and ADR changes recorded in step 3 go into the acceptance criteria of the Ticket whose work they belong to, a Spec's Ticket or the single Ticket, so they land through its pull request.

### 5. File the idea

Only for a top recommendation that is not `Strong` and that no open issue covers.

Publish one issue to the issue tracker, labelled `needs-triage`, for a human to flesh out. Its title names the deepening. Its body is the report: the candidate's card as Markdown with a Mermaid before/after diagram, its recommendation strength, and what stopped it being `Strong`. See [REPORT.md](REPORT.md) for the card.

Publish nothing else: no Spec, no Tickets, and no second idea.

### 6. End with the final line

Unless the scan surfaced no candidate at all, end your final message with the one final line the Session prompt asks for, in exactly the format it gives. The format is defined there and nowhere else. The line names one issue:

- the plan's top issue, when you published a plan;
- the idea issue, when you filed one;
- the open issue that already covers the top recommendation, when you filed nothing.

Include any recommendation metadata the Session prompt asks for before that final line. Keep the full candidate card in the issue.
