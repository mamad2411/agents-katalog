---
name: demo-video-playbook
description: Plan, script, stage, or review evidence-led software demo videos. Use for new products, feature launches or upgrades, hackathon projects, AI or agent workflows, CLI or API tools, technical walkthroughs, onboarding or help videos, sales demos, website loops, changelogs, and demo series when the agent must decide what to show, say, prove, cut, record, or ask viewers to do next. Not for brand films, testimonials, or videos that never demonstrate working software.
---

# Demo Video Playbook

A software demo is a claim made visible. Build it around the smallest honest proof that matters to the intended viewer.

## Route the request

Choose by the state of the work first:

- **New demo:** run the main flow.
- **Existing script, storyboard, rough cut, or export:** use the review path.
- **Several audiences, jobs, or independent capabilities:** plan a demo system or series before scripting one video.
- **Only a recording or editing question:** read [references/capture.md](references/capture.md) and keep the answer scoped to that operation.

Then choose the intent branch in [references/modes.md](references/modes.md). New product launches, feature updates, website loops, sales demos, tutorials, AI workflows, developer tools, changelogs, and hackathon submissions share the same proof contract, but they do not share the same opening, pace, evidence, or CTA.

## Main flow: frame -> verify -> prove -> cut -> stage

### 1. Frame the assignment

Resolve the viewer, decision, real-world scenario, destination, availability, runtime constraint, and next action. Infer from the project and publishing context when the answer is already present. Ask only for a choice that would materially change the demo.

Write one demo thesis:

```text
For [viewer], show [job] moving from [before] to [after],
prove it with [inspectable detail], then ask them to [next step].
```

**Done when:** the demo has one primary viewer, job, result, and CTA.

### 2. Build the truth map

Inspect the materials in scope: running software, README, routes, components, commands, tests, feature flags, release notes, sample data, API responses, logs, screenshots, and approved messaging. Classify each planned claim as:

- **verified:** supported by working behavior or authoritative project evidence
- **conditional:** true only for a stated build, plan, role, dataset, or environment
- **excluded:** unsupported, unreliable, private, unreleased, or outside this demo

Do not turn roadmap language, a mockup, or marketing copy into shipped behavior. Show prototypes, staged data, simulated screens, edited waits, and best-case AI runs for what they are.

**Done when:** every spoken or written claim has a source, condition, or explicit exclusion.

### 3. Choose the proof

Pick the evidence pattern that makes the value inspectable. Read [references/proof-patterns.md](references/proof-patterns.md) when the value is invisible, technical, asynchronous, distributed across tools, or easy to fake.

The **proof spine** is the logical cause-and-effect chain:

```text
starting state -> meaningful action -> product response -> outcome -> verification
```

The edit may reveal the outcome first, but the viewer must still be able to reconstruct the chain. Keep one primary spine. Put secondary capabilities in a cut list or follow-up video.

**Done when:** removing any remaining beat would break the claim, causality, or proof.

### 4. Design the explanation

Choose a hook that begins the proof: show the task, result, contrast, constraint, or objection. Do not add a slogan that delays the software.

Write a shot contract with:

- exact frame and starting state
- user or system action
- narration or on-screen copy
- state change and proof detail
- edit treatment, including disclosed cuts or speed changes
- hold requirement and reset steps

Use the product's real nouns. Narration should explain meaning and transitions, not read the interface aloud. Give the proof longer than the setup. Use [references/workflow.md](references/workflow.md) for difficult selection and [references/templates.md](references/templates.md) for the output shape.

**Done when:** every important line arrives with matching evidence, and the muted cut still preserves the task, change, result, and next step.

### 5. Stage a repeatable take

Prepare a safe demo environment, believable data, stable starting state, reset path, readable application scale, deliberate cursor path, clean audio, and truthful fallback for unreliable steps. Read [references/capture.md](references/capture.md) before recording or directing an edit.

**Done when:** the complete proof spine succeeds twice from the written reset steps.

### 6. Run the clarity gate

Review the asset at its real player size:

1. from a cold start
2. muted
3. with sound
4. at the destination's smallest likely size

Use [references/review-rubric.md](references/review-rubric.md). Repair promise, causality, proof, trust, and readability before polish.

**Done when:** a new viewer can name the job, result, proof detail, and next step without extra explanation.

## Review path

For an existing asset:

1. Establish the intended viewer, promise, destination, and CTA.
2. Reconstruct the proof spine from what is actually present.
3. Find the first frame where the promise, action, result, or verification becomes uncertain.
4. Give the earliest applicable verdict: **replan**, **re-record**, **recut**, or **ready**.
5. Cite timestamps or exact script fragments and recommend the smallest repair that restores the proof.
6. Separate blocking repairs from optional polish.

Do not reward production value for hiding a broken proof spine.

## Boundaries

- Planning does not authorize recording, uploading, publishing, or contacting anyone.
- Preserve private data, credentials, internal URLs, notifications, local paths, and unreleased information outside the frame.
- Keep a single source of truth for each claim. Surface conflicts instead of smoothing them over.
- Show generated output with enough input, result, and human or system control to judge it.
- Verify current platform specifications from an official source only when exact export or upload settings matter.
