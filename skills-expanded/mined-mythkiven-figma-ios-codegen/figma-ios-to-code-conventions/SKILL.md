---
name: figma-ios-to-code-conventions
description: >-
  Conventions for turning a figma-ios-preload-data data package (design.json) into app UI
  (UIKit): which nodes to skip, how to treat design-only chrome (Home Indicator /
  Status Bar / Device Frame / 设计标注). Use when implementing Figma designs from
  the data package, or when the user asks for Figma-to-code skip rules.
---

# Figma → 代码：约定与跳过规则

从 `figma-ios-preload-data` 数据包（`design.json` / `index.json`）**还原业务界面** 时，除用户另有说明外，遵守下列规则。后续可在本文 **「规则列表」** 中追加条目（保持编号递增）。

## 规则列表

### 1. 忽略 Home Indicator（系统底部横条）

**必须跳过的节点**（不要生成任何代码）：

- **节点类型**：`INSTANCE`、`COMPONENT`、`FRAME` 或任何其他类型
- **节点名称匹配**（任一即跳过）：
  - 完全匹配：`Home Indicator`、`home indicator`
  - 包含关键词：`Home Indicator/`（如 `系统控件/home indicator/dark`）
  - 包含关键词：`iPhone X/Home Indicator`
  - Component ID: `1:31` 或类似系统组件 ID

**识别特征**：
- 通常位于页面底部（y ≈ 页面高度 - 34）
- 尺寸：width ≈ 页面宽度, height ≈ 34pt
- 外观：白色或黑色的圆角横条（宽约 134pt，高约 5pt）

**匹配规则（强制）**：
```javascript
// 跳过 Home Indicator 的判断逻辑
function shouldSkipNode(node) {
  const name = node.name.toLowerCase();
  
  // 规则 1: 名称包含 "home indicator"
  if (name.includes('home indicator')) {
    return true;
  }
  
  // 规则 2: 名称包含 "home-indicator"（短横线）
  if (name.includes('home-indicator')) {
    return true;
  }
  
  // 规则 3: 特定 component ID（视具体文件而定）
  if (node.id === '1:31' || node.id === '1:326') {
    return true;
  }
  
  return false;
}
```

**Swift 代码生成时**：
- ❌ **禁止**：创建 `homeIndicatorView`、`homeIndicatorLayer` 等属性
- ❌ **禁止**：为 Home Indicator 添加 `addSubview`、约束、样式
- ❌ **禁止**：下载 Home Indicator 相关的图片资源
- ✅ **正确**：完全跳过该节点及其子树，就像它不存在一样

**原因**：
- iOS 系统会自动在设备上绘制 Home Indicator（iPhone X 及以上）
- Figma 中的 Home Indicator 只是设计稿示意，不是真实 UI
- 在代码中实现会导致：
  - 重复渲染（系统已经有了）
  - 与系统手势区域冲突
  - 在 iPhone 8 及以下设备显示错误的横条

**做法**：
1. 遍历 `design.json` 节点树（或 `index.json` 的扁平列表）时，检查节点名称
2. 如果匹配 Home Indicator，完全跳过该节点及其子树
3. 不要将其坐标用于计算其他元素的布局（除了判断安全区域）
4. 注释中可说明"已跳过 Figma 中的 Home Indicator（系统控件）"

### 2. 忽略状态栏（Status Bar）

**必须跳过的节点**（不要生成任何代码）：

- **节点名称匹配**（任一即跳过）：
  - 完全匹配：`Status Bar`、`status bar`、`状态栏`
  - 包含关键词：`系统控件/status bar`、`iPhone Status Bar`
  - 包含关键词：`状态栏/`

**识别特征**：
- 位于页面顶部（y = 0 或接近 0）
- 高度：20pt（iPhone 8 及以下）或 44pt（iPhone X 及以上）
- 包含时间、信号、电池等元素

**原因**：
- iOS 系统自动绘制状态栏
- 应用只能通过 `statusBarStyle` 控制状态栏样式（浅色/深色）
- 在 `Info.plist` 中配置 `UIStatusBarStyle`

**做法**：
- 完全跳过该节点及其子树
- 布局顶部元素时使用 `safeAreaLayoutGuide.snp.top`

### 3. 忽略设备外壳（Device Frame）

**必须跳过的节点**（不要生成任何代码）：

- **节点名称匹配**（任一即跳过）：
  - 完全匹配：`Device`、`iPhone Frame`、`设备外壳`
  - 包含关键词：`iPhone 14 Pro Frame`、`Device Mockup`
  - 节点类型为设备外壳的 Component

**识别特征**：
- 包含物理设备的外形、刘海、边框等
- 尺寸大于实际内容区域
- 通常在最外层或作为背景

**原因**：
- 设备外壳只是设计稿展示用
- 实际应用运行在真实设备上，不需要模拟外壳

### 4. 忽略设计标注和说明

**必须跳过的节点**（不要生成任何代码）：

- **节点名称匹配**（任一即跳过）：
  - 包含关键词：`标注`、`annotation`、`说明`、`note`
  - 节点名称以 `//` 或 `#` 开头（注释性节点）
  - 包含关键词：`设计说明`、`Design Note`

**识别特征**：
- 通常是文本或线条
- 用于设计师之间沟通
- 颜色通常是醒目的红色或黄色

**原因**：
- 这些是设计过程的辅助信息
- 不是最终用户看到的 UI

### 5. 节点级 `opacity` 必须落地（红线）

**问题描述**：Figma 节点除了 `fills/strokes` 自身可以带 alpha，节点本身还有一个独立的 `opacity` 字段（取值 0~1，默认为 1.0）。它表示**整个 layer 的整体透明度**，会在 fills/strokes/effects/children 渲染完成后**再叠加一次乘 alpha**。漏读这个字段，会导致看上去颜色/亮度都对，但实际「太重」「太亮」「太醒目」。

**强制规则**：

1. 生成任何视觉节点（TEXT / RECTANGLE / FRAME / VECTOR / INSTANCE 等）的代码前，**必须读取 `design.json[node].opacity`**：
   - `opacity == None` 或 `opacity == 1.0` → 无需处理
   - `0 < opacity < 1.0` → **必须**在生成的 view 上应用 `view.alpha = opacity`（UIKit）
   - `opacity == 0` → 节点不可见，等价于跳过（但仍占位置，不要去掉布局）

2. **位置**：`alpha` 应作用在**该 Figma 节点对应的最外层 UIView** 上。
   - TEXT 节点 → `label.alpha`
   - 容器节点 → `containerView.alpha`（注意会传递给所有子 view，与 Figma 行为一致）
   - iconfont label → `iconLabel.alpha`

3. **不要**用 `UIColor(..., alpha: opacity)` 伪装节点级 opacity——这只能作用在颜色上，丢失节点对子 view 的整体衰减。

**自检（强制）**：

生成代码前，在数据包目录跑一次：

```bash
python3 - << 'PY'
import json
d = json.load(open('design.json'))
print("=== 节点级 opacity != 1.0 的节点 ===")
for nid, n in d['nodes'].items():
    op = n.get('opacity')
    if op is not None and op != 1.0:
        print(f"  {nid}  {n['type']}  '{n['name']}'  opacity={op}")
PY
```

把输出列表逐个核对：
- 是要渲染的节点 → 必须带 `view.alpha = opacity` 进入代码
- 是 iconfont 内部子矩形 / Home Indicator / Status Bar → 跳过（因为整个父节点本来就不渲染）

**反例**（曾经发生过的事故）：

```swift
// ❌ 漏读 opacity，看上去字太亮太重
let l = UILabel()
l.text = "STEP.1"
l.font = MKUIStyle.mk_f16() /* 等宽数字场景：优先 font_map；未命中再用 monospacedDigitSystemFont */

applyGradient(...)  // 颜色对了

// ✅ 正确：节点 341:277 数据包里 opacity=0.2033
let l = UILabel()
l.text = "STEP.1"
l.font = MKUIStyle.mk_f16() /* 等宽数字场景：优先 font_map；未命中再用 monospacedDigitSystemFont */

applyGradient(...)
l.alpha = 0.2033  // ⭐️ 节点级 opacity 必须落地
```

**原因**：fills 自带的 alpha 与节点 opacity 是**两个独立通道**，Figma 渲染管线先做 fills，再乘节点 opacity，再混合。漏掉任意一层都会出视觉差异。

### 6. 占位 RECTANGLE 必须跳过（红线，多维识别）

**问题描述**：Figma 设计师常使用纯色 RECTANGLE 作为**区域占位/对齐参考/蒙版/未来填图占位**。它在 Figma 设计稿中通常配合上层蒙版/混合模式/最终切图，**最终视觉效果是不可见或被完全覆盖**。漏掉这条规则的后果是：在 bg 切图（深色星空底）上**叠了一块大灰矩形**，把整个表单区域全部遮成实色，业务内容也跟着被盖掉。

> ⚠️ **不要用单一颜色 + 命名硬编码**——之前曾用「D9D9D9 + 通用命名 + 无样式」三条硬编码识别，结果只命中 1 个节点（341:312），漏掉了一大批 alpha≈0.0001 的蒙版节点（设计师可能用任意颜色 + 极低 alpha 标记 mask）。**现在采用多维信号**，由 `audit.json.placeholder_rectangles[]` 自动产出，每条带 `confidence` + `reasons`，不依赖任何颜色硬编码。

**判定规则**（满足任一即 `must_skip=True / confidence=high`，由 `figma-ios-preload-data/src/normalize/audit.py::_classify_placeholder_rectangle` 自动跑）：

| # | 信号 | 强度 | 说明 |
|---|---|---|---|
| **D** | 被同父 `is_export_asset` sibling **完全覆盖** | ★★★★★ | 决定性证据：最终视觉被切图盖住，渲染它就是错的（**与颜色无关**） |
| **E** | 节点级 `opacity ≤ 0.05` | ★★★★ | 设计师明示透明 |
| **B2** | fills 唯一 SOLID 且 fill alpha ≤ 0.05 | ★★★★ | 蒙版式占位（任意颜色 + 极低透明度） |

**附加规则**（仅"中等置信度"，`confidence=medium`，仍建议跳过）：

| # | 信号组合 |
|---|---|
| **A+B1+C** | 通用命名（`Rectangle\d*` / `矩形N` / `蒙版` / `mask` / `Frame N` / `bg` / `占位`） + 颜色 = `#D9D9D9`（Figma 默认填充色） + 无圆角/边框/阴影 |

**业务卡不会被误判的护栏**：

- 有圆角 / 有边框 / 有阴影 → 不是占位（业务卡几乎都有圆角）
- 有 IMAGE / GRADIENT 填充 → 不是占位
- 自定义命名（"主标题背景"、"价格条卡片底"）→ 不会触发弱信号 A
- fill alpha > 0.05 + 不是 D9D9D9 + 不被切图覆盖 + 自定义命名 → 即使是大块 SOLID 也不判占位

**Swift 代码生成时**：

- ❌ **禁止**：保留这个节点的 lazy 属性 / `addSubview` / 约束 / `backgroundColor` 渲染
- ✅ **正确**：跳过该节点，在节点→view 映射表里标 `<skip>`，加注释说明 `// Figma node: 341:312 'Rectangle 11' 占位 RECTANGLE（audit.json placeholder_rectangles, confidence=high, 被 sibling 切图 341:266 完全覆盖），已跳过`

**预防自检**（强制，生成代码前先 `cat audit.json | jq .placeholder_rectangles`，或运行下面脚本）：

```bash
python3 - << 'PY'
import json
audit = json.load(open('audit.json'))
for x in audit['placeholder_rectangles']:
    flag = '🚫' if x['confidence'] == 'high' else '⚠️'
    print(f"{flag} [{x['confidence']:>6}] {x['node_id']}  '{x['name']}'  ({x['color']})")
    for r in x['reasons']:
        print(f"     · {r}")
PY
```

把输出列表的节点全部从生成代码中剔除（包括 `addSubview` / 约束 / lazy 属性 / 节点→view 映射表条目）。

**反例**（曾经发生过的事故，2026-04 / Figma 341:312）：

```swift
// ❌ 错误：把占位 RECT 渲染成实色，整片表单区背景被一块大灰矩形遮住
private lazy var middleDimmingView: UIView = {
    let v = UIView()
    v.backgroundColor = MKUIStyle.mk_cXX() /* color_map: #D9D9D9 alpha=1.0 */
    return v
}()
view.addSubview(middleDimmingView)

// ✅ 正确：完全跳过 341:312
// Figma node: 341:312 'Rectangle 11' 占位 RECTANGLE，已跳过
// audit.json.placeholder_rectangles[0].confidence=high
// 原因：被同父 sibling 切图 341:266 'bg'（is_export_asset=true）完全覆盖
// 表单区背景由 bg 切图（img_51be1_bg）提供
```

**为什么不直接用「颜色硬编码」**：

| 反面案例 | 后果 |
|---|---|
| 假设设计师把占位色改成黑色 `rgba(0,0,0,1)` | 颜色硬编码漏判 → 仍然渲染成黑块遮挡背景 |
| 设计师用 `rgba(255,255,255,0.0001)` 标记蒙版 | 颜色硬编码（只认 D9D9D9）漏判 |
| 业务真有一张 `#D9D9D9` 灰色卡片（带圆角/阴影） | 颜色硬编码会**误删业务节点** |
| 设计师把灰色卡命名为 `Rectangle 99`（业务） | 命名硬编码会**误删业务节点** |

> 多维信号的核心思想：**单一信号都不够强，组合起来才是强证据**。其中信号 D（被切图覆盖）是**与颜色完全无关**的决定性证据——只要"最终视觉被另一层盖住"，无论它什么颜色、什么命名都该跳过。

### 7. 预留后续规则

后续新增规则时，在此追加 `### N. …`，格式建议：**触发条件** → **做法** → **原因**（可选）。

## 通用说明

- 规则优先于「逐节点 1:1 贴齐」：被跳过的节点不参与代码生成。
- 若用户明确要求保留某类节点（例如为截图测试画 Indicator），以用户当次说明为准。
- **布局**：优先相对约束、少用整控件绝对 `frame`；SnapKit 与 Figma 数值对应见 skill **`figma-ios-snapkit-layout`**。
- **颜色 / 字体**：从 `design.json[node]` 读取 `fills[].color`（背景 **与 TEXT 文字色**）、`iconfont.color`（图标）、`font.{family,weight,size}`，查 **`bindings/color_map.json` / `font_map.json`**，见 skill **`figma-ios-design-token-mapping`**。
  - ⚠️ TEXT 节点的 `text` 字段是**字符串**（文案），**没有** `text.color`；文字颜色在 `fills[].color`（`rgba(...)`）。
  - 所有字段已规范化（snake_case + `rgba(...)` 字符串），无需自己解析 Tailwind 或 fills。
- **最低系统**：生成代码默认可在 **iOS 12** 编译运行，见 skill **`figma-ios-minimum-deployment-12`**（避免无条件使用 SF Symbols、`darkContent`、`.cornerCurve` 等）。
- **商用一次交付**：默认可合并主线的自检与禁止项见 skill **`figma-ios-commercial-delivery`**。

## 相关

- **总入口**（推荐流程、Skill 索引、新增 Skill 防重叠规则）：[figma-ios-playbook](../figma-ios-playbook/SKILL.md)
- **相对布局与 SnapKit**：[figma-ios-snapkit-layout](../figma-ios-snapkit-layout/SKILL.md)
- **商用一次交付验收**：[figma-ios-commercial-delivery](../figma-ios-commercial-delivery/SKILL.md)
