---
name: okr-role-splitter
description: Build a DoWithOKR role tree from GM OKR, including hierarchy, responsibilities, participation reasons, and role pruning notes.
---

# OKR Role Splitter

## 前置条件

- 需要：已确认的 GM OKR（`.okr/active.md` 中存在 `## GM OKR` 区块）。
- 缺失处理：提示用户先运行 `okr-gm` 生成 GM OKR。

## 前置读取

- 读取 `.okr/active.md`。
  - 文件不存在 → 提示用户先运行 `okr-gm` 生成 GM OKR。
  - 文件存在但缺少 `## GM OKR` 区块 → 提示 GM OKR 尚未生成。
- 从 `## GM OKR` 区块提取 GM Objective 和所有 GM KR，作为角色拆解的输入。

## 执行规则

- 先读取 GM OKR，再拆解角色树。
- 默认组织树为 GM 下设 PD 产品总监和 ArchD 技术总监，PD 下设 PM 产品经理、UI 设计师、TW 文档专家/DX，ArchD 下设 BE、FE、QA、DevOps、SEC 等技术角色。
- 小任务可以裁剪角色，但必须说明裁剪原因和风险。
- 每个角色必须有职责、上级和参与原因。
- 角色树用于后续层级 OKR、交付幕和上级评分。

## 执行步骤

1. 读取 `.okr/active.md` 中的 GM OKR，提取所有 GM KR。
2. 评估需求规模，决定组织树裁剪策略：
   - 轻量需求（1-2 个 GM KR，单模块）：保留 GM + 2-3 个核心角色。
   - 中等需求（3-4 个 GM KR，多模块）：保留 GM + PD/ArchD + 4-6 个角色。
   - 复杂需求（5+ GM KR，跨系统）：使用完整默认组织树。
3. 为每个保留的角色确定：
   - 职责：该角色在本次需求中具体负责什么。
   - 上级：直接汇报对象。
   - 参与原因：该角色与哪些 GM KR 相关。
4. 为每个裁剪掉的角色说明：
   - 裁剪原因：为什么本次不需要。
   - 风险：裁剪后哪些能力缺失，由谁承担。
5. 按 `../../references/role-tree-template.md` 格式组织输出。
6. 写入 `.okr/active.md` 的 `## 角色树` 区块。

## 输出格式

使用 `../../references/role-tree-template.md`，并展示角色树、上下级关系、角色职责、参与原因、裁剪说明。

必须包含：

- 角色树
- 上下级关系
- 参与原因
- 裁剪说明

## 异常处理

- GM OKR 只有 1 个 KR 且非常简单：建议最小角色树（GM + 1 个执行角色），提示用户确认。
- GM KR 之间存在职责重叠：在角色职责中标注共享 KR，建议指定主负责人。
- 用户要求自定义角色：接受自定义，但提示该角色不在默认评分链路中，需手动指定上级。

## 产出写入

- 更新 `.okr/active.md`：
  - 写入 `## 角色树` 区块（含 `### 裁剪说明`）。
  - 更新 frontmatter：`current_act: M1`、`last_updated`、`updated_by: okr-role-splitter`。
  - 不修改 `## 甲方需求` 和 `## GM OKR` 区块。
