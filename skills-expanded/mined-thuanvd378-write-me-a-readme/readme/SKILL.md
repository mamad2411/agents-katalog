---
name: readme
description: Create, redesign, audit, or update a repository README.md by inspecting the actual project; write accurate setup and usage guidance with a selectable brand voice, polished information architecture, evidence-based badges and claims, discoverability suggestions, and an optional editable SVG/PNG banner. Use when the user asks for a README, README refresh or audit, repository landing page, GitHub presentation or SEO improvement, tone/style rewrite, social preview, or README banner. Do not use for unrelated documentation or generic marketing copy.
---

# Write Me a README

Create a trustworthy repository front page from project evidence. Write for a new visitor who must understand the value, verify the fit, and reach a working first result quickly.

Resolve every bundled path relative to this `SKILL.md`. Run scripts with the current Python interpreter; do not assume the skill is installed at a fixed global path.

## Operating contract

- Produce or update `README.md` in the target project unless the user requests audit-only output.
- Inspect before writing. Treat source files, manifests, tests, CI, examples, existing docs, and user statements as evidence in that order.
- Never invent commands, compatibility, performance, adoption, maintainers, security posture, or production readiness.
- Never copy prose, slogans, banners, or layouts from another repository. Learn patterns, then create original content and visuals.
- Preserve useful existing material, deliberate terminology, status warnings, legal notices, and user-authored sections.
- Keep source-code changes out of scope. Add only README-related files unless the user explicitly expands the task.
- Do not promise search ranking, GitHub Trending placement, virality, or adoption. Optimize discoverability, comprehension, conversion, and trust.
- Prefer a complete first pass over blocking questions. Ask only when a missing choice would materially change the result and cannot be inferred safely.

## 1. Establish scope

Infer these choices from the request and repository:

- **Mode:** create, refresh, redesign, translate, or audit-only.
- **Audience:** end user, library consumer, operator, contributor, learner, or mixed.
- **Language:** preserve the established README language; otherwise use the dominant project-doc language; otherwise default to English.
- **Voice:** honor an explicit style request; otherwise infer the established brand voice and default to confident-friendly. Use one primary profile plus at most one modifier, such as `professional + warm` or `playful + concise`.
- **Visuals:** generate a banner for a new README by default. Keep an existing high-quality branded hero unless replacement is requested. Honor text-only requests.
- **Depth:** keep a small tool concise; move extensive concepts, API reference, and contributor internals to existing or new `docs/` pages only when needed.

State any consequential inference briefly while working. Do not add an “assumptions” section to the README unless readers need it.

Read [voice-and-style.md](references/voice-and-style.md) when the user names a tone, asks for marketing-oriented copy, the repository has a recognizable brand voice, or the existing README feels stiff or inconsistent. Lock a lightweight style brief before drafting. Let voice change how verified facts are expressed, never which facts are claimed.

## 2. Inspect the project

Run the deterministic inventory first:

```text
python <skill-root>/scripts/inspect_project.py --root <project-root> --format json
```

Then read the small set of first-party files that can confirm the README:

1. Existing README variants and status notices.
2. Package/build manifests and lockfiles.
3. CLI entry points, public API exports, example code, and configuration examples.
4. Tests and CI workflows that reveal supported commands and platforms.
5. License, contribution, security, code-of-conduct, and citation files.
6. Documentation index, deployment files, and screenshots.

Do not open secret-bearing files such as `.env`; inspect `.env.example` only. Ignore vendored dependencies, generated builds, caches, and binaries.

Build a scratch evidence ledger with `claim`, `evidence path`, and `confidence`. Omit claims without evidence. Mark user-provided facts separately when the repository cannot verify them.

Classify the project as one primary archetype: library/SDK, CLI/tool, application/platform, service/API, collection/curriculum, template/starter, or monorepo. Read [readme-patterns.md](references/readme-patterns.md) and select only sections useful to that archetype.

## 3. Design the information path

Make the first screen answer, in order:

1. Is the project active, deprecated, experimental, or migrating?
2. What is it, who is it for, and what verified outcome does it enable?
3. Where can the reader try it, read docs, or get started?
4. What is the shortest verified path to a first success?

Use this default flow, removing irrelevant sections:

```text
status notice → banner → text H1 → one-sentence positioning → CTA links
→ purposeful badges → demo or minimal example → quickstart → key capabilities
→ how it works → configuration/deployment → limitations → support
→ contributing → security → license/maintainers
```

Keep the text H1 and essential tagline outside the banner for accessibility and search. Do not create a manual table of contents for a short README; GitHub already provides an outline.

Write a Quickstart that includes prerequisites, install, minimal configuration, run, and a visible success condition. Keep user installation separate from contributor development setup. Run safe existing checks where practical; if a command cannot be verified, use only syntax directly supported by project evidence and disclose the verification gap in the handoff, not as marketing copy.

## 4. Create visual assets

Read [banner-design.md](references/banner-design.md) and [asset-licensing.md](references/asset-licensing.md) whenever generating or replacing a banner.

Default to the `minimal-center` composition: one full-bleed background, baked blur, one readability scrim, the project name centered, and an optional short subtitle. Do not add a card, pattern, kicker, badge, footer label, fake logo, or decorative UI chrome unless the user explicitly asks for a different direction. Prefer title only; keep a subtitle only when it adds a verified category, audience, or outcome.

Choose the visual source in this order: project-owned asset or screenshot, official first-party media, a clearly licensed contextual image, then the deterministic gradient fallback. When a contextual photograph or texture materially improves the design:

1. Use an available image-search tool or the bundled Wikimedia Commons client.
2. Search concrete subjects tied to the project rather than generic technology imagery.
3. Open or download the best 3-6 candidates and inspect the actual images and likely banner crop; never choose from filenames or snippets alone when a visual tool is available.
4. Confirm the selected file page, author, license, restrictions, and resolution.
5. Default to public-domain/CC0 media. Use CC BY only with attribution. Do not use ShareAlike, non-free, restricted, logo, or identifiable-person media without an explicit decision.
6. Save the source record and attribution beside the generated assets.

Before rendering PNG or social-preview assets, verify Pillow is available with `python -c "from PIL import Image"`. If it is missing, ask permission to run `python -m pip install -r <skill-root>/requirements.txt`; keep text-only and audit-only workflows dependency-free.

Search or download a license-aware Commons candidate with:

```text
python <skill-root>/scripts/fetch_commons.py search "<visual subject>" --limit 8
python <skill-root>/scripts/fetch_commons.py download "<visual subject>" --output <asset-dir>/source.jpg --provenance <asset-dir>/image-sources.json
```

Generate a self-contained editable SVG, a raster fallback, and a GitHub social preview:

```text
python <skill-root>/scripts/banner.py --title "<project name>" --subtitle "<optional verified tagline>" --layout minimal-center --theme <theme> --svg <asset-dir>/banner.svg --png <asset-dir>/banner.png --social <asset-dir>/social-preview.png
```

Add `--source <licensed-image> --anchor <focal-anchor> --blur <10-18>` only after completing the license checks. Omit `--subtitle` when the name is strong enough alone. Use the explicit `left` layout only for an intentionally busier launch/editorial banner or to preserve an existing identity. Use `assets/readme/` in the target project unless its existing asset convention is clearer. Commit `image-sources.json` and an attribution file whenever license terms require them.

Embed the banner with a relative path and useful alt text. Do not put status, compatibility, or other essential information only inside an image.

## 5. Draft evidence-based copy

- Apply the selected voice consistently to headings, positioning, feature framing, transitions, and calls to action. Keep install commands, warnings, limitations, security guidance, and legal text unambiguous even in playful styles.
- Lead with category + audience + outcome. Use active voice and concrete verbs.
- Explain the reader's problem before listing implementation details.
- Express features as capability + benefit + evidence or example.
- Use “open source”, “local-first”, “self-hosted”, “production-ready”, “fastest”, or “best” only when the repository and license actually support the claim.
- Qualify benchmark and adoption numbers with scope, method, source, and date.
- Distinguish the open-source package from any hosted or paid offering.
- Add known limitations or fit boundaries when they affect adoption.
- Keep badges to a small useful set. Each badge must resolve to a real package, workflow, license, docs page, or community destination.
- Prefer relative links for repository files and assets.

For discoverability or “SEO/trending” requests, read [seo-discovery.md](references/seo-discovery.md). Include natural category and ecosystem terms, then report suggested repository description, topics, and the generated social-preview path in the handoff. Do not change remote repository settings without explicit authorization.

## 6. Validate and refine

Read [quality-rubric.md](references/quality-rubric.md), then run:

```text
python <skill-root>/scripts/validate_readme.py --root <project-root> --readme README.md --format text --strict
```

Fix every error and review warnings. Also:

- Render or inspect the generated PNG/SVG at full width and a narrow mobile width when a visual tool is available.
- Check title wrapping, safe margins, contrast, crop focus, spelling, and asset size.
- Confirm local relative links and images exist with exact case.
- Re-run the shortest safe Quickstart or project check that validates the documented path.
- Review the final diff for accidental source changes, placeholders, stale sections, copied wording, and unsupported claims.

Finish with a concise handoff listing the README and visual assets created, checks run, any command not executed, attribution obligations, and optional repository description/topics. Do not claim the README is “SEO optimized” or “trending-ready” without qualifying what was actually improved.

## Reference map

- Read [readme-patterns.md](references/readme-patterns.md) for archetypes, section choices, wording, badges, and anti-patterns.
- Read [voice-and-style.md](references/voice-and-style.md) for voice profiles, prompt patterns, copy transformations, and humor guardrails.
- Read [quality-rubric.md](references/quality-rubric.md) before final validation.
- Read [seo-discovery.md](references/seo-discovery.md) for repository search, topics, metadata, and social-preview guidance.
- Read [banner-design.md](references/banner-design.md) for the SVG/PNG visual system and QA rules.
- Read [asset-licensing.md](references/asset-licensing.md) before using any third-party image, font, logo, or copied material.
- Read [research-sources.md](references/research-sources.md) only when design precedent or research provenance is useful. Treat it as pattern evidence, never as a copy library.
