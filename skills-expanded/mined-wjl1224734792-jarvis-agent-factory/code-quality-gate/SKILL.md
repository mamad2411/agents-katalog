---
name: code-quality-gate
description: "代码质量门——Gate C1 的四项强制检查：Lint、Type-check、Build、依赖安全扫描。按项目类型自动选择对应工具链，失败回退修复，全部通过方可进入测试验证。"
version: "4.3.8"
updated: "2026-05-14"
---

# 代码质量门（Gate C1）

## 概述

实现完成后、测试验证前，必须通过代码质量门。这不是可选检查——是进入 Gate C2 的硬性前置条件。四项检查按顺序执行，任一项失败即阻断。

**核心原则：** 未通过质量门的代码不允许进入测试。质量门通过 = 代码具备"可测试"的基本条件。

## 何时使用

**强制使用（主流程）：** 全部实现 Batch 完成后，Gate C2 之前（Gate C1）。不可跳过、不可绕过。

**强制使用（最终验证）：** Gate E 发布前，Gate D 评审触发了代码修复时，**必须重新运行本技能所有四项检查**，确保修复未引入新问题。

**强制使用（CI 前置验证）**：在 push 代码前，若项目配置了远程 CI，应先通过本质量门所有检查，再推送。本地质量门通过 = CI 通过概率大幅提高。

**不适用：** 纯文档变更（无代码修改）、探索/研究任务（无交付代码）。

## 四项检查（四项检查可并行启动，但修复后的重检需全部重跑）

### 1. Lint（代码风格）

| 判定 | 动作 |
|------|------|
| 0 error | ✅ 通过。warning 记录但不阻断 |
| 有 error | ❌ 回退对应实现 agent 修复 |

### 2. Type-check（静态类型）

| 判定 | 动作 |
|------|------|
| 0 error | ✅ 通过 |
| 有 error | ❌ 回退对应实现 agent 修复 |

### 3. Build（构建）

| 判定 | 动作 |
|------|------|
| exit 0 | ✅ 通过 |
| exit ≠ 0 | ❌ 回退对应实现 agent 修复 |

### 4. Deps Audit（依赖安全）

| 判定 | 动作 |
|------|------|
| 无 Critical/High | ✅ 通过 |
| 有 High+ | ⚠️ 评估→修复或书面豁免→记录在案 |

## 与 CI 的关系

本质量门检查（Lint + Type-check + Build + Deps Audit）是 CI 流水线的本地等效检查：

- **本地质量门通过 ↑** → 远程 CI 通过概率大幅提高
- **本地质量门不通过** → 远程 CI 几乎必定失败 → 不要推送
- **本地质量门通过 + 远程 CI 通过** → 可以推送 tag、发布

🔴 **红线**：本地质量门未通过时，不允许推送代码触发远程 CI。先修本地问题，再推远程。

## 按项目类型选择工具链

| 项目类型 | Lint | Type-check | Build | Deps Audit |
|---------|------|------------|-------|------------|
| TypeScript/JavaScript | `eslint` / `prettier --check` | `tsc --noEmit` | `npm run build` / `tsup` | `npm audit` |
| Python | `ruff check` / `black --check` | `mypy` | —（解释型跳过） | `pip-audit` / `safety check` |
| Rust | `cargo clippy` / `rustfmt --check` | `cargo check` | `cargo build` | `cargo audit` |
| Go | `golangci-lint run` | `go vet` | `go build ./...` | `govulncheck ./...` |
| Kotlin/Android | `ktlint` / `detekt` | 编译检查 | `./gradlew build` | `./gradlew dependencyCheckAnalyze` |
| Swift/iOS | `swiftlint` | 编译检查 | `xcodebuild` | —（SPM 自动校验） |
| Flutter/Dart | `flutter analyze` / `dart format --check` | `dart analyze` | `flutter build` | `dart pub outdated` |

## 失败处理

- 同文件 lint/type-check 错误 → 回退对应实现 agent，修复后仅重跑该项
- Build 失败 → 回退导致编译错误的实现 agent
- 同一错误修复 2 次仍失败 → 标记任务 `BLOCKED`，不阻塞同批其他任务
- 修复后 → 重新执行全部四项（确保修复未引入新问题）

## 输出

通过后生成 Gate C1 质量检查摘要（用作 Gate C2 前置输入）：

```
## Gate C1 质量检查摘要
- Lint: ✅ 通过（0 errors, N warnings）
- Type-check: ✅ 通过（0 errors）
- Build: ✅ 通过（exit 0, duration: Xs）
- Deps Audit: ✅ 通过（0 Critical, 0 High）
```
