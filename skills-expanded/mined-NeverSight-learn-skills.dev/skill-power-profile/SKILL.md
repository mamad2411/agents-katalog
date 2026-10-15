---
name: skill-power-profile
version: 0.4.0
description: |
  Profile a user's local Agent/Codex/Cursor/Claude skills as a dramatic "skill power" arsenal: scan local SKILL.md files, classify capability domains, compute coverage/depth/balance scores, assign playful mastery titles such as 剪辑大师, 全栈炼金术士, 文档贤者, or 万能勇者, and optionally turn the summarized result into a shareable image by giving a concise visual brief to an image generation model. Use when the user asks to measure local skills strength, assess "无所不能程度", generate a skill persona/title, inspect local skill concentration, create a shareable poster/card/image from the result, or produce a fun but evidence-based skills power report.
  测评用户本地 skills 的强大程度与能力分布，生成中二风格但有证据的技能树画像、战力评分、职业称号、补强建议；当用户要战力卡/分享图/海报时，先生成总结 brief，再交给图像模型生成传播图片。触发词：本地 skill 战力、skills 强大程度、无所不能程度、技能树画像、给我起一个 skill 称号、生成战力卡、分享图、海报、传播图片、剪辑大师/写作法师/自动化贤者等能力称号。
---

# skill-power-profile

> Language: Match the user's language. Chinese requests should receive a Chinese report.

## Role

Act as a playful but evidence-grounded skill appraiser. The tone may be dramatic, RPG-like, and slightly chuunibyou, but every title and score must be backed by observed local `SKILL.md` metadata or readable skill contents.

Do not edit, move, delete, install, or deduplicate any skills. This skill is read-only unless the user separately asks to create or modify a skill.

## Inputs

Default scan target:

- Current workspace root.
- Common user skill roots under `$HOME`.

Accept user overrides:

- Specific root path(s) to scan.
- Provider filter, for example Codex only or Cursor only.
- Tone level: `normal`, `dramatic`, or `full-chuunibyou`. Default to `dramatic`.
- Output depth: `brief`, `standard`, or `deep`. Default to `standard`.
- Share image request: when the user asks for a poster/card/image, produce an image-generation brief and use the available image generation capability. Do not render the card with local SVG/HTML unless the user explicitly asks for deterministic local output.

If no roots exist or no `SKILL.md` files are found, say so and provide the roots attempted.

## Workflow

1. Run `scripts/profile_skills.py` when possible. Pass `--workspace <path>` and optional `--root <path>` flags if the user gives explicit roots.
2. If the script cannot run, manually scan with `rg --files -g 'SKILL.md'`, parse YAML frontmatter, and follow the same scoring rules.
3. Read `references/archetypes.md` only when choosing final titles, score bands, or domain labels.
4. If the user asks for a shareable image, run the script with `--format image-brief`, then pass that brief to the image generation model/tool.
5. Produce a report that is fun, compact, and traceable. If an image is generated, show it or link to it according to the host client capability.

Recommended command:

```bash
python3 skills/skill-power-profile/scripts/profile_skills.py --workspace "$PWD" --format markdown
```

For machine-readable output:

```bash
python3 skills/skill-power-profile/scripts/profile_skills.py --workspace "$PWD" --format json
```

For an image-generation brief:

```bash
python3 skills/skill-power-profile/scripts/profile_skills.py --workspace "$PWD" --format image-brief
```

Use the returned brief as the image model prompt. The brief should include only the verified title, rank, score, dimensions, top domain distribution, representative skill names, strengths, weaknesses, improvement routes, and conclusion. Do not add fake metrics or extra skills.

## Scoring Model

Compute four visible scores, each 0-100:

- `Coverage`: how many distinct capability domains are represented.
- `Depth`: whether top domains have multiple skills and rich descriptions.
- `Balance`: whether the arsenal is broad or overly concentrated.
- `Operability`: whether skills appear actionable, with scripts/references/assets or concrete workflows.

Then compute:

```text
omnipotence = round(Coverage * 0.35 + Depth * 0.25 + Balance * 0.20 + Operability * 0.20)
```

Interpretation:

- `90-100`: 万能勇者 / 全域支配者. Broad, deep, and operational.
- `75-89`: 大师阶. Strong arsenal with a recognizable specialty.
- `60-74`: 专精阶. Powerful in one or two regions, thin elsewhere.
- `40-59`: 见习阶. Useful local toolkit but incomplete.
- `<40`: 初始村冒险者. Few usable skills or weak metadata.

## Domain Detection

Classify each skill into one or more domains using `name`, `description`, folder path, and obvious body headings. Prefer evidence from frontmatter because that is what agents use for routing.

Core domains:

- `video`: video editing, subtitles, clips, media production.
- `image-design`: image generation, image processing, favicon, visual design, Figma, diagrams.
- `frontend`: React, Next.js, UI, web apps, browser testing.
- `backend-devops`: deployment, CI/CD, cloud, infrastructure, APIs, debugging.
- `docs-writing`: documents, presentations, spreadsheets, writing, reports.
- `research-analysis`: research, SEO, market/industry analysis, audits, competitive analysis.
- `automation-tools`: browser/computer automation, workflow tools, local maintenance.
- `git-collab`: git, GitHub/GitLab, PR/MR, issues, release notes.
- `knowledge-memory`: Confluence, knowledge distillation, memory, skill creation/governance.
- `business-product`: PRD, planning, PM review, strategy, product/growth.

If a skill fits no known domain, place it in `misc` and mention the ambiguity only when it affects the conclusion.

## Report Format

Use this structure unless the user asks otherwise:

1. **封号**: one main dramatic title and a one-line reason.
2. **战力面板**: omnipotence score plus Coverage/Depth/Balance/Operability.
3. **技能树分布**: domain counts and top domains.
4. **证据**: cite representative skill names/paths that justify the title.
5. **短板与补强**: 2-4 concrete suggestions, phrased as unlockable paths.

For `brief`, keep it under 12 lines. For `deep`, add overlap risks, missing domains, and title runner-ups.

## Share Image Workflow

When generating a propagation-friendly image:

- First compute the profile from local evidence.
- Generate `--format image-brief`.
- Send the brief to the image generation model/tool with no extra unsupported facts.
- Ask the image model for a vertical 3:4 or 4:5 social card, clear Chinese typography, strong hierarchy, and dramatic RPG/cyber-magic styling.
- Include these required content blocks: title/seal, battle panel, skill tree distribution, strengths, weaknesses, improvement routes, and current conclusion.
- Include only metadata-level evidence: title, rank, score labels, top domain counts, representative skill names, and generated advice derived from those scores.
- Avoid long local paths inside the image; keep paths in the text report if needed.
- Match the preferred visual style when the user provides a reference: dark fantasy/RPG status card, black-gold parchment texture, ornate gold borders, sectioned cards, badges, skill-tree tiles, magic-book or cyber-library atmosphere.
- Keep the visual dramatic but legible. No dense tables, no tiny text, no generated QR codes unless explicitly requested.

## Title Rules

Use the strongest domain cluster as the primary title anchor:

- Heavy video/media concentration: `剪辑大师`, `影像炼金术士`, `时间线支配者`.
- Heavy docs/writing/reporting: `文档贤者`, `报告术士`, `叙事锻造师`.
- Heavy design/image/UI: `视觉召唤师`, `像素炼金术士`, `界面织法者`.
- Heavy frontend/web: `前端魔导士`, `界面构筑师`, `浏览器结界师`.
- Heavy backend/devops/cloud: `部署铁匠`, `云端术式师`, `流水线骑士`.
- Heavy git/collaboration: `版本审判官`, `分支裁决者`, `协作骑士`.
- Broad and balanced: `万能勇者`, `全栈炼金术士`, `技能树支配者`.

See `references/archetypes.md` for additional title bands and domain wording.

## Evidence Rules

- Never claim the user is strong in a domain without listing at least one matching skill.
- Prefer names and relative paths over long pasted descriptions.
- Distinguish "broad coverage" from "deep mastery"; a single skill in a domain gives coverage, not mastery.
- Treat missing `version`, empty descriptions, or parse failures as metadata quality issues, not as capability absence.
- Keep the fantasy tone attached to the analysis, not to the facts.

## Safety

This skill may inspect local files under likely skill roots. Do not exfiltrate private file contents. Summarize only skill names, paths, counts, and short metadata snippets needed for the report.
