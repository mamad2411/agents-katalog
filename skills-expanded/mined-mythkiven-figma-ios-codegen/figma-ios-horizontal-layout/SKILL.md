---
name: figma-ios-horizontal-layout
description: >-
  从 Figma 固定宽度设计稿（375pt）生成横向自适应的 iOS 布局代码。
  根据容器左右间隙判断布局策略：对称布局/接近全宽布局使用动态宽度，其他使用固定宽度。
  子元素根据容器特征选择比例缩放或列表布局。
  Use when generating ANY horizontal layout from Figma.
---

# Figma 横向布局适配策略

## 核心原则

**默认：从左往右按设计稿绝对位置布局（SnapKit）**

**特殊：容器左右间隙满足条件时，使用动态宽度 + 子元素比例缩放**

> 注：垂直方向的布局（导航栏高度、安全区、吸底按钮）由 [figma-ios-vertical-layout-safearea](../figma-ios-vertical-layout-safearea/SKILL.md) 负责。

---

## ⭐️ 数据包优先：先查 `_layout_hint.horizontal_pattern`

`figma-ios-preload-data` 阶段 1 已经把"左右间隙差 ≤ 2 / 接近全宽 / 自由布局"算好写入：

```jsonc
"_layout_hint": {
  "horizontal_pattern": "symmetric" | "near_full_width" | "free",
  "left_inset": 16.0,
  "right_inset": 16.0,
  "child_count": 4
}
```

**判断流程**：
1. 容器节点存在 `_layout_hint.horizontal_pattern` → 直接采用其结果
   - `symmetric` → 对称布局策略（动态宽度 + 比例缩放）
   - `near_full_width` → 接近全宽（动态宽度 + 子元素策略选择）
   - `free` → 端固定布局（默认）
2. 没有 `_layout_hint` → fallback 到下面的"步骤 1：判断容器宽度策略"自己算

---

## 步骤 1：判断容器宽度策略（仅当 `_layout_hint` 缺失时）

从 Figma 读取容器数据，计算左右间隙：

```python
# Figma 数据
screen_width = 375  # 设计稿屏幕宽度
container_x = 16    # 容器相对屏幕 x
container_width = 343

# 计算左右间隙
left_margin = container_x  # 16
right_margin = screen_width - container_x - container_width  # 375 - 16 - 343 = 16
```

### 判断规则

```python
# 场景 1：对称布局（左右间隙相等，偏差 ≤2pt）
if abs(left_margin - right_margin) <= 2:
    → 容器使用动态宽度
    → 子元素按比例缩放

# 场景 2：接近全宽布局（左右边距都较小）
elif right_margin <= 20 and left_margin <= 80:
    → 容器使用动态宽度
    → 子元素根据类型选择策略（见步骤 2）

# 场景 3：固定宽度布局（默认）
else:
    → 容器使用固定宽度
    → 子元素使用固定位置
```

---

## 步骤 2：判断子元素布局策略

**前提**：容器已确定为动态宽度（场景 1 或 2）

### 子元素策略

```python
# 检查 1：是否是滚动容器？
if container.is_scrollable or 'scroll' in container.name.lower():
    → 使用 UICollectionView/UIScrollView
    → 子元素固定尺寸、固定间距
    → 走 [figma-ios-listview-recognition](../figma-ios-listview-recognition/SKILL.md) 逻辑

# 检查 2：多个横向排列的子元素（非滚动）
elif len(horizontal_children) >= 1:
    → 子元素按比例缩放（位置、宽度、高度都缩放）
    → child_x = figma_x × scale
    → child_width = figma_width × scale
    → child_height = figma_height × scale

# 默认：固定布局（不应该出现）
else:
    → 子元素使用固定位置和尺寸
```

---

## 代码生成规则

### 场景 1：对称布局（动态宽度 + 比例缩放）

**示例**：步骤条（左 16pt，右 16pt）

```swift
// 计算缩放比例
let screenWidth = /* host.utils.screen_width */
let scale = (screenWidth - 32) / 343.0  // (屏幕宽 - 左右边距) / Figma 容器宽

// 容器：动态宽度
stepIndicatorContainer.snp.makeConstraints { make in
    make.leading.trailing.equalToSuperview().inset(16)
    make.height.equalTo(68)
}

// 子元素：位置和宽度都按比例缩放
// Figma 数据: step1(x=18, width=56), sep1(x=91, width=24), step2(x=131, width=71)

step1View.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(18 * scale)  // 位置缩放
    make.width.equalTo(56 * scale)  // ✅ 宽度也缩放
    make.centerY.equalToSuperview()
}

stepSeparator1.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(91 * scale)
    make.width.height.equalTo(24 * scale)  // ✅ 尺寸缩放
    make.centerY.equalToSuperview()
}

step2View.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(131 * scale)
    make.width.equalTo(71 * scale)  // ✅ 宽度缩放
    make.centerY.equalToSuperview()
}
```

---

### 场景 2A：接近全宽 + 滚动列表

**示例**：品类滚动条（左 62pt，右 0pt）

```swift
// 容器：动态宽度
categoryScrollView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(62)
    make.trailing.equalToSuperview()
    make.height.equalTo(72)
}

// 子元素：UICollectionView（固定尺寸 + 固定间距）
let layout = UICollectionViewFlowLayout()
layout.scrollDirection = .horizontal
layout.itemSize = CGSize(width: 80, height: 40)  // Figma 子元素尺寸
layout.minimumInteritemSpacing = 12  // Figma 子元素间距

let collectionView = UICollectionView(frame: .zero, collectionViewLayout: layout)
```

---

### 场景 2B：接近全宽 + 比例缩放

**示例**：多个横向按钮（左 20pt，右 8pt）

```swift
// 计算缩放比例
let screenWidth = /* host.utils.screen_width */
let scale = (screenWidth - 20 - 8) / 347.0  // Figma 容器宽度

// 容器：动态宽度
buttonContainer.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(20)
    make.trailing.equalToSuperview().offset(-8)
}

// 子元素：位置和宽度都按比例缩放
button1.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(12 * scale)
    make.width.equalTo(68 * scale)  // ✅ 宽度缩放
}

button2.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(88 * scale)
    make.width.equalTo(68 * scale)  // ✅ 宽度缩放
}
```

---

### 场景 3：固定宽度布局

**示例**：左对齐卡片（左 16pt，宽 280pt，右 79pt）

```swift
// 容器：固定宽度
cardView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(16)
    make.width.equalTo(280)  // Figma 宽度
    make.height.equalTo(120)
}

// 子元素：固定位置（不缩放）
titleLabel.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(12)  // Figma x，固定值
    make.top.equalToSuperview().offset(8)
}
```

---

## 判断流程图

```
读取 Figma 容器数据（x, width）
↓
计算左右间隙
left_margin = container_x
right_margin = screen_width - container_x - container_width
↓
判断容器宽度策略：
├─ |left - right| ≤ 2？
│  └─ 是 → 场景 1：对称布局
│         容器：动态宽度
│         子元素：比例缩放
├─ right ≤ 20 且 left ≤ 80？
│  └─ 是 → 场景 2：接近全宽
│         容器：动态宽度
│         子元素：根据类型选择
│         ├─ 滚动容器 → UICollectionView
│         ├─ 多个横向元素 → 比例缩放
│         └─ 其他 → 固定布局
└─ 否 → 场景 3：固定宽度
       容器：固定宽度
       子元素：固定位置
```

---

## 缩放比例计算公式

### 场景 1：对称布局
```swift
scale = (屏幕宽度 - left_margin × 2) / Figma 容器宽度

// 应用到子元素：
子元素位置 = Figma x × scale
子元素宽度 = Figma width × scale
子元素高度 = Figma height × scale
```

### 场景 2：接近全宽
```swift
scale = (屏幕宽度 - left_margin - right_margin) / Figma 容器宽度

// 应用到子元素：同场景 1
```

### 示例计算（场景 1：步骤条）

| 设备 | 屏幕宽度 | 容器宽度 | scale | step1 位置 | separator1 位置 |
|------|---------|---------|-------|-----------|----------------|
| SE   | 320pt   | 288pt   | 0.84  | 15pt      | 76pt           |
| 14   | 375pt   | 343pt   | 1.00  | 18pt      | 91pt           |
| Pro Max | 430pt | 398pt  | 1.16  | 21pt      | 106pt          |

**效果**：所有设备保持相同的视觉比例 ✅

---
