---
name: figma-ios-uicollectionview-codegen
description: >-
  根据 Figma 节点数据生成完整的 UICollectionView Swift 代码。
  包括：分析 Cell 子元素 → 推断模型字段 → 生成 Mock 数据 → 
  生成 CollectionView/Cell 代码 → 生成交互逻辑（选中态/日志）。
  Use when generating UICollectionView code from Figma designs.
trigger: 生成 UICollectionView 代码、生成列表代码
dependencies: 依赖 figma-ios-listview-recognition 的识别结果
output: Swift 代码（Model + Mock Data + CollectionView + Cell + 交互）
---

# UICollectionView 代码生成

## ⚡ QUICK_REF（Agent 优先读此处）

**核心定位**：本 SKILL 提供"流程框架 + 指导原则 + 强制约束"，具体如何分析和生成代码由大模型根据实际场景判断。

**本 skill 的定位**：阶段 2 基础 UI 代码生成（UI + 临时模型 + Mock 数据 + 交互骨架），阶段 3 会用 PRD + 接口文档把 mock 换成真实接口、临时模型换成 API 模型，本 skill 不管阶段 3。

**核心流程（6 步）**：

1. **分析 Cell 结构** → 遍历所有子节点，识别布局和元素
2. **推断临时模型字段** → 根据语义推断阶段 2 临时 struct（阶段 3 会用真实 API 模型替换）
3. **生成 Mock 数据** → 阶段 2 **强制**（图片走 `manifest.json.mock.default_image_url`，其他字段语义生成）
4. **生成 CollectionView** → lazy var + layout + DataSource
5. **生成 Cell 代码** → 子视图 + 布局（SnapKit）+ configure 方法
6. **生成交互逻辑** → didSelectItemAt（有选中态 → toggle；无 → print + `// TODO(阶段3): 补业务跳转/网络请求`）

---

### 生成内容清单

| 组件 | 说明 | 必须 |
|------|------|------|
| **Model 定义** | 根据子元素推断字段 | ✅ |
| **Mock 数据** | 从 Figma 提取或生成占位 | ✅ |
| **CollectionView** | lazy var + layout 配置 | ✅ |
| **Cell 定义** | configure(item:) 方法 | ✅ |
| **DataSource** | numberOfItemsInSection + cellForItemAt | ✅ |
| **Delegate** | didSelectItemAt 交互逻辑 | ✅ |
| **LeftAlignedFlowLayout** | 标签集合专用（可选） | ⚠️ |

---

### 强制约束（质量保证）

**✅ 必须遵守**:
- 模型必须包含 `id` 字段
- 必须使用 Model，禁止字符串数组
- 颜色/字体走 bindings map（未命中用 UIKit fallback）
- 布局按 host.layout_engine（默认相对约束；可用 SnapKit 或原生 Auto Layout）
- 交互逻辑：有 `isSelected` → toggle + reload；无 → print
- **访问级别匹配**：DataSource / Delegate 的 extension 访问级别**必须等于宿主类**。详见下方「访问级别匹配规则」。

**❌ 严格禁止**:
- 禁止跳过流程步骤
- 禁止硬编码数据（必须从 Figma 提取或根据语义生成）
- 禁止同时使用 `estimatedItemSize` 和 `sizeForItemAt`
- 禁止生成不完整的代码
- **禁止 `public class` 配 `extension`（默认 internal）的搭配** —— 必报「Method must be declared public」编译错误。

---

### 访问级别匹配规则（强制，避免协议一致性报错）

**报错形态**（这是本规则要根除的）：
```
Method 'collectionView(_:numberOfItemsInSection:)' must be declared public
because it matches a requirement in public protocol 'UICollectionViewDataSource'
```

**原因**：`public` 类实现 `public` 协议，方法访问级别必须 ≥ `public`，但 `extension` 默认是 `internal`。

---

**另一常见报错**（同文件内独立 `UICollectionViewCell` 子类 + `configure(item:)`）：

```
Method must be declared fileprivate because its parameter uses a private type
```

**原因**：数据模型写成 `private struct FooItem`，而 Cell 的 `func configure(item: FooItem)` 默认为 **internal**。方法的可见性不能高于签名中出现的类型——`private` 类型只能出现在 `private` / `fileprivate` 成员签名里。

**处置（二选一，推荐前者）**：

| 方案 | 写法 |
|---|---|
| **A（推荐）** | 模型改为 **internal**：`struct FooItem { ... }`（去掉 `private`）。同文件 VC + Cell 共用，仍为模块内封装，不污染其他文件除非 `public`。 |
| **B** | 保留 `private struct`，则 Cell 上写 **`fileprivate func configure(item: FooItem)`**（或把整个 Cell 标 `fileprivate final class`）。 |

**生成约定**：凡是「VC 私有数组元素类型」又要传给「同文件 Cell.configure」的 Model，**不要用 `private struct`**，直接用 **internal struct**（或 **fileprivate struct**，与 Cell 方法同级）。

#### 生成前必做：探测宿主基类访问级别

```bash
# 在 Agent 生成代码前先扫一次（基类名 = host.bases.*）
rg -n "^(public |open |@objc public |@objc open )?class\s+<BaseClassName>\b" <host_project_root>
rg -n "^@interface\s+<BaseClassName>\b" <host_project_root>
```

#### 模板选择表

> 下表中的 `XxxVC` / `XxxCell` 都是占位符，**实际类名必须以业务前缀 `<P>` 开头**（见 host.json / PROJECT_BINDING §0）。例：`AppCategoryListVC` / `AppCategoryCell`。

| 探测结果 | 类声明 | 协议 extension |
|---|---|---|
| `open class <VC_BASE>` | `open class <P>XxxVC: <VC_BASE>` | `extension <P>XxxVC: ... { open func ... }` |
| `public class <VC_BASE>` | `public class <P>XxxVC: <VC_BASE>` | **`public extension <P>XxxVC: ... { ... }`** |
| `class <VC_BASE>`（internal）| `class <P>XxxVC: <VC_BASE>` | `extension <P>XxxVC: ... { ... }` |
| OC `@interface <VC_BASE>` | `class <P>XxxVC: <VC_BASE>` | `extension <P>XxxVC: ... { ... }` |
| 探测失败 | `class <P>XxxVC: <VC_BASE>`（保守 internal）| `extension <P>XxxVC: ... { ... }` |

#### 推荐模板（90% 场景：基类是 internal 或 OC）

```swift
class AppCategoryListViewController: UIViewController {
    private var categoryRows: [CategoryRow] = []
}

// MARK: - UICollectionViewDataSource
extension AppCategoryListViewController: UICollectionViewDataSource {
    func collectionView(_ collectionView: UICollectionView,
                        numberOfItemsInSection section: Int) -> Int {
        return categoryRows.count
    }

    func collectionView(_ collectionView: UICollectionView,
                        cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(
            withReuseIdentifier: AppCategoryCell.reuseId,
            for: indexPath
        ) as! AppCategoryCell
        cell.configure(categoryRows[indexPath.item])
        return cell
    }
}
```

#### 仅当基类是 public 时才用此模板

```swift
public class AppCategoryListViewController: UIViewController {
    public private(set) var categoryRows: [CategoryRow] = []
}

// MARK: - UICollectionViewDataSource —— 整个 extension 加 public
public extension AppCategoryListViewController {
    func collectionView(_ collectionView: UICollectionView,
                        numberOfItemsInSection section: Int) -> Int { ... }
}
```

> 注：把协议一致性写在主类定义里（`class XxxVC: <VC_BASE>, UICollectionViewDataSource`），extension 仅放方法，写 `public extension XxxVC { ... }` 最简洁，不用重复一致性声明。

---

## 使用场景

当 `figma-ios-listview-recognition` 返回识别结果后，调用本 SKILL 生成代码。

**输入**：
- 识别结果 dict（来自 `figma-ios-listview-recognition`）
- 数据包 `design.json` + `comments.json` + `assets/ios/manifest.json` + `manifest.json`（含 `mock.default_image_url`）
- **优先读列表容器上的预算字段**（阶段 1 已写好，勿重算）：
  - `design.json[list_node]._role.is_list_container`
  - `design.json[list_node]._layout_hint.list` → `{ scroll_axis, cell_template_node_id, cell_count }`
  - `index.json.by_role.list_container` / `audit.json.list_containers`

**输出**：
- Swift 阶段 2 基础 UI 代码（完整 UICollectionView 实现 + 临时模型 + Mock 数据 + `// TODO(阶段3)` 锚点）

---

## 步骤 0：从 `_layout_hint.list` 定模板与滚动轴

```text
hint = design.json[list_node_id]._layout_hint.list
cell_root = nodes[hint.cell_template_node_id]   # Cell 结构分析的根
scroll_axis = hint.scroll_axis                  # "horizontal" | "vertical"
cell_count = hint.cell_count                    # Mock 条数上限参考
```

若 `_layout_hint.list` 缺失，再 fallback 到 listview-recognition 的识别结果 dict。

## 步骤 1：分析 Cell 结构

### 目标

分析 Cell 的所有子节点，识别其结构、布局模式和所有元素。

### 执行指导

**分析内容**：
- 遍历 Cell 的**所有**子节点（包括深层嵌套节点）
- 识别所有节点类型（TEXT/IMAGE/FRAME/VECTOR/COMPONENT/等）
- 记录每个节点的：
  - 位置信息（x, y, width, height）
  - 样式信息（字号/颜色/填充等）
  - 语义信息（节点名称/评论标注）
- 识别布局模式（垂直/水平/网格/复杂布局）

**注意事项**：
- ⚠️ **不要限制遍历深度**：Cell 可能有多层嵌套，应遍历完整子树
- ⚠️ **不要只识别特定类型**：识别所有节点类型，包括容器节点（FRAME/GROUP）
- ⚠️ **识别特殊场景**：
  - Cell 中有输入框（TextField/TextArea）
  - Cell 中嵌套了列表（识别为嵌套 CollectionView）
  - Cell 有多个状态（从评论或节点名判断）

### 输出

一个内部分析结构（非代码产物），至少覆盖：所有子节点的 `node_id / type / name / 几何 / 样式`、整体 `layout_pattern`（vertical / horizontal / grid / complex）、`special_cases` 标记（has_input / has_nested_list / has_states 等）。用于驱动后续步骤。

---

## 步骤 2：推断/映射模型字段

### 目标

根据 Cell 结构和可用的模型信息，确定模型字段名和类型。

**⚠️  注意**：本步骤支持两种模式，根据输入决定使用哪种模式。

---

### 推断临时模型（阶段 2 唯一模式）

> 📌 阶段 2 只做**临时模型**（从 Figma 语义推断）。阶段 3 会把临时模型替换为接口文档对应的真实 API 模型——那不是本 skill 的职责。

**场景**：只有 Figma 设计稿，没有真实 API 模型（阶段 2 的默认状态）

**推断指导原则（优先级从高到低）**：

**1. 评论标注（最高优先级）**
- 如果评论中明确标注了字段名（如"字段：price"），直接使用
- 如果评论标注了"选中态"，生成 `isSelected: Bool`
- 如果评论标注了"状态：A/B/C"，生成 `enum State`

**2. 节点名称语义**
- 节点名包含"价格"/"price"/"金额"/"¥" → `price: String`
- 节点名包含"时间"/"time"/"日期"/"date" → `timestamp: String`
- 节点名包含"数量"/"count"/"点赞"/"评论" → `count: Int`
- 节点名包含"状态"/"status" → `status: String`
- 节点名包含"标签"/"tag" → `tags: [String]`
- 节点名包含"头像"/"avatar" → `avatar: String`
- 更多语义可自行推断...

**3. 样式特征辅助**
- 字号最大的 TEXT → `title: String`
- 字号第二大的 TEXT → `subtitle: String`
- 颜色特殊（红色/黄色） → `highlightText: String`（或根据语义命名）

**4. 位置关系辅助**
- 位于顶部的 TEXT → 可能是标题
- 位于底部的 TEXT → 可能是描述或时间
- 位于左侧的 IMAGE → 可能是头像或图标

**5. 兜底规则**
- 无法判断时，使用通用命名：`text1`, `text2`, `image1`, `image2` 等
- 或者根据节点名直接作为字段名（去除特殊字符）

### 字段类型指导

| 场景 | 字段类型 | 示例 |
|------|---------|------|
| TEXT 节点 | `String` | `let title: String` |
| IMAGE 节点 | `String` | `let icon: String` |
| 评论标注"选中态" | `Bool` | `var isSelected: Bool = false` |
| 节点名包含"数量"/"计数" | `Int` | `let count: Int` |
| 节点名包含"标签" | `[String]` | `let tags: [String]` |
| 评论标注"状态：A/B/C" | `enum` | `var state: State = .normal` |
| TextField 节点 | `String`（可编辑） | `var inputText: String` |

### 强制规则

- ✅ **必须**：第一个字段必须是 `id: String`（唯一标识）
- ✅ **必须**：所有字段都要有注释说明用途
- ⚠️ **建议**：字段名使用驼峰命名法，语义清晰

**输出格式（示例）**：

```swift
struct CategoryModel {
    let id: String              // 唯一标识
    let title: String           // 品类名称
    let icon: String            // 品类图标（本地 asset_name 或 http URL）
    var isSelected: Bool = false  // 选中态（有需求时才加）
}
```

---

### 关于阶段 3 的 API 模型映射（超出本 skill 范围）

阶段 3 拿到接口文档后会把临时模型替换为真实 API 模型（例如 `title` → `productName`、`icon` → `iconUrl`）。这一步由**阶段 3** 另行完成，本 skill **不生成** 基于 API 模型的代码，只生成临时模型 + mock 数据 + `// TODO(阶段3)` 锚点；阶段 3 沿着锚点 grep 后做替换。

---

## 步骤 3：生成 Mock 数据（阶段 2 强制）

### 目标

为模型生成合理的占位数据，让阶段 2 代码**开箱可跑、可预览**。阶段 3 会用接口文档替换这些 mock。

> 📌 阶段 2 **必须**生成 mock 数据——这是阶段 2 的定位（UI 能跑能看），不是"偷懒"。阶段 3 的任务之一就是把 mock 换成真实数据。

### 数据来源优先级

1. **优先级 1：提取实际子节点数据**
   - 如果父节点有多个实际子节点（非 SYMBOL），从这些节点提取数据

2. **优先级 2：根据字段语义生成占位数据**
   - 如果只有 SYMBOL 节点（内容未展开），根据字段名推断占位内容

3. **优先级 3：使用评论指定的数据**
   - 如果评论中指定了 Mock 数据，优先使用

4. **图片字段（任一情况）**：服务器下发图 → `manifest.json.mock.default_image_url` + `// TODO(阶段3): 接入业务接口`

### Mock 数据生成指导

**根据字段名推断占位内容**：

| 字段名关键词 | 占位数据示例 |
|------------|-------------|
| `price` / `价格` / `金额` | `"¥99.00"`, `"¥199.00"`, `"¥299.00"` |
| `time` / `时间` / `timestamp` | `"10:30"`, `"昨天"`, `"2026-01-01"` |
| `count` / `数量` / `点赞` | `"100"`, `"999+"`, `"1.2k"` |
| `status` / `状态` | `"待支付"`, `"已发货"`, `"已完成"` |
| `avatar` / `头像` | 走服务器下发图 → 统一用 `manifest.json.mock.default_image_url`（禁止写死 `img_avatar_1` 等假名） |
| `nickname` / `昵称` | `"张三"`, `"李四"`, `"王五"` |
| `title` / `标题` | 根据场景推断（品类/商品/订单等） |
| `icon` / `image` / `iconUrl` / `imageUrl` | 见下方"图片字段处理策略" |
| `tags` / `标签` | `["热门", "新品"]`, `["包邮", "促销"]` |

---

### 图片字段处理策略

**数据来源**（仅数据包，禁止再调 API）：

1. **本地切图（首选）**：`{data_dir}/assets/ios/manifest.json`
   - `manifest.items[node_id].asset_name` → `UIImage(named: ...)`
2. **服务器下发图片（含头像/封面/品类图等 INSTANCE 或 IMAGE fill）**：节点没在 `manifest.items` 里
   - **统一用** `{data_dir}/manifest.json` → `mock.default_image_url`，配 `sd_setImage` + TODO 注释
   - 详见 [figma-ios-image-assets-download](../figma-ios-image-assets-download/SKILL.md)「服务器下发图片场景」
   - ⛔ 禁止退化成 `image = nil` + 纯色占位
   - ⛔ 禁止编造 `img_avatar_1` / `img_game_pubg` / `img_placeholder_1` 等不存在的 asset 名

---

**生成 Mock 数据时的查找逻辑**：

```python
import json, os

def get_image_for_node(node_id: str, data_dir: str) -> str:
    # 1) 本地切图优先
    assets_manifest = os.path.join(data_dir, "assets/ios/manifest.json")
    if os.path.exists(assets_manifest):
        with open(assets_manifest) as f:
            items = json.load(f).get("items", {})
        if node_id in items:
            return items[node_id]["asset_name"]
    # 2) 没有切图 → 服务器下发图，统一用数据包的 mock URL（禁止编造 asset 名）
    with open(os.path.join(data_dir, "manifest.json")) as f:
        return json.load(f)["mock"]["default_image_url"]
```

---

**示例 1：服务器下发图片**（节点是 IMAGE 但本地无切图）

```swift
// 服务器图统一用数据包的 mock URL（manifest.json → mock.default_image_url）
// ⛔ 严禁写 Figma S3 URL（24h 失效）/ example.com 等假 URL
// 详见 figma-ios-image-assets-download skill「服务器下发图片场景」
CategoryModel(
    id: "1",
    title: "绝地求生",
    icon: "https://picsum.photos/200"  // TODO(阶段3): 接入业务接口后替换为真实图片 URL
)
```

**示例 2：本地切图**（节点已 export，imageset 已下到 `assets/ios/`）

```swift
// Mock 数据使用 Assets 名称
CategoryModel(
    id: "1", 
    title: "步骤分隔", 
    icon: "img_8b86f_bitmap_03"
)
```

**示例 3：无法识别来源时的兜底**

兜底**仍然用 mock URL**，禁止退化成编造的 asset 名：

```swift
CategoryModel(
    id: "1",
    title: "未知",
    icon: "https://picsum.photos/200" // TODO(阶段3): 接入业务接口后替换为真实图片 URL
)
```

**数据数量指导**：
- 有实际子节点：提取实际数量
- 有 SYMBOL：生成 5-10 条
- 默认：生成 3-5 条

**数据多样性**：
- 保持数据的多样性，不要所有项都一样
- 如果无法推断，使用 `字段名_序号`（如 `"title_1"`, `"title_2"`）

### 输出示例

```swift
// 服务器下发图字段统一用 manifest.json.mock.default_image_url
// ⛔ 禁止编造 img_game_pubg / img_product_1 这类不存在的 asset 名
private static let kMockImageURL = "https://picsum.photos/200"

private var categories: [CategoryModel] = [
    CategoryModel(id: "1", title: "绝地求生", icon: kMockImageURL, isSelected: false),
    CategoryModel(id: "2", title: "LOL",     icon: kMockImageURL, isSelected: false),
    CategoryModel(id: "3", title: "王者荣耀", icon: kMockImageURL, isSelected: false),
]
```

---

## 步骤 4：生成 CollectionView 代码

### 目标

生成 `UICollectionView` 的定义和 `DataSource` 实现。

### 代码生成指导

**CollectionView 配置**：
- 根据识别结果设置 `scrollDirection`（horizontal/vertical）
- 根据识别结果设置 `isScrollEnabled`（true/false）
- 设置 `itemSize` 或使用 `estimatedItemSize`（自动计算）
- 设置间距（`minimumLineSpacing`/`minimumInteritemSpacing`）

**Layout 选择**：
- 标准列表：`UICollectionViewFlowLayout`
- 标签集合（左对齐换行）：`LeftAlignedFlowLayout`（见后文）
- 复杂布局：可自定义 Layout

**DataSource 实现**：
- `numberOfItemsInSection` → 返回数据数组的 count
- `cellForItemAt` → dequeue Cell 并调用 `configure(item:)`

### 必须遵守

- ✅ 使用 `lazy var` 定义 CollectionView
- ✅ 必须实现 `UICollectionViewDataSource`
- ✅ 注释标注 Figma 节点 ID 和名称
- ✅ 如果页面有多个 CollectionView，使用 `if collectionView == xxx` 区分

---

## 步骤 5：生成 Cell 代码

### 目标

生成 `UICollectionViewCell` 子类，包括子视图定义、布局和 `configure(item:)` 方法。

### 代码生成指导

**子视图定义**：
- 根据 Cell 结构生成对应的子视图（UILabel/UIImageView/UIButton/等）
- 使用闭包初始化子视图，设置默认属性

**布局约束**：
- **必须使用相对约束**（按 host.layout_engine）
- **优先相对布局**（而不是绝对坐标）
- 根据布局模式选择：
  - 简单布局：直接用相对约束
  - 复杂布局：可以使用 UIStackView 辅助
  - 嵌套列表：生成嵌套的 UICollectionView

**configure(item:) 方法**：
- 将模型字段映射到子视图属性
- TEXT 字段 → `label.text = item.xxx`
- IMAGE 字段 → `imageView.image = UIImage(named: item.xxx)`
- Bool 字段 → 更新外观（背景色/边框/透明度等）

### 必须遵守

- ✅ 使用 `private class` 定义 Cell
- ✅ 颜色/字体走 bindings map
- ✅ 布局用相对约束（按 host.layout_engine）
- ✅ 必须实现 `configure(item:)` 方法

### 图片加载处理

**根据图片来源自动选择加载方式**：

```swift
// 需要导入图片库
// 远程图按 host.image_load_template，勿写死宿主图片库 import

func configure(item: CategoryModel) {
    titleLabel.text = item.title
    
    // 自动判断图片来源
    if item.icon.hasPrefix("http") {
        // 在线图片 - 按 host.image_load_template
        iconImageView.sd_setImage(with: URL(string: item.icon), placeholderImage: UIImage(named: "img_placeholder"))
    } else {
        // 本地图片 - 直接加载
        iconImageView.image = UIImage(named: item.icon)
    }
    
    // 根据选中状态更新外观（如果有）
    contentView.alpha = item.isSelected ? 1.0 : 0.6
}
```

**注意**：
- 远程图按 `host.image_load_template`（默认可用 `sd_setImage`）；**不要**写死宿主图片库类名
- 服务器下发图片**统一用** `{data_dir}/manifest.json` 的 `mock.default_image_url`
- ⛔ **严禁** 在 Mock 数据中直接写 `https://figma-alpha-api.s3.*` 临时 URL（24h 失效）
- ⛔ **严禁** 写 `example.com` / `placeholder.com` 等假 URL（运行时只能看到失败占位）

**数据来源说明**：
- **本地切图**（节点 `_role.is_export_asset = true`）：从 `{data_dir}/assets/ios/manifest.json` 读取 `asset_name`，`UIImage(named:)` 引用
- **服务器下发图片**（节点 fills 含 IMAGE 但未 export）：从 `{data_dir}/manifest.json` 读取 `mock.default_image_url`，所有此类字段统一用同一个 URL + TODO 注释
- 详细规范见 [figma-ios-image-assets-download](../figma-ios-image-assets-download/SKILL.md)「服务器下发图片场景」

---

## 步骤 6：生成交互代码

### 目标

生成 `UICollectionViewDelegate` 的 `didSelectItemAt` 实现。

### 交互逻辑规则

**有 `isSelected` 字段**：
```swift
func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    // 1. 更新选中状态
    categories[indexPath.item].isSelected.toggle()
    
    // 2. 刷新 Cell
    collectionView.reloadItems(at: [indexPath])
    
    // 3. 打印日志（可选）
    print("选中: \(categories[indexPath.item].title)")
}
```

**无 `isSelected` 字段**：
```swift
func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    // 打印日志
    let item = categories[indexPath.item]
    print("点击了: \(item.title)")
}
```

### 必须遵守

- ✅ 必须实现 `UICollectionViewDelegate`
- ✅ 如果页面有多个 CollectionView，使用 `if collectionView == xxx` 区分
- ✅ 有选中态 → 必须 toggle + reload
- ✅ 无选中态 → 打印日志或留空（由业务实现）

---

## LeftAlignedFlowLayout（标签集合专用）

当识别结果 `layoutType == 'LeftAlignedFlow'` 时，生成此布局类：

```swift
// MARK: - LeftAlignedFlowLayout
/// 左对齐流式布局，用于标签集合、可换行列表等场景
private class LeftAlignedFlowLayout: UICollectionViewFlowLayout {
    override func layoutAttributesForElements(in rect: CGRect) -> [UICollectionViewLayoutAttributes]? {
        guard let attributes = super.layoutAttributesForElements(in: rect) else { return nil }
        
        var leftMargin: CGFloat = sectionInset.left
        var maxY: CGFloat = -1.0
        
        let modifiedAttributes = attributes.map { $0.copy() as! UICollectionViewLayoutAttributes }
        
        for attribute in modifiedAttributes {
            if attribute.frame.origin.y >= maxY {
                leftMargin = sectionInset.left
            }
            attribute.frame.origin.x = leftMargin
            leftMargin += attribute.frame.width + minimumInteritemSpacing
            maxY = max(attribute.frame.maxY, maxY)
        }
        
        return modifiedAttributes
    }
}
```

---

## 常见场景处理

每个场景给出识别信号 + 必须遵守的实现规则，代码细节由 LLM 按场景展开。

### 场景 1：Cell 中有输入框

- **识别**：节点类型为 `INPUT`，或节点名含 `输入` / `input`
- **规则**：生成 `UITextField`（字体/色走 bindings map），**`configure(item:)` 里不要赋 `text`**（保持可编辑状态），`placeholder` 用 Figma 原文

### 场景 2：Cell 中嵌套 CollectionView

- **识别**：Cell 内部又命中 `list_container` / `chip_group_hits`
- **规则**：在 Cell 内 lazy 一个子 `UICollectionView` + **单独**实现 `UICollectionViewDataSource`（extension 挂在 Cell 类上）；标签集合用 `LeftAlignedFlowLayout`

### 场景 3：Cell 有多种状态

- **识别**：评论标注「状态：A/B/C」或节点名含 `状态` / `state`
- **规则**：定义 `enum State`，模型里 `var state: State`，`configure` 内 `switch item.state` 更新外观；**禁止**用多个 Bool 模拟互斥状态

### 场景 4：Cell 元素 ≥5 或布局不规则

- **规则**：用 `UIStackView` 组合行（axis + spacing），或拆多个 `UIView` 容器再 SnapKit 嵌套；**不要**在 `contentView` 里平铺 10+ 个 subview 用绝对约束

### 场景 5：Cell 动态高度

- **识别**：TEXT 节点行数/长度不固定
- **规则**：layout 设 `estimatedItemSize = .automaticSize`；Cell 重写 `preferredLayoutAttributesFitting` 用 `systemLayoutSizeFitting(targetSize, horizontal: .required, vertical: .fittingSizeLevel)` 计算真实高度；**禁止**与 `sizeForItemAt` 共用（见「常见错误」）

---

## 常见错误

> 「字符串数组」「硬编码数据」「编造 asset 名」已在 QUICK_REF 强制约束里列出，此处只列非直觉错误。

### ❌ 同时使用 estimatedItemSize 和 sizeForItemAt

两者冲突，**必须二选一**：

- 自适应高度 → 只用 `layout.estimatedItemSize = UICollectionViewFlowLayout.automaticSize`，**不要**实现 `sizeForItemAt`
- 固定/手算高度 → 只用 `sizeForItemAt`，**不要**设 `estimatedItemSize`

---

## 与其他 Skill 的协作

```
figma-ios-listview-recognition   → 识别结果（list_container / chip_group_hits / layoutType）
        ↓
     本 SKILL                 → Swift 基础 UI 代码（UI + 临时模型 + Mock + // TODO(阶段3)）
        ↓
figma-ios-snapkit-layout      → 约束
figma-ios-rxswift-interaction-pattern   → 交互骨架（可选）
        ↓
    阶段 3（不在本 skill）     → 结合 PRD + 接口文档替换 mock、接入真实 API
```

**临时模型 + Mock 数据**是本 skill 的**标准产物**，不要因为"不够生产级"就跳过或降级为编造 asset 名。

---

<!-- QUICK_REF 已是总结，不再冗余重复。 -->
