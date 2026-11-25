---
name: figma-ios-component-state-recognition
description: >-
  从 figma-ios-preload-data 数据包（design.json）提取组件各状态的视觉特征（背景色、边框、文字颜色、字体），
  生成带 updateAppearance() 的状态切换代码。
  Use when extracting visual states from Figma components, generating selected/unselected/disabled
  state code, or when user asks about 选中态、状态切换、updateAppearance。
---

# Figma 组件状态特征提取与代码生成

## 职责边界

- ✅ 从数据包 `design.json` 识别组件有哪些**视觉状态**（selected/unselected/disabled/enabled）
- ✅ 提取每种状态的**视觉特征**（背景色、边框、文字颜色、字体字重）
- ✅ 生成 `updateAppearance()` 状态切换代码（Pattern A / Pattern B）
- ✅ 识别**默认选中项**
- ❌ 不识别组件是什么类型（Selector/Stepper/Toggle）→ 见 [figma-ios-standard-components](../figma-ios-standard-components/SKILL.md)
- ❌ 不处理点击后的交互逻辑 → 见 [figma-ios-selection-interaction](../figma-ios-selection-interaction/SKILL.md)
- ❌ 不处理动画效果

---

## ⚡ QUICK_REF

```
⚠️  数据来源：design.json[node_id]（fills / strokes / font / iconfont 已规范化）
          assets/ios/manifest.json（状态图）
          comments.json（评论修正状态颜色）
          禁止跨组件颜色复用（不同组件视觉规范可能不同）

同类节点中，主题色特征 = 已选中；灰色/低透明度 = 未选中
状态差异维度：背景色 / 边框 / 文字颜色 / 字体字重（Regular ↔ Medium）
默认选中：背景/边框/文字用了主题色的那个节点
Pattern A（简单图形）→ 代码绘制背景 + updateAppearance()
Pattern B（复杂图形）→ UIImageView + 两张 asset + updateAppearance()
生成后必查：updateAppearance() 覆盖了所有差异维度 + configure() 里调用了它
```

---

## 状态识别规则

### 规则 0：数据来源

**唯一数据来源**：`{data_dir}/design.json`（图片状态切换：`assets/ios/manifest.json`）

字段已规范化：
- `node.fills[].color` / `node.strokes[].color`：`rgba(...)`（**TEXT 文字色也在 fills，无 `text.color`**）
- `node.text`（字符串文案）/ `node.font.{family,weight,size}`
- `node.iconfont.{symbol,color,size_hint}`
- `node.corner_radius` / `node.opacity`
- `node.comments[]`（高优先级覆盖，详见 figma-ios-comments-integration）

> 阶段 2 不再调 MCP / REST，也不需要判断数据优先级（已在数据包内固化）。

**禁止跨组件颜色复用**：
```
❌ 禁止：品类 Cell 参考性别按钮的颜色
✅ 允许：在代码注释中标注"⚠️  参考节点 X:Y（设计模式相同）"
```

**如果某节点缺字段**：
```
1. 检查 design.json[node_id] 是否存在该节点
2. 仍缺失 → 代码加 TODO 注释 + 用语义默认色，并在 README "待人工确认" 列出
```

### 规则 A：同类节点的差异 = 状态差异

对比并列的同类节点，找视觉差异：

| 特征 | 已选中（Selected）| 未选中（Unselected）| 字段 |
|------|-----------------|-------------------|---------|
| 背景色 | 主题色（如 `#FFF606` alpha 0.1）| 灰色 / 低透明度 | `node.fills[].color` |
| 边框 | 主题色边框 0.5~1px | 无边框 或 灰色 | `node.strokes[].color` / `node.stroke_weight` |
| 文字颜色 | 主题色 | 白色 80% / 灰色 | TEXT 节点 `fills[].color` |
| 字体字重 | Medium / Bold | Regular | `node.font.weight` |
| 背景图片 | 已选中 asset | 未选中 asset | `assets/ios/manifest.json` |

### 规则 B：识别默认选中项

按以下优先级判断哪个节点是默认已选中：

1. 背景色使用主题色 → 已选中
2. 边框色使用主题色 → 已选中
3. 文字颜色使用主题色 → 已选中
4. 字体字重为 Medium / Bold → 已选中
5. 节点名包含 `selected` / `选中` / `active` → 已选中

### 规则 C：Stepper 的 enabled / disabled

对比减少/增加按钮的 `node.opacity`（数据包字段）：
- `opacity = 1.0` → enabled
- `opacity < 0.5` → disabled（灰化状态）

---

## 代码生成

### Pattern A：代码绘制背景（纯色/圆角/简单边框）

**⚠️ 命名注意**：UIKit 属性名冲突详见 [figma-ios-vector-vs-code](../figma-ios-vector-vs-code/SKILL.md) "禁止使用的属性名"（如 `UICollectionViewCell.backgroundView`）

```swift
private class CategoryButton: UIControl {

    private var isButtonSelected: Bool = false

    private lazy var backgroundView: UIView = {
        let v = UIView()
        v.layer.cornerRadius = 8
        v.isUserInteractionEnabled = false
        return v
    }()

    private lazy var titleLabel: UILabel = {
        let label = UILabel()
        label.textAlignment = .center
        return label
    }()

    init(title: String, isSelected: Bool) {
        self.isButtonSelected = isSelected
        super.init(frame: .zero)
        setupUI()
        setupConstraints()
        updateAppearance()
    }

    required init?(coder: NSCoder) { fatalError() }

    func configure(with title: String, isSelected: Bool) {
        titleLabel.text = title
        isButtonSelected = isSelected
        updateAppearance()  // ← 必须调用
    }

    private func updateAppearance() {
        if isButtonSelected {
            // 从 Figma 已选中节点提取
            backgroundView.backgroundColor = MKUIStyle.mk_cXX() /* color_map: #FFF606 alpha=0.1 */
            backgroundView.layer.borderColor = MKUIStyle.mk_cXX() /* color_map: #FFF606 */.cgColor
            backgroundView.layer.borderWidth = 0.946
            titleLabel.textColor = MKUIStyle.mk_cXX() /* color_map: #FFF606 */
            titleLabel.font = MKUIStyle.mk_f14_m() /* font_map */
        } else {
            // 从 Figma 未选中节点提取
            backgroundView.backgroundColor = /* color_map 命中或 UIColor fallback */
            backgroundView.layer.borderWidth = 0  // 未选中时移除边框
            titleLabel.textColor = /* color_map */
            titleLabel.font = MKUIStyle.mk_f14() /* font_map */
        }
    }
}
```

### Pattern B：图片背景（渐变/阴影/特殊形状）

```swift
private func updateAppearance() {
    if isButtonSelected {
        // asset 名称从 {data_dir}/assets/ios/manifest.json 取（见 figma-ios-image-assets-download）
        backgroundImageView.image = UIImage(named: "img_xxxxx_selected")
        titleLabel.textColor = MKUIStyle.mk_cXX() /* color_map: #FFF606 */
        titleLabel.font = /* font_map */
    } else {
        backgroundImageView.image = UIImage(named: "img_xxxxx_unselected")
        titleLabel.textColor = /* color_map */
        titleLabel.font = /* font_map */
    }
}
```

**何时用 Pattern A vs B**：→ 见 [figma-ios-vector-vs-code](../figma-ios-vector-vs-code/SKILL.md)

---

## 常见错误

| 错误 | 修复 | 案例 |
|------|------|------|
| **❌ 跨组件复用颜色（最常见）** | 从 `design.json[node]` 读取该组件自己的颜色 | 品类 Cell 错误复用了性别按钮的文本颜色 |
| **❌ 数据包缺少节点文本颜色** | 标注 TODO + 在 README "待人工确认" 列出，向 figma-ios-preload-data 反馈 | SYMBOL 节点 TEXT 颜色丢失 |
| 所有按钮用相同样式，忽略状态差异 | 在 `updateAppearance()` 中根据 `isButtonSelected` 分支处理 | |
| 字体不随状态变化（固定 Regular）| 已选中用 `mk_f*_m()`，未选中用 `mk_f*()` | |
| 边框始终存在 | 未选中时设 `borderWidth = 0` | |
| `configure()` 中未调用 `updateAppearance()` | 每次更新 `isButtonSelected` 后必须调用 | |

---

## 生成后自检

```
✅ 每个有状态的组件都有 updateAppearance() 方法
✅ updateAppearance() 覆盖：背景色、边框（含 width=0）、文字颜色、字体字重
✅ configure() 或 init() 中调用了 updateAppearance()
✅ 默认选中项正确识别（主题色 → 已选中）
✅ 字体随状态切换（Regular ↔ Medium）
```

---

## 相关

- **组件类型识别**：[figma-ios-standard-components](../figma-ios-standard-components/SKILL.md)（先识别是 Selector/Stepper/Toggle 再来这里）
- **点击交互逻辑**：[figma-ios-selection-interaction](../figma-ios-selection-interaction/SKILL.md)
- **图片 vs 代码绘制判断**：[figma-ios-vector-vs-code](../figma-ios-vector-vs-code/SKILL.md)
- **颜色字体 Token**：[figma-ios-design-token-mapping](../figma-ios-design-token-mapping/SKILL.md)
- **图片资源**：[figma-ios-image-assets-download](../figma-ios-image-assets-download/SKILL.md)
- **总入口**：[figma-ios-playbook](../figma-ios-playbook/SKILL.md)
