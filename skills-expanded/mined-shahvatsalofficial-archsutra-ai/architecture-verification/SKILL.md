---
name: architecture-verification
description: Verify architecture deliverables before they are shared. Spot-checks that each finding's file and line evidence is real, runs the archsutra verify checks (skills, agents, links, diagram syntax, findings schema), confirms ADR completeness, proposes fitness functions and lists what was not verified. Use this skill whenever the user is about to publish, send, merge or present an audit, design document, ADR or diagram, or asks "are these findings real", "check my report", "validate the docs" or "double-check this", even if they do not mention architecture. Do not use it to produce new analysis.
license: Apache-2.0
compatibility: Works with file read and search tools. The archsutra CLI (Node 20+, offline) runs the structural checks; without it, do them by reading.
---
# Architecture Verification

Be the reader's last line of defense. Check that what is about to be shared is true, consistent and reproducible, and say plainly what you could not check.

## Why this skill is built the way it is

- Reports written by a model, or built from scanner output, contain confident mistakes. A wrong finding costs the reader's trust in all the right ones.
- Structure is cheap to check and evidence is not, so both are checked, evidence first.
- A verification that hides what it skipped is worse than none. The skipped list is part of the result.

## Workflow

1. **Run the structural checks.** If available: `archsutra verify .`. Report the exact output, including failures. Without the CLI, check by reading: frontmatter of skills and agents, relative links, diagram syntax, findings fields.
2. **Spot-check evidence.** Pick at least five findings (all critical and high ones first) and open each cited file and line range. Use [references/evidence-spot-check.md](references/evidence-spot-check.md). Downgrade, correct or remove anything that fails, and say which.
3. **Check diagrams.** Valid Mermaid type, balanced brackets, every element traceable to evidence or labeled `proposed`. Note that syntax checks do not prove the diagram renders.
4. **Check ADRs.** Each has status, context, options considered, decision, consequences and a revisit trigger. A decision without rejected options is a gap.
5. **Check consistency.** Numbers, names and ids agree across the report, the findings file and the diagrams. Counts in the summary match the lists.
6. **Check claims against limits.** No certification or compliance language; no "secure" or "100%"; scores are `not assessed` where evidence is missing; secrets are redacted.
7. **Propose fitness functions** from [references/fitness-functions.md](references/fitness-functions.md) for the rules the report relies on, and say which exist and run automatically today.
8. **Close with a verdict**: pass, pass with changes (list them), or do not publish (reason). Then list what was not verified.

## Rules that keep verification credible

- **Reproduce, do not trust.** If you cannot reproduce a claim from the cited location, it is `unknown` until someone can.
- **Report failures plainly.** Do not soften a failed check or bury it in a long list.
- **Never imply a check ran if it did not.** "Not verified: diagram rendering" is a good line; silence is not.
- **Stay read-only.** Propose corrections; apply none without approval.

## Output

A short result: verdict, checks run with pass or fail, corrected or removed findings with reasons, proposed fitness functions, and the explicit "not verified" list.

Write that result as both `docs/architecture/verification.md` and `docs/architecture/verification.html`. Save the Markdown, then run `archsutra html docs/architecture/verification.md`. Do not hand-write HTML. Do not leave the verdict only in chat.
