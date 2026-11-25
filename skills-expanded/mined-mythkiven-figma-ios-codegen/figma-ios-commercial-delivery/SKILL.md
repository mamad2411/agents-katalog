---
name: figma-ios-commercial-delivery
description: >-
  Quality bar for the **phase-2 baseline UI code** produced by this repo's
  Figma-to-UIKit/Swift workflow (not phase-3 production code, which is out of scope
  here). Covers: acceptance checklist, forbidden shortcuts, the UI-node-coverage
  audit, and when human input is still required. The "commercial" in the name refers
  to the phase-2 quality floor ("no shortcuts / no fabricated content / no missing
  nodes"), not to final production-ready business code — production code is produced
  in phase 3 by combining this baseline with PRD + API docs. Use when generating or
  reviewing the phase-2 Figma-based iOS UI output.
---

# Figma → iOS：阶段 2 基础 UI 代码 · 质量底线（验收）

## 📌 「商用」一词的澄清

本 skill 名字里的 **commercial-delivery / 商用** 指的是 **阶段 2 基础 UI 代码的质量底线**，不是「直接上线的最终业务代码」。

- ✅ 本 skill 管：UI 节点覆盖率 100%、无编造资源、无假 URL、无跳过规则以外的偷工、颜色/字体走 bindings、相对布局语义。
- ❌ 本 skill **不**管：接口对接、ViewModel、路由、埋点、错误处理——这些是 **阶段 3**（PRD + 接口文档二次加工）的职责。

简单说：阶段 2 保证交给阶段 3 的「UI 地基」干净、完整、可识别；阶段 3 在此之上盖业务楼。

## 职责边界

- **负责**：规定 **阶段 2 基础 UI 代码** 的最低质量标准（自检清单、禁止项、须显式声明的依赖）。
- **不负责**：重复 `figma-ios-design-token-mapping`、`figma-ios-minimum-deployment-12`、`figma-ios-to-code-conventions`、`figma-ios-snapkit-layout` 的正文；以链接为准。
- **不负责**：阶段 3 的任何内容（接口接入 / ViewModel / 业务逻辑 / 埋点），这些应该保留 `// TODO(阶段3): ...` 注释，交给阶段 3。

## 目标（与「来回改细节」的关系）

阶段 2 一次产出应尽量 **自带** 布局策略、bindings 色/字映射、可维护结构，使 UI 地基**默认就接近主工程可合入水平**（只剩阶段 3 的数据/业务补完）。  
**仍可能**需要人工或第二轮的情况见文末「仍须确认」——Agent 应在代码注释或回复中 **一次性列清**，而不是留到用户追问。

## 宿主前提（不满足则必须在交付物中写明）

- 已配置 `.cursor/bindings/`（`host.json` + 三张 map）；生成时按配置输出，**不要**在 skill/代码里强制写死某宿主 SDK `import`。
- 布局：按 `host.layout_engine`（如 snapkit）；若工程无对应库，用 `NSLayoutConstraint`/`anchor`，**语义仍须是相对约束**。

## 类名前缀（强制）⚠️

所有新建的顶层 `class` / `struct` / `enum` / `protocol` / `actor` 必须以**业务类前缀 `<P>`** 开头（见 `host.json` 的 `class_prefix` / `class_prefix_fallback`，以及 [`PROJECT_BINDING` §0](../figma-ios-PROJECT_BINDING.md#0-类名前缀class_prefix)）。

- ViewController → `<P>FillOrderViewController`
- View → `<P>OrderHeaderView`
- Cell → `<P>RequirementCell`
- Model / Service / ViewModel → `<P>RequirementModel` / `<P>RequirementService`

**豁免**（仅这些，不加业务前缀）：
- `extension`（跟着主类名）
- **引用**宿主已有类型：`host.bases.*` 里的基类名、以及 color/font/iconfont map **value 里已出现的类型**（只引用、不新建）
- `private` / `fileprivate` 的文件内辅助类型

不必再单独列宿主类名豁免表。

## 交付前自检（生成或审阅时逐项打勾）

> **前置硬约束**：本节自检与 [`figma-ios-codegen-workflow` §「全量还原原则」](../../rules/figma-ios-codegen-workflow.mdc) 共同生效。**任何一项不通过就不算交付完成**，禁止以"已实现主要功能"为由跳过剩余自检。

### 0. 节点覆盖率对账（强制，先于其他所有自检）⭐️

视觉验收无法判断"少画了什么"——必须先用节点 ID 做结构化对账。

**对账步骤**：

1. 从 `{data_dir}/index.json` 的 `by_id` / `tree` 提取**应实现节点集合 S**，剔除以下：
   - `figma-ios-to-code-conventions` 跳过项（Home Indicator / Status Bar / Device Frame / 设计标注）
   - 父节点已生成且本节点是 `_role.is_transparent_wrapper` / `_role.is_single_child_wrapper` 的纯结构容器
2. 从生成的 Swift 代码中提取**已实现节点集合 G**：
   - 每个 view / cell / 配置块都应在代码注释里有 `// Figma node: <node_id>` 标记
   - 用 `rg "Figma node:" <output_dir>` 拉取所有 node_id
3. 计算 `missing = S - G`，输出**节点覆盖率报告**（强制，必须在回复正文里贴出）：

```
节点覆盖率报告
─────────────────────────
应实现节点数：N
已实现节点数：M
覆盖率：M/N = X%

✅ 已实现（按 frame.relative.y 排序，便于对照截图）：
  - 1:280  AppCategoryListViewController（根容器）
  - 1:291  导航栏
  - 30:8689 品类 icon
  ...

❌ 未实现：
  - 30:9001 标签组容器     原因：?
  - 30:9015 价格步进器     原因：?
  - 30:9020 段位选择器     原因：?

⚠️ 已豁免（属于「唯一允许的简化场景」之一，须注明依据）：
  - 30:9100 服务器下发图片占位（依据：场景 1，已加 TODO）
```

**判定**：
- ❌ 节列表非空 且 无显式豁免理由 → **未通过**，按 [`figma-ios-codegen-workflow` §「未完成处置模板」](../../rules/figma-ios-codegen-workflow.mdc) 立即继续生成，**禁止使用降级话术包装缺漏**（详见下文「回复纪律」章节）
- ⚠️ 全部缺失项都属「唯一允许的简化场景」三类 → 通过，但每条都需在代码 + 报告里写明依据
- ✅ `missing == ∅` → 通过，进入下面的质量自检

#### 0.1 假覆盖检测（必须做，否则覆盖率报告无意义）⚠️

**只在代码注释里写 `// Figma node: <id>` 不足以证明节点真的实现了**。下面这些是「假覆盖」，必须算作未实现并补齐：

| 假覆盖模式 | 例子 | 判定 |
|---|---|---|
| **整组用切图代替含语义子节点的容器** | `stepStripImageView` 用一张 `img_7ebee_3` 代替了 6 个 STEP 文本/箭头子节点 | 子节点全部算未实现，按 [`figma-ios-vector-vs-code` §「红线规则」](../figma-ios-vector-vs-code/SKILL.md) 拆解 |
| **hardcode 文字数组** | `let titles = ["排位赛","娱乐赛","QQ区"]` | 每个字符串对应的 TEXT node_id 都算未实现，必须改成读 `design.json[node].text` |
| **绕过映射表硬编码色** | 未查 `color_map.json` 就写死色值/臆造 token | 视为「样式未实现」，按 [`figma-ios-design-token-mapping`](../figma-ios-design-token-mapping/SKILL.md) 重做（命中 map / 未命中 fallback） |
| **hardcode 尺寸/坐标 但与 design.json 不一致** | offset(49) 但 `frame.relative.y == 96` | 视为「布局未实现」，按 `frame.relative` 修正 |
| **图标用普通 UIView 替代 iconfont 节点** | `let plus = UIButton(title:"+")` 代替 `iconfont/icon_plus_24` | iconfont node 算未实现，按 [`figma-ios-iconfont-mapping`](../figma-ios-iconfont-mapping/SKILL.md) 重做 |
| **节点级 `opacity` 漏读**（⭐️常见事故） | `design.json[341:277].opacity = 0.2033`，代码里没设 `view.alpha` | 视为「样式未实现」，按 [`figma-ios-to-code-conventions` §5](../figma-ios-to-code-conventions/SKILL.md) 补 `view.alpha = opacity` |
| **文件顶部映射表与代码不一致** | 表里写 `→ 拆解`，但代码里只 addSubview 了一个 ImageView | 视为不合规，必须二选一：要么补齐子节点，要么改表格说明真用了切图（同时通过红线检查） |

**自检方法**：

```bash
# 1. 拉所有 Figma node 注释
rg -o "Figma node: ([0-9I:;]+)" -r '$1' <output_file> | sort -u > /tmp/coverage_claimed.txt

# 2. 拉所有 hardcode 文字（中文字符串）
rg '"[\u4e00-\u9fa5]+"' <output_file>     # 每条都要能在 design.json[*].text 找到对应 node_id

# 3. 拉所有 hardcode hex 颜色
rg 'withHexString: "#[0-9A-Fa-f]{6}"' <output_file>  # 每条都要能在 design.json[*].fills 找到

# 4. 拉所有非 1.0 的节点 opacity（每条都必须在代码里有 view.alpha = ...）
python3 -c "
import json
d = json.load(open('design.json'))
for nid, n in d['nodes'].items():
    op = n.get('opacity')
    if op is not None and op != 1.0:
        print(f'{nid}  opacity={op}  name={n[\"name\"]}')
"

# 5. 对照 index.json 检查覆盖率（含上面的假覆盖修正）
```

**实现 hint**：按 `design.json.nodes` 对账生成代码里的 `// Figma node: <node_id>` 注释；自动剔除 Home Indicator / Status Bar / Device Frame / 设计标注 / iconfont_library / `audit.placeholder_rectangles[].must_skip` 节点及其后代。LLM 不用自己数节点，只要**保证每个生成的 view 都带 `Figma node:` 注释**即可。

#### 0.2 高风险字段对账（必须做，与 audit.json 配套）⚠️⚠️

`audit.json` 列出的每条 entry 都**必须**在生成代码里有对应处理。**不查 audit = 交付不算完成**。

**强制对账流程**：

1. 读 `{data_dir}/audit.json`
2. 对 7 类字段逐一对账：

| audit 字段 | 必须在代码中能找到 | 缺失则视为 |
|---|---|---|
| `non_default_opacity[].node_id` | `view.alpha = <opacity>` 在该节点对应 view 上 | **样式未实现** |
| `non_solid_fills[].node_id`（GRADIENT） | `CAGradientLayer` / `applyGradient` / `MKGradientView` 等 | **样式未实现** |
| `non_solid_fills[].node_id`（IMAGE） | `UIImage(named:)` 引用 `assets/ios/manifest.json` 里的资源 | **资源未挂** |
| `non_solid_strokes[].node_id` | `CAShapeLayer` mask + `CAGradientLayer` 实现渐变边框 | **边框未实现** |
| `with_effects[].node_id` | `layer.shadow*` 或 `UIVisualEffectView` | **阴影未实现** |
| `non_standard_fonts[].node_id` | 查 `font_map`；未命中则 `UIFont(name:)` + systemFont fallback | **字体退化** |
| `letter_spacing[].node_id` | `NSAttributedString` `.kern = <value>` | **字距漏读** |
| `non_normal_blend_modes[].node_id` | `CALayer.compositingFilter = ...` 或自绘 | **混合模式未实现** |
| `list_containers[].node_id`（⭐红线） | `UICollectionView`（按 `scroll_axis` 选 horizontal/vertical FlowLayout） | **列表退化** |
| `export_asset_with_semantic_children[].node_id`（⭐红线） | 拆解为子节点逐一实现，**禁止**用 `UIImage(named:)` 整组替代 | **切图吞掉子树** |

3. **任何一项不通过 → 必须补，不能在「视觉差异不大」名义下放过**。

**自检**：对照 `audit.json` 逐条对账。详见 [`figma-ios-codegen-workflow` §2.0](../../rules/figma-ios-codegen-workflow.mdc)。

### 1. 节点
按 [figma-ios-to-code-conventions](../figma-ios-to-code-conventions/SKILL.md) 跳过 Home Indicator 等系统装饰；业务图层无多余重复。
### 2. 布局
主要 UI **非**「整屏 `frame` 堆砌」；相对约束 + SnapKit（或等价的 Auto Layout）；安全区、横竖屏/不同宽度下无灾难性断裂（至少 leading/trailing 有依据）。

### 3. 色与字
颜色与字体走 [figma-ios-design-token-mapping](../figma-ios-design-token-mapping/SKILL.md)：先查 `.cursor/bindings` map；**仅未命中时**才用 fallback 的 `UIColor` / `UIFont`；禁止臆造未在 map 中的设计系统 API。

### 4. 系统版本
符合 [figma-ios-minimum-deployment-12](../figma-ios-minimum-deployment-12/SKILL.md)；无未包裹的 iOS 13+ API。

### 5. 可维护
子视图职责清晰；魔法数尽量收拢为 `private enum`/`static let` 并注明对应 Figma 节点或尺寸含义。

### 6. 资源与网络
图片若有占位，须标注 **占位** 与后续替换方式；异步加载须有取消/弱引用，避免泄漏与崩溃。

### 7. 导航/状态栏（强制）
- **若 `host.json` 的 `vc_required_overrides` 非空**：每个生成的 VC 必须按模板实现；`{has_custom_nav}` 按是否使用 `navigation.custom_nav_class` 替换
- `navigation.strategy == "system"` → 用系统导航栏，不强制宿主钩子
- 若全屏自定义顶栏，须处理返回栈预期（避免闪栏、叠栏），与宿主约定一致时在注释中写一句。

### 8. 无障碍（⚠️ 当前未实现）
当前生成的代码**不包含**无障碍属性（`accessibilityLabel` / `accessibilityTraits` / `isAccessibilityElement`）。如项目有无障碍要求，需人工补充。

### 9. Swift / OC 互操作（按需）
**仅当** `host.base_is_objc == true` 或用户明确要求 OC 混编时，才按下文「Swift / OC 互操作约定」加 `@objc` / `@objcMembers`。  
纯 Swift / 系统基类场景**不必**默认加 `@objcMembers`，也**不必**写宿主 SDK 的 `import`。

## 回复纪律（禁止的措辞模式，与「全量还原原则」配套）⛔

> 这一节直接针对 LLM 在交付时使用客服式"礼貌降级"话术，把规范包装成偏好的反模式。

| ❌ 禁止使用 | 为什么禁止 | ✅ 正确写法 |
|---|---|---|
| 「若你希望下一步把 X / Y 也按节点 ID 全部对齐，我可以继续……」 | 把"全量还原"这一**默认规范**包装成"可选服务"，让用户误以为缺漏是默认状态 | 「本轮已实现 A / B / C，design.json 中 D / E / F（节点 ID: ...）未实现，**违反全量还原原则**，现在继续补齐」 |
| 「为简化代码示例，省略了 ...」 | 简化不是默认许可的；除非属于「唯一允许的简化场景」三类 | 直接生成完整代码；上下文不足按 workflow 「未完成处置模板」声明 |
| 「当前为简化版，需要可补全」 | 同上，把规范当偏好 | 不发生这种交付；若真的截断，按未完成模板**先声明再继续** |
| 「视觉差异不大」/「整体已对齐」（实际上少了节点） | 用视觉相似度掩盖结构性缺漏 | 必须先输出节点覆盖率报告，再谈视觉相似度 |
| 「这一版本未实现，如有需要可继续完善」 | 同样是把缺漏伪装成增值服务 | 「未实现节点：[列表]，原因：[token/上下文限制]，正在继续补齐」|

**自检触发条件**：在生成回复**最终文本前**，必须扫描自己的回复草稿，命中上表任一句式 → **改写**为右列正确写法 → 再发送。

## Swift / OC 互操作约定（仅 `host.base_is_objc == true` 或用户要求时）

### 类声明

- 需要被 OC 调用时：类可加 `@objcMembers`；访问级别与基类一致。
- **不要**无脑加 `@objcMembers`；纯 Swift UIKit 场景可省略。
- **不要**在 skill 里强制写某宿主 SDK 的 `import`。

```swift
// 示例：系统基类 + 业务前缀（来自 host）
class AppCategoryListViewController: UIViewController {
    var categoryRows: [CategoryRow] = []
}
```

- **纯 Swift 类型**（`struct` / `enum` / 泛型）不能 `@objc`，只在 Swift 内使用。

### 访问级别 + 协议一致性（生成时强制规避，禁止事后修补）

**报错形态**：
```
Method 'collectionView(_:numberOfItemsInSection:)' must be declared public
because it matches a requirement in public protocol 'UICollectionViewDataSource'
```

**根因**：类被声明为 `public` / `open` 时，实现 `public` 协议（`UICollectionViewDataSource` / `UITableViewDataSource` / `UIScrollViewDelegate` 等）的方法访问级别必须 ≥ `public`，而 `extension` 默认是 `internal`。

#### 生成阶段强制流程（按基类访问级别匹配）

**Step 1：在生成代码前，先探测宿主基类访问级别**

宿主工程的基类（读 `host.json` → `bases.view_controller`，下称 `<VC_BASE>`）可能是 `public`、`open` 或 `internal`，三种情况生成的代码不同：

```bash
# Agent 在生成代码前必跑（把 <VC_BASE> 换成 host 里的实际类名）
rg -n "^(public |open |@objc public |@objc open )?class\s+<VC_BASE>\b" <host_project_root>
rg -n "^@interface\s+<VC_BASE>\b"  <host_project_root>
```

判定规则：

| 基类形态 | 生成的 Swift 类 | 协议实现 extension |
|---|---|---|
| `open class <VC_BASE>` | `open class XxxVC: <VC_BASE>` | `extension XxxVC: ... { open func ... }` |
| `public class <VC_BASE>` | `public class XxxVC: <VC_BASE>` | **`public extension XxxVC: ... { ... }`** |
| `class <VC_BASE>`（internal） | `class XxxVC: <VC_BASE>` | `extension XxxVC: ... { ... }` |
| OC `@interface <VC_BASE>` | `class XxxVC: <VC_BASE>` | `extension XxxVC: ... { ... }` |
| 探测失败 / 无法访问宿主源码 | **保守默认走 internal**，文件顶加 NOTE | 同上 |

**Step 2：基于探测结果选模板**

✅ **基类是 `public` 时唯一正确写法**（整个 extension 加 `public`，一次性提升所有方法）：

```swift
public class AppCategoryListViewController: UIViewController { ... }

// MARK: - UICollectionViewDataSource
public extension AppCategoryListViewController {
    func collectionView(_ collectionView: UICollectionView,
                        numberOfItemsInSection section: Int) -> Int { ... }
}
```

✅ **基类是 internal / OC 时**（默认场景，最简洁）：

```swift
class AppCategoryListViewController: UIViewController { ... }

// MARK: - UICollectionViewDataSource
extension AppCategoryListViewController: UICollectionViewDataSource {
    func collectionView(_ collectionView: UICollectionView,
                        numberOfItemsInSection section: Int) -> Int { ... }
}
```

❌ **绝对禁止的反模式**：

```swift
public class AppCategoryListViewController: UIViewController { ... }

// 类是 public，extension 默认 internal —— 必报「must be declared public」
extension AppCategoryListViewController: UICollectionViewDataSource {
    func collectionView(_ cv: UICollectionView, numberOfItemsInSection s: Int) -> Int { ... }
}
```

#### 自检（生成完成后回头看一次）

- [ ] 类访问级别与基类一致（不要无脑 public）
- [ ] 若类是 `public`/`open`，**所有协议实现 extension 也是 `public`/`open`**
- [ ] 同一个文件内，类与 extension 的访问级别一致
- [ ] 无法探测时已选择保守的 internal 默认，并加注释说明

### 重写 OC 基类方法

若基类为 OC（host.base_is_objc），其可重写方法，Swift 子类重写时**必须显式加 `@objc`**（即使类已 `@objcMembers`，重写场景仍需要），见 [figma-ios-navigation](../figma-ios-navigation/SKILL.md)。

### OC 互操作自检

- [ ] 仅当需要 OC 互操作时才加 `@objcMembers`（见 host.base_is_objc）
- [ ] 类访问级别 = 基类访问级别（见下文探测流程；默认 internal）
- [ ] 若类是 `public`/`open`，**所有协议实现 extension 也用 `public`/`open`**
- [ ] 重写 OC 方法显式加了 `@objc`
- [ ] 不向 OC 暴露 struct / 关联值 enum / 泛型类
- [ ] **若 host.`vc_required_overrides` 非空**：已按模板实现（含 `{has_custom_nav}` 替换）

## 禁止项（默认不允许出现在「交付」里）

- `// TODO` / `FIXME` 且无替代方案说明。
- 整页业务布局仅靠 `layoutSubviews` 里写死 `frame`（无约束）作为 **唯一** 手段。
- 绕过 bindings map 臆造设计系统 API，或未命中时不用 fallback。
- 无条件使用 SF Symbols、`UIStatusBarStyle.darkContent`、`CALayerCornerCurve` 等 **未** 按 `figma-ios-minimum-deployment-12` 处理。

## 仍须产品/宿主确认（须在交付时一次性写清）

- 接口、文案、埋点、路由、权限、多语言。
- 设计稿未给出的 **空态 / 错误态 / 加载态**。
- 宿主 **未** 声明 layout_engine / 导航策略等——须在注释或回复中列出假设。
- **无障碍属性**：当前未自动生成，如项目有 VoiceOver/无障碍要求，需人工补充或等待 `figma-accessibility` Skill 实现（见 [MAINTAINER_GUIDE.md](../MAINTAINER_GUIDE.md) P1 第 3 条）。

## 相关

- **总入口**：[figma-ios-playbook](../figma-ios-playbook/SKILL.md)
- **布局**：[figma-ios-snapkit-layout](../figma-ios-snapkit-layout/SKILL.md)
