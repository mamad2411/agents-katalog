---
name: skill-creator-pro
description: Design, build, validate, and publish production-ready Codex skills. Use when Codex needs to turn a repeated workflow or new capability into a new skill, organize its scripts/references/assets, forward-test it before first release, or package it as an installable repository.
metadata:
  short-description: Engineer and release a new Codex skill
---

<!-- Modified from OpenAI's Skill Creator in 2026; see the repository NOTICE. -->

# Skill Creator Pro

Engineer skills that make an agent follow a predictable process. Predictability means the same
decision discipline and verification path across runs, not identical output. Treat a skill as
production-ready only when its invocation, gates, resources, and verification evidence are explicit.

Treat the active Codex harness and its validator as the compatibility authority. Borrow design
ideas from other skill systems only after translating them to Codex-native fields and tools.

## Core standard

Every line must earn its context cost by changing behavior. Prefer:

- a checkable completion criterion over an adjective such as "careful"
- one strong, established term over repeated explanations
- a deterministic script over repeatedly generated fragile code
- a conditional context pointer over always-loaded branch-specific detail
- the positive target behavior over a prohibition
- one source of truth over restating a rule in several sections

For a new skill or a substantial behavioral rewrite, read
[references/predictable-skill-design.md](references/predictable-skill-design.md) before Step 2.
For a narrow metadata, typo, or resource update, skip that reference.

## Process

Follow the steps in order. Skip a step only when it is irrelevant to the requested change, and
state the reason in the final handoff.

### 1. Establish the behavior contract

Start with concrete runs, not prose. Derive examples from the user's request and local evidence;
ask only for decisions that cannot be discovered safely.

Capture working notes for:

- **Outcome**: what capability or repeatable discipline the skill adds
- **Trigger branches**: distinct situations that should load the skill
- **Near misses**: similar requests that should not load it
- **Inputs and state**: files, tools, environment, prior artifacts, or user decisions it consumes
- **Outputs and side effects**: files, messages, commands, or external mutations it may produce
- **Success evidence**: what the agent can observe to prove the run worked
- **Failure behavior**: where the run must stop, fall back, or ask for authority

If the request starts from an existing skill and asks why it misfires, what quality problems it has,
or how to improve it in place, route the task to the existing-skill review workflow (`Skill Review`).
Use this skill on existing material only when the user is deliberately forking or rebuilding it as a
new skill identity; inspect the upstream skill as source evidence for the new behavior contract.

**Done when:** every distinct trigger branch has at least one concrete example, and success or
failure is observable for each branch.

### 2. Choose invocation and boundaries

Decide whether Codex should load the skill implicitly:

- **Implicit invocation** fits reusable disciplines Codex must discover from ordinary requests, or
  skills that other workflows need to reach.
- **Explicit-only invocation** fits workflows that require deliberate user control or would trigger
  too broadly. Set `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

Codex still requires `name` and `description` in `SKILL.md` for both modes. Use the product-native
policy field; fields such as `disable-model-invocation` belong to other harnesses.

Keep one skill when its branches share the same outcome, state, and verification path. Split when a
branch has an independent trigger and behavior contract, or when isolating a long phase prevents
the agent from rushing the current phase. Account for both costs: more implicit skills consume
model context; more explicit-only skills require the user to remember them. A small router can make
an explicit skill family discoverable to the user.

For a skill collection, assign each responsibility once:

- reusable disciplines and vocabulary belong in small implicit skills
- deliberate end-to-end entry points belong in explicit orchestrators
- cross-session facts and decisions belong in durable artifacts with narrow purposes
- provider-specific commands belong behind adapters or conditional references
- human discoverability belongs in a router that names flows and neighboring skills

When an existing skill moves or changes role, inspect and update its callers, router, metadata, and
documentation. A correct leaf with a stale route is still a broken system.

**Done when:** invocation mode is explicit, each proposed skill has one coherent contract, and every
split has a concrete behavioral reason. In a collection, every shared behavior, artifact, adapter,
and route has one owner.

### 3. Design the information hierarchy

Classify proposed content before writing:

1. **Steps in `SKILL.md`**: actions every relevant run must perform, in order.
2. **Reference in `SKILL.md`**: compact rules every branch needs while acting.
3. **Conditional references**: detailed or branch-specific knowledge loaded through a precise
   pointer that says when and why to read it.
4. **Scripts**: deterministic or repeatedly reconstructed operations.
5. **Assets**: templates, media, or boilerplate copied into outputs rather than read as guidance.

Inline what every branch needs. Move branch-only material behind a direct pointer from `SKILL.md`.
Keep references one level deep and co-locate each concept's definition, rules, and caveats. Give a
reference over 100 lines a table of contents. For a reference over roughly 10,000 words, include
search terms or section anchors in its pointer.

Create only resource directories that carry real content. Keep a fact or rule in exactly one place.

For a large skill with many conditional modules or optional dependencies, consider a machine-readable
capability manifest. Each module should declare its status, triggers, references, dependencies,
fallback, and verifier. Add a deterministic manifest validator. Use this only when it makes routing
and release state more checkable than prose; a small skill needs no manifest.

**Done when:** every planned item has one home, every conditional file has a firing condition, and
the main workflow remains legible without reading an irrelevant branch.

### 4. Encode the control flow

Write the workflow around observable gates:

- Validate cheap preconditions before expensive work or parallel delegation.
- Give each phase a fixed source-discovery order when several inputs are possible.
- End every consequential step with a checkable completion criterion. Make it exhaustive where
  partial coverage is a common failure, such as "every modified file accounted for."
- State the fallback or stop condition where evidence, access, or authority is missing.
- Separate independent evaluation axes. If one axis can bias another, run them in isolated contexts
  and aggregate without silently reranking them.
- Preserve user checkpoints only for genuine decisions or consequential side effects; gather facts
  from the environment directly.
- Bound delegated prompts with the exact inputs, evidence standard, and output contract they need.
- Audit negative space: when source authority, mutation scope, evidence, or stopping behavior is
  unstated, decide whether that freedom is intentional or an unsafe delegation to model defaults.

For a stateful or high-risk workflow, keep progress, evidence outcome, execution scope, and claim
eligibility as separate state dimensions. Bind consequential authorization to the relevant source
revision and material parameters; a changed source or envelope makes the authorization stale.
Require an explicit user decision for approval, leaving silence as a pending gate. Make preflight
validate the plan without performing its live side effects.

For a skill that can both review and modify an artifact, route those as distinct modes. Keep review
read-only by default. Before modification, define an immutable ledger of facts, identifiers,
citations, numbers, or other invariants, then verify the output against it. Preserve stable finding
IDs and exact status tokens across rechecks when downstream artifacts depend on them.

Use a compact leading term when an established concept already carries the intended behavior, such
as "red-green-refactor," "fail fast," or "single source of truth." Define a coined term once before
using it as shorthand.

Phrase the desired action directly. Use hard prohibitions only for genuine guardrails, and pair each
with the action to take instead.

**Done when:** another agent can follow every branch without inventing the order, stopping rule,
authority, or evidence standard.

### 5. Build the skill

For a new skill, initialize it with:

```bash
scripts/init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets] [--examples] [--implicit-invocation true|false]
```

Use lowercase hyphen-case, under 64 characters, and name the folder exactly after the skill.
Prefer a short verb-led name; add a tool namespace when it materially improves triggering.

Implement reusable resources before finalizing `SKILL.md`. Test each added script by running it;
for a family of mechanically similar scripts, test a representative sample. Remove unused example
files and empty resource directories.

Write `SKILL.md` in imperative form:

- `name`: the exact skill name
- `description`: what the skill does plus one trigger for each genuine branch; front-load the action
- body: execution guidance and resource pointers, with invocation triggers kept in the description

Before generating or refreshing `agents/openai.yaml`, read
[references/openai_yaml.md](references/openai_yaml.md) for its field constraints:

```bash
scripts/generate_openai_yaml.py <skill-folder> \
  --interface display_name="..." \
  --interface short_description="..." \
  --interface default_prompt="Use $skill-name to ..." \
  [--implicit-invocation true|false]
```

Preserve unrelated user changes in the working repository. Keep only files that directly support
agent execution; process notes and user documentation belong outside the skill folder.

**Done when:** the folder contains the smallest complete implementation of the behavior contract,
all referenced resources exist, and UI metadata matches the finished skill.

### 6. Prune sentence by sentence

Run these passes separately:

1. **Behavior pass**: delete sentences that would not change the capable model's default behavior.
2. **Duplication pass**: choose one authoritative home for each meaning; replace restatements with a
   pointer or a compact term.
3. **Relevance pass**: remove stale rationale, obsolete branches, scaffolding, and historical notes.
4. **Hierarchy pass**: move live but conditional detail to a referenced file.
5. **Language pass**: replace vague adjectives with evidence or a completion criterion; rewrite
   avoidable negations as positive instructions.
6. **Negative-space pass**: identify consequential decisions the skill leaves unstated; encode the
   ones that must stay stable and leave the rest as deliberate degrees of freedom.

Aim for a `SKILL.md` under 500 lines. Length is a diagnostic, not permission to compress live rules
into ambiguity.

**Done when:** each remaining sentence changes behavior, supplies required knowledge, establishes a
gate, or points to conditional material.

### 7. Validate structure and mechanics

Run:

```bash
scripts/quick_validate.py <skill-folder>
scripts/quality_lint.py <skill-folder>
```

Fix structural errors. Review lint findings as prompts for judgment; hard guardrails and reference-
only skills can legitimately trigger heuristic warnings.

Also run every command or script the skill tells a future agent to run, using a safe fixture or
dry-run when live effects would require additional authority.

Test every claimed operating system or state the supported runtime boundary explicitly. Use native
path conversion APIs such as Node's `fileURLToPath(import.meta.url)`, and use the active interpreter
such as Python's `sys.executable` instead of assuming `python3` or `bash` exists on Windows.

**Done when:** structural validation passes, linked local resources resolve, scripts have been
executed successfully, and every lint warning is fixed or consciously justified.

### 8. Forward-test behavior

Scale testing to risk. A narrow wording change may need only targeted inspection. A new, complex,
or previously unreliable skill needs realistic forward tests covering:

- a request that should trigger it
- a near miss that should not trigger it
- the common happy path
- at least one materially different branch
- a missing-input or blocked-permission path
- any pre-release regression already observed during the current build

When independent agents or fresh threads are available, give them the skill and raw task artifacts
with only task-local context. Keep the expected answer, suspected flaw, and intended fix out of the
prompt unless the test explicitly measures those facts. Treat their outputs, diffs, logs, and traces
as evidence. If a test only passes after coaching, improve the skill or the fixture and rerun it.

Ask before a forward test that could take substantial time, require new approval, or mutate a live
system.

**Done when:** representative runs follow the intended process without hidden coaching, failures
stop at the right gate, and the observed artifacts satisfy the behavior contract.

### 9. Package and release when requested

When the user asks to share, package, install, or publish the skill, read
[references/release-engineering.md](references/release-engineering.md) before creating a remote
repository or release. Treat identity, attribution, repository boundaries, CI, installation, and
remote metadata as one release contract. Run its gates against the published artifact, and preserve
the upstream skill when a renamed derivative must coexist with a bundled or system skill.

**Done when:** the repository is clean, attribution and version state are explicit, remote CI passes,
remote installation succeeds, and users can distinguish the skill from upstream and neighboring skills.

### 10. Hand off the result

Report the behavior that changed, the files created or updated, validation commands and outcomes,
and any residual risk. Distinguish structural validation from behavioral evidence.

**Done when:** the user can locate the skill, understand what is now more predictable, and see what
was actually tested.

## Quality model

Use these failure modes while authoring the current skill:

- **Misfire**: description branches are missing, duplicated, or too broad.
- **Premature completion**: a step has a vague finish line and later steps pull attention forward.
- **Thin legwork**: the completion criterion does not demand enough evidence or coverage.
- **Context-pointer miss**: required material is hidden behind a weakly worded condition.
- **Interference**: independent review or decision axes share context and bias one another.
- **No-op**: an instruction merely repeats capable-model defaults.
- **Duplication**: one meaning has several authorities.
- **Sediment**: stale content survives because additions were easier than deletion.
- **Sprawl**: live content is too large for the main workflow to stay legible.
- **Negation rebound**: the forbidden behavior is more prominent than the desired behavior.
- **Negative-space drift**: an unstated consequential decision silently falls back to model priors.
- **Release drift**: the runtime folder works locally while repository identity, documentation,
  attribution, CI, remote installation, or the installed copy no longer matches it.

Fix the earliest causal failure. For example, sharpen a completion criterion before splitting a
workflow, and strengthen a context pointer before inlining a large reference.
