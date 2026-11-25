---
name: okr-execution-plan
description: Create a delivery verification plan with acceptance criteria, verification methods, and evidence types for each role KR.
---

# OKR Execution Plan（交付验证计划）

## 前置条件

- 需要：已确认的 GM OKR、角色树和层级 OKR（`.okr/active.md` 中存在对应区块）。
- 缺失处理：
  - 缺少层级 OKR → 提示先运行 `okr-planner`。
  - 缺少角色树 → 提示先运行 `okr-role-splitter`。

## 前置读取

- 读取 `.okr/active.md`。
  - 文件不存在 → 提示用户先运行 `okr-gm`。
  - 缺少 `## 层级 OKR` 或 `## 交付幕计划` 区块 → 提示用户先运行 `okr-planner`。
- 从 `## 层级 OKR` 提取所有角色 KR（含时间节点、交付物、质量指标）及上级映射。
- 从 `## 交付幕计划` 提取幕次信息。

## 核心定位

本技能的定位是**交付验证计划**，而非执行计划。系统只关注"怎么验证做到了"，不规定"怎么做"。

- **不输出** step1/step2/step3 任务列表
- **输出** 验收标准 + 验证方法 + 证据类型
- 尊重角色自主权：角色自行决定实现路径，系统只验证结果是否达标

## 执行规则

- 基于已确认的层级 OKR 生成交付验证计划。
- 每个角色 KR 必须有对应的验收标准、验证方法和证据类型。
- 验收标准从 KR 的质量指标中提取，必须可被第三方独立验证。
- 发现无法定义验收标准的 KR 时，标记为"KR 定义不足"并建议回退修正。

## 执行步骤

1. 读取 `.okr/active.md` 中的层级 OKR。
2. 为每个角色 KR 生成验收标准：
   - 从 KR 的质量指标提取可验证的条件。
   - 每个验收标准必须是二值判定（达标/未达标），不允许模糊表述。
   - 示例：KR 质量指标"单测覆盖率 ≥ 90%" → 验收标准"jacoco 报告显示行覆盖率 ≥ 90%"。
3. 为每个验收标准定义验证方法：
   - 描述如何证明达标（运行什么命令、检查什么文件、对比什么数据）。
   - 示例：验证方法"运行 `mvn test` + 查看 jacoco 报告"。
4. 为每个验收标准定义证据类型：
   - 从 `../../references/evidence-spec.md` 的证据类型枚举中选择。
   - 标注需要提供的具体证据（如 commit hash、测试报告截图、API 响应日志）。
5. 检查覆盖完整性：
   - 每个角色 KR 至少有一组验收标准。
   - 每个 GM KR 至少被一个下级 KR 的验收标准间接覆盖。
   - 缺失覆盖 → 标记为风险。
6. 写入 `.okr/active.md`。

## 输出格式

输出交付验证计划表。

| KR ID | 角色 | 验收标准 | 验证方法 | 证据类型 | 上级映射 |
| --- | --- | --- | --- | --- | --- |
| BE-KR1 | BE 后端开发 | jacoco 行覆盖率 ≥ 90% | `mvn test` + jacoco 报告 | 测试 + 文件 | ARCHD-KR1 |
| BE-KR1 | BE 后端开发 | 代码已合入主分支 | `git log --oneline` 确认 | commit | ARCHD-KR1 |
| FE-KR1 | FE 前端开发 | 页面功能可正常操作 | 浏览器手动验证 + 截图 | 截图 | ARCHD-KR2 |

必须包含：

- 交付验证计划
- 验收标准
- 验证方法
- 证据类型
- 上级映射

## 异常处理

- KR 质量指标模糊无法提取验收标准：标记为"KR 定义不足"，建议回退到 `okr-planner` 修正 KR。
- 某个角色所有 KR 均无量化指标：阻塞该角色的验证计划生成，提示补充量化指标。
- 验收标准与证据类型不匹配（如要求截图但角色是 BE）：参考 `../../references/evidence-spec.md` 的角色-证据匹配表调整。

## 产出写入

- 更新 `.okr/active.md`：
  - 写入 `## 交付验证计划` 区块（包含验收标准、验证方法、证据类型的完整表格）。
  - 不修改 `## 交付幕计划` 区块（由 okr-planner 维护的幕级概览保留不变）。
  - 更新 frontmatter：`last_updated`、`updated_by: okr-execution-plan`。
  - 不修改其他区块。
- 更新 `.okr/status.md`：
  - 如果 `okr-planner` 已生成初始看板，保持不变。
  - 如果 `status.md` 不存在，根据层级 OKR 生成初始看板。
