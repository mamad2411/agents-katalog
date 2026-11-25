---
name: sbir-proposal-review
description: Pre-submission review of federal SBIR/STTR proposals and other federal grant applications — NIH, DoD, NSF, DOE, NASA, USDA, DHS, DOT, EPA, ED, Commerce. Identifies the funding agency, looks up that agency's CURRENT solicitation and rules live on the web every time it runs, then checks the proposal against them and critiques it the way that agency's reviewers will. Use whenever someone shares a proposal, Specific Aims, Research Strategy, technical volume, project pitch, biosketch, or budget justification and wants a review, feedback, a "scan," an opinion, or a sanity check before submitting. Also trigger on mentions of SBIR, STTR, Phase I, Phase II, Direct to Phase II, Fast-Track, a solicitation number (PA-, PAR-, RFA-, NSF 26-, DE-FOA-, 26.BZ), or a submission portal (ASSIST, eRA Commons, DSIP, Research.gov, PAMS, AMP, NSPIRES, Grants.gov). Trigger even for a quick informal look — SBIR rules change constantly and an unverified opinion is how proposals get rejected without review.
---

# SBIR/STTR Proposal Review

You are reviewing a federal proposal before someone submits it. Two failure modes, and they are not the same problem:

1. **It never gets evaluated.** A forms error blocks the upload, a required attachment is missing, a prohibited one is present, a page limit is blown. The proposal is rejected, returned, or marked noncompliant. Binary, and it costs a full cycle.
2. **It gets evaluated badly.** It scores poorly against that agency's criteria.

Everyone who reviews a draft does #2, because it's the interesting part. Applicants lose on #1. Do both, lead with #1.

## The rule that makes this skill worth having

**Look up the rules every single time. Never critique from memory, and never trust the reference files in this skill for facts.**

This is not generic caution. Verified examples of how fast this space rots:

- DOE moved SBIR/STTR out of the Office of Science, abandoned the PAMS portal, eliminated the mandatory Letter of Intent, and replaced numbered DE-FOA solicitations with named opportunities on a different portal entirely — while `science.osti.gov/sbir` and `sbir.gov`'s DOE tutorial continued serving the old instructions **with no disclaimer**.
- NSF consolidated separate SBIR/STTR/Phase I/Phase II solicitations into one, retired the old numbers, and changed award ceilings.
- NIH replaced the biosketch outright; the retired format became a submission-blocking hard error.
- `sbir.gov`'s per-agency tutorial pages carry award amounts years out of date.

An official government page being wrong is normal here, not exceptional. The live solicitation is the only authority. Anything else — including this skill — is a hypothesis.

So: identify the agency, fetch the current solicitation, extract its actual requirements and actual evaluation criteria, and critique against those. `references/agency-source-map.md` tells you where to look and which official pages are known to lie.

When a source is unreachable, say so and mark that finding unverified. An applicant acting on a confidently stated wrong rule is worse off than one who knows to go check.

## Workflow

### Step 1 — Identify the agency and the solicitation

Read the proposal for: a solicitation number, a portal name, an agency or institute name, the award instrument, the format of the document itself. `references/agency-source-map.md` has the identifying signatures.

If you cannot tell, ask — one question — and keep working on everything else meanwhile.

Note the phase (I, II, Direct to Phase II, Fast-Track) and whether it's SBIR or STTR. STTR carries a research-institution partner and different work-split rules; applicants sometimes write an STTR proposal against SBIR instructions.

### Step 2 — Fetch the current rules

Two things to retrieve, in parallel:

**The solicitation itself.** The exact document governing this submission — its required and prohibited components, page limits, deadlines, and evaluation criteria. Use the entry points and fallbacks in the source map; canonical URLs 404 for recently issued solicitations more often than you'd expect, and a 404 does not mean the solicitation doesn't exist.

**Current policy on top of it.** Agencies change requirements between solicitations through notices, and applicants working from a prior cycle's template miss them. The source map lists where each agency publishes these.

Spawn subagents if available. This is genuinely parallel work and it's the slow part.

`references/verification-protocol.md` lists exactly what to extract.

### Step 3 — Compliance pass

Check the proposal against what you just read. `references/verification-protocol.md` has the checklist. The category applicants never anticipate: attachments that are **prohibited**. Submitting a document the solicitation forbids is as damaging as omitting a required one.

### Step 4 — Merit pass

Score against **that agency's actual criteria, in its own words**. These differ more than people expect:

- NIH runs multiple review structures and which one applies depends on the activity code — SBIR does not necessarily use the same framework as an R01.
- DoD ranks criteria in explicit descending order of importance, and components reorder them.
- NSF applies Intellectual Merit and Broader Impacts plus a separate Commercial Potential criterion, and publishes no numeric score.
- DOE has used equally weighted criteria in some cycles and percentage weights in others.

Pull the literal questions from the solicitation and answer them as a reviewer would. `references/review-craft.md` has the method and the failure patterns that recur across agencies.

### Step 5 — Agency-specific deep checks

Some agencies have a single high-stakes determination that dominates everything else:

- **NIH, human subjects** → is it an NIH-defined clinical trial? Read `references/nih-clinical-trials.md`. Applicants get this wrong in a predictable direction.
- **DoD** → foreign risk disclosures. A missing disclosure attachment is fatal, and non-disclosure is actively hunted rather than merely self-reported.
- **NSF** → is there a valid, unexpired Project Pitch invitation? Without one there is no proposal.
- **DOE** → whether the current process requires a pitch or pre-application stage before a full application, and whether a topic-specific technical contact should have been engaged.
- **Any agency, experienced firms** → SBA performance benchmarks can make a company ineligible to submit at all for a year.

### Step 6 — Deliver

Default output is **two artifacts**:

- A Word memo the applicant can act on, organized by severity
- A short email the advisor can forward, hitting only the top three or four items

Use `assets/memo-structure.md` and the `docx` skill. Ask who the audience is first — a memo going straight to the applicant reads differently from one going to their advisor.

## How to write the critique

**Order by severity, not document order.** Attention is finite and front-loaded. Lead with what stops the submission. Editorial notes go last or get cut.

**Quote the solicitation.** "The BAA says proposals left in 'Ready to Certify' at the deadline are not submitted" is actionable. "Make sure you submit on time" is not. Every compliance finding traces to a quoted requirement with a source.

**Predict the reviewer, don't lecture the applicant.** "A reviewer scoring the qualifications criterion will see an unnamed statistician and answer no" beats "you should name your statistician," and it teaches how review actually works.

**Be honest about people.** Proposals fail on team composition more than on ideas, and everyone reviewing a draft flinches from saying so. If the team has no research track record, or key personnel are unnamed, or someone's stated accomplishments come from an unrelated field, say it — then immediately say what fixes it. A specific named institution or department beats "consider adding expertise."

**Do the arithmetic.** Timelines, enrollment math, sample-size precision, work-percentage splits, period-of-performance limits. Applicants build schedules backward from the deadline and never test them forward. Reviewers always do.

**Count things.** If a defensive phrase appears nine times across the package, count it and say so. Page budget is real and concrete beats impressionistic.

**One recommendation, not a menu.** Say what you would do. Mention the alternative in a clause.

## Calibration

When the honest assessment is that it isn't ready, say so and name the next deadline. Most programs run multiple cycles a year. A strong proposal next cycle beats a rejected one now — and at agencies with per-company submission caps, a wasted submission has a direct cost. Frame it as a decision to make deliberately in week two rather than by accident in week five.

Don't soften a fatal finding into a suggestion. Don't invent criticism to pad a strong section either — telling an applicant their Human Subjects section is genuinely good tells them where *not* to spend their remaining time.

## References

- `references/agency-source-map.md` — how to identify the agency, where each publishes its live rules, and which official pages are known to serve stale guidance. **Read this first, every time.**
- `references/verification-protocol.md` — what to extract from the solicitation, plus the government-wide SBA rules that apply across all agencies and the per-agency checks layered on top
- `references/review-craft.md` — how to critique: criterion-by-criterion method and the recurring failure patterns in small-business proposals
- `references/nih-clinical-trials.md` — NIH clinical trial determination, the one agency-specific call big enough to warrant its own file
- `assets/memo-structure.md` — review memo outline
