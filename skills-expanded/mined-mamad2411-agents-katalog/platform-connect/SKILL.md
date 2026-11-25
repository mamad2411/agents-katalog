---
name: platform-connect
description: Adapts a pasted article, TXT, Markdown, Word, PDF, HTML file, or article URL into a fact-preserving brief, 2–3 platform recommendations when targets are unspecified, platform-native copy, approved visual assets, and an outcome-first offline delivery board. Use when the user asks to repurpose, localize, rewrite, script, illustrate, or package an article for Chinese or overseas social platforms including Xiaohongshu, Douyin, WeChat, Bilibili, TikTok, YouTube, Instagram, Facebook, LinkedIn, X, Threads, Pinterest, and Snapchat.
---

# Platform Connect

Turn one source article into selected platform-native content packages without changing its factual claims or author stance. Accept the source directly; do not require a specially formatted prompt.

## Output scopes

- `plan`: create the shared brief, platform strategy, visual-direction proposal, and proposed asset list. Stop at a plan-review gate; do not draft final copy or generate images.
- `copy`: create the shared brief and platform copy without visual work.
- `full`: create the brief, platform copy, visual assets, QA, and delivery package.

Infer `full` only when the user explicitly requests images or delegates the image decision through a saved profile. Otherwise use `copy`.

## Review policies

Read [interaction-policy.md](references/interaction-policy.md) before choosing a policy.

- `compact` is the default. Present one combined review packet containing the brief, platform assumptions, copy drafts, and—only for `full`—visual direction and asset plan. Accept one reply that approves or revises the whole packet.
- `strict` uses separate copy, image-intent, visual-direction, and asset-manifest gates. Use it when the user asks for step-by-step control or the content has material factual, brand, legal, medical, financial, identity, or safety risk.
- `autopilot` completes the run without intermediate review only when the user explicitly says to proceed without confirmation or a user-authored profile grants equivalent authority. Never infer permission to generate images.

Keep output scope and review policy independent. Record both in the manifest.

## Required flow

1. Read [source-intake.md](references/source-intake.md), identify the input type, and read the entire source before drafting. Use the host document, PDF, web, or browser capability that matches the input.
2. Build one shared content brief using [content-brief-schema.md](references/content-brief-schema.md). Treat it as the factual baseline for every downstream output.
3. If `platform-connect.profile.json` exists in the working directory, read it as a user-authored default profile. Resolve platforms, language, market, image intent, and review policy from the request or profile, with the current request taking precedence.
4. If platforms are unspecified, apply [interaction-policy.md](references/interaction-policy.md): recommend two platforms by default and at most three, prefer a useful domestic and overseas mix, and include a preliminary article-specific visual direction for each. Ask once for platform choice, image intent, and whether to review or complete directly. Do not draft every candidate before selection.
5. Ask one consolidated blocking question only when missing information would materially change factual accuracy, localization, brand safety, source completeness, or image authorization. Keep the source language when localization is not requested. For an unlisted platform, ask for its format and audience unless the user delegates a provisional adapter.
6. Read only the selected platform entries in [platform-adapters.md](references/platform-adapters.md).
7. In `plan`, produce strategy, visual directions, and a proposed asset list, then apply the selected review policy without drafting final copy or generating images.
8. In `copy` or `full`, generate visibly different platform versions from the shared brief. Present every version as editable.
9. For `full`, read [visual-handoff.md](references/visual-handoff.md) and the relevant industry entry in [industry-visual-routing.md](references/industry-visual-routing.md). Recommend 3–4 article-specific directions with editable prompts, plus `自定义提示词` as an equal option, then create the editable asset manifest using [output-schema.md](references/output-schema.md).
10. Apply the review policy: use one combined approval in `compact`, separate gates in `strict`, or recorded preauthorization in `autopilot`. Treat requested revisions as replacing approval for the affected decision.
11. Generate no image unless `image_intent` is `yes` and its provenance is explicit, bundled, profile-based, or preauthorized. Never use inferred image consent.
12. After authorization, use the available image-generation tool once per distinct asset. Inspect every output, apply the QA checklist in [visual-handoff.md](references/visual-handoff.md), and change one variable at a time when revising.
13. When filesystem output is requested, follow the deterministic delivery loop below. Create a new immutable run directory for every revision; never overwrite a prior approved run.
14. Render the bundled offline showcase from the completed run. Make final copy and ready images the primary content; keep recommendations, decisions, and execution trace secondary or collapsed. Treat the board as a read-only delivery report, not a control surface or a separate AI application.

## Non-negotiable boundaries

- Preserve names, numbers, dates, causal claims, quotations, examples, and the author's stated position.
- Do not claim the source was completely read when a file, page, OCR passage, or URL body is missing.
- Do not invent evidence, success claims, credentials, product capabilities, or platform rules.
- Adapt the angle, opening, pacing, structure, duration, CTA, and packaging—not the underlying facts.
- Mark unclear source claims for human review instead of silently repairing them.
- Localize for language and market context; do not perform mechanical sentence-by-sentence translation.
- Preserve separate decision records for copy, image intent, visual direction, and asset manifest even when one bundled reply or preauthorization resolves several of them.
- Never infer image consent. Accept it only from an explicit request, a combined user approval, an explicit no-confirmation authorization, or a user-authored profile.
- Let unresolved high-risk ambiguity override `compact` or `autopilot` and stop for clarification.
- Recommend visual directions from the actual article's subject, audience, industry, and communication job. Do not offer generic style labels without an article-specific rationale and editable prompt.
- A user-written custom prompt is a first-class visual direction. Keep it editable, record it in the manifest, and reconcile it with factual invariants instead of replacing it wholesale.
- Route the visual plan through the source article's industry and communication job; industry determines factual risks and visual vocabulary, not a fixed aesthetic.
- Treat Xiaohei as one optional visual preset, not the product's default identity or industry scope.
- Do not make the final board look interactive in ways that imply platform selection, approval, or image generation. Board interactions may only switch, filter, copy, preview, or open delivered results.

## Output order

For `copy` and `full`, return results in this order:

1. content brief;
2. selected or recommended platforms, locale assumptions, and decision provenance;
3. one copy package per platform;
4. factual or editorial review flags;
5. for `full`, visual directions and the proposed asset list;
6. one next action appropriate to the review policy.

Keep platform labels explicit. Do not merge several platform scripts into one generic version.

When platforms were unspecified, return the recommendation packet before this output order. After the user chooses, continue from item 1 without asking them to repeat the article.

In `compact`, make the next action one combined approval or one consolidated revision. In `autopilot`, proceed to final delivery without requesting a reply unless a blocking ambiguity appears. In `strict`, expose only the current gate.

## Runtime and deterministic delivery

Require Python 3.10 or newer. The scripts use only the Python standard library. The offline showcase has no package, CDN, network, React, or FastAPI dependency. Use the image-generation capability available in the host environment; do not assume a named provider.

Execute these scripts for file operations; do not manually recreate their behavior:

- `scripts/prepare_workspace.py <slug> --platforms ... --review-policy ...` creates an immutable versioned run directory and starter manifest.
- `scripts/validate_manifest.py <manifest.json>` validates required fields, platform selection, duplicate assets, ratios, and approval state.
- `scripts/build_delivery_index.py <manifest.json>` builds a Markdown delivery index after assets and copy paths are recorded.
- `scripts/render_showcase.py <manifest.json>` renders the bundled offline execution showcase.
- `scripts/validate_showcase.py <showcase-dir>` checks the rendered showcase contract and offline constraints.

Run scripts from the repository or skill consumer's working directory. Use `--root` to choose a different output root.

Follow this delivery loop:

1. Run `prepare_workspace.py` after platform selection.
2. Write the brief, copy packages, decisions, asset plan, and review flags into the run.
3. Run `validate_manifest.py`.
4. If validation fails, fix the manifest or source files and rerun validation. Do not continue from an invalid run.
5. After validation passes, run `render_showcase.py`, then `validate_showcase.py`.
6. If showcase validation fails, fix the manifest, display data, or source template and rerender. Do not patch generated HTML as the source of truth.
7. Run `build_delivery_index.py` only after the manifest and showcase pass.

Treat nonzero exit codes and JSON with `"status": "failed"` as blocking. Report the error and preserve the failed run for diagnosis; start a child run for any approved revision.

## Reference routing

- Always read [content-brief-schema.md](references/content-brief-schema.md) before creating the shared brief.
- Always read [source-intake.md](references/source-intake.md) before extracting an attached file, pasted article, or URL.
- Always read [interaction-policy.md](references/interaction-policy.md) before choosing review cadence, inferring platforms, or recording bundled or preauthorized decisions.
- Search [platform-adapters.md](references/platform-adapters.md) by its exact `##` heading and read only the selected platform sections plus Cross-platform QA.
- Read [visual-handoff.md](references/visual-handoff.md) only for `plan` visual proposals or after image intent is `yes`.
- Read [output-schema.md](references/output-schema.md) before creating or validating a filesystem delivery package.
- Search [industry-visual-routing.md](references/industry-visual-routing.md) by its exact `##` heading and read only the relevant industry sections.
- Read [open-source-visual-research.md](references/open-source-visual-research.md) when maintaining the prompt schema or adding visual categories.
- Read [third-party-notices.md](references/third-party-notices.md) before using, adapting, or distributing Xiaohei-derived rules, prompts, or examples.
