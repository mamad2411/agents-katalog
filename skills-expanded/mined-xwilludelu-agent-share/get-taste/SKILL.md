---
name: get-taste
description: "Develop foundational knowledge, disciplinary fluency, and research taste through reusable field guides. Use when the user wants research prompts for one or more fields, synthesis of returned research reports, or autonomous research through final delivery. Supports manual handoff to an external researcher and an auto mode that runs the same workflow directly."
---

# Get Taste

Build the background that helps an agent understand a field, discuss it
naturally, and exercise informed judgment across projects. Teach research taste
through concepts, distinctions, and examples rather than generic rules. The
deliverables are research prompts and one integrated field guide.

## Establish the task

Recover the target fields, intended reader, interests, and current stage from
the conversation and supplied materials. Start from prompts, returned reports,
or an existing guide as appropriate.

Default to **manual handoff**: the user takes prompts to an external research
LLM or agent and returns its reports. Use **auto** when the user asks you to
run the research and deliver the guide directly. Switching modes later
continues from existing work.

Honor any requested prompt count or grouping. Otherwise pick a practical count
for the scope and briefly explain the grouping: combine related fields or split
a broad field into complementary directions so every requested field is covered
by substantive connections rather than equal-sized buckets. Ask only when an
unresolved scope choice would materially change the work.

The final guide defaults to **English, ~4,000 body words (excluding
references)** across all requested fields. Prompts and returned reports may use
the user's language while retaining established technical terms. Honor explicit
language and length overrides. Prefer selection and compression to expansion;
if essential connections still require substantially more space, propose a
specific increase and its content tradeoff for approval.

## Prepare research prompts

Read [Research design and source practice](references/research.md).

Write the requested number of clearly separated, self-contained prompts,
preceded by a brief scope and grouping explanation. Each prompt is a complete
research brief — purpose, field scope, substantive directions, source
expectations, and expected report format — carrying all context an external
researcher needs without access to this conversation, the skill files, or the
other prompts.

In manual mode, deliver the prompts and wait for reports (a prompt-only request
ends here). In auto mode, execute the same prompts directly without per-group
approval.

## Research and integrate

Apply the source practice in `references/research.md` across both modes.

**Returned reports:** Read supplied reports in full, including source notes.
Map coverage to the agreed fields, spot overlap and connections, and examine
consequential disagreements or missing foundations. Accept reports
incrementally; if more are forthcoming, wait to finalize until they arrive or
the user asks to proceed.

**Auto:** Execute the prompts with available search, retrieval, and
source-reading tools, working sequentially or delegating bounded groups where
useful without asking the user to relay reports or approve routine steps.

In both modes, re-read, reinterpret, and supplement material within the agreed
scope. Close consequential gaps and conflicts with targeted research — or, in
manual mode, a focused follow-up prompt. Respect any user limits on source use.
Synthesize once the foundations and central connections are supported and
further reading would mainly add redundant examples.

## Write the field guide

Read [Field-guide editing](references/field-guide.md). Select the concepts and
relationships that carry the guide, then write one coherent account — research
groups and report outlines need not become chapters.

For editorial calibration, pick a relevant guide from the
[example index](examples/README.md). Borrow its explanatory depth, terminology,
and selection discipline, not its disciplinary scope or chapter structure.

## Save and deliver

Save only the research prompts and final guide in the user's chosen workspace;
keep working notes, source extracts, intermediate reports, and drafts in
context. Leave user-supplied reports, unrelated files, and the skill directory
untouched. Reuse the agreed guide path for revisions.

Deliver prompts at handoff in manual mode, or alongside the final guide in auto
mode. Return full Markdown inline when files are not requested or available.

Review explanations, terminology, selection, and citation support, then check
body length and footnotes with the bundled helper (resolving `<skill-dir>` to
the canonical skill directory):

```bash
python3 <skill-dir>/scripts/check_guide.py <guide.md> --budget 4000
```

Pass `-` on stdin for an inline guide, match `--budget` to the agreed target,
and use `--references-heading "Heading text"` for a custom bibliography heading.
The helper checks approximate English word counts and footnote consistency;
editorial and scientific quality still require reading the guide. For
non-English guides, use an appropriate length measure and distinguish estimates
from measured counts.

Deliver the completed guide with its body length (excluding references) and
reference count. Mention coverage or source-access limitations only when they
materially affect the result.
