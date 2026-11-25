---
name: visualize-data-structures
description: 为知识库文档生成算法数据结构与执行状态图；调用对应的 kb_draw_* 工具前加载，以选择正确 renderer、输入形状和状态参数。
---

# 数据结构可视化

使用与 renderer 一一对应的 `kb_draw_*` 工具为当前知识库文档生成清晰的算法与数据结构 PNG 配图，例如 `draw_array` 对应 `kb_draw_array`。本 Skill 负责选择 renderer、准备数据和表达算法状态；工具负责用专属参数 schema 受控执行并返回图片路径。

## 适用范围

- 数组、字符串、多行数组、矩阵、表格和网格。
- 栈、队列、双端队列、循环队列和链表。
- 一般树、二叉树、堆、Trie、B+ 树、并查集、线段树和 Fenwick Tree。
- 有向/无向图、DAG、邻接表、邻接矩阵、边列表和多视图图表示。
- DP 表、区间、时间线、位掩码、哈希表、桶、直方图、单调栈/队列。
- 点、线段、向量、多边形、圆和扫描线等坐标几何状态。

## Renderer 路由表

### 线性、表格与区间

| Renderer | 对应工具的必需数据 | 常用可选字段 |
|---|---|---|
| `draw_array` | 一个序列 | `states`、`pointers`、`ranges`、`index_labels`、`row_label` |
| `draw_string` | 一个字符串 | `pattern`、`pattern_offset`、`states`、`pointers`、`ranges` |
| `draw_multi_array` | 行名映射或多行数组 | 单元格 `states`、`column_labels` |
| `draw_matrix` / `draw_table` | 二维单元格数组 | 单元格 `states`、行列标签、annotations |
| `draw_grid` | 矩形网格 | `start`、`end`、`obstacles`、`path`、单元格箭头 |
| `draw_stack` | bottom-to-top 序列 | `states`、`pointers`、`capacity`、`top_label` |
| `draw_queue` | front-to-rear 序列 | `states`、`pointers`、端点标签 |
| `draw_deque` | front-to-rear 序列 | 端点标签、操作箭头、`states` |
| `draw_circular_queue` | 固定槽位序列，`null` 表示空位 | `front`、`rear`、`states` |
| `draw_linked_list` | 节点值序列 | `doubly`、`circular`、`pointers`、`random_links` |
| `draw_dp_table` | DP 二维数组 | 单元格状态、依赖、current/answer、公式 |
| `draw_intervals` / `draw_timeline` | 区间序列 | 扫描位置、轴标签 |
| `draw_mapping` | key/value 映射 | key 与 value 的独立状态 |
| `draw_set` | 元素集合 | 元素状态 |
| `draw_buckets` | bucket 映射或多行 bucket | bucket-entry 状态 |
| `draw_histogram` | 数值高度序列 | `states`、`pointers`、矩形、水位 |
| `draw_hash_table_chaining` | bucket 到键值对的映射 | `capacity` |
| `draw_hash_table_open_addressing` | 键值对或 `null` 槽位序列 | `capacity`、探测序列 |
| `draw_bitmask` / `draw_bits` | 整数或 label-to-integer 映射 | 位宽、有符号模式、高亮位、位标签 |
| `draw_monotonic_stack` | `values`、原数组中的 `stack_indices` | 数组/栈双面板状态 |
| `draw_monotonic_queue` | `values`、原数组中的 `deque_indices` | 数组/队列双面板状态 |

### 树与索引结构

| Renderer | 对应工具的必需数据 | 关键约定 |
|---|---|---|
| `draw_tree` | 嵌套树映射、标量根或 TreeNode | 一般 N 叉树，可选横向/纵向 |
| `draw_binary_tree` | 层序序列、嵌套映射或 TreeNode | 二叉布局与节点语义状态 |
| `draw_heap` / `draw_binary_heap` | heap 数组 | 树和数组双面板；`heap_type` 为 `min`/`max`，工具不验证堆性质 |
| `draw_trie` | 单词序列 | terminal 双环、word/prefix path |
| `draw_bplus_tree` | B+ 树嵌套映射 | 内部索引、叶链，可选 `search_key` |
| `draw_union_find` | parent 整数序列 | parent 数组与森林；`previous_parent` 显示路径压缩 |
| `draw_segment_tree` | 线段树嵌套映射 | query coverage、update path、lazy tag、可选原数组 |
| `draw_fenwick_tree` / `draw_binary_indexed_tree` | BIT 值序列 | 1-based range/path；可选原数组与二进制索引 |

一般树节点形状：

```json
{"value":"root","children":[{"value":"left"},{"value":"right"}]}
```

线段树节点形状：

```json
{"interval":[0,1],"value":3,"children":[{"interval":[0,0],"value":1},{"interval":[1,1],"value":2}]}
```

B+ 树节点使用 `keys`、`children`、`leaf`；内部节点必须有 `len(keys)+1` 个 children，keys 已排序，所有叶子同深度。

### 图与坐标几何

| Renderer | 用途 | 关键参数/约定 |
|---|---|---|
| `draw_graph` | 有向/无向加权图 | edges、`nodes`、布局/位置、`path`、node/edge states |
| `draw_dag` | 严格有向无环图 | 拒绝环和自环；分层布局与跨层边 |
| `draw_adjacency_list` | 邻接表面板 | 显式节点顺序、directed |
| `draw_adjacency_matrix` | 邻接矩阵面板 | 显式节点顺序、directed、absent marker |
| `draw_edge_list` | 边表 | source、target、可选 weight |
| `draw_graph_representations` | 图/邻接表/矩阵/边表多面板比较 | 选择需要展示的 panels |
| `draw_coordinate_plane` | 坐标几何状态 | points、segments、vectors、polygons、circles、scan lines |

图边可写成 `[source,target]` 或 `[source,target,weight]`。权重 0 仍是边；需要保留孤立节点或固定矩阵顺序时显式提供 `nodes`。坐标向量使用 `origin + delta`，不是两个端点；多边形按传入顶点顺序连接，不会自动计算凸包。

## 必须遵守的工作流

1. 先识别图片真正要传达的结构、值、标签、索引以及某一个明确的算法状态。每次渲染是一张**已计算好的快照**；并查集合并、区间聚合、凸包、遍历步骤等算法结果必须先自行推导，再作为参数传给 renderer。
2. 从本 Skill 的路由表中选择最贴切的 renderer。不要用通用图形勉强模拟已经有专用 renderer 的结构，也不要臆造 renderer 名称。
3. 调用同名的 `kb_draw_*` 工具，并按该工具 schema 直接填写 renderer 参数。例如 `draw_dp_table` 对应 `kb_draw_dp_table`。不要猜参数名；复杂 tuple、set 或非字符串映射键按下文使用 `$tuple`、`$set`、`$map`。
4. `kb_draw_skip_list` 已固定使用 legacy 引擎；其余 `kb_draw_*` 工具固定使用 modern 引擎，不要提交 `engine`。
5. 工具成功时只返回 `/media/...png`。随后用 `kb_edit_file` 将 `![简洁且有意义的替代文字](返回路径)` 插入当前 Markdown 文档；不得编造路径或使用本机绝对路径。

示例 `kb_draw_array` 参数：

```json
{
  "values": [2, 7, 11, 15],
  "title": "Two Sum",
  "states": {"current": [1], "success": [2]},
  "pointers": {"left": 0, "right": 3},
  "file_name": "two-sum"
}
```

## 执行边界

- 不执行 Bash、PowerShell、Python 命令或任意脚本；只调用本轮已注册的 `kb_draw_*` 工具。
- 不提供 `renderer`、`engine`、`args`、`kwargs`、`output`、`filename`、`ax`、`axes` 或 `theme`；工具名决定 renderer/engine，输出位置和 PNG 格式由工具管理。
- renderer 参数直接作为工具顶层字段提交；不要把整个规格再次编码成字符串。可选输出名使用 `file_name`。
- 一次工具调用只生成一张图。确实需要多个算法步骤时，分别生成多张有明确用途的快照。

## 数据与状态约定

- 用 `current`、`visited`、`candidate`、`selected`、`success`、`error`、`path`、`frontier`、`disabled`、`empty` 等语义状态表达颜色，不要依赖装饰性颜色传递含义。
- 对支持反向状态映射的索引/节点 renderer，JSON 优先写成 `{"current":[1],"success":[2]}`。
- 矩阵、网格、DP、bucket、Trie、graph edge 等以 selector 为键的状态，按 JSON spec 使用 `$map` 和 `$tuple`。
- Fenwick Tree 的逻辑索引和路径使用 1-based；位掩码业务位编号始终使用 LSB=0。
- 单调栈/队列以原数组索引作为元素身份，重复值不能只靠数值区分。
- 图的矩阵/列表顺序重要时显式提供 `nodes`；权重 0 是有效边。要求无环时使用 `draw_dag`，不要用 `draw_graph` 假装 DAG。
- 显式 `states` 优先于 renderer 自动推导的 query、path 或 component 颜色。

普通索引/节点 renderer 优先使用 state-to-items：

```json
{"current":[1],"success":[2]}
```

需要 tuple selector 的单元格或边状态使用 tagged mapping。例如网格坐标 `(0,2)`：

```json
{
  "$map": [
    [{"$tuple":[0,2]}, "current"]
  ]
}
```

图的边状态同理：

```json
{
  "$map": [
    [{"$tuple":["A","B"]}, "path"],
    [{"$tuple":["B","C"]}, "visited"]
  ]
}
```

只有需要 hashable tuple/set/非字符串键时才使用 tagged form；普通坐标数组通常直接写 `[row,column]` 即可。

## 视觉质量

- 标题说明算法状态而不只是结构名称，例如“Dijkstra：确定节点 B”优于“Graph”。
- 只突出与当前叙述有关的节点、区间、路径或单元格，避免所有元素同时高亮。
- 标签要短且一致；节点很多时减少非必要注释，必要时拆图。
- 保持箭头方向、front/rear、top、父子关系和索引语义与正文一致。
- 中文或特殊符号可能受系统字体影响；无把握时优先使用清楚的 ASCII `->`、`-` 和简短标签。
- 工具报参数或验证错误时，依据后附 reference 修正规格后重试，不要改用 Bash 绕过。

## 维护来源

本正文是知识编辑 Agent 的自足适配版，参数约定来自同目录 `references/api-reference.md` 与 `references/json-spec.md`。模型调用时无需也不能继续读取这些相对文件；以本正文为准直接构造工具参数。
