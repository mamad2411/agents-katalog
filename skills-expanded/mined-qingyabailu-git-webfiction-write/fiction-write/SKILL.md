---
name: fiction-write
description: |
  正文写作 + 章节修改。写作支持 Normal（标准流程）和 Deep（增加底本/产物同步）两种建议模式；修改支持 Re-craft（局部事实变更）和 Rewrite（整章重写）两种内建模式。Polish 模式请走 fiction-polish。
  系统根据章节位置给出模式建议，但不代替用户确认；默认一次只处理一章，明确日更时每轮最多三章。
  写作前自动检查章纲是否存在，不存在则阻断。
  触发方式：/fiction-write {章号}、「写第X章」「续写」「继续写」「日更」「下一章」「接着写」「开始写」。
---
# fiction-write：正文写作

每章产出一节可供用户审阅的正文，写入 `正文/第{章号}章-{标题}.md`。
默认字数目标依据题材和细纲确定；不要把平台经验值当成硬性市场事实。

单独说“写作/继续”时只报告项目状态和下一章细纲情况，停在选择菜单，不自动连写。具体停靠点、批量上限和写后证据规则见 [`references/workflow-daily.md`](references/workflow-daily.md)。

## 双模式设计

| 模式 | 适用场景 | 耗时 |
|------|---------|------|
| **Normal** | 常规推进章 | ~30-40 分钟/章 |
| **Deep** | 第 1 章/卷首/卷末/高潮章/里程碑章 | ~60-90 分钟/章 |

## 模式建议

写每章前根据位置和章纲给出建议；用户可以确认或切换：

| 条件 | 推荐模式 |
|------|---------|
| 本章是第 1 章 | Deep |
| 本章是某卷的第 1 章 | Deep |
| 本章是某卷的最后 2 章 | Deep |
| 本章是第 10/20/30... 章（里程碑） | Deep |
| 章纲标记了 `climax: true` / `is_reversal: true` | Deep |
| 章纲标记了 `mode: deep` | Deep |
| 以上都不是的常规章 | Normal |

交互示例：
```
📌 检测到本章是开篇第一章。
建议使用 Deep 深度模式，以确保：
  · 留下完整的底本基线
  · 审查报告与 metrics 落库
  · 提取初始事实供后续查询（LLM 直接执行）

本次使用 Deep 模式？[Y/n]
```

用户可拒绝（n 切换到 Normal）或确认。

## 前置检查

```bash
# SCRIPTS_DIR 由安装宿主指向本仓库或已安装的 scripts/ 目录。
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${CODEX_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}}" where)"
```

### 检查一：是否已开书

检查 `state.json.progress.writing_started`。未开书则阻断：
```
⚠️ 还没正式开书，不能写正文。
先运行 fiction-start 完成开书流程。
```

### 检查二：本章细纲是否存在

检查 `大纲/第{卷号}卷/详细大纲.md` 中是否包含本章章节。
不存在则阻断：
```
⚠️ 第 X 卷的细纲还没做到第 N 章。
先规划：fiction-plan {卷号}
```

### 检查三：本章是否已有正文

检查 `正文/第{章号}章-*.md` 是否存在。
存在则提示：本章已有正文，是否覆盖？[Y/n]

覆盖前必须保留可恢复副本，并记录用户明确允许覆盖；不能因为“自动写回”而静默覆盖手工编辑。

## Normal 模式流程

```
Step 1: 加载上下文
  │ 读取章纲目标（核心事件/情绪目标/爽点/禁区）
  │ 读取最近 3 章摘要
  │ 读取活跃伏笔
  │ 加载本回涉及的设定卡
  │ 确认情绪目标 ❮一句话❯
  │
Step 2: 起草正文
  │ 按需加载对应题材的写作公式和项目文风；参考只借鉴结构与技法
  │ 如有拆文结果，自动引用最相关段落作为参考
  │ agent 起草 + 目标字数/章纲预算核对
  │
Step 3: reviewer 审查
  │ 返回结构化 JSON:
  │   blocking: []     # 阻断问题，必须修复
  │   suggestions: []  # 非阻断建议
  │ reviewer 未调用、失败或结果不完整时标记 unverified，不伪造通过
  │ blocking 定点修复，用户裁决暂不修复的项
  │
Step 4: 去 AI 味 + 格式规范 + 提交
  │ 4a: banned-words 扫描（一级词替换/二级词按语境判断）
  │ 4b: AI 腔模式检测（对称句/判断句/过度副词）
  │ 4c: 人工化改写（拆长句/抽象替换/对话潜台词化/标点去模板化）
  │ 4d: 格式规范化（引号统一、断句、标点）
  │ 4e: scripts/check_prose.py 确定性闸门
  │ 4f: chapter-commit（记录正文路径和内容哈希）
  │ 4g: 按本章已发生事实更新追踪文件
  │     ├─ 追踪/上下文.md 更新
  │     ├─ 追踪/伏笔.md 追加/闭合
  │     ├─ 追踪/时间线.md 追加
  │     ├─ 追踪/角色状态.md 更新
  │     └─ 设定集/配角卡 增量/新建
  │ 4h: 生成章节摘要（仅在项目已有该投影约定时）
  │     写入 .novel/summaries/ch{N}.md
  │ 4i: 生成完成报告，列明已验证与未验证项
  │
Step 5: 里程碑检查（自动，无交互）
  │ 检查当前章节号触发哪个里程碑
  │ 触发时在完成报告中展示建议，不自动开启下一轮写作
```

## Deep 模式增量

在 Normal 流程基础上增加（以下"agent"指由主线 LLM 直接扮演的角色，非独立进程）：

```
Step 1 → context-agent（LLM 扮演）生成完整写作任务书
          （含全部活跃伏笔、底本约束、文风指引）

Step 3 → 审查报告写入 审查报告/第{章号}章审查报告.md
       → review metrics 写入 .novel/reviews/chapter_{N}.metrics.json

Step 4 → data-agent（LLM 扮演）提取三份 artifact:
          fulfillment_result.json（目标完成度）
          disambiguation_result.json（消歧义）
          extraction_result.json（本章新事物）
       → 将三份 artifact 写入 .novel/tmp/
       → chapter-commit --data-artifacts（把已提供的 artifact 记录进 commit）
       → projections retry --chapter {章号}（重建脚本负责的摘要投影）
       → postcommit gate 校验（报告缺失项，不把空产物当成通过）

Step 5 → 三段式 user-report 最终总结
```

> **实现说明**：context-agent、data-agent、reviewer 和 postcommit gate 仍由主线 LLM 或宿主 Agent 执行；仓库脚本负责初始化、状态/体检、artifact 记录、chapter-commit、review-pipeline、摘要 projection 和导出。脚本不会凭空生成 data-agent 事实，也不会声称已经刷新 index、memory、vector 等宿主专属投影。独立 reviewer 不存在时，审查状态必须写成 `unverified`。

## 里程碑提示（写完每章后自动触发）

当前章节号触发对应提示，展示在完成报告中：

| 位置 | 提示内容 |
|------|---------|
| 第 1 章 | "第 1 章已完成。建议立即做一次深度审查：fiction-review 1（deep 模式）。这章是全书的脸面。" |
| 第 5 章 | "连续写了 5 章。建议：fiction-review 1-5 批量审查；检查追踪/伏笔.md；回看第 1 章风格一致性。" |
| 第 10 章 | "第 10 章完成。建议完整 review-pipeline：fiction-review 1-10；运行一致性检查；检查追踪/伏笔.md。" |
| 卷最后一章 | "「{卷名}」全部写完。建议：卷末深度审查；卷摘要归档；规划下一卷：fiction-plan {下一卷号}" |
| 距上次审查 ≥5 章 | "距上次审查过了 5 章。建议：fiction-review {上次+1}-{当前}" |

**压制规则**：
- 同一类型 24 小时内不重复
- 用户刚主动审查过 → 跳过对应提示
- 批量写多章时只在最后写完那章触发
- "每 5 章"基准点是上次审查位置

## 关于写回（只写已确认事实）

每章完成后按实际发生情况更新以下内容，并在完成报告中列出变更：
- 追踪/上下文.md：更新进度、关键决策
- 追踪/伏笔.md：追加新伏笔/标记已回收
- 追踪/时间线.md：追加事件时间锚点
- 追踪/角色状态.md：更新属性/境界/关系变化
- 设定集/配角卡：首次出现且后续复用 → 自动建卡；已有 → 增量补充
- 大纲/第X卷/详细大纲.md：若正文与计划有出入，先报告差异；大纲是计划，不得静默覆盖正文事实

如果文件在上次 commit 后有用户手动编辑，先询问是否保留手动版本。跨章传播必须先输出受影响章节清单，等待用户确认后再改。

## 参考

写作技法参考库（从 story-* 系列继承）：
- genre-writing-formulas.md：各题材创作公式
- hooks-chapter.md / hooks-paragraph.md / hooks-suspense.md：钩子设计
- reversal-toolkit.md：反转设计
- emotional-methods.md / emotional-arc-design.md：情绪设计
- anti-ai-writing.md：去 AI 味核心规则
- banned-words.md：禁用词表
- dialogue-mastery.md：对话技法
- writing-craft.md：通用写作技法

以上参考按需加载，不一次性全部读入。

```bash
# 参考加载示例：按题材加载对应公式
python -X utf8 "${SCRIPTS_DIR}/reference_search.py" \
  --skill write --table genre-writing-formulas \
  --query "{当前题材}" --genre "{当前题材}"
```

## 失败恢复

每步独立，失败补跑不后退。
- 审查缺失 → 重跑 Step 3
- 写回失败 → 只重跑写回步骤
- chapter-commit 未生成 → 重跑 commit
- projection 失败 → 执行 `python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${PROJECT_ROOT}" projections retry --chapter {章号}`；脚本会重建摘要并记录 projection log，宿主专属投影仍需由对应宿主处理

## 延申阅读

- 修改已写章节（大改/重写）→ 本 skill 内建修改模式
- 单纯润色 → fiction-polish
- 单独审查 → fiction-review
- 单独润色/去 AI 味 → fiction-polish
- 批量更新细纲 → fiction-plan
- 查询章节/设定状态 → fiction-query
- 项目体检 → fiction-doctor
- 提取写作模式 → fiction-learn
- 导出/完本 → fiction-export
- 日更停靠与证据规则 → `references/workflow-daily.md`
- 状态追踪最小写回 → `references/state-tracking.md`
- 写后质量闸门 → `references/quality-checklist.md`
- data-agent artifact 与 projection 边界 → `references/data-artifacts.md`
---

## 附录：情绪确认交互示例

Normal 模式下 Step 1 的情绪确认部分：
```
📖 第 7 章写作准备

章纲目标：
  · 核心事件：主角发现李四的账本
  · 情绪目标：紧张 + 期待
  · 本章爽点：李四吃瘪
  · 细纲节点：CBN(发现) → CPN(对峙) → CPN(反转) → CEN(悬念)

最近 3 章摘要：[...]
活跃伏笔：[...]
相关设定：[...]

本章交付什么情绪？（一句话确认）
→ "紧张+期待，李四吃瘪时的畅快感"
```

## 附录：去 AI 味交互示例

Step 4 去 AI 味处理输出：
```
Step 4: 去 AI 味处理
────────────────────
banned-words 扫描：
  🟢 一级词命中 3 处 → 已替换
  🟢 二级词命中 7 处 → 已替换（2 处保留，语境合理）

AI 腔模式识别：
  🟢 对称句密度正常
  🟢 判断式语句 2 处 → 已改写
  ⚠️ 副词修饰偏多（可选处理）
────────────────────
去 AI 味验证：通过 ✓
```

## 附录：完成报告示例

Normal 模式完成后的报告：
```
═══════════════════════════════════════
  第 7 章 完成

  已生成：
  · 正文/第07章-账本.md
  · 审查结果（非阻断信息已标注）
  · 追踪/伏笔.md 已更新（李四的会计 → 已回收）
  · 追踪/时间线.md 已更新
  · git backup ✓

  下一章建议：
  → fiction-write 8
═══════════════════════════════════════
```
---

## 附录：写回清单（底本，按证据执行）

每章完成后只把正文中已经发生的事实写回以下内容，并在报告中说明未更新的文件。

**必写回**：
- 追踪/上下文.md → 更新当前进度、本章关键决策
- 追踪/伏笔.md → 追加新埋伏笔、标记已回收伏笔为 closed
- 追踪/时间线.md → 追加本章事件的时间锚点
- 追踪/角色状态.md → 更新属性/境界/关系的变化

**条件写回**：
- 设定集/配角卡 → 首次出现的具名角色且后续会复用：自动建卡；已有卡：增量补充
- 大纲/第X卷/详细大纲.md → 若实际写作和章纲有出入，先记录差异并等待用户决定是否回填
- 设定集/文风档案.md → Deep 模式下检查文风一致性并追加记录

**Deep 模式下可额外写回**：
- 审查报告/第N章审查报告.md
- .story-system/chapters/chapter_N.json（项目已有该投影时）
- .story-system/commits/chapter_N.commit.json（也可通过脚本单独生成）

写回遵循原则：
- 追踪文件有变动就更新，无变动不写入
- 不把写回当成审查通过证明
- 文件在上次 commit 后有用户手动编辑时，先问“是否保留你的版本？”
- 跨章或跨卷写回先给出影响报告，再由用户确认

## 章节修改模式（内建）

本 skill 同时承担章节修改职责（原 fiction-revise 已合并进来）。一次修订 = 定位变更点 → 备份原稿 → 执行修订 → 探测影响范围 → 用户确认后传播 → 校验一致性。
不能改完一章就宣称全链路完成：必须报告这章改了什么、哪些地方可能受影响、哪些地方实际已同步。

### 修改模式速查

| 模式 | 场景 | 传播 | 耗时 | 路由 |
|------|------|------|------|------|
| **Polish（润色）** | 改表达，不改事实 | 不传播 | 5-10 分钟 | 转交 `fiction-polish` |
| **Re-craft（大改）** | 改了事实（人名/情节/细节），主干不变 | 先报告，确认后传播 | 20-40 分钟 | 本 skill 内建 |
| **Rewrite（重写）** | 整章推翻重来，情节走向变了 | 先报告，确认后刷新 | 60-90 分钟 | 本 skill 内建 |

### 自动检测推荐

| 检测条件 | 推荐模式 |
|---------|---------|
| 用户说"改一下这句""润色""太啰嗦" | Polish → 转交 fiction-polish |
| 用户说"把 XXX 改成 YYY""设定不对" | Re-craft |
| 用户说"这章重写""推倒重来""重来一遍" | Rewrite |
| 修改范围超过一章（"第 5-8 章都要改"） | Rewrite |
| 修改波及设定集（"世界观改了""主角能力改"） | Rewrite（广播） |

### 详细流程

Re-craft 六步流程、Rewrite 六步流程、写回规则、撤销/回滚、修改模式参考详见：
→ [`references/revise-modes.md`](references/revise-modes.md)

进入修改模式时加载该文件获取完整步骤。
---

## 致谢

本 skill 的开发参考了以下开源项目的思路与实现：

- [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer)
- [worldwonderer/oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode)

感谢原作者的开源贡献。
