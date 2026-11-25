---
name: playbook
description: Use this skill when the user asks to create, review, improve, trim, audit, or standardize an AGENTS.md file, or to derive agent instructions from a codebase. Produces compact, repo-specific, LLM-optimized AGENTS.md files and, when useful, companion authoring guidance such as AGENTS_MD_GUIDELINE.md.
---

# Playbook

`AGENTS.md` is an instruction file for coding agents. Optimize it for fast machine consumption, not human onboarding.

Examples in this skill are illustrative only. Never copy example terms, commands, or paths into the target `AGENTS.md`. Derive every word from the actual repository.

## Prime Directive: Minimalism

A bloated `AGENTS.md` is worse than no `AGENTS.md`. Every extra line:
- Pollutes the agent's context window on every task in the repo.
- Becomes long-term tech debt that drifts out of sync with the code.
- Dilutes the high-signal rules and degrades agent performance.

**Size budget**:
- Typical repo: 5–20 bullets total.
- Complex monorepo or unusual stack: up to ~40 bullets.
- Hard ceiling: if the file would exceed ~50 lines, you are almost certainly wrong. Cut.

A great `AGENTS.md` may have only 3 bullets. Short is the goal, not a side effect.

## The Justification Test (Mandatory)

For every candidate line, the agent MUST stop and answer all three questions out loud in its reasoning before keeping it:

1. **What concrete, expensive mistake does this prevent?** Name the failure. If you cannot name one, cut.
2. **Could a competent agent infer this in seconds from `ls`, manifests, imports, framework conventions, or the README?** If yes, cut.
3. **Is this specific to THIS repo?** If the same line would apply to any project in the same language/framework, cut.

A line survives only if it prevents a real, repo-specific mistake that an agent would not catch from a quick glance at the code.

**When in doubt, cut.** The bar for inclusion is intentionally high. Err on the side of an empty section over a marginal bullet.

## Mandatory Project-Maturity Interview

Before finalizing `AGENTS.md`, ask the user the following questions unless the repo answers them unambiguously through release docs, public API guarantees, migration history, or existing contributor guidance:

1. **Project stage**: early development / actively evolving / established and stable?
2. **Breaking changes**: freely allowed / allowed with care / forbidden?
3. **Backward compatibility**: required for public APIs, CLIs, schemas, or configs / not a concern?

Use the answers to set the maintenance posture, encoded as 1–2 directive bullets:

- **Fresh / early-development projects**: agents MUST prioritize clean, well-organized, maintainable code. Prefer large refactors over backward-compatible shims. Compatibility is explicitly not a goal.
- **Established / stable projects**: preserve public interfaces unless the task explicitly allows breaking them. Prefer minimal diffs and migration plans over sweeping rewrites.
- **Mixed**: state the rule per surface (e.g. "internal modules: refactor freely; HTTP API: preserve").

Skip a question only when the repo's answer is obvious. Do not pad the interview with unrelated questions.

## What Belongs (only if it passes the Justification Test)

- Canonical domain terminology when the repo uses non-obvious or overloaded terms.
- Generated / codegen paths that must not be hand-edited.
- Canonical validation, build, lint, test, or typecheck commands.
- Subproject or monorepo boundary rules.
- Maintenance posture from the interview above.
- Repo-specific footguns that have actually bitten contributors.

## What Does Not Belong (cut on sight)

- Generic engineering advice ("write clean code", "run tests before committing").
- Facts visible from `ls`, manifests, imports, or framework conventions ("this project uses Python").
- Setup or architecture content — belongs in `README.md`.
- Soft wording: "try to", "consider", "be aware", "where appropriate".
- Restated content from other docs that does not prevent a likely mistake.
- Volatile operational details that will go stale fast.
- Aspirational rules nobody in the repo actually follows.

## No Fixed Template

Do not impose a section structure. Sections invite padding because the agent feels obligated to fill them.

- If the file has 5 useful bullets, ship 5 bullets with no headings.
- Add a heading only when grouping genuinely helps scanning a longer file.
- Never include an empty or near-empty section as a placeholder.

The file should read like the shortest possible answer to: "What will an agent get wrong in this repo if nobody tells it?"

## Discovery Workflow

1. Inspect repo root docs, manifests, CI workflows, package scripts, lint/typecheck config.
2. Inspect codegen paths and generated artifacts.
3. Identify domain terminology that must stay consistent.
4. Identify subproject boundaries and local conventions.
5. Run the project-maturity interview if the repo does not already answer it.
6. Draft candidate bullets from findings.
7. Run every bullet through the Justification Test. Cut aggressively.
8. Order surviving bullets by cost-of-mistake, highest first.

Never invent constraints. Derive them from the repo or from the user's answers.

## Writing Style

- Imperative phrasing.
- Exact commands, filenames, paths, and terms — no placeholders, no hedging.
- Highest-cost mistakes first.
- No rationale unless the rationale itself changes agent behavior.
- No prose paragraphs.

Good:
```
- Use `Order` (not `Purchase`) as the canonical domain term.
- Do not hand-edit files under `gen/proto/`; regenerate via `bun run codegen`.
- Validate with `bun run check`. Full CI parity: `bun run verify`.
- Internal refactors welcome; preserve the public HTTP API.
```

Bad:
```
This project values clean code, so please try to write maintainable
implementations. There are some generated files which you should be
careful with. Tests should be run before committing changes.
```

## Updating an Existing AGENTS.md

- Apply the Justification Test to every existing line. Cut what fails — even lines that look reasonable.
- Preserve sharp, repo-specific guidance verbatim.
- Compress prose into bullets.
- Do not rewrite for style if a line is already correct and tight.
- A successful update almost always shrinks the file. If yours grew, re-check the Justification Test.

## AGENTS.md vs AGENTS_MD_GUIDELINE.md

When the user asks for both:

- **`AGENTS.md`** — for agents. Tiny, directive, repo-specific. LLM-oriented.
- **`AGENTS_MD_GUIDELINE.md`** — for humans authoring `AGENTS.md`. Explanatory, generalizable, may include rationale, heuristics, anti-patterns, and templates.

Never let the human-oriented guideline bleed into `AGENTS.md`.

## Final Review (run before delivering)

Answer each, honestly:

- Did every line pass the Justification Test out loud?
- Is the maintenance posture explicit, and does it match the user's interview answers?
- Are domain terms, codegen paths, and validation commands accurate and current?
- Would removing any single line genuinely hurt an agent's next task in this repo?

If the last answer is "no" for any line, cut that line and review again.

## One-Sentence Standard

A good `AGENTS.md` is the shortest possible set of repo-specific directives that prevents an agent from making expensive, hard-to-catch mistakes — and nothing more.
