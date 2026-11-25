---
name: check-reasonix-update
description: 检查 DeepSeek-Reasonix 最新版本更新日志，翻译总结并与旧版对比，保存报告到 ./ReasonixUpdateLog/。当用户提到"检查更新"、"查看更新日志"、"版本对比"、"Reasonix 更新"、"DeepSeek-Reasonix"时使用此技能。
---

# Check DeepSeek-Reasonix Update

检查 DeepSeek-Reasonix 最新版的更新日志，翻译总结并对比旧版本变更，将报告保存到 `./ReasonixUpdateLog/`。

---

## 工作流程

### 第一步：检查本地已有总结

1. 查看 `./ReasonixUpdateLog/` 目录是否存在
   - 如果不存在，创建它
2. 列出该目录下所有 `.md` 文件
3. 逐个读取文件内容，从内容中提取已总结的最新版本号
   - 搜索模式：「最新版（vX.Y.Z）」或 `vX.Y.Z`
   - 取最大的版本号作为「已总结的最新版本」
   - 如果没有找到任何文件或版本号，标记为「无已有总结」

### 第二步：获取 GitHub 最新版本

4. 用 `web_fetch` 获取以下 URL 的内容：
   ```
   https://github.com/esengine/DeepSeek-Reasonix/releases
   ```
5. 从页面中找到最新的 CLI release 版本号（格式 `v1.x.x`）

### 第三步：版本对比决策

6. 比较 GitHub 最新版与已总结的最新版本：
   - 如果 **GitHub 最新版 ≤ 已总结版本** → 输出「✅ 已是最新版本 vX.X.X，无需更新」，**停止任务**
   - 如果 **GitHub 最新版 > 已总结版本** 或 **无已有总结** → 继续执行

### 第四步：获取详细更新日志

7. 获取最新版 release 详情页：
   ```
   https://github.com/esengine/DeepSeek-Reasonix/releases/tag/vX.X.X
   ```
8. 同时获取前一个版本的 release 详情页（用于对比基准）

### 第五步：翻译与对比分析

9. 将最新版的更新内容逐条翻译为中文，按功能领域分类：
   - Memory 系统变更
   - MCP / Plugin 变更
   - Desktop / TUI / CLI 变更
   - 架构重构
   - Bug 修复
   - 其他改进

10. 制作新版本 vs 旧版本的详细对比表

### 第六步：保存报告

11. 生成完整的 Markdown 总结报告，内容包含：
    - **版本概览**（版本号、发布时间、对比基准、发布链接）
    - **更新内容中文翻译**（按分类整理，逐条列出）
    - **版本对比表**（新 vs 旧，多维度对比）
    - **关键发现与趋势分析**
    - **报告信息**（生成时间、保存路径）

12. 报告文件命名规则：
    ```
    DeepSeek-Reasonix-v{版本号}-更新日志总结-{YYYY-MM-DD-HHmm}.md
    ```
    例如：`DeepSeek-Reasonix-v1.13.0-更新日志总结-2026-06-28-1530.md`

13. 保存到 `./ReasonixUpdateLog/` 目录

### 第七步：输出摘要

14. 输出最终结果摘要：
    - 检查的版本
    - 报告文件路径
    - 主要更新亮点（3-5 条）

---

## 流程图

```
开始
  │
  ├─ 检查 ./ReasonixUpdateLog/ 目录
  │     │
  │     ▼
  │  读取已有报告，提取已总结的最新版本号
  │
  ├─ 获取 GitHub Releases 页面 → 得到最新版号
  │
  ├─ 比较版本
  │     ├─ 已是最新 → 输出消息，停止 ✅
  │     └─ 有新版本 → 继续 ⏩
  │           │
  │           ├─ 获取详细发布说明
  │           ├─ 翻译 + 按领域分类
  │           ├─ 制作对比表
  │           │
  │           └─ 生成报告 → 保存到 ./ReasonixUpdateLog/
  │
  └─ 输出结果摘要
```

---

## 输出规范

- **报告使用清晰的 Markdown 层级标题**（`#` → `##` → `###`）
- **版本号明确标注**在文件名和报告标题中
- **翻译内容保持技术术语原文**（如 Memory v5、MCP、CLI 等不翻译）
- **对比表使用表格格式**，清晰展示新旧版本差异

---

## 错误处理

| 异常场景 | 处理方式 |
|---|---|
| GitHub 页面获取失败 | 重试 1 次，仍失败则输出错误信息并停止 |
| ReasonixUpdateLog 目录不存在 | 自动创建 |
| 已有报告格式不标准，无法提取版本号 | 标记为「无已有总结」，继续执行 |
