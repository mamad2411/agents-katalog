---
name: wiki
description: >
  LLM 维护的持久化 Markdown 知识库 —— 既可用作个人知识库（~/wiki/），
  也可用于给开源项目做架构 wiki（<repo>-wiki/）。
  触发场景：用户说 "wiki"、"/wiki"、"添加到wiki"、"ingest"、"wiki lint"、
  "wiki add"、"wiki query"、"wiki status"、"添加到知识库"、"导入这篇文章"、
  "收藏这个"、"记到wiki里"、"建一个 wiki"、"给 X 做架构 wiki"。
metadata:
  version: 1.2.0
  author: lanshu
  permissions:
    file-read: true
    file-write: true
    network: true
    shell: true
---

# LLM Wiki Skill

让 LLM 增量构建并维护一个持久化的 Markdown 知识库，基于 [Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

---

## Step 1：定位 wiki root（每次触发先做这件事）

按下列规则**自上而下**判断，命中即停：

| 条件 | wiki root | 模式 |
|---|---|---|
| CWD 或任一上级目录含 `SCHEMA.md` + `index.md` | 该目录 | **code-repo** |
| CWD 是 `~/wiki/` 或其子目录 | `~/wiki/` | **personal** |
| CWD 含 `CLAUDE.md` + `index.md`（且不是项目源码的 CLAUDE.md） | CWD | **personal** |
| 上述都不满足，但用户在说 wiki 操作 | `~/wiki/`（默认） | **personal** |
| 用户明确说"建一个新 wiki" | 走 [Step 4：新建 wiki 引导](#step-4新建-wiki-引导) | — |

**模式的本质区别**：
- **personal**：跟踪多元来源（文章 / 视频 / PDF）的阅读笔记，目录五层（`raw/sources/entities/concepts/syntheses/`），有 reliability 分级
- **code-repo**：跟踪单一开源项目源码的架构 wiki，目录三层（`concepts/entities/changelog/`，可选 `guide/`），结论必带 `文件:行号`

---

## Step 2：读 schema 获取所有规则（一次性）

每次新会话首次触发 wiki 操作时，**先读取**当前 wiki root 的 schema 文件：

- **personal 模式** → 读 `<wiki-root>/CLAUDE.md`
- **code-repo 模式** → 读 `<wiki-root>/SCHEMA.md`

**schema 文件是唯一权威**——所有页面格式、标签体系、frontmatter 字段、ingest 步骤、lint 检查项都在里面。本 SKILL.md **不重复** schema 内容，只做路由。

> 如果 schema 文件缺失，说明这个 wiki 还没正确初始化 → 走 [Step 4](#step-4新建-wiki-引导)。

---

## Step 3：会话启动协议（首次触发时执行）

按顺序：

1. 读 schema（见 Step 2）
2. 读 `<wiki-root>/index.md` —— 了解 wiki 全貌（不读全文，了解有哪些页面）
3. 读 `<wiki-root>/log.md` 最后 10 条 —— 了解最近做了什么
4. 读 `<wiki-root>/inbox.md`（如存在）—— 看是否有待处理项
5. 一句话向用户汇报：「wiki 状态：N 个页面，最近操作 X，待处理 Y 项」

后续操作只要不切换 wiki root 就不重复读这些。

---

## Step 4：新建 wiki 引导

用户在一个**没有现成 wiki 标记**的目录说"建一个 wiki"、"给 X 做架构 wiki"、"做个新知识库" 时：

### 4.1 问清楚类型

```
你这个 wiki 想做什么？
A) 个人知识库 —— 沉淀阅读笔记、跨领域观察（personal 模式）
B) 代码仓库 wiki —— 跟踪一个开源项目的源码架构（code-repo 模式）
```

### 4.2 从模板初始化

本 skill 仓库（默认在 `~/code/lanshu-wiki-skill/`）的 `schema/` 目录有两份模板：

| 类型 | 模板源 | 目标 |
|---|---|---|
| personal | `schema/wiki-personal-CLAUDE.md` | `<wiki-root>/CLAUDE.md` |
| code-repo | `schema/wiki-code-repo-SCHEMA.md` | `<wiki-root>/SCHEMA.md` |

执行（以 personal 为例）：

```bash
SKILL_ROOT="${SKILL_ROOT:-$HOME/code/lanshu-wiki-skill}"
WIKI_ROOT="$HOME/wiki"  # 或用户指定的路径

# 建立五层目录骨架
mkdir -p "$WIKI_ROOT"/{raw,sources,entities,concepts,syntheses,reports,assets}

# 复制权威 schema
cp "$SKILL_ROOT/schema/wiki-personal-CLAUDE.md" "$WIKI_ROOT/CLAUDE.md"

# 初始化必备文件
cd "$WIKI_ROOT"
echo "# Wiki Index" > index.md
echo "# Wiki Log" > log.md
echo "# Wiki Inbox" > inbox.md
```

code-repo 模式同理：目录建 `{concepts,entities,changelog}` 三层，schema 复制 `wiki-code-repo-SCHEMA.md` 到 `<wiki-root>/SCHEMA.md`。

### 4.3 引导用户填模板里的 ⚠️ 字段

读完模板后，搜索 `⚠️` 标记的位置，逐项问用户：

- **personal**：「标签体系」一节 —— 你的领域标签是什么？（给 5 个场景模板供选）
- **code-repo**：「Domain」和「Tag Taxonomy」两节 —— 项目名 / commit hash / 子系统列表 / 项目相关的标签

### 4.4 提示用户长期工作流

- 后续 `/wiki ingest <来源>` 即可开始填充
- code-repo wiki 推荐先做 5 个最核心模块再扩展
- 推荐 wiki 仓库 `git init` 并定期 push 备份

---

## 命令路由表

所有命令的**具体步骤都在 schema 里**。本表只做映射。

| 命令 | 自然语言触发 | 做什么 | 详细规则去哪读 |
|---|---|---|---|
| `/wiki add <来源>` | "加到 wiki"、"收藏" | 追加到 inbox.md，不立即处理 | schema 的 Ingest 节 |
| `/wiki ingest <来源>` | "ingest"、"导入" | 完整 ingest 工作流 | schema 的 Ingest 节 |
| `/wiki inbox` | "看待办" | 列 inbox.md 内容，问是否逐个 ingest | — |
| `/wiki query <问题>` | "wiki 里有 X 吗" | 读 index → 读相关页 → 合成答案 → 可能归档为 synthesis | schema 的 Query 节 |
| `/wiki lint` | "lint 一下" | 按 schema Lint 节扫描，写 `reports/lint-report.md` | schema 的 Lint 节 |
| `/wiki status` | "wiki 现状" | 见下方 status 模板 | — |
| `/wiki deprecate <页>` | "废弃这页" | 标 archived + 加废弃说明 + 移出 index 正常列表 | schema 的 Deprecate 节 |
| `/wiki retract <来源>` | "撤回这来源" | 标 archived + 扫描所有引用页降置信度 | schema 的 Retract 节 |
| `/wiki merge <A> <B>` | "合并这两页" | 内容合并 + 链接全局替换 + 副页归档 | schema 的 Merge 节 |

### status 命令模板

```bash
# 以已定位的 $WIKI_ROOT 为准（Step 1 决定）
echo "=== 页面统计 ==="
find "$WIKI_ROOT" -name "*.md" -not -path "*/\.*" -not -path "*/raw/*" -not -path "*/_archive/*" | wc -l
echo "=== 最近操作 ==="
grep "^## \[" "$WIKI_ROOT/log.md" 2>/dev/null | tail -3
echo "=== 待处理 ==="
[ -f "$WIKI_ROOT/inbox.md" ] && grep -c "^- \[ \]" "$WIKI_ROOT/inbox.md" || echo "(无 inbox)"
```

---

## 跨模式不变的硬规则

不论 personal 还是 code-repo，以下规则都成立（schema 里也会重申）：

- **schema 文件是权威**：当 schema 与本 SKILL.md 冲突时以 schema 为准
- **结论必须可追溯**：personal 用 source-ids，code-repo 用 `文件:行号`；做不到宁可不写
- **先读后写**：更新页面前必须读全文，禁止只看 index 摘要就改
- **去重优先**：创建新页面前必须搜 index.md 是否已有同概念
- **追加而非覆盖**：`raw/` 不可变，`log.md` 只追加，矛盾要标注不要消解
- **中文内容**：wiki 页面正文用中文，frontmatter 字段名保持英文
- **不跨目录污染**：所有路径基于 Step 1 定位的 wiki root，与 CWD 无关

---

## 给开发者：扩展更多模式

`schema/` 目录可以按需放更多模板（如 `wiki-paper-research-SCHEMA.md` 用于文献综述、`wiki-product-research-SCHEMA.md` 用于产品研究）。新模板需要：

1. 文件名格式 `wiki-<scenario>-SCHEMA.md` 或 `wiki-<scenario>-CLAUDE.md`
2. 顶部必须有「使用方式」说明
3. 自包含（不依赖其他 schema）—— agent 单次读取就要能干活

加新模板后，在 [Step 4.1](#41-问清楚类型) 增加对应选项即可。
