---
name: ob-router
description: "Obsidian 多仓库路由管理。当用户有多个 Obsidian 仓库、需要切换当前激活仓库、注册新仓库、查看仓库列表时触发。触发词：ob-router、切换仓库、切换知识库、设置当前仓库。"
---

<role>Obsidian 多仓库路由中心，管理所有已注册仓库，并维护当前激活仓库的单一真理来源。</role>
<purpose>通过 ~/.claude/ob-router.json 为所有 ob-* skills 提供统一的仓库解析入口，解耦各 skill 与具体仓库路径的绑定。</purpose>
<trigger>

```text
触发词：
- ob-router
- ob-router list
- ob-router use <name>
- ob-router add <name> <path>
- ob-router remove <name>
- ob-router init
- 切换仓库 / 切换知识库
- 设置当前 Obsidian 仓库

示例：
- "ob-router" — 查看当前激活仓库
- "ob-router list" — 列出所有已注册仓库
- "ob-router use work" — 切换到 work 仓库
- "ob-router add personal ~/Documents/personal-vault" — 注册新仓库
- "ob-router init" — 从 CLAUDE.md 中的 OBSIDIAN_REPO 初始化
```

</trigger>
<gsd:workflow xmlns:gsd="urn:gsd:workflow">
  <gsd:meta>config=~/.claude/ob-router.json; focus=repo-routing</gsd:meta>
  <gsd:goal>维护 ~/.claude/ob-router.json 中的多仓库配置，为其他 ob-* skills 提供统一的仓库路径解析。</gsd:goal>
  <gsd:phase>读取 ~/.claude/ob-router.json，识别用户意图（查看/切换/注册/初始化）。</gsd:phase>
  <gsd:phase>执行对应操作并更新配置文件，显示操作结果。</gsd:phase>
</gsd:workflow>

# Obsidian 多仓库路由 (ob-router)

管理本地多个 Obsidian 仓库，作为所有 ob-* skills 的仓库解析中心。

## 配置文件

路径：`~/.claude/ob-router.json`

```json
{
  "active": "personal",
  "repos": {
    "personal": "/path/to/personal-vault",
    "work": "/path/to/work-vault"
  }
}
```

| 字段 | 说明 |
|------|------|
| `active` | 当前激活仓库的名称（对应 repos 的 key） |
| `repos` | 已注册仓库的名称 → 绝对路径映射 |

## 命令详解

### `ob-router`（无参数）— 查看当前状态

读取 `~/.claude/ob-router.json`，展示当前激活仓库：

```
当前激活仓库：personal
路径：/path/to/personal-vault

已注册仓库（2 个）：
  ★ personal  /path/to/personal-vault
    work      /path/to/work-vault
```

若配置文件不存在，提示用户运行 `ob-router init` 初始化。

### `ob-router list` — 列出所有仓库

同无参数模式，额外展示每个仓库的 wiki 文章数（扫描 `{path}/wiki/**/*.md` 文件数）：

```
已注册仓库（2 个）：
  ★ personal  /path/to/personal-vault  (128 篇文章)
    work      /path/to/work-vault      (43 篇文章)
```

### `ob-router use <name>` — 切换激活仓库

1. 读取配置文件，确认 `<name>` 存在于 `repos` 中
2. 如果不存在，列出所有可用名称并报错
3. 将 `active` 字段更新为 `<name>`，写入配置文件
4. 确认展示：

```
✅ 已切换至：work
路径：/path/to/work-vault

所有 ob-* skills 现在将使用此仓库。
```

### `ob-router add <name> <path>` — 注册新仓库

1. 验证 `<path>` 是否为合法绝对路径且目录存在
2. 如果 `<name>` 已存在，询问用户是否覆盖（使用 AskUserQuestion）
3. 将新仓库追加到 `repos` 并写入配置文件
4. 询问用户是否立即切换到新仓库

```
✅ 已注册仓库：research → /path/to/research-vault
是否立即切换到 research？
```

### `ob-router remove <name>` — 移除仓库注册

1. 确认 `<name>` 存在
2. 如果是当前 `active` 仓库，警告并要求用户先切换到其他仓库
3. 从 `repos` 中删除该条目并写入配置文件
4. 提示：**仅移除注册信息，不删除实际仓库目录**

### `ob-router init` — 从现有配置初始化

当用户首次使用 ob-router，但已有 `OBSIDIAN_REPO` 配置在 `~/.claude/CLAUDE.md` 时：

1. 读取全局 `~/.claude/CLAUDE.md`，提取 `OBSIDIAN_REPO` 变量值
2. 如果找到，询问用户为这个仓库起一个名字（默认：`main`）
3. 创建 `~/.claude/ob-router.json`，将其注册为 `active` 仓库
4. 如果用户本地还有其他 Obsidian 仓库，可继续追加（使用 AskUserQuestion 引导）

```
✅ 初始化完成
已将 CLAUDE.md 中的 OBSIDIAN_REPO 导入：
  ★ main  /path/to/my-vault

还有其他 Obsidian 仓库需要注册吗？（可继续添加）
```

## 其他 ob-* skills 如何读取

所有 ob-* skills 在执行前按以下优先级获取 `$OBSIDIAN_REPO`：

```
优先级 1：读取 ~/.claude/ob-router.json
           → 取 repos[active] 的路径

优先级 2：读取全局 ~/.claude/CLAUDE.md 中的 OBSIDIAN_REPO 变量
           （向下兼容旧配置）

优先级 3：AskUserQuestion 询问用户
           → 询问是否同时保存到 ob-router（运行 ob-router add）
```

## 异常处理

| 场景 | 处理 |
|------|------|
| 配置文件不存在 | 提示运行 `ob-router init` 初始化 |
| `active` 对应路径目录不存在 | 警告路径失效，列出其他可用仓库请用户切换 |
| `active` 字段为空或缺失 | 回退到 CLAUDE.md 的 OBSIDIAN_REPO |
| JSON 格式损坏 | 展示损坏内容，引导用户修复或重新初始化 |
| 用户指定了不存在的仓库名 | 列出所有已注册名称 |
