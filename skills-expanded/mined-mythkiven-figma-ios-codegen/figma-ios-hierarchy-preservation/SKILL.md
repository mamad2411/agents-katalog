---
name: figma-ios-hierarchy-preservation
description: >-
  Maps Figma node hierarchy (FRAME/GROUP/INSTANCE) to UIKit UIView containers,
  preserving parent-child relationships, addSubview order, and coordinate system.
  Decides which nodes become UIView containers vs leaf views, and how to read
  relative/absolute coordinates from the data package. Use when generating UIKit
  code from a Figma data package, or when the user mentions 层级保持、拍平、
  addSubview 顺序、坐标系转换、relative frame、frame.relative。
---

# Figma 层级结构保持规则

## 职责边界（与 figma-ios-snapkit-layout 的分工）

- **本 Skill 负责**：Figma 节点 → UIView 层级映射（**建哪些容器、addSubview 顺序、坐标系转换**）
- **不负责**：约束写法语法（SnapKit `make.*` 写法）→ 见 [figma-ios-snapkit-layout](../figma-ios-snapkit-layout/SKILL.md)

> 两者协作：本 Skill 确定"建什么容器、父子关系"，snapkit-layout 确定"如何写约束值"。

---

## ⚡ QUICK_REF（Agent 优先读此处）

**核心规则：每个 Figma `<frame>` / `<group>` 必须对应一个 UIView，不得拍平。**

| Figma 节点类型 | iOS 对应 | 说明 |
|--------------|---------|------|
| `<frame>` | `UIView` 容器 | 保持层级，设置 `clipsToBounds` 按 clipsContent |
| `<group>` | `UIView` 容器 | 通常透明，仅作分组 |
| `<rectangle>` | `UIView` 或 `UIImageView` | 看填充类型 |
| `<text>` | `UILabel` | 直接 |
| `<instance>` (iconfont) | `UILabel` | 见 figma-ios-iconfont-mapping |

**坐标转换核心规则：**
- 数据包 `design.json[node].frame.relative.{x,y}` 是**相对直接父容器**的坐标，**直接用作 SnapKit `offset`**
- 如需绝对坐标，读 `frame.absolute.{x,y}`（已由数据包预计算）
- **禁止**跨层累加坐标（会双重计算）

```
Figma: <frame id="A" x="16" y="100">
           <frame id="B" x="0" y="0">
               <rect id="C" x="45" y="10" />

Swift:
A.snp: leading=16, top=100  ← 用 A 自己的 x/y
B.snp: leading=0, top=0     ← 用 B 自己的 x/y（相对A）
C.snp: leading=45, top=10   ← 用 C 自己的 x/y（相对B）
```

> 详细规则、坐标转换公式、addSubview 顺序规范见下文。

---

## 目标

确保生成的 Swift/UIKit 代码**完整保留 Figma 的层级结构**，避免将嵌套的容器"拍平"成扁平结构。

---

## 核心原则

### ✅ 原则 1：每个 Frame/Group 都对应一个 UIView 容器

Figma 中的每个 `<frame>` 或 `<group>` 节点，在代码中都应该有对应的 `UIView` 容器。

**Figma**:
```xml
<frame id="1:305" name="编组">
  <frame id="1:309" name="编组 6">
    <rectangle id="1:310" name="图片A" />
    <rectangle id="1:325" name="图片B" />
  </frame>
</frame>
```

**Swift**:
```swift
// ✅ 正确：保持层级
private lazy var groupContainer: UIView = { ... }()
private lazy var group6Container: UIView = { ... }()
private lazy var imageA: UIImageView = { ... }()
private lazy var imageB: UIImageView = { ... }()

// setupUI
groupContainer.addSubview(group6Container)
group6Container.addSubview(imageA)
group6Container.addSubview(imageB)
```

```swift
// ❌ 错误：拍平层级
private lazy var groupContainer: UIView = { ... }()
private lazy var imageA: UIImageView = { ... }()
private lazy var imageB: UIImageView = { ... }()

// setupUI
groupContainer.addSubview(imageA)  // 缺少中间容器
groupContainer.addSubview(imageB)
```

---

### ✅ 原则 2：坐标转换要考虑层级关系

**关键：`design.json[node].frame.relative.{x,y}` 是相对于【直接父容器】的坐标。需要绝对坐标时读 `frame.absolute`。**

#### 核心规则（必须遵守）

**规则 1：永远使用【节点的 frame.relative.x/y】作为约束 offset**

```swift
// design.json:
// 1:329 frame: Frame 1, frame.relative={x:16, y:392}
//   1:330 frame: Group 4, frame.relative={x:0, y:0}
//     1:331 rectangle: Rectangle, frame.relative={x:45, y:0}

// ✅ 正确：使用每个节点自己的 x/y
frame1View.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(16)  // Frame 1 的 x=16
    make.top.equalToSuperview().offset(392)     // Frame 1 的 y=392
}

group4View.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(0)   // Group 4 的 x=0（相对 Frame 1）
    make.top.equalToSuperview().offset(0)       // Group 4 的 y=0
}

rectangleView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(45)  // Rectangle 的 x=45（相对 Group 4）
    make.top.equalToSuperview().offset(0)       // Rectangle 的 y=0
}
```

**规则 2：如果跳过中间容器，必须累加偏移量**

```swift
// 如果代码中跳过了 Group 4（因为它无样式、偏移为 0），
// Rectangle 仍然要用自己的 x=45（相对 Group 4），
// 因为 Group 4 相对 Frame 1 的偏移是 0，所以累加后还是 45。

// ✅ 跳过 Group 4 后（Group 4 偏移为 0）
rectangleView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(45)  // 45 + 0 = 45（相对 Frame 1）
}

// ⚠️ 但如果 Group 4 的 x=10（不是 0），跳过后会出错：
rectangleView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(45)  // ❌ 应该是 45+10=55
}
```

**规则 3：⚠️ 危险场景：中间容器有非零偏移**

**如果中间容器相对父容器有偏移（x≠0 或 y≠0），且代码跳过了这个容器，必须累加偏移：**

```python
def calculate_offset_skipping_groups(node, target_ancestor):
    """
    计算节点相对于目标祖先容器的累积偏移
    （用于跳过中间 Group 时的坐标修正）
    """
    total_offset_x = 0
    total_offset_y = 0
    
    current = node
    while current != target_ancestor:
        # 从数据包读：design.json[node_id].frame.relative.{x,y}
        total_offset_x += current.frame.relative.x
        total_offset_y += current.frame.relative.y
        current = current.parent
    
    return total_offset_x, total_offset_y

# 示例
# Figma 层级：Cell → Frame 1 (x=16) → Group 4 (x=0) → Rectangle (x=45)
# 代码层级：Cell.contentView → rectangleView（跳过 Frame 1 和 Group 4）
# 
# 累积偏移 = 16 (Frame 1) + 0 (Group 4) + 45 (Rectangle) = 61
# 
# rectangleView.leading = 61（不是 45！）
```

---

#### 实战案例：本设计稿的坐标陷阱

**`design.json` 节选（仅展示关键字段）：**

```jsonc
{
  "1:329": { "name": "Frame 1", "frame": { "relative": { "x": 16, "y": 392 } } },  // 相对 CollectionView Cell
  "1:330": { "name": "Group 4", "frame": { "relative": { "x": 0,  "y": 0   } } }, // 相对 Frame 1
  "1:331": { "name": "RoundedRectangle", "frame": { "relative": { "x": 45, "y": 0 } } }, // 相对 Group 4
  "1:345": { "name": "备注", "frame": { "relative": { "x": 0, "y": 4 } } }                  // 相对 Group 4
}
```

**代码设计：**

```swift
// Cell.contentView 对应 Figma Cell（垂直滚动容器）
// remarkView 对应 Frame 1 (1:329)
// Group 4 (1:330) 被跳过（因为偏移为 0，无样式）

// ✅ 方案 A：保留 Frame 1，跳过 Group 4
RemarkInputCell.contentView
  └─ remarkView (Frame 1)           ← leading = 16（Figma Frame 1 的 x）
      ├─ titleLabel                 ← leading = 0（Figma 备注的 x，相对 Group 4）
      └─ remarkBackgroundView       ← leading = 45（Figma Rectangle 的 x，相对 Group 4）

// ❌ 方案 B：跳过 Frame 1 和 Group 4（错误）
RemarkInputCell.contentView
  ├─ titleLabel                     ← leading = 0  ← 错！应该是 16+0=16
  └─ remarkBackgroundView           ← leading = 45 ← 错！应该是 16+0+45=61
```

**为什么之前恰好对：**
- Frame 1 的 x=16，但代码中 `remarkView.edges.equalToSuperview()` **丢失了这 16pt**
- 后续所有子元素的坐标都错了（都少了 16pt）
- **巧合的是**：Figma 设计中所有内容都有左边距，所以视觉上"看起来对"，实际上整体左移了 16pt

---

#### 修正方案

**已修正：**

```swift
// RemarkInputCell
remarkView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(16)  // ← 新增：Frame 1 的 x 偏移
    make.trailing.top.bottom.equalToSuperview()
}
```

**现在所有子元素的坐标基准正确：**

```swift
// remarkView 内部（对应 Group 4，偏移为 0，可跳过）
titleLabel.leading = 0     // 相对 remarkView，实际相对 Cell = 16+0 = 16  ✅
remarkBg.leading = 45      // 相对 remarkView，实际相对 Cell = 16+45 = 61 ✅
```

---

#### 示例：坐标转换

**`design.json` 节选**：

```jsonc
{
  "1:305": { "name": "编组",   "frame": { "relative": { "x": 16, "y": 12 } } },
  "1:309": { "name": "编组 6", "frame": { "relative": { "x": 10, "y": 5  } } }, // 注意：x=10（非零）
  "1:310": { "name": "文字",   "frame": { "relative": { "x": 58, "y": 21 } } }, // 相对编组 6
  "1:325": { "name": "图片",   "frame": { "relative": { "x": 50, "y": 0  } } }  // 相对编组 6
}
```

**代码方案对比：**

```swift
// ✅ 方案 A：保留完整层级（推荐）
编组Container.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(16)  // 编组的 x
}

编组6Container.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(10)  // 编组 6 的 x（相对编组）
    make.top.equalToSuperview().offset(5)
}

textView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(58)  // 文字的 x（相对编组 6）
    make.top.equalToSuperview().offset(21)
}

// 实际相对最外层：16 + 10 + 58 = 84  ✅
```

```swift
// ⚠️ 方案 B：跳过编组 6（需累加偏移）
编组Container.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(16)
}

// 跳过编组 6，子元素直接添加到编组Container
textView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(68)  // ← 必须累加：10(编组6) + 58(文字) = 68
    make.top.equalToSuperview().offset(26)      // ← 必须累加：5(编组6) + 21(文字) = 26
}

// 实际相对最外层：16 + 68 = 84  ✅
```

```swift
// ❌ 方案 C：跳过编组 6，但忘记累加偏移（错误）
textView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(58)  // ❌ 少了编组 6 的 10pt 偏移
    make.top.equalToSuperview().offset(21)      // ❌ 少了编组 6 的 5pt 偏移
}

// 实际相对最外层：16 + 58 = 74  ❌ 错了 10pt！
```

---

#### 数据包已预计算偏移（无需脚本）

`figma-ios-preload-data` 在阶段 1 已经把每个节点的相对/绝对坐标都算好放入 `design.json[node].frame`：

```json
{
  "id": "1:331",
  "name": "Rectangle",
  "frame": {
    "absolute": {"x": 61, "y": 587, "w": 100, "h": 50},
    "relative": {"x": 45, "y": 0}
  }
}
```

> ⚠️ `frame.relative` **只有 `x` / `y`**（不含 `w` / `h`）。宽高永远从 `frame.absolute.w` / `frame.absolute.h` 取，避免误用。

- **保留所有容器层级**：直接使用 `frame.relative`
- **跳过透明/无样式包装层**（`_role.is_transparent_wrapper` 为 true）：
  - 把被跳过节点的 `frame.relative` 累加到子节点上，**或**直接拿子节点的 `frame.absolute` 减去保留容器的 `frame.absolute`
  - 数据包已用 `_role.is_transparent_wrapper` 标记可拍平的包装层

---

#### 手动计算公式（无脚本时）

**步骤：**

1. **列出从根容器到目标节点的完整路径：**
   ```
   Cell → Frame 1 (x=16) → Group 4 (x=0) → Rectangle (x=45)
   ```

2. **判断每个中间容器是否可跳过：**
   ```
   Group 4: x=0, y=0, 无样式 → 可跳过 ✅
   Frame 1: x=16, 有子元素 → 不可跳过 ❌
   ```

3. **累加不可跳过容器的偏移：**
   ```
   如果代码保留 Frame 1，跳过 Group 4：
   Rectangle 相对 Frame 1 的偏移 = 0 (Group 4) + 45 (Rectangle) = 45
   
   如果代码跳过 Frame 1 和 Group 4：
   Rectangle 相对 Cell 的偏移 = 16 (Frame 1) + 0 (Group 4) + 45 (Rectangle) = 61
   ```

4. **生成代码：**
   ```swift
   // 保留 Frame 1，跳过 Group 4
   frame1View.snp.makeConstraints { make in
       make.leading.equalToSuperview().offset(16)  // Frame 1 的 x
   }
   
   rectangleView.snp.makeConstraints { make in
       make.leading.equalToSuperview().offset(45)  // 相对 frame1View
   }
   ```

---

### ✅ 原则 3：优先使用相对布局而非绝对坐标

当子元素之间有明显的相对关系时，优先使用相对约束，而不是绝对偏移。

**示例：按钮内的图片+文字**

```swift
// ❌ 不推荐：使用绝对坐标
imageView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(50)
    make.top.equalToSuperview()
}

textView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(58)  // 硬编码
    make.centerY.equalToSuperview().offset(10)
}
```

```swift
// ✅ 推荐：使用相对布局
imageView.snp.makeConstraints { make in
    make.leading.equalToSuperview()  // 或根据设计意图
    make.top.equalToSuperview()
    make.size.equalTo(50)
}

textView.snp.makeConstraints { make in
    make.leading.equalTo(imageView.snp.trailing).offset(8)  // 相对于图片
    make.centerY.equalTo(imageView.snp.centerY).offset(5)
    make.width.equalTo(85)
    make.height.equalTo(19)
}
```

**优势**：
- ✅ 更易维护（改图片大小，文字自动跟随）
- ✅ 更符合设计意图（"文字在图片右边"）
- ✅ 更适应不同屏幕尺寸

---

## 标准工作流程

### Step 0: 直接读数据包预算的偏移

每个节点的 `frame.relative` 与 `frame.absolute` 已由 `figma-ios-preload-data` 阶段 1 计算并写入 `design.json`，**禁止再调脚本**。

如要确认"跨容器累积偏移"，二选一：
- 拍平到祖先容器：用子节点 `frame.absolute - 祖先 frame.absolute` 即得
- 保留所有容器：直接读子节点的 `frame.relative`

`_role.is_transparent_wrapper=true` 的容器可以拍平。

---

### Step 1: 分析 Figma 层级树

从 `design.json` 提取完整的层级树（每个节点的 `children` 字段已展开）：

```xml
<frame id="A" name="根容器">
  <frame id="B" name="子容器1">
    <element id="C" />
  </frame>
  <frame id="D" name="子容器2">
    <element id="E" />
    <element id="F" />
  </frame>
</frame>
```

**检查清单**：
- ✅ 识别所有 `<frame>` 和 `<group>` 节点
- ✅ 标记哪些是容器（有子元素）
- ✅ 标记哪些是叶子节点（UIImageView, UILabel 等）

---

### Step 2: 为每个容器创建 UIView

**规则**：
- `<frame name="编组 6">` → `group6Container: UIView`
- `<frame name="按钮">` → `buttonContainer: UIView`
- `<frame name="Object">` → `objectContainer: UIView`

**命名规范**：
- 使用 Figma 节点名的驼峰命名 + `Container` 后缀
- 如果 Figma 名称是中文，翻译为英文或使用拼音
- 例如：`编组 6` → `group6Container`，`按钮` → `buttonContainer`

---

### Step 3: 建立父子关系

**Figma 层级**：
```
A (根)
├─ B (子容器1)
│  └─ C (元素)
└─ D (子容器2)
   ├─ E (元素)
   └─ F (元素)
```

**Swift 代码**：
```swift
private func setupUI() {
    // 建立父子关系
    rootContainer.addSubview(subContainer1)
    rootContainer.addSubview(subContainer2)
    
    subContainer1.addSubview(elementC)
    
    subContainer2.addSubview(elementE)
    subContainer2.addSubview(elementF)
}
```

**检查清单**：
- ✅ 每个容器都添加到其直接父容器中
- ✅ 每个叶子元素都添加到其直接父容器中
- ✅ 没有跳级（子元素不能直接添加到祖父容器）

---

### Step 4: 直接读 frame.relative

数据包已经把每个节点的相对/绝对坐标都算好了：

```python
node = design["nodes"]["1:331"]
rel = node["frame"]["relative"]   # {"x": 45, "y": 0}     ← 只含 x/y
abs_ = node["frame"]["absolute"]  # {"x": 61, "y": 587, "w": 100, "h": 50}  ← 宽高在这里
```

如果跳过祖先容器（拍平到祖父）：
```python
flat_x = node["frame"]["absolute"]["x"] - keep_ancestor["frame"]["absolute"]["x"]
```

---

### Step 5: 生成 SnapKit 约束

使用转换后的相对坐标生成约束：

```swift
// 容器约束（相对于其父容器）
group6Container.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(81)
    make.top.equalToSuperview().offset(0)
    make.width.equalTo(143)
    make.height.equalTo(50)
}

// 子元素约束（相对于 group6Container）
imageView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(50)  // 相对坐标
    make.top.equalToSuperview().offset(0)
    make.size.equalTo(50)
}

textView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(58)  // 相对坐标
    make.top.equalToSuperview().offset(21)
    make.width.equalTo(85)
    make.height.equalTo(19)
}
```

---

## 常见错误和解决方案

### ❌ 错误 1：跳过中间容器

**问题**：
```swift
// Figma: 编组 → 编组 6 → 图片
// 错误代码：跳过了"编组 6"
buttonContainer.addSubview(imageView)  // ❌ 缺少 group6Container
```

**解决**：
```swift
// ✅ 保持完整层级
buttonContainer.addSubview(group6Container)
group6Container.addSubview(imageView)
```

---

### ❌ 错误 2：坐标系统混乱

**问题**：
```swift
// 图片在 Figma 中的绝对 x=131
// 但相对于 group6Container 应该是 x=50
imageView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(131)  // ❌ 用了绝对坐标
}
```

**解决**：
```swift
// ✅ 使用相对坐标
imageView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(50)  // 131 - 81 = 50
}
```

---

### ❌ 错误 3：忽略容器尺寸

**问题**：
```swift
// 容器没有设置尺寸，导致子元素布局错误
group6Container.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(81)
    make.top.equalToSuperview()
    // ❌ 缺少 width 和 height
}
```

**解决**：
```swift
// ✅ 明确设置容器尺寸
group6Container.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(81)
    make.top.equalToSuperview()
    make.width.equalTo(143)   // 从 Figma 获取
    make.height.equalTo(50)   // 从 Figma 获取
}
```

---

### ❌ 错误 4：属性声明顺序导致初始化失败

**问题**：
```swift
// group6Container 在初始化时访问了 imageView
private lazy var group6Container: UIView = {
    let v = UIView()
    v.addSubview(imageView)  // ❌ 可能导致循环依赖
    return v
}()

private lazy var imageView: UIImageView = { ... }()
```

**解决**：
```swift
// ✅ 在 setupUI() 中建立父子关系
private lazy var group6Container: UIView = {
    let v = UIView()
    return v
}()

private lazy var imageView: UIImageView = { ... }()

private func setupUI() {
    group6Container.addSubview(imageView)
}
```

---

## 自动化检查清单

生成代码后，必须进行以下检查：

### 层级结构检查

- [ ] 每个 Figma `<frame>` / `<group>` 都有对应的 `UIView` 容器
- [ ] 所有容器的父子关系与 Figma 一致
- [ ] 没有元素被"拍平"到错误的父容器中

### 坐标检查（⚠️ 关键）

- [ ] **所有元素的约束都是相对于【直接父容器】**
- [ ] **坐标转换公式：直接读 `design.json[node_id].frame.relative.{x,y}`（数据包已规范化为相对父容器）**
- [ ] **如果跳过中间容器，必须累加所有祖先容器的偏移**
- [ ] 优先使用相对布局（`equalTo(xxx.snp.trailing)`）而非绝对偏移

**⚠️ 最容易出错的场景：**

```swift
// Figma 层级：Cell → Frame A (x=16) → Group B (x=0) → Element C (x=45)
// 代码层级：Cell.contentView → frameAView → elementC（跳过 Group B）

// ❌ 错误：frameAView 忽略了自己的 x=16 偏移
frameAView.snp.makeConstraints { make in
    make.edges.equalToSuperview()  // ← 错！丢失了 x=16
}

// ✅ 正确：frameAView 必须设置 leading offset
frameAView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(16)  // Frame A 的 x
    make.trailing.top.bottom.equalToSuperview()
}

// elementC 相对 frameAView
elementC.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(45)  // Group B(x=0) + Element C(x=45) = 45
}
```

**检查方法**：对比代码 `make.leading.equalToSuperview().offset(N)` 与 `design.json[node].frame.relative.x` 是否一致。若代码跳过了中间容器，N 应等于 `frame.absolute.x - 保留祖先.frame.absolute.x`。

### 尺寸检查

- [ ] 所有容器都设置了明确的 `width` 和 `height`（或通过子元素撑开）
- [ ] 叶子元素的尺寸与 Figma 一致

### 命名检查

- [ ] 容器命名清晰（`group6Container`, `buttonContainer`）
- [ ] 避免与 UIKit 系统属性冲突（如 `maskView`）

---

## 工具和辅助脚本

### 数据包字段速查

- 坐标：`design.json[node].frame.relative` / `.absolute`
- 层级：`design.json[node].children`、`design.json[node].parent_id`、`index.json` 扁平索引
- 包装层标记：`design.json[node]._role.is_transparent_wrapper`、`is_single_child_wrapper`、`is_layout_container`

---

## 何时可以"拍平"层级？

### ✅ 可以省略容器的情况

只有当以下**所有条件**同时满足时，才可以省略中间容器：

1. **容器只有一个子元素**
2. **容器没有自己的样式**（无背景、无边框、无圆角）
3. **容器的尺寸完全由子元素决定**
4. **不影响响应式布局**

**示例**：
```xml
<!-- Figma -->
<frame id="1:100" name="Wrapper">
  <text id="1:101" name="标题" />
</frame>
```

如果 Wrapper 只是单纯的包裹层，可以省略：

```swift
// ✅ 可以省略 wrapperContainer
private lazy var titleLabel: UILabel = { ... }()

// 直接添加到更上层
parentContainer.addSubview(titleLabel)
```

### ❌ 不能省略容器的情况

- **容器有多个子元素**
- **容器有自己的样式**（背景色、圆角、阴影等）
- **容器参与布局计算**（如横向滚动、垂直居中等）
- **设计师明确标记为"编组"**（说明有语义意义）

---

## 与其他 Skill 的关系

- **依赖**：`figma-ios-playbook` → 主流程
- **依赖**：`figma-ios-snapkit-layout` → 约束语法
- **依赖**：`figma-ios-to-code-conventions` → 命名规范
- **被使用于**：所有 Figma 转 iOS 代码的场景

---

## 总结

**核心要点**：

1. ✅ **每个 Frame/Group 都对应一个 UIView 容器**
2. ✅ **坐标要从"绝对"转换为"相对于直接父容器"**
3. ✅ **保持完整的层级树，不要拍平**
4. ✅ **优先使用相对布局而非绝对坐标**
5. ✅ **直接使用数据包预算的 frame.relative / frame.absolute，禁止再调脚本或 MCP**
6. ✅ **跳过透明包装层时，用 `frame.absolute` 差值算累积偏移**

**检查方法**：

```
design.json[node].frame.relative   ← 直接读
            ↓
生成 Swift 代码
            ↓
对比代码 offset 与 frame.relative.x/y
```

**典型错误场景：**

```
design.json: Cell(0,0) → Frame 1(16,392) → Group 4(0,0) → Element(45,0)
代码: Cell.contentView → frame1View → element  （跳过了 Group 4）

❌ 错误：frame1View.edges = superview（丢失 x=16）
✅ 正确：frame1View.leading = superview + 16
✅ 元素相对 frame1View：offset(45)（取 element.frame.absolute.x - frame1View.frame.absolute.x = 45）
```

遵循这个 skill，可以确保生成的代码**完整保留 Figma 的设计意图**，避免布局错误和维护困难。

---

## 附录：常见坐标陷阱

### 陷阱 1：顶层容器的偏移被忽略

```jsonc
// design.json
{
  "A": { "frame": { "relative": { "x": 16, "y": 0 } } }, // 左边距 16pt，容易被忽略
  "B": { "frame": { "relative": { "x": 10, "y": 0 } } }  // A 的子节点
}
```

```swift
// ❌ 错误
frameAView.edges = superview  // 丢失 x=16

// ✅ 正确
frameAView.leading = superview + 16
```

**检测**：`design.json[A].frame.relative.x == 16`，但代码 offset 写成了 0。

---

### 陷阱 2：中间 Group 有非零偏移但被跳过

```xml
<frame id="A" x="0" y="0">
  <frame id="B" name="Group 5" x="10" y="5">   ← Group 有偏移！
    <element id="C" x="20" y="0" />
  </frame>
</frame>
```

```swift
// ❌ 错误：跳过 Group B，但忘记累加偏移
frameAView.addSubview(elementC)
elementC.leading = superview + 20  // ← 少了 Group B 的 10pt

// ✅ 正确：累加偏移
elementC.leading = superview + 30  // 10(Group B) + 20(Element C)

// ✅ 更推荐：不跳过 Group B
frameAView.addSubview(groupBView)
groupBView.leading = superview + 10
groupBView.addSubview(elementC)
elementC.leading = superview + 20
```

**检测**：跳过 B 后，C 的 offset 应等于 `C.frame.absolute.x - A.frame.absolute.x`（数据包字段直接给出）。

---

### 陷阱 3：嵌套 3 层以上的复杂结构

```xml
<frame A x="16">
  <frame B x="10">
    <frame C x="5">
      <element D x="20" />
    </frame>
  </frame>
</frame>
```

**累积偏移：16 + 10 + 5 + 20 = 51**

```swift
// 如果代码跳过 B 和 C（假设它们无样式、零偏移）
// 但实际上 B(x=10) 和 C(x=5) 都有偏移！
elementD.leading = superview + 20  // ❌ 错！应该是 51

// 数据包直接给出 D.frame.absolute.x = 51
```

---

### 陷阱 4：垂直滚动容器的 Cell 坐标

**Figma 中 CollectionView 的 Cell 通常有顶部偏移：**

```xml
<frame name="垂直滚动" y="195">       ← 容器在页面 y=195 处
  <frame name="Cell1" y="392">        ← Cell 相对容器的 y（不是 0！）
    <element x="16" y="0" />
  </frame>
</frame>
```

**代码中：**

```swift
// ❌ 错误：Cell 的 y=392 被忽略（以为 Cell 总是从 0 开始）
// ✅ 正确：y=392 是 Figma 中的 Cell 位置，代码中的 Cell 从 0 开始是对的
//         但 Cell 内部元素要考虑相对 Cell 的偏移

// Cell 内部元素
elementView.snp.makeConstraints { make in
    make.leading.equalToSuperview().offset(16)  // Element 的 x（相对 Cell）
    make.top.equalToSuperview().offset(0)       // Element 的 y（相对 Cell）
}
```

**关键：CollectionView Cell 在代码中从 (0, 0) 开始，但 Figma 中可能有偏移（这是正常的）**
