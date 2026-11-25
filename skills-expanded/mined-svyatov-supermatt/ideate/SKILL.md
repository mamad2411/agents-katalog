---
name: ideate
description: Generate grounded ideas for what to build next, critique every one, and rank the survivors in a Markdown file.
disable-model-invocation: true
argument-hint: "[focus area or constraint]"
license: MIT
---

# Ideate

Answer one question: **which ideas are worth building?** Generate many, critique all of them, and explain only the **survivors**. Picking one and shaping it is the job of `/grill-with-docs`; this skill ends when the user holds a ranked list.

Every idea carries a **basis**, the evidence a reader can check. An idea without one is slop, however plausible it sounds. Tag each basis:

- `direct:` a file, issue, or commit the agent actually read, quoted with its `file:line`, issue reference, or commit identifier.
- `external:` named prior art or a known pattern, with its source.
- `reasoned:` a first-principles argument, written out in full.

## Process

### 1. Scope

The argument is the **focus**: a feature, a flow, a constraint, or nothing. Ideate at full ambition inside the focus, and keep the whole repo as the subject when there is none.

When the subject cannot be identified (no argument and no clear project in the working directory), ask one question through the host's live multiple-choice capability when available, otherwise in chat, with these options: a subject the user names, **Surprise me** (each frame picks the subject it finds most interesting), and **Cancel**. Follow the live schema and recommend the smallest option that fits. Leave solution direction, audience, and success criteria to `/grill-with-docs`.

Done when the subject is named or the user picked Surprise me.

### 2. Ground

Read the glossary and the ADRs (`docs/agents/domain.md` gives the layout; by default `GLOSSARY.md` and `docs/adr/` at the root), and the README. Then spawn one fresh read-only exploration subagent to map the subject: what exists, where it hurts, what recently changed (`git log`), open TODOs, and open issues in the repo's issue tracker (`docs/agents/issue-tracker.md` says where). It returns a **grounding summary** of at most 150 lines, with provenance for every claim: `file:line` for files, issue references for tracker evidence, and commit identifiers for history. If subagents are unavailable, use a sequential fresh session where possible. Otherwise perform this task and the later generation and verification tasks yourself, and report the lack of an independent verifier.

Done when the grounding summary exists. If grounding fails (no repo, empty repo), say so and ideate from the user's description, with `reasoned:` and `external:` bases only.

### 3. Generate

Check the host's worker limit and occupied slots. Dispatch only the frame tasks that fit, queue the rest, and start the next task when a worker finishes. If capacity is unknown, use one worker at a time. Each gets the same grounding summary, the focus, and its assigned **frames**. A frame is a starting bias, not a fence; cross-frame ideas are welcome.

1. **Pain and friction**: what is slow, broken, or annoying.
2. **Inversion, removal, or automation**: flip a painful step, delete it, or automate it away.
3. **Assumption-breaking**: what is treated as fixed but is a choice; reframe one level up or sideways.
4. **Leverage and compounding**: moves that make many future moves cheaper.
5. **Cross-domain analogy**: how a different field solves the same shape of problem. Push past the first analogy.
6. **Constraint-flipping**: take a constraint to its opposite or extreme (budget 10x or 0, one user or a million), and keep the design that falls out.

Use four frame tasks: frames 1, 2, and 4 get one each; frames 3, 5, and 6 share the fourth, since all three invert givens. Give every task this charter:

> The user will pick one of these ideas to build, so an idea earns its place only if it could change what they do next. Your first few ideas are the obvious ones: treat them as warm-up. Return about 6 per frame, each with a title, a 2-4 sentence summary, a tagged basis, and one line on why it matters. A `direct:` basis quotes a line you read, never a guessed citation. Drop any idea you cannot give a basis. Stay inside the focus.

Done when all four frame tasks have returned results.

### 4. Merge

Dedupe into one list, then add up to five **combinations**: ideas from different frames that are stronger together. In Surprise me, combinations are the point, so give them more attention.

### 5. Verify

Spawn one fresh subagent. It gets only the grounding summary and the merged list, never the generation history. Its job is to **refute**: check that every `direct:` quote exists, that every `external:` source says what is claimed, and that every `reasoned:` argument holds. It returns a verdict per idea.

Then you decide which ideas make the final cut. Overrule a verdict only when evidence in context contradicts it, and say so. Every cut idea gets a one-line reason: vague, basis refuted, no basis, duplicate of a stronger idea, already done, cost over value, or outside the focus.

Rank the survivors by basis strength (`direct:` above `external:` above `reasoned:`, all else equal), expected value, leverage, and size. Keep 5-7, or the count the user asked for. When fewer pass, report fewer.

Done when every merged idea is either ranked or carries a cut reason.

### 6. Write

Write `docs/ideation/YYYY-MM-DD-<topic>.md` (`open` as the topic when there is no focus), creating the directory if needed:

- **Subject**: the focus, and the grounding summary cut to its key points.
- **Ranked ideas**: for each survivor, the title, summary, basis, why it matters, size (S, M, or L), and a **Take it further** prompt in a fenced block. The prompt opens with the grill-with-docs command in the form this session invoked `ideate` with: `/grill-with-docs` in Claude linked installs or Cursor, `/supermatt:grill-with-docs` from the Claude plugin, `$grill-with-docs` in Codex, or `/skill:grill-with-docs` in OMP. It then names the idea, reproduces its basis verbatim with the file, issue, commit, or external-source references, or complete first-principles argument, and says why it matters. A fresh session has no report and no grounding, so the prompt stands alone. `grill-with-docs` ships alongside this skill and is intended for user invocation; it may be absent from the model-facing skill listing. OMP hiding is not an authorization boundary. Keep this as a user handoff and write the applicable command exactly.
- **Cut**: a table of every cut idea and its reason.

### 7. Present

Print one line with the counts and the absolute path (`7 ranked, 31 cut → <path>`), then one line per survivor: `1. <title> · <basis type> · <size>`. When at least one idea survives, name the top pick in a sentence; otherwise say no idea passed verification. Then stop: the user takes a surviving idea into `/grill-with-docs` by pasting its **Take it further** prompt.
