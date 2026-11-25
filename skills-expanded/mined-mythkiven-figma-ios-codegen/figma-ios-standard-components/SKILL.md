---
name: figma-ios-standard-components
description: >-
  从 figma-ios-preload-data 数据包（design.json）识别标准 UI 组件类型（Selector、Stepper、Toggle、Tag Group 等），
  提取布局模式和通用特征，指导后续状态提取和代码生成。
  Use when identifying component type from Figma, or when user mentions
  Selector、Stepper、Toggle、标准组件、通用组件、组件类型识别。
---

# Figma 标准组件类型识别

## 职责边界

- ✅ 识别组件是**什么类型**（Selector / Stepper / Toggle / Tag Group）
- ✅ 提取**布局模式**（水平/垂直/Flow）和**结构特征**（三段式、并列节点等）
- ❌ 不提取各状态的视觉特征 → 见 [figma-ios-component-state-recognition](../figma-ios-component-state-recognition/SKILL.md)
- ❌ 不生成 updateAppearance() 代码 → 同上
- ❌ 不处理业务逻辑

---

## ⚡ QUICK_REF

```
数据来源：design.json[node]（VECTOR/INSTANCE/SYMBOL 已展开，fills/strokes/corner_radius/opacity 已规范化）

多个并列节点 + 样式不同 + 等宽  → Selector
多个并列节点 + 样式不同 + 不等宽 → Tag Group
三段式：[减] [值] [加]          → Stepper
两种状态（开/关）               → Toggle
```

---

## 生成代码前的对比流程（VECTOR 子节点）

```
1. 从 design.json 取出所有子节点（已含 `fills` / `strokes` / `corner_radius` / `opacity` / `vector_geometry`）
2. 对比同类节点的 `fills[].color`（`rgba` 已含 alpha）、`strokes[].color`（**无** `strokes[].visible`：不可见 stroke 阶段 1 已丢弃）、`corner_radius`
3. 验证对称性（Stepper 的减号/加号 fills 应一致）
4. 再生成代码
```

> 阶段 2 不再调 Figma REST API；所有字段都在数据包里。旧名 `vector_paths` / `fills[].opacity` / `strokes[].visible` **不要再读**。

---

## 组件类型识别

### 决策树

```
有多个并列同类节点？
  └─ 是 → 节点宽度是否相等？
          ├─ 是 → 样式有差异？ → Selector（单选 or 多选）
          └─ 否 → 是否可换行？ → Tag Group
有三个子节点，水平排列，左右对称？
  └─ 是 → Stepper
只有两种状态（开/关），有滑块？
  └─ 是 → Toggle / Switch
```

### 各类型特征

#### Selector（选择器）

**Figma 特征：**
- 多个并列节点，结构相同，样式不同（主题色 vs 灰色）
- 通常水平排列，节点等宽

**分析步骤：**
1. 检测是否有多个并列节点 → 是
2. 节点结构是否相同 → 是
3. 节点样式是否有差异 → 是（颜色/边框/字体不同）
4. → 识别为 Selector

**变种：**
- 单选 vs 多选：由业务逻辑控制，视觉识别方式一致
- 图标 + 文字 vs 纯文字：检测节点是否含 IMAGE / VECTOR 子节点
- 水平 vs 垂直：通过节点 y 坐标关系判断

---

#### Stepper（步进器）

**Figma 特征：**
- 三段式水平布局：[减少] [值显示] [增加]
- 左右两侧按钮结构对称（图标或文字）
- 中间是数字或文字显示区域

**分析步骤：**
1. 是否有三个子节点 → 是
2. 是否水平排列 → 是
3. 左右两侧是否对称（尺寸/结构相似）→ 是
4. 中间是否包含文本 → 是
5. → 识别为 Stepper

**变种：**
- 按钮样式：纯色背景 / 图片背景 / 无背景
- 图标类型：+/-、</>、▲▼、iconfont 自定义
- 中间内容：纯数字 / 数字+单位 / 图标+数字

**关键原则**：不要假设固定尺寸，从 `design.json[node].frame.absolute` 取实际值。

---

#### Tag Group（标签组）

**Figma 特征：**
- 多个不等宽小按钮
- 可能换行排列（Flow Layout）
- 通常可多选

**分析步骤：**
1. 是否有多个按钮 → 是
2. 按钮宽度是否不等 → 是
3. 是否可能换行 → 是
4. → 识别为 Tag Group，使用 `UICollectionView + LeftAlignedFlowLayout`

---

#### Toggle（开关）

**Figma 特征：**
- 只有两种状态：开/关
- 通常有圆形滑块或方形开关
- 有明显的"开"和"关"视觉区别

**实现方式：**
- 简单场景：`UISwitch`
- 自定义场景：自定义 `UIControl` + 动画

---

## 通用分析原则

| ❌ 错误（具体值）| ✅ 正确（模式）|
|----------------|--------------|
| 按钮宽度 68px | 宽度 = 容器宽度 / 按钮数量 - 间距 |
| 背景色 `#FFF606` alpha 0.1 | 已选中背景 = 主题色 + 低透明度 |
| 字体 `mk_f13_m()` | 已选中字体 = 字号 + Medium 字重 |

**不硬编码具体实现**——从 Figma 实际数据提取，保持布局比例和相对关系。

---

## 相关

- **状态视觉特征提取 + 代码生成**：[figma-ios-component-state-recognition](../figma-ios-component-state-recognition/SKILL.md)
- **点击交互逻辑**：[figma-ios-selection-interaction](../figma-ios-selection-interaction/SKILL.md)
- **Tag Group 列表实现**：[figma-ios-listview-recognition](../figma-ios-listview-recognition/SKILL.md)
- **总入口**：[figma-ios-playbook](../figma-ios-playbook/SKILL.md)
