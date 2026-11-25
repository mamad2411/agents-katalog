---
name: b2b-pmm-orchestrator
description: Route vague B2B product marketing requests to the right PMM skill, sequence multiple skills into intelligent GTM workflows, and keep the agent focused on the smallest useful artifact that moves the business forward.
---

# B2B PMM Orchestrator

## When to use

Use this skill first when the user has a B2B product marketing problem but has not already named the exact downstream skill or workflow.

Use it for requests like:

- "Help me with positioning."
- "We need a launch plan."
- "Turn these customer notes into messaging."
- "Make this sales deck better."
- "What should our GTM story be?"
- "Review this landing page."
- "We need a category POV."
- "Help us build the full GTM system for this product."

This is not a content-generation skill. It is the front door, router, and sequencing layer for the rest of the B2B PMM skill suite.

## Core principle

Do not make artifacts just because the agent can.

Move the GTM system forward.

Before choosing a skill, identify:

- What decision needs to be made?
- What asset needs to ship?
- Who is the audience?
- What evidence exists?
- What is the highest-leverage next artifact?
- What would be overkill right now?

The best PMM work starts with judgment, not output volume.

## Skill routing

Use this table to choose the right downstream skill.

| User situation | Use this skill | Why |
|---|---|---|
| Raw customer calls, notes, sales feedback, interviews, win/loss notes, surveys, support themes, or research | `voice-of-customer-synthesis` | Turns messy customer evidence into PMM inputs: pains, triggers, jobs, alternatives, objections, exact language, proof, and implications. |
| Need sharper positioning, messaging, homepage copy, one-liner, ICP clarity, value proposition, or differentiated narrative | `positioning-messaging-framework` | Makes the core choices: segment, buyer, alternative, differentiated value, proof, positioning statement, and messaging pillars. |
| Need a sales deck, sales story, founder pitch, first-call narrative, or executive/investor narrative | `sales-narrative-deck` | Turns positioning into a story a seller can actually use in conversation. |
| Need a launch plan, launch tier, roadmap GTM strategy, feature announcement plan, or season-of-launch plan | `launch-tier-framework` | Decides how much GTM weight a product moment deserves and how to sequence launch activity. |
| Need customer proof, case study, customer story, sales proof point, reference narrative, or one-pager | `customer-story-engine` | Turns customer wins into credible proof without inventing claims. |
| Need demo flow, sales demo, founder demo, discovery-led demo, or demo narrative | `demo-storyline` | Builds demos around buyer pain, realistic data, discovery, proof, and recap. |
| Need market thesis, thought leadership, category narrative, problem ownership, or strategic POV | `category-point-of-view` | Helps define the problem, shift, category frame, narrative pillars, and content system. |
| Need critique, cleanup, QA, or sharpening of AI-generated marketing work | `ai-pmm-reviewer` | Reviews against customer truth, positioning, proof, voice, plain English, and AI tells. |

## Diagnostic workflow

### 1. Classify the starting point

Identify what the user is bringing to the table:

- Customer evidence: interviews, notes, transcripts, quotes, win/loss, sales feedback
- Product input: roadmap, feature, demo, launch, product brief, technical notes
- Strategy input: ICP, category thesis, positioning, competitive context, market problem
- Draft asset: landing page, deck, blog, launch post, email, campaign, enablement doc
- Vague business problem: pipeline issue, adoption issue, weak story, sales confusion, unclear differentiation

If the starting point is unclear, ask one short clarifying question. Do not send a long intake form.

### 2. Identify the business job

Name what the work needs to accomplish.

Common jobs:

- Make the market understand the problem
- Help buyers see themselves in the pain
- Explain why the status quo is no longer good enough
- Differentiate from a competitor or incumbent workflow
- Create pipeline
- Improve sales conversion
- Support expansion or retention
- Drive feature adoption
- Give sales a clearer story
- Turn proof into repeatable assets
- Make AI-generated work sound less generic

A draft can be well written and still fail the business job.

### 3. Choose the smallest useful output

Default to the smallest artifact that can unlock the next decision or shipment.

Examples:

- If the team is unsure who the buyer is, do not write a launch plan. Build a positioning diagnosis.
- If customer evidence is messy, do not write homepage copy. Synthesize voice of customer first.
- If the product moment is minor, do not create a Tier 1 campaign. Classify the launch tier.
- If the draft is already written, do not rebuild everything. Review it, diagnose gaps, and rewrite only where useful.
- If the story is strategically confused, do not polish words. fix positioning, narrative, or evidence first.

### 4. Route to one skill or sequence multiple skills

Use one skill when the task is narrow and the input is good enough.

Sequence skills when the work depends on earlier strategic choices.

Do not run the full suite unless the user explicitly wants a full GTM system or the situation truly requires it.

## Sequencing recipes

### Customer notes to positioning

Use when the user has customer evidence and needs sharper messaging.

1. `voice-of-customer-synthesis`
2. `positioning-messaging-framework`
3. `ai-pmm-reviewer`

Stop when there is a clear target segment, status quo, differentiated value, proof, and message pillars.

### Customer notes to sales narrative

Use when sales needs a better story and customer evidence exists.

1. `voice-of-customer-synthesis`
2. `positioning-messaging-framework`
3. `sales-narrative-deck`
4. `ai-pmm-reviewer`

Stop when the sales story has a clear pain, market shift, status quo, product value, proof, demo moments, and call-to-action.

### Product launch workflow

Use when the user has a product, feature, roadmap, or release to launch.

1. `launch-tier-framework`
2. `positioning-messaging-framework`
3. `demo-storyline`
4. `customer-story-engine` if proof exists or needs to be packaged
5. `ai-pmm-reviewer`

If customer evidence is weak, run `voice-of-customer-synthesis` before positioning.

Stop when the launch tier, target audience, narrative, channels, proof plan, demo story, and review criteria are clear.

### Category and thought leadership workflow

Use when the user wants to own a problem, shape a market narrative, or create founder/executive POV.

1. `category-point-of-view`
2. `voice-of-customer-synthesis` if research or customer notes exist
3. `positioning-messaging-framework`
4. `sales-narrative-deck` if the POV needs to support selling
5. `ai-pmm-reviewer`

Stop when the market shift, named problem, enemy/status quo, POV, proof, and content pillars are clear.

### Demo-led sales workflow

Use when the product is best understood through a demo or when sales calls are too feature-led.

1. `positioning-messaging-framework`
2. `demo-storyline`
3. `sales-narrative-deck` if the demo needs a broader first-call narrative
4. `ai-pmm-reviewer`

Stop when the demo starts with buyer pain, shows realistic before/after value, uses credible proof, and ends with a clear recap.

### Customer proof workflow

Use when the team needs stronger proof for sales, launch, website, or campaigns.

1. `customer-story-engine`
2. `positioning-messaging-framework` if the story needs to ladder to broader messaging
3. `sales-narrative-deck` or `launch-tier-framework` depending on where the proof will be used
4. `ai-pmm-reviewer`

Stop when the customer story has a credible before state, trigger, product role, outcome, quote/proof, and sales usage.

### Review and rescue workflow

Use when the user has an existing asset that feels generic, weak, or too AI-written.

1. `ai-pmm-reviewer`
2. Route to the domain skill that matches the problem:
   - Positioning problem: `positioning-messaging-framework`
   - Launch problem: `launch-tier-framework`
   - Sales story problem: `sales-narrative-deck`
   - Demo problem: `demo-storyline`
   - Proof problem: `customer-story-engine`
   - Category problem: `category-point-of-view`
   - Evidence problem: `voice-of-customer-synthesis`
3. Return to `ai-pmm-reviewer` for final QA.

Stop when strategic gaps are fixed, not when the wording merely sounds smoother.

## Operating modes

### Quick fix

Use when the user wants one immediate improvement.

- Pick one downstream skill.
- Produce one artifact.
- State assumptions and confidence.
- Do not expand scope unless the current artifact would be misleading without upstream work.

### Deep work

Use when the user wants a meaningful GTM asset and has enough context.

- Sequence two to four skills.
- Build from evidence to strategy to asset.
- Mark which parts are supported by customer truth and which are assumptions.
- End with what should be validated next.

### Full GTM system

Use when the user explicitly wants to build the whole system for a product, market, or launch.

A full sequence may include:

1. `voice-of-customer-synthesis`
2. `category-point-of-view`
3. `positioning-messaging-framework`
4. `launch-tier-framework`
5. `sales-narrative-deck`
6. `demo-storyline`
7. `customer-story-engine`
8. `ai-pmm-reviewer`

Do not dump all artifacts at once. Build them in dependency order and verify each major strategic choice before moving on.

### Review mode

Use when there is already a draft.

- Start with `ai-pmm-reviewer`.
- Diagnose whether the problem is strategy, evidence, messaging, voice, or structure.
- Use the relevant domain skill only if needed.
- Rewrite after diagnosis, not before.

## Minimum intake questions

Ask only what blocks progress. Prefer making reasonable assumptions and labeling them.

Useful questions:

1. What are we trying to ship or decide?
2. Who is the audience: buyer, user, executive, seller, investor, customer, or internal team?
3. What input do we have: customer evidence, product notes, market thesis, roadmap, or a draft?
4. What is the business goal: pipeline, conversion, adoption, retention, expansion, awareness, or sales enablement?
5. What must be true for this work to be considered useful?

If the user gives enough context, proceed without asking.

## Output format

When orchestrating, respond with:

1. Diagnosis
   - What kind of PMM problem this is
   - What is known vs assumed

2. Recommended path
   - The skill or sequence to use
   - Why that order makes sense

3. First artifact
   - The smallest useful artifact to create now
   - What it should include

4. Inputs needed
   - Only the missing inputs that would materially improve quality

5. Stop condition
   - How we know this workflow is complete enough for the current goal

When actually executing a downstream skill, follow that skill's output format.

## Quality bar

Good orchestration should:

- Reduce ambiguity, not add process
- Push the agent toward customer truth
- Prevent premature copywriting
- Avoid generic GTM templates
- Choose one clear next move when possible
- Sequence work only when dependencies matter
- Call out weak evidence directly
- Separate strategy problems from writing problems
- Protect the user from overbuilding

## Common pitfalls

1. Running every skill by default.
   The full suite is for full GTM system work. Most requests need one to three skills.

2. Treating weak strategy as a copywriting problem.
   If the audience, alternative, value, or proof is unclear, route to positioning or VOC before rewriting.

3. Asking a giant intake questionnaire.
   Ask only what blocks progress. PMM judgment includes knowing when to move with imperfect inputs.

4. Starting with launch planning before positioning.
   A launch plan without a clear audience, pain, value, and proof becomes a channel checklist.

5. Starting with category POV when the problem is actually tactical.
   Not every product needs a category narrative. Sometimes the right answer is a clearer demo, sharper launch tier, or better proof.

6. Reviewing against taste instead of evidence.
   The question is not whether the copy sounds nice. It is whether it is specific, believable, differentiated, and useful to the intended audience.

7. Producing polished fiction.
   Do not invent customer quotes, metrics, proof, competitors, or market evidence. Mark missing evidence as a gap.

## Verification checklist

Before finishing, check:

- [ ] Did you identify the PMM problem type?
- [ ] Did you choose the smallest useful next artifact?
- [ ] Did you route to the right skill or sequence?
- [ ] Did you avoid unnecessary artifacts?
- [ ] Did you distinguish known facts from assumptions?
- [ ] Did you preserve customer truth and avoid invented proof?
- [ ] Did you define a clear stop condition?
