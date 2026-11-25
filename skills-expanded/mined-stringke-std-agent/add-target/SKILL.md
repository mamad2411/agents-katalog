---
type: skills
name: add-target
description: 维护 stdagent 的 AI CLI target 全集。发现最新平台、对照官方规范更新适配器（落点、5 种 type、MCP、frontmatter、上下文限额），并在产品停更或配置面消失时移除。用于全量扫描、新增、更新或删除 target。
priority: high
applyTo:
  - "internal/transformer/**/*.go"
  - "internal/budget/**/*.go"
  - "internal/config/schema.go"
  - "internal/writer/gitignore.go"
  - "docs/targets/*.md"
---

# Maintain targets

目标：`ValidTargets` 与仍在维护、且有项目级配置面的 AI CLI 对齐。新平台按官方能力接入 5 种 type；已有平台只改有证据的差异；官方停更或配置面消失则移除。不破坏共享输出。

开始前读取 `.stdai/standards/references/transformer-design.md`、`docs/format-spec.md`、`docs/conversion-rules.md`，以及相近 target 的 `docs/targets/<name>.md` 与 transformer。

- 用户点名工具：只处理该 target（含接入、更新或移除）。
- 未点名：必须同时做三件事，先出差异表再改代码。无证据变化不要重写。
  1. 发现未注册的新平台
  2. 复核每个 `ValidTargets` 的官方规范
  3. 判定停更项并准备移除

未要求时不 commit、不发版。移除是 breaking change：先列出官方证据和受影响路径，确认后再删代码。

## 发现新平台

对照 `internal/config.ValidTargets` 搜索尚未接入的 AI coding CLI / IDE agent。用 `exa` 查产品与新闻，用 `context7` 和官方站点查项目级配置，用 `gh_grep` 核仓库实现。社区文章只作明确标注的补充。

接入门槛：有文档化的项目级 rules/skills/commands/agents 配置，且 stdagent 能写出该工具会发现的文件。只有用户级 `~/` 配置或纯聊天 UI 的列入 skip，不要接入。

每个候选记 add / skip / watch，并带来源 URL。

## 调研现有 target

官方文档和官方仓库是协议依据。每条结论带完整来源 URL。

用当前官方页面对照 adapter 与 `docs/targets/<name>.md`。逐项标 native / degrade / skip / UNKNOWN：

| 维度 | 要确认的事实 |
|---|---|
| 存活 | 产品是否仍发布；仓库是否 archived；是否改名/被后继产品取代 |
| 发现路径 | 项目根文件、目录、加载顺序、嵌套、本地覆盖文件 |
| rules | 原生路径、path matcher、always-on、是否 inline 到根文件 |
| skills | 是否 Agent Skills；目录；frontmatter 白名单 |
| commands | 原生 prompts/commands/workflows，或降为 skill 子目录 |
| references | 原生目录或 fallback |
| subagents | 原生 agents 目录与字段，或 fallback |
| MCP | 项目级文件与顶层 key；用户配置合并则不要覆盖 |
| 共享路径 | 是否消费 `AGENTS.md` / `.agents/`；多 target 同路径必须字节一致 |
| 限额 | 单文件、根文件、总量的 soft/hard；超限是截断、拒载还是淘汰 |
| 不写 | hooks、用户 settings、全局 `~/` 配置、`crush.json` / `kilo.jsonc` 这类 JSONMerge 用户文件 |

硬限制只记录有官方证据的值，并同步 `internal/budget.Limits`。没有文档化上限就写 `UNKNOWN`，不要发明数字。

## 停更与移除

满足任一官方证据则移除（或先迁到后继 target）：

- 官方宣布停更、sunset 或产品下线
- 官方仓库 archived，且没有沿用同一项目配置的后继产品
- 项目级配置面消失，stdagent 再也写不出该工具会发现的文件
- 产品改名或被后继取代：优先把现有 target 迁到后继约定，不要留僵尸名

不要因为发布间隔长、用户少、文档暂时 404 就移除。证据不足标 `UNKNOWN` 并保留。

改名迁移不算静默删除：保留用户仍在用的路径，直到后继 adapter 能写出等价文件。

从 `ValidTargets` 删除会使旧 `config.toml` 校验失败，commit 使用 `!` 与 `BREAKING CHANGE`。共享路径（如 `AGENTS.md`）只要还有其他 producer 就保留。本仓库先从 `.stdai/config.toml` 去掉该 target，再 `go run ./cmd/stdagent sync --no-pull --strict` 让 prune 清掉其独占生成物，然后删代码。

## 实现

优先复用现有 protocol：`AgentsMD`、`ClaudeMD`、`Cursor`、`Clinerules`、`WindsurfStyle`、`Copilot`。仅当多个 target 共享且 adapter 无法表达时扩展协议层。单 target 特性留在 wrapper。

原生能力优先。缺失类型走现有 graceful degradation。不要虚构工具不会消费的文件。同一路径冲突必须在写盘前失败。

新增做完整注册；更新只改被证据触及的项；移除做对称删除：

1. `internal/transformer/<name>.go` 及其 smoke / golden 测试
2. `internal/config.ValidTargets` 与 `Default().Targets`（模板里新 target 默认 `enabled=false`）
3. 本仓库 `.stdai/config.toml` 只开本仓库实际使用的 target；多 target / gitignore 模式展示放 `examples/`
4. `internal/writer.targetIgnorePrefixes`（JSONMerge 用户文件不列入）
5. 该 target 的 `internal/budget.Limits`
6. `docs/targets/<name>.md`
7. 协议族或 MCP 表：`docs/conversion-rules.md`
8. 用户可见清单与数量，以 `ValidTargets` 为准：`.stdai/standards/root.md`、`internal/cli/root.go` 的 Long、`README.md` / `README.zh-CN.md` 及其余 `README.*`、`docs/README.md`

## Done means

- 差异表覆盖新平台、现有差异、停更项；每项 native / degrade / skip / add / remove / UNKNOWN 都有官方 URL
- 测试覆盖 5 种 type、target filter、关键路径和所有共享文件；先复现风险再证明修复
- `go test ./...`、`go test -race ./internal/transformer/...`、`mise run check`
- `go run ./cmd/stdagent sync --no-pull --strict` 与 `go run ./cmd/stdagent status` 通过

无法执行的验证标 `UNKNOWN`。
