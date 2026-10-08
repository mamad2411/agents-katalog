---
description: "Distill an article, blog post, video transcript, talk, or tutorial into a reusable skill when the user explicitly asks to turn it into a skill/command, save the method, or make it reusable. Do not trigger for method analysis alone."
---

# /content-to-skill

Distill source content (articles, video transcripts, talks, tutorials) into a reusable skill.

Do not summarize the content. Extract the repeatable method inside it, strip the noise, and produce instructions another agent can execute without ever seeing the source.

## Inputs

Pasted articles, blog posts, video/podcast transcripts, talk notes, or tutorials. A file path when repository access is available. If the input is a URL, fetch it only when the user asked for URL reading and the fetch succeeds; otherwise ask for the content or stop with the fetch error.

Expect noisy input: intros, sponsor reads, anecdotes, audience banter, filler speech, and repetition are normal in transcripts. Treat them as raw ore, not as structure to preserve.

## Step 0 — Triage: is there a skill here?

Not all content contains a reusable method. Before building anything, classify the content:

* **Method content** — teaches a procedure, technique, framework, or decision process that applies to future inputs. → Proceed.
* **Multiple methods** — contains several independent techniques. → Pick the one with the clearest trigger and most operational detail as the core skill; list the others under **Open decisions** as candidates for separate skills. Split into separate skills only when the user asks, or when the methods have different triggers, inputs, outputs, or maintenance cycles and share no workflow.
* **No method** — news, opinion, narrative, product reviews, motivation, descriptive background knowledge, a one-off solution with no generalizable pattern, or advice too generic to change model behavior. → Say so plainly, state what the content would support instead (e.g., a reference note, not a skill), and stop. Do not force a skill out of descriptive content.

State the classification in one line before the skill design.

## Step 1 — Extract the method from the noise

Discard: intros, sponsor segments, personal stories, credibility-building, repetition, hedging, and anything that does not change what the executing model would do.

Keep: steps, decision criteria, thresholds, tool names, formats, warnings drawn from the author's failures, and worked examples that clarify a boundary.

Classify useful material into these categories as you extract:

* **Capability** — what the model should become able to do
* **Inputs** — what information or artifacts the skill receives
* **Procedure** — what actions it performs
* **Decision rules** — how it chooses between alternatives
* **Constraints** — what must remain true
* **Failure modes** — what commonly goes wrong
* **Validation** — how to determine whether the result is acceptable
* **Output** — what usable artifact or answer it produces

Convert as you extract:

* Third-person narration → imperative instructions ("the author recommends checking X first" → "Check X first").
* Source-specific details (the author's stack, dates, company names, specific numbers from their case) → generalized parameters, unless the specific value is the method's point.

Then classify each extracted rule and apply the matching treatment:

* A **general rule** — applies broadly → write as a direct imperative instruction
* A **context-specific rule** — applies only under stated conditions → keep the condition attached ("when X, do Y")
* An **illustrative example** — demonstrates but does not prescribe → extract the general rule it illustrates; keep the example itself only if it clarifies a boundary
* An **unsupported opinion** — no verifiable reasoning behind it → phrase as a default or heuristic ("prefer X; adjust when Y"), never as an absolute
* A **possible exception** — boundary case that constrains a rule → attach it to the rule as a condition, or encode it as a guardrail in Step 5

When the source presents competing approaches or is uncertain, preserve that uncertainty as selection criteria rather than pretending there is one universal answer.

## Step 2 — Define trigger and scope

Write frontmatter where the `description` carries all triggering information: what the skill does AND when to activate.

Models under-trigger skills, so make the description slightly pushy: enumerate concrete trigger phrases and near-miss wordings a real user would type, including indirect ones. Balance with explicit exclusions ("Do NOT use for…") when the method's domain borders common tasks.

Avoid descriptions that only repeat the skill name, describe implementation instead of user intent, or depend on the source article's context.

## Step 3 — Write the operational procedure

Convert the extracted method into an ordered procedure. For each important step, specify where relevant:

* What the model should inspect
* What decision it should make
* What action it should take
* What criteria or evidence should guide the decision
* What to do when information is incomplete

Use explicit rules where mistakes affect correctness. Leave judgment where rigid instructions would reduce quality. Preserve the author's domain reasoning when it changes execution; drop it when it is commentary.

## Step 4 — Define the output contract

Specify the artifact the skill must produce: required sections, ordering, formatting, level of detail, and what must NOT be included. Describe the usable artifact, not the model's reasoning process.

## Step 5 — Encode failure modes

Add concise guardrails for the failures most likely for THIS method — especially mistakes the author explicitly warns about, since those are field-tested. Standard traps to check:

* Applying the method to inputs it was not designed for (scope creep into adjacent tasks)
* Producing a summary or description when the method requires a transformation or artifact

These guardrails go into the produced SKILL.md and must make sense to its future user, who will never see the source article. Distillation-quality checks (faithfulness to the source) belong in Step 7, not here.

Do not add speculative warnings unlikely to affect real use. Do not turn every observation into a rule.

## Step 6 — Progressive disclosure

Keep the core SKILL.md focused: trigger, scope, procedure, guardrails, output contract, definition of done. Target well under 500 lines.

Move substantial material into supporting files with clear pointers on when to read them:

* Long worked examples from the article → `references/examples.md`
* Domain background needed only sometimes → `references/domain-notes.md`
* Fixed output structures → `templates/`
* Deterministic repeatable steps → `scripts/`

Every supporting file must have:

* A specific purpose
* An explicit condition for when to load it
* No unnecessary duplication with `SKILL.md`

Do not create empty directories or placeholder files merely to make the skill appear complete.

## Step 7 — Validate before presenting

Check that:

* The skill is understandable with the source article forgotten — no "as the video explains", no undefined jargon from the source
* The description accurately matches the skill's actual behavior
* Examples do not accidentally narrow the general rule
* The article's examples have not been copied in as if they were requirements
* No single case from the author has become a universal rule, and no steps were invented beyond what the source supports
* No instruction conflicts with another section
* Single-source claims are phrased as defaults, not laws

## Output format

### Triage

* 1–3 sentences: method content / multiple methods (which one chosen and why) /
  no method (stop here). Note major material intentionally excluded.

### Skill design

* The repeatable problem, the intended trigger, the expected output, and any core/supporting split. 3–5 lines. Do not summarize the article.

Choose one output mode before writing:

* **Draft mode** — provide the design and focused outlines when placement or scope still needs a decision.
* **Save-ready mode** — provide complete contents for every file needed to install the skill; do not provide outlines as if they were ready to save.

### SKILL.md

* Complete, ready to save, in a fenced Markdown block: frontmatter, purpose, inputs, procedure, output contract, guardrails, definition of done. Omit sections that do not earn their tokens.

### Supporting files

* Only when warranted: full contents or focused outlines. Do not repeat SKILL.md material.

### Test prompts

* 2–3 realistic prompts a user would actually type that should trigger this skill, plus 1 near-miss prompt that should NOT trigger it. These validate the description's trigger quality.

### Open decisions

* Only decisions that materially depend on the user's environment or scope — including other methods in the article worth their own skill. Omit the section if empty.

### Recommendation

End with one of:

* `Use as a standalone skill`
* `Use core skill + supporting resources`
* `Split into multiple skills`
* `Not skill material — keep as reference notes`

## Writing rules

Prefer concise, imperative instructions. Write for execution, not explanation.

Do not preserve the author's name, dates, or organizations unless necessary to the method.

Do not create an "expert persona" as a substitute for procedure.

Do not add motivational language or best-practice commentary unless it changes behavior.

Keep examples minimal and contrastive — include them mainly to clarify a boundary, trigger, or failure mode.

Do not require access to the original source after the skill is created.

## Definition of done

The distillation is complete when:

* The source's reusable capability has been clearly identified
* Narrative and repetitive material has been removed
* The skill has a recognizable trigger and bounded scope
* The procedure contains executable actions with usable decision criteria
* Source-derived mistakes and exceptions have become guardrails
* The output contract produces a directly usable result
* Supporting files, if any, have explicit loading conditions
* The skill works without the original source
* Positive and near-miss trigger tests are provided
