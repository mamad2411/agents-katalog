---
name: wiki-sync-local
version: 3.0.0
description: |
  维护系统元数据层：更新 wiki-index、记录 wiki-log、同步 wiki-sync-state。
  **职责边界：只碰 00-META/ 下的系统文件。不碰内容页（20-AREAS/ / 30-Zettelkasten/ / 40-RESOURCES/ / 60-BLOGS/）。**
  手动触发：创建/删除笔记后补充 wiki-index 和 wiki-log。
  自动触发：会话启动时检测 git 变更，同步状态文件。
argument-hint: "[create|update|delete <笔记路径>]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash
---

# wiki-sync-local

## 触发场景

- 用户创建笔记后，补充 wiki-index 条目和 wiki-log 记录
- 用户删除笔记后，从 wiki-index 移除条目并记录 wiki-log
- 会话启动时自动检测 git 变更并更新状态

## 模式一：手动触发（由 obsidian-note-local 或用户调用）

在笔记创建/删除后调用，只处理元数据层（index + log + state），不修改笔记内容。

### 1. 读取笔记信息

读取笔记 frontmatter，提取：
- `title` / `aliases` — 页面标题
- `content-type` — 类型（moc/concept/sop/atomic...）
- `up` — 父页面
- `description` — 一句话描述（用于 wiki-index 条目）
- `date-created` — 创建日期

### 2. 更新 wiki-index

读取 `00-META/Index/wiki-index.md`，按操作类型处理：

**create**：
- 根据 content-type 和 up 字段找到对应分类
- 在父条目下添加 `	- [[新笔记]] — {{description}}`
- 如果父条目不存在，在对应区域分类下添加完整条目

**delete**：
- 在 wiki-index 中搜索并移除对该页面的引用
- 清除所有子条目

### 3. 记录 wiki-log

追加条目到 `00-META/Log/wiki-log.md`，格式：

**create**：
```markdown
- [YYYY-MM-DD] ingest | 新建 {{content-type}}「{{title}}」
	- 位置：{{相对路径}}
	- 父页面：{{父页面链接}}
```

**delete**：
```markdown
- [YYYY-MM-DD] archive | 移除 {{content-type}}「{{title}}」
	- 原因：{{如用户说明}}
```

### 4. 更新同步状态

更新 `wiki-sync-state.json`：
- `lastSyncTime` → 当前时间
- `lastCommit` → HEAD commit hash

### 5. 提交状态变更

```bash
git add content/00-META/wiki-sync-state.json content/00-META/wiki-log.md content/00-META/Index/wiki-index.md
git commit -m "sync: update wiki-sync-state"
```

## 模式二：自动检测 Git 变更（会话启动时）

### 1. 读取同步状态

读取 `content/00-META/wiki-sync-state.json`，获取 `lastCommit`（上次同步的 commit hash）。

### 2. 检测变更文件

```bash
git diff <lastCommit>..HEAD --name-status
```

过滤 `content/` 目录下的 `.md` 文件，排除：
- `.obsidian/` 目录
- `00-META/wiki-sync-state.json` 自身
- `00-META/wiki-log.md` 自身
- `00-META/wiki-index.md` 自身
- `Inbox/` 目录

### 3. 变更分类处理

根据 git status：
- `A`（新增）→ 记录到日志，标记为 "待 ingest"
- `M`（修改）→ 记录到日志
- `D`（删除）→ 记录到日志

不读取或修改变更文件内容，只记录事件。

### 4. 更新同步状态

将 `wiki-sync-state.json` 的 `lastCommit` 更新为当前 HEAD commit，`lastSyncTime` 更新为当前时间。

### 5. 提交状态变更

```bash
git add content/00-META/wiki-sync-state.json
git commit -m "sync: update wiki-sync-state"
```

### 6. 汇总报告

```
Wiki 同步完成

检测到变更：N 个文件
- 新增：X 个
- 修改：Y 个
- 删除：Z 个
上次同步点：{lastCommit}
本次同步点：{currentCommit}
```