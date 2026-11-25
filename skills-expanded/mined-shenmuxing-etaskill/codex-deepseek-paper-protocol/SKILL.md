---
name: codex-deepseek-paper-protocol
description: Protocol-level two-agent paper writing workflow. Use when the user wants Codex to plan and review from global context while DeepSeek writes or revises the manuscript through the global deepseek-agent skill, with muxing-style-review used for explicit prose style checks.
---

# Codex-DeepSeek Paper Protocol

Use this skill to coordinate two agents for academic writing:

- **Codex** is the principal reviewer, planner, and protocol controller.
- **DeepSeek** is the writing agent.
- **K = 4** review-feedback rounds by default, unless the user specifies another value.
- The concrete DeepSeek invocation is handled by the global `deepseek-agent` skill.

This skill is a protocol that defines how the agents cooperate.

## Required Companion Skill

Use `@deepseek-agent` whenever this protocol delegates to DeepSeek.  That skill owns the installed OpenCode execution mechanics for the DeepSeek backend, including:
- checking OpenCode and DeepSeek provider credentials when needed,
- calling the bundled `deepseek-agent/scripts/invoke_deepseek.ps1` wrapper,
- choosing `direct-edit`, `unified-diff`, `replacement-block`, or `answer-only`,
- using the standard invocation path with `-Auto`, `-UsePromptFileReference`, and `-ResultFile`,
- optionally using `-ResumeSession` or `-Continue` for later rounds of the same bounded task.

This protocol owns the brief, review, feedback loop, and integration judgment. Do not duplicate CLI calling details here beyond the delegation rules below.

Use `muxing-style-review` as the style-control layer in two distinct modes. Before delegation, explicitly use the compact mode by loading `muxing-style-review/references/check-compact.md` and injecting only the relevant compact rule directives into the DeepSeek brief. After DeepSeek returns prose, explicitly request a complete/full `muxing-style-review` review. For non-trivial manuscript prose, use the skill's dedicated review-subagent option for the manual/model part of the full review when the active harness supports subagents. Treat the returned rule-level findings and revision brief as Codex review evidence; do not let the style review replace DeepSeek's authorship.

## Core Rule

Codex must not directly write manuscript prose when this protocol is active.

Codex may:

- inspect project context,
- decide what should be written,
- select and summarize necessary context,
- write task briefs for DeepSeek,
- review DeepSeek output,
- request revisions,
- apply mechanical integration only when necessary to preserve files, such as accepting a patch, fixing a broken include path, or resolving a trivial LaTeX syntax issue introduced by a patch.

Codex must not:

- draft paragraphs, theorem explanations, related work prose, abstracts, introductions, or conclusions itself,
- rewrite DeepSeek prose directly because it sounds weak,
- silently replace DeepSeek's writing with Codex-authored text,
- over-specify wording so tightly that DeepSeek is reduced to filling blanks.

If prose quality is insufficient, Codex writes a better revision instruction and sends it back to DeepSeek.

## Role Split

### Codex Responsibilities

Codex owns judgment and global coherence:

1. Understand the user's actual goal, target artifact, and audience.
2. Read enough project context to determine what content is needed.
3. Identify the local writing unit: whole paper, chapter, section, subsection, theorem explanation, related work block, or revision pass.
4. Decide the minimum sufficient context DeepSeek needs.
5. Write a clear but non-overconstraining DeepSeek brief.
6. Review DeepSeek output for:
   - self-containedness,
   - logical clarity,
   - correctness,
   - consistency with project context,
   - claim-evidence alignment,
   - notation consistency,
   - citation discipline,
   - venue or book style fit,
   - absence of fabricated results, citations, or claims.
7. Produce revision requests until the output passes or K rounds are exhausted.
8. Report remaining risks to the user.

### DeepSeek Responsibilities

DeepSeek owns writing and revision:

1. Draft the requested manuscript text.
2. Preserve the target format, usually LaTeX or Markdown.
3. Use only the context supplied by Codex and any explicitly allowed project files.
4. Make substantive prose, structure, and explanation changes requested by Codex.
5. Return either direct workspace edits, a unified diff, a clearly delimited replacement block, or answer-only text according to the `deepseek-agent` output contract selected by Codex.

DeepSeek should have room to choose wording, local paragraph order, examples, and explanatory framing, as long as it satisfies Codex's constraints.

## Workflow

### Step 1: Build Task Context and Plan Writing

Codex first combines the user's intent with enough project context to make the task actionable, then forms a bounded writing plan before delegation. Determine the target writing unit, hard constraints, source materials, and assumptions only to the level needed for delegation.

Read relevant project context before delegating. Prefer:

- current manuscript files,
- outline or table of contents,
- nearby sections,
- project notes,
- figures/tables/captions,
- bibliography files,
- reviewer comments or TODOs,
- prior drafts.

Before writing the DeepSeek brief, Codex should identify the planned content components:

- the target writing unit and its function in the manuscript,
- the reader state at this point in the manuscript,
- the concepts, definitions, claims, equations, examples, citations, or figures that the unit should cover,
- the evidence or source map for claims that need support,
- notation and terminology constraints from nearby manuscript context,
- the local structure or argument flow at the level of sections, paragraphs, or proof responsibilities,
- exclusion boundaries for material that should not be introduced,
- acceptance checks Codex will apply after DeepSeek returns output,
- choices left to DeepSeek, such as wording, transitions, local examples, and explanatory framing.

This plan should specify content responsibilities and integration constraints, not draft manuscript prose. Avoid full paragraph drafts, sentence-level wording, or an outline so detailed that DeepSeek is reduced to filling blanks.

Codex should not dump all context or the full planning notes into DeepSeek. Select only what is necessary for the writing unit, and ask the user only when missing information would materially change the artifact.

If DeepSeek may edit files directly, record the target file state before delegation so later review can distinguish intended changes from unrelated user edits.

### Step 2: Write the DeepSeek Brief

Every DeepSeek brief must include:

1. **Task**: what to write or revise.
2. **Target files**: exact path(s), and whether edits are direct, patch-based, or replacement-block based.
3. **Purpose**: why this text exists in the paper.
4. **Audience**: expected reader and venue/book style.
5. **Context**: concise summaries plus exact excerpts when needed.
6. **Must include**: claims, definitions, equations, examples, citations, or figures that must appear.
7. **Must avoid**: fabricated results, invented citations, unsupported claims, author metadata, unexplained notation, excessive hype.
8. **Freedom**: what DeepSeek may decide independently, such as wording, paragraph transitions, local organization, and explanatory examples.
9. **Output contract**: direct edit, unified diff, replacement block, or answer-only; include changed-file list when edits are allowed.
10. **Style criteria**: compact `muxing-style-review` directives selected from `muxing-style-review/references/check-compact.md`, especially reader state, supported claims, calibrated claims, consistent terms, and concrete language.
11. **Acceptance criteria**: concrete checks Codex will apply.

The brief should constrain substance without becoming a hidden draft. Give DeepSeek goals, facts, constraints, examples when needed, and acceptance criteria. For style criteria, use the compact mode only: read `muxing-style-review/references/check-compact.md`, select the directives relevant to the writing unit, and paste those concise directives into the brief. Do not paste `RULES.md`, `check-human.md`, or the full rule body into the DeepSeek writing prompt unless the user explicitly asks for that heavier context. Avoid full paragraph drafts, sentence-by-sentence outlines, exact phrasing unless preserving a required term, unnecessary rhetorical style commands, and large source dumps when a summary is enough.

### Step 3: Delegate to DeepSeek

Use `deepseek-agent` to send the brief. Save the brief to a temporary or task-local Markdown file, have DeepSeek read that file, and require the artifact to be written to `-ResultFile`.

Session policy:

- Start fresh for round 1 of each distinct manuscript task.
- Reuse the same session for later rounds of that same task when useful.
- Prefer `-ResumeSession <id-or-prefix>` when the session id is known.
- Use `-Continue` only when no unrelated DeepSeek task has run in this workspace since the prior round.
- Never reuse a session across materially different target files, sections, or source contexts.

Each revision brief must still restate the active target files, output contract, non-negotiable constraints, and concrete issues to fix. Session reuse is an optimization, not a substitute for a complete revision brief.

Use the standard wrapper path from `deepseek-agent` with `-Auto`, `-UsePromptFileReference`, `-ResultFile`, and structured output/transcript files. Add `-Model <provider/model>` when the DeepSeek backend must be forced rather than taken from OpenCode's configured default. Add exactly one session reuse flag when needed: `-ResumeSession <id-or-prefix>`, or `-Continue` only under the safety condition above.

In this protocol, `-Auto` means the DeepSeek process can read the saved brief and use workspace tools. It does not by itself grant permission to edit manuscript files. The output contract in the brief decides what DeepSeek may change.

Choose the output contract before invoking:

- `direct-edit`: DeepSeek may edit only the explicit target files. Require a changed-file list and inspect the diff after return.
- `unified-diff`: DeepSeek must not edit manuscript files directly. It writes the patch to `-ResultFile`; Codex inspects and applies it after review.
- `replacement-block`: DeepSeek must not edit manuscript files directly. It writes the bounded replacement text to `-ResultFile`; Codex integrates it after review.
- `answer-only`: DeepSeek must not edit manuscript files directly. It writes analysis, critique, planning, or draft text to `-ResultFile`.

Use `-Model <name>` only when the user specifies one or a project rule requires it. Otherwise use the configured DeepSeek profile.

If the DeepSeek calling skill does not exist yet, stop at a prepared brief and tell the user the missing dependency. Do not substitute Codex drafting for DeepSeek writing.

### Step 4: Codex Review

Codex reviews DeepSeek output against the acceptance criteria and global context. Inspect changed files, verify only intended files changed, check formatting and references, run available compile or lint commands when appropriate, and avoid overwriting unrelated user edits.

If DeepSeek returns a patch, Codex may apply the patch after review, but should not rewrite the manuscript content while applying it.

Run an explicit complete/full `muxing-style-review` check when DeepSeek returns prose in a Markdown-compatible file or extract:

1. If DeepSeek edited a Markdown manuscript file, call `@muxing-style-review` or `/muxing-style-review FILE` and explicitly request a complete/full check.
2. If DeepSeek returned a replacement block or LaTeX-only prose, save only the prose-bearing excerpt to a temporary Markdown review file, then call `@muxing-style-review` or `/muxing-style-review` on that file and explicitly request a complete/full check.
3. If comparing a previous draft with DeepSeek's revision, call `/muxing-style-review A.md B.md` and ask it to judge full-rule regressions and improvements, not only mechanical detector counts.
4. For non-trivial complete/full reviews, ask `muxing-style-review` to use its dedicated review-subagent option when the active harness supports subagents and the user has not prohibited delegation. The parent Codex thread should provide the target excerpt, local reader, venue or book style, manuscript position, nearby definitions, notation, claims, citations, and reviewer comments needed to judge reader state, evidence, citation discipline, terminology, and manuscript fit.
5. Keep the full rule body out of the parent DeepSeek-writing prompt. The full review may use `check-human.md`, `RULES.md`, and `subagent-review-prompt.md` inside the review path, but Codex should pass only the necessary excerpt and context instead of injecting the full rule contract into the main writing loop.
6. In the parent Codex thread, inspect the subagent output instead of accepting it blindly. Merge it with automatic `agent-style review --audit-only` evidence when available, remove false positives, and add issues the subagent missed because it lacked local manuscript state.
7. Record the rule-level findings and classify style issues as BLOCKER, MAJOR, or MINOR according to their manuscript impact.
8. If style fixes are needed under this protocol, convert accepted findings into a DeepSeek revision brief, preferably using `muxing-style-review/references/revision-brief-template.md`; do not directly rewrite manuscript prose in Codex.

Do not run `muxing-style-review` on raw LaTeX fragments when markup would dominate the audit. Extract prose or convert a bounded excerpt to Markdown first, preserving citations, equations, labels, and inline code as literal text where needed.

Use this review checklist:

- Is the text self-contained for its position in the manuscript?
- Does the logic flow from motivation to claim to evidence?
- Are all technical statements consistent with the project files?
- Are equations, variables, assumptions, and names consistent?
- Are citations present where needed and absent where unsupported?
- Are results and numbers copied accurately?
- Does the text avoid overclaiming?
- Does the section connect to the previous and next manuscript units?
- Is the output in the requested format?
- Does it introduce any stale labels, duplicate labels, broken references, or TODO placeholders?
- Does `muxing-style-review` flag 21-rule style violations that materially weaken trust, reader state, evidence, citation discipline, terminology, clarity, or structure?

Codex classifies issues as:

- **BLOCKER**: incorrect, unsupported, fabricated, incoherent, or unusable.
- **MAJOR**: substantially weak, incomplete, inconsistent, or poorly integrated.
- **MINOR**: localized clarity, style, formatting, or small consistency issue.

### Step 5: Feedback Loop

Run up to K rounds.

For each failed round:

1. Codex writes a revision brief listing only the issues that must change.
2. Codex preserves DeepSeek's valid choices instead of resetting the draft.
3. Codex gives evidence from files or context for each requested change.
4. DeepSeek revises through `deepseek-agent`, following the Step 3 session policy.
5. Codex reviews again.

Track the session identity for each task in the temporary task notes, transcript, or output metadata when available. If session identity cannot be recovered, keep the next revision brief self-contained and either start fresh or use `-Continue` only after confirming no unrelated DeepSeek invocation has occurred in this workspace.

Stop early when:

- no BLOCKER or MAJOR issues remain,
- remaining MINOR issues are acceptable or purely mechanical,
- the user asks to stop.

When K rounds are exhausted, Codex reports:

- what passed,
- what remains unresolved,
- whether the current output is usable,
- the next most useful action.

## Feedback Style

Codex feedback to DeepSeek should be precise and actionable:

- Bad: "Improve the introduction."
- Good: "The introduction states the method before defining the problem. Revise the first three paragraphs so the reader first sees the bottleneck, then the missing capability, then the proposed mechanism. Preserve the current quantitative claim and citation list."

- Bad: "Make it more rigorous."
- Good: "The proof sketch uses `converges` without stating the topology or limit object. Add a sentence that identifies the convergence mode and points to the formal statement in Section 3. Do not introduce a new theorem."

## Final Response

Codex reports:

- target files touched,
- number of DeepSeek rounds used,
- remaining issues by severity,
- verification performed,
- steps that failed, were skipped, or were unavailable, with concrete reasons,
- whether the artifact is ready for the next workflow step.

Keep the final response concise. Do not include the full DeepSeek brief unless the user asks for it.
