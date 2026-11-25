---
name: contact-qualification-framework
description: Build a contact qualification framework through guided profile review — extract tacit judgment about which contacts are worth pursuing, then organize it into documented criteria with persona classification and fit assessment.
---

# Contact Qualification Framework

This skill guides someone through building a contact qualification framework for their company — the criteria for what makes a specific person at a target account worth pursuing, organized as persona classification (what they do) and fit assessment (whether they're relevant to your sales process). The output is documented criteria they can use to build a repeatable qualification process.

## How This Skill Works

This is a two-part facilitation workflow: an interview that extracts the user's judgment about contact fit, then a framework generation step that organizes what was extracted into a usable document.

1. **Load the cartridge** from `references/cartridge.md` and **use the Skill tool to load `gtm:interview-me`** with the cartridge content as your briefing. Interview Me handles the conversational mechanics; the cartridge tells you what to probe for.
2. **Load the signal idea bank** from `references/signal-idea-bank.md` as a background reference. Don't surface it to the user — draw from it to ask sharper follow-up questions during the profile review.
3. After the interview, **load the generator** from `references/generator.md` and build the framework document section by section with the user.

The user never sees these internals. They experience one continuous conversation.

## Orienting the User

When the user starts, walk them through what's ahead. Use plain language — no internal terminology. Something like:

"We're going to build a contact qualification framework for your company — a clear picture of what makes a specific person at a target account worth pursuing, beyond just their title and seniority. Here's how we'll get there:

1. **Quick context on your company and who you sell to.** We'll start with what you sell, who your target personas are, and how you currently build contact lists. If you have an ICP document or persona definitions, bring them — we'll use them as a starting point.

2. **Checking against your deal data (optional).** If you have CRM data — inbound leads, contacts on closed deals, buying role designations — we can use that to pressure-test your assumptions about who matters. Most companies don't have perfectly clean data here, and that's fine.

3. **Live profile review — this is the core.** You'll pull up contacts at a few target accounts using Sales Navigator, LinkedIn, or whatever tool you use, and react to what you see. I'll ask you about each person: would you reach out, why or why not, what catches your eye. After going through enough profiles, patterns emerge.

4. **Building the framework.** We'll take everything that came out of the profile review and organize it into documented qualification criteria — who you're looking for, how to tell them apart from similar-looking people who aren't a fit, and what action to take with each tier."

Adapt the language to the conversation. If they want to jump in, let them. If they have questions about the process, answer them.

**Tell them what to have ready.** They should have a contact search tool open on another screen — Sales Navigator is ideal, but LinkedIn, ZoomInfo, Apollo, or whatever they have works. If they have CRM data they can reference (exports, saved lists), that's useful but not required.

## The Interview

**Cartridge**: `references/cartridge.md`
**Background reference**: `references/signal-idea-bank.md`

**What it produces:** The user's tacit judgment about contact fit, made explicit — which signals drive their yes/no decisions, how company size changes the picture, where titles mislead, and what attributes matter most.

**What "done" looks like:** You've reviewed enough profiles to surface reliable patterns — usually 5-8 before the first pattern check, across at least two companies per segment the user sells into. You've reflected patterns back and the user has confirmed or corrected them. You've checked whether the criteria hold across company sizes or need segmentation. If patterns feel unresolved or the profiles reviewed lacked variety, offer to continue. The user owns the exit — don't push toward a number.

**How to assess progress:** After 5-8 profiles, start reflecting patterns back. If the user is confirming patterns and new profiles aren't adding new information, you're approaching done. If each new profile reveals something the framework doesn't account for, keep going.

## Framework Generation

**Reference**: `references/generator.md`
**Supporting reference**: `references/signal-idea-bank.md`

**What it produces:** One contact qualification framework document — persona classification (the job functions that matter and how to identify them), fit assessment (the attributes that determine whether someone is worth pursuing), tier definitions that map to action, and open questions.

**What "done" looks like:** The user has reacted to each section. The crystallization pass has been run — the user has been asked where the framework would give the wrong answer, which criteria they're least confident in, and where a rep would get tripped up. Open questions are documented rather than ignored.

## Navigation Principles

**You own the navigation.** The user should never have to ask "what's next?" Tell them where you are, what you're about to do, and when you're transitioning. "OK, I have a good picture of your company and your personas. Let's look at some real profiles and see how your criteria hold up" is a transition. Don't ask the user to initiate it.

**Signpost without being mechanical.** Let the user know where they are — especially during the profile review, which is the longest part. "We've gone through about eight profiles — I'm starting to see some patterns. Let me play those back before we keep going" keeps them oriented. But don't recite the process structure at every turn.

**Transition when the signal is clear, not when a checklist is complete.** If the user comes in with a detailed ICP document and well-formed persona definitions, the context phase might take five minutes. If they're working through uncertainty, it might take twenty. Don't rush past genuine exploration, and don't pad a phase that's already done.

**If the conversation gets stuck, shift gears.** If a line of questioning isn't producing new signal, name it: "I think we've gotten what we can from this angle. Let me try a different approach." Don't keep circling.

## Handling Existing Materials

Some users will arrive with existing documents — an ICP document, persona definitions, a qualification rubric, notes from a previous exercise.

**Read what they bring and map it to the workflow.** A detailed ICP doc might mean the context phase is five minutes of follow-up questions. Existing persona definitions give you a head start on classification. Understand what you have before deciding what to abbreviate.

**The profile review adds something documents can't.** Even if the user has well-documented criteria, the live profile review tests whether those criteria hold when applied to real people. Recommend the profile review even if the user feels their criteria are solid — it almost always surfaces nuance that wasn't captured in the document.

**Take whatever they have on CRM data.** If they can share deal contact associations, inbound lead lists, or buying role data, use it. If the data is messy or incomplete, acknowledge that and move on — most companies are in that situation, and the profile review is where the real signal comes from.

## What Not to Say to the User

- **"Cartridge"** — use phase, step, or just describe what you're doing
- **"Generator"** — say "building your framework" or "pulling this together"
- **"Signal idea bank"** — never reference this; draw from it silently
- **"Elephant vs. ant"** — introduce this distinction when you get to fit assessment. Frame it as "how critical is this signal?" — an elephant is a non-negotiable that changes the decision on its own, an ant is a green flag if true but not a deal-breaker if not. Define it plainly; don't present it as jargon.
- **"Context assets" or "synthesis artifacts"** — just say "what we've covered" or "what we've captured"
- **"Interview Me"** — don't name the methodology; just do the work
- **"Persona classification" and "fit assessment" as technical terms** — use them if the user naturally thinks in those terms, but don't lead with the terminology. "First let's figure out what people actually do, then we'll assess whether they matter for your process" says the same thing.

Speak like someone who's done this before and is walking a colleague through it. Not like a tool describing its own architecture.
