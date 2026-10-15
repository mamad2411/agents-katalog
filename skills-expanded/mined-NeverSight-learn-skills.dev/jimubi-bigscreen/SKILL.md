---
name: jimubi-bigscreen
description: Use when user asks to create/design a big screen (大屏), full-screen data visualization, or says "创建大屏", "生成大屏", "新建大屏", "设计大屏", "做一个大屏", "BI大屏", "数据大屏", "可视化大屏", "监控大屏", "create big screen", "design big screen", "BI visualization big screen". Also triggers when user describes big screen requirements like "做一个销售数据大屏" or mentions full-screen display like "展厅展示", "监控室大屏". Make sure to use this skill for big screens (大屏) — NOT dashboards (仪表盘/看板), which use a completely different layout and styling system.
---

# JeecgBoot 大屏 AI 自动生成器

将自然语言的大屏需求转换为 drag page 配置，并通过 API 自动创建。

> **本 skill 专门处理大屏（bigScreen）模式**：全屏展示，绝对定位（像素坐标），深色主题，适用于监控室/展厅/展示墙。
> 仪表盘（看板）请使用 `jimubi-dashboard` skill。

## 大屏特征

- **布局**：绝对定位，坐标和尺寸单位为**像素**（如 x=50, y=280, w=860, h=380）
- **主题**：默认 `dark`，深色背景，亮色/霓虹文字
- **背景图**：默认 `/img/bg/bg4.png`，支持自定义
- **装饰元素**：常用 JDragBorder（边框）、JDragDecoration（装饰条）增强视觉效果
- **典型分辨率**：1920×1080

## 前置条件

用户必须提供：
1. **API 地址**：JeecgBoot 后端地址（如 `https://api3.boot.jeecg.com`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

## 交互流程

### Step 0: 解析用户需求

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 页面名称 | 用户指定 | "销售数据大屏" |
| 主题 | dark | dark |
| 背景图 | `/img/bg/bg4.png` | 可自定义 |
| 组件列表 | 从描述中解析 | 销售额(数字)、订单趋势(折线图)、区域分布(地图) |

### Step 1: 识别组件并选择类型

阅读 `references/bi-component-types.md` 获取完整组件类型清单。

**常用大屏组件速查：**

| 用户描述关键词 | 组件 component | 说明 |
|---------------|---------------|------|
| 数字/KPI/指标 | `JNumber` | 数字指标卡 |
| 翻牌器/数字动画 | `JCountTo` | 数字翻牌器 |
| 柱状图 | `JBar` | 基础柱状图 |
| 横向柱状图 | `JHorizontalBar` | 水平柱状图 |
| 堆叠柱状图 | `JStackBar` | 堆叠柱状图 |
| 折线图/趋势 | `JLine` | 折线图 |
| 曲线图 | `JSmoothLine` | 平滑曲线 |
| 柱线混合 | `JMixLineBar` | 柱状+折线混合 |
| 饼图 | `JPie` | 饼图 |
| 环形图 | `JRing` | 环形图 |
| 玫瑰图 | `JRose` | 南丁格尔玫瑰图 |
| 仪表盘/表盘 | `JGauge` | 仪表盘表盘 |
| 水球图 | `JLiquid` | 水球图 |
| 进度条 | `JProgress` | 进度条 |
| 雷达图 | `JRadar` | 雷达图 |
| 漏斗图 | `JFunnel` | 漏斗图 |
| 词云 | `JWordCloud` | 词云图 |
| 地图/区域地图 | `JAreaMap` | 区域地图 |
| 飞线地图/迁徙 | `JFlyLineMap` | 飞线地图 |
| 热力地图 | `JHeatMap` | 热力地图 |
| 滚动表格 | `JScrollTable` | 自动滚动表格 |
| 排行榜/排名 | `JScrollRankingBoard` | 滚动排行榜 |
| 文本/标题 | `JText` | 文本显示 |
| 图片 | `JImg` | 图片 |
| 视频 | `JVideoPlay` | 视频播放 |
| 边框/装饰 | `JDragBorder` | 装饰边框（13种样式） |
| 装饰条 | `JDragDecoration` | 装饰条（12种样式） |
| 时钟 | `JCurrentTime` | 实时时钟 |

### Step 2: 展示设计摘要并确认

**必须展示，等待用户确认后再执行：**

```
## 大屏设计摘要

- 页面名称：销售数据大屏
- 主题：dark
- 背景图：/img/bg/bg4.png

### 组件列表

| 序号 | 组件名称 | 组件类型 | 位置(x,y) | 尺寸(w×h) | 数据源 |
|------|---------|---------|-----------|----------|--------|
| 1 | 今日销售额 | JNumber | (50,50) | 400×200 | 静态数据 |
| 2 | 销售趋势 | JLine | (50,280) | 860×380 | 静态数据 |

确认以上信息正确？(y/n)
```

### Step 3: 调用 API 创建大屏

**优先使用共通工具库 `bi_utils.py`**（两个位置均有副本）：
- Skills 目录（权威副本）：`C:\Users\zhang\.claude\skills\jimubi-bigscreen\references\bi_utils.py`
- 后端项目根目录（运行副本）：`{后端项目根目录}\bi_utils.py`

> 如果后端项目根目录没有 `bi_utils.py`，先从 skills 目录复制过去再使用。

**执行步骤：**
```
1. 确认后端项目根目录有 bi_utils.py（没有则从 skills 复制）
2. Write 工具 → 写入业务脚本 create_xxx_screen.py（项目根目录）
3. Bash 工具 → cd {后端项目根目录} && python create_xxx_screen.py
4. Bash 工具 → rm create_xxx_screen.py（清理临时脚本）
```

---

## 备选方式：从模板复制创建大屏

> **注意：模板复制方式仅作为备选。** 模板 JSON 中的 config 结构复杂且样式耦合严重，批量文本替换容易破坏配置完整性，生成效果往往不理想。仅在需要精确还原某个已有模板的视觉布局时才考虑使用。

### 模板目录

`references/templates/bigScreen/` 下有 40 个大屏模板 JSON 可供选择。

### 模板复制完整流程

```python
import sys, json
sys.path.insert(0, r'{后端项目根目录}')
from bi_utils import *
import bi_utils

init_api('http://api3.boot.jeecg.com', 'your-token')

# 1. 读取模板 JSON
tpl_path = r'C:/Users/zhang/.claude/skills/jimubi-bigscreen/references/templates/bigScreen/集团综合数据大屏_1151069555267260416.json'
with open(tpl_path, 'r', encoding='utf-8') as f:
    tpl_data = json.load(f)
template_components = tpl_data.get('template', [])

# 2. 建立旧 ID → 新 ID 映射（关键！）
id_mapping = {}
for comp in template_components:
    old_i = comp['i']
    id_mapping[old_i] = bi_utils._gen_uuid()

# 3. 更新组件 ID 和清理
for comp in template_components:
    comp['i'] = id_mapping[comp['i']]
    comp.pop('pageCompId', None)
    # config 字符串转 dict
    config = comp.get('config', {})
    if isinstance(config, str):
        try: config = json.loads(config)
        except: config = {}
    comp['config'] = config

# 4. 更新 JTabToggle 的 compVals 引用（否则页签切换不工作）
for comp in template_components:
    if comp['component'] == 'JTabToggle':
        for item in comp['config'].get('option', {}).get('items', []):
            item['compVals'] = [id_mapping.get(v, v) for v in item.get('compVals', [])]

# 5. 更新 JGroup 内部 props.elements 中的 ID 引用
for comp in template_components:
    if comp['component'] == 'JGroup':
        props = comp.get('props', {})
        elements = props.get('elements', [])
        if elements:
            el_str = json.dumps(elements, ensure_ascii=False)
            for old_id, new_id in id_mapping.items():
                el_str = el_str.replace(old_id, new_id)
            props['elements'] = json.loads(el_str)

# 6. 创建页面并保存
page_id = create_page('我的大屏', style='bigScreen', theme='dark',
                       background_image='/img/bg/bg4.png')
bi_utils._page_components[page_id] = template_components
save_page(page_id)
```

### 模板复制踩坑记录

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| **页签切换不工作** | JTabToggle 的 `compVals` 引用了旧组件 ID | 必须建立 ID 映射，更新 `config.option.items[].compVals` |
| **JGroup 内部组件异常** | JGroup 的 `props.elements` 内也有 ID 交叉引用 | 序列化后批量替换旧 ID |
| **新增组件不显示** | config 格式不完整或被头部背景图遮挡 | 用模板中已有的同类组件 config 作参考；设 `orderNum: 300` 提高层级 |

### 替换业务数据

对整个 template JSON 字符串做批量文本替换，可高效替换所有标题、标签、数值：

```python
# 序列化为字符串
tpl_str = json.dumps(tpl_data['template'], ensure_ascii=False)

# 批量替换
replacements = {
    '集团业务综合管理平台': '招商银行经营管理驾驶舱',
    '新成业务板块': '零售金融业务',
    '合同': '业务单',
    # ... 更多映射
}
for old, new in replacements.items():
    tpl_str = tpl_str.replace(old, new)

# 解析回 list
template_components = json.loads(tpl_str)
```

### 向已有大屏新增组件

> **关键：新增组件的 config 必须从模板中同类组件复制，不要自己拼装。**

```python
# 从其他模板中找到参考组件的 config
# 例如 JWeatherForecast 用 template=11 样式
weather = {
    'component': 'JWeatherForecast',
    'componentName': '今日天气',
    'visible': True,
    'i': bi_utils._gen_uuid(),
    'x': 15, 'y': 15, 'w': 300, 'h': 50,
    'orderNum': 300,  # 高层级，不被背景图遮挡
    'config': {
        'size': {'width': 300, 'height': 50},
        'w': 300, 'dataType': 1, 'h': 50,
        'option': {
            'template': 11, 'bgColor': '', 'city': '',
            'num': 1, 'fontSize': 16, 'fontColor': '#ffffff', 'url': '',
        },
    },
}

# JCurrentTime 用模板中已有的完整 config
# 先从模板中读取：
for comp in tpl_data['template']:
    if comp.get('component') == 'JCurrentTime':
        ref_config = comp.get('config', {})
        break

clock = {
    'component': 'JCurrentTime',
    'componentName': '实时日期',
    'visible': True,
    'i': bi_utils._gen_uuid(),
    'x': 1580, 'y': 15, 'w': 320, 'h': 40,
    'orderNum': 300,
    'config': ref_config,  # 直接用模板的 config
}

# 查询页面、追加组件、保存
page = query_page(page_id)
tmpl = page.get('template', [])
if isinstance(tmpl, str): tmpl = json.loads(tmpl)
tmpl.append(weather)
tmpl.append(clock)
bi_utils._page_components[page_id] = tmpl
save_page(page_id)
```

---

## 推荐方式：使用默认组件函数创建大屏（效果最佳）

> **重要：优先使用 bi_utils 的默认组件函数（add_chart、add_number、add_text、add_ranking 等）逐个添加组件，只填充业务数据。** bi_utils 内置了经过验证的大屏样式预设（深色配色、轴标签颜色、card 配置等），生成效果稳定且美观，远优于模板复制后批量替换的方式。

**大屏创建示例：**
```python
import sys
sys.path.insert(0, r'{后端项目根目录}')
from bi_utils import *

init_api('https://api3.boot.jeecg.com', 'your-token')

# 创建大屏（style='bigScreen'，像素坐标）
page_id = create_page('销售数据大屏', style='bigScreen', theme='dark',
                       background_image='/img/bg/bg4.png')

# 添加组件（坐标和尺寸单位为像素）
add_number(page_id, '今日销售额', x=50, y=50, w=400, h=200,
           value=128560, prefix='¥', suffix='元')

add_chart(page_id, 'JLine', '销售趋势', x=50, y=280, w=860, h=380,
          categories=['1月','2月','3月','4月','5月','6月'],
          series=[{'name':'销售额', 'data':[820,932,901,934,1290,1330]}])

add_chart(page_id, 'JBar', '部门业绩', x=950, y=280, w=860, h=380,
          categories=['研发部','销售部','市场部','运营部'],
          series=[{'name':'业绩', 'data':[320,302,341,374]}])

add_chart(page_id, 'JPie', '客户来源', x=50, y=700, w=500, h=350,
          pie_data=[
              {'name':'直接访问', 'value':335},
              {'name':'邮件营销', 'value':310},
              {'name':'联盟广告', 'value':234},
          ])

add_table(page_id, '销售明细', x=600, y=700, w=700, h=350,
          columns=['日期','客户','金额','状态'],
          data=[
              {'日期':'2026-03-01','客户':'A公司','金额':'50000','状态':'已完成'},
              {'日期':'2026-03-02','客户':'B公司','金额':'32000','状态':'进行中'},
          ])

# 添加装饰元素
add_border(page_id, x=30, y=30, w=440, h=240, border_type=1, color='#00BAFF')
add_decoration(page_id, x=660, y=20, w=600, h=60, deco_type=5, color='#00BAFF')

save_page(page_id)
print(f'大屏创建成功！ID: {page_id}')
```

**大屏样式特点（bi_utils.py 自动应用）：**
- 背景：透明 `rgba(0,0,0,0)`
- 文字颜色：白色 `#ffffff`
- 轴标签：白色 `#ffffff`
- 网格线：`rgba(255,255,255,0.1)`
- 表格：深色背景 + 白色文字

## 大屏标题规则（重要）

### card.title 必须为空

大屏模式下，所有图表组件的 `option.card.title` 必须为空字符串 `''`。图表标题只通过 `option.title.text` 显示（ECharts 内部标题）。

**原因：** card.title 会在组件顶部生成一个单独的卡片头部条（白色背景），与深色大屏背景严重冲突，且与 ECharts 的 option.title 形成双重标题。`bi_utils.py` 已自动处理此逻辑——大屏模式下 `_make_card()` 始终将 card.title 设为空。

### 大屏页面标题用 JText

大屏页面的主标题（如 "CRM 数据大屏"）使用 `add_text()` 组件，推荐配置：
- **fontSize**: 40 以上（大屏标题要醒目）
- **fontWeight**: `'bold'`
- **letterSpacing**: 5（增加间距，提升视觉效果）
- **color**: 白色 `#ffffff`

```python
add_text(page_id, 'CRM 数据大屏', x=560, y=15, w=800, h=60,
         font_size=42, color='#ffffff', font_weight='bold',
         text_align='center', letter_spacing=5)
```

### JText 正确的 config 格式

`add_text()` 内部使用的 config 结构（从真实模板验证）：
```python
config = {
    'dataType': 1,
    'chartData': {'value': '显示文本'},  # 注意：是 dict 不是字符串
    'option': {
        'body': {
            'color': '#ffffff',
            'fontSize': 42,
            'fontWeight': 'bold',
            'letterSpacing': 5,
            'text': '',
            'marginTop': 0,
            'marginLeft': 0,
        },
        'textAlign': 'center',
        'card': {'title': '', ...},
    },
}
```

### 不要用 JDragDecoration 做标题装饰

JDragDecoration 的各种 type（红色虚线条、红绿色段等）与大屏标题区域不搭配。真实的大屏模板中，标题区域只用 JText 或 JImg，不使用 JDragDecoration。JDragBorder 和 JDragDecoration 适合用在图表区域的边框装饰。

### Step 4: 输出结果

```
## 大屏创建成功

- 页面ID：{id}
- 页面名称：{name}
- 模式：大屏（bigScreen）
- 预览地址：{API_BASE}/drag/page/view/{id}
- 组件数量：{count} 个

请在大屏设计器中查看：打开 JeecgBoot 后台 → 大屏设计器 → 找到该页面
```

---

## 数据集管理（动态数据源）

大屏组件支持三种数据类型（`config.dataType`）：
- `1` — 静态数据（直接写在 `chartData` 中）
- `2` — 动态数据（从数据集获取，支持 SQL / API / JSON / WebSocket）
- `4` — 表单数据（从表单关联字段查询）

### 数据集 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/drag/onlDragDatasetHead/add` | POST | 创建数据集 |
| `/drag/onlDragDatasetHead/edit` | POST | 编辑数据集（需要 `sign` 字段） |
| `/drag/onlDragDatasetHead/delete?id=xxx` | DELETE | 删除数据集 |
| `/drag/onlDragDatasetHead/list` | GET | 分页查询数据集列表 |
| `/drag/onlDragDatasetHead/getAllChartData` | POST | 执行数据集查询（获取图表数据） |
| `/drag/onlDragDatasetHead/queryFieldBySql` | POST | 解析 SQL 返回字段列表 |
| `/drag/onlDragDatasetHead/queryFieldByApi` | POST | 解析 API 返回字段列表 |

### 数据集实体结构（OnlDragDatasetHead）

```python
{
    'name': '数据集名称',
    'code': '数据集编码',          # 可选，唯一标识
    'dataType': 'sql',             # sql / api / json / singleFile / FILES
    'dbSource': '707437208002265088',  # 数据库源 ID（SQL 类型必填！）
    'querySql': 'SELECT ...',      # SQL 语句（SQL 类型）或 API 地址（API 类型）
    'apiMethod': 'get',            # HTTP 方法（API 类型用）
    'izAgent': '0',                # 是否代理：'0'=直连, '1'=服务端代理
    'content': '',                 # 描述
    'parentId': '',                # 父级分类 ID
    'datasetItemList': [           # 字段列表（注意：不是 onlDragDatasetItemList）
        {'fieldName': 'name', 'fieldTxt': '名称', 'fieldType': 'String', 'izShow': 'Y', 'orderNum': 0},
        {'fieldName': 'value', 'fieldTxt': '数值', 'fieldType': 'String', 'izShow': 'Y', 'orderNum': 1}
    ],
    'datasetParamList': [          # 参数列表（注意：不是 onlDragDatasetParamList）
        {'paramName': 'sex', 'paramTxt': '性别', 'paramValue': '1', 'dictCode': 'sex'}
    ]
}
```

### 创建 SQL 数据集

```python
import sys, json
sys.path.insert(0, r'{后端项目根目录}')
import bi_utils
bi_utils.init_api('http://api3.boot.jeecg.com', 'your-token')

# 创建 SQL 数据集（dbSource 必填！）
result = bi_utils._request('POST', '/drag/onlDragDatasetHead/add', data={
    'name': '用户男女比例统计',
    'code': 'user_sex_ratio',
    'dataType': 'sql',
    'dbSource': '707437208002265088',   # 本地 MySQL 数据源 ID
    'querySql': "SELECT sex as name, COUNT(*) AS value FROM demo WHERE sex IS NOT NULL AND sex != '' GROUP BY sex",
    'apiMethod': 'GET',
    'datasetItemList': [
        {'fieldName': 'name', 'fieldTxt': 'name', 'fieldType': 'String', 'izShow': 'Y', 'orderNum': 0},
        {'fieldName': 'value', 'fieldTxt': 'value', 'fieldType': 'String', 'izShow': 'Y', 'orderNum': 1}
    ],
    'datasetParamList': []
})
dataset_id = result['result']['id']

# 测试数据集
test = bi_utils._request('POST', '/drag/onlDragDatasetHead/getAllChartData', data={'id': dataset_id})
print(json.dumps(test, ensure_ascii=False))
# 返回: {"success":true, "result":{"data":[{"name":"1","value":6},{"name":"2","value":5}]}}
```

### 创建 API 数据集

```python
result = bi_utils._request('POST', '/drag/onlDragDatasetHead/add', data={
    'name': '产品销量排行榜',
    'code': 'product_sales',
    'dataType': 'api',
    'dbSource': None,                   # API 类型不需要数据库源
    'querySql': 'https://api.jeecg.com/mock/31/graphreport/aiproducttest',  # API 地址存在 querySql 字段
    'apiMethod': 'get',
    'izAgent': '0',                     # '0'=前端直连, '1'=后端代理（跨域时用）
    'datasetItemList': [
        {'fieldName': 'name', 'fieldTxt': 'name', 'fieldType': 'String', 'izShow': 'Y', 'orderNum': 0},
        {'fieldName': 'value', 'fieldTxt': 'value', 'fieldType': 'String', 'izShow': 'Y', 'orderNum': 1}
    ],
    'datasetParamList': []
})
dataset_id = result['result']['id']
```

### 组件绑定数据集（dataType=2）

组件的 `config` 中需要设置以下字段来绑定数据集：

```python
config = {
    'dataType': 2,                      # 2=动态数据
    'dataSetId': dataset_id,            # 数据集 ID
    'dataSetName': '数据集名称',
    'dataSetType': 'sql',               # sql / api / json / websocket
    'dataSetApi': 'SELECT ...',         # SQL 语句或 API 地址
    'dataSetMethod': 'get',             # HTTP 方法
    'dataSetIzAgent': '1',              # SQL 类型用 '1'（走后端代理），API 直连用 '0'
    'dataMapping': [                    # 字段映射（关键！）
        {'filed': '维度', 'mapping': 'name'},   # 注意：filed 不是 field（系统拼写）
        {'filed': '数值', 'mapping': 'value'},
        # {'filed': '分组', 'mapping': 'type'},  # 多系列图表需要
    ],
    'chartData': '[]',                  # 动态数据时可为空数组
    'option': { ... }                   # ECharts 配置
}
```

### 标准字段映射规则

| 映射标签（filed） | 标准字段（key） | 说明 |
|-------------------|----------------|------|
| `维度` / `名称` | `name` | 图表类目/维度 |
| `数值` | `value` | 图表数值 |
| `分组` | `type` | 多系列区分字段 |
| `文本` | `label` | 文本标签 |

### 组件绑定数据集完整示例（SQL 饼图）

```python
pie_comp = {
    'component': 'JPie',
    'componentName': '男女比例',
    'visible': True,
    'i': bi_utils._gen_uuid(),
    'x': 750, 'y': 700, 'w': 450, 'h': 350,
    'orderNum': 300,
    'config': {
        'dataType': 2,
        'w': 450, 'h': 350,
        'size': {'width': 450, 'height': 350},
        'dataSetId': dataset_id,
        'dataSetName': '用户男女比例统计',
        'dataSetType': 'sql',
        'dataSetApi': "SELECT sex as name, COUNT(*) AS value FROM demo ...",
        'dataSetMethod': 'GET',
        'dataSetIzAgent': '1',
        'dataMapping': [
            {'filed': '维度', 'mapping': 'name'},
            {'filed': '数值', 'mapping': 'value'}
        ],
        'chartData': '[]',
        'option': { ... }
    }
}
```

### 组件绑定数据集完整示例（API 柱形图）

```python
bar_comp = {
    'component': 'JBar',
    'componentName': '销量排行',
    'visible': True,
    'i': bi_utils._gen_uuid(),
    'x': 1350, 'y': 700, 'w': 540, 'h': 350,
    'orderNum': 300,
    'config': {
        'dataType': 2,
        'w': 540, 'h': 350,
        'size': {'width': 540, 'height': 350},
        'dataSetType': 'api',
        'dataSetApi': 'https://api.jeecg.com/mock/31/graphreport/aiproducttest',
        'dataSetMethod': 'get',
        'dataSetIzAgent': '0',          # API 直连不走代理
        'dataMapping': [
            {'filed': '维度', 'mapping': 'name'},
            {'filed': '数值', 'mapping': 'value'}
        ],
        'chartData': '[]',
        'option': { ... }
    }
}
```

### 数据集踩坑记录

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| **"数据源不存在"** | SQL 数据集未设置 `dbSource` | 必须指定 `dbSource`（如 `707437208002265088`） |
| **字段列表不生效** | 用了 `onlDragDatasetItemList` | 正确字段名是 `datasetItemList` |
| **编辑数据集 510 权限错误** | 缺少 `sign` 字段 | 编辑时需传 `sign: 'E19D6243CB1945AB4F7202A1B00F77D5'` |
| **dataMapping 的 filed 拼写** | 系统中 `filed` 不是 `field` | 必须用 `filed`（少一个 d），这是系统设计 |
| **API 类型跨域** | 前端直连外部 API 遇到 CORS | 设置 `izAgent: '1'` 走后端代理 |
| **SQL 参数替换** | 需要动态参数 | SQL 中用 `#{paramName}`（系统变量）或 `${paramName}`（FreeMarker） |
| **SQL 最大返回 1000 条** | 后端限制 | `getChartData` 方法限制最大 1000 条记录 |

### 数据库源 ID 参考

| 环境 | dbSource / dbCode | 说明 |
|------|-------------------|------|
| api3.boot.jeecg.com 主库 | `707437208002265088` | 默认 MySQL 数据库 |

> **注意**：不同环境的 dbSource ID 不同，部署到新环境时需要通过 `/sys/dataSource/list` 查询可用的数据源列表。

---

## 编辑已有大屏

```python
from bi_utils import *
init_api('https://api3.boot.jeecg.com', 'your-token')

page = query_page(page_id)
print(page['name'], page['updateCount'])

add_chart(page_id, 'JBar', '新增图表', x=0, y=500, w=600, h=300,
          categories=['A','B','C'], series=[{'name':'值','data':[10,20,30]}])
save_page(page_id)
```

---

## 删除大屏

```python
from bi_utils import *
init_api('https://api3.boot.jeecg.com', 'your-token')

delete_page(page_id)                # 软删除
delete_page(page_id, physical=True) # 硬删除
recover_page(page_id)               # 恢复
```

---

## 修改组件样式

阅读 `references/bi-comp-option-config.md` 获取每种组件的完整配置项路径。

**关键规则：**
- 颜色使用色值（`#000000`），不用英文单词
- customColor 格式：`[{color1:'#xxx',color:'#xxx'}]`（适用于 JPie/JLine/JBar 等 20+ 组件）
- 柱体颜色：`option.series[index].itemStyle.color`

```python
import sys, json
sys.path.insert(0, r'{后端项目根目录}')
from bi_utils import *
import bi_utils

init_api('https://api3.boot.jeecg.com', 'your-token')

page_id = 'xxx'
page = query_page(page_id)
tmpl = page.get('template', [])
if isinstance(tmpl, str):
    tmpl = json.loads(tmpl)

for comp in tmpl:
    config_str = comp.get('config', '{}')
    config = json.loads(config_str) if isinstance(config_str, str) else config_str
    if comp.get('component') == 'JBar':
        option = config.get('option', {})
        option['series'][0]['itemStyle'] = {'color': '#FF0000'}
        config['option'] = option
        comp['config'] = json.dumps(config, ensure_ascii=False)

bi_utils._page_components[page_id] = tmpl
save_page(page_id)
```

---

## 可用的快捷函数

**API 初始化：**
- `init_api(api_base, token)` — 初始化 API 地址和 Token

**页面管理：**
- `create_page(name, style='bigScreen', theme='dark', background_image, type_id, design_type)` — 创建大屏
- `query_page(page_id)` — 查询页面详情
- `list_pages(style='bigScreen')` — 列表查询
- `save_page(page_id)` — 保存设计
- `delete_page(page_id, physical)` — 删除
- `recover_page(page_id)` — 恢复
- `copy_page(page_id)` — 复制

**添加组件（像素坐标）：**
- `add_number(page_id, title, x, y, w, h, value, prefix, suffix)` — 数字指标
- `add_chart(page_id, chart_type, title, x, y, w, h, categories, series, pie_data)` — 图表
- `add_table(page_id, title, x, y, w, h, columns, data)` — 数据表格
- `add_scroll_table(page_id, title, x, y, w, h, columns, data)` — 滚动表格
- `add_ranking(page_id, title, x, y, w, h, data)` — 排行榜
- `add_text(page_id, title, x, y, w, h, content, font_size, color)` — 文本
- `add_image(page_id, title, x, y, w, h, src)` — 图片
- `add_gauge(page_id, title, x, y, w, h, value, max_val, unit, color)` — 仪表盘表盘
- `add_liquid(page_id, title, x, y, w, h, value, color)` — 水球图
- `add_countdown(page_id, title, x, y, w, h, value, font_size, color)` — 翻牌器
- `add_border(page_id, x, y, w, h, border_type, color)` — 装饰边框
- `add_decoration(page_id, x, y, w, h, deco_type, color)` — 装饰条
- `add_component(page_id, component, title, x, y, w, h, config)` — 通用组件

---

## API 踩坑记录

| 问题 | 说明 |
|------|------|
| `POST /drag/page/add` 返回值 | 返回完整实体含 ID，`result.id` 即页面 ID |
| `POST /drag/page/edit` 乐观锁 | 必须传 `updateCount`（当前数据库值） |
| Windows curl 中文问题 | 必须用 Python urllib/requests |
| 坐标单位 | 大屏用**像素**坐标 |
| 组件 config 分离 | config 存在 onl_drag_page_comp 表 |
| **chartData 必须是 JSON 字符串** | `config.chartData` 的值必须是 `json.dumps(...)` 后的字符串，不能是原生 list/dict |
| **图表标题去重** | 大屏和仪表盘的图表组件 `option.card.title` 都应为空字符串，标题仅通过 `option.title.text` 显示 |
| **多系列 chartData 格式** | 多系列图表需要 `type` 字段区分：`[{"name":"1月","value":10,"type":"系列A"}]` |
| **HTTPS 连接问题** | api3.boot.jeecg.com 使用 HTTP 协议，`init_api` 时用 `http://` |
| **模板复制后页签切换失效** | 复制模板时必须建立旧→新 ID 映射，更新 JTabToggle 的 `compVals` 和 JGroup 的 `props.elements` 内引用 |
| **新增组件不显示** | config 不完整或被背景图遮挡。必须从模板中同类组件复制 config，并设 `orderNum: 300` 提高层级 |
| **JGroup 子组件存储位置** | JGroup 的子组件在 `comp.props.elements` 数组中（不是 config.chartData 也不是 group 字段） |

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401） | 重新获取 X-Access-Token |
| `updateCount` 不匹配 | 重新查询页面获取最新值 |
| 组件不显示 | 检查 dataType、chartData（必须是 JSON 字符串）、option 是否完整 |
| 新增组件不显示 | **从模板中复制同类组件的完整 config**，不要自己拼装；设 `orderNum: 300` |
| 布局错乱 | 确认使用像素坐标（不是栅格） |
| 中文乱码 | 使用 Python（不要用 curl） |
| 页签切换不工作 | 检查 JTabToggle 的 `compVals` 是否指向正确的 JGroup `i` 值 |

## 参考文档

- `references/bi-component-types.md` — 完整组件类型清单
- `references/bi-comp-option-config.md` — 组件样式配置路径
- `references/bi_utils.py` — 工具库源码
- `references/templates/bigScreen/` — 40 个大屏模板 JSON 参考
