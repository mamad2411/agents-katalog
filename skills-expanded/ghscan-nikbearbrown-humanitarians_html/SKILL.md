---
title: "Claude, Dpa Review., The DPA-Review Skill"
seoTitle: "How Claude's DPA-review skill actually works"
description: "Explains how Claude's dpa-review skill checks a vendor data processing agreement against a fixed clause checklist instead of judging it."
summary: "A skill called dpa-review has Claude check a vendor's Data Processing Agreement against a fixed list of required clauses, including sub-processor naming and end-of-contract data handling, without judging whether the terms are actually adequate."
keywords: ["how does claude review a data processing agreement", "dpa review skill claude explained", "what clauses does claude check in a dpa", "sub processor clause missing from vendor agreement", "claude skill md file explained legal review", "data deleted or returned after contract ends", "does claude approve vendor agreements", "checklist for reviewing a data processing agreement"]
generated: "article"
---

When Claude reviews a vendor's Data Processing Agreement, it is not approving the agreement. It is reading a Skill, a folder with one instruction file, and executing a fixed checklist against the document. Understanding that distinction changes what you should and should not expect from the output.

## What a Skill is, mechanically

A Skill is a folder Claude reads before it acts. The dpa-review skill is a single file, SKILL.md, written in plain language with no hidden logic and no freeform judgment built in. Claude reads the file, then executes each step in order. The instructions live in a step section, and the process is linear: read the file, execute each step, return the result. There is no branching unless a specific step calls for it. The file is the program; Claude is running it, not improvising around it.

## The two clauses that go missing most often

One rule inside this particular skill is specific and worth naming directly. Claude checks whether the agreement names every sub-processor involved in handling the data, and whether it states what happens to the data when the contract ends, whether it gets deleted or returned. According to the skill, these two clauses are the ones vendors leave out most often. Flagging their absence is a mechanical check: is the clause present in the text or not.

## What the checklist cannot do

The skill cannot judge whether the security measures described in the agreement are actually strong enough for the data involved. That is a substantive judgment call that requires someone who understands the systems, the data sensitivity, and the vendor's actual practices, not just the words on the page. Claude is not evaluating whether the agreement is good enough. It is checking the SKILL.md's list of required clauses, one step at a time, and only doing what that file instructs.

## Running it on your own agreement

The practical exercise is straightforward: before signing a vendor's data processing agreement, ask Claude to read the dpa-review skill and, before checking anything, explain exactly what it will do. Which clauses will it check for, what counts as missing, and what will it not be able to tell you. Running that walkthrough first makes the limits of the review visible before you rely on the output, and it should be run on your own actual agreement rather than a hypothetical.

## Why the distinction matters

Treating a Skill's output as a mechanical clause check, rather than a legal opinion, keeps expectations calibrated. The skill is useful precisely because it applies the same fixed list every time, catching the two most commonly missing clauses without variation. But nothing about that mechanism substitutes for a privacy lawyer's judgment on whether the substance of an agreement is adequate. The checklist is the limit of what this step does.

## Key takeaways

- Claude's dpa-review skill checks a Data Processing Agreement against a fixed, written list of required clauses; it does not approve or evaluate the agreement.
- The skill runs as a linear pipeline: read the file, execute each step, return the result.
- Two clauses are flagged specifically because they go missing most often: naming every sub-processor, and stating what happens to data at contract end.
- The skill cannot judge whether described security measures are actually adequate for the data involved; that requires a person who knows the systems.
- Before relying on the review, ask Claude to walk through what it will check, what counts as missing, and what it cannot tell you.

## Who this is for

Anyone responsible for reviewing vendor data processing agreements who wants a fast, repeatable first pass on clause completeness, with a clear understanding that it is not a substitute for legal judgment on substance.
