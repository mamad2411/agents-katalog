---
name: create-alignment-page
description: Create or amend a portable HTML alignment review page in a target repo using bundled conventions and skillpacks alignment commands
type: ops
version: v0.3
required_conventions: [alignment-page]
argument-hint: "<skill-or-topic> [target artifact or repo path]"
---

# Create Alignment Page

Invoke as `$create-alignment-page`.

Use this skill when the user asks to create, refresh, or amend an `alignment/*.html` review page for an existing skill output, research artifact, spec, plan, report, prototype, or other durable deliverable. This skill is for target repositories that may only have skills installed through the `skillpacks` npm package, so it must not assume this source checkout's `docs/` or `scripts/` directories are present.

## Workflow

1. Resolve the target repository and page scope:
   - Default to the current working directory.
   - Identify the source artifact(s), producing skill name, topic slug, and intended page path `alignment/<skill-name>-<topic>.html`.
   - Confirm the page path is repo-relative, directly under `alignment/`, and ends in `.html`.
   - If amending an existing page, read the whole current page and archive it before replacing it.

2. Load the best available convention:
   - First read the producing skill's bundled sibling `ALIGNMENT-PAGE.md` from the installed skill directory, such as `.codex/skills/<skill>/ALIGNMENT-PAGE.md` or `.claude/skills/<skill>/ALIGNMENT-PAGE.md`.
   - For ad hoc pages that are not owned by a normal producing skill, create the starter file with `npx skillpacks alignment pages scaffold <skill> <topic> --out alignment/<skill>-<topic>.html`, then replace every placeholder with the actual artifact, evidence, gates, and compiler content before handoff.
   - In this source checkout or a package-shaped checkout with `docs/`, `base/`, and `packs/`, source paths such as `base/<agent>/<skill>/ALIGNMENT-PAGE.md`, `packs/<pack>/<agent>/<skill>/ALIGNMENT-PAGE.md`, `docs/alignment-page-convention.md`, and `node scripts/upgrade-alignment-page.mjs --check` are acceptable maintenance fallbacks.
   - `npx skillpacks alignment bundles --check` is a source/package maintenance check for repositories that contain the packaged convention inputs (`docs/`, `base/`, and `packs/`). Do not use it as a bare target-repo fallback.
   - If a normal producing skill should own the page but no installed sibling `ALIGNMENT-PAGE.md` or valid source/package-shaped convention source exists, stop and report which skill convention is missing. Do not route that normal skill invocation through `create-alignment-page`; the scaffold is infrastructure, not a replacement for skill-owned gates.

3. Build or amend the page:
   - For a new ad hoc page, run the scaffold command before filling the page. If the target page already exists, archive it first and amend the archived-derived page manually rather than rerunning scaffold over it.
   - Render the full source artifact content directly in HTML. Do not replace the deliverable with an iframe, object embed, or link-only preview.
   - Preserve evidence, assumptions, decisions, source paths, proposed file changes, gate questions, feedback context, and prior approval records.
   - For a new review page, set `data-alignment-status="review"`, `data-alignment-category`, and `data-visual-tier`.
   - For an amended page, archive the previous page under `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/<filename>.html`, show what changed, and regenerate affected gates from the amended content.
   - Include the TTS script tag `<script src="../scripts/alignment-tts-kokoro.js"></script>` before `</body>`.

4. Verify and make the page portable:
   - Run `npx skillpacks alignment pages inject-tts alignment/<page>.html` so the packaged TTS asset is installed when missing and the page tag is current.
   - Run `npx skillpacks alignment pages audit`.
   - Attempt to open the page with `npx skillpacks alignment pages open alignment/<page>.html --browser auto`.
   - In this source checkout only, if `npx skillpacks` is unavailable, fall back to `node scripts/inject-tts.mjs alignment/<page>.html`, `node scripts/audit-alignment-pages.mjs`, and `node scripts/open-html-page.mjs alignment/<page>.html --browser auto`.
   - Treat browser-open status `blocked` as non-fatal when the page was written and audited successfully; report the absolute path.

5. Handoff:
   - If the page is in `review`, give a concrete handoff: ask the user to review `alignment/<skill-name>-<topic>.html`, use local `Compile Feedback YAML` under a section for targeted revision feedback or bottom `Compile Responses` for gate answers and final approval, then paste the YAML into the producing skill context, normally `$<producing-skill> ...` with the YAML included.
   - Treat section-feedback YAML, `feedback_status: revision-request`, partial response YAML, and any `approval_status: not-approved` YAML as a review/revision request. The receiving producing skill investigates, answers or pushes back when needed, amends the page or artifacts when warranted, and returns the page for renewed review.
   - Treat only final compiled response YAML with `approval_status: ready-for-agent-review` and no unresolved negative or clarification feedback as authorization to write or confirm approved canonical artifacts.
   - If the user is already consuming pasted YAML in a fresh session, do not recommend another context clear; continue through the current YAML handling path.
   - Do not route to downstream implementation until final compiled response YAML is approved and any approved canonical artifacts are written.

## Output

Report:

- Page path and source artifact path(s)
- Convention source used
- TTS injection result
- Audit command and result
- Browser-open status: `focused`, `opened`, `fallback-opened`, `blocked`, or `failed`
- Archive path when an existing page was amended
- Next review action or final confirmation status

## Constraints

- Do not assume repo-local `scripts/` or `docs/` exist outside this source checkout.
- Do not create or modify GitHub Actions workflows.
- Do not write outside the target repository.
- Do not overwrite an existing alignment page without archiving it first.
- Do not create a second alignment page merely to review the alignment page created by this skill; the requested page is the review artifact.
- Do not make ordinary skill invocations call this skill as a subskill; producing skills populate their own alignment pages directly, using the packaged scaffold/template only as infrastructure when useful.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/create-alignment-page-{topic}.html`.

## Default Shipping Contract

- Modified alignment pages, archive copies, index updates, and source artifacts are normal repo artifacts. Follow the target repo's shipping rules after verification.
- When operating in this `agentic-skills` repository, commit and push intended tracked changes on the primary branch before stopping unless the user explicitly says not to ship.
