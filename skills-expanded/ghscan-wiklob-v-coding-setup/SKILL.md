---
description: Evaluate a GitHub skill/command for import into this pipeline — fetch the candidate read-only, score it against a license → format → craft-fit rubric grounded in craft/, emit an import / adapt / build-fresh verdict citing craft/, and draft an adapted skill for an "adapt" verdict. Reach for it when you've found an OSS skill, subagent, or slash-command on GitHub and want to know whether (and how) to bring it in.
argument-hint: "<github repo/skill ref>  (owner/repo[/path][@tag])  — omit to get candidate suggestions"
allowed-tools: Bash, Read, Grep, Glob, WebSearch, WebFetch, Skill
---

# /import-skill — judge an external skill against our craft standard, before importing

GitHub is full of reusable agent craft — Claude Code skills (`SKILL.md` folders), subagents, slash-command markdown — and the original goal (a) of the craft layer is to **scour it and bring the good parts in, adapted to our standard, not reinvented**. This command is that ongoing fuel: point it at a candidate, and it returns an auditable **import / adapt / build-fresh** verdict scored against a fixed rubric, plus a draft adapted skill when the call is *adapt*.

It is the GitHub-import sibling of `/research` (which surveys prior art and emits a brief into `/scope`'s plan) and `/review-claude-md` (which fact-roots a file against ground truth and proposes — never silently writes — edits). The contract here is different from both: `/research` produces a *brief*, this produces a *per-candidate verdict + a draft artifact*. Importing a skill is load-bearing context for every future agent that runs it, so — like `/review-claude-md` — this command **proposes a draft for human approval; it never installs into `commands/` itself**.

Read `~/.claude/workflow-conventions.md` first, then `~/.claude/craft/README.md` (the craft register — the standard a candidate is judged against) and `~/.claude/craft/authoring.md` (how to apply that standard to a skill file). This command both *enforces* the craft bar and must *model* it: keep its own judgment terse and reasoned, and cite which `craft/` line drives each gate.

## Why a rubric, and why these three gates in this order

A reuse call is not taste — it is a decision with a dominant axis. License compatibility comes first because it is **disqualifying**, not gradable: a candidate we cannot legally vendor is a dead end no matter how good it is, and resolving it first means we never even fetch source we can't use. Format conformance comes second because it is **mechanical** — does the artifact match the Agent Skills / slash-command shape we can actually load — and cheap to check once the source is in hand. Craft-fit comes last because it is the **judgment** call, the one `craft/` exists to ground, and it only matters for a candidate that already cleared the first two. The verdict falls out of where a candidate stops passing.

## Load config
- `root="$(git rev-parse --show-toplevel)"`; read `$root/.claude/ticket-flow.json` (missing → `/ticket-flow-init`, STOP). `WT_ABS="$root"`.

## 0. Resolve the candidate ref

Take the ref from `$ARGUMENTS`: `owner/repo`, optionally a `/path/to/skill` within the repo, optionally `@tag-or-branch` to pin. Examples: `wshobson/commands`, `anthropics/skills/document-skills/pdf@main`.

- **No ref given** → there is nothing to judge yet, so don't guess one. Run candidate **discovery** instead: invoke `/research` (`Skill(skill="research", args="importable OSS Claude Code skills / subagents / slash-commands on GitHub for <the capability you're after>")`) — it reuses `/deep-research` for depth and returns a `## Prior art & standards` brief naming candidate source repos with cited URLs. Print the brief, suggest re-running `/import-skill <owner/repo>` on a named candidate, and STOP (`needs input: no candidate ref — ran discovery; pick one of the suggested repos and re-run /import-skill <ref>.`). Discovery names sources; it does not score them — scoring needs a specific ref.
- **Ref given** → continue. (Known good starting points from the P7 survey: `anthropics/skills` is the format-of-record to import from; `wshobson/commands` + `wshobson/agents` are permissive-MIT adapt sources; the awesome-lists — `hesreallyhim/awesome-claude-code`, `VoltAgent/awesome-agent-skills` — are *discovery indexes*, not single skills, so feed those to discovery above rather than scoring them as one candidate.)

## 1. Gate 1 — license (resolve before fetching any source)

License is disqualifying, so settle it **before** cloning — never fetch source you may not legally vendor. Resolve the candidate repo's license from metadata, not by eye:

- `gh api repos/<owner>/<repo> --jq '.license.spdx_id // "NONE"'` if `gh` is available; else `WebFetch` the repo's GitHub page / its `LICENSE` file and read the SPDX identifier.
- **Permissive** (`MIT`, `Apache-2.0`, `BSD-*`, `CC0-1.0`, `ISC`, `Unlicense`) → import/adapt is clean. Record the SPDX id (from the real response — never assume; a missing field is `NONE`, surfaced, not guessed — convention 8).
- **Copyleft** (`GPL-*`, `AGPL-*`, `MPL-2.0`) → flag the obligation: vendoring may impose license terms on this repo. Continue to evaluate, but the verdict must surface the obligation and default away from a silent import.
- **Source-available / no license / `NONE`** → STOP this candidate: `needs input: <ref> is <source-available | unlicensed> (<spdx>) — cannot be vendored. Build-fresh from its ideas, or pick a permissively-licensed candidate.` (Real case: `anthropics/skills`' example skills are Apache-2.0 but its document-skills set is source-available — check the *path* you're importing, not just the repo root.)

A failing license gate ends with a `build-fresh` (or stop) verdict and **no clone**.

## 2. Fetch the candidate (read-only, cost-bounded)

License cleared → fetch only the skill, reusing `commands/research.md` §2's source-read discipline **verbatim** (referenced, not re-derived, so the two never drift): shallow + ref-pinned + path-scoped + read-only.

- `git clone --depth 1 --branch <tag|branch> --filter=blob:none --sparse <url> "$WT_ABS/tmp/import-skill-src"` then `git -C "$WT_ABS/tmp/import-skill-src" sparse-checkout set <path/of/the/skill>` — shallow (`--depth 1`), pinned (`--branch`; a release tag is the stable pin, a commit SHA only when no tag fits), path-scoped (`--filter=blob:none --sparse` fetches only the targeted skill's blobs). Clone into `$WT_ABS/tmp/` — the worktree scratch dir convention 5 sanctions for an isolated session; never the shared checkout.
- **Read-only, never execute.** `git clone` runs no repo-provided hooks, so reading is the whole interaction: `Read`/`Grep` the scoped files only — the `SKILL.md` / command `.md` + any one-level-deep references it declares. No `npm install`, no build, no scripts. The security surface stays bounded to file reads of a size-capped tree.
- **Cost bound** (research.md §55): one repo, the one skill path, a handful of files (~5–10 / a few hundred KB) — the artifact the call turns on, not a directory sweep. Delete `$WT_ABS/tmp/import-skill-src` when the read is done.

## 3. Gate 2 — format conformance (mechanical)

Does the candidate match a shape we can actually load — a Claude Code skill or a slash-command? Check against the Agent Skills standard (the format-of-record; `anthropics/skills` is the reference):

- **Skill shape:** a `SKILL.md` with YAML frontmatter — `name` (≤64 chars, lowercase/hyphens), `description` (≤1024 chars, **third person**, stating *what it does + when to use it*), a markdown body, and any reference files **one level deep** (progressive disclosure).
- **Slash-command shape (our `commands/*.md`):** frontmatter `description` + `argument-hint` + `allowed-tools`, body = the procedure.
- Score each: present / malformed / missing. A candidate that is neither shape (a bare prompt dump, a README masquerading as a skill) **fails** format conformance — it would need restructuring before it could even be loaded, which pushes the verdict toward `build-fresh` or a heavy `adapt`.

Record the format evidence as concrete facts from the file read (`frontmatter.description is first-person and 1400 chars`), not impressions.

## 4. Gate 3 — craft-fit (the judgment call, grounded in craft/)

The instinct here is to wave a popular, polished skill through — resist it: polish is not our craft standard. Hold the candidate against the **five `skill-creator` authoring conventions** (the canonical list lives in `craft/README.md` "Authoring conventions"; `craft/authoring.md` is how to *apply* and *revise* against each one — cite README for the rule, authoring.md for the application):

1. **Explains the why** behind its rules, rather than bare directives.
2. **Body under ~500 lines**, depth pushed to on-demand references — not a monolith.
3. **Metadata drives invocation** — the description says what it's *for* and *when*; the body is the procedure.
4. **Progressive disclosure** — a read-first index pointing to detail loaded only when relevant.
5. **No all-caps `ALWAYS`/`NEVER` shouting** — a rule that stopped explaining itself.

Then hold it against `craft/judgment.md`'s `## Constraints` + `## Anti-Patterns` as the self-critique rail: does the candidate carry **ceremony** (steps that look rigorous and carry no load), **scope creep**, or rules without their why? Name *which* convention or anti-pattern each finding trips — diagnostic "why this feels off," not "seems weak."

A candidate that already meets the bar is rare (it was authored to someone else's standard, not ours); the common outcome is "good bones, needs rewriting to our register" → **adapt**.

## 5. The verdict (rubric-scored, cited)

Combine the three gates into one decisive call. Surface the full block — never collapse to the bare word:

```
## Import verdict: <owner/repo[/path][@tag]>
Verdict: import | adapt | build-fresh
Gates:
- License: <SPDX> — <pass: permissive | flag: copyleft obligation | fail: source-available/none>
- Format:  <pass | malformed: what | missing: what>  (skill | slash-command | neither)
- Craft-fit: <pass | adapt-needed: which of the 5 conventions / which anti-pattern> — cite craft/
Rationale: <one line tying the call to the gate that decided it>
```

The decision rule, in order:
- **License fails** → `build-fresh` (take the idea, not the code) — nothing downstream matters.
- **License passes/flags, format + craft-fit both pass as-is** → `import` (rare; cite that it already meets our bar).
- **License passes/flags, but format or craft-fit needs rework** → `adapt` (good shape, must be rewritten to our standard) → §6.
- **The gap to our standard exceeds the cost of writing it fresh** (a heavy rewrite that keeps little of the original) → `build-fresh`, and say *why nothing imported cleanly*.

Every gate cites its evidence: the SPDX id from the real `gh`/`LICENSE` response (convention 8 — never invented), concrete format facts from the file read, and the `craft/` line each craft-fit finding trips.

## 6. Draft the adapted skill (adapt verdict only)

For an `adapt` verdict, produce a **draft** — the rewrite-to-our-standard, not the original — so a human can review the actual artifact, not a promise of one:

- Write it to `$WT_ABS/tmp/import-skill-draft/<name>/` (scratch, never `commands/` — importing is load-bearing and the human approves the install, per `/review-claude-md`'s propose-don't-silently-write discipline). Use our shape: a `commands/<name>.md` with `description` + `argument-hint` + `allowed-tools` frontmatter and a read-first line to `workflow-conventions.md` (+ `craft/` where it exercises judgment), or a `SKILL.md` if a skill is the better fit.
- Apply `craft/authoring.md`'s rewrite moves: attach the missing why to each bare directive, push depth out of an over-long body, move the trigger into metadata, reframe any all-caps shouting into a reasoned constraint, and cut any ceremony the original carried.
- Print the draft path and a short diff-of-intent (what changed from the original to meet our standard, and why). The human reviews, then moves it into place — this command does not.

## Hard rules

- **Read-only on the external repo.** `Read`/`Grep` the sparse-checked path only, then delete the temp clone; never run anything from it (`git clone` runs no hooks — reading is the whole interaction).
- **License gate first, before any fetch.** A source-available/unlicensed candidate is never cloned; a copyleft one carries its obligation into the verdict.
- **Draft, never install.** The verdict and any adapted draft are for human approval; this command never writes into `commands/` or otherwise installs a skill (load-bearing-context discipline, mirroring `/review-claude-md`).
- **Every gate cites real evidence** — the SPDX id from the actual response, format facts from the file read, the `craft/` line behind each craft-fit finding (convention 8; never fabricate an identifier or a verdict).
- **Model the bar it enforces** — keep this command's own body concise, every rule carrying its why, no all-caps shouting (`craft/authoring.md`'s commit-test applied to itself).
- Convention 4: name the next step on exit — re-run on another candidate, or (for an `adapt` draft) review the scratch draft and move it into `commands/` if it passes.
