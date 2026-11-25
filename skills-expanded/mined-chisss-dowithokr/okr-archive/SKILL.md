---
name: okr-archive
description: Manually archive the current OKR cycle and clean up workspace state files, preserving wisdom for capability accumulation.
---

# OKR Archive

## 前置条件

- 需要：`.okr/active.md` 存在（有当前周期数据可归档）。
- 缺失处理：
  - `.okr/` 目录不存在或 `active.md` 不存在 → 提示"无可归档的 OKR 周期"。

## 前置读取

- 读取 `.okr/active.md`，提取甲方需求摘要和当前交付幕。
- 读取 `.okr/status.md`（如存在），统计 KR 完成情况。
- 读取 `.okr/reviews/` 目录（如存在），获取最近一次评分的 GM 最终 R。
- 扫描 `.okr/evidence/` 目录，统计证据文件数量。

## 执行规则

- 用户可在任意时间点手动触发归档。
- 归档前必须展示归档摘要并请求用户确认。
- 归档操作不可逆（但归档内容完整保留在 archive/ 中）。
- wisdom/ 始终保留，不参与归档和清理。

## 执行步骤

1. 读取当前 OKR 状态，生成归档摘要：
   - 甲方需求（一句话）。
   - 当前交付幕（M0-M4）。
   - GM 最终 R（如已评分）。
   - KR 完成统计（已完成/总数）。
   - 参与角色列表。
   - 证据文件数量。
2. 展示归档摘要，请求用户确认。
3. 用户确认后执行归档：
   - 创建 `.okr/archive/<YYYY-MM-DD>-cycle/` 目录。
   - 同一天多次归档时追加序号：`<YYYY-MM-DD>-cycle-2/`。
   - 移动 `active.md` → `archive/<date>-cycle/active.md`。
   - 移动 `status.md` → `archive/<date>-cycle/status.md`（如存在）。
   - 移动 `evidence/` → `archive/<date>-cycle/evidence/`（如存在）。
   - 移动 `reviews/` → `archive/<date>-cycle/reviews/`（如存在）。
   - 为归档目录中的 `active.md` 和 `status.md` 追加 frontmatter：
     - `archived_at: <YYYY-MM-DD>`
     - `archived_reason: manual`
   - 生成 `archive/<date>-cycle/summary.md` 归档摘要文件。
4. 清空工作区：
   - 删除 `.okr/active.md`。
   - 删除 `.okr/status.md`。
   - 删除 `.okr/evidence/` 目录。
   - 删除 `.okr/reviews/` 目录。
5. 输出归档完成确认。

## 输出格式

输出归档操作报告。

必须包含：

- 归档摘要（需求、交付幕、R 分数、KR 统计）
- 归档路径
- 清理的文件列表
- 保留的文件列表（wisdom/、archive/）

## 异常处理

- 用户拒绝确认：不执行任何操作，退出。
- `.okr/active.md` 不存在：提示无可归档内容。
- 归档目录已存在（同名冲突）：自动追加序号。

## 产出写入

- 创建 `.okr/archive/<YYYY-MM-DD>-cycle/` 归档目录及其内容。
- 创建 `.okr/archive/<YYYY-MM-DD>-cycle/summary.md` 归档摘要。
- 删除 `.okr/active.md`、`.okr/status.md`、`.okr/evidence/`、`.okr/reviews/`。
- **不修改** `.okr/wisdom/` 和 `.okr/archive/` 中的已有内容。
