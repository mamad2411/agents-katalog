---
name: qa-static-baseline
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
description: >-
  QA child skill - pre-test static quality gate: auto-discovers package manager and scripts, runs tsc + ESLint + Prettier + npm audit + git-secrets + schema/OpenAPI lint, and detects threshold weakening, disabled rules and generated-file false positives. Owns parent section 4 Layer 1.
---

# qa-static-baseline

## 1. Position

所有测试前的静态质量门禁。**不是简单 lint** —— 它包括类型检查、代码风格、依赖漏洞、密钥扫描、schema 校验，并且**检测配置弱化**（关 strict、降 coverage threshold、禁 rule）。

## 2. Triggers

- Parent §6 Step 5 默认 dispatch（Static layer 任何项目必跑）
- 独立触发：开发者 PR 准备阶段
- 独立触发：CI 启动时 fast-fail gate
- 独立触发：dependency 升级 / lockfile 变更后的 audit

## 3. Responsibilities

- **Auto-discover**：package manager（npm / pnpm / yarn / bun）、scripts、framework lint
- **Run**：
  - `tsc --noEmit`（TypeScript 项目）
  - `eslint .` / `biome check .`
  - `prettier --check .`
  - `npm audit --audit-level=high`（hard fail 条件）
  - git-secrets / TruffleHog（secret 扫描）
  - OpenAPI / JSON Schema lint（若有 spec）

> **ESLint 9 命令漂移（务必核对）**：① **`--format compact` 已从 core 移除** —— ESLint 9 下传 `--format compact` 会直接 `exit 2` 报错。机器解析用 `--format json`（或 `stylish` 给人看）；仍要 compact 文本则 `npm i -D eslint-formatter-compact` 后 `--format compact`。② **TS 项目须前置 `typescript-eslint` parser** —— flat config（`eslint.config.js`）里 `languageOptions.parser = tseslint.parser`，否则 `.ts` 的类型注解语法直接 parse-error。本 skill 解析 ESLint 输出时默认 `--format json`（见 §6 by-rule 计数），不依赖已移除的 compact formatter。
- **Detect**：
  - threshold 弱化（strict: false、coverage threshold 降低、rule 关闭）
  - 生成文件误报（标 `dist/` / `build/` / `*.generated.*` 应在 ignore）
  - 配置漂移（`.eslintrc` vs PR 变更）
- **Output static_baseline YAML**

## 4. Non-responsibilities

- 不做 TDD（属于 `qa-test-design-tdd-bridge`）
- 不替代 code-reviewer（属于 `code-reviewer` agent）
- 不允许为 pass 而删 rule / 调低 threshold / skip 文件

## 5. Workflow

1. Discover stack
2. Build run plan（按 discovered tools）
3. Run each tool，capture stdout + exit code
4. Detect threshold weakening（对比 git log 看 config 历史）
5. Classify failures（code / config / dep / generated-file false positive）
6. Output `static_baseline` YAML

## 6. Output Contract

```yaml
static_baseline:
  commands_run:
    - command: npx tsc --noEmit
      exit_code: 0
      stdout_excerpt: ...
    - command: npx eslint .
      exit_code: 0
      stdout_excerpt: ...
    - command: npm audit --audit-level=high
      exit_code: 0
      vulnerabilities: { critical: 0, high: 0, moderate: 2 }
    - command: <secret scan>
      exit_code: 0
  config_integrity:
    threshold_weakened: false  # tsc strict 关 / coverage threshold 降 / lint disable
    rules_disabled_in_pr: []
    config_drift_detected: false
  failures:
    - file: <path>
      category: code | config | dep | generated_false_positive
      severity: critical | high | medium | low
      owner: <github handle>
      recommended_fix: ...
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 7. Parent Integration

- Triggered by: parent §6 Step 5
- Returns: `static_baseline` YAML
- Consumed by: `qa-evidence-bundle` → `child_skill_results.static`

## 8. Forbidden patterns

- 通过删 lint rule 让 PR pass
- 把 `--audit-level=critical` 改成 `=none` 跳过 audit
- `tsc strict: false` 静默改
- 忽略 secret scan hit

## 9. References

- [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [ESLint](https://eslint.org/docs/latest/) / [Biome](https://biomejs.dev/)
- [TruffleHog secret scan](https://github.com/trufflesecurity/trufflehog)
- [git-secrets](https://github.com/awslabs/git-secrets)
