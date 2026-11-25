---
name: figma-ios-listview-recognition
description: >-
  识别 Figma 节点是否需要用 UICollectionView 实现。
  通过 3 个条件（节点名称/子节点相似度/SYMBOL）判定，
  返回识别结果供代码生成使用。
  Use when analyzing Figma nodes to determine if they should be 
  implemented as UICollectionView.
trigger: 分析 Figma 节点、判断列表场景
output: 识别结果 dict（component, direction, scrollEnabled, confidence）
---

# Figma ListView 识别与生成

## ⛔ 硬规则（红线，违反即视为交付失败）

> 这一节优先级**高于**下文所有"识别条件"。任何与本节冲突的判定，以本节为准。

### 红线 1：`audit.json.list_containers` / `index.json.by_role.list_container` 全部必须 UICollectionView

**两处来源等价**：
- `{data_dir}/audit.json` 的 `list_containers[]`（推荐，自带 must_use/forbidden 提示）
- `{data_dir}/index.json` 的 `by_role.list_container[]`

**强制规则**：
- 这两处列出的**每一个 node_id**，在生成代码里**必须**有对应的 `UICollectionView`（不是 UIScrollView，不是 UIStackView，不是手摆 UIView）
- 即使该节点的父节点 `export.is_export_asset == true`，**也禁止把父节点整组切图**——切图会吃掉列表，列表的语义子节点必须保留为 cell（详见 [`figma-ios-vector-vs-code` 红线规则](../figma-ios-vector-vs-code/SKILL.md)）
- 即使该节点 children 全是 IMAGE 节点，也仍然是列表 cell——cell 内容是图就用 `UIImageView` 当 cell 内容，不要把整个列表退化成 N 张 ImageView

**自检脚本**（生成完代码后必跑）：

```bash
data_dir=<data_dir>
out_file=<your_generated.swift>

python3 - <<PY
import json, sys
audit = json.load(open(f"$data_dir/audit.json"))
src_raw = open("$out_file").read()

# 剔除文件顶部连续的"节点树注释块"（常见形态：Figma 代码生成器会在文件开头 dump
# 一整棵树的 `// ├ 341:xxx  INSTANCE  ...`，如果不剔除，每个 node_id 的"第一次出现"
# 其实都在注释里，后续窗口扫描会串到其他节点的代码上造成误判）。
# 规则：从文件起始连续的 `空行` 或 `//` 开头行视为注释块，遇到第一个非注释非空行停止。
lines = src_raw.splitlines(keepends=True)
i = 0
while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith("//")):
    i += 1
src = "".join(lines[i:])
fail = []

# 1) list_containers：必须 UICollectionView（同构列表红线）
for it in audit.get("list_containers", []):
    nid = it["node_id"]
    if nid not in src:
        fail.append(f"❌ list_container {nid} '{it['name']}' 未在代码中出现（可能被父切图吃掉）")
        continue
    window = src.split(nid, 1)[1][:2000]
    if "UICollectionView" not in window and "CollectionView" not in window:
        fail.append(f"❌ list_container {nid} '{it['name']}' 没用 UICollectionView（scroll_axis={it['scroll_axis']}, cell_count={it['cell_count']}）")

# 2) list_keyword_hits（scroll_intent=True）：子节点异构仍要 UIScrollView，禁止降到 UIView
for it in audit.get("list_keyword_hits", []):
    if not it.get("scroll_intent"):
        continue  # 集合语义不检查
    nid = it["node_id"]
    if nid not in src:
        continue  # 节点可能属于 list_containers（已在 1 校验）
    window = src.split(nid, 1)[1][:2000]
    has_scroll = any(k in window for k in ("UICollectionView", "CollectionView", "UIScrollView", "ScrollView"))
    if not has_scroll:
        fail.append(
            f"❌ 滚动语义节点 {nid} '{it['name']}'（matched={it['matched_keyword']!r}）"
            f"没用 UICollectionView 或 UIScrollView，禁止降到 UIView"
        )

# 3) chip_group_hits（红线 2）：父异构 + 子段连续 ≥4 同构 INSTANCE/COMPONENT/FRAME，必 UICollectionView
#    注意：不能简单用 "cell_id 附近出现 UICollectionView" 判断。
#    同一文件里如果有其他 CV（例如 categoryCollectionView），cell_id 的位置会撞到那个 CV
#    导致假阴性。下面用两条判据：
#      (a) 反模式正则：[UIView]/[UIButton]/[UILabel]/[UIImageView] 数组声明后 1500 char 内
#          覆盖了 run 中过半 cell id → 典型的"chip 被做成 view 数组"事故（如 rankChipViews: [UIView]）
#      (b) 距离兜底：每个 cell id 距离任何 UICollectionView/Cell/register 声明 >600 char
#          → 大概率根本没用 UICollectionView 承载
import re
_chip_anti_array = re.compile(
    r"(?:lazy\s+var|var|let)\s+(\w+)\s*:\s*\[UI(?:View|Button|Label|ImageView)\]"
)
_chip_cv_sign = re.compile(
    r"UICollectionView(?:Cell|FlowLayout|DataSource|Delegate)?|register\s*\("
)
_cv_region_starts = [m.start() for m in _chip_cv_sign.finditer(src)]
for it in audit.get("chip_group_hits", []):
    run_ids = it.get("run_node_ids") or []
    present = [nid for nid in run_ids if nid in src]
    if not present:
        fail.append(
            f"❌ chip_group parent={it['parent_id']} '{it['parent_name']}' 的 "
            f"{it['run_length']} 个 cell 全部未在代码中出现（可能被整组切图吃掉）"
        )
        continue

    # 判据 (a)：反模式正则
    caught = False
    for m in _chip_anti_array.finditer(src):
        tail = src[m.end(): m.end()+1500]
        hits = [nid for nid in run_ids if nid in tail]
        if len(hits) >= max(2, len(run_ids)//2):
            fail.append(
                f"❌ chip_group {it['parent_id']} '{it['parent_name']}' 命中反模式 "
                f"`{m.group()}`（覆盖 {len(hits)}/{len(run_ids)} 个 cell）— "
                f"chip 群必须 UICollectionView + cell 承载，不能做成 view 数组"
            )
            caught = True
            break
    if caught:
        continue

    # 判据 (b)：距离兜底
    too_far = False
    for nid in present:
        nid_pos = src.find(nid)
        nearest = min((abs(nid_pos - s) for s in _cv_region_starts), default=10**9)
        if nearest > 600:
            too_far = True
            break
    if too_far:
        fail.append(
            f"❌ chip_group {it['parent_id']} '{it['parent_name']}' "
            f"(run_length={it['run_length']}, layout={it['layout_hint']}) 的 cell "
            f"离任何 UICollectionView 声明都 >600 char，大概率没用 CV 承载 — "
            f"对照 must_use：{it['must_use']}"
        )

if fail:
    print("\n".join(fail))
    sys.exit(1)
print("✅ list_containers / scroll_intent / chip_group_hits 节点都已用滚动容器")

# 注：判据 (b) 的 600 char 阈值是经验值；如真实代码里 cell id 挨着某个无关 CV 声明（偶发的假阴性），
# 请在代码评审中人工确认；大多数情况下此脚本能钉住 rankChipViews 这类事故形态。
PY
```

**违反处置**：脚本输出 `fail` → 必须重写对应节点，禁止以"视觉一致"为由放过。滚动语义一旦命中，组件类型降级到 `UIView` 即视为交付失败。

### 红线 2：异构容器内的 chip/tag 子集（≥4 个 INSTANCE/COMPONENT/相似 FRAME）也要 UICollectionView

脚本 `_role.is_list_container` 判定要求"父节点的**全部**子节点同构"，但很多设计稿的列表是**藏在异构容器里**的——比如父节点同时有"标题 + 段位 chip 群 + 选中态指示"，脚本就不会把父节点标成 list_container。

**强制规则**：
- 父节点的子节点中存在**连续 ≥4 个 INSTANCE/COMPONENT 或同构 FRAME**（同 size、同 type、x 等间距） → 把这一段单独抽出来当 cell 群 → 用一个 UICollectionView (`LeftAlignedFlowLayout`) 承载
- 例：`341:315 'Group 4'` 的子节点 `[Rectangle, Component 1, Component 5, Component 2, Component 3, Component 4, Component 6, Component 7, TEXT, TEXT, TEXT]` 中，连续 7 个 `Component N` 就是一个 chip 群，必须 UICollectionView，不能各写一个 lazy var

> 📌 **此判定已由 `figma-ios-preload-data` 预扫并写进 `audit.json.chip_group_hits`**，LLM **不需要**自己全局扫 design.json 找 chip 群——只要把 `chip_group_hits` 当必读清单即可。每条 entry 带 `parent_id / run_node_ids / scroll_axis / wrap / layout_hint / must_use / forbidden`，`layout_hint=LeftAlignedFlow` 表示多行折行（`scrollEnabled=false` + 随外层 UIScrollView 滚）、`FlowLayout` 表示单轴排布。下方自检脚本 §3 会反查代码是否落地。

### 红线 3：列表关键词的"三档降级"（**区分滚动语义 vs 集合语义**）⭐️

`audit.json.list_keyword_hits` 列出了所有名字含列表/滚动/集合关键字的节点。每条 entry 带一个 `scroll_intent` 字段，由 `figma-ios-preload-data` 根据关键字自动分类，下游 **禁止** 无视：

**① 滚动语义关键字**（`scroll_intent=true`）：
`可滚动 / 垂直滚动 / 水平滚动 / 垂直列表 / 水平列表 / 列表 / 滚动 / scroll / list`

→ 这类关键字命中时，**节点必须可以滚动**，按以下三档降级选组件：

| 场景 | 组件 | 备注 |
|---|---|---|
| A. 子节点同构（同 type + 相似 size + 命名规律） | `UICollectionView` | `_role.is_list_container` 已自动标，见 list_containers |
| B. 子节点异构（如 `垂直滚动` 容器里塞了 4 个不同表单分区） | **`UIScrollView + contentView`** ⚠️ | **禁止**直接降级到 `UIView`——设计师用"滚动"命名就是要能滚 |
| C. 节点名无滚动语义 **且** 内容总高 ≤ 可用区域 | `UIView` | 仅在两个条件同时满足时允许（本档**不适用滚动关键字命中**场景）|

**② 集合语义关键字**（`scroll_intent=false`）：
`标签组 / 标签区 / 集合 / tag集合 / collection`

→ 多行自适应，本身不一定滚动，按以下两档选组件：

| 场景 | 组件 | 备注 |
|---|---|---|
| A. 子节点同构（5 个 chip 等） | `UICollectionView(LeftAlignedFlow)` | `scrollEnabled=false`，多行自适应 |
| B. 子节点异构 | `UIView` 允许 | 若异构容器里仍有**连续 ≥4 个**同构 INSTANCE/COMPONENT（红线 2），那一段仍然要独立 `UICollectionView` |

**已修复的历史事故**：把 `341:313 "垂直滚动"` 做成了 `UIView`——因为它子节点异构（4 个不同表单分区）。正确做法是 `UIScrollView + contentView`，小屏上内容仍可滚动可见。

判定的 4 维度相似度见下方 §「相似度判定（4 维度）」。

---

## ⚡ QUICK_REF（Agent 优先读此处）

**核心原则：识别 Figma 节点是否需要用 `UICollectionView` 实现。**

**本 SKILL 职责**：
- ✅ 识别节点是否为列表/集合场景
- ✅ 返回识别结果（component, direction, scrollEnabled, confidence）
- ❌ 不负责代码生成（由 `figma-ios-uicollectionview-codegen` SKILL 处理）

### ⭐️ 数据包优先：先查 `_role.is_list_container`

`figma-ios-preload-data` 阶段 1 已经做了**同构子节点的几何判定**，把列表容器标记到了：

- `design.json[node]._role.is_list_container = true`
- `design.json[node]._layout_hint.list = {scroll_axis: "vertical"|"horizontal", cell_template_node_id, cell_count}`
- `index.json.by_role.list_container = [node_id, ...]`

**判断顺序**：
1. **优先查 `_role.is_list_container`**：为 true 时直接当列表容器，`cell_template_node_id` 就是 cell 模板
2. 命中后再用下面的"识别条件"细化 `scrollEnabled` 与 `LeftAlignedFlowLayout` vs `FlowLayout`
3. 没命中 `_role.is_list_container` 时，仍按下面的 A/B/C 条件兜底（脚本判定要求严格，名称含"可滚动/列表/标签组"等关键词的容器可能不被打 list_container 但仍要走 UICollectionView）

### 识别条件（OR 逻辑，满足任一即可）

> **主路径**：先吃 `audit.json.list_containers` / `chip_group_hits` / `list_keyword_hits` 与 `_role.is_list_container`（见上文红线与「数据包优先」）。下表 A/B/C 与后文长段伪代码仅作 **audit 未命中时的兜底**，不要绕过 audit 重算一遍。

| 条件 | 说明 | 置信度 | 示例 |
|------|------|-------|------|
| **A. 节点名称关键词** | "可滚动"/"列表"/"集合"/"标签组" | 0.95 | "可滚动" → UICollectionView |
| **B. 子节点 ≥ 4 且相似** | 4 维度判定，满足 ≥ 2 个维度 | 0.80 | 5 个相似标签 → UICollectionView |
| **C. 包含 SYMBOL/INSTANCE** | 即使只有 1 个，也可能是重复内容 | 0.85 | "可滚动" + SYMBOL → UICollectionView |

### 相似度判定（4 维度）

| 维度 | 判定标准 | 示例 |
|------|---------|------|
| 1. 类型相同 | `type` 一致或都是容器 | 5 个 FRAME |
| 2. 尺寸相似 | width/height 误差 ≤ 20% | 宽度 60-80 |
| 3. 命名规律 | 数字递增/相同前缀/重复名 | "品类"、"品类备份2" |
| 4. 位置规律 | x/y 坐标等间距（误差 ≤ 10%） | x: 0, 100, 200 |

**判定规则**：满足 **2 个或以上维度** → 认为"具有相同特征"

---

### 生成组件对照表

**滚动语义关键字（scroll_intent=true）**：

| Figma 特征 | 子节点同构 | 子节点异构 |
|-----------|-----------|-----------|
| `可滚动` | UICollectionView (horizontal) | **UIScrollView + contentView** |
| `垂直滚动` / `垂直列表` / `列表` | UICollectionView (vertical) | **UIScrollView + contentView** |
| `水平滚动` / `水平列表` | UICollectionView (horizontal) | **UIScrollView + contentView** |
| `滚动` / `scroll` / `list` | UICollectionView（按 axis 推断） | **UIScrollView + contentView** |

**集合语义关键字（scroll_intent=false）**：

| Figma 特征 | 子节点同构 | 子节点异构 |
|-----------|-----------|-----------|
| `标签组` / `标签区` / `集合` / `collection` | UICollectionView (LeftAlignedFlow, `scrollEnabled=false`) | UIView 允许（但连续 ≥4 个同构子集仍要单独抽 UICollectionView）|

**其他推断**：

| 触发条件 | 组件 |
|---|---|
| 含 SYMBOL/INSTANCE 子节点 | UICollectionView |
| ≥4 个相似子节点（详见相似度判定）| UICollectionView |

---

### 识别结果格式

```python
# 成功识别，返回 dict:
{
    'component': 'UICollectionView',
    'direction': 'horizontal' | 'vertical',
    'scrollEnabled': True | False,
    'layoutType': 'FlowLayout' | 'LeftAlignedFlow',  # 可选
    'confidence': 0.80 | 0.85 | 0.95,
    'reason': '识别原因',
    'needModel': True,
    'homogeneous': True | False,  # 可选，是否同构内容
    'warning': 'TODO 提示'  # 可选
}

# 未识别，返回 None
```

---

## 使用场景

当 Agent 需要判断一个 Figma 节点是否应该用 UICollectionView 实现时，调用本 SKILL。

**输入**：
- 数据包 `design.json[node_id]`（数据来自 figma-ios-preload-data 阶段 1）
- 节点 ID 和名称

**输出**：
- 识别结果 dict（如上格式）
- 或 None（不需要 UICollectionView）

**后续流程**：
- 如果返回 dict → 调用 `figma-ios-uicollectionview-codegen` SKILL 生成代码
- 如果返回 None → 按其他规则处理节点

---

## 识别规则（统一决策树）

### 核心识别条件（OR 逻辑）

满足**任一条件**即判定为 UICollectionView：

**A. 节点名称包含关键词**（优先级最高，置信度 0.95）  
**B. 子节点 ≥ 4 且相似度 ≥ 2**（4 维度判定，置信度 0.80）  
**C. 包含 SYMBOL/INSTANCE 节点**（可能是重复内容，置信度 0.85）

---

### 识别函数

```python
def recognize_listview(node_name, node_data):
    """
    统一识别 ListView 类型（统一用 UICollectionView）
    
    返回: {'component', 'direction', 'scrollEnabled', 'confidence', 'reason', ...} 或 None
    """
    name_lower = node_name.lower()
    children = node_data.get('children', [])

    # ========== 优先级 1：可滚动容器关键词 ==========

    scroll_keywords = {
        '可滚动': {'direction': 'horizontal', 'scrollEnabled': True},
        '垂直滚动': {'direction': 'vertical', 'scrollEnabled': True},
        '水平滚动': {'direction': 'horizontal', 'scrollEnabled': True},
        '列表': {'direction': 'vertical', 'scrollEnabled': True},
        'list': {'direction': 'vertical', 'scrollEnabled': True}
    }

    for keyword, config in scroll_keywords.items():
        if keyword in name_lower:
            return {
                'component': 'UICollectionView',
                'direction': config['direction'],
                'scrollEnabled': config['scrollEnabled'],
                'confidence': 0.95,
                'reason': f'节点命名包含"{keyword}"',
                'needModel': True
            }

    # ========== 优先级 2：标签集合关键词 ==========

    collection_keywords = ['标签组', '集合', 'tag集合', 'collection']

    for keyword in collection_keywords:
        if keyword in name_lower:
            return {
                'component': 'UICollectionView',
                'direction': 'vertical',
                'scrollEnabled': False,
                'layoutType': 'LeftAlignedFlow',
                'confidence': 0.95,
                'reason': f'节点命名包含"{keyword}"',
                'needModel': True,
                'homogeneous': True
            }

    # ========== 优先级 3：包含 SYMBOL/INSTANCE ==========
    
    for child_id in children:
        child = get_node(child_id)
        if child and child.get('type') in ['SYMBOL', 'INSTANCE', 'COMPONENT']:
            direction = 'horizontal' if '水平' in name_lower or '可滚动' in name_lower else 'vertical'
            
            return {
                'component': 'UICollectionView',
                'direction': direction,
                'scrollEnabled': True,
                'confidence': 0.85,
                'reason': f'包含 SYMBOL/INSTANCE 节点（可能是重复内容）',
                'needModel': True,
                'warning': 'TODO(阶段3): 接入接口文档后替换为真实数据源（当前为阶段 2 mock）'
            }

    # ========== 优先级 4：子节点 ≥ 4 且相似度 ≥ 2 ==========
    
    if len(children) >= 4:
        similarity_result = check_children_similarity(children, node_data)
        similarity_score = similarity_result.get('score', 0)
        
        if similarity_score >= 2:
            is_tag_collection = similarity_result.get('is_small_items', False)
            
            return {
                'component': 'UICollectionView',
                'direction': 'vertical',
                'scrollEnabled': not is_tag_collection,
                'layoutType': 'LeftAlignedFlow' if is_tag_collection else 'FlowLayout',
                'confidence': 0.80,
                'reason': f'发现 {len(children)} 个相似子节点（相似度: {similarity_score}/4）',
                'needModel': True,
                'homogeneous': True
            }

    return None
```

---

### 相似度判定函数（4 维度）

```python
def check_children_similarity(children, node_data):
    """
    检查子节点相似度（返回满足的维度数 0-4）
    
    返回: {
        'score': int (0-4),
        'is_small_items': bool (判断是否为小标签)
    }
    """
    if len(children) < 2:
        return {'score': 0, 'is_small_items': False}
    
    score = 0
    child_nodes = [get_node(c) for c in children if get_node(c)]
    
    if len(child_nodes) < 2:
        return {'score': 0, 'is_small_items': False}
    
    # 维度 1: 类型相同
    types = [n.get('type') for n in child_nodes]
    container_types = {'FRAME', 'INSTANCE', 'COMPONENT'}
    
    if len(set(types)) == 1 or all(t in container_types for t in types):
        score += 1
    
    # 维度 2: 尺寸相似（容错 20%）
    widths = [n.get('width', 0) for n in child_nodes if n.get('width', 0) > 0]
    heights = [n.get('height', 0) for n in child_nodes if n.get('height', 0) > 0]
    
    size_similar = False
    if len(widths) >= 2 and len(heights) >= 2:
        if is_similar_range(widths, 0.2) and is_similar_range(heights, 0.2):
            score += 1
            size_similar = True
    
    # 维度 3: 命名模式相似
    names = [n.get('name', '') for n in child_nodes]
    if has_naming_pattern(names):
        score += 1
    
    # 维度 4: 位置排列规律
    xs = [n.get('x', 0) for n in child_nodes]
    ys = [n.get('y', 0) for n in child_nodes]
    
    if is_regular_spacing(xs) or is_regular_spacing(ys):
        score += 1
    
    # 判断是否为小标签（width < 150 且 height < 50）
    is_small_items = False
    if size_similar and widths and heights:
        avg_width = sum(widths) / len(widths)
        avg_height = sum(heights) / len(heights)
        if avg_width < 150 and avg_height < 50:
            is_small_items = True
    
    return {'score': score, 'is_small_items': is_small_items}


def is_similar_range(values, tolerance=0.2):
    """检查数值是否在相似范围内（容错比例）"""
    if not values or len(values) < 2:
        return False
    
    avg = sum(values) / len(values)
    if avg == 0:
        return all(v == 0 for v in values)
    
    return all(abs(v - avg) / avg <= tolerance for v in values)


def has_naming_pattern(names):
    """检查命名是否有规律（数字递增/相同前缀/重复名）"""
    if not names or len(names) < 2:
        return False
    
    # 规律 1: 数字递增
    import re
    numbers = [int(m.group(1)) for name in names if (m := re.search(r'(\d+)', name))]
    if len(numbers) == len(names) >= 2:
        if numbers == sorted(numbers) and len(set(numbers)) == len(numbers):
            return True
    
    # 规律 2: 相同前缀（至少 2 个字符）
    import os
    common_prefix = os.path.commonprefix(names)
    if len(common_prefix) >= 2:
        return True
    
    # 规律 3: 相同名称（重复节点）
    if len(set(names)) == 1:
        return True
    
    return False


def is_regular_spacing(positions):
    """检查位置是否等间距分布"""
    if len(positions) < 2:
        return False
    
    sorted_pos = sorted(positions)
    spacings = [sorted_pos[i+1] - sorted_pos[i] for i in range(len(sorted_pos)-1)]
    
    return is_similar_range(spacings, tolerance=0.1)
```

---

## 排除规则

### 不生成 UICollectionView 的场景

1. **节点数量 < 4 且不含关键词**
   - 例：性别选择器（3 个固定按钮）
   - 结果：生成独立按钮

2. **包含右箭头图标**（即使 ≥4 个节点）
   - 判断：节点名包含 `icon_next` 或 `arrow`
   - 结果：单独处理为导航按钮

---


## 实际案例

### 案例 1：品类水平滚动（当前案例）

**Figma 结构**：
```
96:92 "可滚动" (FRAME)
  └─ 96:91 "Property 1=水平" (SYMBOL)
```

**识别流程**：
```
1. 检查节点名称: "可滚动" ✅ → 满足条件 A
   置信度: 0.95
   方向: horizontal（默认）
   
2. 检查子节点: 包含 SYMBOL (96:91) ✅ → 满足条件 C
   置信度: 0.85
   
3. 综合判定: 取最高置信度 = 0.95
```

**生成结果**：UICollectionView（horizontal, scrollEnabled=true）

---

### 案例 2：标签集合（5 个相似标签）

**场景 A：设计师添加了编组"标签组"**
```
条件 A: 节点命名包含"标签组" ✅
置信度: 0.95
```

**场景 B：设计师没有添加编组**
```
条件 B: 子节点 ≥ 4 且相似度判定
  - 节点数量：5 ≥ 4 ✅
  - 维度 1（类型）：都是 FRAME ✅
  - 维度 2（尺寸）：width 60-80, height 28 ✅
  - 维度 4（位置）：x 等间距分布 ✅
  相似度: 3/4 ≥ 2 ✅
  
置信度: 0.80
```

**生成结果**：UICollectionView（LeftAlignedFlow, scrollEnabled=false）

---

### 案例 3：性别选择器（3 个固定按钮）

```
节点数量：3（< 4）
样式不一致：有边框 vs 无边框

结果：生成 3 个独立按钮（不是 CollectionView）
理由：节点数量 < 4，不满足自动识别条件
```

---

## 与其他 Skill 的协作

### 协作流程

```
本 SKILL（识别）
    ↓ 返回识别结果 dict
figma-ios-uicollectionview-codegen（代码生成）
    ↓ 生成 Swift 代码
figma-ios-snapkit-layout（布局约束）
```

### 职责划分

- **本 SKILL**：识别节点是否需要 UICollectionView
- **`figma-ios-uicollectionview-codegen`**：生成完整代码（Model + Mock + CollectionView + Cell + 交互）
- **`figma-ios-snapkit-layout`**：生成 SnapKit 约束代码
- **`figma-ios-rxswift-interaction-pattern`**：生成 RxSwift 交互代码

---

## 设计师协作建议

为了提高识别准确率，建议设计师在 Figma 中使用关键词命名：

**推荐操作（1 分钟）**:
1. 选中所有列表元素
2. Cmd+G 创建编组
3. 重命名为关键词

| UI 场景 | 推荐命名 | scroll_intent | 识别置信度 |
|--------|---------|---|-----------|
| 通用滚动区 | `可滚动` / `滚动` | ✅ true | 0.95 |
| 垂直列表 / 滚动 | `垂直滚动` / `垂直列表` / `列表` | ✅ true | 0.95 |
| 水平列表 / 滚动 | `水平滚动` / `水平列表` | ✅ true | 0.95 |
| 标签集合 | `标签组` / `标签区` / `集合` | ❌ false | 0.95 |

**效果**：识别准确率从 ~80%（自动判定）提升至 99%（关键词匹配）

**关键字单一来源**：完整列表见 `figma-ios-preload-data/src/normalize/audit.py` 的 `LIST_KEYWORDS_SCROLL` 与 `LIST_KEYWORDS_COLLECTION`。新增关键字时，先改那里，再在本文档同步。
