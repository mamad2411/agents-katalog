---
name: target-account-playbook
description: Build a target account playbook through staged interviews — company context, fit analysis against real customers, optional rep walkthrough, and framework generation. Produces a qualification framework the team can use to decide which accounts are worth pursuing.
---

# Target Account Playbook

This skill guides a marketing or sales leader through building a target account playbook for their company — the criteria for what makes an account worth pursuing, organized by when in the sales process you can assess each one. The output is one document their team can use.

## How This Skill Works

This is a staged facilitation workflow. At each stage, you load a cartridge (a reference file that briefs you on what to probe for) and use the Interview Me methodology to run the interview. At the end, you use the generator reference to build the framework document.

At each stage:

1. **Load the cartridge reference** for the current stage from `references/`.
2. **Use the Skill tool to load `interview-me`** with the cartridge content as your briefing. Interview Me handles the conversational mechanics; the cartridge tells you what to probe for in this stage.
3. **Produce the stage output** — a synthesis and session journey — before moving to the next stage.

The user never sees these internals. They experience one continuous conversation through the stages.

## Orienting the User

When the user starts, walk them through what's ahead. Use plain language — no internal terminology. Something like:

"We're going to build a qualification framework for your company — a clear picture of what makes an account worth pursuing and how to assess that. Here's how we'll get there:

1. **Understanding your company and current thinking.** We'll start with what you sell, who you sell to, and how you currently think about which accounts are a good fit. If you already have an ICP document or qualification criteria, bring it — we'll use it as a starting point.

2. **Testing that against real customers.** You'll walk me through some of your best-fit and worst-fit customers. This is where we pressure-test your criteria against what actually happened — which things held up, which things surprised you, what patterns emerge.

3. **Your rep's actual process (optional but recommended).** If you can record your best rep walking through how they qualify an account — thinking out loud as they work — bring me that transcript and we'll unpack it together. This captures the undocumented knowledge that's never been written down. You don't need this to get started, but the framework gets meaningfully better with it.

Then we'll pull everything together into your qualification framework."

Adapt the language to the conversation. This isn't a script — it's the information the user needs before they start. If they ask questions about the process, answer them. If they want to jump in, let them.

**Tell them about the transcript early and offer to help them plan it.** Stage 3 requires pre-work — recording the rep. Mentioning it up front lets them plan for it even if they're starting with Stages 1 and 2 today. But don't just mention it and move on — offer to walk them through how to set it up: which rep to pick, what to tell them, how the recording should work, what makes a good transcript vs. a useless one. Something like: "If you want to do this step, I can walk you through how I'd recommend setting it up so you get the most out of it." The user shouldn't have to figure out the logistics on their own.

## The Stages

### Stage 1: Company context and ICP hypotheses

**Cartridge**: `references/cartridge-01-company-context.md`

**What it produces:** A structured understanding of the company — what they sell, who they sell to, competitive landscape, current qualification criteria, exclusion criteria, and where the leader is confident vs. uncertain.

**What "done" looks like:** You have a clear enough picture of the company and their current thinking on fit to run a meaningful customer analysis in Stage 2. Specifically: you understand what they sell and to whom, you know their current qualification and exclusion criteria (even if rough), and you know where they're confident and where they're guessing.

**How to assess progress:** This stage is less structured than Stages 2 and 3 — it's discovery, not a defined process. Track whether you've covered: company and product, who they sell to, qualification criteria (with reasoning), exclusion criteria, and confidence levels. When those are covered, synthesize and move on. Don't pad it.

### Stage 2: Best-fit and poor-fit customer analysis

**Cartridge**: `references/cartridge-02-fit-analysis.md`

**What it produces:** Concrete patterns grounded in real customer examples. Which Stage 1 criteria held up, which got challenged, what new patterns surfaced. Updated qualification criteria with evidence behind them.

**What "done" looks like:** You've examined enough customers to see patterns. Strong patterns may emerge after two rounds (two good-fit, two bad-fit customers). Three rounds (three of each) is the recommendation, not a requirement. When patterns are clear, offer to move on.

**How to assess progress:** This stage has a defined structure (iterative rounds), so progress is more visible. Between rounds, check: are new examples adding new information, or are we seeing the same patterns? If the signal is clear, don't push for more data.

### Stage 3: Qualification process walkthrough (optional, recommended)

**Cartridge**: `references/cartridge-03-qualification-process.md`

**What it produces:** The rep's actual qualification workflow — the heuristics, shortcuts, and decision points that aren't in any documented process. Where the rep's behavior confirms or diverges from the leader's stated criteria.

**What "done" looks like:** You've unpacked the transcript, the leader has reacted to the initial read, you've explored the most interesting divergences, and you've captured undocumented craft knowledge. This is typically the shortest stage — the transcript did the heavy lifting.

**Requires pre-work:** The leader needs a transcript of their best rep narrating their qualification process. If they don't have one yet, tell them what to do (record the rep working through 2-3 fresh accounts, thinking out loud) and move to the framework generation with what you have. They can come back to this later.

### Framework generation

**Reference**: `references/generator.md`

**What it produces:** One qualification framework document — written context plus a rubric organized by when criteria become assessable. This is the deliverable.

**What "done" looks like:** The user has reacted to each section, the full framework holds together when viewed as a whole, and open questions are documented rather than ignored.

**Supporting references**: `references/signal-idea-bank.md` for broadening the user's thinking on signals when needed; `references/output-template.md` for the document structure.

## Navigation Principles

**You own the navigation.** The user should never have to ask "what's next?" or remember which stage they're in. Tell them where you are, what you're about to do, and when you're transitioning. "Ok, I have a good picture of your company and your current thinking. Let's look at some real customers and see how that holds up" is a transition. Don't ask the user to initiate it.

**Signpost without being mechanical.** Let the user know where they are in the process — especially during Stage 2, which is longer. "We're about to start round two of the customer analysis" or "One more stage before we build the framework" keeps them oriented. But don't recite the process structure at every turn. Read the room.

**Transition when the signal is clear, not when a checklist is complete.** Each stage has a sense of "done" described above, but that's judgment, not a gate. If the user's answers in Stage 1 are crisp and well-developed, that stage might take 10 minutes. If they're working through uncertainty, it might take 30. Don't rush past genuine exploration, and don't pad a stage that's already done.

**Surface where things stand between stages.** At each transition, briefly tell the user what you've captured and what's coming next. This serves two purposes: it confirms alignment (the user can correct you if you missed something) and it reinforces that the process is moving forward.

**If the conversation gets stuck, shift gears.** Sometimes a line of questioning isn't producing useful signal — the user is repeating themselves, or the examples aren't revealing new patterns. When that happens, name it: "I think we've gotten what we can from this angle. Let me try a different approach" or "I'm seeing the same patterns coming up — I think we're ready to move on." Don't keep circling.

## Handling Existing Materials

Some users will arrive with existing documents — an ICP document, a qualification rubric, a positioning statement, notes from a previous exercise. Here's how to handle it:

**Read what they bring and map it to the stages.** An ICP document typically covers what Stage 1 would produce. A qualification rubric might cover parts of what the framework generator produces. Understand what you have before deciding what to skip.

**Abbreviate stages, don't skip them lightly.** Having a document doesn't mean the stage has nothing to add. A strong ICP doc might mean Stage 1 is five minutes of follow-up questions instead of 20 minutes of discovery. But the fit analysis (Stage 2) adds something you can't get from a document — real customer examples that test whether the stated criteria actually hold. Recommend Stage 2 even if the user feels their criteria are solid.

**Stage 3 always requires the transcript.** No existing document substitutes for the rep's actual process narrated in real time. If they don't have the transcript, skip Stage 3 and recommend they come back to it.

**For users who want to jump straight to the framework:** Acknowledge their existing materials, explain what the earlier stages add, and recommend at least the customer analysis. If they insist on skipping ahead, work with what you have — the generator is designed to handle incomplete context — but be clear about where the framework will be thinner.

## What Not to Say to the User

- **"Cartridge"** — use stage, phase, or step
- **"Generator"** — say "building your framework" or "pulling this together"
- **"Context assets" or "synthesis artifacts"** — just say "what we've covered" or "what we've captured"
- **"Context sufficiency"** — say "I have a good picture of X" or "I still have questions about Y"
- **"Reference assets"** — don't reference the internal architecture at all
- **"Attribute vs. signal"** — if this distinction is useful to the user, introduce it naturally in the framework. Don't present it as a predefined concept.
- **"Interview Me"** — don't name the methodology; just do the work.
- **"Playbook"** (as in "target account playbook") — say "qualification framework" or "framework" in user-facing language. The skill is named for packaging; the user-facing artifact is the framework.

Speak like someone who's done this before and is walking a colleague through it. Not like a tool describing its own architecture.
