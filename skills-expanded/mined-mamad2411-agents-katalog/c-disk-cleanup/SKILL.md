---
name: c-disk-cleanup
description: 使用场景：用户要求分析C盘空间、清理C盘、生成C盘清理报告、查看磁盘占用。触发词包括"分析C盘"、"C盘清理"、"清理C盘"、"C盘空间"、"磁盘清理"、"总结一份c盘清理分析建议"、"给我一份C盘清理报告"等。
---

# C盘清理分析技能

## 概述

一键扫描 C 盘关键路径，由 AI 为每个条目生成中文描述和风险定级（安全/需确认/危险），生成只读 HTML 分析报告，帮助用户判断哪些可以清理。扫描脚本仅按目录位置分类，所有智能分析由 AI 完成。

## 触发条件

- "分析C盘" / "扫描C盘" / "C盘分析"
- "C盘清理" / "清理C盘" / "C盘空间"
- "磁盘清理" / "看看C盘"

## 工作流程

### 步骤1：运行扫描

```bash
powershell -ExecutionPolicy Bypass -File "${USERPROFILE}\.claude\skills\c-disk-cleanup\scan.ps1"
```

脚本自动完成扫描 → 生成数据 → 生成报告 → 打开浏览器。

首次扫描或发现新路径时，输出会显示 `⚠ N items need AI descriptions`。

### 步骤2：AI 描述与风险定级生成

1. 读取 `~\.cleanup\ai-needed.json`
2. 对每个条目分析路径和名称，生成中文描述（20-80 字）：
   - 说明该目录/文件的用途和内容
   - 给出是否可清理的建议和具体风险提示
   - 分配风险等级：safe（可安全删除）/ confirm（需确认）/ danger（危险勿删）
3. 写入 `~\.cleanup\ai-descriptions.json`，格式：`{"路径": {"description": "...", "risk": "safe|confirm|danger"}}`
4. 重新运行 `python make-report.py` 应用 AI 描述和风险，并重新计算摘要统计

AI 描述和风险定级持久化缓存，后续扫描相同路径时直接复用，仅新增/变更的路径需要重新生成。

### 步骤3：告知用户

汇报关键数据：C 盘使用率、总扫描项数、各类风险项数量和容量。

## 报告功能

生成的 HTML 只读报告包含：

- **页首**：C 盘概览（总容量 / 已用 / 剩余）、使用率进度条（中性色，仅显示占比）、三类风险统计（安全 / 需确认 / 危险及其容量）
- **中/英文切换**：右上角按钮，偏好保存到 localStorage
- **侧边栏**：按类别分组的目录导航，显示每类条目数和总大小，滚动联动高亮（IntersectionObserver 模拟）
- **文件列表**：每个类别一张表格，4 列 — 风险（色标）| 路径 | 大小 | 说明
- **AI 说明**：纯 AI 生成 — 所有条目的描述和风险定级（安全/需确认/危险）均由 AI 分析路径和名称后生成，持久化缓存到 `ai-descriptions.json`
- **风险等级**：安全（绿）/ 需确认（黄）/ 危险（红）
- **清理建议**：根据扫描结果动态生成可操作的清理建议卡片（如 `powercfg -h off`、`cleanmgr`、`dism` 等），含具体命令行

报告不包含交互式清理功能（无复选框、筛选、搜索），用户需自行判断并手动清理。

## 扫描覆盖

| 扫描区域 | 说明 |
|----------|------|
| AppData/Local | 用户本地应用数据（Top 30） |
| AppData/Roaming | 用户漫游应用数据（Top 30） |
| AppData/LocalLow | 低完整性应用数据（Top 15） |
| User Dirs | 用户目录下的子目录（Top 40） |
| Dot Dirs | 用户目录下隐藏目录（`.` 开头） |
| ProgramData | 系统级应用数据（Top 20） |
| System Files | pagefile.sys / hiberfil.sys / swapfile.sys |
| Windows Dirs | Temp / Installer / SoftwareDistribution / Prefetch / Logs / WinSxS |
| Recycle Bin | 系统回收站 |
| Windows.old | 旧版 Windows 备份 |
| Program Files | Program Files 和 Program Files (x86)（Top 25） |
| Desktop | 桌面文件和文件夹 |
| Registry | 启动项孤立注册表键 |

## 风险定级与描述

- **纯 AI 分析**：所有条目的描述和风险等级（安全/需确认/危险）由 AI 根据路径和名称实时分析生成
- **分类**：scan.ps1 仅按目录位置分类（App Local / App Roaming / System 等），不做风险评估
- **白名单过滤**：`~\.cleanup\whitelist.json` 中的路径会被跳过
- **AI 缓存**：AI 生成的描述和风险写入 `ai-descriptions.json`，后续扫描自动复用，仅新增/变更的路径需要重新生成
- **摘要重算**：make-report.py 加载 AI 缓存后重新计算安全/需确认/危险的数量和容量

## 清理建议

报告底部根据扫描结果动态生成清理建议卡片，左色条标记风险等级：

- **安全（绿）**：`powercfg -h off`、`cleanmgr`、清空回收站、npm/pip 缓存等
- **需确认（黄）**：Docker prune、Maven 仓库、MSI 缓存等
- **危险（红）**：页面文件说明、空间严重不足警告等

同时包含通用建议：定期运行磁盘清理、卸载不常用软件、检查下载文件夹。根据 C 盘使用率动态追加空间充裕提示或紧急清理警告。

## 文件位置

| 文件 | 路径 |
|------|------|
| 扫描脚本 | `技能目录/scan.ps1` |
| 报告生成器 | `技能目录/make-report.py` |
| 扫描数据 | `~\.cleanup\data.json` |
| AI 待处理列表 | `~\.cleanup\ai-needed.json` |
| AI 描述缓存 | `~\.cleanup\ai-descriptions.json` |
| HTML 报告 | `~\Desktop\C盘清理分析报告.html` |

## 注意事项

- 扫描使用 PowerShell 并行 Job，可能需要 30-90 秒
- 不要硬编码用户名，使用 `$env:USERNAME` 和 `$env:USERPROFILE`
- 分类和风险完全由 AI 判断，scan.ps1 不包含任何硬编码的规则或模式匹配
- HTML 模板嵌入在 make-report.py 中（`report-template.html` 仅作为生成缓存）
- 表格表头不使用 `position: sticky`（Chromium 渲染 bug）
- 侧边栏底部留白 50vh 确保所有项目可点击
- `history` 和 `whitelist` 不再写入 data.json 输出
