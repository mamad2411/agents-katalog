---
name: similar-color-confusion-trap
description: |
  当用户选择的分类色板中相邻颜色相似度过高时触发，用于警告色盲用户无法区分。触发场景：用户问"这两个蓝色可以吗？"、"颜色太接近了会不会有问题？"、"如何检查颜色是否适合色盲用户？"。不适用于：单色图表、语义色（已有固定配色）。关键 trigger 信号：颜色相似度 / 色盲友好 / 颜色区分 / 相邻颜色。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 7. Don'ts #2
tags: [accessibility, color-blindness, categorical-palette, design-taboo]
related_skills: [categorical-palette-glossary, chart-taboo-principles, semantic-coloring-principles]
---

# Similar Color Confusion Trap（相似色混淆陷阱）

## R (Reading) — 原文引用

> "Don'ts: 不要在分类色板中使用相似度 >80% 的颜色 — 色盲用户无法区分"

## I (Interpretation) — 方法论骨架

**核心问题**：当分类色板中相邻颜色的相似度过高（>80%）时，色盲用户（尤其是红绿色盲，占男性 8%）将无法区分不同数据系列，导致图表失去信息传达能力。

**失败机制**：
1. **色觉缺陷**：红绿色盲用户无法区分红色和绿色，蓝黄色盲用户无法区分蓝色和黄色
2. **相似度过高**：即使正常视力用户勉强可区分，色盲用户完全无法分辨
3. **信息丢失**：用户无法判断哪个柱子/折线代表哪个系列

**正确做法**：分类色板中相邻颜色的相似度必须 ≤80%，并通过工具（如 Coblis 色盲模拟器）验证可区分性。必要时配合图案/纹理辅助区分。

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范中，作者定义了 18 色分类色板，确保相邻颜色有足够的差异：
```css
--chart-c-1: #4B7AFA;  /* 蓝 */
--chart-c-2: #44C2FD;  /* 浅蓝 */
--chart-c-3: #FFCE0E;  /* 黄 */
--chart-c-4: #4DCB73;  /* 绿 */
```
这些颜色在色相环上分布均匀，避免相似色相邻。

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"这两个蓝色可以作为两个数据系列的颜色吗？"
- 前端工程师说"如何检查我的配色是否适合色盲用户？"
- QA 测试人员说"色盲用户反馈无法区分图例，怎么办？"

**关键 trigger 词**：颜色相似度 / 色盲友好 / 颜色区分 / 相邻颜色 / Coblis / 色觉缺陷

## E (Execution) — 可执行步骤

**步骤 1：计算颜色相似度**
- 使用 CIEDE2000 色差公式或简化版 RGB 欧氏距离：
  ```javascript
  function colorSimilarity(hex1, hex2) {
    const r1 = parseInt(hex1.slice(1,3), 16);
    const g1 = parseInt(hex1.slice(3,5), 16);
    const b1 = parseInt(hex1.slice(5,7), 16);
    const r2 = parseInt(hex2.slice(1,3), 16);
    const g2 = parseInt(hex2.slice(3,5), 16);
    const b2 = parseInt(hex2.slice(5,7), 16);
    const distance = Math.sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2);
    return 1 - distance / 441.67; // 归一化到 0-1
  }
  
  const similarity = colorSimilarity('#4B7AFA', '#5C8BFB');
  console.log(`相似度: ${(similarity * 100).toFixed(1)}%`);
  if (similarity > 0.8) {
    console.error('颜色相似度过高，应替换');
  }
  ```

**步骤 2：使用色盲模拟工具验证**
- 在线工具：Coblis (https://www.color-blindness.com/coblis-color-simulator/)
- 上传图表截图，选择"Deuteranopia"（红绿色盲）模式
- 检查是否仍能区分不同数据系列

**步骤 3：替换相似色**
- 如果相似度过高，从品牌色板中选择差异更大的颜色
- 或使用 ENCY-charts 预定义的 18 色分类色板

**步骤 4：添加辅助编码**
- 不依赖单一颜色，配合图案/纹理/标签：
  ```javascript
  // ECharts 示例：使用不同图案
  series: [
    { name: '系列1', type: 'bar', itemStyle: { color: '#4B7AFA' } },
    { name: '系列2', type: 'bar', itemStyle: { color: '#44C2FD' } }
  ]
  // 同时在 Legend 中添加图标或文字标识
  ```

## B (Boundary) — 边界与盲点

**例外情况**：
- 单色图表（仅一个数据系列）
- 语义色（已有固定的成功/警告/危险配色）

**相关 skills**：
- `categorical-palette-glossary` — 分类色板
- `chart-taboo-principles` — 图表禁忌清单
- `semantic-coloring-principles` — 语义化配色原则
