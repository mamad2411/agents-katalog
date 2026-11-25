---
name: figma-ios-snapkit-layout
description: >-
  When turning Figma designs into iOS UIKit/Swift, prefers relative Auto Layout
  over absolute frames and uses SnapKit for constraints. Use when generating or
  refactoring Figma-based views, layout code, constraints, or when the user
  mentions SnapKit, relative layout, or avoiding fixed frames from Figma.
---

# Figma → iOS：相对布局与 SnapKit

## 职责边界（与 figma-ios-hierarchy-preservation 的分工）

- **本 Skill 负责**：**约束写法**（SnapKit 语法、相对 vs 绝对选择、offset 值如何从 Figma 数值得出、Safe Area 处理）。
- **不负责**：层级映射（哪些 Figma 节点对应哪些 UIView、addSubview 顺序）→ 见 [figma-ios-hierarchy-preservation](../figma-ios-hierarchy-preservation/SKILL.md)。
- **不负责**：颜色/字体 token → 见 [figma-ios-design-token-mapping](../figma-ios-design-token-mapping/SKILL.md)。
- **不负责**：iOS 最低版本 API 限制 → 见 [figma-ios-minimum-deployment-12](../figma-ios-minimum-deployment-12/SKILL.md)。
- **不负责**：节点跳过规则 → 见 [figma-ios-to-code-conventions](../figma-ios-to-code-conventions/SKILL.md)。

## 核心原则

1. **尽量避免「纯绝对布局」**：不要用 Figma 的 `absoluteBoundingBox` 直接换算成 `view.frame = CGRect(...)` / 在 `layoutSubviews` 里手写整套 frame 作为**唯一**布局手段（除非用户明确要求或极少数动态几何场景）。
2. **优先相对关系**：视图相对 **父视图**（边距、对齐）、相对 **兄弟视图**（间距、基线、等高），保证旋转、Dynamic Type、不同屏宽时仍可维护。
3. **约束用 SnapKit 表达**：新建/维护 UIKit 布局时，默认使用 **SnapKit**（`import SnapKit`），与项目内已有用法保持一致。
4. **必须使用 Figma 节点的精确尺寸**（重要）：当 Figma 节点有明确的 width/height 时，代码中**必须**使用该精确值，而不是估算值或填满父容器。

## Figma 数值怎么落到「相对」

| 稿里的含义 | 相对布局做法 |
|------------|----------------|
| 相对画板/Frame 的 x、y、宽、高 | 转为对 `superview` 的 **leading/trailing/top/bottom** 或 **width/height**，必要时加 **offset**（对应稿中边距）。 |
| 两控件间距 | `make.leading.equalTo(other.snp.trailing).offset(8)` 一类，而不是两个绝对 frame 相减。 |
| 水平/垂直居中 | `centerX` / `centerY` / `center` 相对父或相对某兄弟。 |
| 贴安全区 | 对 `safeAreaLayoutGuide.snp.*` 或 `view.safeAreaLayoutGuide` 约束（SnapKit 项目常用 `snp.safeArea` 等，按宿主工程惯例）。 |
| 固定小图标尺寸 | 可用 **固定宽高约束**（仍是约束，不是运行时算 frame）；资源本身尺寸与稿一致即可。 |
| **Figma 节点有明确 width/height** | **必须**使用精确值：`make.width.equalTo(298)` / `make.height.equalTo(100)`，**禁止**使用 `equalToSuperview()` 除非节点确实占满父容器。 |
| **子节点在稿里有明确 x（相对父 Frame）** | 用 **`make.leading.equalToSuperview().offset(node.frame.relative.x)`**（或相对兄弟锚点），**禁止**用 `make.centerX.equalToSuperview().multipliedBy(0.xx)` 等魔法比例「估位置」。数据直接读 `design.json[node].frame.relative.x`，跳过包装层时改用 `frame.absolute.x − 保留祖先.frame.absolute.x`。 |

### ❌ 常见错误：不使用精确尺寸

**问题：**
```swift
// ❌ 错误：备注框占满整个宽度
remarkBackgroundView.snp.makeConstraints { make in
    make.leading.trailing.equalToSuperview()  // 宽度 = 父容器宽度（错误）
    make.height.greaterThanOrEqualTo(100)      // 高度估算（错误）
}
```

**Figma 实际尺寸：** width=298px, height=100px, left=45px

**修复：**
```swift
// ✅ 正确：使用 Figma 节点的精确尺寸
remarkBackgroundView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(45)  // ✅ Figma x 坐标
    make.width.equalTo(298)   // ✅ Figma width（精确值）
    make.height.equalTo(100)  // ✅ Figma height（精确值）
}
```

#### ❌ 常见错误：用 `centerX.multipliedBy` 代替稿面坐标

```swift
// ❌ 错误：魔法比例，与 Figma 子节点 x 无对应关系
iconView.snp.makeConstraints { make in
    make.centerX.equalToSuperview().multipliedBy(0.707)
}
```

**修复**：直接读 `design.json[child].frame.relative.x`（数据包已计算）→ **`make.leading.equalToSuperview().offset(…)`**。跨容器累加用 `frame.absolute.x − 保留祖先.frame.absolute.x`。

---

#### ❌ 常见错误：用 `trailing.equalToSuperview()` 代替从左往右布局

**问题场景：** 一组水平排列的元素（文字 + 图标），错误地让图标相对屏幕右侧布局。

```swift
// ❌ 错误：icon 相对屏幕右侧布局
// Figma: /局 (x=212) → icon (x=236)，间距 24pt
unitLabel.snp.makeConstraints { make in
    make.leading.equalTo(stepperView.snp.trailing).offset(8)
    make.centerY.equalToSuperview()
}

searchIconLabel.snp.makeConstraints { make in
    make.trailing.equalToSuperview().offset(-121)  // ❌ 相对右侧
    make.centerY.equalToSuperview()
}
```

**问题：**
- 宽屏设备（iPad、横屏）时，icon 和 `/局` 之间的间隙会异常变大
- 违反了 Figma 的设计意图（从左往右排列）

**修复：**
```swift
// ✅ 正确：icon 相对 /局 文字布局（从左往右）
unitLabel.snp.makeConstraints { make in
    make.leading.equalTo(stepperView.snp.trailing).offset(8)
    make.centerY.equalToSuperview()
}

searchIconLabel.snp.makeConstraints { make in
    make.leading.equalTo(unitLabel.snp.trailing).offset(4)  // ✅ 从左布局
    make.centerY.equalToSuperview()
}
```

**判断规则：**
```python
# 从 Figma metadata 判断布局方向
def should_use_leading(node, prev_node, container_width):
    """
    判断是否应该用 leading 布局（从左往右）
    """
    # 如果节点有明确的前一个兄弟节点（x 坐标接近）
    if prev_node and (node['x'] - prev_node['x'] - prev_node['width']) < 50:
        # 间距小于 50pt → 从左往右排列
        return True
    
    # 如果节点距离右侧很远（说明不是吸右布局）
    if (container_width - node['x'] - node['width']) > 50:
        return True
    
    return False

# 示例：
# /局: x=212, width=20 → right=232
# icon: x=236 → 距离 /局 右侧 4pt < 50pt
# → 应该用 make.leading.equalTo(unitLabel.snp.trailing).offset(4)
```

**强制规则：**
```
✅ 水平排列的元素，应该从左往右布局（leading → trailing）
✅ 只有明确的"吸右"元素（如导航栏右侧按钮），才用 trailing.equalToSuperview()
❌ 不要因为"计算方便"而用 trailing，要遵循 Figma 的设计意图
```

---

### ✅ 强制规则：尺寸精确度

生成代码时，必须：
```
✅ 从数据包 `design.json[node_id].frame.absolute.w/h` 读取节点的 width/height
✅ 在约束中使用精确值：make.width.equalTo(<figma_width>)
✅ 不要使用估算值：make.height.greaterThanOrEqualTo(500)
✅ 不要随意填满父容器：make.leading.trailing.equalToSuperview()
✅ 除非 Figma 节点确实占满父容器（x=0, width=父容器width）
```

---

## 底部安全区域（Safe Area）处理（重要）

### 问题背景

Figma 设计稿通常基于固定画板尺寸（如 375×812），但实际设备有：
- **刘海屏/灵动岛**（iPhone X 及以上）：顶部安全区域 ~44pt
- **Home Indicator**（iPhone X 及以上）：底部安全区域 ~34pt
- **传统屏幕**（iPhone 8 及以下）：无额外安全区域

### ✅ 强制规则：底部按钮必须贴 Safe Area Bottom

**场景**：吸底按钮、工具栏、TabBar 等底部固定元素

#### ❌ 错误写法（会被 Home Indicator 遮挡）

```swift
submitButton.snp.makeConstraints { make in
    make.leading.trailing.bottom.equalToSuperview()  // ❌ 直接贴底
    make.height.equalTo(111)
}
```

**问题**：在 iPhone X 及以上设备，按钮会被底部 Home Indicator 遮挡 ~34pt。

#### ✅ 正确写法（考虑安全区域）

```swift
submitButton.snp.makeConstraints { make in
    make.leading.trailing.equalToSuperview()
    make.height.equalTo(111)
    // 考虑底部安全区域（iPhone X 及以上）
    if #available(iOS 11.0, *) {
        make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom)
    } else {
        make.bottom.equalToSuperview()
    }
}
```

**效果**：
- iPhone X 及以上：按钮底部贴安全区域底部（自动避开 Home Indicator）
- iPhone 8 及以下：按钮底部贴屏幕底部（无额外间距）

### 顶部安全区域

**场景**：自定义导航栏、顶部横幅等

```swift
navigationView.snp.makeConstraints { make in
    make.leading.trailing.equalToSuperview()
    // 顶部贴安全区域（自动避开刘海/灵动岛）
    if #available(iOS 11.0, *) {
        make.top.equalTo(view.safeAreaLayoutGuide.snp.top)
    } else {
        make.top.equalToSuperview().offset(20)  // 状态栏高度
    }
    make.height.equalTo(44)
}
```

### Figma 设计稿中的安全区域识别

`figma-ios-preload-data` 已在数据包中预标记安全区域相关节点（详见 `figma-ios-vertical-layout-safearea`）。仅在数据包字段缺失需要回退时，可按下列规则人工识别：

1. **Home Indicator 节点**（通常命名为 `home indicator`、`Home Indicator`）
   - 位置：y = 页面高度 - 34（如 778 = 812 - 34）
   - 尺寸：width = 页面宽度, height = 34

2. **吸底按钮的实际位置**
   - 如果按钮 y + height = Home Indicator 的 y
   - 说明按钮应该在 Home Indicator 上方
   - 代码中需要用 `safeAreaLayoutGuide.snp.bottom`

### 自动化判断规则

生成代码时，如果满足以下条件，**必须**使用 Safe Area：

```
✅ 底部元素 && (元素底部 + Home Indicator 高度 ≈ 页面高度)
   → 使用 make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom)

✅ 顶部导航栏 && (元素顶部 = 0 或接近状态栏)
   → 使用 make.top.equalTo(view.safeAreaLayoutGuide.snp.top)

❌ 中间内容区域
   → 正常使用 equalToSuperview() 或相对布局
```

### iOS 12 兼容性说明

`safeAreaLayoutGuide` 是 iOS 11.0+ 引入的，本项目最低支持 iOS 12.0，因此：

- ✅ 可以直接使用 `safeAreaLayoutGuide`（iOS 12 可用）
- ✅ 建议加 `#available(iOS 11.0, *)` 检查（向下兼容性考虑）
- ❌ 不需要手动计算安全区域高度

### 常见错误

#### ❌ 错误 1：忽略安全区域

```swift
// ❌ 吸底按钮直接贴底
make.bottom.equalToSuperview()
```

**后果**：iPhone X 及以上设备，按钮被 Home Indicator 遮挡。

#### ❌ 错误 2：硬编码安全区域高度

```swift
// ❌ 不要硬编码 34pt
make.bottom.equalToSuperview().offset(-34)
```

**问题**：
- iPhone 8 及以下无安全区域，会有 34pt 空白
- 未来设备安全区域可能变化

#### ✅ 正确：使用系统 API

```swift
// ✅ 让系统自动处理
if #available(iOS 11.0, *) {
    make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom)
} else {
    make.bottom.equalToSuperview()
}
```

## SnapKit 习惯写法（UIKit）

- 子视图：`addSubview` 后 **`snp.makeConstraints`**；动态变更用 **`snp.updateConstraints`** 或 **`snp.remakeConstraints`**（避免重复 `makeConstraints` 堆叠）。
- 与父视图：`equalToSuperview()`，边距用 **`inset`** / **`offset`** / **`UIEdgeInsets`**。
- 与兄弟视图：锚定到 **`otherView.snp.leading`** 等，体现 **顺序与间距**。
- **Content hugging / compression**（`UILabel`、`UIImageView`）：按需设置 `Content Priority`，避免被错误拉伸；与「不用绝对 frame」不冲突。

## 反例（生成代码时避免作为默认）

```swift
// 避免：整屏用 Figma 坐标直接写 frame
subview.frame = CGRect(x: 24, y: 120, width: 327, height: 48)

// 更好：约束表达「距父左 24、距某参照顶 16、宽随父或固定」
subview.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(24)
    make.top.equalTo(titleLabel.snp.bottom).offset(16)
    make.trailing.equalToSuperview().offset(-24)
    make.height.equalTo(48)
}
```

## 与「绝对数值」的关系

- Figma 的 **px 仍可作 offset/常量**，但应体现在 **约束的 constant** 上，而不是每个子视图独立一套全局坐标。
- 若宿主工程 **未集成 SnapKit**，不在此 Skill 内改 Pod；用户需先加依赖，或临时用 `NSLayoutConstraint` / `anchor` API，但 **语义仍应是相对约束**，而非整屏 frame。

## 多屏幕适配策略

**详见**：[figma-ios-horizontal-layout](../figma-ios-horizontal-layout/SKILL.md)

**快速规则：**
- **对称布局**（如步骤条）→ 动态间距（layoutSubviews 计算）
- **左对齐流式**（如表单）→ 固定间距（相对约束）
- **其他** → 固定布局 + TODO 标记提醒开发者

## 相关

- **总入口**（流程与索引）：[figma-ios-playbook](../figma-ios-playbook/SKILL.md)
- **节点跳过、稿内装饰**：[figma-ios-to-code-conventions](../figma-ios-to-code-conventions/SKILL.md)
- **商用一次交付验收**：[figma-ios-commercial-delivery](../figma-ios-commercial-delivery/SKILL.md)
