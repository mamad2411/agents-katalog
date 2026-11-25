---
name: learn-as-you-go
description: |
  Use when technical AI output would slow down a non-technical or semi-technical user who needs to act on it. Trigger on requests such as "say it plainly", "I do not understand this", "explain in plain language", or when output contains dense engineering terms, acronyms, configuration names, database terms, deployment language, debugging conclusions, API concepts, schemas, migrations, rollback plans, or runtime behavior that should remain precise but become understandable.
license: MIT
metadata:
  tags: [communication, plain-language, learning-by-doing, vibe-coding, accessibility]
  related_skills: [humanizer]
---

# Learn As You Go

Keep the technical output intact, then add a plain-language Chinese explanation immediately below it.

This skill is not a glossary and not a rewrite pass. It is a side-by-side reading aid for people who can follow technical instructions but get slowed down by dense engineering wording.

## Core Contract

For each semantic block that needs help:

```md
[Original technical output]
↳ [Plain-language meaning in everyday Chinese]
```

Use the `↳` line to explain what the original block means in ordinary Chinese. Preserve the original wording so the user can still copy, search, audit, or compare it.

### Generated Explanation Mode

If the user asks to explain a technical topic rather than providing text to transform, still use the side-by-side pattern.

For each important point:

1. Write a concise technical anchor sentence first, using the primary language requested by the user.
2. Add `↳` immediately below with the plain-language meaning.
3. Keep code, paths, config keys, and labels exact inside both lines.
4. Put optional tables, bullets, or flow details after this pair, not before it.

Do not switch a Chinese request to English merely to create a technical/plain-language pair. Use English anchors only when the user requests English or when preserving user-provided English source text.

Every numbered or headed section in a generated explanation should start with this local contract:

```md
[Technical anchor sentence]
↳ [Plain-language consequence for the user]

[Optional details: table, bullets, short flow]
```

Do not use `↳` only as a section-level summary after a table or long explanation. The `↳` line is the user's local reading aid, so it must appear before the optional details become dense.

Good:

```md
`memoryMode=policy-only` means failure records are searchable but not automatically injected into the system prompt.
↳ 这表示失败记录还在库里，agent 可以主动查；但系统不会每次开局都把这些失败记录塞进 prompt。
```

Bad:

```md
policy-only 不注入；legacy-inject 全量注入。
```

The bad version is shorter, but it drops the paired plain-language explanation and forces the user to infer the consequence.

## Activation

Apply this skill when:

- The user asks for "说人话", "看不懂", "翻译一下", "白话解释", "plain language", or similar help.
- The user appears non-technical or semi-technical and must act on technical advice.
- The output contains multiple engineering terms, acronyms, config names, database terms, deployment terms, API concepts, schema, migration, rollback, runtime, CI, lint, feature flag, or debugging language.
- The user needs to make a decision from a technical recommendation.

Do not apply it when:

- The user explicitly asks for only the technical conclusion.
- The user requests exact JSON, XML, YAML, a single exact string, or another machine-readable output shape.
- The output is mainly code, commands, logs, paths, hashes, issue IDs, or exact identifiers.
- The user is asking for API precision, type definitions, or implementation details and has not requested plain-language help.
- For code review findings, keep the exact finding first; add `↳` only when the finding contains dense technical reasoning or the user needs to act on it.
- The user has clearly shown they already understand the terms in this context.

## Pairing Rules

Pair by semantic block, not by physical line.

| Source shape | Output shape |
|---|---|
| Paragraph | Add one `↳` line below the paragraph |
| Bullet list | 入门档: one indented `↳` line below **each** bullet. 标准档: multiple similar short bullets **share one** `↳` line after the group — keep every bullet's original text |
| Dense semicolon list | Keep the full block, then split the plain explanation into short lines |
| Markdown table | Keep the table intact, then add a separate plain-language section below |
| Code, shell, path, hash, issue ID | Do not insert `↳` inside it; explain outside if needed |

For generated explanations, use the same shapes: table for compact comparison, then `↳ 白话版:` below when the table contains dense terms.

### Pairing granularity — by reader level

The grouping rule depends on the active reader level (see Reader Level below). The original text is never removed at any level.

**入门 (Level 1) — every unit gets its own explanation** (each bullet paired individually):

```md
- 对瞬态错误 fail-fast：网络超时直接抛出去 → 上游用户看错误页，1 秒后重试就成功
  ↳ 临时性的小错不要立刻报错，重试一下就好
- 对不可逆错误 graceful degradation：catch NullPointerException 重试 3 次 → 永远不会成功
  ↳ 代码 bug 那种永久错误不要靠重试解决
```

**标准 (Level 2) — similar short items may share one explanation** (all original bullets stay):

```md
- 对瞬态错误 fail-fast：网络超时直接抛出去
- 对不可逆错误 graceful degradation：catch NullPointerException 重试 3 次
↳ 临时性小错直接重试就好；代码 bug 那种永久错误重试也没用，两条的应对方式相反。
```

**Bad** (merging in 入门 level, or merging while dropping original items):

```md
- 对瞬态错误 fail-fast：网络超时直接抛出去
- 对不可逆错误 graceful degradation：catch NullPointerException 重试 3 次
↳ 这四条都是常见错误。
```

The bad version loses the per-unit reading aid (入门 level) or drops original content (any level).

## Reader Level

The skill supports **two** reader-depth levels. The level controls **which terms need `↳` and how explanations are grouped** (identifier preservation is invariant across levels — see Non-Negotiable Rules).

| 维度 | 1 · 入门 (Beginner) | 2 · 标准 (Standard, default) |
|---|---|---|
| 术语处理 | 概念性技术词汇**全部白话化**：整句技术描述直接做白话转换，不留概念术语（fail-fast → "立刻报错，别假装能用"） | **保留技术名词**原文，白话解释围绕它展开（fail-fast ↳ 立刻报错，不假装能继续） |
| 解释单元 | **每个段落或每次换行 = 一个单元，每个单元都必须有解释** | 按语义块；同一块内多个同类短项（如一组验证项）可合并为一条解释，每条原文保留 |
| 白话程度 | 口语化 + 日常类比 + 说明因果 | 简短直白，只解释影响理解或行动的部分 |
| ↳ 长度 | 30-50 字 | 15-25 字 |

**两档都不变**：路径、环境变量、命令名、端口、ID、产品名等标识符原样保留（Non-Negotiable #4），白话解释围绕标识符展开；代码块、命令、表格内部不插 `↳`（Exemptions）。

### Level 1 example

```md
ALTER TABLE orders ADD COLUMN status TEXT;
↳ 改表结构。给"orders"这张表加一个叫"status"的新字段，类型是可以存文字的（TEXT 就是文本类型）。
```

### Level 2 example

```md
ALTER TABLE orders ADD COLUMN status TEXT;
↳ 给表加一个新字段。
```

### Style gradient

| Level | ↳ length | Tone | Analogies | "Why" |
|---|---|---|---|---|
| 1 | 30-50 字 | everyday, gentle | encouraged when helpful | include when present in the original |
| 2 | 15-25 字 | direct | only when genuinely abstract | only when it changes what the user does |

The level is selected by the runtime (extension or skill environment), not by the LLM. The LLM only applies the chosen level's criteria.

## Non-Negotiable Rules

1. Keep the original technical output unchanged.
2. Put the plain-language explanation immediately below the original block.
3. Do not explain jargon with more jargon.
4. Preserve names, file paths, environment variables, function names, ports, IDs, hashes, and product names.
5. Do not add facts, risks, decisions, emotions, blame, certainty, or urgency that the original did not contain.
6. Preserve modality: do not turn "consider" into "must", or "must" into "maybe".

## Plain-Language Style

Use everyday Chinese. Short is better than ornate. The skill should be driven by judgment, not by a fixed glossary.

Core rule: translate concepts that affect understanding or action; preserve identifiers that must remain exact.

Decision test:

1. Would the user need to copy, search, configure, compare, or audit this exact string?
   - If yes, preserve it exactly.
2. Does this word or phrase change what the user needs to understand, decide, or do?
   - If yes, explain it in plain Chinese.
3. If both are true, preserve the exact string and explain its role around it.
4. If neither is true, do not explain it.

### What To Explain

Explain terms or phrases when the user cannot safely act on the technical output without understanding them.

Prioritize:

- **Next-action terms**: words that decide what the user should do, such as migrate, rollback, approve, block, enable, disable, import, export.
- **System behavior**: runtime, startup, fail-fast, fallback, timeout, retry, cache, queue, worker.
- **Data shape or data movement**: schema, payload, migration, validation, normalization, serialization.
- **Environment and release state**: production, staging, canary, deployment, rehearsal, release candidate.
- **Risk and control flow**: regression, audit, guardrail, feature flag, permission, allowlist, denylist.
- **Acronyms and compressed labels**: explain unless they are already clear from the conversation.
- **Dense English phrases**: explain when a non-technical user would need to guess before acting.

When in doubt, ask: "Does this word change what the user needs to do next?" If yes, explain it.

### What To Preserve

Preserve exact strings that the user may need to copy, search, compare, or configure:

- Product names and tool names
- File paths and URLs
- Port numbers, IP addresses, IDs, hashes, PR numbers, and issue numbers
- Environment variables, config keys, table names, function names, class names, and command names
- Release labels or status labels that must stay auditable

For preserved identifiers, explain their role without changing the identifier:

```md
Set APP_DATABASE_URL before running the migration.
↳ 跑数据迁移之前，先用 APP_DATABASE_URL 告诉系统数据库在哪里。
```

### Conflict Rule

When a term is both an identifier and a concept, identifier preservation wins.

Keep the exact string, then explain what it does.

Bad:

```md
Set APP_DATABASE_URL before running the migration.
↳ 设置“应用数据库地址”之后再迁移。
```

Good:

```md
Set APP_DATABASE_URL before running the migration.
↳ 跑数据迁移之前，先用 APP_DATABASE_URL 告诉系统数据库在哪里。
```

Release or status words can be explained, but exact labels must remain intact.

```md
Do not call this a production-ready candidate.
↳ 不要把它标成 production-ready candidate，也就是“已经可以正式上线的版本”。
```

### How To Choose The Wording

Choose the shortest explanation that makes the sentence actionable. Do not chase a perfect dictionary translation.

| If the source contains... | Do this | Example |
|---|---|---|
| A common product/tool name | Keep it as-is | `Codex`, `Cloudflare`, `GitHub` |
| An exact identifier | Keep it, explain its role | `APP_DATABASE_URL` -> "告诉系统数据库在哪里的变量" |
| A common Chinese engineering word | Use the common Chinese word | `rollback` -> "回滚" |
| A dense English pattern | Explain the behavior | `fail-fast` -> "立刻报错，不要假装能继续" |
| An abstract data term | Explain the intent | `schema` -> "数据长什么样的约定" |
| A priority code | Explain once, then preserve | `P0/P1` -> "最重要 / 次重要" |

Tiny examples are enough. Do not add a large glossary unless the user provides a project-specific vocabulary for the current task.

### Noise Control

- Explain a repeated term only on first meaningful use within the same local section, unless its meaning changes.
- Do not add a `↳` line to a sentence that is already plain Chinese and contains only preserved identifiers.
- When a dense paragraph contains several technical terms but one plain explanation can cover the whole block, use one `↳` block instead of one explanation per term.
- Prefer one explanation per semantic block over one explanation per physical line.
- Do not use decorative status icons or emoji unless the source text already uses them.
- Keep headings short and functional; do not turn the response into a stylized tutorial when the user asked for plain understanding.

## Tables

Do not insert `↳` lines inside Markdown tables.

In generated explanations, do not start a section with a table. Start with a technical anchor sentence and a `↳` line, then use a table only as supporting detail.

```md
| Term | Meaning |
|---|---|
| runtime | where the app is actually running |
| rollback | return to the previous working state |

↳ 白话版:
- runtime 指系统真正跑起来的地方。
- rollback 指出问题后退回之前能用的状态。
```

## Exemptions

Do not put plain-language lines inside:

- Shell commands
- Code blocks
- Function signatures
- File paths
- URLs
- Commit hashes
- Pull request or issue numbers
- Exact IDs and identifiers

Explain the purpose before or after the block instead.

When showing pseudocode or a flow, prefer bullets or tables if the content is explanatory rather than copyable code. If a fenced code block is necessary, keep the block clean and put `↳` explanations before or after it, never inside it.

## User Controls

Honor temporary user instructions:

- "白话再短一点" -> keep each explanation around 15-25 Chinese characters when possible.
- "加日常类比" -> use simple analogies, while preserving the original meaning.
- "中英双语" -> add both Chinese and English plain-language explanations.
- "关闭 Learn As You Go" or "不要白话" -> stop adding `↳` lines for the rest of the current task.
- "强语气模式" -> use stronger wording only when the original already has strong wording.

## Relationship With Humanizer

`humanizer` changes writing style. `learn-as-you-go` changes understandability of technical meaning. They can be combined, but do not let style polishing delete the original technical text.

## Verification Checklist

Before returning output:

- [ ] Dense technical blocks have `↳` explanations.
- [ ] Original technical text is unchanged.
- [ ] Tables remain valid Markdown.
- [ ] Commands, code, paths, hashes, and IDs are untouched internally.
- [ ] Plain language avoids unexplained English jargon.
- [ ] Names, paths, variables, ports, and IDs are preserved.
- [ ] No new facts, risks, emotions, or decisions were added.
- [ ] Modality and responsibility match the original.
