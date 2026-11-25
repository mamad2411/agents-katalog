---
name: figma-ios-selection-interaction
description: >-
  从 Figma 节点自动识别选择交互模式（单选/多选/Toggle），生成选中态变化逻辑（更新数据模型 + 刷新 UI），
  集成 RxSwift 交互模式。Use when generating selection interaction code, or when user mentions 
  选中态交互、单选、多选、didSelectItem、Toggle。
---

# Figma 选择交互逻辑生成

## 职责范围

- ✅ 从 `figma-ios-preload-data` 数据包（`design.json`）自动识别选择交互模式（单选/多选/Toggle）
- ✅ 生成选中态变化逻辑（更新数据模型、刷新 UI）
- ✅ 生成 `didSelectItemAt`（列表统一 UICollectionView；**不用** `UITableView` / `didSelectRowAt`）
- ✅ 生成单个按钮 Toggle 逻辑
- ✅ 集成 RxSwift 交互模式（按 `host.interaction`；默认也可 target-action，见 rxswift skill）
- ✅ 保持数据模型与 UI 同步
- ❌ 不处理业务逻辑（网络请求、页面跳转等，留 TODO 注释）
- ❌ 不处理动画效果（由其他 Skill 负责）
- ❌ **不**从 Figma MCP / REST 再拉数据；视觉差异读 `design.json`（或已由 `figma-ios-component-state-recognition` 提取的状态）
- ❌ **不**替代 `figma-ios-component-state-recognition`（外观 / `updateAppearance`）与 `figma-ios-uicollectionview-codegen`（CV 骨架）

---

## 适用场景

| 场景 | Figma 特征 | 生成代码 |
|------|-----------|---------|
| **ListView 单选** | 多个同类节点，只有 1 个选中 | `didSelectItemAt` + 单选互斥逻辑 |
| **ListView 多选** | 多个同类节点，多个选中 | `didSelectItemAt` + Toggle 逻辑 |
| **单个按钮 Toggle** | 单个节点有选中态 | RxSwift tap + Toggle 逻辑 |
| **SegmentedControl** | 多个并列按钮，1 个选中 | 按钮组 + 单选互斥逻辑 |

---

## 识别规则

### 规则 1：ListView 单选模式

**触发条件（必须全部满足）：**

```python
def is_single_selection_listview(figma_nodes):
    """
    判断是否为单选 ListView
    """
    # 1. 节点数量 ≥ 2
    if len(figma_nodes) < 2:
        return False
    
    # 2. 有选中态视觉差异（读 design.json 的 fills/strokes/font，见 component-state-recognition）
    if not has_selection_state(figma_nodes):
        return False
    
    # 3. 只有 1 个节点处于选中态
    selected_count = count_selected_nodes(figma_nodes)
    if selected_count != 1:
        return False
    
    # 4. 是 ListView（本仓统一 UICollectionView；见 listview-recognition）
    if not is_listview(figma_nodes):
        return False
    
    return True
```

**识别结果：**
```python
{
    'interaction_mode': 'single_selection',
    'default_index': 0,  # 默认选中第一个（"绝地求生"）
    'ui_component': 'UICollectionView',
    'refresh_mode': 'reload_all'  # 刷新所有 Cell
}
```

---

### 规则 2：ListView 多选模式

**触发条件（必须全部满足）：**

```python
def is_multiple_selection_listview(figma_nodes):
    """
    判断是否为多选 ListView
    """
    # 1. 节点数量 ≥ 2
    if len(figma_nodes) < 2:
        return False
    
    # 2. 有选中态视觉差异
    if not has_selection_state(figma_nodes):
        return False
    
    # 3. 多个节点处于选中态（≥ 2）
    selected_count = count_selected_nodes(figma_nodes)
    if selected_count < 2:
        return False
    
    # 4. 是 ListView
    if not is_listview(figma_nodes):
        return False
    
    return True
```

**识别结果：**
```python
{
    'interaction_mode': 'multiple_selection',
    'default_indexes': [0, 2],  # 默认选中多个
    'ui_component': 'UICollectionView',
    'refresh_mode': 'reload_single'  # 只刷新点击的 Cell
}
```

---

### 规则 3：单个按钮 Toggle 模式

**触发条件（必须全部满足）：**

```python
def is_toggle_button(figma_node):
    """
    判断是否为 Toggle 按钮
    """
    # 1. 单个节点（非列表）
    if is_part_of_list(figma_node):
        return False
    
    # 2. 有选中态视觉差异
    if not has_selection_state(figma_node):
        return False
    
    # 3. 节点名称包含 Toggle 关键词
    toggle_keywords = ['like', 'favorite', 'follow', 'bookmark', 'toggle', '喜欢', '收藏', '关注']
    name = figma_node['name'].lower()
    if any(kw in name for kw in toggle_keywords):
        return True
    
    # 4. 或者是独立的按钮（不在列表中）
    return True
```

**识别结果：**
```python
{
    'interaction_mode': 'toggle',
    'default_state': False,  # 默认未选中
    'ui_component': 'UIButton / UIControl'
}
```

---

## 代码生成模板

### 模板 1：ListView 单选模式（UICollectionView）

**数据模型（由 `figma-ios-listview-recognition` 生成）：**
```swift
struct CategoryItem {
    let id: String
    let title: String
    var isSelected: Bool  // ← 选中态字段
}

private var categories: [CategoryItem] = [
    CategoryItem(id: "1", title: "绝地求生", isSelected: true),   // ← 默认选中
    CategoryItem(id: "2", title: "LOL", isSelected: false),
    CategoryItem(id: "3", title: "三角洲行动", isSelected: false),
    CategoryItem(id: "4", title: "无畏契约", isSelected: false),
    CategoryItem(id: "5", title: "更多", isSelected: false)
]
```

**生成交互逻辑：**
```swift
// MARK: - UICollectionViewDelegate

extension CategoryScrollCell: UICollectionViewDelegate {
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        // ========== 单选模式：取消所有选中，只选中当前项 ==========
        
        // 1. 取消所有选中
        for i in 0..<categories.count {
            categories[i].isSelected = false
        }
        
        // 2. 选中当前项
        categories[indexPath.item].isSelected = true
        
        // 3. 刷新所有 Cell（视觉反馈）
        collectionView.reloadData()
        
        // TODO(阶段3): 结合 PRD + 接口文档补业务逻辑（网络请求 / 页面跳转 / 数据联动等）
        // 示例：
        // - 网络请求：根据选中品类加载数据
        // - 页面跳转：跳转到详情页
        // - 数据联动：影响其他 UI 组件
        print("选中品类: \(categories[indexPath.item].title)")
    }
}
```

**关键点：**
- ✅ 先取消所有选中（单选互斥）
- ✅ 再选中当前项
- ✅ 刷新所有 Cell（确保视觉一致）
- ✅ 留 TODO 注释提示业务逻辑

---

### 模板 2：ListView 多选模式（UICollectionView）

**数据模型：**
```swift
struct TagItem {
    let id: String
    let title: String
    var isSelected: Bool
}

private var tagItems: [TagItem] = [
    TagItem(id: "1", title: "排位赛", isSelected: true),   // ← 默认选中
    TagItem(id: "2", title: "声音好听", isSelected: true), // ← 默认选中
    TagItem(id: "3", title: "娱乐赛", isSelected: false),
    TagItem(id: "4", title: "QQ区", isSelected: false),
    TagItem(id: "5", title: "微信区", isSelected: false)
]
```

**生成交互逻辑：**
```swift
// MARK: - UICollectionViewDelegate

extension RemarkInputView: UICollectionViewDelegate {
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        // ========== 多选模式：Toggle 当前项 ==========
        
        // 1. Toggle 当前项选中态
        tagItems[indexPath.item].isSelected.toggle()
        
        // 2. 只刷新点击的 Cell（性能优化）
        collectionView.reloadItems(at: [indexPath])
        
        // TODO(阶段3): 结合 PRD + 接口文档补业务逻辑（网络请求 / 页面跳转 / 数据联动等）
        // 示例：
        // - 实时统计：已选中标签数量
        // - 数据验证：是否至少选中一个
        // - 网络同步：同步到服务器
        let selectedTags = tagItems.filter { $0.isSelected }.map { $0.title }
        print("已选中标签: \(selectedTags)")
    }
}
```

**关键点：**
- ✅ 直接 Toggle 当前项（多选模式）
- ✅ 只刷新单个 Cell（性能优化）
- ✅ 支持全部取消选中（业务逻辑可控制）

---

### 模板 3：ListView 单选模式（UICollectionView，性别等短列表）

> 本仓列表**一律** UICollectionView。短选项（性别 / 筛选项）也用 CV，不要生成 `UITableView`。

**数据模型：**
```swift
struct GenderItem {
    let id: String
    let title: String
    var isSelected: Bool
}

private var genders: [GenderItem] = [
    GenderItem(id: "1", title: "不限", isSelected: true),
    GenderItem(id: "2", title: "男生", isSelected: false),
    GenderItem(id: "3", title: "女生", isSelected: false)
]
```

**生成交互逻辑：**
```swift
// MARK: - UICollectionViewDelegate

extension GenderSelectionCell: UICollectionViewDelegate {
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        // ========== 单选模式：取消所有选中，只选中当前项 ==========
        
        for i in 0..<genders.count {
            genders[i].isSelected = false
        }
        genders[indexPath.item].isSelected = true
        collectionView.reloadData()
        
        // TODO(阶段3): 结合 PRD + 接口文档补业务逻辑（网络请求 / 页面跳转 / 数据联动等）
        print("选中性别: \(genders[indexPath.item].title)")
    }
}
```

---

### 模板 4：单个按钮 Toggle 模式

**数据模型（在 View/Cell 中）：**
```swift
private var isSelected: Bool = false {
    didSet {
        updateAppearance()  // 状态变化时自动更新外观
    }
}
```

**生成交互逻辑（RxSwift 模式）：**
```swift
private let disposeBag = DisposeBag()

private func setupBindings() {
    // Toggle 按钮点击事件
    likeButton.rx.tap
        .subscribe(onNext: { [weak self] in
            guard let self = self else { return }
            
            // Toggle 选中态
            self.isSelected.toggle()
            
            // TODO(阶段3): 结合 PRD + 接口文档补业务逻辑（网络请求 / 页面跳转 / 数据联动等）
            // 示例：
            // - 网络请求：同步到服务器
            // - 本地存储：保存喜欢状态
            // - 动画效果：播放点赞动画
            if self.isSelected {
                print("已喜欢")
                // self.sendLikeRequest()
            } else {
                print("取消喜欢")
                // self.sendUnlikeRequest()
            }
        })
        .disposed(by: disposeBag)
}
```

**生成交互逻辑（传统 target-action 模式，不推荐）：**
```swift
private var isSelected: Bool = false {
    didSet {
        updateAppearance()
    }
}

override init(frame: CGRect) {
    super.init(frame: frame)
    setupUI()
    
    // 添加点击事件
    likeButton.addTarget(self, action: #selector(handleLikeButtonTapped), for: .touchUpInside)
}

@objc private func handleLikeButtonTapped() {
    // Toggle 选中态
    isSelected.toggle()
    
    // TODO(阶段3): 结合 PRD + 接口文档补业务逻辑（网络请求 / 页面跳转 / 数据联动等）
    print(isSelected ? "已喜欢" : "取消喜欢")
}
```

---

### 模板 5：SegmentedControl 单选模式（按钮组）

**数据模型：**
```swift
private var currentSelectedIndex: Int = 0 {
    didSet {
        updateAllButtonAppearance()
    }
}
```

**生成交互逻辑：**
```swift
private func setupBindings() {
    // 为每个按钮绑定点击事件
    for (index, button) in buttons.enumerated() {
        button.rx.tap
            .subscribe(onNext: { [weak self] in
                guard let self = self else { return }
                
                // 单选模式：更新选中索引
                self.currentSelectedIndex = index
                
                // TODO(阶段3): 结合 PRD + 接口文档补业务逻辑（网络请求 / 页面跳转 / 数据联动等）
                print("选中第 \(index) 个按钮")
            })
            .disposed(by: disposeBag)
    }
}

private func updateAllButtonAppearance() {
    for (index, button) in buttons.enumerated() {
        let isSelected = (index == currentSelectedIndex)
        button.updateAppearance(isSelected: isSelected)
    }
}
```

---

## 识别流程（完整）

### Step 1：检查是否有选中态

```python
def has_selection_state(nodes):
    """
    从 design.json 节点对比 fills / strokes / font，判断是否存在选中/未选中视觉差。
    优先复用 figma-ios-component-state-recognition 的结论，不要再调 MCP / REST。
    """
    if len(nodes) < 2:
        return False
    # 对比同类节点的 fills[].color、strokes[].color、font.weight（rgba 已含 alpha）
    signatures = [
        (
            tuple((f.get("color"), f.get("type")) for f in (n.get("fills") or [])),
            tuple((s.get("color"), s.get("type")) for s in (n.get("strokes") or [])),
            (n.get("font") or {}).get("weight"),
        )
        for n in nodes
    ]
    return len(set(signatures)) > 1
```

---

### Step 2：统计选中节点数量

```python
def count_selected_nodes(figma_nodes):
    """统计有多少个节点处于选中态（读 design.json）。"""
    return sum(1 for node in figma_nodes if is_node_selected(node, peers=figma_nodes))

def is_node_selected(node, peers=None):
    """
    判断单个节点是否更像「选中态」。读 design.json，不读 Tailwind / MCP。
    启发式（可与 component-state-recognition 对齐）：
    - fills/strokes 的 rgba alpha 更高、或颜色与同伴不同
    - font.weight 更粗（如 ≥500）
    - 名称含 选中/selected/active
    """
    name = (node.get("name") or "").lower()
    if any(k in name for k in ("选中", "selected", "active")):
        return True
    font = node.get("font") or {}
    if (font.get("weight") or 0) >= 500 and peers:
        weights = [(p.get("font") or {}).get("weight") or 400 for p in peers]
        if font.get("weight") == max(weights) and len(set(weights)) > 1:
            return True
    fills = node.get("fills") or []
    for f in fills:
        color = f.get("color") or ""
        # alpha 段：rgba(r,g,b,a) 中 a 明显大于同伴常见「淡选中底」
        if "rgba(" in color and color.rstrip(")").split(",")[-1].strip() not in ("0", "0.0", "1", "1.0"):
            # 有半透明主题底时倾向选中；精确对比交给 peers 差分
            if peers and has_selection_state(peers):
                return True
    return False
```

> 具体主题色以当前稿 `fills[].color` 为准，**不要**写死某业务色值；上表只示意差分思路。

---

### Step 3：判断交互模式

```python
def detect_interaction_mode(figma_nodes):
    """
    综合判断交互模式
    """
    # 1. 检查是否有选中态
    if not has_selection_state(figma_nodes):
        return None
    
    # 2. 统计选中节点数量
    selected_count = count_selected_nodes(figma_nodes)
    
    # 3. 判断是否为列表
    is_list = is_listview(figma_nodes)
    
    # 4. 返回交互模式
    if is_list:
        if selected_count == 1:
            return 'single_selection'  # ListView 单选
        elif selected_count >= 2:
            return 'multiple_selection'  # ListView 多选
        else:
            return None  # 没有默认选中（需要手动处理）
    
    else:
        # 单个节点
        if len(figma_nodes) == 1:
            return 'toggle'  # 单个按钮 Toggle
    
    return None
```

---

## 与其他 Skills 的协作

```
[1] figma-ios-component-state-recognition
    ↓ 识别选中/未选中视觉特征 → updateAppearance() + isSelected 模型字段

[2] figma-ios-listview-recognition
    ↓ 判定 UICollectionView（禁 UITableView）→ audit / _layout_hint.list

[2b] figma-ios-uicollectionview-codegen（list 命中后必须加载）
    ↓ CV / Cell / DataSource 骨架 + Mock

[3] figma-ios-selection-interaction（本 Skill）
    ↓ 单选/多选/Toggle → didSelectItemAt / toggle 逻辑（不写 TableView）

[4] figma-ios-rxswift-interaction-pattern
    ↓ 按 host.interaction 绑点击（按钮 Toggle 等）
```

**生成顺序：**
1. `figma-ios-component-state-recognition` → 数据模型（含 `isSelected`）+ `updateAppearance`
2. `figma-ios-listview-recognition` → 是否列表
3. **`figma-ios-uicollectionview-codegen`** → CV 骨架（识别为列表时**必做**）
4. **`figma-ios-selection-interaction`（本 Skill）** → Delegate 交互
5. `figma-ios-rxswift-interaction-pattern` → 非列表按钮的点击绑定

---

## 常见错误与避坑指南

### ❌ 错误 1：忘记取消旧选中（单选模式）

**问题：**
```swift
func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    // ❌ 错误：直接选中新项，旧项仍然是选中态
    items[indexPath.item].isSelected = true
    collectionView.reloadData()
}
```

**结果：** 多个 Cell 同时选中（违反单选逻辑）

**修复：**
```swift
func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    // ✅ 正确：先取消所有，再选中当前
    for i in 0..<items.count {
        items[i].isSelected = false
    }
    items[indexPath.item].isSelected = true
    collectionView.reloadData()
}
```

---

### ❌ 错误 2：忘记刷新 UI

**问题：**
```swift
func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    items[indexPath.item].isSelected.toggle()
    // ❌ 错误：没有刷新 UI，数据变了但界面没变
}
```

**结果：** 选中态变化了，但 UI 没有更新

**修复：**
```swift
func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    items[indexPath.item].isSelected.toggle()
    // ✅ 正确：刷新 UI
    collectionView.reloadItems(at: [indexPath])
}
```

---

### ❌ 错误 3：单选模式刷新单个 Cell

**问题：**
```swift
func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    for i in 0..<items.count {
        items[i].isSelected = false
    }
    items[indexPath.item].isSelected = true
    
    // ❌ 错误：只刷新当前 Cell，旧选中的 Cell 仍显示选中态
    collectionView.reloadItems(at: [indexPath])
}
```

**结果：** 新旧两个 Cell 都显示选中态

**修复：**
```swift
func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    for i in 0..<items.count {
        items[i].isSelected = false
    }
    items[indexPath.item].isSelected = true
    
    // ✅ 正确：刷新所有 Cell（或记录旧索引，刷新新旧两个）
    collectionView.reloadData()
}
```

**性能优化版本：**
```swift
private var previousSelectedIndex: Int = 0

func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    // 取消旧选中
    items[previousSelectedIndex].isSelected = false
    
    // 选中新项
    items[indexPath.item].isSelected = true
    
    // 只刷新新旧两个 Cell
    collectionView.reloadItems(at: [
        IndexPath(item: previousSelectedIndex, section: 0),
        indexPath
    ])
    
    // 更新记录
    previousSelectedIndex = indexPath.item
}
```

---

### ❌ 错误 4：didSet 与手动调用 updateAppearance 冲突

**问题：**
```swift
private var isSelected: Bool = false {
    didSet {
        updateAppearance()  // didSet 会自动调用
    }
}

func configure(isSelected: Bool) {
    self.isSelected = isSelected
    updateAppearance()  // ❌ 重复调用
}
```

**结果：** `updateAppearance()` 被调用两次

**修复：**
```swift
// 方案 A：只在 didSet 中调用
private var isSelected: Bool = false {
    didSet {
        updateAppearance()
    }
}

func configure(isSelected: Bool) {
    self.isSelected = isSelected  // ✅ 自动触发 didSet
}
```

**或者：**
```swift
// 方案 B：不用 didSet，手动调用
private var isSelected: Bool = false

func configure(isSelected: Bool) {
    self.isSelected = isSelected
    updateAppearance()  // ✅ 手动调用
}
```

---

### ❌ 错误 5：多选模式下不允许全部取消

**问题：**
```swift
func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    items[indexPath.item].isSelected.toggle()
    
    // ❌ 业务需求：至少选中一个，但没有验证
    collectionView.reloadItems(at: [indexPath])
}
```

**结果：** 用户可以取消所有选中，违反业务规则

**修复：**
```swift
func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    let currentItem = items[indexPath.item]
    
    // 如果当前是选中态，且是唯一选中项，不允许取消
    if currentItem.isSelected {
        let selectedCount = items.filter { $0.isSelected }.count
        if selectedCount == 1 {
            // TODO(阶段3): 结合 PRD 决定交互（Toast 提示 / 禁用按钮 / 忽略）
            print("至少需要选中一个标签")
            return
        }
    }
    
    // Toggle 选中态
    items[indexPath.item].isSelected.toggle()
    collectionView.reloadItems(at: [indexPath])
}
```

---

## 自动化检查清单

生成代码后，必须验证：

```
✅ 数据模型包含 isSelected 字段
✅ 默认选中项正确初始化（isSelected = true）
✅ 单选模式：点击时先取消所有，再选中当前
✅ 多选模式：点击时 Toggle 当前项
✅ UI 刷新逻辑正确（reloadData / reloadItems）
✅ RxSwift 使用 [weak self]（避免循环引用）
✅ 留 TODO 注释提示业务逻辑
✅ didSet 与手动调用不冲突
✅ 多选模式考虑业务约束（如至少选中一个）
```

---

## 代码生成规范

### 1. 注释规范

```swift
// ========== 单选模式：取消所有选中，只选中当前项 ==========
// 或
// ========== 多选模式：Toggle 当前项 ==========
// 或
// ========== Toggle 模式：切换选中态 ==========
```

### 2. TODO 注释规范

```swift
// TODO(阶段3): 结合 PRD + 接口文档补业务逻辑（网络请求 / 页面跳转 / 数据联动等）
// 示例：
// - 网络请求：根据选中品类加载数据
// - 页面跳转：跳转到详情页
// - 数据联动：影响其他 UI 组件
```

### 3. 调试输出规范

```swift
print("选中品类: \(categories[indexPath.item].title)")
// 或
let selectedTags = tagItems.filter { $0.isSelected }.map { $0.title }
print("已选中标签: \(selectedTags)")
```

---

## 相关 Skill

- **总入口**：[figma-ios-playbook](../figma-ios-playbook/SKILL.md)
- **状态识别**：[figma-ios-component-state-recognition](../figma-ios-component-state-recognition/SKILL.md)
- **ListView 识别**：[figma-ios-listview-recognition](../figma-ios-listview-recognition/SKILL.md)
- **交互事件**：[figma-ios-rxswift-interaction-pattern](../figma-ios-rxswift-interaction-pattern/SKILL.md)
- **标准组件**：[figma-ios-standard-components](../figma-ios-standard-components/SKILL.md)

---

**生成时间：** 2026-03-31  
**核心价值：** 自动生成选中态交互逻辑，减少重复代码，统一交互模式  
**适用范围：** 所有涉及选择交互的 UI 组件（ListView、按钮组、Toggle 按钮等）
