---
name: jimubi-dashboard
description: Use when user asks to create/design a dashboard (仪表盘/看板), data kanban, or says "创建仪表盘", "生成仪表盘", "做一个仪表盘", "数据看板", "做一个看板", "创建看板", "数据面板", "统计看板", "运营看板", "create dashboard", "generate dashboard", "design dashboard", "data kanban", "KPI dashboard". Also triggers when user describes dashboard/kanban requirements like "做一个运营数据看板" or mentions grid-layout data display like "统计系统数据". Make sure to use this skill for dashboards (仪表盘/看板) — NOT big screens (大屏), which use completely different positioning, styling, and component configurations.
---

# JeecgBoot 仪表盘 AI 自动生成器

将自然语言的仪表盘需求转换为 drag page 配置，并通过 API 自动创建。

> **本 skill 专门处理仪表盘（default）模式**：网格布局（24列栅格），亮色主题，带卡片头，适用于日常数据看板。
> 大屏请使用 `jimubi-bigscreen` skill。

## 仪表盘特征

- **布局**：24 列栅格，坐标和尺寸单位为**栅格单位**（如 x=0, y=0, w=6, h=17）
- **主题**：默认 `default`，白色背景，深色文字
- **无背景图**：仪表盘通常不设背景图
- **卡片头**：仪表盘支持卡片头，但图表组件的 `card.title` 应留空（标题由 ECharts `option.title` 显示），避免标题重复
- **颜色体系**：白底 `#FFFFFF`、深灰标题 `#464646`、浅灰轴标签 `#909198`、浅灰网格 `#F3F3F3`

## 仪表盘栅格布局规则

| 组件类型 | 推荐 w | 推荐 h | 说明 |
|---------|--------|--------|------|
| JNumber | 6 | 17 | 数字卡片，4 个一行正好 24 列 |
| JLine/JBar/JSmoothLine | 12-14 | 28-35 | 图表，通常半宽或更宽 |
| JPie/JRing/JRose | 10-12 | 28-35 | 饼图/环形图 |
| JHorizontalBar | 12 | 28-35 | 横向柱状图 |
| JTable/JCommonTable | 12 | 30-40 | 数据表格 |
| JScrollTable | 12 | 30-40 | 滚动表格 |
| JScrollRankingBoard | 12 | 30-35 | 排行榜 |
| JGauge | 6-8 | 25-30 | 仪表盘表盘 |
| JLiquid | 6 | 25-30 | 水球图 |

**布局原则：**
- 总宽度 24 列，组件 w 之和不要超过 24
- 第一行通常放 4 个 JNumber（w=6×4=24）
- 第二行放图表组合（如 JLine w=14 + JPie w=10 = 24）
- 第三行放表格/排行等

## 前置条件

用户必须提供：
1. **API 地址**：JeecgBoot 后端地址（如 `https://api3.boot.jeecg.com`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

## 交互流程

### Step 0: 解析用户需求

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 页面名称 | 用户指定 | "运营数据看板" |
| 主题 | default | default |
| 组件列表 | 从描述中解析 | 用户总数(数字)、增长趋势(折线)、来源分布(饼图) |

### Step 1: 识别组件并选择类型

阅读 `references/bi-component-types.md` 获取完整组件类型清单。

**常用仪表盘组件速查：**

| 用户描述关键词 | 组件 component | 说明 |
|---------------|---------------|------|
| 数字/KPI/指标/总数 | `JNumber` | 数字指标卡（带卡片头） |
| 柱状图 | `JBar` | 基础柱状图 |
| 横向柱状图 | `JHorizontalBar` | 水平柱状图 |
| 折线图/趋势 | `JLine` | 折线图 |
| 曲线图 | `JSmoothLine` | 平滑曲线 |
| 柱线混合 | `JMixLineBar` | 柱状+折线混合 |
| 饼图 | `JPie` | 饼图 |
| 环形图 | `JRing` | 环形图 |
| 玫瑰图 | `JRose` | 南丁格尔玫瑰图 |
| 表盘 | `JGauge` | 仪表盘表盘 |
| 水球图 | `JLiquid` | 水球图 |
| 进度条 | `JProgress` | 进度条 |
| 雷达图 | `JRadar` | 雷达图 |
| 漏斗图 | `JFunnel` | 漏斗图 |
| 地图 | `JAreaMap` | 区域地图 |
| 数据表格 | `JTable` / `JCommonTable` | 数据表格 |
| 滚动表格 | `JScrollTable` | 自动滚动表格 |
| 排行榜 | `JScrollRankingBoard` | 滚动排行榜 |
| 日历 | `JCalendar` | 日历组件 |

### Step 2: 展示设计摘要并确认

**必须展示，等待用户确认后再执行：**

```
## 仪表盘设计摘要

- 页面名称：运营数据看板
- 主题：default

### 组件列表

| 序号 | 组件名称 | 组件类型 | 位置(x,y) | 尺寸(w×h) | 数据源 |
|------|---------|---------|-----------|----------|--------|
| 1 | 总用户数 | JNumber | (0,0) | 6×17 | 静态数据 |
| 2 | 今日活跃 | JNumber | (6,0) | 6×17 | 静态数据 |
| 3 | 用户增长趋势 | JLine | (0,17) | 14×35 | 静态数据 |
| 4 | 用户来源 | JPie | (14,17) | 10×35 | 静态数据 |

确认以上信息正确？(y/n)
```

### Step 3: 调用 API 创建仪表盘

**优先使用共通工具库 `bi_utils.py`**（两个位置均有副本）：
- Skills 目录（权威副本）：`C:\Users\zhang\.claude\skills\jimubi-dashboard\references\bi_utils.py`
- 后端项目根目录（运行副本）：`{后端项目根目录}\bi_utils.py`

> 如果后端项目根目录没有 `bi_utils.py`，先从 skills 目录复制过去再使用。

**执行步骤：**
```
1. 确认后端项目根目录有 bi_utils.py（没有则从 skills 复制）
2. Write 工具 → 写入业务脚本 create_xxx_dashboard.py（项目根目录）
3. Bash 工具 → cd {后端项目根目录} && python create_xxx_dashboard.py
4. Bash 工具 → rm create_xxx_dashboard.py（清理临时脚本）
```

**仪表盘创建示例：**
```python
import sys
sys.path.insert(0, r'{后端项目根目录}')
from bi_utils import *

init_api('https://api3.boot.jeecg.com', 'your-token')

# 创建仪表盘（style='default'，栅格坐标）
page_id = create_page('运营数据看板', style='default', theme='default')

# 第一行：4 个数字卡片（w=6×4=24，h=17）
add_number(page_id, '总用户数', x=0, y=0, w=6, h=17, value=15890, suffix='人')
add_number(page_id, '今日活跃', x=6, y=0, w=6, h=17, value=3256, suffix='人')
add_number(page_id, '今日收入', x=12, y=0, w=6, h=17, value=89600, prefix='¥')
add_number(page_id, '转化率', x=18, y=0, w=6, h=17, value=23.5, suffix='%')

# 第二行：折线图 + 饼图
add_chart(page_id, 'JLine', '用户增长趋势', x=0, y=17, w=14, h=35,
          categories=['周一','周二','周三','周四','周五','周六','周日'],
          series=[{'name':'新增用户', 'data':[120,200,150,80,70,110,130]}])

add_chart(page_id, 'JPie', '用户来源', x=14, y=17, w=10, h=35,
          pie_data=[
              {'name':'微信','value':40},
              {'name':'APP','value':30},
              {'name':'网页','value':20},
              {'name':'其他','value':10},
          ])

save_page(page_id)
print(f'仪表盘创建成功！ID: {page_id}')
```

**仪表盘样式特点（bi_utils.py 自动应用）：**
- 背景：白色 `#FFFFFF`
- 边框：浅灰 `#E8E8E8`
- 标题颜色：深灰 `#464646`
- 轴标签：`#909198`
- 网格线：`#F3F3F3`
- 卡片头：白色背景 + 深灰粗体标题（`headColor: '#FFFFFF'`）
- 图例：深灰色文字

## 仪表盘标题规则（重要）

### 图表组件：card.title 留空，用 option.title 显示

根据真实模板验证，**图表组件**（JBar/JLine/JPie/JRing 等）在仪表盘模式下 `card.title` 应为空字符串，标题通过 ECharts `option.title.text` 显示。如果两者都设置，标题会重复出现（卡片头一次 + 图表内部一次）。

`bi_utils.py` 的 `add_chart()` 已自动处理：调用 `_make_card(mode, '')` 传入空标题。

**JNumber 等非图表组件**可以使用 `card.title` 显示标题。

### 大屏 vs 仪表盘标题对比

| 特征 | 大屏（bigScreen） | 仪表盘（default） |
|------|-------------------|-------------------|
| 图表标题 | `option.title.text`（ECharts 内部） | `option.title.text`（ECharts 内部） |
| card.title（图表） | 必须为空 `''` | 必须为空 `''`（避免重复） |
| card.title（JNumber等） | 为空 `''` | 可填标题 |
| 页面主标题 | JText 组件（fontSize 40+） | 不需要 |

### JText 正确的 config 格式

如果仪表盘中需要使用 JText（少见），config 结构为：
```python
config = {
    'dataType': 1,
    'chartData': {'value': '显示文本'},  # dict 格式，不是字符串
    'option': {
        'body': {
            'color': '#464646',
            'fontSize': 16,
            'fontWeight': 'normal',
            'letterSpacing': 0,
            'text': '',
            'marginTop': 0,
            'marginLeft': 0,
        },
        'textAlign': 'left',
        'card': {'title': '', ...},
    },
}
```

**手动构建组件（用于高级定制，需直接操作 config）：**

当 `add_chart` 等快捷函数无法满足需求时（如需要多系列 chartData、自定义 customColor），可直接构建组件 config：

```python
import json, time, random
import bi_utils

def _key():
    return f'{int(time.time()*1000)}_{random.randint(100000,999999)}'

# 仪表盘亮色主题通用样式
CARD = {
    'size': 'default',
    'headColor': '#FFFFFF',
    'textStyle': {'color': '#464646', 'fontSize': 16, 'fontWeight': 'bold'},
    'extra': '', 'rightHref': ''
}

# 直接构建折线图组件
line_data = [
    {'name': '1月', 'value': 120, 'type': '新增'},
    {'name': '1月', 'value': 80, 'type': '流失'},
    # ...
]
comp = {
    'component': 'JLine',
    'x': 0, 'y': 17, 'w': 14, 'h': 35,
    'i': _key(),
    'config': json.dumps({
        'dataType': 1,
        'chartData': json.dumps(line_data, ensure_ascii=False),
        'background': '#FFFFFF',
        'borderColor': '#E8E8E8',
        'size': {'width': 700, 'height': 375},
        'option': {
            'customColor': [
                {'color': '#1890FF', 'color1': '#1890FF'},
                {'color': '#52C41A', 'color1': '#52C41A'},
            ],
            'title': {'show': True, 'text': '用户变化趋势',
                      'textStyle': {'color': '#464646'}},
            'tooltip': {'show': True},
            'legend': {'show': True, 'textStyle': {'fontSize': 12}},
            'xAxis': {
                'type': 'category',
                'axisLabel': {'color': '#909198'},
                'axisLine': {'lineStyle': {'color': '#F3F3F3'}},
            },
            'yAxis': {
                'axisLabel': {'color': '#909198'},
                'splitLine': {'lineStyle': {'color': '#F3F3F3'}},
            },
            'grid': {'top': 70, 'left': 60, 'right': 30, 'bottom': 40},
            'card': {**CARD, 'title': '用户变化趋势'},
        }
    }, ensure_ascii=False)
}
bi_utils._page_components[page_id].append(comp)
```

### Step 4: 输出结果

```
## 仪表盘创建成功

- 页面ID：{id}
- 页面名称：{name}
- 模式：仪表盘（default）
- 预览地址：{API_BASE}/drag/page/view/{id}
- 组件数量：{count} 个

请在仪表盘设计器中查看：打开 JeecgBoot 后台 → 仪表盘 → 找到该页面
```

---

## 编辑已有仪表盘

```python
from bi_utils import *
init_api('https://api3.boot.jeecg.com', 'your-token')

page = query_page(page_id)
print(page['name'], page['updateCount'])

add_chart(page_id, 'JBar', '新增图表', x=0, y=52, w=12, h=35,
          categories=['A','B','C'], series=[{'name':'值','data':[10,20,30]}])
save_page(page_id)
```

---

## 删除仪表盘

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

**仪表盘样式修改关键规则：**
- 颜色使用色值（`#000000`），不用英文单词
- customColor 格式：`[{color1:'#xxx',color:'#xxx'}]`
- 卡片头样式：`option.card.textStyle.color`、`option.card.headColor`
- 背景色：`config.background`（仪表盘默认 `#FFFFFF`）
- 边框色：`config.borderColor`（仪表盘默认 `#E8E8E8`）

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
        option['series'][0]['itemStyle'] = {'color': '#1890FF'}
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
- `create_page(name, style='default', theme='default')` — 创建仪表盘
- `query_page(page_id)` — 查询页面详情
- `list_pages(style='default')` — 列表查询
- `save_page(page_id)` — 保存设计
- `delete_page(page_id, physical)` — 删除
- `recover_page(page_id)` — 恢复
- `copy_page(page_id)` — 复制

**添加组件（栅格坐标）：**
- `add_number(page_id, title, x, y, w, h, value, prefix, suffix)` — 数字指标
- `add_chart(page_id, chart_type, title, x, y, w, h, categories, series, pie_data)` — 图表
- `add_table(page_id, title, x, y, w, h, columns, data)` — 数据表格
- `add_scroll_table(page_id, title, x, y, w, h, columns, data)` — 滚动表格
- `add_ranking(page_id, title, x, y, w, h, data)` — 排行榜
- `add_text(page_id, title, x, y, w, h, content, font_size, color)` — 文本
- `add_image(page_id, title, x, y, w, h, src)` — 图片
- `add_gauge(page_id, title, x, y, w, h, value, max_val, unit, color)` — 仪表盘表盘
- `add_liquid(page_id, title, x, y, w, h, value, color)` — 水球图
- `add_component(page_id, component, title, x, y, w, h, config)` — 通用组件

---

## API 踩坑记录

| 问题 | 说明 |
|------|------|
| `POST /drag/page/add` 返回值 | 返回完整实体含 ID |
| `POST /drag/page/edit` 乐观锁 | 必须传 `updateCount` |
| Windows curl 中文问题 | 必须用 Python urllib/requests |
| 坐标单位 | 仪表盘用**栅格**坐标（24列） |
| 组件 config 分离 | config 存在 onl_drag_page_comp 表 |
| **size 字段必须是像素** | `config.size.width/height` 是像素值，不是栅格单位。仪表盘栅格转像素：`width = w * 75`, `height = h * 11`。如果直接传栅格值，图表会缩成一小团 |
| **chartData 必须是 JSON 字符串** | `config.chartData` 的值必须是 `json.dumps(...)` 后的字符串，不能是原生 list/dict，否则图表不渲染或显示异常 |
| **图表标题去重** | 图表组件（JBar/JLine/JPie 等）的 `option.card.title` 应为空字符串，标题仅通过 `option.title.text` 显示；否则卡片头和图表内部会重复显示标题 |
| **多系列 chartData 格式** | 多系列图表的 chartData 需要 `type` 字段区分系列：`[{"name":"1月","value":10,"type":"系列A"}, {"name":"1月","value":20,"type":"系列B"}]` |
| **HTTPS 连接问题** | api3.boot.jeecg.com 使用 HTTP 协议（非 HTTPS），`init_api` 时用 `http://` 前缀 |

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401） | 重新获取 X-Access-Token |
| `updateCount` 不匹配 | 重新查询页面获取最新值 |
| 组件不显示 | 检查 dataType、chartData（必须是 JSON 字符串）、option 是否完整 |
| 图表缩成小点 | 检查 `config.size` 是否用了像素值（不是栅格单位），仪表盘需 `w*75` / `h*11` |
| 标题重复显示 | 图表组件的 `option.card.title` 设为空，仅用 `option.title.text` |
| 布局错乱 | 确认使用栅格坐标（不是像素），w 总和 ≤ 24 |
| 中文乱码 | 使用 Python（不要用 curl） |

## 参考文档

- `references/bi-component-types.md` — 完整组件类型清单
- `references/bi-comp-option-config.md` — 组件样式配置路径
- `references/bi_utils.py` — 工具库源码
- `references/templates/default/` — 41 个仪表盘模板 JSON 参考
