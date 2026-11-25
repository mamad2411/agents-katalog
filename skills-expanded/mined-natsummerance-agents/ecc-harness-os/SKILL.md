---
name: ecc-harness-os
description: |
  基于 ECC（affaan-m/ECC，Agent Harness 操作系统）为 CLI coding agent 安装与配置整套
  工程纪律：当用户要把「计划→测试→实现→评审→沉淀」流程固化进 Claude Code/Codex/Kimi
  等 harness、跨 harness 共享技能与会话记忆、或对已装 ECC 做 doctor/repair 体检修复与
  AgentShield 安全扫描时触发。边界：不做多 agent 可视化协作仿真，不解决纯网页 chat
  产品的接入，不充当专用记忆层选型方案。
source_project: affaan-m/ECC
tags: [harness, orchestration, claude-code, codex, kimi, agentshield, workflow]
---

# ecc-harness-os

## R | 引用

> "Your agent can write code, but ECC gives it a coordinated engineering system and
> toolbox: it plans before it builds, verifies changes with tests, reviews its own work
> from a fresh context, remembers what matters, and turns repeated wins into reusable
> skills and workflows. … Optimize the context window. Persist everything else."

流水线：`plan -> test -> implement -> review -> verify -> remember -> improve`
来源：<https://github.com/affaan-m/ECC>（README，2026-08-25 抓取）

## I | 骨架

- 定位一句话：单体 agent 的「装机即用的工程操作系统」——把优秀实践装一次，处处生效，而不是每个 prompt 里重讲一遍。
- 流水线七环：plan（/ecc:plan 出蓝图）→ test（tdd-workflow 先写失败测试）→ implement → review（/code-review 新上下文自查）→ verify → remember（/save-session）→ improve。
- 组件清单：68 个专业 agents + 286 个 skills + 94 条命令 + hooks/memory 运行时 + 按语言选择的 rules 包 + AgentShield 配置安全扫描。
- 跨 harness 支持矩阵：Claude Code 原生插件 `ecc@ecc`（推荐）；Codex 原生 marketplace 插件；Kimi Code 托管项目文件 `.kimi-code/`；Cursor/OpenCode/Gemini/Zed/Qwen 等经 `install.sh --target` 适配器；无原生目标走 manual adaptation guide。
- 铁律——同一 harness 只选一条安装路径：插件安装与手动 install.sh 叠加会重复 skills/hooks；Codex 的 sync 与 marketplace 插件同理互斥。
- 运维面：`node scripts/ecc.js list-installed / doctor / repair / uninstall --dry-run`，配 reset 四步清理顺序。
- 记忆与上下文：Unified Memory Vault（`ecc memory`）用统一的本地 Markdown 格式在 Claude/Codex/Hermes/Kimi 等 harness 间共享持久上下文与交接；Plan Canvas 把计划放进回环浏览器里点选批注评审。
- 安装画像：--profile minimal（无 hook 运行时的低上下文档）/ core / full；hook profile 三档 `ECC_HOOK_PROFILE=minimal|standard|strict`。

## A1 | 案例

五人团队要把「先计划、测试先行、写完自查」统一装进各自的 Claude Code。动作：

1. 各自执行 `/plugin marketplace add https://github.com/affaan-m/ECC` + `/plugin install ecc@ecc`；
2. 只补拷需要的规则包：`rules/common` + `rules/typescript` 到 `~/.claude/rules/ecc/`（Claude 插件不分发 rules）；
3. 设 `ECC_HOOK_PROFILE=standard` 统一 hook 力度；
4. 试运行一个功能：`/ecc:plan "加 OAuth 登录"` → tdd-workflow 写失败测试 → 实现 → `/code-review`；
5. 收工 `/save-session`，次日 `/resume-session` 接续。

验收：`/plugin list ecc@ecc` 显示 enabled；doctor 无 error；团队产出物均带 TDD 测试痕迹。

## A2★ | 适用判定

情境一（触发）：「把 plan→test→implement→review 这套工程纪律一次性装进我的 CLI agent」——本 skill 的定义性场景。
情境二（触发）：「Claude Code 和 Codex 并用，想共享同一套技能、规则和会话记忆」——跨 harness 安装与 Memory Vault 归口在此。
情境三（触发）：「感觉装重了/skills 重复/hook 打架，帮我体检修复」——doctor/repair/reset 是运维职能所在。

语言信号（命中任意一条即倾向触发）：
- 「ECC」「ecc@ecc」「harness」「agent 编排框架」「工程流程固化」
- 「tdd-workflow」「/ecc:plan」「code-review 技能包」
- 「AgentShield」「rules 包」「hook profile」「doctor / repair」

与兄弟区分：
- `multi-agent-office`：要多个 agent 同时开工、互相发消息、可视化看谁在干活的协作仿真 → 归兄弟；ECC 面向单个 agent 的流程强化。
- 记忆四兄弟（mem0/hindsight/aep/pkg）：纯记忆能力诉求归它们；ECC 的 memory vault 只是 harness 附带的交接格式，不替代记忆层选型。

## E | 执行步骤

1. 盘点现状防叠加：确认目标 harness 上已有的 ECC 痕迹（`/plugin list`、`codex plugin list`、既有目录）。完成标准：现状清单在手，判定「全新装/已有装/疑似重复装」三种之一。
2. 选唯一路径安装：推荐原生插件命令（Claude：两条 /plugin；Codex：marketplace add+add）。完成标准：`ecc@ecc` 在目标 harness 中 enabled，且未叠加第二条路径。
3. 按需补 rules 包：common + 实际使用的一门语言。完成标准：`~/.claude/rules/ecc/`（或项目级 .claude/rules/ecc/）就位且整目录拷贝。
4. 定 hook profile：minimal/standard/strict 三选一并写入环境。完成标准：`ECC_HOOK_PROFILE` 明确可查，重复 hook 已排除。
5. 主工作流演练：/ecc:plan → tdd-workflow → /code-review 全链走一遍真实小需求。完成标准：三个环节产物齐备（蓝图、失败后转绿的测试、评审意见）。
6. 体检基线：`node scripts/ecc.js doctor`。完成标准：无 error 级问题；如有则按 repair→reset 四步顺序处理并复检。
7. 安全审计（可选）：`npx -y ecc-agentshield scan --path .` 扫 prompts/hooks/MCP/权限/secrets。完成标准：scan 报告产出且高危项清零或有豁免理由。

## B | 边界

不适用：
- 多 agent 办公室式可视化协作仿真（多进程编队、头像楼层）→ 转 `multi-agent-office`。
- 无文件系统能力的纯网页 chat 产品：连 manual adaptation 也拿不到 hooks 与技能发现，不应承诺等效体验。

局限：
- npm `ecc-universal` 2.1.0 尚无引导式 setup（等 2.2.0），当前以原生插件命令为准。
- 跨 harness 功能不对齐（hooks 仅部分平台支持），须查 support matrix 后再承诺。
- 单一维护者高频发版，升级节奏快，需留意 release notes 与命名变更（repo affaan-m/ECC ≠ 插件名 ecc@ecc ≠ npm 名 ecc-universal）。

## 相关 skills

- `multi-agent-office`：多角色协作仿真的姊妹场景
- `mem0-memory-layer` / `hindsight-retrieval` / `agent-experience-persistence`：需要独立记忆层时的专业方案
- `project-knowledge-graph`：代码库结构化理解

## 审计信息

- V1✓ 来源核验：github.com 页面成功抓取 README 主体（尾部截断），安装矩阵/铁律/组件数等关键事实完整
- V2✓ 结构完整：R/I/A1/A2/E/B/相关/审计八节齐备，frontmatter 四要素齐全
- V3✓ 测试通过：test-prompts.json 共 7 条推演全 PASS，见 test-results.md
- 审计日期：2026-08-25
- 来源 URL：<https://github.com/affaan-m/ECC> ；<https://ecc.tools>
