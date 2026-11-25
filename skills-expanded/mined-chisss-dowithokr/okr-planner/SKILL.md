---
name: okr-planner
description: Create hierarchical OKR, delivery act plans, and mapping relationships from GM OKR and the DoWithOKR role tree.
---

# OKR Planner

## 前置条件

- 需要：已确认的 GM OKR 和角色树（`.okr/active.md` 中存在 `## GM OKR` 和 `## 角色树` 区块）。
- 缺失处理：
  - 缺少 GM OKR → 提示先运行 `okr-gm`。
  - 缺少角色树 → 提示先运行 `okr-role-splitter`。

## 前置读取

- 读取 `.okr/active.md`。
  - 文件不存在 → 提示用户先运行 `okr-gm`。
  - 缺少 `## GM OKR` 区块 → 提示 GM OKR 尚未生成。
  - 缺少 `## 角色树` 区块 → 提示用户先运行 `okr-role-splitter`。
- 从 `## GM OKR` 提取所有 GM KR，从 `## 角色树` 提取角色列表和上下级关系。

## 执行规则

- GM OKR 是所有角色 OKR 的唯一源头。
- 下级角色 KR 必须映射到上级 KR。
- 每个角色 Objective 搭配 2-5 个 Key Results。
- 角色 KR 必须符合"交付标准"范式：时间节点 + 交付物 + 质量指标，且质量指标必须是上层 KR 的具体化。
- 使用交付幕表达虚拟进度，不使用现实时间周期承诺。
- 交付幕固定为 M0、M1、M2、M3、M4，可按需求合并或重复。
- 映射关系缺失时，必须提示无人负责或局部完成风险。

## 执行步骤

1. 读取 GM KR 列表和角色树。
2. 为每个角色生成 Objective：
   - 用该角色的职责视角表达目标，而非复述 GM OKR。
   - Objective 必须与该角色的上级 KR 相关。
3. 为每个角色拆解 2-5 个 Key Results：
   - 每个 KR 编号格式：`{角色缩写}-KR{序号}`（如 PD-KR1、PM-KR1、ARCHD-KR1、BE-KR1）。
   - 每个 KR 必须符合"交付标准"范式：时间节点（交付幕）+ 交付物 + 至少一个量化指标。
   - 每个 KR 的质量指标必须是上层 KR 质量指标的具体化（如 GM-KR 要求覆盖率 ≥ 80%，BE-KR 应要求 ≥ 90%）。
   - 每个 KR 标注上级映射（映射到哪个上级 KR）。
   - 每个 KR 标注所属交付幕（M2 或 M3）。
4. 验证映射完整性：
   - 每个 GM KR 至少有一个下级角色 KR 映射到它。
   - 如果存在无人负责的 GM KR → 标记为风险并提示。
5. 验证对齐质量：
   - 检查下层 KR 的交付物是否能支撑上层 KR 的质量指标。
   - 标记"对齐弱"的 KR（交付物与上层质量指标关联不明确）并给出修正建议。
6. 生成交付幕计划表：
   - M0 需求转译幕：GM OKR 获得确认。
   - M1 组织拆解幕：角色树与角色 OKR 完成。
   - M2 方案成型幕：产品和架构形成可执行方案。
   - M3 构建验证幕：研发、测试、交付角色产出证据。
   - M4 收敛复盘幕：上级评分并汇总最终 R。
7. 写入 `.okr/active.md` 和 `.okr/status.md`。

## 输出格式

输出层级 OKR、交付幕计划、映射关系。

必须包含：

- 层级 OKR
- 交付幕计划
- 映射关系
- M0 需求转译幕
- M1 组织拆解幕
- M2 方案成型幕
- M3 构建验证幕
- M4 收敛复盘幕

## 异常处理

- 角色树只有 1 个执行角色：合并 M2 和 M3 为单幕，简化交付幕计划。
- GM KR 无法映射到任何角色：标记为"无人负责"风险，建议用户补充角色或调整 GM KR。
- 角色 KR 数量超过 5 个：建议拆分为多轮交付，每轮聚焦 2-3 个核心 KR。

## 产出写入

- 更新 `.okr/active.md`：
  - 写入 `## 层级 OKR` 区块（每个角色一个三级标题，含上级映射、O 和 KR 列表）。
  - 写入 `## 交付幕计划` 区块。
  - 更新 frontmatter：`current_act: M1`、`last_updated`、`updated_by: okr-planner`。
  - 不修改 `## 甲方需求`、`## GM OKR`、`## 角色树` 区块。
- 创建 `.okr/status.md`：
  - 写入 frontmatter：`version: 1`、`last_updated`、`updated_by: okr-planner`。
  - 根据所有角色 KR 生成初始状态看板表格，所有 KR 状态为"未开始"，进展为 0.0。
