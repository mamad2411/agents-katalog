---
name: lyra-de-slop
description: "Removes AI-generation artifacts from code, prose, and tests: narration comments, `any` escape hatches, dead code, debug statements, defensive theater, over-abstraction, over-nesting, assertion-free tests that manufacture false green, and AI-sounding docs (emoji headers, 'comprehensive/seamlessly' filler, changelog bullets that restate the diff). Diff-scoped by default, verified after every sweep. Use when asked to clean up AI-generated code, remove slop, tidy a branch before review, or humanize documentation."
compatibility: "No tools required. Optional: git (diff scoping), typechecker + test runner (verification), knip/depcheck (dependency slop). Composes with lyra-clean-code, lyra-bug-hunter, lyra-security-supply-chain. Version policy: examples target the latest stable release of every tool; minimum supported is the newest LTS (or last maintained major), and features newer than the minimum are flagged inline."
---

# lyra-de-slop

## What it does

Removes what AI-assisted development leaves behind — in code, in prose, and in tests — without changing behavior. Slop is anything that exists because a model generated it, not because the codebase needs it: comments narrating the obvious, `any` types papering over unknowns, defensive try/catch on paths that cannot fail, helpers with one caller, tests that assert nothing, READMEs full of emoji headers and "comprehensive" adjectives. De-slop deletes or repairs it, scoped to your own changes by default, and backstops every sweep with the typechecker and tests — necessary evidence of preservation, not proof, so the riskier the removal, the more the sweep leans on review (see Verification).

## Scopes and modes

| Mode        | Behavior                                                                    |
| ----------- | --------------------------------------------------------------------------- |
| default (`--changed`) | Clean only files/hunks this branch introduced vs the merge-base — the reviewable scope |
| `--all`     | Whole tree (monorepo: per package, sequentially) — only when explicitly asked |
| `--dry-run` | Detect and report every artifact grouped by type with counts; edit nothing  |

Mode names are **vocabulary, not a CLI** (same convention as lyra-bug-hunter): they arrive as words in the user's request, and absent any, the default applies. Resolve the branch scope with `git merge-base HEAD origin/HEAD` (fallbacks in order: `origin/main`, `main`, `master` — `origin/HEAD` only exists on cloned repos); only touch files in that diff, and prefer staying inside the changed hunks. Pre-existing slop elsewhere is reported, not edited — keeping cleanup reviewable is the point.

## Code slop

### 1. Comments that narrate instead of explain

Delete comments that restate the code (`// increment counter`), narrate the generation process (`// Now we handle the error case`), or log the change (`// added validation`, `// new helper function`) — that last kind is the model talking to its reviewer, dead the moment the PR merges. Keep comments that state a *why* or a constraint the code can't express.

### 2. Type escape hatches

Replace `any`, `as any`, and `@ts-ignore`/`@ts-expect-error` without a reason with real types. Type the boundary once (parse/validate at the edge) instead of casting at every use. If the correct type is genuinely unknowable, `unknown` plus narrowing beats `any`.

### 3. Dead code

Remove commented-out blocks (git remembers), unused imports/variables/exports, unreachable branches, and feature flags whose rollout finished. Side-effect imports (CSS, polyfills, module registration) are not dead — check before cutting.

### 4. Debug artifacts

`console.log`/`print` debugging goes — route real logging through the project's logger, delete the rest. TODO/FIXME without an owner or issue link either gets one or gets deleted; a bare TODO is a wish, not a plan.

### 5. Defensive theater

Remove try/catch that swallows errors or rethrows without adding context on trusted internal paths, and null-guards for states the types already forbid. Keep validation at real trust boundaries — user input, network, filesystem, third-party APIs. The test: can this branch execute? If no input reaches it, it's theater.

### 6. Over-abstraction

Inline single-caller helpers, unwrap wrapper classes that add nothing, delete config options nothing configures, and collapse premature interfaces with one implementation. Three concrete uses justify an abstraction; a model's habit of "making it reusable" does not.

### 7. Over-nesting

Collapse `if/else` pyramids into early returns and guard clauses, matching the surrounding file's style. Depth beyond ~3 levels in generated code is almost always inversion, not necessity.

## Prose slop (docs, READMEs, comments, commit messages, changelogs)

### 8. AI-register vocabulary and structure

Delete "comprehensive", "robust", "seamlessly", "leverage", "delve", "streamlined", and enthusiasm that no human wrote ("This powerful feature..."). Strip emoji headers and decorative emoji from technical docs. Replace bullet lists that restate the diff with one sentence saying what changed and why it matters. Rewrite hedged non-claims ("this should generally work in most cases") into what is actually true.

### 9. Documentation that documents nothing

Remove README sections that exist to have sections (empty "Contributing", boilerplate "Features" lists restating the nav), JSDoc that repeats the signature (`@param name — the name`), and changelog entries padded to look substantial. A doc that says less, accurately, beats one that says more, generically.

## Dependency slop

### 10. Packages installed by reflex

A model needing one function installs a library — left-pad thinking at 2026 scale. Sweep the diff's dependency additions: a package used in zero files (remove), a heavy dependency used for one call the stdlib covers (inline it and remove), a duplicate of something already in the tree (consolidate). Detect with `knip`/`depcheck` or by grepping imports against the manifest diff. Every removed package is attack surface returned to sender (lyra-security-supply-chain rule 4 is the policy; this rule is the cleanup).

## Test slop

### 11. Tests that prove nothing

The most damaging AI artifact, because it manufactures false green: tests with no meaningful assertion (`expect(result).toBeDefined()` on something that can't be undefined), tests that mock the unit under test and then assert the mock, copy-pasted test scaffolds whose name promises a scenario the body never exercises, and snapshot tests nobody reviewed. Fix by writing the real assertion when the intent is recoverable; delete when the test asserts nothing a compiler doesn't already guarantee. Never count deleting a fake test as lost coverage — it was never coverage.

## Verification (mandatory)

After every sweep: run the typechecker and the test suite; both must be as green as they were before the sweep. Green is **necessary evidence, not proof** — deleting guards, catch blocks, or logging *does* alter error propagation and output, and tests only witness behavior where coverage exists, which in AI-generated code is exactly where it's thinnest. So calibrate by risk: mechanical removals (unused imports, dead comments) need only the green run; behavior-adjacent removals (defensive theater, rule 5; dependency removals, rule 10; test deletions, rule 11) get a dry-run first, a human-readable justification per site, and extra scrutiny where coverage is thin. If a "cleanup" breaks the run, that artifact was load-bearing — revert it and flag it instead. Never delete configs, entry points, license headers, or lint pragmas that carry a reason. Report the sweep grouped by artifact type with counts, plus anything flagged as suspicious-but-kept.

---

_Part of the [skill collection](../README.md)._
