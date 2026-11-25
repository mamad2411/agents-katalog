---
name: figma-ios-vertical-layout-safearea
description: >-
  Handles vertical layout rules and safe-area insets when generating UIKit code
  from Figma designs. Covers: iPhone X vs iPhone 8 form factor detection, Status
  Bar height, Home Indicator skip rule, sticky-top/sticky-bottom views, and why
  vertical values must never be scaled by screenWidth ratio. Use when generating
  vertical constraints, handling safe area or safeAreaLayoutGuide, or when the
  user mentions 吸顶、吸底、Safe Area、Status Bar 高度、Home Indicator、
  safeAreaLayoutGuide、垂直 scale 禁止。
---

# Figma 垂直布局与安全区识别规范

**版本**: v2.1
**最后更新**: 2026-04-20

---

## ⛔ 红线规则（最高优先级）

### 1. 禁止用宽度比例 scale 缩放垂直方向

```swift
// ❌ 严重错误：把宽度比例用在 y / height
let scale = /* host.utils.screen_width */ / 375.0
view.snp.makeConstraints { make in
    make.top.equalTo(...).offset(49 * scale)        // ❌
    make.height.equalTo(111 * scale)                 // ❌
    make.bottom.equalToSuperview().offset(-34 * scale) // ❌
}
```

垂直方向**只允许**以下三种写法：

| 场景 | 写法 |
|---|---|
| 相对相邻元素的固定 gap | `make.top.equalTo(prev.snp.bottom).offset(figma_gap)` |
| 相对 safeArea | `make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom).offset(-figma_gap)` |
| 元素本身的 height/width | `make.height.equalTo(figma_h)`（直接用 Figma 实测值，**不乘 scale**）|

> **理由**：scale = 屏宽 / 375 仅反映横向像素缩放。如果把它用在 y / height，iPhone SE（375）和 iPhone 16 Pro Max（430）会产生 ~14% 的纵向偏差，严重时按钮会被吃掉、内容跑出 safeArea。设计稿的 y / height **是固定 pt**，不应随屏宽缩放。

### 2. 禁止把 safeArea.top 当导航栏底

如果设计稿没有原生导航栏（直接是吸顶卡片），用 `view.safeAreaLayoutGuide.snp.top` 即可；如果有导航栏，用 `host.json` → `utils.status_bar_nav_height` 的表达式，**不要混用**。

### 3. 禁止凭空给容器加 padding/margin

任何 offset 都要能从 Figma `frame.absolute` / `frame.relative` 推出来，禁止"看着别扭加 12pt"。如果数据不对，**先回 design.json 找根因**，不要在代码里加补丁。

### 4. Scroll 容器的顶/底必须锚定邻居，禁止硬编码 y/height ⭐️

如果页面上存在 `_role.is_sticky_top` / `is_sticky_bottom` 节点（见 `audit.json.sticky_keyword_hits`，关键字：`吸顶 / 吸底 / sticky_top / sticky_bottom`），它们之间的 scroll 承载区必须把顶/底约束到这些 sticky 节点上：

```swift
// ❌ 错误：scroll 容器用绝对 y/height（已在 341:313 '垂直滚动' 事故中出现）
formScrollView.snp.makeConstraints { make in
    make.top.equalToSuperview().offset(195)
    make.height.equalTo(407)   // iPhone 8 上直接盖掉底部吸底按钮
}

// ✅ 正确：顶对 sticky_top.bottom，底对 sticky_bottom.top
formScrollView.snp.makeConstraints { make in
    make.leading.trailing.equalToSuperview()
    make.top.equalTo(stepStripContainer.snp.bottom).offset(figma_gap_top)
    make.bottom.equalTo(bottomBarContainer.snp.top).offset(-figma_gap_bottom)
}
```

**判定依据**：audit.json 里 `sticky_keyword_hits[].sibling_rule` 会明确列出本规则。

---

## ⚡ 核心原则

**统一使用 `host.json` → `utils.status_bar_nav_height` 表达式（原样粘贴），无需判断机型。**

---

## ⭐️ 数据包优先：屏幕机型与吸底节点已预标

`figma-ios-preload-data` 阶段 1 已经把以下信息算好：

| 信息 | 字段 |
|---|---|
| 设计稿机型（iPhone X / iPhone 8）| 根节点 `_layout_hint.screen_kind`；`manifest.json.summary.screen_size` |
| 吸顶节点（贴 status bar / nav bar）| `design.json[node]._role.is_sticky_top` |
| 吸底节点（贴 home indicator）| `design.json[node]._role.is_sticky_bottom` |
| 吸顶/吸底节点列表 | `index.json.by_role.sticky_top` / `sticky_bottom` |

**不需要再让 LLM 用导航栏 Y 坐标 / 页面总高度自己推算机型**。`is_sticky_bottom=true` 的节点就是要贴 `safeArea.bottom` 的吸底按钮。

代码里仍然统一用 `/* host.utils.status_bar_nav_height */`，机型只作辅助判断（如 iPhone 8 没有 home indicator 就不用预留 34pt 安全区）。

---

## 一、导航栏布局（标准写法）

```swift
// ✅ 推荐：统一写法，自动适配所有机型
navigationView.snp.makeConstraints { make in
    make.top.leading.trailing.equalToSuperview()
    make.height.equalTo(/* host.utils.status_bar_nav_height */)
    // iPhone X: 返回 88 (44状态栏 + 44导航)
    // iPhone 8: 返回 64 (20状态栏 + 44导航)
}

// 内容区：从导航栏下方开始
contentView.snp.makeConstraints { make in
    make.top.equalTo(navigationView.snp.bottom).offset(figma_gap)
    // figma_gap = Figma 中第一个内容元素的 y - 导航栏的 bottom
}
```

**为什么无需判断机型？**

`host.utils.status_bar_nav_height` 表达式应由宿主实现按设备返回正确高度：

```objc
// host.utils 提供的导航总高表达式（示例）
+ (CGFloat)mk_systemNavStatusBarHeight {
    CGFloat statusBarHeight = [UIApplication sharedApplication].statusBarFrame.size.height;
    CGFloat navBarHeight = 44;
    return statusBarHeight + navBarHeight;
    // iPhone X: 44 + 44 = 88
    // iPhone 8: 20 + 44 = 64
}
```

---

## 二、吸底按钮布局

### 规则：检查按钮底部是否对齐 Home Indicator

**判断逻辑**：

```python
button_bottom = button.y + button.height
home_indicator_top = 778  # iPhone X 标准位置（或从 Figma 读取）

if abs(button_bottom - home_indicator_top) < 2:
    # 设计师把 Home Indicator 空间画进了按钮容器
    use_safe_area = True
else:
    # 设计师没有预留 Home Indicator 空间
    use_safe_area = False
```

### 代码模板

#### 情况 A：Figma 含 Home Indicator 占位

```swift
// Figma: 按钮容器高度 111 = 实际内容 77 + Home Indicator 34
submitButton.snp.makeConstraints { make in
    make.leading.trailing.equalToSuperview()
    make.height.equalTo(111)  // Figma 容器高度（含 Home Indicator 占位）
    
    if #available(iOS 11.0, *) {
        make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom)
    } else {
        make.bottom.equalToSuperview()
    }
}

// 按钮内容：距容器底部 34pt（为 Home Indicator 预留）
buttonLabel.snp.makeConstraints { make in
    make.centerX.equalToSuperview()
    make.bottom.equalToSuperview().offset(-34)
}
```

**运行效果**：
- **iPhone X**: 按钮内容在 Home Indicator 上方 ✅
- **iPhone 8**: 按钮底部贴屏幕底部（无 Home Indicator）✅

---

#### 情况 B：Figma 不含 Home Indicator 占位

```swift
// Figma: 按钮高度 48（只有按钮本身）
submitButton.snp.makeConstraints { make in
    make.leading.trailing.equalToSuperview()
    make.height.equalTo(48)
    
    if #available(iOS 11.0, *) {
        make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom).offset(-16)
        // iPhone X: 自动在 Home Indicator 上方留 16pt 间距
        // iPhone 8: 在屏幕底部留 16pt 间距
    } else {
        make.bottom.equalToSuperview().offset(-16)
    }
}
```

### 常见事故：Home Indicator 占位被"算两遍"⚠️

Figma 按钮容器高度 = 77（内容） + 34（Home Indicator）= 111 时，已经内建占位，**不要再 +34**：

```swift
// ❌ 把 Home Indicator 加了两次（事故：iPhone 8 上底部内容被裁）
bottomBarContainer.snp.makeConstraints { make in
    make.height.equalTo(111)                                 // Figma 已含 34
    make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom).offset(34)  // ❌ 再 +34
}

// ✅ 正确
bottomBarContainer.snp.makeConstraints { make in
    make.height.equalTo(111)
    if #available(iOS 11.0, *) {
        make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom)
    } else {
        make.bottom.equalToSuperview()
    }
}
```

---

## 二·半、吸顶/吸底关键字识别（数据包已预判）

设计师用下列名字标注时，figma-ios-preload-data 会把节点标成 `_role.is_sticky_top` / `is_sticky_bottom`，并在 `audit.json.sticky_keyword_hits` 里写出配套规则：

| 关键字（中文） | 关键字（英文，大小写不敏感） | side | 来源 |
|---|---|---|---|
| `吸顶` | `sticky top` / `sticky_top` / `stickytop` | top | hint_tagger 名字 fallback |
| `吸底` | `sticky bottom` / `sticky_bottom` / `stickybottom` | bottom | 同上 |

两路判定（**合并**，任一命中即标）：

1. **几何判定**：节点 y ≈ 安全区顶 / 底 + 近全宽（w/parent ≥ 0.92）
2. **名字判定**：名字含上述关键字子串（子串匹配，大小写不敏感）

**代码生成规则**（`audit.json.sticky_keyword_hits[].must_apply` 里也会写）：

```swift
// 吸顶节点
stickyTopNode.snp.makeConstraints { make in
    make.leading.trailing.equalToSuperview()
    if #available(iOS 11.0, *) {
        make.top.equalTo(view.safeAreaLayoutGuide.snp.top)
    } else {
        make.top.equalToSuperview()
    }
    make.height.equalTo(figma_height)
}

// 吸底节点（Figma 含 Home Indicator 占位时）
stickyBottomNode.snp.makeConstraints { make in
    make.leading.trailing.equalToSuperview()
    make.height.equalTo(figma_height)
    if #available(iOS 11.0, *) {
        make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom)
    } else {
        make.bottom.equalToSuperview()
    }
}
```

**连带规则（红线 4）**：同父兄弟里位于 sticky 节点之上/之下的「主内容区」通常就是 scroll 承载区，顶/底必须相对 sticky 节点锚定，见本文件顶部红线 4。

---

## 三、垂直间距规则

**原则：间距用 Figma 实测值，相对相邻元素，不直接相对 `safeArea`**

```swift
// ✅ 正确：相对实际相邻元素
contentCollectionView.snp.makeConstraints { make in
    make.top.equalTo(stepIndicatorBar.snp.bottom).offset(31)   // 步骤条下方 31pt
    make.bottom.equalTo(submitButton.snp.top).offset(-65)      // 按钮上方 65pt
}

// ❌ 错误：直接相对 safeArea
contentCollectionView.snp.makeConstraints { make in
    make.top.equalTo(view.safeAreaLayoutGuide.snp.top).offset(某个数)
    make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom).offset(-某个数)
    // ← 在不同设备上间距会不一致
}
```

**计算 Figma 间距**：

```python
# 顶部间距
gap_top = content_element.y - previous_element.bottom

# 底部间距
gap_bottom = next_element.y - content_element.bottom

# 例如：
# - 导航栏 bottom: 88
# - stepIndicatorBar top: 119
# → gap = 119 - 88 = 31
```

---

## 四、完整布局示例

```swift
private func setupConstraints() {
    // 1️⃣ 导航栏
    navigationView.snp.makeConstraints { make in
        make.top.leading.trailing.equalToSuperview()
        make.height.equalTo(/* host.utils.status_bar_nav_height */)
    }
    
    // 2️⃣ 步骤指示器（Figma: 导航栏下方 31pt）
    stepIndicatorBar.snp.makeConstraints { make in
        make.leading.trailing.equalToSuperview()
        make.top.equalTo(navigationView.snp.bottom).offset(31)
        make.height.equalTo(75)
    }
    
    // 3️⃣ 滚动容器（顶部间距 31pt，底部间距 65pt）
    contentCollectionView.snp.makeConstraints { make in
        make.leading.trailing.equalToSuperview()
        make.top.equalTo(stepIndicatorBar.snp.bottom).offset(31)
        make.bottom.equalTo(submitButton.snp.top).offset(-65)
    }
    
    // 4️⃣ 吸底按钮（Figma 含 Home Indicator 占位）
    submitButton.snp.makeConstraints { make in
        make.leading.trailing.equalToSuperview()
        make.height.equalTo(111)
        
        if #available(iOS 11.0, *) {
            make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom)
        } else {
            make.bottom.equalToSuperview()
        }
    }
}
```

---

## 五、常见错误与修正

### ❌ 错误 1：写死导航栏高度

```swift
// ❌ 错误：在 iPhone 8 上会多 24pt
navigationView.snp.makeConstraints { make in
    make.height.equalTo(88)
}

// ✅ 正确：自动适配
navigationView.snp.makeConstraints { make in
    make.height.equalTo(/* host.utils.status_bar_nav_height */)
}
```

---

### ❌ 错误 2：滚动容器直接相对 `safeArea`

```swift
// ❌ 错误：在不同设备上间距不一致
contentCollectionView.snp.makeConstraints { make in
    make.top.equalTo(view.safeAreaLayoutGuide.snp.top).offset(200)
}

// ✅ 正确：相对实际元素
contentCollectionView.snp.makeConstraints { make in
    make.top.equalTo(stepIndicatorBar.snp.bottom).offset(31)
}
```

---

### ❌ 错误 3：按钮底部用 `superView` 而非 `safeArea`

```swift
// ❌ 错误：Figma 含 Home Indicator 占位时会被遮挡
submitButton.snp.makeConstraints { make in
    make.bottom.equalToSuperview()
}

// ✅ 正确：用 safeArea（内容自动在 Home Indicator 上方）
submitButton.snp.makeConstraints { make in
    if #available(iOS 11.0, *) {
        make.bottom.equalTo(view.safeAreaLayoutGuide.snp.bottom)
    } else {
        make.bottom.equalToSuperview()
    }
}
```

---

## 六、机型识别（可选）

**通常不需要判断机型**，但如果确实需要（例如生成文档说明）：

```python
# 简化识别：只看导航栏 Y 坐标
nav_bar = find_navigation_bar(metadata)

if nav_bar.y == 44:
    device_type = 'iphone_x_plus'  # 状态栏 44pt
    note = 'iPhone X+ 设计稿（含刘海/灵动岛）'
elif nav_bar.y == 20:
    device_type = 'iphone_8'       # 状态栏 20pt
    note = 'iPhone 8 设计稿（无刘海）'
else:
    device_type = 'unknown'
    note = '无法判断机型'
```

**仅用于注释，不影响代码生成。**

---

## 七、与其他 Skill 的协作

### `figma-ios-playbook`

调用顺序：
```
figma-ios-playbook
    ↓
调用 figma-ios-vertical-layout-safearea（垂直布局规则）
    ↓
调用 figma-ios-snapkit-layout（生成 SnapKit 约束）
```

### `figma-ios-horizontal-layout`

- **本 Skill（vertical）**：处理垂直方向（导航栏、吸底按钮、安全区）
- **`figma-ios-horizontal-layout`（horizontal）**：处理横向方向（左右边距、横向适配）

---

## 变更历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-04-13 | v2.0 | 大幅精简：删除复杂的机型识别逻辑，统一使用 `/* host.utils.status_bar_nav_height */` |
| 2026-03-31 | v1.0 | 初始版本（1594 行） |
