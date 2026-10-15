---
name: project-memory-manager
description: 'KB-first AI project memory manager for full-stack repositories with structured semantic summary extraction and intelligent querying. Use when: (1) initializing project memory, (2) building knowledge bases with call chain analysis, (3) querying method relationships using natural language (e.g., "find methods that filter data"), (4) analyzing code semantics without reading source, or (5) working with Cocos/Pinus/Vue/React/Node.js projects.'
---

# 项目记忆管理器

## 先判断任务类型

- 初始化新仓库时，先读 `references/core/onboarding-playbook.md` 与 `references/core/work-protocols.md`，再运行 `scripts/init_project_memory.js` 和 `scripts/detect_project_topology.js`
- 迁移旧体系时，先读 `references/core/document-boundaries.md`，再运行 `scripts/migrate_legacy_memory.js`，把长期结论迁入 docs，把可重建事实迁入 KB 配置和产物
- 需要全盘扫描整个仓库、学习项目自己的消息/状态协议时，先运行 `scripts/build_project_kb.js --root <repo-root>`，再读 `references/core/project-protocol-learning.md`
- 当问题本质是"为什么这个阶段太早/太晚切换""为什么动画没播完就进下一步"这类业务时序问题时，优先看 `timing / phase / transition` patterns
- 构建或刷新链路 KB 时，先读 `references/core/kb-schema.md`，再按技术栈读取对应 `references/adapters/*.md`，准备配置后运行 `scripts/build_chain_kb.js --config ...`
- 查询调用链、事件、request、state 时，优先运行 `scripts/query_project_kb.js --root <repo-root>`；当范围已经缩到 feature 再用 `scripts/query_kb.js --feature ...`
- 当任务是"给 Cocos 节点挂脚本、补点击事件、给脚本字段绑节点/组件/资源"时，先读 `references/adapters/cocos.md`，再运行 `scripts/cocos_authoring.js`
- 校验技能包或在新环境自举依赖时，先读 `references/core/validation.md`，再在技能根目录运行 `python scripts/validate_skill_runtime.py . --mode auto`
- 需要扩展新技术栈、补拓扑规则或制定前后端协同时，先读 `references/core/adapter-protocol.md` 与 `references/core/fullstack-coordination.md`
- 当任务是"升级这个技能本身"时，永远以 GitHub 源仓库为准，不要直接修改已安装副本目录

## 默认工作流

### 会话开始

- 先读目标仓库根的 `AGENTS.md`
- 再读 `project-memory/state/active-work.json` 与 `project-memory/state/project-profile.json`
- 再读任务相关 docs，优先看 `FAQ.md`、`LOCATE.md`、`CHANGE_GUIDE.md` 和对应 feature 文档
- 当任务是定位入口、事件绑定、request-callback、状态流转或上下游调用时，先查 `project-global KB`，再决定是否做 feature 级或局部源码搜索
- 若目标仓库还没有 `project-memory/`，立即切到"初始化或刷新项目记忆"流程

### 初始化新仓库

- 运行 `node scripts/init_project_memory.js --root <repo-root> --name <project-name>`
- 运行 `node scripts/detect_project_topology.js --root <repo-root>`
- 按 `references/core/onboarding-playbook.md` 的默认顺序补齐 `AGENTS.md`、project overview、active work 与工作协议
- 只在识别出技术栈后读取对应适配器，避免一次性加载全部技术说明

### 迁移旧体系

- 运行 `node scripts/migrate_legacy_memory.js --root <repo-root> --source .kimi`
- 先保留旧体系快照，再迁移长期结论
- 用 `references/core/document-boundaries.md` 判断哪些内容进入 docs，哪些内容应沉淀为 KB 配置或可重建产物
- 迁移后刷新 `project-profile.json`、`active-work.json` 与 feature registry

### 构建或刷新功能 KB

- 先准备 KB 配置 JSON，明确 `featureKey`、入口文件、关注目录与语义标签
- **标准构建**: `node scripts/build_chain_kb.js --config <config-path>`
- **启用结构化摘要**（推荐，支持语义查询）: `node scripts/build_chain_kb.js --config <config-path> --enable-structured-summary`
- 构建后会自动同步 `feature-registry.json` 与 `kb/indexes/features.json`
- 用 `references/core/kb-schema.md` 校验节点类型、边类型与查询面是否覆盖任务需求

#### 结构化语义摘要

启用 `--enable-structured-summary` 后，提取器会分析方法体 AST，生成语义操作序列：
- **操作类型**: filter, map, condition, loop, assignment, method_call, return
- **数据流**: 追踪变量从输入到输出的流转路径
- **复杂度**: 自动评估为 low/medium/high

**优势**:
- AI 不读源码即可理解方法语义（80%场景）
- 支持自然语言查询："找到过滤数据的方法"
- 精确匹配代码模式而非文本搜索

### 查询调用链

**节点 ID 格式说明**:
- 节点 ID 使用 `slugify` 标准化（全小写、路径分隔符转为 `-`），例如 `method:e-xile-xy-client-assets-script-game-poker-liuyangsanshierzhangviewcomp.ts:onroundend`
- **查询时使用原始驼峰命名**（如 `onOpenSmallSettlement`），工具自动匹配

**基础查询**:
```bash
# 方法上下游链路
node scripts/query_chain_kb.js --feature <key> --method <name> --downstream

# 事件订阅关系
node scripts/query_chain_kb.js --feature <key> --event <name>

# 诊断调用链
node scripts/analyze_call_chain.js --feature <key> --caller <method> --callee <method>
```

**语义查询（需启用结构化摘要）**:
```bash
# 查询包含 filter 操作的方法
node scripts/query_chain_kb.js --feature <key> --has-operation filter

# 查询包含条件判断且复杂度>=medium的方法
node scripts/query_chain_kb.js --feature <key> --has-operation condition --min-complexity medium

# 查询数据流向特定变量的方法
node scripts/query_chain_kb.js --feature <key> --data-flow-to <variable>

# 支持的操作类型: filter, map, condition, loop, assignment, method_call
# 复杂度级别: low, medium, high
```

**使用语义查询的场景**:
- "找到所有过滤无效数据的方法" → `--has-operation filter`
- "找到有复杂业务逻辑的方法" → `--min-complexity high`
- "找到处理 historyData 的方法" → `--data-flow-to historyData`
- 若拓扑或抽取结果不稳定，只补适配器规则，不要手改 KB 产物
- 后端仓库可直接使用 `serverRoots`、`moduleRoots`、`dbRoots` 或 `scanTargets.handlers/remotes/modules/routes/schemas`
- Pinus 后端优先参考 `assets/templates/KB_CONFIG_PINUS_BACKEND_EXAMPLE.json`
- 类似 `qyserver` 的仓库优先用绝对 `scanTargets` + `extractorAdapter: "pinus"`，不要在目标仓库里手工同步索引
- **全栈项目（前后端混合）**：使用 `"extractorAdapter": "fullstack"`，同时支持 Cocos 前端和 Pinus 后端解析
- **预制体自动扫描**：`prefabs` 字段为空时，会自动从 `assetRoots` 递归扫描所有 `.prefab` 文件
- **JSDoc 语义提取**：自动提取代码注释中的 @param、@returns、@example 等标签，提供业务语义
- **类型信息增强**：方法节点包含参数类型、返回类型、访问修饰符等完整类型信息
- **导入解析诊断**：构建后显示导入解析成功率，如有未解析导入可使用 `scripts/diagnose_import_resolution.js` 诊断
- **前后端数据流分析**：使用 `scripts/query_dataflow.js` 追踪字段级和方法级的数据流向
- 旧字段 `key` / `name` / `outputDir` 与旧输出文件名仍兼容，但会打印弃用告警

### 构建 project-global KB

- 运行 `node scripts/build_project_kb.js --root <repo-root>`
- 这一步会全盘扫描仓库，产出：
  - `project-memory/kb/project-global/chain.graph.json`
  - `project-memory/kb/project-global/chain.lookup.json`
  - `project-memory/kb/project-global/build.report.json`
  - `project-memory/state/project-protocols.json`
- 这一步不是替代 feature KB，而是提供全局入口、消息协议学习和跨区域链路基座
- 当升级技能版本后，优先重建 `project-global KB`，再重建 feature KB

### 查询链路

- 全局入口优先：`node scripts/query_project_kb.js --root <repo-root>`
- 全局消息查询：`node scripts/query_project_kb.js --root <repo-root> --message <message> --downstream`
- 全局时序查询：`node scripts/query_project_kb.js --root <repo-root> --timing <query>`
- 全局阶段查询：`node scripts/query_project_kb.js --root <repo-root> --phase <query>`
- 全局状态转换查询：`node scripts/query_project_kb.js --root <repo-root> --transition <query>`
- 当范围已经缩小到单一 feature，再运行 `node scripts/query_kb.js --feature <feature-key> ...`
- 若已经在技能根目录，可直接运行 `node scripts/query_kb.js --feature <feature-key> ...`
- 若不在技能根目录，再使用 `node <skill-path>/scripts/query_kb.js --feature <feature-key> ...`
- 若只执行 `--feature <key>`，脚本会先返回 feature 摘要、默认排查顺序、推荐命令和各 KB 文件用途
- 优先用 `--downstream <query>`、`--upstream <query>`，或 `--method/--event/--request/--state <query> --downstream|--upstream`
- `scripts/query_chain_kb.js` 仍保留兼容，但默认推荐入口改为 `scripts/query_kb.js`
- 兼容旧写法 `--from <query> --direction <upstream|downstream>`
- `build.report.json` 是给人看的说明文件；`chain.lookup.json` / `chain.graph.json` / `scan.raw.json` 默认都不建议直接手读
- 当只知道业务语义词时，先试 `--name` 或 `--tag`
- 只有 KB 无法回答时，才做补充性的 `rg` / `grep`

### Cocos 创作辅助

- 先运行 `node scripts/cocos_authoring.js --feature <feature-key> --prefab <prefab-name> --intent profile` 看 prefab 的节点、组件、可绑定字段和已有事件模式
- 如果问题是"节点 / 组件索引是多少""Spine 组件在哪""脚本字段有没有绑上"，优先继续用 profile 过滤：
  - `--node <node-name>` / `--component <component-name>` / `--field <field-name>`
- 新增点击事件时，运行：
  - `node scripts/cocos_authoring.js --feature <feature-key> --prefab <prefab-name> --intent click-event --source-node <source-node> --target-component <target-component> --handler <method>`
- 新增字段绑定时，运行：
  - `node scripts/cocos_authoring.js --feature <feature-key> --prefab <prefab-name> --intent field-binding --component-node <component-node> --component <target-component> --field <field-name> --target-node <node-path>`
  - 或 `--target-component <component-name>` / `--target-asset <asset-name>`
- 先让脚本输出"该改脚本还是改 prefab"的规划，再决定是否真正修改 prefab

### Cocos Profile 查询（避免 PowerShell 转义问题）

**重要**：当需要查询 `cocos-authoring-profile.json` 中的原始配置信息时，**不要**使用 `python -c "..."` 内联代码（PowerShell 对 `[]` 等特殊字符处理有问题），而是使用专用脚本：

```bash
# 列出所有 features
node scripts/query_cocos_profile.js --list-features

# 列出包含 golden 的 features
node scripts/query_cocos_profile.js --list-features --filter golden

# 列出所有 prefabs
node scripts/query_cocos_profile.js --list-prefabs

# 查找包含 goldenEgg 的 prefabs
node scripts/query_cocos_profile.js --list-prefabs --filter goldenEgg

# 查找标题动画节点（如 EggsTitle, PrizeBoxTitle）
node scripts/query_cocos_profile.js --find-node EggsTitle

# 查看特定 prefab 详情
node scripts/query_cocos_profile.js --prefab-detail goldenEgg

# JSON 输出（供脚本解析）
node scripts/query_cocos_profile.js --prefab-detail goldenEgg --json
```

### 会话收口

- 更新 active work 或对应工作文档
- 结构变化时刷新 KB 与索引
- 长期认知变化后更新 docs
- 高频修复优先补 `FAQ.md`、`LOCATE.md`、`CHANGE_GUIDE.md`

### 升级这个技能本身

- 永远不要把 `<installed-skill-path>` 或其它已安装副本当作最终修改目标
- 正确流程是：修改 GitHub 源仓库 -> 校验 -> commit/push -> `npx skills update`
- 技能升级完成后，必须在技能根目录执行 `node scripts/rebuild_kbs.js --root <project-root>` 重建现有 KB
- 如果当前查询脚本提示 `[stale-kb]`，说明 KB 还是旧技能版本构建的，先重建再继续分析

## 环境依赖

技能自带 TypeScript 运行时（位于 `node_modules/typescript`），不依赖目标项目的 TypeScript 安装：
- **AST 解析**: 使用技能自己的 TS 解析器分析代码结构
- **版本兼容性**: 技能使用 TypeScript 6.x，支持最新 TS/JS 语法
- **无需项目安装**: 目标项目即使没有安装 typescript，技能也能正常工作

如遇到 TypeScript 相关问题：
```bash
# 重新安装技能依赖
cd <skill-install-path>
npm install
```

## 故障排除

常见问题及解决方案见 `references/core/troubleshooting.md`：

- **技能版本不更新** - `npx skills update` 无效
- **安装路径混乱** - 脚本找不到文件
- **残留文件报警告** - 清理临时配置
- **路径解析问题** - Windows 大小写问题
- **调用链断裂** - 诊断导入解析
- **构建失败** - 检查清单

## 按需读取这些 references

- 接管与首次落地：`references/core/onboarding-playbook.md`
- 日常协作顺序：`references/core/work-protocols.md`
- docs 与 KB 边界：`references/core/document-boundaries.md`
- KB schema 与查询面：`references/core/kb-schema.md`
- 项目协议学习：`references/core/project-protocol-learning.md`
- 全栈协同：`references/core/fullstack-coordination.md`
- 适配器扩展规则：`references/core/adapter-protocol.md`
- 校验与环境自举：`references/core/validation.md`

## 核心规则

- `docs` 是长期结论层
- `KB` 是可脚本重建事实层
- 不要把全仓库搜索当作第一轮定位动作
- 不要把穷举方法表直接灌进长期 docs
- 不要手改 KB 产物
- 结构变化后刷新 KB
- 长期认知变化后更新 docs
- 优先补脚本、配置或适配器，不要把一次性推理结果写成长期协议
- 依赖 `process.cwd()` 的脚本要先切到目标仓库根；带 `--root` 的脚本可以从任意目录运行
- **避免使用 `python -c "..."` 内联代码**（PowerShell 转义问题），优先使用 Node.js 脚本或 Python 文件
