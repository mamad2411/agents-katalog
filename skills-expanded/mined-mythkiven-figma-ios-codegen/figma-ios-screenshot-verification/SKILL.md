---
name: figma-ios-screenshot-verification
description: >-
  Phase 4 visual fidelity check. Read the pre-fetched screenshot.png in the data package,
  compare it visually against generated code, and emit a difference report.
  Use after iOS code generation to confirm visual fidelity.
---

# Figma 视觉还原比对（Phase 4，强制）

代码生成完成后必须执行；用户明确写「无需比对」时方可豁免（须在回复注明）。

## ⛔ 前置硬约束：先做节点对账，再做视觉比对

**视觉比对天然存在盲区**：截图能验"画得对不对"，但**验不出"少画了什么"**——少了一整个区块时，剩下的区块视觉上仍可能"看起来挺对"，造成假阳性的"基本对齐"判断。

因此进入视觉比对**之前**，必须先完成 [`figma-ios-commercial-delivery` §0「节点覆盖率对账」](../figma-ios-commercial-delivery/SKILL.md) 并满足以下任一：

- ✅ 节点覆盖率 = 100%
- ✅ 缺失节点全部属于 [`figma-ios-codegen-workflow` §「全量还原原则」](../../rules/figma-ios-codegen-workflow.mdc)「唯一允许的简化场景」三类，且每条已注明依据

**如果节点覆盖率不达标**：
1. **立即停止**视觉比对（不要先比已实现部分、不要"边比边补"）
2. 按 workflow 的「未完成处置模板」声明缺失节点
3. 回到阶段 2 补齐代码
4. 补齐后再重新进入本 skill

**禁止反模式**：
- ❌ 「视觉差异不大，缺失部分可后续补」——视觉差异低 ≠ 节点齐全
- ❌ 「主要区块已对齐，标签组/段位等可继续完善」——这是把缺失伪装成增量
- ❌ 跳过节点对账直接发"视觉还原比对报告"——会让用户以为已经全量交付

## 数据来源

- 截图：`{data_dir}/screenshot.png`（`figma-ios-preload-data` 阶段 1 已下载）
- 节点数据：`{data_dir}/design.json`（用于核对颜色/字体/尺寸等"事实值"）

> 不再调用 MCP `get_screenshot` 或自行截图。

## 比对维度

| 维度 | 检查要点 | 常见问题 |
|---|---|---|
| 整体布局 | 各区块位置、间距、对齐 | 层级拍平、坐标偏移、漏渲染 |
| 导航栏 | 标题/按钮/高度/背景 | 高度 44 vs 88 弄错 |
| 颜色 | 背景/文字/边框 | 绕过 color_map / 未用 fallback |
| 字体/字重 | 字号、粗细 | Regular/Medium 混淆 |
| 切图 | 位图位置/比例 | imageset 未拷或路径错 |
| iconfont | 图标类型/尺寸/颜色 | 用了错误的 symbol |
| 底部安全区 | 吸底按钮 | 被 Home Indicator 遮挡 |
| 状态切换 | 选中/未选中视觉差异 | 未实现 updateAppearance() |

## 输出报告（强制写入交付物）

```markdown
## 视觉还原比对报告

### ✅ 一致项
- 整体布局：与设计稿一致
- 导航栏：高度用 host.utils.status_bar_nav_height，标题居中
- 颜色：背景 `MKUIStyle.mk_c10()`、文字 `MKUIStyle.mk_c2()`（以 color_map 为准）
- iconfont：查 iconfont_map.json，与稿一致

### ⚠️ 差异项（已处置）
- 「步骤标签」字号：稿 16px，代码生成时取 design.json 实测 14px。已按数据包为准。
- 圆角：图层 1:289 在截图上看似 16，design.json corner_radius=16，已对齐。

### ❌ 无法还原项
- 渐变文字（bg-clip-text + transparent）：UIKit 不原生支持，已用 CAGradientLayer + mask 模拟（轻微差异）
- 服务器下发图片：mock 占位，实际由业务接口注入
```

## 差异处置规则

| 差异类型 | 处置 |
|---|---|
| 代码 bug（颜色/坐标写错）| **立即修复**，重新比对 |
| 数据包字段与截图冲突 | **以数据包为准**（已固化优先级），在报告中说明 |
| 技术限制（MeshGradient 等）| 若有切图则用 imageset；无则代码近似 + 报告说明 |
| 动态内容 | 占位 + 注释说明注入点 |

## 自检清单

- [ ] **前置：节点覆盖率对账已通过（100% 或缺失项全部豁免）**
- [ ] 已读 `{data_dir}/screenshot.png`
- [ ] 按 8 个维度逐一比对
- [ ] 报告分 ✅ / ⚠️ / ❌ 三块
- [ ] 差异已处置或明确告知用户
- [ ] 没有调用 MCP get_screenshot
- [ ] 报告里**没有**出现"差异不大但缺了 X，如需要可补"等降级话术（见 commercial-delivery 「回复纪律」）
