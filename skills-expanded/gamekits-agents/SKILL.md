# AGENTS.md

本文件是后续所有自动化开发代理和人工协作者的仓库入口规则。开始任何实现前，先阅读本文件，再阅读 `docs/` 中对应主题。

## 必读文档

每轮开发至少检查：

- `docs/project-design.md`：确认项目定位、目标、非目标和设计信条。
- `docs/architecture.md`：确认包边界和依赖方向。
- `docs/modules/`：涉及具体模块时，确认该模块的最终长期设计、协议和 adapter 边界。
- `docs/implementation-principles.md`：确认实现原则和代码质量要求。
- `docs/best-practices.md`：确认测试、性能、模块拆分实践。
- `docs/development-governance.md`：确认常态开发阶段如何记录状态、关闭工作流，并避免短期状态污染长期文档。
- `docs/release.md`：涉及发布、版本、Changesets、npm、GitHub Actions 或包消费流程时，确认当前发布触发和排障规则。

涉及重大技术选择、包边界变化、第三方库引入、公共 API 调整时，必须新增或更新 `docs/adr/`。

## 文档职责边界

不要在多个文档中重复维护同一段事实。选择文档时按以下规则：

- 项目定位、为什么做、长期目标、非目标、设计信条：写入 `docs/project-design.md`。
- 跨模块包职责、依赖方向、分层结构、公共架构约束：写入 `docs/architecture.md`。
- 单个模块的最终长期职责、公共协议、adapter 边界、扩展点：写入 `docs/modules/<module>.md`。
- 代码质量、实现约束、可测试性、可解释性：写入 `docs/implementation-principles.md`。
- 已验证的开发实践、性能经验、测试策略、反模式：写入 `docs/best-practices.md`。
- 常态开发中的具体状态、任务拆分、review、测试证据：写入任务系统、PR，或按需写入 `docs/implementation/` 下的短期工作流记录。
- 开发文档治理、状态记录和关闭规则：写入 `docs/development-governance.md`。
- 发布触发、Version PR、npm dist-tag、GitHub Release 和发布故障排查：写入 `docs/release.md`。
- 重大决策的背景、候选方案、取舍和后果：写入 `docs/adr/`。

如果一个改动看起来需要更新多个文档，先判断它是不是由两类不同事实组成。不要复制粘贴同一内容；在次要文档中只保留一句引用。

`docs/modules/` 只能写最终长期设计，不写当前实现状态、临时方案、阶段计划、下一步计划、完成定义、TODO、backlog 或 milestone。这些内容分别放入任务系统、PR、`docs/implementation/` 短期工作流记录或 `docs/adr/`。

## 核心设计约束

后续开发必须持续维护这些设计约束：

- GameKits 是可复用游戏框架，不是单一游戏业务仓库，也不是完整自研引擎。
- 成熟库负责底层能力，GameKits 负责稳定协议和组合边界。
- 核心包保持薄内核，不直接绑定具体 ECS、renderer、animation、UI primitive。
- App Host 是应用组合层，负责统一 service registry、生命周期、配置、平台 profile 和 diagnostics；GameRuntime 不能直接拥有 driver/renderer/input/camera/platform/asset/data。
- Phaser、Three.js 等跨 renderer/input/camera/asset 的外部运行时必须优先通过 Driver 统一集成；Adapter 只负责单协议映射，不能各自独立持有同一个外部 runtime。
- Driver 负责创建和持有 Phaser.Game、Three renderer/scene 等外部 runtime；renderer/input/camera/asset adapter 只能绑定到 Driver 提供的 runtime slice，不能在 adapter 内部再次创建整套外部 runtime。
- 必须先判断能力属于 App Service 还是 Game Module：平台、资源、渲染、输入来源、配置、诊断属于应用服务；需要 world/tick/EventBus/gameplay data/context 的能力属于游戏模块。
- Camera/TCA/GAS 是游戏会话能力，应优先通过标准 GameModule helper 启动，不应默认膨胀为 App Host 标准服务。
- 第三方库必须通过 driver、adapter 或 app 层接入，不能泄漏进业务公共 API。
- Renderer 以 RenderObject / RenderNode / RenderCommand 为核心抽象，不以 Sprite 作为公共协议中心。
- Input 是独立大模块，不属于 Renderer；Renderer 只能通过预留桥接点接收已经归一化后的语义指令。
- Gameplay/Camera 输入必须能通过 Input Scope 约束到 game viewport 等交互域，避免在 UI、DevTools、文本输入或其他窗口中误触发。
- Camera 是独立模块，负责镜头状态、控制器、rig 和 adapter 同步；长期归属是 GameModule toolkit + renderer camera adapter，不是 App Host 默认标准服务。
- Platform 是运行环境抽象；Tauri 是当前重要目标 adapter，不是核心架构本身。
- Effect/Fx 不是首层独立业务包；Effect 是 Asset、Renderer、GAS、UI 等基础设施内部可选实现手段。
- Renderer/Input 边界以 `docs/architecture.md` 和 `docs/adr/0003-general-render-objects-and-input-decoupling.md` 为准；不要继续扩展 Phase 2 prototype 的 sprite/input API。
- Renderer lifecycle 不归 GameRuntime；当前由 app/App Host 组合层持有，详见 `docs/adr/0002-app-owned-renderer-lifecycle.md` 和 `docs/adr/0004-app-host-composition-layer.md`。
- 数据驱动能力必须同步设计 trace/debug 入口。
- 高频逻辑、低频规则、表现动画、React UI 必须分层，不互相穿透。
- Sandbox 是验证场，不是长期玩法承载层。
- 文档是架构的一部分，设计变化必须同步更新文档。

## 开发规则

- 优先保持薄内核：核心包定义协议，第三方库进入 adapter。
- 不允许业务代码直接依赖 Koota、Phaser、GSAP 等底层库，除非该代码本身就是 adapter。
- `src/index.ts` 只做公共出口，不写主要实现。
- 新模块按职责拆分文件：类型、创建函数、运行时实现、adapter 私有类型、测试工具分开。
- 不使用 `innerHTML`、HTML 字符串模板或 `insertAdjacentHTML` 实现交互 UI、游戏内容 UI 或 Editor UI；优先使用 React/组件系统或 DOM API + `textContent`。确需渲染外部 HTML 时必须有清洗边界、测试和 ADR。
- 不提交构建产物、缓存、日志、本地环境文件。
- 不做无关重构，不回滚他人改动。

## 文档维护规则

每个较大改动或工作流结束前，必须判断是否需要更新文档：

- 项目定位、目标、非目标、设计信条变化：更新 `docs/project-design.md`。
- 公共 API 或包边界变化：更新 `docs/architecture.md`。
- 模块最终长期设计、协议、adapter、扩展点变化：更新对应的 `docs/modules/<module>.md`。
- 实现约束、代码质量标准变化：更新 `docs/implementation-principles.md`。
- 新形成的实践、反模式、性能经验：更新 `docs/best-practices.md`。
- 模块专属最佳实践：更新对应 `docs/modules/<module>.md` 的“最佳实践”段落；跨模块通用实践仍写入 `docs/best-practices.md`。
- 具体工作流的状态、任务拆分、review、验证和提交：更新任务系统、PR，或 `docs/implementation/` 下对应工作流文档。
- 开发文档治理规则变化：更新 `docs/development-governance.md`。
- 高影响决策：新增 ADR，文件名格式为 `docs/adr/000X-short-title.md`。

文档不是补充材料，是项目设计的一部分。实现和文档冲突时，必须主动修正其中一方。

新增模块、公共 API、adapter、driver、App Host standard service、standard GameModule helper、Save contributor 或长期测试夹具时，必须判断是否需要补充最佳实践。模块文档里的最佳实践必须是长期设计实践，并明确区分“模块集成”和“模块使用”：集成写一次性装配、lifecycle、profile/driver/adapter/test harness；使用写业务代码和工具日常如何消费该模块。不写当前实现状态、临时计划、完成定义、TODO 或 Sandbox 玩法细节；如果同一实践适用于多个模块，写入 `docs/best-practices.md`，不要在多个模块文档复制同一段。若相关工作流已关闭，必须把可复用结论迁移到长期文档，并把执行记录标记为 Closed 或 Archived。

## 验证命令

提交前至少运行：

```bash
corepack pnpm test
corepack pnpm build
corepack pnpm lint
corepack pnpm format
```

涉及 world/adapter/性能相关改动时，额外运行：

```bash
corepack pnpm bench:world
```

涉及本地前端 app 时，启动并检查页面：

```bash
corepack pnpm dev
```

## 提交流程

- 提交前查看 `git status --short`。
- 只提交与当前任务相关的文件。
- commit message 使用简短祈使句，说明实际完成的工程结果。

## Cursor Cloud specific instructions

These notes are for Cloud Agents starting from an already-provisioned VM (dependencies installed by the update script `corepack pnpm install --frozen-lockfile`). Standard commands live in `README.md` and the `## 验证命令` section above; do not duplicate them here.

- Node/toolchain: CI and this environment target **Node 24** (there is no `.nvmrc`/`engines`; the version is only pinned in `.github/workflows/*.yml`). `nvm` has `default -> 24` set, so login/interactive shells (including `tmux` sessions started with `bash -l`) already resolve to Node 24. Gotcha: a bare non-login exec context can hit an `/exec-daemon/node` shim that is Node 22. If a command unexpectedly runs under Node 22, prepend Node 24 explicitly: `export PATH="$HOME/.nvm/versions/node/v24.19.0/bin:$PATH"`.
- Package manager is **pnpm via Corepack** (pinned `pnpm@11.1.2`); always invoke as `corepack pnpm ...`. First install runs native postinstalls for `esbuild` and `msgpackr-extract`, which are pre-approved via `allowBuilds` in `pnpm-workspace.yaml` (no interactive `pnpm approve-builds` needed).
- Build/test/lint/format are Turborepo tasks and are heavily cached; a warm run may report most tasks as `cached`. `pnpm test` also runs a root `node --test` release-state check before the Turbo test graph.
- No Docker, devcontainer, database, or external broker is required. The two multiplayer demos (`dev:multiplayer`, `dev:outpost`) start a Colyseus authority **in-process** via `tsx` alongside Vite — self-contained, no external service to provision.
- Local dev apps are Vite (bound to `127.0.0.1`). The sandbox (`corepack pnpm dev:sandbox`) is the primary manual validation surface and serves at `http://127.0.0.1:5173/`; it is a scene explorer (Tiny Camp, Combat Range, AI Lab, Navigation Lab, Animation Lab, etc.). Other surfaces: `dev:game`, `dev:three`, `dev:physics2d`, `dev:physics3d`, `dev:outpost`.

<!-- gitnexus:start -->

# GitNexus — Code Intelligence

This project is indexed by GitNexus as **gamekits** (43965 symbols, 125178 relationships, 1106 execution flows).

> Index stale? Run `node .gitnexus/run.cjs analyze --index-only` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? Bootstrap with `npx`, `bunx`, or `pnpm dlx` — e.g. `bunx gitnexus@latest analyze` (npm 11 npx crash; #1939).

## Always Do

- **MUST run impact analysis before editing.** Use `impact({target: "symbolName", direction: "upstream"})` (MCP) or `node .gitnexus/run.cjs impact "symbolName" --direction upstream --repo .` (CLI fallback); report callers, processes, and risk. Never substitute grep for graph analysis.
- **MUST analyze graph changes before committing.** Use `detect_changes({scope: "all"})` (MCP) or `node .gitnexus/run.cjs detect-changes --scope all --repo .` (CLI fallback). `partial: true` or `truncated: true` is not a clean check — a zero means unseen, not unaffected; re-run it. For regression review: `detect_changes({scope: "compare", base_ref: "main"})` or `node .gitnexus/run.cjs detect-changes --scope compare --base-ref "main" --repo .`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- **MUST treat `risk: UNKNOWN` as unresolved, not as low.** An empty caller set is not evidence the symbol is unused — it can also mean the callers are not resolvable by the index (plain-object property access, dynamic dispatch, cross-language calls). `impact` pairs `UNKNOWN` with a `riskNote` saying so. Confirm with a text search before treating the symbol as safe to change or delete; do not proceed on the strength of a zero.
- When exploring unfamiliar code, use `query({search_query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `context({name: "symbolName"})`.
- For security review, `explain({target: "fileOrSymbol"})` lists taint findings (source→sink flows; needs `analyze --pdg`).

## Never Do

- NEVER edit a function, class, or method before MCP/CLI impact analysis.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis, and never read `UNKNOWN` as an all-clear — it means the walk could not answer, which is the one verdict that requires confirming by other means.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit before MCP/CLI graph change analysis.

## Resources

| Resource                                  | Use for                                  |
| ----------------------------------------- | ---------------------------------------- |
| `gitnexus://repo/gamekits/context`        | Codebase overview, check index freshness |
| `gitnexus://repo/gamekits/clusters`       | All functional areas                     |
| `gitnexus://repo/gamekits/processes`      | All execution flows                      |
| `gitnexus://repo/gamekits/process/{name}` | Step-by-step execution trace             |

## CLI

| Task                                         | Read this skill file                               |
| -------------------------------------------- | -------------------------------------------------- |
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus-exploring/SKILL.md`       |
| Blast radius / "What breaks if I change X?"  | `.claude/skills/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?"             | `.claude/skills/gitnexus-debugging/SKILL.md`       |
| Rename / extract / split / refactor          | `.claude/skills/gitnexus-refactoring/SKILL.md`     |
| Tools, resources, schema reference           | `.claude/skills/gitnexus-guide/SKILL.md`           |
| Index, status, clean, wiki CLI commands      | `.claude/skills/gitnexus-cli/SKILL.md`             |

<!-- gitnexus:end -->
