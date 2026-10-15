---
name: cloudinary-get-started
description: >-
  Guide Cloudinary onboarding for new or existing projects through a gated,
  stack-detected setup flow. Use when the user asks to get started with
  Cloudinary, configure Cloudinary in a repo, set up Cloudinary in an IDE or
  agent environment, validate an existing integration, configure MCP or skills,
  handle credentials safely, choose the right SDK, validate upload presets,
  test delivery URLs, document environment setup, or identify next steps.
  Detect the project stack first; never assume React, Python, Node.js, or any
  other SDK unless detected or explicitly chosen.
---

# Cloudinary Getting Started

## When to use this skill

Use this skill when helping a user set up Cloudinary in a new or existing project, or when validating an existing Cloudinary integration.

This skill is especially useful when the user asks to:

- Get started with Cloudinary or CLD
- Configure Cloudinary in a codebase
- Set up Cloudinary in an IDE or agent environment
- Install or configure the right Cloudinary SDK for the detected stack
- Set up Cloudinary MCP servers or related AI tooling
- Handle credentials, environment variables, or .env files safely
- Validate upload presets or upload behavior
- Test generated delivery URLs
- Measure, inspect, or compare delivered assets
- Document the Cloudinary setup for the project
- Decide what to do next after the initial integration

## Operating principle

Run Cloudinary onboarding as a guarded, SDK-agnostic stage flow. Detect the project stack first, then use the official Cloudinary SDK, framework docs, or Cloudinary docs that match that stack. Full SDK rule: see `references/global-rules.md`.

Keep user-facing replies short, practical, and action-oriented. Do not narrate investigation steps. Recap completed work before asking the next question.

Follow this hard order whenever work remains:

1. Silent explore — then present the setup checklist
2. Stage 1: AI tooling
3. Stage 2: repo/framework check (ends with confirmation gate)
4. Stage 3: detected-stack SDK + env file setup
5. Stage 4: credentials (starts with D1 account check)
6. Stage 5: preset + validation artifacts + **Done gate** (REQUIRED — do not skip)
7. After the user replies `Done`: What's next (includes MCP activation)

**CRITICAL:** Stage 5 MUST end with the Done gate before showing What's next. The Done gate appears in `references/stage-5-validation.md` (lines 113-116). Do not show What's next until the user explicitly replies "Done".

At the end of every stage, use the stage completion format defined below.

Skip redundant work when silent explore, files, MCP behavior, or the user proves a stage is already satisfied. Do not replay or pseudo-validate work that was never missing. Even when skipping, still end with the Done gate, and always provide What's next after `Done`.

## Stage completion format

Use this exact format at the end of every stage. No exceptions.

```
**Stage X complete:**

- [one bullet per concrete thing done: files created, packages installed, config written, etc.]

**Here's the plan:**
- [x] Stage 1: AI tooling (MCP servers + skills)
- [ ] Stage 2: Framework detection
- [ ] Stage 3: SDK setup + environment file
- [ ] Stage 4: Credentials
- [ ] Stage 5: Verify setup automatically

**Stage X+1 — [stage name]**
[One or two sentences describing what will happen in the next stage.]

---
**Reply to continue setup:**

[Concrete gate question]

**Suggested reply:** [adapted cues]

---
```

**CRITICAL:** After the blocking prompt footer, you MUST STOP and wait for the user's response before proceeding to the next stage. Do not continue, do not start Stage X+1, do not run Stage X+1 setup code until the user answers.

Rules:
- Mark every completed stage with `[x]` in the checklist; leave upcoming stages as `[ ]`.
- The "Stage X complete" bullets are concrete and specific — name actual files, packages, and actions, not categories.
- The "Stage X+1" intro previews the next stage scope before the blocking prompt footer.
- **Exception for the Stage 4 → Stage 5 transition:** replace the one or two sentence preview with the full validation plan as a bulleted list, drawn from the "What this stage does" section of `references/stage-5-validation.md`. This gives the user a clear picture of everything validation covers before they confirm.
- The blocking prompt footer is always last (per `references/global-rules.md`).
- **DO NOT execute the next stage until the user confirms.** Wait for their explicit answer to the gate question.

**Before silent explore:** output a single friendly intro sentence such as "Sure, I'll help you set up your app with Cloudinary today. I'll start by silently exploring the project and reading the reference files." before doing any file inspection. Do not narrate the exploration itself.

**Before Stage 1:** immediately after silent explore, output the checklist alone (no "Stage X complete" header yet) with any already-complete stages pre-checked, then proceed into Stage 1.

## Internal setup state

Track internally: `stage`, `repo_shape`, `stack`, `react_status`, `delivery_lane`, `skills_status`, `mcp_config_status`, `credential_status`, and `stage_5_status`.

Update state only from actual repo checks, tool results, MCP behavior, or user confirmation. Do not infer completion from expected behavior or prior plans.

## Gate definitions

Use these gates as the single source of truth for stage progression.

### After Stage 1 — proceed to Stage 2

Both are true:

- Required Cloudinary skills are installed in the current IDE or agent environment's canonical skills location.
- Both Cloudinary MCP server configurations are present for `cloudinary-asset-mgmt` and `cloudinary-env-config`.

### After Stage 2 — proceed to Stage 3

Both are true:

- Stack and delivery lane are confirmed with the user.
- User explicitly confirms readiness to proceed to Stage 3 (blocking prompt footer required at end of Stage 2).

### After Stage 3 — proceed to Stage 4

Stage 3 complete:

- SDK installed and configured.
- `.env.example` created with placeholder credentials.
- `.gitignore` updated to exclude `.env`.

### Before Stage 4 — D1 account check is mandatory

**CRITICAL:** Stage 4 MUST begin with D1 (Cloudinary account check) before requesting any credentials. Never skip D1 or ask for credentials before confirming the user has an account.

**Stage 3 gate question:** The blocking prompt footer at the end of Stage 3 must ask only whether the user is ready to continue — NOT whether they have a Cloudinary account. The account check belongs to Stage 4 D1. Use this exact gate question and answer cues:

```
---
**Reply to continue setup:**

Ready to fill in your Cloudinary credentials?

**Suggested reply:** Yes, let's continue

---
```

### After Stage 4 D1+D2 — proceed to Stage 5

All are true:

- D1 complete: user has confirmed they have a Cloudinary account.
- D2 complete: user has retrieved cloud name, API key, and API secret from Cloudinary Console and filled `.env` with real credentials.

### Before Stage 5 — SDK and credentials fully ready

All are true:

- The workspace-root `.env` file exists with real credentials filled in.
- The user confirms `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET` are saved.
- Any required client-side env placeholders are handled for the detected framework.

Never read `.env` contents to verify this gate.

## Reference files

Read the appropriate reference file when entering each stage or when detailed rules are needed. All files are in `references/` relative to this skill.

| File | When to read |
| --- | --- |
| `references/global-rules.md` | Before any stage — covers SDK rule, security rules, interaction rules, and the blocking prompt footer |
| `references/silent-explore.md` | Before classification — covers what to inspect, how to classify, and delivery lane rules |
| `references/stage-1-ai-tooling.md` | When entering Stage 1 — covers MCP server definitions, IDE config patterns, permission gate, and approval steps |
| `references/stage-2-framework-check.md` | When entering Stage 2 — covers repo shape branching and React detection |
| `references/stage-3-sdk-setup.md` | When entering Stage 3 — covers SDK install, env file setup, and Stage 4 gate enforcement |
| `references/stage-4-credentials.md` | When entering Stage 4 — covers D1/D2 credential retrieval and `.env` setup |
| `references/stage-5-validation.md` | When entering Stage 5 — covers preset creation, artifact requirements, and validation response format |
| `references/after-done.md` | After the user replies `Done` — covers next-step bullets (VS Code ext, run app, activate MCP, build with Cloudinary) and cleanup guidance |
