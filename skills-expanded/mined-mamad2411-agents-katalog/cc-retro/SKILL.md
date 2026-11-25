---
name: "cc-retro"
description: "项目复盘与技能评估：使用统计→问题识别→改进追踪→知识沉淀。"
---

# Retro - 项目复盘

## 职责
**统计技能使用 → 检查流程完整性 → 识别问题 → 生成报告 → 知识沉淀（raw only）**

## 复盘流程（5 步）

```
触发 → 数据收集 → 覆盖+完整性检查 → 问题识别 → 生成报告 → 知识沉淀
```

### Step 1: 数据收集

扫描 `wiki/` 目录，统计各技能产出文件数、状态分布。

**升级统计维度**（新增）:

| 维度 | 数据源 | 价值 |
|------|--------|------|
| 各技能使用次数 | wiki/ 各目录文件数 | 基础覆盖度 |
| **各技能跳过率和原因** | 用户反馈 + 流程中断点 | 流程优化依据 |
| **端到端周期时间** | REQ created → FEAT done 的时间差 | 流程效率指标 |
| **回退次数** | design.md 中"设计变更记录"的数量 | 需求/设计质量指标 |
| **stale 文档数** | `stale: true` 的文档数 | 变更传播效率 |
| **KB 检索命中次数** | 各技能 KB 检索是否找到相关经验 | 知识库价值指标 |

### Step 2: 覆盖 + 完整性检查

**合并原 Step 2+3+4**

#### 技能覆盖

| 技能 | 做了？ | 跳过原因合理？ |
|------|--------|---------------|
| cc-init / cc-req / cc-arch / cc-feat / cc-fix / cc-review / cc-kb | ☐ | 如跳过：不知晓/太繁琐/不适用/忘记？ |

跳过原因判断：**不知道有这个技能**或**觉得太繁琐** → 需改进；**不适用当前项目** → 合理。

#### 流程完整性（关键项）

| 技能 | 关键检查项 |
|------|-----------|
| cc-req | 有需求文档？含验收标准？ |
| cc-feat | 模式选择正确？checklist 完成？ |
| cc-review | 有 verdict？request_changes 已追踪？ |

> 代码质量审计不是 retro 的职责。如需评估代码质量，引用 **cc-review** 技能的结论。

### Step 3: 问题识别

收集执行中的问题，对每个问题做 5 Whys 根因分析：

```
问题: {描述}
  Why 1 → Why 2 → Why 3 → 根本原因
```

| 类别 | 示例 |
|------|------|
| 技能定义不清 | 不知道如何执行某步骤 |
| 流程不适配 | 现有流程无法满足需求 |
| 工具 Bug | 脚本报错/路径问题 |
| 绕过技能 | 直接操作未走技能流程 |

### Step 4: 生成报告

输出 `retro/retroYYYYMMDDHHMM.yaml`：

```yaml
meta:
  project_name: "{项目名}"
  retrospect_date: "YYYY-MM-DD"

statistics:
  skills_used: {各技能使用次数}
  files_created: {各目录文件数}

coverage:
  - skill: cc-req; used: true; skipped_reason: null
  # ... 每个技能一行

issues:
  - id: I1; category: skill_definition; severity: medium
    description: "问题描述"; root_cause: "根本原因"; suggestion: "改进建议"

improvements:
  - priority: high; target: "cc-feat/SKILL.md"; action: "具体改动"

knowledge_captured:
  - title: "经验标题"; category: pattern|lesson; source: issue-fix

next_actions:
  - "待办项1"
```

同时输出摘要（控制台）：

```
📊 复盘报告 — {项目名}
✅ 技能覆盖: X/8  ⚠️ 问题: N 个  💡 知识: M 条待整理
📝 改进建议: [高/中/低] 各 N 项   📅 下次复盘: YYYY-MM-DD
```

### Step 5: 知识沉淀

**只写 raw，不生成半正式条目**（整理是 kb 技能的职责）。

> **与 cc-kb 的边界厘清**（新增）:
> - retro 发现的"流程改进经验" → 写入 `raw/`，category 标记为 `lesson`
> - retro 发现的"通用反模式" → 写入 `raw/`，category 标记为 `pattern`
> - retro **不写 decision 类型**（那属于 cc-arch ADR 的职责）
> - 与 kb 已有 lesson 重复的内容，在 raw 中标注 `see_also: {已有条目}`，由 kb 整理时合并

将有价值经验写入 `kb/raw/{type}-{slug}YYYYMMDDHHMM.md`：
- 流程改进经验、工具技巧、常见问题解决方案
- 有代码示例的踩坑教训
- 复盘中发现的问题根因和改进措施

**写入原则**: 有明确复用价值才写，不凑数量。质量 > 数量。

### Step 6: 闭环行动追踪（新增）

> **核心原则: 改进项不能躺在 YAML 里，必须转化为可追踪的行动。**

**改进项分类处理**:

| 改进项类型 | 转化为 | 追踪方式 |
|----------|--------|---------|
| 技能定义改进 | 修改对应 SKILL.md | 下次 retro 检查是否已修改 |
| 流程不适配 | 创建新的 cc-req 需求 | 在 `req/` 中追踪 |
| 工具 Bug | 创建 issue | 在 `issues/` 中追踪 |
| 知识缺失 | 触发 cc-kb 补充 | 检查 `kb/` 是否已补充 |

**强制闭环机制**:
1. 本次 retro 的改进项，写入 `next_actions` 时**必须标注责任人**（用户/技能/工具）
2. **下次 retro Step 2 时**，自动检查上次 `next_actions` 的完成情况
3. 连续 2 次未完成的改进项 → 升级为 issue（写入 `issues/`）

```yaml
# retrospect-report.yaml 中 next_actions 增强格式
next_actions:
  - action: "改进 cc-feat 的模式选择维度"
    owner: "技能定义"  # 用户 / 技能定义 / 工具
    target: "cc-feat/SKILL.md"
    status: pending     # pending | done | escalated
    from_retro: "2026-04-14"  # 来源复盘日期
    origin_retro: "2026-04-14"  # 来源复盘日期 (用于 REQ 关联)
    req_created: false   # 是否已创建关联 REQ
```

### 改进项 → REQ 转化通道

当改进项 `category` 为 `process_gap` 或 `skill_definition` 时，提供转化为正式 REQ 的通道：

**转化条件** (任一满足):
- 改进项涉及新功能/新流程需求
- 改进项需要跨技能协作才能解决
- 用户明确要求"创建需求"

**转化流程**:
1. retro 报告中标记 `req_candidate: true`
2. 用户确认后，调用 cc-req 创建需求文档
3. 新 REQ 的 frontmatter 自动填充 `origin_retro: "{retro-date}"`
4. 更新 retro 报告的 `next_actions.req_created: true` + `req_id: "{slug}"`
5. 下次 retro Step 2 检查该 REQ 的实施状态

## 与其他技能的关系

| 技能 | 关系 |
|------|------|
| cc | 读取路由表，检查流程衔接是否正确 |
| cc-kb | **写入 raw/**（仅原始记录），不越权生成正式条目 |
| cc-review | **引用 cc-review 结论**评估代码质量，不做重复审计 |
| cc-init | 检查 AGENTS.md 索引完整性 |

## 注意事项

- **客观记录**：只记事实不做主观评价
- **聚焦改进**：每個问题必须有改进建议
- **闭环追踪**：上次复盘的改进项本次检查完成情况
- **定期执行**：建议每 2-4 周或每个大版本后
