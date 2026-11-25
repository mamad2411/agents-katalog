---
name: developer-survey-design
description: >-
  Designs a recurring survey of external developers - an annual "State of" community survey or a
  product survey - from the decisions it informs to the published report: question cuts,
  recruitment and a calibration sample, pilot, GDPR, cleaning, analysis and a
  methodology section that makes headline numbers defensible. Use whenever someone plans a
  developer or community survey, inherits a questionnaire drafted by marketing, wants to publish
  percentages from their own survey, or asks about sampling bias, response rates, incentives,
  survey length or year-over-year comparison - even if they only say "we want to run a State of
  X". Not internal employee surveys or one event's feedback form. Do NOT use for community NPS or
  pulse items - use samber/developer-relations-skills@developer-community-health.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Developer Survey Design

You design developer surveys that inform real decisions and publish numbers that survive scrutiny.

A developer survey is two products at once: a measurement instrument and a publication. Most failures come from the publication side asking the instrument for claims it cannot carry. A survey recruited through the project's own blog, Discord and newsletter measures the people those channels reach, mostly engaged fans. "62% of developers use X" from that sample is false; "62% of respondents use X" is true and still useful.

Design around three promises. Every question changes a named decision or earns a place in the published report. Every published number states who answered, how many, and the exact wording. Every respondent's data is handled as the privacy notice says.

Stay out of neighbouring jobs:

- Who the segments are: samber/developer-relations-skills@developer-segmentation (a survey can feed it)
- Community health pulse items (recommendability, burnout, newcomer welcome): samber/developer-relations-skills@developer-community-health
- DevRel KPIs and targets: samber/developer-relations-skills@devrel-metrics
- Tracking and instrumentation: samber/developer-relations-skills@devrel-analytics
- Routing feature requests to product: samber/developer-relations-skills@developer-feedback-loop
- One event's attendee survey: samber/dev-event-organizer-skills@event-feedback, if that collection is installed

## Interview

Ask one question at a time, multiple-choice where you can, skipping what the user already said. Questions 1-4 gate the design; stop after them when the work order below says so.

When the user only wants to vet a percentage from a survey someone else ran, skip the interview: apply Step 2's claim ladder to that survey's published methodology and stop.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. Which decisions will the results feed, and who owns each one (roadmap, docs, community programme, marketing positioning)?
2. Will results be published outside the team? Will anyone quote headline percentages, in a report, a press release or a sales deck?
3. Who is the population: users of the product, community members, the wider language or tool ecosystem, prospects?
4. Is this a one-off, or the first edition of a yearly series? When must results land?
5. Which surfaces do you control that reach that population: product or CLI prompt, docs, release notes, user email list, blog, newsletter, community channels, partners?
6. Is there a draft questionnaire already? Paste it.
7. What does telemetry or other data already tell you (usage, versions, OS, region, downloads)?
8. Who analyses the results, and how many hours do they have, especially for reading open-text answers?
9. Where are respondents and the organisation based? Is a partner co-running the survey? Is any incentive planned?
10. Has a previous edition run? Share its questions and channel mix.
11. Which survey tool will you use? Can it carry hidden fields, route questions, and switch off IP logging?

Answers 1 and 2 set the work order:

- **No decision owner and no publication plan:** recommend not running the survey yet. Offer five user interviews instead, which answer "what should we ask" faster than a survey.
- **Decisions named, nothing published:** run every step; Step 9 shrinks to an internal readout.
- **Publication planned:** run every step, and treat the claim rules in Step 2 as release blockers.

Answers 2, 4, 5, 7, 8 and 9 re-rank or delete options below. Say which answer moved which option, in one block at the top of the survey plan, one line each: `Answer <n> (<value>): <option> promoted | demoted | deleted, because <reason>`.

- A one-off with nothing published (2, 4) moves owned channels to first and makes the calibration sample optional (Step 3); a yearly series freezes the core module (Step 4).
- A date under four weeks away (4) demotes the calibration sample and the pilot's cognitive interviews to "next edition"; owned channels and an expert-review pilot remain.
- No product surface or user list (5) deletes the calibration sample; name the gap in the bias sentence.
- Telemetry (7) deletes the questions it answers (Step 1) and becomes a bias check (Step 2).
- Few analyst hours (8) cut open-text boxes before closed questions (Step 4) and delete paid ads (Step 3).
- Respondents in the EU or UK, or a partner co-running the survey (9), make Step 7 a release blocker and push prize draws to the bottom of Step 8.

## Step 1 - Earn every question

Build a decision table before writing or keeping any question. One row per question: the decision it informs, the owner, and what answer would change that decision. A question with no row is cut. Book a readout with each owner before launch; results with no meeting waiting for them go unused.

Cut three more kinds of question:

- **Questions telemetry answers.** Version, OS, install method and region are measured better than recalled. Ask only where telemetry is missing or opt-in, and say so in the methodology.
- **Questions nobody will act on either way.** "Would you like better docs?" returns yes.
- **Questions the sample cannot answer.** "What share of the ecosystem uses us?" needs a population the channels never reached. "Are we faster than X?" needs a benchmark, not opinions.

Publication questions are legitimate: a headline about tool adoption is a reason to run a survey. Mark them `publish` in the table. They take the same claim rules as everything else, and they compete for the same minutes.

When a draft from marketing or leadership arrives, run it through the table with the author rather than cutting it alone. Each cut reads "no decision named" or "telemetry answers this", never "bad question". Keep the original number beside each kept, merged or rewritten question, so the author can trace every item.

## Step 2 - Fix the population and the claim ladder

Write the target population in one sentence ("developers who used the product in the last 12 months") and the sampled population next to it ("people reached by our blog, docs banner and Discord"). The gap between those sentences is the bias the report must name.

Every published number sits on one rung of this ladder. Write the rung into the publication plan per question:

1. "X% of respondents": always allowed, with n and wording.
2. "X% of users invited at random through <surface>": allowed when Step 3's calibration sample exists. Print the group's invited-to-completed rate beside the number: a random invitation with a low completion rate still carries most of an opt-in survey's nonresponse bias.
3. "X%, weighted to <benchmark>": allowed only with a benchmark for each weighting variable, its source published, and the unweighted figure beside it. A published source is not an independent one: say when the benchmark is your own estimate.
4. "X% of developers" or "of the ecosystem": not available from an opt-in survey. Rewrite to rung 1.

Trend claims ("up 8 points") are allowed only on core-module questions with unchanged wording and position and a similar source mix. Otherwise label the pair "not comparable".

Every chart carries, so it survives being cropped: exact wording; who saw it and n; "multiple answers allowed" where true; how "Don't know" was handled, the same way every year; its rung.

Segment gaps cannot be tested formally on an opt-in sample. Write the reading rule before analysis: a gap counts only when it is large enough to change the decision and its direction holds in every source channel that clears the subgroup minimum. Report smaller channels, often the calibration group, as "untested", never as agreeing.

Never print a margin of error on an opt-in sample. AAPOR states that margin of sampling error does not apply to opt-in online surveys; "n=385 gives ±5%" assumes a random sample. A rung-2 calibration group is the exception: its sampling error may be shown with the stated assumption that nonresponse is ignorable. Label any other interval model-based and state the assumption.

Do not report a response rate for open-link channels: they have no denominator. Report the funnel instead (views where known, starts, completes, kept). A calibration group has a denominator; publish its invited, started and completed counts.

When telemetry measures something the survey also asks about (OS, version, deployment target), compare the two distributions as a bias check. Do not weight to install or instance counts: they count machines, not people. Account-level data where one account is one person in the target population, such as a cloud product's user base, is a legitimate rung-3 benchmark.

## Step 3 - Choose recruitment channels

Rank channels by publishable, bias-measurable responses per hour of effort. The default below assumes the usual case for this skill, a published or yearly survey:

- efficiency: random calibration subsample > owned channels (blog, newsletter, docs banner, release notes) > partner-sent invitations > targeted outreach to under-represented groups > paid ads
- effort (least first): owned channels (a post and a link) > partner-sent (one ask per partner) > calibration subsample (a small engineering change or a random draw from the user list) > targeted outreach (relationship work per group) > paid ads (budget, fraud screening)
- value (bias reduction): calibration subsample (measures how far the self-selected respondents drift) > paid ads (reach beyond the community, at a fraud cost) > targeted outreach (narrows one known gap) > partner-sent (a second audience with its own skew) > owned channels (volume, mostly fans)

The calibration subsample leads because only it makes rung 2 and a bias measurement possible: show the survey prompt to a random fraction of product users, then compare that group with self-selected respondents question by question. Owned channels run in every survey for volume, never as representative. For an unpublished one-off, owned channels move to first and the calibration subsample becomes optional.

Efficiency starves paid ads: second on value, last on effort. Promote them only when Step 2's bias check shows a large group the owned channels miss and someone can screen fraud.

Further rules:

- Size the calibration group to clear Step 9's subgroup minimum for the subgroups you plan to compare. Invite each user or install once, remind the same draw at most once, and use single-use tokens kept apart from the answers, so a forwarded link cannot contaminate the group.
- Tag every response with its source channel through distinct links or a hidden field. Publish the source mix.
- Decide the survey language. A single-language survey under-samples everyone less comfortable in it; translate or name that gap in the bias sentence.
- Partners send the invitation to their own lists. Never import a partner's list.
- Leave scraped addresses out entirely, commit metadata included: it breaks email rules in several jurisdictions and the trust of the people you survey.
- Fix the field window before launch. Published developer surveys stay open from two weeks (Go) to about three months (JetBrains).
- Show sponsors and partners the outline when everyone else sees it, never a private draft. Name in the methodology who could see and change the questionnaire.

## Step 4 - Set the length budget

Set a target median completion time before choosing questions, then spend it. Budget the longest routed path, not the average one. Published developer surveys run from a 12-13 minute median to about 30 minutes on average with heavy routing. Longer stated length lowers starts, and later questions get faster, thinner answers. No study sets an ideal length: price the decision-table questions, add the publish questions, and cut until the total fits what you can state honestly in the invitation.

- Price per screen or per grid row, never per question: a 30-row tool grid is one question and several minutes. Time the soft launch (Step 6) and re-price from it.
- Price each open-text box at a minute or more for the respondent, and at analyst time for coding. Time yourself coding 50 answers, extrapolate to the expected completes, and cap boxes at what question 8's hours cover.
- Put the questions that feed decisions early; position degrades quality.
- Route: show a section only to respondents it applies to.
- For a yearly series, split a **core module** of decision questions kept word-for-word every year from a **rotating module** for this year's topic. Step 2's trend rule applies only to the core module.

## Step 5 - Write the questions

Write for the answer you would act on:

- Use item-specific scales ("How easy or hard is it to…? Very easy … Very hard"), not agree/disagree statements: agree/disagree items produce lower-quality data and inflate agreement.
- Ask behaviour before attitude, and frequency in a concrete window ("in the last 3 months").
- Keep one idea per question. Split "fast and reliable".
- Strip the product's marketing vocabulary and any praise from the stem.
- Make options exhaustive and exclusive, with "Other (please specify)" and "Don't know" or "Not applicable" where true.
- Randomise option order for unordered lists; keep scales in fixed order.
- Put demographics late and optional, in broad bands.
- Keep the same scale direction everywhere.
- For role, experience and tool-use questions you want to set beside a large published survey, copy its wording word for word and cite it. A paraphrase breaks the comparison.

Good and bad pairs, scale templates and the demographic block: [./references/question-writing.md](./references/question-writing.md).

## Step 6 - Pilot before launch

1. **Expert review:** one person outside the team reads every question against Step 5, then completes it on a phone and with a screen reader; grids and long multi-selects fail first there.
2. **Cognitive interviews:** five to fifteen developers think aloud while answering; fix every question two of them read differently. The range is common practice, not a measured threshold.
3. **Soft launch:** send to a small slice of one channel, check median time against the budget, breakoff point and empty answers. Tag these responses `pilot`; keep them only if no wording changes afterwards.
4. **Freeze the wording before the full launch.** A change after it splits the data into two incomparable groups.

When question 4's date rules out interviews, keep the expert review and the soft launch, and log the gap in the methodology.

## Step 7 - Handle personal data

Treat the survey as personal-data processing unless nothing can identify a respondent. Pseudonymised data, an email beside an answer, or a rare combination of country, role and company size all count.

- Pick the legal basis per purpose. Aggregate research often runs on legitimate interest with an opt-out; follow-up contact, panel enrolment, raw-data sharing and sensitive items take separate, unticked consent.
- Publish a privacy notice on the first page: who runs the survey, purposes, legal basis, processors and partners, transfers, retention, rights, and what open data will be released.
- Keep identifiers out of the response table. Collect contact details for follow-up or incentives in a separate form.
- Treat Article 9 data (ethnicity, politics, religion, trade-union membership, health, sexual orientation) and gender identity as sensitive: optional, "prefer not to say", explicit consent by default, aggregate reporting only.
- Put an age gate right after the privacy notice, before question 1.
- Never publish raw open text; publish coded themes and quotes checked for names and employers.
- Merge or suppress any published cell, chart slice or open-data combination under 10 respondents. No regulator sets this number; it is a defensible convention.
- Delete identifiable raw data once cleaning and analysis finish; carry only anonymised data into the next edition.

A survey that also collects leads for sales is marketing, and marketing-email rules apply. When marketing asks for demo interest, budget or a "nurture" list, cut those items and link the existing signup page from the thank-you screen, under its own consent. Notice wording, the processor and partner split, invitation rules and retention: [./references/privacy-and-consent.md](./references/privacy-and-consent.md). Check the result with whoever handles data protection for the organisation; this skill gives the checklist, not legal advice.

## Step 8 - Decide on an incentive

Rank incentives by completes gained per unit of effort and risk:

- efficiency: none, with results shared first with respondents > a donation per complete > a badge or small thank-you for every completer > a prize draw > paid responses
- effort (least first): none > donation > badge > prize draw (rules, contact data, winner handling) > paid responses (payments, fraud screening)
- value: paid responses (material incentives raise starts and completes, modestly, across web-survey experiments) > prize draw == badge == donation == none (draw effects are small and inconsistent; badges and donations are untested; no evidence separates the four for an open-link developer survey)
- compliance cost (least first): none == donation (no contact data, no sweepstakes rules) > badge (an account link) > prize draw (contact data, a separate store, sweepstakes rules per jurisdiction) > paid responses (payment data, tax)

Default to none, plus results shared with respondents first: posted to every recruitment channel before any press release. Efficiency starves paid responses: a small gain, shared with prize draws, and the highest fraud pull. Move to a donation, then paid responses, only when question 4's date is near and the soft launch shows too few completes. Large surveys that run prize draws absorb a legal and fraud-screening cost this default assumes you lack. Any public incentive draws bots and machine-written answers: switch on Step 9's fraud checks before launch.

## Step 9 - Clean, analyse and publish

Write the cleaning rules before fielding, and report what each removed: qualifiers (wrong population), speeders below a self-set fraction of the median for their routed path, straight-lined grids, duplicates, bots and machine-written answers. Keep email and account IDs out of the response table even for fraud control; when an incentive is public, a salted hash of the IP address in a separate column, declared in the notice and dropped at cleaning, is proportionate. Publish the funnel: views where known, starts, completes, kept.

Report distributions, never Likert means alone, with Step 2's chart caption and gap rule. Set a minimum subgroup n before analysis, label it self-set, and hide subgroups below it; it sits above Step 7's privacy floor of 10, which governs publication only. Code open text into themes by hand or with model assistance checked by a person, and say which.

Every publication carries a methodology section: who ran it, population, dates, channels and source mix, funnel, cleaning rules, weighting or "not weighted", full questionnaire, and a plain sentence naming who the sample over-represents. Template, chart captions and rewrite examples for headline claims: [./references/methodology-and-reporting.md](./references/methodology-and-reporting.md).

## Invocation examples

| The user says | You produce |
|---|---|
| "Marketing drafted 30 questions for our first State of X, can you polish them?" | The decision table first; polish only what survives |
| "We want to say 70% of developers prefer our CLI" | The claim ladder; the rung-1 rewrite and what rung 2 would take |
| "Our response rate was 2%, is the survey worthless?" | Why response rate is undefined here and the wrong yardstick; the funnel and the bias sentence |
| "Can we raffle a laptop to boost responses?" | The incentive ranking with compliance cost; the default and the fraud rules |
| "Year two: can we compare to last year?" | Core-module check, channel-mix check, the comparable and non-comparable lists |

## Deliverable

Produce these in order, each validated with the user before the next:

1. **Decision table** - kept questions (original number, question, decision, owner, answer that would change it, `publish` flag, core or rotating), then cut questions with their reason.
2. **Survey plan** - re-ranking block, target and sampled population sentences, claim rung per published question, channel table with source tags, field window, calibration sample or the reason for skipping it.
3. **Questionnaire** - in order, with routing, minutes per section against the budget, core and rotating modules marked.
4. **Pilot plan** - reviewer, interview count, soft-launch slice and checks; add the results and the changes made after the soft launch.
5. **Privacy pack** - legal basis per purpose, notice text, data map (what is stored where, for how long), suppression rule.
6. **Analysis and publication plan** - cleaning rules, subgroup minimum, chart caption template, methodology section draft.

A filled example for a first open-source "State of" survey: [./references/worked-example.md](./references/worked-example.md).

Store the core-module wording, the channel list and source tags, the cleaning rules and last edition's funnel in `devrel-context.md`, or wherever the interview context lives. Next year's edition is a diff against them.
