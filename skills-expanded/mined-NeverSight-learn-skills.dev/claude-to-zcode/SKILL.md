---
name: claude-to-zcode
description: >
  当需要把 `.claude`、已有 `.zcode`、或 `.claude-plugin/.codex-plugin/.zcode-plugin`
  的工程化配置迁移为符合 ZCode 规范的工作区资源或插件包时使用此技能。适用于自动盘点来源、
  比较现有 `.zcode` 差异、迁移 skills/commands/hooks/mcp/agents/templates/scripts，
  并处理 ZCode plugin manifest、hook JSON 协议、命令覆盖、MCP schema 等兼容问题。
when_to_use: >
  用户要求从 Claude Code 或兼容目录迁移到 ZCode；要求检测 `.claude` 与 `.zcode`
  的差异；要求把现有配置整理成 `.zcode/*` 或 `.zcode-plugin/plugin.json`；或遇到
  ZCode plugin、hooks、commands、mcp 配置不生效时。
---

# Claude Code / Plugin → ZCode 迁移指南

## 概述

这个技能不再把任务简化成“把 `.claude` 复制到 `.zcode`”。标准做法是四步：

1. **检测来源**：确认项目里到底有哪些工作区目录和插件目录。
2. **比较现状**：先看现有 `.zcode` / `.zcode-plugin` 与源配置是否已一致、是否有冲突。
3. **选择目标**：决定输出到工作区 `.zcode/*`、插件包 `.zcode-plugin/*`，还是两者并存。
4. **按规范迁移**：对可以直接复制的资源直接迁移，对 hooks / mcp / plugin manifest 这类结构敏感资源做协议转换。

本技能适用于两类目标：

* **工作区迁移**：输出到 `.zcode/skills`、`.zcode/commands`、`.zcode/agents`、`.zcode/templates`、`.zcode/hooks`、`.zcode/config.json`
* **插件迁移**：输出到 `.zcode-plugin/plugin.json` 与插件根目录内的组件/辅助资源

### 边界

* ✅ 管：工程化资源迁移、目录识别、差异分析、ZCode 规范适配、插件清单设计
* ❌ 不管：业务代码迁移、框架升级、功能重写

### 配套资源

遇到复杂迁移时，优先引用同目录下的辅助资源：

* `references/source-discovery-and-diff.md`
* `references/workspace-and-plugin-mapping.md`
* `references/zcode-plugin-spec.md`
* `templates/zcode-config.example.json`
* `templates/zcode-plugin.plugin.json`
* `scripts/inventory-zcode-sources.js`
* `scripts/analyze-zcode-diff.js`

---

## 先做检测，不要先复制

### 必查来源

在任何迁移开始前，先检查这些目录是否存在：

* 工作区来源：
  * `.claude/`
  * `.zcode/`
* 插件来源：
  * `.claude-plugin/`
  * `.codex-plugin/`
  * `.zcode-plugin/`
* 共享资源：
  * `.agents/skills/`

如果可以运行辅助脚本，优先执行：

```powershell
node .\skills\claude-to-zcode\scripts\inventory-zcode-sources.js .
```

如果不能运行脚本，就按下面的 PowerShell 方式手工盘点：

```powershell
$paths = @(
  ".claude",
  ".zcode",
  ".claude-plugin",
  ".codex-plugin",
  ".zcode-plugin",
  ".agents\\skills"
)

foreach ($path in $paths) {
  [pscustomobject]@{
    Path = $path
    Exists = Test-Path $path
  }
}
```

### 检测结论必须包含什么

无论是脚本输出还是手工盘点，结论里至少要说明：

* 发现了哪些来源目录
* 每类资源数量（skills / commands / hooks / mcp / agents / templates / scripts）
* 现有 `.zcode` 是否为空、是否已有同名资源
* 现有 `.zcode-plugin/plugin.json` 是否存在
* 哪些资源可直接迁移，哪些必须转换

---

## 工作区迁移还是插件迁移

### 优先走工作区 `.zcode/*` 的场景

满足以下任一条件时，优先迁移到工作区资源：

* 目标是当前仓库内直接生效
* 资源本身需要随着项目版本一起维护
* 需要使用 `.zcode/agents/*.md`
* 只是迁移 `.claude/*` 到当前项目，而不是要分发插件

### 优先走插件包 `.zcode-plugin/*` 的场景

满足以下任一条件时，优先产出插件包：

* 需要跨项目复用
* 需要通过 marketplace 或本地插件目录安装
* 资源天然是插件组件：`skills` / `commands` / `hooks` / `mcpServers`
* 希望把配置与辅助脚本封装在单独插件根目录里

### 两者都要的场景

以下情况通常要双轨输出：

* 项目内已有 `.zcode/*`，但同时需要整理成可分发插件
* 运行时能力希望由 plugin 提供，而项目内仍保留本地 agents 或模板
* 需要先落地项目，再提炼成可复用插件

### 一个关键限制

根据 ZCode 的插件规范，plugin manifest 真正执行的组件是：

* `skills`
* `commands`
* `hooks`
* `mcpServers`

`agents` 在 plugin manifest 中目前只是**记录字段，不会作为可执行组件运行**。所以：

* 如果 agent 需要在项目中真正生效，优先落到 `.zcode/agents/*.md`
* 如果 agent 只是给插件使用者参考，可以在插件中保留说明，但不要把它当成“插件已完成 agent 迁移”

---

## 先比对现有 `.zcode`，不要盲目覆盖

对每一类资源，都先把来源与目标分成以下五类：

* **可直接迁移**：目标不存在，或目标只是旧副本
* **内容一致**：可跳过
* **需协议转换**：如 hooks、mcp、plugin manifest
* **存在冲突**：同名目标已被本地修改
* **需人工确认**：无法可靠判断语义等价

如果可以运行差异分析脚本，优先执行：

```powershell
node .\skills\claude-to-zcode\scripts\analyze-zcode-diff.js .
```

如果手工执行，最少要按这个顺序比：

1. `.claude/*` vs `.zcode/*`
2. `.claude-plugin` / `.codex-plugin` vs `.zcode-plugin`
3. `.agents/skills/*` 是否与工作区 `.zcode/skills/*` 同名冲突

同名资源处理原则：

* 完全一致：跳过
* 仅源端更新：迁移
* 两端都改过：停止自动覆盖，输出冲突说明并请求确认

---

## 资源迁移总规则

详细矩阵见 `references/workspace-and-plugin-mapping.md`。这里先给执行级规则。

### 1. Skills

* 工作区目标：`.zcode/skills/<name>/SKILL.md`
* 插件目标：plugin root 下的 `skills/` 目录，并在 `plugin.json` 中声明
* 迁移难度：低

规则：

* Claude 与 ZCode 的 `SKILL.md` 基本兼容，可直接复制目录
* 但要检查 frontmatter：
  * `name` 存在
  * `description` 存在
  * `description` 不宜过长
* 若同名 skill 同时出现在 `.agents/skills/` 与 `.zcode/skills/`，`.zcode` 优先

### 2. Commands

* 工作区目标：`.zcode/commands/**/*.md`
* 插件目标：plugin root 下的 `commands/` 目录，并在 `plugin.json` 中声明
* 迁移难度：低

规则：

* ZCode command 是裸 markdown 文件，不要误加 frontmatter
* 嵌套路径在命令名中映射为 `:`
* 同名 command 按发现顺序 first match wins，已有更高优先级命令时不要假设新文件会生效

### 3. Hooks

* 工作区目标：`.zcode/hooks/*` + `.zcode/config.json`
* 插件目标：plugin root 下的 `hooks/` 目录 + `plugin.json` 中的 `hooks`
* 迁移难度：高

核心原则：**保留业务逻辑，重写协议适配**

必须同时处理：

* 事件名：只能使用 7 个合法事件
* `matcher`：大小写敏感，工具名按 ZCode 真实名称匹配
* stdout：必须是严格 JSON
* `decision`：`allow` / `ask` / `deny`
* 工作区 hooks：必须 `hooks.enabled: true`

纯文本输出必须改写为：

```javascript
process.stdout.write(JSON.stringify({
  additionalContext: "这里放注入内容"
}));
```

不要继续输出 Claude 风格字段：

* `continue`
* `systemMessage`
* `decision: "block"`

### 4. MCP

* 工作区目标：`.zcode/config.json` → `mcp.servers`
* 插件目标：`plugin.json` → `mcpServers`
* 迁移难度：中高

规则：

* 工作区配置使用 `mcp.servers`
* schema 严格，未知字段可能导致 server 被丢弃
* 配置文件里的 `${...}` 模板不展开，不要把 plugin 变量写进工作区 `mcp.servers`
* `command` 必须是字符串，`args` 必须是字符串数组

### 5. Agents

* 工作区目标：`.zcode/agents/*.md`
* 插件目标：仅可作为记录性资源保留，不视为已插件化执行
* 迁移难度：中

规则：

* Claude 与 ZCode 工作区 agent 结构兼容，可迁移为 `.md + frontmatter`
* 若来源是 `.codex/agents/*.toml`，先转换为 markdown frontmatter，再进入 `.zcode/agents`
* 不把 plugin manifest 里的 `agents` 当成运行保障

### 6. Templates

* 工作区目标：`.zcode/templates/*`
* 插件目标：plugin 根目录下的辅助文件
* 迁移难度：低

规则：

* 模板不是 plugin manifest 的一等可执行组件
* 在插件中保留时，应由 skill / command / hook 通过相对路径引用

### 7. Scripts

* 工作区目标：`.zcode/scripts/*`（如项目需要）
* 插件目标：plugin 根目录下的 `scripts/` 或同类辅助目录
* 迁移难度：中

规则：

* script 不是 plugin manifest 的顶级执行组件
* 需要被 hooks / commands / skills 显式调用
* 在 Windows 项目中优先给出 PowerShell 或 Node.js 调用示例

---

## 配置转换重点

### `.claude/settings.json` → `.zcode/config.json`

关键差异：

| 项 | Claude | ZCode |
|---|---|---|
| Hooks 开关 | 无需显式开启 | 必须 `hooks.enabled: true` |
| Hooks 结构 | 顶层 `hooks.<Event>` | `hooks.events.<Event>` |
| MCP 结构 | 顶层 `mcpServers` | `mcp.servers` |
| Hook 输出 | 纯文本可注入 | 严格 JSON |
| 变量 | `$CLAUDE_PROJECT_DIR` | `${ZCODE_PROJECT_DIR}` |

优先复用模板：

* `templates/zcode-config.example.json`

Windows / PowerShell 示例：

```powershell
Copy-Item .\.claude\settings.json .\.zcode\config.json -ErrorAction SilentlyContinue
```

但复制后必须继续做结构转换，不能把它当成最终结果。

### 插件 manifest 迁移

当来源是 `.claude-plugin/plugin.json`、`.codex-plugin/plugin.json` 或已有 `.zcode-plugin/plugin.json` 时：

1. 先看 manifest 位置和命名是否符合 ZCode 要求
2. 校对 `name`
3. 校对组件路径是否都在 plugin root 内部
4. 只把真正可执行的组件字段写入默认示例：
   * `skills`
   * `commands`
   * `hooks`
   * `mcpServers`
5. 对 `agents`、`templates`、`scripts` 写清“辅助资产 / 文档资产”的角色

优先复用模板：

* `templates/zcode-plugin.plugin.json`

详细规则见：

* `references/zcode-plugin-spec.md`

---

## 推荐执行流程

### 阶段 1：盘点来源

* 运行 `scripts/inventory-zcode-sources.js`
* 或手工确认 `.claude` / `.zcode` / 各类 plugin 目录

### 阶段 2：分析差异

* 运行 `scripts/analyze-zcode-diff.js`
* 把结果分为：
  * 直接迁移
  * 需协议转换
  * 内容冲突
  * 需人工确认

### 阶段 3：决定输出路径

* 若目标是项目内直接生效：优先工作区 `.zcode/*`
* 若目标是可分发复用：优先 `.zcode-plugin/*`
* 若两者都要：先工作区落地，再抽取 plugin

### 阶段 4：逐类迁移

建议顺序：

1. skills
2. commands
3. agents
4. templates / scripts
5. hooks
6. mcp
7. plugin manifest

原因：前四类更稳定，后面三类更依赖结构与协议。

### 阶段 5：验证

至少验证：

* `SKILL.md` frontmatter 可加载
* command 名与嵌套路径正确
* hooks 事件名、matcher、stdout schema 正确
* `mcp.servers` / `mcpServers` 字段正确
* plugin 组件路径全部位于 plugin root 内
* agent 如果需要运行，必须已经落到 `.zcode/agents/*.md`

---

## 高风险点

### 1. Hooks 输出不是 JSON

症状：

* hook 执行但效果丢失
* 日志里出现 `hook.run.failed`

修复：

* 改为 `process.stdout.write(JSON.stringify(...))`

### 2. `hooks.enabled` 漏掉

症状：

* 工作区 hooks 完全不触发

修复：

* 在 `.zcode/config.json` 中加入：

```json
{
  "hooks": {
    "enabled": true,
    "events": {}
  }
}
```

### 3. 把 plugin `agents` 当成可执行组件

症状：

* plugin 安装成功，但 agent 在会话中不可用

修复：

* 把真正需要运行的 agent 迁移到 `.zcode/agents/*.md`

### 4. MCP 字段名沿用旧格式

症状：

* server 丢失
* Settings -> MCP 中状态异常

修复：

* 工作区用 `mcp.servers`
* 避免在配置文件中使用未知 key
* `command` 用字符串，`args` 用数组

### 5. Windows 上沿用 POSIX shell 示例

症状：

* hooks / commands 在 Windows 中无法执行

修复：

* 优先使用 PowerShell 或 `type: "process"`
* 必要时通过 `node script.js` 显式调用

---

## 与官方技能协作

| 场景 | 优先使用 |
|---|---|
| 需要看 ZCode 资源发现顺序、优先级、配置落点 | `zcode-configuration-guide` |
| Hook 不触发、JSON 输出失败、matcher 不匹配 | `diagnosing-hooks` |
| `/command` 不出现、参数不替换、命令重名被覆盖 | `diagnosing-commands` |
| MCP 服务器不连接、字段不合法、超时 | `diagnosing-mcp` |
| plugin 不显示、manifest 不合法、组件路径越界 | `diagnosing-plugins` |
| skill 不触发、description 不合规、被同名覆盖 | `diagnosing-skills` |

---

## 完整检查清单

### 来源识别

- [ ] 已扫描 `.claude`
- [ ] 已扫描 `.zcode`
- [ ] 已扫描 `.claude-plugin`
- [ ] 已扫描 `.codex-plugin`
- [ ] 已扫描 `.zcode-plugin`
- [ ] 已识别 `.agents/skills` 是否参与共享或覆盖

### 差异分析

- [ ] 已对比 `.claude/*` 与 `.zcode/*`
- [ ] 已对比 plugin 来源与 `.zcode-plugin/*`
- [ ] 同名资源已分类为“一致 / 可迁移 / 冲突 / 需确认”

### 工作区迁移

- [ ] `.zcode/skills/*/SKILL.md` frontmatter 可用
- [ ] `.zcode/commands/**/*.md` 命令名与路径匹配
- [ ] `.zcode/agents/*.md` 仅放真正需要运行的 agent
- [ ] `.zcode/config.json` 含 `hooks.enabled: true`
- [ ] `mcp.servers` 字段符合 ZCode schema

### 插件迁移

- [ ] `.zcode-plugin/plugin.json` 位置正确
- [ ] `name` 合法
- [ ] 组件路径都在 plugin root 内
- [ ] `skills` / `commands` / `hooks` / `mcpServers` 已正确声明
- [ ] `agents` 已明确标注为记录性资源或迁移到工作区
- [ ] `templates` / `scripts` 已作为辅助资产保留并有引用路径

### 验证

- [ ] hooks 输出为有效 JSON
- [ ] command / skill / plugin 描述未因格式错误被加载器丢弃
- [ ] Windows 环境示例命令可执行

---

## 快速参考

```text
先检测，再比对，再分流，再迁移。

工作区迁移：
  .claude/* -> .zcode/*

插件迁移：
  .claude-plugin/.codex-plugin/.zcode-plugin -> .zcode-plugin/*

可直接进 plugin.json 的默认组件：
  skills / commands / hooks / mcpServers

不要误判为已插件化可执行的内容：
  agents

常见高风险项：
  hooks.enabled 漏掉
  hook stdout 不是 JSON
  mcp 字段名不规范
  Windows 仍使用 POSIX shell
```
