---
name: ob-bridge
description: "终端 Claude Code ⇄ Obsidian 的上下文桥。① 卸货：把工作产物(md/html/图片)+可选完整会话 transcript 落到 vault 的 _inbox 暂存区；② 接手：在新会话/新 AI 里查询 _inbox、列出可恢复的会话与文件结构、读 transcript 恢复全量上下文继续。触发词：ob-bridge、落地到 obsidian、卸货到 inbox、从 obsidian 恢复、继续之前的工作、接手 inbox。"
---

<role>终端 Claude Code 与 Obsidian 之间的双向上下文桥。卸货端：把会话产物原样写入 vault 的 _inbox/{日期}-{话题}/，可选连完整 transcript 一起带；接手端：在新会话里从 _inbox 发现并读回之前的上下文继续干。</role>
<purpose>解决"终端结论易逝 + 换环境续不上"：① 把探索/实现产物(及完整上下文)沉淀进本地 Obsidian 暂存区；② 让任何新会话/新 AI（尤其 Obsidian 内的 Claudian）能**发现并读回**这些内容接着干。不进 wiki、无 ceremony。</purpose>
<trigger>

```text
触发词：
- 卸货：ob-bridge、落地到 obsidian、卸货到 inbox、沉淀到暂存区、连上下文带过去
- 接手：从 obsidian 恢复、继续之前的工作、接手 inbox、ob-bridge list、ob-bridge resume、读桥接

示例：
- "ob-bridge browser-automation-migration"（卸货）
- "把刚才的工作连完整上下文带过去"（卸货 + 桥接 transcript）
- "从 obsidian 恢复之前的工作"（接手）
- "ob-bridge list"（列出 _inbox 里可恢复的会话）
```

</trigger>

# Obsidian 上下文桥 (ob-bridge)

> ⚠️ 给「维护本 skill 的人」的硬约束（动手前先读）：
> - **绝不**在本 SKILL.md、示例、或生成的产物里写任何**真实的**本地绝对路径、用户名、vault 名、token/密钥。一律用变量（`$OBSIDIAN_REPO`）或 `<占位符>`。真实值只在运行时解析。
> - 所有外部依赖（ob-router、Obsidian 插件、Claudian）都**前置探测 + 缺失降级**，不假设用户环境。
> - 路径、vault 名、日期等**运行时解析**，不写字面量。

## 一、本质与边界

**本质**：vault 的 `_inbox/` 是「终端 ⇄ Obsidian」的中转区。**卸货**把会话产物（及可选完整 transcript）写进去；**接手**从里面把上下文读回来继续。

**明确不做（硬边界）**：
- ❌ 不提升进 `wiki/`（那是 ob-topic / ob-compile / Claudian 的事）
- ❌ 不写 README / 状态 / manifest / 交接文件（无 ceremony，就一个日期+话题文件夹）
- ❌ 不转换格式（html 直接产出 .html）
- ❌ 不擅自触发 Remotely Save 同步（除非用户要求）
- ❌ 接手模式**只读** `_inbox/`，不改不删里面的东西

## 二、前置检查（新用户视角：缺什么提示什么，能降级就降级）

### 1. 解析 vault 路径 `$OBSIDIAN_REPO`（绝不写死）
优先级解析，存入变量，**全程用变量、不打印写死的绝对路径**：
1. 有 **ob-router** skill → 委托它解析
2. 否则读环境变量 `$OBSIDIAN_REPO`
3. 否则读项目/全局 `CLAUDE.md` 的 `OBSIDIAN_REPO` 配置
4. 都没有 → 询问用户路径，建议持久化

校验 `[ -d "$OBSIDIAN_REPO" ]`，不存在则停下提示。

### 2. 运行时派生
```bash
VAULT_NAME="$(basename "$OBSIDIAN_REPO")"
INBOX="$OBSIDIAN_REPO/_inbox"
DATE="$(date +%F)"
```

### 3. 深链能力 / Claudian 探测（仅卸货用）
- `obsidian://open` 是核心协议，无需插件 → 默认用它。
- 读 `$OBSIDIAN_REPO/.obsidian/community-plugins.json`：含 `obsidian-advanced-uri` 可选增强；含 `claudian` → 正常引导，否则降级为「仅暂存供阅读」。

## 三、卸货流程（dump，默认无摩擦）

1. **话题 slug**：带参数则规整用之；否则从当前工作推断一个简短 slug。
2. **目标文件夹**：`$INBOX/$DATE-<slug>/`（同会话复用追加 / 用户点名已存在则用它 / 否则新建）。
3. **写入产物**：
   ```bash
   mkdir -p "$INBOX/$DATE-<slug>"
   ```
   - 文本/Markdown → Write `.md`；HTML → Write 直接产出 `.html`（不转 md）；图片/二进制 → `cp` 进去。原样保真。
4. **生成交接信息**：
   - 选主产物（优先主 `.md`；只有 html/图片时深链降级为打开 vault）。
   - 拼核心深链：`obsidian://open?vault=<VAULT_NAME>&file=<主产物相对 vault 路径>`（`file` 保留原样 `/`，**不要** `%2F`；编码用 `python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "<相对路径>"`）。
   - 输出：文件夹路径 + 主产物深链 + 一行引导「产物已落 `_inbox/$DATE-<slug>/`，去 Obsidian 用 Claudian 接着干」。

## 四、产出示例（全部占位符）

```
✅ 已卸货 3 个产物到 _inbox：

📁 $OBSIDIAN_REPO/_inbox/2026-06-14-<topic-slug>/
   ├── 对比分析.md
   ├── demo.html
   └── 截图.png

🔗 obsidian://open?vault=<vault-name>&file=_inbox/2026-06-14-<topic-slug>/对比分析.md
👉 去 Obsidian 用 Claudian 接着干，vault 即其工作目录，直接读上面这个文件夹即可。
```

## 五、桥接模式（可选：连完整 transcript 一起卸）

> 用途：要断终端、换 Claudian/新 AI 接着干。摘要是有损的（常 < 完整上下文的 1%）。本模式额外把**本会话完整 transcript** 卸进同一文件夹，让接手方读全量上下文。**默认不开**，用户说「连完整上下文带过去」「完整迁移」时开启。

**⚠️ 安全（transcript 几乎必然含密钥：启动注入的 CLAUDE.md、命令里的 token）**：

1. **是否上云？——先问清/按用户既定偏好**：
   - 默认（最稳）：往 `.remotely-save-ignore` 追加 `_inbox/**/*.jsonl` → transcript 只本机读、不同步上云/手机。
   - 例外（用户明确接受上云，如个人单用户/私有云）：跳过 sync-ignore，transcript 随 vault 同步；此时安全只剩打码，**务必告知残留风险**。
2. **best-effort 打码（始终做）**：**运行时**从用户 `CLAUDE.md`/配置读取已知密钥值，`sed` 替换为 `<REDACTED-*>` 再拷。**skill 绝不内置真实密钥值**；打码追不干净，仅纵深防御。
3. **拷贝**（当前会话 transcript = 项目目录里最新的 .jsonl）：
   ```bash
   PROJ="$HOME/.claude/projects/$(pwd | sed 's#/#-#g')"
   SRC="$(ls -t "$PROJ"/*.jsonl | head -1)"
   # （可选打码后）写到 $INBOX/$DATE-<slug>/transcript-<id>.jsonl
   ```
4. **摘要留指针**：主产物 md 顶部加一句「完整上下文在 `transcript-*.jsonl`，接手的 AI 直接读它」。

## 六、接手/恢复模式（resume：新会话从 _inbox 捡起上下文）

> 用途：在**新会话 / 新 AI**（尤其 Obsidian 内的 Claudian）里，从 `_inbox/` **发现并读回**之前卸下的上下文接着干。这是桥的另一端，回答「没有上下文的新 AI 怎么知道去哪读」。
>
> 触发：用户说「从 obsidian 恢复」「继续之前的工作」「接手 inbox」「ob-bridge list/resume」。

1. **解析 `$OBSIDIAN_REPO`**（同前置检查第 1 步）。
2. **列出可恢复的会话**（扫 `_inbox/`，按日期倒序）：
   ```bash
   ls -dt "$OBSIDIAN_REPO/_inbox"/*/ 2>/dev/null
   ```
   - 空 → 提示「`_inbox/` 暂无内容，可能还没卸过货」，结束。
3. **报告每个候选的文件结构**（让用户/AI 一眼知道有啥、去哪读）：
   ```bash
   ls -la "$OBSIDIAN_REPO/_inbox/<选中文件夹>/"
   ```
   文件角色约定：
   | 文件 | 角色 | 怎么用 |
   |------|------|--------|
   | `transcript-*.jsonl` | **完整逐字上下文** | 读它恢复**全量**（首选） |
   | `*.md` | 摘要 / 产物 | 快速概览、导航 |
   | `*.html` / 图片 | 富产物 | 按需查看 |
4. **恢复并继续**：
   - 用户要「完整接着干」→ 读 `transcript-*.jsonl` 拿全量上下文（含决策来龙去脉），再继续。
   - 只要概览 → 读摘要 `.md`。
   - 默认挑**最新**的文件夹；用户点名某话题则用对应文件夹。
5. **多个候选时**先把列表给用户挑，不擅自假设。

## 七、Check List（执行后自检）

**卸货**：
- [ ] vault 路径经解析、**未写死绝对路径**；前置依赖探测过且缺失降级
- [ ] 深链用核心 `obsidian://open`、`/` 未错编 `%2F`
- [ ] 文件夹 `_inbox/$DATE-<slug>/` 已建、产物原样写入（html 直接产出）
- [ ] 未写 wiki/README/状态、未转格式、未擅自同步

**桥接 transcript（如开启）**：
- [ ] 已按用户偏好定 sync-ignore（默认加；接受上云则跳过且已打码+知会风险）
- [ ] transcript 拷入、完整密钥已 best-effort 打码、摘要留指针

**接手（如使用）**：
- [ ] 只读 `_inbox/`，未改/删；列出了候选与文件结构；按用户选择读 transcript 或摘要

**通用**：
- [ ] skill 内（含示例）未出现任何真实密钥值
