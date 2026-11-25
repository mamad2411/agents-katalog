---
name: liuyishou
description: Help workers capture work proof, protect tacit judgment, and grow a personal career moat from day-to-day work. Use when the user wants to log work, review weekly progress, spot AI-compressible tasks, generate manager/performance/internal-mobility packs, or build a local-first record of their professional value. / 帮助员工基于日常工作沉淀个人护城河。适用于记录工作、生成周度复盘、识别容易被 AI 压缩的任务、导出绩效/转岗/撤离材料。
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "0.1.0"
  argument-hint: "[init|capture|weekly|moat|pack]"
  user-invocable: true
---

> **Language / 语言**: Follow the user's language. If the user writes in Chinese, respond in Chinese. If the user writes in English, respond in English.

# 留一手

`留一手` is a daily career-defense skill. It helps the user do real work, keep a private record of judgment and impact, and turn recent work into reusable career assets.

This skill is not for fabricating impact or sabotaging teammates. It is for:
- capturing real work proof
- preserving tacit knowledge before it disappears
- separating shareable output from private reasoning
- growing toward harder-to-replace work

## When To Use

Use this skill when the user wants to:
- initialize a personal career-defense workspace
- capture a recent piece of work in 30-60 seconds
- produce a weekly defense review
- assess whether recent work is growing or shrinking their moat
- export manager updates, performance bullets, mobility packs, or exit packs

## Storage Model

By default, the skill stores user data under `.liuyishou/` in the current workspace.

Use `--root <path>` only when the user explicitly wants a custom location.

Generated files:
- `profile.json`
- `entries/*.json`
- `outputs/weekly/*.md`
- `outputs/moat/*.md`
- `outputs/packs/*.md`

Read [product-shape.md](./references/product-shape.md) when you need the product rationale.
Read [data-contract.md](./references/data-contract.md) when you need the exact file layout and field meanings.

## Command Map

All deterministic writes and exports should go through:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/liuyishou.py <subcommand> ...
```

If `CLAUDE_SKILL_DIR` is unavailable, resolve the script path relative to this `SKILL.md`.

### 1. `init`

Use when `.liuyishou/profile.json` does not exist yet, or the user wants a fresh setup.

Required fields:
- current role
- current work focus
- current goal

Optional fields:
- company or team alias
- level or years
- target roles
- soft skills to grow
- privacy boundary
- extra notes

Ask only for missing required fields. Do not force a long onboarding form.

Command pattern:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/liuyishou.py init \
  --root .liuyishou \
  --role "后端工程师" \
  --focus "支付与结算" \
  --goal "保住当前位置" \
  --company "某大厂" \
  --level "P6" \
  --target-role "技术负责人" \
  --soft-skill "跨团队推进" \
  --privacy-boundary "分享结果与流程，保留判断脉络和敏感上下文"
```

After running `init`, summarize the created profile in one short paragraph.

### 2. `capture`

Use when the user mentions a recent task, incident, launch, review, alignment, rescue, or decision.

Required inputs:
- what happened
- why it mattered

Optional inputs:
- impact
- evidence link
- stakeholders
- workstream
- tags
- private notes
- share level

Default behavior:
- if the user already gave enough detail, do not interrogate them
- if details are sparse, ask only for the two required fields
- keep capture fast

#### Signal assessment

Before calling the capture script, assess the entry using all available context (summary, importance, impact, private notes, the user's profile). Do not rely on keyword matching — use your judgment.

**Moat dimensions** — pick all that genuinely apply (comma-separated):
- `judgment`: the work required making tradeoffs, scoping decisions, prioritization, or risk assessment — not just executing a spec
- `influence`: the work required persuading people, aligning stakeholders, driving cross-team action, or resolving conflict
- `domain-context`: the work depended on knowledge only someone with lived experience would have — incident history, legacy quirks, edge cases, undocumented behavior
- `leverage`: the work produced something reusable — a tool, automation, template, or process — that amplifies future output
- `mobility`: the work demonstrates signals toward a next-level or adjacent role — mentoring, presenting, planning roadmaps, hiring
- `execution-only`: the work was straightforward execution with no meaningful judgment, influence, or domain depth — use this when none of the above apply

**AI compression risk** — pick one:
- `high`: an AI tool could do 80%+ of this work today (data reformatting, copy-pasting between systems, simple summarization, template-filling)
- `medium`: AI can assist but a human's judgment, taste, or context is still the bottleneck
- `low`: the work is deeply dependent on human judgment, interpersonal dynamics, organizational context, or domain intuition — AI cannot meaningfully replace it in the near term

**Share advice** — write one sentence of concrete guidance:
- Consider the share_level, whether private_notes contain sensitive content, and the user's privacy_boundary from their profile
- If content involves people-sensitive context (performance, politics, reorgs, interpersonal conflict), advise keeping dynamics private
- If the work is high AI-risk, advise highlighting the judgment and quality bar that made the work matter
- Otherwise, advise sharing the outcome and keeping the reasoning private

Pass your assessment via the `--moat-dimensions`, `--ai-risk`, and `--share-advice` flags.

Command pattern:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/liuyishou.py capture \
  --root .liuyishou \
  --summary "修复了结算对账的漏单问题" \
  --importance "避免月末人工兜底和客户投诉" \
  --impact "把人工排查时间从半天降到二十分钟" \
  --evidence "https://example.com/pr/123" \
  --stakeholder "财务" \
  --stakeholder "客服" \
  --workstream "结算稳定性" \
  --tag "incident" \
  --tag "cross-team" \
  --private-note "真正难点是历史订单状态不一致，公开材料里不要展开" \
  --share-level "manager" \
  --moat-dimensions "judgment,domain-context" \
  --ai-risk "low" \
  --share-advice "Share the fix outcome and timeline; keep the root cause analysis about legacy state inconsistency in your private vault."
```

After capture:
1. confirm what was stored
2. surface the moat signals in plain language — explain *why* you assigned each dimension and risk level
3. suggest one thing worth adding if the entry lacks evidence or judgment

### 3. `weekly`

Use when the user asks for:
- weekly review
- 周报
- 这周我做了什么
- 本周护城河复盘

Command pattern:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/liuyishou.py weekly --root .liuyishou --days 7
```

Then read the generated markdown and also read the entry files in `.liuyishou/entries/` for the same period.

Return:
- one short summary
- the top value proof from the week
- the top moat risk from the week
- the top 3 actions for next week

#### Rewriting next actions

The script generates placeholder next actions using simple rules. After reading the report and the raw entries, replace them with your own assessment. Consider:
- the user's profile (role, focus, goal, target roles)
- which moat dimensions are strong vs missing
- the AI compression risk mix — if too many entries are high-risk, suggest pulling toward harder-to-replace work
- what specific, actionable steps would improve the user's position next week
- each action should be distinct and concrete, not generic filler

Use the Edit tool to replace the `## Next Week Actions` section in the generated markdown file, then present the updated version to the user.

### 4. `moat`

Use when the user wants a broader 30-day assessment of replaceability, growth direction, or AI-compression risk.

Command pattern:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/liuyishou.py moat --root .liuyishou --days 30
```

Then read the generated report and also read the entry files in `.liuyishou/entries/` for the same period.

Explain:
- where the user's recent value is coming from
- what work looks too commoditized
- what kind of work they should pull toward next

#### Rewriting recommended moves

The script generates placeholder recommended moves using simple rules. After reading the report and the raw entries, replace them with your own assessment. Consider:
- the user's profile and career goal
- which moat dimensions dominate and which are absent
- whether the user is drifting toward easily-automated work
- what specific shifts in work selection would strengthen their moat over the next 30 days
- each move should be distinct and tied to real patterns you see in the entries

Use the Edit tool to replace the `## Recommended Moves` section in the generated markdown file, then present the updated version to the user.

### 5. `pack`

Use when the user wants a reusable artifact for someone else.

Supported pack types:
- `manager-update`
- `performance-bullets`
- `mobility-pack`
- `exit-pack`

Command patterns:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/liuyishou.py pack --root .liuyishou --type manager-update
python3 ${CLAUDE_SKILL_DIR}/scripts/liuyishou.py pack --root .liuyishou --type performance-bullets --days 90
python3 ${CLAUDE_SKILL_DIR}/scripts/liuyishou.py pack --root .liuyishou --type mobility-pack --days 90
python3 ${CLAUDE_SKILL_DIR}/scripts/liuyishou.py pack --root .liuyishou --type exit-pack --days 90
```

`pack` is intentionally split in two layers:
- the script writes a deterministic local draft
- the agent rewrites the audience-facing judgment and wording

The script must exclude `share_level = private` entries from all pack exports by default. Never reintroduce private entries or `private_notes` in your rewrite.

After generation, read the markdown file and the raw shareable entries.
- For `manager-update`, rewrite the draft into a short manager-facing weekly update. Default shape:
  - `## Wins`: 3-5 flat bullets, ordered by strategic importance
  - `## Risks / Asks`: 0-2 flat bullets
  - `## Next Steps`: exactly 3 items
  - Do not add long prose, capability essays, or theme subheadings unless the user explicitly asks.
- For `performance-bullets`, default to 5-8 copy-ready Chinese bullets only. Each bullet should follow "做了什么 + 为什么重要 + 结果/影响". Do not add sections, tables, maturity models, keyword indexes, or long commentary unless the user explicitly asks for a longer review packet.
- For `mobility-pack`, rewrite around target-role fit. A structured memo is fine here: role target, ability mapping, strongest evidence, gaps, next proof points.
- For `exit-pack`, you may keep the longer emergency-switch format: short self-intro, transferable stories, resume-ready bullets, target-role directions, evidence index.

## Operating Rules

1. Never invent achievements, numbers, or evidence.
2. Distinguish clearly between:
   - shareable facts
   - private reasoning
   - people-sensitive context
3. Prefer deterministic script writes for storage, filtering, and scaffolding; use LLM judgment for audience-specific wording and recommendations.
4. Keep user data local unless the user explicitly asks for export or sharing.
5. If the user asks for a new feature, preserve the existing storage contract in [data-contract.md](./references/data-contract.md).

## Minimal Intake Rules

For fast adoption, keep prompts short.

`init` needs only:
- role
- focus
- goal

`capture` needs only:
- what happened
- why it mattered

Everything else is optional and can be enriched later.

## Output Contract

This skill should produce two classes of output:

Private outputs:
- work receipts timeline
- weekly defense review
- moat report

Shareable outputs:
- manager update
- performance bullets
- mobility pack
- exit pack

Output formats for v0:
- markdown files on disk
- short in-chat summary
- copy-ready bullets

Artifact shape defaults:
- `manager-update`: short enough to paste into chat or email without trimming
- `performance-bullets`: bullets first, no report styling by default
- `mobility-pack`: argument memo for internal role change
- `exit-pack`: external-facing interview and resume ammo pack

Do not add PDF, database, browser extension, or cloud sync logic inside this skill unless the user explicitly asks for it.
