---
name: go-cli-ship
description: "Build or upgrade Go CLI projects to production quality with a deterministic workflow: architecture, stable CLI contract, tests/lint gates, cloud smoke tests, release automation, installer, README quality, and skill packaging. Use when users ask to develop a Go CLI from scratch, improve engineering quality, fix CI/release issues, ship versions, or standardize docs and SKILL.md."
---

# Go CLI Ship

将“需求 -> 设计 -> 实现 -> 验证 -> 发版 -> 文档/技能”固化为可重复执行的交付流程。

## 触发意图

当用户出现以下诉求时使用本技能：

- “开发一个 Go CLI/重构现有 CLI”
- “把项目做成可发布、可安装、可自动化”
- “CI / lint / release 一直报错，帮我闭环”
- “README 不专业，发版质量不稳定”
- “需要技能化，让后续项目复用流程”

## 第一性原理

1. CLI 本质是自动化接口，不只是命令行工具。
2. 稳定契约优先于局部体验：向后兼容、错误码稳定、JSON 可机读。
3. 发版是系统工程：版本一致性 + workflow 可重复 + 产物可验证。
4. 文档是产品一部分：README 决定信任和采用率。
5. 技能文档不是科普文，应是可执行操作手册。

## 逆向约束（先防失败）

先检查这些高频失败点：

1. `go.mod` Go 版本与 CI/lint 构建器是否一致。
2. `golangci-lint` 是否会因编译器版本低于目标版本而 panic。
3. release artifact 下载后是否为目录结构（checksum 误扫目录）。
4. tag 是否指向正确提交（release 仅对 tag push 触发）。
5. `Makefile/install.sh/CHANGELOG.md` 版本是否一致。
6. README 是否缺少价值主张、安装路径、云端教程、输出契约。
7. SKILL.md 是否符合 skill-creator（frontmatter 仅 `name/description`）。

## 标准交付流程

### 1) 需求建模

- 定义用户、核心场景、非目标。
- 定义命令边界：
  - 人类输出（table）
  - 机器输出（json，默认）
- 定义错误模型：稳定 `code` + `message` + `retryable` + 可选 `details`。

### 2) CLI 合同设计

- 命令命名稳定，不随文案变化。
- 参数新增优先“增量兼容”，不要破坏旧参数。
- JSON 采用“新增字段兼容”，避免删改现有字段语义。
- 高价值命令支持别名（如 `--max` = `--limit`），但保留主参数。

### 3) 工程骨架

最小建议结构：

- `cmd/` 命令层
- `pkg/` 业务层与适配层
- `e2e/` 端到端测试
- `scripts/` 安装与一致性脚本
- `.github/workflows/` CI + release
- `skills/<skill-name>/SKILL.md`

### 4) 质量门禁（必须）

必须绿灯：

```bash
gofmt -l .
go vet ./...
golangci-lint run
CGO_ENABLED=1 go test -count=1 ./...
make release-check
```

如果本地与 CI 不一致，以 CI 为准并回灌本地脚本。

### 5) CI 与 lint 最佳实践

- `actions/setup-go` 版本与 `go.mod` 主版本一致。
- `golangci-lint-action@v7` 建议：
  - `version: v2.5.0`（或你锁定的版本）
  - `install-mode: goinstall`（避免“linter 用旧 Go 构建”导致 panic）
- `.golangci.yml` 的 `run.go` 与 `go.mod` 对齐。

### 6) Release 工作流最佳实践

- 触发：`on.push.tags: v*`
- 构建矩阵：`linux/darwin` + `amd64/arm64`
- 注入版本：`-ldflags "-X <module>/cmd/<cli>.Version=${GITHUB_REF_NAME#v}"`
- artifact 下载建议：
  - `actions/download-artifact@v4`
  - `pattern: <cli>-*`
  - `merge-multiple: true`
- checksum：`sha256sum <cli>-* > SHA256SUMS`

### 7) 版本治理

版本源必须唯一且一致：

- `Makefile` 的 `VERSION`
- `scripts/install.sh` 的 `VERSION`
- `CHANGELOG.md` 顶部版本

发布前必跑：

```bash
make release-check
```

### 8) 云端真实联调

如果 CLI 依赖外部认证/API，交付前至少完成一次真实 smoke：

- 授权链路
- 最小查询命令
- 关键错误路径（凭据缺失/权限不足/网络失败）

强调：mock 测试不能替代真实认证链路验证。

### 9) README 最佳实践（交付标准）

README 需具备：

1. 首屏信任区：徽章 + 一句话价值主张。
2. 问题定义：本项目解决什么、不解决什么。
3. 差异化：与官方或主流方案关系（互补/优势边界）。
4. 安装方式：release 下载与一键安装。
5. 快速开始：30 秒命令路径。
6. 生产卡点教程：尤其云服务器授权场景。
7. 输出契约：成功/失败 JSON。
8. 安全策略：最小权限、凭据处理。

### 10) SKILL.md 最佳实践（与 skill-creator 一致）

必须遵守：

- frontmatter 仅保留 `name` 与 `description`。
- `description` 写清“做什么 + 何时触发”。
- body 聚焦可执行流程，不写长篇背景。
- 默认用动词指令句：检查、执行、验证、回滚。
- 写清失败兜底路径与最小恢复步骤。

## 可直接复用的执行清单

### A. 新建项目

1. 初始化目录与模块。
2. 先落 `cmd` 骨架和输出契约。
3. 先写 `make release-check` 与 CI，再写功能。
4. 每完成功能子集都跑全门禁。

### B. 旧项目升级

1. 先锁定行为契约（命令/JSON/错误码）。
2. 补齐 `Makefile` 门禁目标。
3. 修 CI 版本对齐（Go/lint）。
4. 修 release 工程化（artifact/checksum/tag）。
5. 重写 README 首屏与上手路径。

### C. 发版

1. 改版本：`Makefile`、`install.sh`、`CHANGELOG.md`。
2. `make release-check`。
3. 推送 `main`。
4. 打 tag：`vX.Y.Z`。
5. 确认 release 产物与 checksum。

## 常见故障速解

- lint panic：`application built with go1.xx` 低于项目 Go 版本
  - 处理：`install-mode: goinstall` + `.golangci.yml run.go` 对齐。
- checksum 报目录错误
  - 处理：`download-artifact` 使用 `merge-multiple: true`。
- 改了 workflow 但 release 不触发
  - 处理：检查是否 push tag；必要时重打 tag 到正确提交。
- 本地通过 CI 失败
  - 处理：统一缓存/编译参数，按 CI 命令本地复现。

## 完成定义（DoD）

满足以下条件才算交付完成：

1. 功能满足需求，且命令契约稳定。
2. 所有质量门禁通过。
3. release 可产出多平台二进制 + `SHA256SUMS`。
4. README 达到“信任 + 上手 + 安全 + 自动化”标准。
5. SKILL.md 通过 skill-creator 校验并能触发正确意图。
