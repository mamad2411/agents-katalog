---
name: dev-memory-tidy
description: 批量清理已结构化的 dev-memory 条目（陈旧/重复/错误/模板残留）。触发词："清下过期的"、"看看哪些还成立"、"记忆有重复/旧条目"。不同于 setup（分类未分类）和 graduate（归档+跨分支提炼）。
---

# Dev Memory Tidy

Tidy 是 dev-memory 套件里**已结构化记忆的定期校准入口**。

| 命令 | 输入状态 | 输出状态 | 主要动作 |
|---|---|---|---|
| `setup` | 无序（unsorted.md） | 有序（分类到 decisions/progress/...） | add（分类塞进去） |
| `tidy` | 有序但漂移 | 有序且校准 | delete + edit + reset（破坏性） |
| `graduate` | branch 完成 | 跨分支知识上提 + 归档 | 提炼 + 归档 |

**Announce at start:** 用一句简短的话说明将先扫描当前 branch（默认）或 branch+repo 的所有 entry，由 agent 把相关条目聚合成几个**事项级 proposal**，生成 HTML 让用户在浏览器对每个 proposal accept/reject，导出 plan.json 后再 apply 落盘。

## 核心思路：以"事项 / proposal"为决策单元

旧版 tidy 把每条 entry 暴露给用户做决策，66 条 entry 就 66 个决策点 —— 太重。新版 tidy 让 **agent 聚合相关条目成 proposal**（一个语义单元，对应"做一件事"），用户对 proposal 整体 accept/reject。决策点从 N 条 entry 降到 ~3-8 个 proposal。

五种 proposal action 类型，agent 按**优先级**从大到小挑（越靠后越微观）：

| 类型 | 场景 | 写法 |
|---|---|---|
| `reset-file` | 整个文件骨架都过期了，重置回 v2 模板最干净 | `{"type": "reset-file", "file_key": "unsorted"}` |
| `delete-section` | 整个 H2 section 都该删 | `{"type": "delete-section", "file_key": "overview", "section_idx": 7}` |
| `delete-block` | 一个语义单元（top bullet + 子 bullet + Why/How 段落）整体删 | `{"type": "delete-block", "block_id": "decisions::1::block-0"}` |
| `delete-entries` | 块内删一组 bullet 但保留块 | `{"type": "delete-entries", "ids": ["overview::6::0", "overview::6::1", ...]}` |
| `edit-entries` | 改写一组 entry 文本 | `{"type": "edit-entries", "edits": [{"id": "...", "new_text": "..."}]}` |

**优先级理由**：粗颗粒优先能让 plan.json 短、用户审起来快、orphan paragraph（如 Why/How）自动被吸附进 block 一起删而不需要手动列。同 file 同时存在 reset-file 和其他 action → reset 赢；同 block 同时被 delete-block 和 delete-entries 命中 → block 赢。**只有"块内删几条但保留块"这种精细微调才用 `delete-entries`。**

每个 proposal 还可以打 priority（可选）：

| Priority | 含义 | UI 颜色 |
|---|---|---|
| `P0` | 紧急 / 必删（陈旧到误导，留着会让下个 agent 走错路） | 红 |
| `P1` | 高 / 强烈建议清理 | 橙 |
| `P2` | 中 / 建议清理但保留也行 | 黄 |
| `P3` | 低 / 可选清理 | 蓝 |
| `P4` | 可有可无 / 标记保留 | 灰 |

HTML 卡片按 priority 升序排列（P0 在最上），未打 priority 的排最后。

聚合原则：
- **同因同果合并**：所有"删 demo 资产模板列表"的条目合一个 proposal，不是 8 条 delete
- **section / file 颗粒度优先**：能用 `delete-section` 就别枚举 entries；能用 `reset-file` 就别 `delete-section` 一堆
- **写好 title 和 reason**：title 要让用户一眼看懂"做什么"，reason 解释"为什么"。proposal 是给用户审的，不是给脚本对账的
- **priority 反映 stale 程度而非数量**：一条让下个 agent 误导的过期决策也是 P0；几十条无害模板占位顶多 P3

## DO / DON'T

**Do:**
- 用户说"整理记忆 / 清下过期的 / 看看哪些还成立 / 记忆有重复 / 这条早就不对了"
- 长期主分支记忆累积变多、context 输出看起来杂乱时主动建议
- 做完 graduate 后用户想再校准剩下的内容

**Don't:**
- 拿 tidy 来做"分类无序内容"（那是 setup 的活）
- 拿 tidy 来归档分支或提炼跨分支知识（那是 graduate 的活）
- 在没让用户审 HTML 的情况下直接 apply（destructive，必须人审）
- 把每条 entry 单独做成一个 proposal —— 那只是把决策从 entry 抬到 proposal、用户决策点没减少

## Workflow（三步）

### Step 1: 扫描 —— 拿到 entries / sections / blocks / annotated md 清单

```bash
npx dev-memory-cli tidy prepare \
  [--repo <repo-path>] [--branch <branch-name>] \
  [--scope branch|branch+repo]
```

默认 `--scope branch`，仅处理 `branch/*.md`。需要顺手清 repo 共享层时加 `--scope branch+repo`。

输出节选：

```json
{
  "review_html": "/Users/.../branches/master/tidy_review/review_<ts>.html",
  "open_url": "file:///.../review_<ts>.html",
  "annotated_md": "/Users/.../branches/master/tidy_review/entries.annotated.md",
  "annotated_md_open": "file:///.../entries.annotated.md",
  "hints_summary": {
    "auto_enabled": true,
    "stale_after_days": 30,
    "auto_count": 8,
    "auto_by_label": {"STALE": 5, "ORPHAN": 3},
    "user_count": 0,
    "total_count": 8
  },
  "entry_count": 66,
  "section_count": 22,
  "block_count": 18,
  "proposal_count": 0,
  "entries": [...],
  "sections": [...],
  "blocks": [...]
}
```

第一次跑没 proposals，HTML 空着 —— 这是给 agent 看 entries / sections / blocks 的。

**自动 hints（默认开）**：prepare 默认跑两个轻量启发式 pass，把"值得 review 的 entry"贴标签写进 review.html 的 hint 区：

| hint   | 触发条件                                                                                                       |
| ------ | -------------------------------------------------------------------------------------------------------------- |
| STALE  | 某文件在 `log.md` 里最近一次出现是 `--stale-after-days` （默认 30）天之前 → 文件下所有 entry 标 STALE      |
| ORPHAN | `glossary.md` / `repo_glossary.md` 的某条 entry 的 key phrase（冒号前的内容，≥ 4 字符）在其他 .md 里零引用 |

输出 `hints_summary.auto_by_label` 显示这次 auto 出了多少条、什么类型。用户传 `--hints-json/--hints-file` 时**用户优先**（不会被 auto 覆盖）。完全关掉用 `--no-auto-hints`；调阈值用 `--stale-after-days N`。STALE 不在 log 出现的文件**不标**（避免冷启动一次性给所有文件贴 STALE）。

**🌟 读取顺序（重要）**：第一次 prepare 完，**优先 Read `annotated_md` 文件**而不是去解 stdout 的 JSON entries 数组。annotated md 是一份**带 entry id + block 边界 + orphan paragraph 注释**的原 md 镜像 —— 一次读完同时拿到语义结构 + 所有 id 映射，不用读两次（不像 JSON 把 markdown 拍平丢了上下文）。

annotated md 片段长这样：
```markdown
<!-- block: decisions::1::block-0 -->
- **前端分工（2026-05-14 决定）：**  <!-- id: decisions::1::0 -->
- 徐帅武负责 FE-1+FE-3  <!-- id: decisions::1::1 -->
  - FE-1.1 登录与登出  <!-- (sub-bullet, no id) -->
**Why:** 湛憬禧已经先期介入  <!-- orphan: paragraph -->
<!-- /block -->
```

`<!-- id: ... -->` 行末注释贴在每个 top-level bullet 后；`<!-- block: ... -->` / `<!-- /block -->` 包裹语义单元；`<!-- orphan: paragraph -->` 标记不属于任何 entry 的散段（Why/How 这类）。stdout JSON 的 `entries` / `blocks` 数组用来快速查 id 拼接，但语义理解全靠 annotated md。

### Step 2: agent 把相关条目聚合成 proposals，重跑 prepare 注入

读完 annotated md，**LLM 把相关条目聚合成几个 proposal**，每个 proposal 写好 title + reason + 一组 actions。**优先用粗颗粒 action**：能 `reset-file` 别 `delete-section`；能 `delete-section` 别 `delete-block`；能 `delete-block` 别枚举 `delete-entries`。理由：粗颗粒 plan.json 短、用户审起来快、orphan paragraph 自动跟着块一起删而不用手动列。例：

```json
[
  {
    "id": "p1",
    "priority": "P0",
    "title": "删除 decisions.md 旧版分工决策 block（被 5/15 修正版推翻）",
    "reason": "这个 block 是 5/14 早期分工记录，已被同 section 的 5/15 重新校正决策推翻。两条互斥决策同存会让下个 agent 误以为接 FE-1。delete-block 一次把块头 + 子 bullet + Why/How 段落整体清掉。",
    "actions": [
      {"type": "delete-block", "block_id": "decisions::1::block-0"}
    ]
  },
  {
    "id": "p2",
    "priority": "P0",
    "title": "删除 overview.md 的 v1 残留 section '提交前同步 dev-memory 会话重构'",
    "reason": "整个 section 描述的是 v1 时代的 update / sync 工作，已被 v2 capture 取代",
    "actions": [
      {"type": "delete-section", "file_key": "overview", "section_idx": 7}
    ]
  },
  {
    "id": "p3",
    "priority": "P1",
    "title": "重置 unsorted.md 回 v2 模板",
    "reason": "v1 时代留下的 H3 骨架 + AUTO-GENERATED 块（v1 错位 bug），所有内容都已过期；整体重置最干净",
    "actions": [
      {"type": "reset-file", "file_key": "unsorted"}
    ]
  }
]
```

重跑 prepare 注入：

```bash
npx dev-memory-cli tidy prepare \
  --scope branch+repo \
  --proposals-file /tmp/tidy-proposals.json
```

也可以同时给 `--hints-json`（entry-level）和 `--proposals-json`（proposal-level）—— 不冲突，前者给"未提议"折叠区里的 entry 标颜色，后者驱动主卡片。

### Step 3: 用户在浏览器审 + 导出 plan.json

引导用户：

> 我已经生成 review HTML：`<open_url>`
> 主视图是 N 张 proposal 卡片，按 priority 排序（P0 红色最紧急 → P4 灰色可选）。
> 每张卡片三选一：**accept**（按原方案做）/ **reject**（不动）/ **custom**（写文字反馈让我参考你的思路处理）。默认全部 accept。
> 同意就跳过，不同意点 reject，要按你思路改写就点 custom 写反馈。
> 想看具体动了哪些 entry → 点卡片底部"查看影响 entries"。
> "未提议"折叠区可以扫漏网之鱼。
> 审完点蓝色"导出 plan.json"下载到 Downloads，告诉我路径。

### Step 4: apply（处理 accept；custom 不 apply，交给 agent 后续判断）

```bash
npx dev-memory-cli tidy apply \
  --plan-file ~/Downloads/tidy_plan_<ts>.json \
  [--repo <repo-path>] [--branch <branch-name>]
```

行为：
- **先备份**：scope 内所有 .md 整份 copy 到 `branches/<branch>/tidy_backup_<ts>/` + 写 manifest
- 按 `plan.actions` 落盘（这里只含 accept 的 proposals），执行顺序：**reset-file → delete-section → delete-block → entry-level delete/edit**。每一步从后续 buckets 里 prune 已被覆盖的范围，避免重复操作
- **`custom_proposals` 不 apply**：apply 把它们记到 summary 的"custom proposals (NOT applied)"section，列出每条用户反馈
- 在 `branches/<branch>/tidy_review/summary_<ts>.md` 写一份 summary（accepted/rejected/custom 计数、rewritten 列表、custom 反馈原文、invalid 列表）
- **block_idx 漂移保护**：apply 时 delete-block 会**重新解析**当前文件的 block 结构（不依赖 prepare 时的快照），如果 block_idx 越界（用户中途手改了文件）→ 该 action 进 invalid 列表，不会误删邻块
- **内容指纹保护（可选、推荐）**：plan.json 里的 delete-block 可以附 `expected_content_hash` 触发更强的内容校验。prepare 输出的 `blocks[].content_hash`（16 字符 hex）就是这一份指纹 —— agent 把要删的 block 的 hash 原样 copy 到 action 里即可。apply 时如果 block_idx 没越界但 block 内容已经漂移（用户手动改了块内容、编号未变）→ 该 action 进 invalid，记 `reason: "content_hash_mismatch"` + `expected` / `actual` 字段，不删任何 block。不带 `expected_content_hash` 的 action 行为不变（仅做越界检查），向后兼容旧 plan.json

### Step 5（仅当有 custom）: 读用户反馈，按反馈内容判断怎么处理

如果 plan.json 含 `custom_proposals`，agent 读每条 `user_feedback` 后，**根据反馈内容**决定下一步 —— 不是机械地"再起一轮"：

| 反馈类型示例 | 合适的处理 |
|---|---|
| "不要整段删，只删第一句" / "把 X 改成 Y" | 直接调用 capture / tidy 子命令在对话里完成 |
| "我不确定这个还要不要，你帮我看下细节" | 在对话里跟用户解释 + 一起决定 |
| "先放着不动，下次再看" | 不做事，记到 progress 或下次 tidy 提醒 |
| "原方案不对，重新出几个 proposal 给我看" | 再起一轮 `tidy prepare --proposals-file <revised>` |
| "和当时讨论 X 的结论冲突了" | 先 capture 一条 decision 修订，再视情况 tidy |

原则：custom 是用户给 agent 的开放式反馈，不强制走任何固定流程；agent 像处理任何其他对话一样基于上下文决定。

## plan.json 格式（HTML 导出形态）

```json
{
  "tidy_id": "20260427T160000Z",
  "scope": { "include_repo": false },
  "accepted_proposals": ["p1", "p3"],
  "rejected_proposals": ["p4"],
  "custom_proposals": [
    {
      "proposal_id": "p2",
      "title": "...",
      "original_actions": [...],
      "user_feedback": "不要整段删，只删第一句"
    }
  ],
  "actions": [
    {"type": "delete-entries", "ids": ["overview::6::0", ...]},
    {"type": "reset-file", "file_key": "unsorted"},
    {"id": "extra::1::0", "action": "delete"}
  ],
  "notes": "用户备注"
}
```

字段说明：
- `actions`：accept 的 proposal 中所有 actions 的 flatten + "未提议"折叠区里用户额外标 delete 的 entry-level actions。Apply 不区分来源，按 `type` vs `id` 字段调度
- `accepted_proposals`：审计字段（不影响 apply 行为）
- `rejected_proposals`：用户明确拒绝了哪些（让 agent 知道哪些不该再提）
- `custom_proposals`：用户对 proposal 给了自由文本反馈；apply 跳过这些不动盘，agent 读完反馈后视情况处理（参见 Step 5）

## 设计取舍

- **以 proposal 为决策单元**：把"删 8 条 demo 资产" 折成 1 个决策，不是 8 个；用户从 66 个决策点降到 3-5 个 proposal
- **annotated md 优先于 JSON**：prepare 生成 `entries.annotated.md` 是带 id 注释的原 md 镜像，agent 读这一份就能同时拿到语义结构 + 所有 id，不用读两次（不像 JSON 把 markdown 拍扁丢上下文）
- **block 是语义单元、entry 是 bullet 单元**：block 把 top bullet + 子 bullet + 紧跟的 Why/How 段落聚成一个，专为 agent 的"以决策 / 以 risk 为单位"思考粒度服务；delete-block 自动吸附 orphan paragraph（旧 delete-entries 删不掉的 Why/How 段落问题）
- **HTML 静态文件 + 浏览器**：不开 server，`file://` 协议；和 skill-creator 的 `eval_review.html` 同款 export-download 工作流
- **agent proposals 是建议不是判决**：用户可以 reject 任一个 proposal，也可以从"未提议"折叠区手工标 delete
- **备份永远跑**：tidy 是破坏性动作，备份开销极小（KB 级），不提供 `--no-backup`
- **action 优先级 reset > section > block > entry**：粗颗粒覆盖细颗粒；同 file 多动作时高优先级赢，被覆盖的动作丢弃
- **block_idx 不固化**：plan.json 里的 block_id 在 apply 时**重新解析**当前文件结构来定位（不用 prepare 时的快照），文件中途被改也不会误删邻块
- **不动 manifest.json / artifacts/**：tidy 只整理 prose 类 markdown，结构化数据交给其他命令
- **不动 progress.md 的 AUTO-GENERATED 块**：rewrite 时整块原样保留；section 删除时如果该 section 含 auto 块，**不要**用 delete-section（用 delete-block 或 entry-level 更安全）

## Always / Never

**Always:**
- prepare 第一次跑完，**优先 Read `annotated_md` 文件**（不是 JSON entries 数组）再聚合 proposals。一次读完拿到 block / entry id / orphan paragraph 全部信息
- 每个 proposal 写好 title + reason，title 让用户一眼懂、reason 解释 why
- 优先用粗颗粒 action：reset-file > delete-section > delete-block > delete-entries（粒度从大到小）
- 含 Why/How 段落的决策必删时用 `delete-block` —— 它会自动吸附段落，不用单独处理 orphan
- apply 完看 summary_*.md 确认 accepted proposal 数 / rewritten 数都对得上

**Never:**
- 跳过 HTML 审阅直接 apply（哪怕 proposals 是 agent 自己生成的）
- 给一个 entry 同时塞进 delete 和 edit（apply 以最后一个为准，未定义）
- 给 progress.md 的"自动同步区" section 用 delete-section（auto 块会被一起删掉，下次 capture sync 会重建但中间状态不一致）
- 用 reset-file 然后又给同文件加 delete-section / delete-block / entry actions —— reset 会赢，其他动作徒劳
- 为了删一个"top bullet + Why/How 段落"组成的语义单元而枚举 14 个 delete-entries —— 用一个 `delete-block` 一行搞定
