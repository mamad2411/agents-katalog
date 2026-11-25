---
name: figma-ios-vector-vs-code
description: >-
  规定哪些 Figma 矢量图形应该下载为图片 Assets，哪些应该用 iOS 代码绘制。
  避免不必要的图片下载，减少包体积。
  Use when generating code from Figma designs with vector graphics, shapes, or masks.
---

# Figma 矢量图形处理策略

## ⛔ 红线规则（最高优先级，覆盖所有下文）

**含「语义子节点」的容器节点，即使被 figma-ios-preload-data 标记为 `is_export_asset=true`，也禁止整组用切图替代，必须按子节点逐一生成代码。**

### 判定：什么是「语义子节点」

只要节点的子树（含跨层）中**任意一个**节点满足以下任一条件，该节点就含语义子节点：

| 条件 | 说明 | 例 |
|---|---|---|
| `type == "TEXT"` | 含可读文本 | "STEP.1"、"找人试音"、"绝地求生" |
| `type == "INSTANCE"` | 含组件实例（按钮/标签/图标 …） | 品类卡片、段位标签、性别 pill |
| `_role.is_iconfont == true` | 含 iconfont | next/query/check 图标 |
| `_role.is_iconfont_library` | 含 iconfont 集合容器 | iconfont_24 |
| `_role.is_list_container` | 含横向 / 纵向列表容器 | `可滚动`、Tag 集合 |

> 设计师在 Figma 上勾导出（export）经常是出于"备份给开发"目的，**不代表这个组应该当成一张静态图**。把"步骤条整组""5 个品类整组"做成切图，**会直接导致**：① 文字写死、改不了；② 状态切换不可能（选中/未选中）；③ 国际化失败；④ 视觉看似 OK 实则功能完全缺失。这是历史上多次出现的高发陷阱，必须强制规避。

### 决策伪代码（先于"代码绘制 vs 下载图片"决策）

```python
def can_use_export_asset(node):
    if not (node.get("export") or {}).get("is_export_asset"):
        return False
    # 判定是否含语义子节点
    for child in walk_subtree(node):
        if child["type"] in ("TEXT", "INSTANCE"):
            return False
        role = child.get("_role") or {}
        if role.get("is_iconfont") or role.get("is_iconfont_library"):
            return False
        if role.get("is_list_container"):
            return False
    return True   # 子树纯几何/矢量，整组切图安全
```

### 允许整组切图的典型场景（白名单）

- 纯位图节点（`fills[].type == "IMAGE"`）
- `BOOLEAN_OPERATION` 美术字 / Logo（无 TEXT 子节点）
- 纯矢量装饰（背景插画、底纹）
- 单个 imageset 的图标（无子节点）

### 红线违反后的处置

如果你已经写出 `UIImageView(image: UIImage(named: "img_xxx"))` 来代替一个含 TEXT/INSTANCE 的节点，**回退该实现**，改为：

1. 把这个 GROUP/FRAME 当作 `UIView` 容器；
2. 它的子节点逐一生成对应的 `UILabel` / `UIButton` / `UIView` / iconfont `UILabel`；
3. 不需要切图（因为切图是为了避免重写美术字之类的 BOOLEAN_OPERATION，与文字/图标无关）。

> 例外：节点确实是「设计师做的截屏占位图」（如设计稿里贴了一张"竞品截图"用作后续修改参考），且团队明确要先按图占位的 → 在代码顶部加 `// TODO(阶段2): 拆解 <node_id> <name> 为子节点实现`，并在 README 列出，**不允许直接当阶段 2 交付**。

---

## 本 Skill 的职责

规定在 Figma → iOS 代码生成时：
- 哪些矢量图形**必须下载为图片 Assets**
- 哪些矢量图形**应该用代码绘制**（`UIView` + `CALayer` + `UIBezierPath`）
- 如何判断和决策

---

## 决策流程图

```
Figma 矢量节点
    ↓
┌──────────────────────────────────────┐
│ 1. 是否为简单几何形状？               │
│   - 矩形、圆角矩形、圆形、椭圆       │
│   - 纯色填充或简单渐变               │
│   - 无复杂路径或布尔运算             │
└──────────────────────────────────────┘
    ↓ 是                    ↓ 否
 用代码绘制            继续判断
                            ↓
┌──────────────────────────────────────┐
│ 2. 是否为复杂矢量图形？               │
│   - 贝塞尔曲线路径（≥3个）           │
│   - 布尔运算（UNION/SUBTRACT/EXCLUDE）│
│   - 美术字体、Logo、特殊图标         │
└──────────────────────────────────────┘
    ↓ 是                    ↓ 否
 下载为图片             用代码绘制
```

---

## 规则 1：用代码绘制（推荐优先）

### 适用场景

以下 Figma 节点类型**必须用代码绘制**，**禁止下载为图片**：

| Figma 类型 | 识别特征 | iOS 实现 | 示例 |
|-----------|---------|---------|------|
| **矩形** | `RECTANGLE`，无圆角或圆角简单 | `UIView` + `backgroundColor` | 纯色背景 |
| **圆角矩形** | `RECTANGLE`，`cornerRadius` ≤ 50 | `UIView` + `layer.cornerRadius` | 按钮背景 |
| **圆形** | `ELLIPSE`，宽高相等 | `UIView` + `layer.cornerRadius = width/2` | 头像容器 |
| **渐变背景** | `fills[0].type == "GRADIENT_LINEAR"` | `CAGradientLayer` | 渐变按钮 |
| **纯色图形** | 单一 `SOLID` 填充，简单形状 | `UIView` + `backgroundColor` | 分隔线 |
| **边框** | `strokes` 数组 | `layer.borderWidth` + `borderColor` | 输入框边框 |

### ⚠️ 强制规则：用数据包字段判断"代码绘制 vs 切图"

`figma-ios-preload-data` 已经在阶段 1 把每个节点的 `type` / `fills` / `strokes` / `corner_radius` / `vector_geometry` / `effects` / `export.is_export_asset` 全部规范化进 `design.json`，并：

- 设计师有 export → `node.export.is_export_asset = true` 且对应 imageset 已在 `assets/ios/` → **直接用切图**
- 设计师无 export → 按下面的判定标准决定 **代码绘制** 或 **生成 mock 图片**

```
1. design.json[node].export.is_export_asset == true
   → 用 assets/ios/manifest.json 中的 asset_name → UIImage(named:)
2. 否则按 should_draw_with_code(node) 判断（见下面"判断标准"）
   → true: 用代码绘制（UIView/CALayer/CAGradientLayer）
   → false: 加 TODO 注释 + mock 占位
```

> 阶段 2 不再调 MCP / Figma REST API；判断只看 `design.json[node]` 字段。

### 判断标准（代码绘制）

满足**以下所有条件**时，用代码绘制：

```
✅ 形状简单（矩形/圆/椭圆）
✅ 填充简单（纯色/线性渐变/径向渐变）
✅ 无复杂路径（子路径 ≤ 1 个）
✅ 无布尔运算（UNION/SUBTRACT/INTERSECT/EXCLUDE）
✅ 圆角简单（`cornerRadius` 统一或仅部分圆角）
✅ 尺寸固定或可缩放（不依赖精确像素）
✅ 无复杂效果（effects 数组为空或 visible=false）
```

---

### ⚠️ 特殊检查：VECTOR 节点的复杂圆角

**问题背景：**

Figma 的 VECTOR 节点可能包含**复杂的圆角路径**（如步进器的单边圆角），但 `corner_radius` 会显示为 0。

**触发条件**（数据包字段）：
- `node.type == "VECTOR"`（或含路径的布尔/星形等）
- `node.corner_radius` 缺失或为 0，且无明显 `corner_radii`
- 但 `node.vector_geometry.fill_paths` 或 `stroke_paths` 非空（阶段 1 从 REST `fillGeometry`/`strokeGeometry` 写入）

**判断**：读 SVG path 字符串：

```text
design.json[node].vector_geometry.fill_paths[].data
design.json[node].vector_geometry.stroke_paths[].data
```

（旧文档里的 `vector_paths` **已废弃**，数据包不再写该字段。）

**判断圆角类型：**

```xml
<!-- 示例：步进器左侧按钮背景（单边圆角）-->
<path d="M0 16C0 7.16344 7.16344 0 16 0H32V32H16C7.16344 32 0 24.8366 0 16Z" 
      fill="white" fill-opacity="0.1"/>
```

**分析 SVG path：**

| Path 特征 | 识别方法 | 圆角类型 |
|----------|---------|---------|
| `C` 或 `A` 命令 | 有圆弧（贝塞尔曲线或弧线）| 有圆角 |
| 圆弧在四周 | 4 个 `C`/`A` 命令分布均匀 | 全圆角 |
| 圆弧在部分边 | 1-2 个 `C`/`A` 命令 | 单边或双边圆角 |
| 无 `C`/`A` 命令 | 只有 `L`/`H`/`V` 命令 | 无圆角（矩形）|

**决策表：**

| SVG path 特征 | 圆角类型 | iOS 实现 | 代码绘制？ |
|-------------|---------|---------|-----------|
| 无 `C`/`A` 命令 | 无圆角 | `UIView` + `backgroundColor` | ✅ 是 |
| 4 个相同的圆弧 | 全圆角 | `layer.cornerRadius = X` | ✅ 是 |
| 单边或双边圆弧 | 部分圆角 | `layer.cornerRadius + layer.maskedCorners` | ✅ 是 |
| 复杂路径 | 不规则圆角 | 下载图片或 `UIBezierPath` | ❌ 否 |

**实现示例（单边圆角）：**

```swift
// 步进器减少按钮（左边圆角，右边直角）
// design.json: type=VECTOR, corner_radius=0
// vector_geometry.fill_paths[0].data: "M0 16C0 7.16344 7.16344 0 16 0H32V32H16C7.16344 32 0 24.8366 0 16Z"
// 识别：左边有圆弧，右边是直线 → 单边圆角

private lazy var decreaseBackgroundView: UIView = {
    let v = UIView()
    v.backgroundColor = UIColor(white: 1.0, alpha: 0.1)
    
    // 左边圆角，右边直角
    v.layer.cornerRadius = 16  // 高度 32 / 2 = 16
    v.layer.maskedCorners = [.layerMinXMinYCorner, .layerMinXMaxYCorner]  // 左上和左下
    
    return v
}()

// 步进器增加按钮（右边圆角，左边直角）
private lazy var increaseBackgroundView: UIView = {
    let v = UIView()
    v.backgroundColor = UIColor(white: 1.0, alpha: 0.1)
    
    // 右边圆角，左边直角
    v.layer.cornerRadius = 16
    v.layer.maskedCorners = [.layerMaxXMinYCorner, .layerMaxXMaxYCorner]  // 右上和右下
    
    return v
}()
```

**iOS 12.0+ 兼容性：**
- ✅ `layer.maskedCorners` 可用于 iOS 11.0+
- ✅ 项目最低部署 iOS 12.0，可以安全使用

**常见单边圆角场景：**

```swift
// 左边圆角
v.layer.maskedCorners = [.layerMinXMinYCorner, .layerMinXMaxYCorner]

// 右边圆角
v.layer.maskedCorners = [.layerMaxXMinYCorner, .layerMaxXMaxYCorner]

// 上边圆角
v.layer.maskedCorners = [.layerMinXMinYCorner, .layerMaxXMinYCorner]

// 下边圆角
v.layer.maskedCorners = [.layerMinXMaxYCorner, .layerMaxXMaxYCorner]

// 对角圆角（左上+右下）
v.layer.maskedCorners = [.layerMinXMinYCorner, .layerMaxXMaxYCorner]
```

**检查清单（VECTOR 节点）：**

```
□ 已读取 design.json[node].corner_radius
□ 如果 corner_radius = 0 且 type = VECTOR
  → 已读取 design.json[node].vector_geometry.fill_paths / stroke_paths
  → 已解析 SVG path（`.data`）
  → 已判断圆角类型
□ 如果是单边圆角 → 使用 layer.maskedCorners
□ 如果是复杂路径 → 下载图片或 UIBezierPath
```

---

### 判断标准（代码绘制）

满足**以下所有条件**时，用代码绘制：

```
✅ 形状简单（矩形/圆/椭圆）
✅ 填充简单（纯色/线性渐变/径向渐变）
✅ 无复杂路径（子路径 ≤ 1 个）
✅ 无布尔运算（UNION/SUBTRACT/INTERSECT/EXCLUDE）
✅ 圆角简单（`cornerRadius` 统一或仅部分圆角）
✅ 尺寸固定或可缩放（不依赖精确像素）
✅ 无复杂效果（effects 数组为空或 visible=false）
```

### 示例 1：Mask（黄色圆角矩形）

**Figma 数据**：
```json
{
  "id": "1:306",
  "name": "Mask",
  "type": "VECTOR",
  "fills": [{
    "type": "SOLID",
    "color": {"r": 1.0, "g": 0.9647, "b": 0.0235}  // #FFF606
  }],
  "cornerRadius": 25.0,
  "cornerSmoothing": 0.6,
  "absoluteBoundingBox": {"width": 343.0, "height": 48.0}
}
```

**判断**：
- ✅ 形状简单：矩形
- ✅ 填充简单：纯色 #FFF606
- ✅ 无复杂路径
- ✅ 无布尔运算
- ✅ 圆角简单：25px 统一圆角

**结论**：**用代码绘制** ✅

**iOS 代码**：
```swift
// ✅ 推荐：用代码绘制（0KB，易维护）
private lazy var maskView: UIView = {
    let v = UIView()
    v.backgroundColor = MKUIStyle.mk_cXX() /* color_map: #FFF606 */  // 黄色
    v.layer.cornerRadius = 25
    v.layer.cornerCurve = .continuous  // 平滑圆角（iOS 13+）
    return v
}()
```

**iOS 12 兼容**：
```swift
// iOS 12 不支持 .continuous，使用普通圆角
v.layer.cornerRadius = 25
// 如果需要更平滑的效果，可以略微增大圆角值
v.layer.cornerRadius = 27  // 视觉上接近 cornerSmoothing: 0.6
```

### 示例 2：渐变背景

**Figma 数据**：
```json
{
  "fills": [{
    "type": "GRADIENT_LINEAR",
    "gradientStops": [
      {"color": {"r": 0, "g": 0.576, "b": 0.933}, "position": 0},
      {"color": {"r": 0.118, "g": 0.396, "b": 0.859}, "position": 1}
    ]
  }]
}
```

**iOS 代码**：
```swift
// ✅ 推荐：用 CAGradientLayer（0KB）
private func setupGradient() {
    let gradientLayer = CAGradientLayer()
    gradientLayer.colors = [
        MKUIStyle.mk_cXX() /* color_map: #0093EE */.cgColor,  // 起始色
        MKUIStyle.mk_cXX() /* color_map: #1E65DC */.cgColor   // 结束色
    ]
    gradientLayer.startPoint = CGPoint(x: 0, y: 0.5)  // 左
    gradientLayer.endPoint = CGPoint(x: 1, y: 0.5)    // 右
    backgroundView.layer.insertSublayer(gradientLayer, at: 0)
}

override func layoutSubviews() {
    super.layoutSubviews()
    // 更新渐变层大小
    backgroundView.layer.sublayers?.first?.frame = backgroundView.bounds
}
```

---

## 规则 2：下载为图片（必须）

### 适用场景

以下 Figma 节点类型**必须下载为图片 Assets**：

| Figma 类型 | 识别特征 | 原因 | 示例 |
|-----------|---------|------|------|
| **复杂贝塞尔曲线** | 子路径 ≥ 3 个 | 代码实现成本高，易出错 | 美术字体、Logo |
| **布尔运算** | `BOOLEAN_OPERATION`（UNION/SUBTRACT/INTERSECT/EXCLUDE）| 需要精确像素级控制 | 特殊形状、镂空图形 |
| **图片填充** | `fills[0].type == "IMAGE"` | 本身就是图片 | 背景图片、照片 |
| **复杂渐变** | 多个渐变点（≥3 个）、径向渐变 + 复杂形状 | iOS 原生渐变限制 | 艺术效果 |
| **阴影/模糊复杂** | 多层阴影、特殊混合模式 | 代码难以完美复现 | 特效文字 |
| **设计师明确标注** | Figma 评论中要求"图片形式" | 尊重设计意图 | - |

### 判断标准（下载图片）

满足**以下任一条件**时，下载为图片：

```
❌ 布尔运算（BOOLEAN_OPERATION）
❌ 贝塞尔曲线路径 ≥ 3 个
❌ 图片填充（fills[0].type == "IMAGE"）
❌ 复杂渐变（≥ 3 个渐变点）
❌ 特殊效果（阴影叠加、混合模式）
❌ 美术字体、Logo、品牌图形
❌ 评论中明确要求
```

### 示例 3：形状结合（美术字体）

**Figma 数据**：
```json
{
  "id": "1:310",
  "name": "形状结合",
  "type": "BOOLEAN_OPERATION",
  "booleanOperation": "EXCLUDE",
  "children": [
    {"id": "1:311", "name": "路径", "type": "VECTOR"},
    {"id": "1:312", "name": "路径", "type": "VECTOR"},
    ... // 共 14 个子路径
  ],
  "fills": [{"type": "SOLID", "color": {...}}]
}
```

**判断**：
- ❌ 布尔运算：`EXCLUDE`（排除）
- ❌ 贝塞尔曲线路径：14 个
- ❌ 用途：美术字体"找人试音"

**结论**：**必须下载为图片** ✅

**下载步骤**（已由 figma-ios-preload-data 完成）：
1. 设计师点了 export → `node.export.is_export_asset=true` → 数据包阶段 1 已下载
2. 设计师没点 export 但代码绘制不可行 → 在 README 标注 TODO，请设计补 export 后重新跑数据包
3. 阶段 2 直接 `UIImage(named: assets/ios/manifest.items[node_id].asset_name)`

**iOS 代码**：
```swift
// ✅ 正确：使用图片 Assets
private lazy var textShapeImageView: UIImageView = {
    let v = UIImageView()
    v.contentMode = .scaleAspectFit
    v.image = UIImage(named: "img_99a99_button_text_shape")
    return v
}()
```

---

## 规则 3：边界情况决策

### 情况 1：圆角矩形（cornerRadius > 50）

**判断**：
- 如果 `cornerRadius` 接近宽度或高度的 50%（类似胶囊形状）
- 且无其他复杂效果

**决策**：**仍然用代码绘制** ✅

```swift
// 胶囊形状
v.layer.cornerRadius = v.bounds.height / 2
```

### 情况 2：仅一个边有圆角

**Figma 特征**：
```json
{
  "rectangleCornerRadii": [10, 10, 0, 0]  // 仅顶部圆角
}
```

**iOS 实现**：
```swift
// iOS 11+
let path = UIBezierPath(
    roundedRect: bounds,
    byRoundingCorners: [.topLeft, .topRight],
    cornerRadii: CGSize(width: 10, height: 10)
)
let mask = CAShapeLayer()
mask.path = path.cgPath
v.layer.mask = mask
```

**决策**：**用代码绘制** ✅（略微复杂，但仍可控）

### 情况 3：简单 Logo（≤2 个路径）

**判断**：
- 虽然是矢量图形，但路径数量少
- 用途明确为 Logo 或品牌标识

**决策**：**下载为图片** ✅（保证品牌一致性）

### 情况 4：Icon（iconfont 可用）

**判断**：
- 设计稿中使用 `iconfont/icon_xxx_24` 命名
- 项目 iconfont 库中有对应图标

**决策**：**用 iconfont** ✅（详见 [figma-ios-iconfont-mapping](../figma-ios-iconfont-mapping/SKILL.md)）

```swift
// 使用 iconfont（最优）
iconLabel.font = MKIconFont.iconFont(withSize: 24)      // iconfont_map.font
iconLabel.text = MKIconFont.shared().mk_icon_xxx        // iconfont_map.text
```

---

## 实施步骤

### 步骤 1：从数据包读节点

```python
node = design["nodes"][node_id]
node_type      = node["type"]                       # RECTANGLE / VECTOR / BOOLEAN_OPERATION / ...
fills          = node.get("fills", [])              # [{"type":"SOLID","color":"rgba(...)"}, ...]
strokes        = node.get("strokes", [])
corner_radius  = node.get("corner_radius", 0)
children_count = len(node.get("children", []))
boolean_op     = node.get("boolean_operation")      # UNION / SUBTRACT / INTERSECT / EXCLUDE
is_export      = (node.get("export") or {}).get("is_export_asset", False)
```

### 步骤 2：应用决策树

```python
def should_download_as_image(node):
    if (node.get("export") or {}).get("is_export_asset"):
        return True
    if any((f.get("type") == "IMAGE") for f in node.get("fills", [])):
        return True
    if node.get("type") == "BOOLEAN_OPERATION":
        return True
    if len(node.get("children", [])) >= 3:
        return True
    for f in node.get("fills", []):
        if f.get("type") in ("GRADIENT_LINEAR", "GRADIENT_RADIAL") \
                and len(f.get("gradient_stops", [])) >= 3:
            return True
    name = node.get("name", "").lower()
    if any(k in name for k in ["logo", "美术", "艺术", "形状结合", "shape"]):
        return True
    return False
```

> 该节点已被 `figma-ios-preload-data` 标记 `_role.is_export_asset` 时，imageset 已经在 `assets/ios/`，直接 `UIImage(named: ...)`。

### 步骤 3：生成对应代码

#### 场景 A：用代码绘制

```swift
// Figma 节点 1:306 - Mask（黄色圆角矩形）
// 决策: 简单矩形 + 纯色 + 统一圆角 → 用代码绘制 ✅
private lazy var maskView: UIView = {
    let v = UIView()
    v.backgroundColor = MKUIStyle.mk_cXX() /* color_map: #FFF606 */
    v.layer.cornerRadius = 25
    v.layer.cornerCurve = .continuous  // iOS 13+
    return v
}()
```

#### 场景 B：下载为图片

```swift
// Figma 节点 1:310 - 形状结合（美术字体）
// 决策: BOOLEAN_OPERATION + 14个路径 → 下载为图片 ✅
// Assets: img_99a99_button_text_shape
private lazy var textShapeImageView: UIImageView = {
    let v = UIImageView()
    v.contentMode = .scaleAspectFit
    v.image = UIImage(named: "img_99a99_button_text_shape")
    return v
}()
```

---

## 代码注释规范

### 必须包含的信息

```swift
// Figma 节点 <node_id> - <节点名称>
// 决策: <判断依据> → <实现方式> ✅
// [如果是图片] Assets: <asset_name>
// [如果是代码] 实现: <UIView/CALayer/CAGradientLayer>
```

### 示例

```swift
// ✅ 代码绘制示例
// Figma 节点 1:289 - 矩形（步骤指示器背景）
// 决策: 线性渐变 + 边框 + 圆角 → 用代码绘制（CAGradientLayer）✅
// 实现: CAGradientLayer + layer.borderWidth
private lazy var backgroundView: UIView = {
    let v = UIView()
    v.layer.cornerRadius = 16
    v.layer.borderWidth = 1
    v.layer.borderColor = UIColor.white.withAlphaComponent(0.15).cgColor
    return v
}()
```

```swift
// ✅ 图片下载示例
// Figma 节点 1:310 - 形状结合（"找人试音"美术字）
// 决策: BOOLEAN_OPERATION(EXCLUDE) + 14个路径 → 下载为图片 ✅
// Assets: img_99a99_button_text_shape (2KB)
// 尺寸: 85×19
private lazy var textShapeImageView: UIImageView = {
    let v = UIImageView()
    v.contentMode = .scaleAspectFit
    v.image = UIImage(named: "img_99a99_button_text_shape")
    return v
}()
```

---

## 优势对比

### 用代码绘制 ✅

**优势**：
- ✅ 包体积：0KB
- ✅ 可维护性：易于调整颜色、尺寸、圆角
- ✅ 适配性：支持动态颜色（深色模式）、动态尺寸
- ✅ 性能：矢量缩放，无失真

**劣势**：
- ⚠️ 开发成本：需要写代码
- ⚠️ 限制：复杂图形无法实现

### 下载为图片 ✅

**优势**：
- ✅ 准确性：100% 还原设计稿
- ✅ 复杂度：支持任意复杂图形
- ✅ 开发速度：直接使用 UIImage

**劣势**：
- ⚠️ 包体积：每个图片 1-10KB
- ⚠️ 维护成本：修改需要重新导出
- ⚠️ 适配性：深色模式需要两套图

---

## 常见错误

### ❌ 错误 1：简单图形也下载为图片

```swift
// ❌ 不推荐：纯色圆角矩形下载为图片（浪费 2KB）
maskImageView.image = UIImage(named: "img_xxx_mask")
```

```swift
// ✅ 推荐：用代码绘制（0KB）
v.backgroundColor = MKUIStyle.mk_cXX() /* color_map: #FFF606 */
v.layer.cornerRadius = 25
```

### ❌ 错误 2：复杂图形用代码硬写

```swift
// ❌ 不推荐：14 个贝塞尔路径用代码手写（易出错）
let path = UIBezierPath()
path.move(to: CGPoint(x: 155, y: 700))
path.addCurve(to: ..., controlPoint1: ..., controlPoint2: ...)
// ... 100+ 行代码
```

```swift
// ✅ 推荐：下载为图片（2KB，准确）
textImageView.image = UIImage(named: "img_xxx_text_shape")
```

### ❌ 错误 3：忘记 iOS 12 兼容

```swift
// ❌ iOS 12 崩溃
v.layer.cornerCurve = .continuous  // iOS 13+
```

```swift
// ✅ iOS 12 兼容
if #available(iOS 13.0, *) {
    v.layer.cornerCurve = .continuous
}
```

### ❌ 错误 4：属性名与系统冲突

```swift
// ❌ 编译错误：UIView 已有只读属性 maskView
private lazy var maskView: UIView = { ... }()
```

```swift
// ✅ 正确：使用描述性名称避免冲突
private lazy var yellowMaskBackgroundView: UIView = { ... }()
```

**禁止使用的属性名**（与 UIKit 冲突）：
- ❌ `backgroundView` - **UICollectionViewCell** 已有此属性（iOS 14+，改用 `cellBackgroundView`）
- ❌ `maskView` - UIView 已有此属性
- ❌ `layer` - UIView 已有此属性
- ❌ `frame` - UIView 已有此属性
- ❌ `bounds` - UIView 已有此属性
- ❌ `superview` - UIView 已有此属性
- ❌ `subviews` - UIView 已有此属性
- ❌ `backgroundColor` - UIView 已有此属性（除非 override）
- ❌ `isHidden` - UIView 已有此属性（除非 override）

**推荐命名方式**：
- ✅ `yellowMaskBackgroundView` - 描述性 + 具体用途
- ✅ `buttonMaskView` - 前缀 + 描述
- ✅ `customMaskLayer` - custom 前缀
- ✅ `maskBackgroundView` - 组合描述

---

## 完整案例：性别选择器按钮

### Figma 节点信息

**节点 1:379（"不限" 背景 - 已选中状态）**

`design.json[1:379]`（数据包字段，颜色已规范化为 `rgba(...)` 字符串；为了便于对照，下面同时展示 Figma 原始 fills 结构）：

```json
{
  "id": "1:379",
  "name": "Rectangle 9备份 3",
  "type": "VECTOR",
  "fills": [
    {
      "opacity": 0.1,
      "type": "SOLID",
      "color": {"r": 1.0, "g": 0.9647, "b": 0.0235}  // #FFF606
    }
  ],
  "strokes": [
    {
      "type": "SOLID",
      "color": {"r": 1.0, "g": 0.9647, "b": 0.0235}  // #FFF606
    }
  ],
  "strokeWeight": 1.0,
  "strokeAlign": "INSIDE",
  "cornerRadius": 8.0
}
```

**节点 1:382（"男生" 背景 - 未选中状态）**

```json
{
  "id": "1:382",
  "name": "Rectangle 9备份 3",
  "type": "VECTOR",
  "fills": [
    {
      "opacity": 0.1,
      "type": "SOLID",
      "color": {"r": 1.0, "g": 1.0, "b": 1.0}  // #FFFFFF
    }
  ],
  "strokes": [
    {
      "visible": false,
      "type": "SOLID"
    }
  ],
  "strokeWeight": 0.0,
  "cornerRadius": 8.0
}
```

### 判断：用代码绘制 ✅

**检查清单：**

```
✅ 形状简单：矩形
✅ 填充简单：纯色 SOLID（#FFF606 / #FFFFFF）
✅ 无复杂路径
✅ 无布尔运算
✅ 圆角简单：8px 统一圆角
✅ 无复杂效果（effects 全部 visible=false）
✅ 尺寸固定：68×32
```

**结论：** **必须用代码绘制，禁止下载图片！**

### 实现代码

```swift
private class GenderButton: UIControl {
    
    private let buttonTitle: String
    private var isButtonSelected: Bool
    
    /// 背景视图（代码绘制）
    /// Figma 节点 1:379（已选中）/ 1:382（未选中）
    private lazy var genderBackgroundView: UIView = {
        let v = UIView()
        v.layer.cornerRadius = 8  // Figma cornerRadius
        v.layer.masksToBounds = true
        v.isUserInteractionEnabled = false
        return v
    }()
    
    private lazy var titleLabel: UILabel = {
        let label = UILabel()
        label.textAlignment = .center
        return label
    }()
    
    init(title: String, isSelected: Bool) {
        self.buttonTitle = title
        self.isButtonSelected = isSelected
        super.init(frame: .zero)
        setupUI()
        setupConstraints()
        updateAppearance()
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    private func setupUI() {
        addSubview(genderBackgroundView)
        addSubview(titleLabel)
        titleLabel.text = buttonTitle
    }
    
    private func setupConstraints() {
        genderBackgroundView.snp.makeConstraints { make in
            make.edges.equalToSuperview()
        }
        
        titleLabel.snp.makeConstraints { make in
            make.center.equalToSuperview()
        }
    }
    
    private func updateAppearance() {
        if isButtonSelected {
            // Figma 节点 1:379 - 已选中背景 / 边框 / 文字 → 查 color_map + font_map
            genderBackgroundView.backgroundColor = MKUIStyle.mk_c26_10() /* 示例：以 color_map 为准 */
            genderBackgroundView.layer.borderColor = MKUIStyle.mk_c26().cgColor
            genderBackgroundView.layer.borderWidth = 1.0
            titleLabel.textColor = MKUIStyle.mk_c26()
            titleLabel.font = MKUIStyle.mk_f14_m()

        } else {
            // Figma 节点 1:382 - 未选中
            genderBackgroundView.backgroundColor = UIColor(white: 1.0, alpha: 0.1) /* 或 color_map 命中值 */
            genderBackgroundView.layer.borderWidth = 0
            titleLabel.textColor = MKUIStyle.mk_c12_80() /* 示例：以 color_map 为准 */
            titleLabel.font = MKUIStyle.mk_f14()
        }
    }
}
```

### 为什么不下载图片？

**如果下载图片会遇到的问题：**

1. ❌ **图片格式 / 体积代价**：简单形状若也走切图，需要导出多倍图（@2x/@3x）才能保证清晰度，包体积无谓增大；而 iOS 原生不支持 SVG，无法直接复用 Figma 的矢量数据

2. ❌ **无法动态修改颜色**
   - 设计稿改了颜色，需要重新下载图片
   - 无法适配深色模式

3. ❌ **增加维护成本**
   - 每个状态需要 2 张图片（@2x + @3x）
   - 修改圆角/边框需要重新制作图片

**用代码绘制的优势：**

1. ✅ **零体积**：不增加包大小
2. ✅ **动态修改**：可以改颜色、圆角、边框
3. ✅ **适配各种尺寸**：不会模糊
4. ✅ **性能更好**：不需要加载图片资源
5. ✅ **维护简单**：修改一行代码即可

---

## 总结

### 决策原则

1. **简单图形 → 代码绘制**（矩形、圆、渐变）
2. **复杂图形 → 下载图片**（布尔运算、多路径、美术字）
3. **有 iconfont → 用 iconfont**（最优）
4. **有疑问 → 优先代码，实在不行再下载**
5. **判断仅依赖数据包字段（type / fills / corner_radius / vector_geometry / export.is_export_asset），不再调 MCP 或 Figma REST API**

### 优先级

```
iconfont > 代码绘制 > 下载图片
```

### 验收标准

- ✅ 简单矩形、圆角不能下载为图片
- ✅ 布尔运算、≥3 路径必须下载为图片
- ✅ 所有代码绘制必须标注决策理由
- ✅ 所有下载图片必须使用语义化命名
- ✅ iOS 12 兼容性检查
- ✅ **下载图片前必须检查文件类型（PNG/SVG）**
