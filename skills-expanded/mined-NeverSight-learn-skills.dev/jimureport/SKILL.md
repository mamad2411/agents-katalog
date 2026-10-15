---
name: jimureport
description: Use when user asks to create/edit JiMu reports (积木报表), visual Excel-style reports, or says "创建积木报表", "积木报表", "jmreport", "做一个可视化报表", "Excel报表", "数据填报", "积木设计器", "create jimureport", "visual report". Also triggers when user describes report requirements involving Excel-like layouts, data binding with #{}, or multi-sheet reports. Supports generating reports from screenshots — when user provides a screenshot/image of a report and asks to reproduce it (e.g., "按照截图生成报表", "照着这个图片做报表", "根据截图创建报表", "generate report from screenshot", "recreate this report").
---

# JeecgBoot 积木报表 (JiMu Report) AI 自动生成器

将自然语言的报表需求描述转换为积木报表配置，并通过 API 在 JeecgBoot 系统中自动创建/编辑报表。

> **重要：本 skill 处理「积木报表」（可视化 Excel 风格报表设计器），不涉及「Online 报表」（SQL 驱动的 cgreport）或「Online 表单」（cgform）。**

## 与 Online 报表的区别

| 特性 | 积木报表 (jimureport) | Online 报表 (cgreport) |
|------|----------------------|----------------------|
| 设计方式 | 可视化 Excel 设计器 | 配置式（字段列表） |
| 布局能力 | 自由布局、合并单元格、多sheet | 固定表格列 |
| 数据绑定 | `#{数据集编码.字段名}` | 自动列映射 |
| 填报功能 | 支持（submitForm=1） | 不支持 |
| 打印配置 | 精细控制（纸张/边距/方向） | 基础打印 |
| 增强能力 | CSS/JS/Python 增强 | 无 |

## 前置条件

用户必须提供以下信息（或由 AI 引导确认）：

1. **API 地址**：JeecgBoot 后端地址（如 `https://boot3.jeecg.com/jeecgboot`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

如果用户未提供，提示：
> 请提供 JeecgBoot 后端地址和 X-Access-Token（从浏览器 F12 → Network → 任意请求的 Request Headers 中复制）。

## 接口签名机制

部分接口标记了 `@JimuSignature` 注解，调用时必须在 Header 中携带 `X-Sign` 和 `X-TIMESTAMP`，否则返回 `code: 1001` 签名校验失败。

**需要签名的接口：** `queryFieldBySql`、`executeSelectApi`、`loadTableData`、`testConnection`、`download/image`、`dictCodeSearch`、`getDataSourceByPage`、`getDataSourceById`

**不需要签名的接口：** `save`、`saveDb`、`get/{id}`、`field/tree/{reportId}`、`loadDbData/{dbId}`

### 签名算法

```
1. 收集所有请求参数（URL query + POST body）
2. 所有值转为字符串（数字→str, 布尔→"true"/"false", 对象→JSON字符串）
3. 按 key 字母升序排序
4. 转为紧凑 JSON 字符串（无空格）: json.dumps(sorted_dict, separators=(',', ':'))
5. 拼接密钥: jsonStr + "dd05f1c54d63749eda95f9fa6d49v442a"
6. MD5 并转大写: hashlib.md5(拼接结果.encode()).hexdigest().upper()
```

> **默认签名密钥：** `dd05f1c54d63749eda95f9fa6d49v442a`（注意第29位是字母 `v` 不是数字 `4`）
> 可通过 `jeecg.signatureSecret` 配置覆盖。
> **时间戳有效期：5 分钟。**

详细文档见 `references/signature.md`。

更多参考文档：
- `references/template-analysis.md` - 模板报表分析（46个模板结构、displayConfig条码、循环报表）
- `references/components.md` - 组件配置（图表、图片、条码、二维码）
- `references/chart-templates.md` - 图表模板与ECharts配置
- `references/chart-config.md` - 图表配置详解

## 交互流程

### Step 0: 判断操作类型

| 用户意图关键词 | 操作类型 |
|---------------|---------|
| 创建/新建/做一个积木报表 | **新增报表** → Step 1 |
| 修改积木报表/改字段/加数据集/加查询条件 | **编辑报表** → 需要报表ID，走编辑流程 |

**编辑报表流程：**
1. `GET /jmreport/field/tree/{reportId}` → 获取所有数据集的 `dbCode` 和 `dbId`
2. `GET /jmreport/loadDbData/{dbId}?reportId={reportId}` → 获取数据集详情（含 fieldList）
3. `POST /jmreport/saveDb`（**传 id = 更新**，不传 id = 新增）→ 更新 SQL / 参数
4. `GET /jmreport/get/{reportId}` → 获取当前 jsonStr
5. 修改 jsonStr 内容后，`POST /jmreport/save` → 保存报表设计

详见 `references/dataset-skills.md` 中的"查询已有数据集"章节。

### Step 1: 解析需求

从用户描述中提取：

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 报表名称 (name) | 用户指定 | "销售统计报表" |
| SQL 语句 | 从需求推导或用户提供 | `SELECT ... FROM ...` |
| 数据源 (dbSource) | 空（默认数据源） | `second_db` |
| 是否分页 (isPage) | "1" | "0"=不分页 |
| 是否填报 (submitForm) | 0 | 1=填报模式 |

### Step 2: 调用 SQL 解析接口获取字段

**POST** `/jmreport/queryFieldBySql`

```json
{
    "sql": "select * from demo",
    "dbSource": "",
    "type": "0"
}
```

**返回结构：**
```json
{
    "success": true,
    "result": {
        "paramList": [],
        "fieldList": [
            {
                "fieldName": "id",
                "fieldText": "id",
                "widgetType": "String",
                "orderNum": 1
            }
        ]
    }
}
```

### Step 3: 调用数据集保存接口

**POST** `/jmreport/saveDb`

```json
{
    "izSharedSource": 0,
    "jimuReportId": "报表ID",
    "dbCode": "数据集编码",
    "dbChName": "数据集中文名",
    "dbType": "0",
    "dbSource": "",
    "jsonData": "",
    "apiConvert": "",
    "isList": "1",
    "isPage": "1",
    "dbDynSql": "SQL语句",
    "fieldList": [],
    "paramList": []
}
```

**关键字段说明：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `jimuReportId` | 关联的报表ID | `"1193766682428530688"` |
| `dbCode` | 数据集编码，在jsonStr中通过 `#{dbCode.fieldName}` 引用 | `"sales"` |
| `dbChName` | 数据集中文名称 | `"销售数据"` |
| `dbType` | 数据源类型："0"=SQL, "1"=API, "2"=JavaBean, "3"=JSON, "4"=共享, "5"=多文件, "6"=单文件 | `"0"` |
| `dbSource` | 数据源标识，空=默认 | `""` |
| `isList` | "1"=列表数据 | `"1"` |
| `isPage` | "1"=分页 | `"1"` |
| `dbDynSql` | SQL语句 | `"select * from demo"` |

**fieldList 每个字段的结构：**
```json
{
    "fieldName": "id",
    "fieldText": "id",
    "widgetType": "String",
    "orderNum": 0,
    "tableIndex": 0,
    "extJson": "",
    "dictCode": ""
}
```

### Step 4: 构造报表 jsonStr

`jsonStr` 是积木报表的核心设计数据，定义了 Excel 风格的布局。

#### 4.1 jsonStr 完整结构

```json
{
    "loopBlockList": [],
    "querySetting": {
        "izOpenQueryBar": false,
        "izDefaultQuery": true
    },
    "recordSubTableOrCollection": { "group": [], "record": [], "range": [] },
    "printConfig": {
        "paper": "A4",
        "width": 210,
        "height": 297,
        "definition": 1,
        "isBackend": false,
        "marginX": 10,
        "marginY": 10,
        "layout": "portrait",
        "printCallBackUrl": ""
    },
    "hidden": { "rows": [], "cols": [], "conditions": { "rows": {}, "cols": {} } },
    "queryFormSetting": { "useQueryForm": false, "dbKey": "", "idField": "" },
    "dbexps": [],
    "dicts": [],
    "fillFormToolbar": {
        "show": true,
        "btnList": ["save","subTable_add","verify","subTable_del","print","close","first","prev","next","paging","total","last","exportPDF","exportExcel","exportWord"]
    },
    "freeze": "A1",
    "dataRectWidth": 700,
    "isViewContentHorizontalCenter": false,
    "autofilter": {},
    "validations": [],
    "cols": { "len": 100 },
    "area": { "sri": 0, "sci": 0, "eri": 0, "eci": 0, "width": 100, "height": 25 },
    "pyGroupEngine": false,
    "submitHandlers": [],
    "hiddenCells": [],
    "zonedEditionList": [],
    "rows": {
        "1": {
            "cells": {
                "1": { "text": "表头1", "style": 4 },
                "2": { "text": "表头2", "style": 4 }
            },
            "height": 34
        },
        "2": {
            "cells": {    "name": "sheet1",

                "1": { "text": "#{数据集编码.字段1}", "style": 2 },
                "2": { "text": "#{数据集编码.字段2}", "style": 2 }
            }
        },
        "len": 200
    },
    "rpbar": { "show": true, "pageSize": "", "btnList": [] },
    "fixedPrintHeadRows": [],
    "fixedPrintTailRows": [],
    "displayConfig": {},
    "fillFormInfo": { "layout": { "direction": "horizontal", "width": 200, "height": 45 } },
    "background": false,
    "styles": [],
    "fillFormStyle": "default",
    "freezeLineColor": "rgb(185, 185, 185)",
    "merges": []
}
```

#### 4.2 行列数据 (rows)

行和列的索引从 **1** 开始（0行通常为空）。

```json
"rows": {
    "1": {
        "cells": {
            "1": { "text": "ID", "style": 4 },
            "2": { "text": "名称", "style": 4 },
            "3": { "text": "金额", "style": 4 }
        },
        "height": 34
    },
    "2": {
        "cells": {
            "1": { "text": "#{ds.id}", "style": 2 },
            "2": { "text": "#{ds.name}", "style": 2 },
            "3": { "text": "#{ds.amount}", "style": 2 }
        }
    },
    "len": 200
}
```

- **第1行**：表头行（通常用 style 4，蓝底白字）
- **第2行**：数据绑定行（用 `#{数据集编码.字段名}` 语法）
- `height`：行高（像素）
- `len`：总行数（默认200）

#### 4.3 数据绑定语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `#{dbCode.fieldName}` | 普通字段绑定 | `#{sales.amount}` |
| `=SUM(#{dbCode.fieldName})` | 聚合函数 | `=SUM(#{sales.amount})` |
| `=COUNT(#{dbCode.fieldName})` | 计数 | `=COUNT(#{sales.id})` |

#### 4.4 样式 (styles)

样式数组，通过索引在 cells 中引用：

```json
"styles": [
    {
        "border": { "bottom": ["thin","#000"], "top": ["thin","#000"], "left": ["thin","#000"], "right": ["thin","#000"] }
    },
    {
        "border": { "bottom": ["thin","#000"], "top": ["thin","#000"], "left": ["thin","#000"], "right": ["thin","#000"] },
        "align": "center"
    },
    {
        "border": { "bottom": ["thin","#000"], "top": ["thin","#000"], "left": ["thin","#000"], "right": ["thin","#000"] },
        "align": "center",
        "valign": "middle"
    },
    {
        "border": { "bottom": ["thin","#000"], "top": ["thin","#000"], "left": ["thin","#000"], "right": ["thin","#000"] },
        "align": "center",
        "valign": "middle",
        "bgcolor": "#01b0f1"
    },
    {
        "border": { "bottom": ["thin","#000"], "top": ["thin","#000"], "left": ["thin","#000"], "right": ["thin","#000"] },
        "align": "center",
        "valign": "middle",
        "bgcolor": "#01b0f1",
        "color": "#ffffff"
    }
]
```

**常用样式索引：**

| 索引 | 效果 | 用途 |
|------|------|------|
| 0 | 边框 | 基础单元格 |
| 1 | 边框+居中 | 文本居中 |
| 2 | 边框+居中+垂直居中 | 数据行 |
| 3 | 边框+居中+垂直居中+蓝底 | 表头（无白字） |
| 4 | 边框+居中+垂直居中+蓝底白字 | 表头（推荐） |

#### 4.5 单元格合并 (merges)

```json
"merges": [
    "B1:F1"
]
```
格式为 Excel 风格的范围表示，如 `B1:F1` 表示合并 B1 到 F1。

#### 4.6 打印配置 (printConfig)

| 属性 | 说明 | 可选值 |
|------|------|--------|
| paper | 纸张大小 | "A4", "A3", "B5", "letter" |
| width/height | 纸张宽高(mm) | A4: 210×297 |
| layout | 方向 | "portrait"(纵向), "landscape"(横向) |
| marginX/marginY | 边距(mm) | 默认10 |
| isBackend | 后端打印 | true/false |

#### 4.7 查询条件 (querySetting)

```json
"querySetting": {
    "izOpenQueryBar": true,
    "izDefaultQuery": true
}
```

- `izOpenQueryBar`: 是否显示查询栏
- `izDefaultQuery`: 是否默认查询

### Step 5: 调用报表保存接口

**POST** `/jmreport/save`

> **关键格式要求：**
> 1. `designerObj` 是 **JSON 字符串**（不是对象）
> 2. 所有 jsonStr 字段（`rows`、`cols`、`styles`、`merges`、`chartList` 等）都放在请求体**顶层**，每个值都是 **JSON 字符串**（不是对象）
> 3. 必须包含 `sheetId`、`sheetName`、`sheetOrder` 字段
> 4. 后端 `saveReport` 逻辑：`json.remove("designerObj")` 后，剩余的顶层 JSON 直接作为 jsonStr 存入数据库

**请求体结构（只有 designerObj 是字符串，其他都是原始对象）：**

```json
{
    "designerObj": "{\"id\":\"报表ID\",\"name\":\"报表名称\",\"type\":\"0\",\"template\":0,\"delFlag\":0,\"submitForm\":0,\"reportName\":\"报表名称\"}",
    "name": "sheet1",
    "freeze": "A1",
    "freezeLineColor": "rgb(185, 185, 185)",
    "rows": {"1": {"cells": {"1": {"text": "表头", "style": 4}}, "height": 34}, "len": 200},
    "cols": {"len": 100},
    "styles": [],
    "merges": [],
    "validations": [],
    "autofilter": {},
    "dbexps": [],
    "dicts": [],
    "loopBlockList": [],
    "zonedEditionList": [],
    "fixedPrintHeadRows": [],
    "fixedPrintTailRows": [],
    "rpbar": {"show": true, "pageSize": "", "btnList": []},
    "fillFormToolbar": {"show": true, "btnList": ["save","subTable_add","verify","subTable_del","print","close","first","prev","next","paging","total","last","exportPDF","exportExcel","exportWord"]},
    "hiddenCells": [],
    "hidden": {"rows": [], "cols": [], "conditions": {"rows": {}, "cols": {}}},
    "fillFormInfo": {"layout": {"direction": "horizontal", "width": 200, "height": 45}},
    "recordSubTableOrCollection": {"group": [], "record": [], "range": []},
    "displayConfig": {},
    "printConfig": {"paper": "A4", "width": 210, "height": 297, "definition": 1, "isBackend": false, "marginX": 10, "marginY": 10, "layout": "portrait", "printCallBackUrl": ""},
    "querySetting": {"izOpenQueryBar": false, "izDefaultQuery": true},
    "queryFormSetting": {"useQueryForm": false, "dbKey": "", "idField": ""},
    "area": {"sri": 0, "sci": 0, "eri": 0, "eci": 0, "width": 100, "height": 25},
    "submitHandlers": [],
    "chartList": [],
    "background": false,
    "dataRectWidth": 700,
    "excel_config_id": "报表ID",
    "pyGroupEngine": false,
    "isViewContentHorizontalCenter": false,
    "fillFormStyle": "default",
    "sheetId": "default",
    "sheetName": "默认Sheet",
    "sheetOrder": "0"
}
```

**Python 构造示例：**

```python
save_data = {
    # 只有 designerObj 是字符串
    "designerObj": json.dumps(designer_obj, ensure_ascii=False),
    # 其他所有字段都是原始对象/数组，不要 json.dumps
    "name": "sheet1",
    "freeze": "A1",
    "freezeLineColor": "rgb(185, 185, 185)",
    "rows": rows_data,          # dict, 不是字符串
    "cols": cols_data,           # dict
    "styles": styles_list,       # list
    "merges": merges_list,       # list
    "chartList": chart_list,     # list
    "loopBlockList": [],         # list
    "querySetting": {"izOpenQueryBar": False, "izDefaultQuery": True},  # dict
    # ... 其他配置字段同理
    "sheetId": "default",
    "sheetName": "默认Sheet",
    "sheetOrder": "0",
    "background": False,         # 布尔值
    "dataRectWidth": 700,        # 数字
    "excel_config_id": report_id,
    "pyGroupEngine": False,
    "isViewContentHorizontalCenter": False,
    "fillFormStyle": "default"
}
```

> **关键：只有 `designerObj` 用 `json.dumps()` 转字符串，其他所有字段（`rows`、`cols`、`styles`、`merges`、`chartList`、`loopBlockList` 等）都保持原始 Python 对象。如果把它们也 json.dumps 转成字符串，会导致双重序列化，前端解析报错。**

**designerObj 关键字段（JSON 字符串内的对象结构）：**

| 字段 | 说明 | 必填 |
|------|------|------|
| `id` | 报表唯一ID | 是 |
| `code` | 报表编码（如时间戳格式） | 是 |
| `name` / `reportName` | 报表名称 | 是 |
| `type` | 报表分类，默认 `"0"` | 是 |
| `template` | 是否为模板（0否） | 是 |
| `cssStr` | CSS增强代码 | 否 |
| `jsStr` | JS增强代码 | 否 |
| `pyStr` | Python增强代码 | 否 |
| `tenantId` | 租户ID | 否 |
| `submitForm` | 是否填报（0否，1是） | 否 |

**注意事项：**
- **只有 `designerObj` 是字符串**（`json.dumps(obj)`），其他所有字段保持原始对象/数组
- `rows`、`cols`、`styles`、`chartList`、`loopBlockList` 等都是 **原始对象/数组**，禁止 json.dumps
- `background`、`pyGroupEngine`、`isViewContentHorizontalCenter` 是布尔值 `False`
- `dataRectWidth` 是数字（如 `700`）
- 必须传 `sheetId: "default"`、`sheetName: "默认Sheet"`、`sheetOrder: "0"`

### Step 6: 展示摘要并确认

**必须展示以下内容，等待用户确认后再执行：**

```
## 积木报表配置摘要

- 报表名称：销售统计报表
- 数据源：默认
- 目标环境：https://boot3.jeecg.com/jeecgboot

### 数据集配置
| 编码 | 名称 | SQL | 分页 |
|------|------|-----|------|
| sales | 销售数据 | SELECT id, name, amount FROM biz_sales | 是 |

### 表头设计
| 列 | 表头文本 | 数据绑定 |
|----|---------|---------|
| B | ID | #{sales.id} |
| C | 名称 | #{sales.name} |
| D | 金额 | #{sales.amount} |

确认以上配置？(y/n)
```

### Step 7: 使用 Python 调用 API

**重要限制：**
1. **Windows 环境下 curl 发送中文/长 JSON 会出错**，必须使用 Python
2. **禁止使用 `python3 -c "..."` 内联方式**
3. **必须先用 Write 工具写入 `.py` 临时文件，再用 Bash 执行，最后删除临时文件**

**完整 Python 脚本模板：**

```python
import urllib.request
import json
import time
import random
import ssl
import hashlib

API_BASE = '{用户提供的后端地址}'
TOKEN = '{用户提供的 X-Access-Token}'
SIGNATURE_SECRET = 'dd05f1c54d63749eda95f9fa6d49v442a'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 需要签名的接口列表
SIGNED_ENDPOINTS = [
    '/jmreport/queryFieldBySql',
    '/jmreport/executeSelectApi',
    '/jmreport/loadTableData',
    '/jmreport/testConnection',
    '/jmreport/download/image',
    '/jmreport/dictCodeSearch',
    '/jmreport/getDataSourceByPage',
    '/jmreport/getDataSourceById',
]

def compute_sign(params_dict):
    """计算积木报表接口签名"""
    str_params = {}
    for k, v in params_dict.items():
        if v is None:
            continue
        if isinstance(v, bool):
            str_params[k] = str(v).lower()
        elif isinstance(v, (int, float)):
            str_params[k] = str(v)
        elif isinstance(v, (dict, list)):
            str_params[k] = json.dumps(v, ensure_ascii=False, separators=(',', ':'))
        else:
            str_params[k] = str(v)
    sorted_params = dict(sorted(str_params.items()))
    params_json = json.dumps(sorted_params, ensure_ascii=False, separators=(',', ':'))
    sign_str = params_json + SIGNATURE_SECRET
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

def api_request(path, data=None, method=None):
    url = f'{API_BASE}{path}'
    headers = {
        'X-Access-Token': TOKEN,
        'Content-Type': 'application/json; charset=UTF-8'
    }
    # 自动判断是否需要签名
    need_sign = any(path.rstrip('/').endswith(ep.rstrip('/')) for ep in SIGNED_ENDPOINTS)
    if need_sign:
        sign_params = data if data else {}
        headers['X-TIMESTAMP'] = str(int(time.time() * 1000))
        headers['X-Sign'] = compute_sign(sign_params)
    if data is not None:
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(url, data=json_data, headers=headers, method=method or 'POST')
    else:
        req = urllib.request.Request(url, headers=headers, method=method or 'GET')
    resp = urllib.request.urlopen(req, context=ctx)
    return json.loads(resp.read().decode('utf-8'))

def gen_id():
    return str(int(time.time() * 1000) * 1000000 + random.randint(100000, 999999))

# ====== Step 1: 解析SQL获取字段 ======
parse_result = api_request('/jmreport/queryFieldBySql', {
    "sql": "select * from demo",
    "dbSource": "",
    "type": "0"
})
print('SQL解析结果:', json.dumps(parse_result, ensure_ascii=False, indent=2))

# ====== Step 2: 保存数据集 ======
db_data = {
    "izSharedSource": 0,
    "jimuReportId": "报表ID",
    "dbCode": "demo",
    "dbChName": "示例数据",
    "dbType": "0",
    "dbSource": "",
    "jsonData": "",
    "apiConvert": "",
    "isList": "1",
    "isPage": "1",
    "dbDynSql": "select * from demo",
    "fieldList": parse_result['result']['fieldList'],
    "paramList": []
}
db_result = api_request('/jmreport/saveDb', db_data)
print('数据集保存结果:', json.dumps(db_result, ensure_ascii=False, indent=2))

# ====== Step 3: 构造请求体并保存报表 ======
# 关键: designerObj 是字符串, 所有 jsonStr 字段也是字符串
# 后端逻辑: json.remove("designerObj") 后, 剩余的顶层字段就是 jsonStr

designer_obj = {
    "id": report_id, "name": "报表名称", "type": "0",
    "template": 0, "delFlag": 0, "viewCount": 0, "updateCount": 0,
    "submitForm": 0, "reportName": "报表名称"
}

rows_data = {
    "1": {"cells": {"1": {"text": "ID", "style": 4}, "2": {"text": "名称", "style": 4}}, "height": 34},
    "2": {"cells": {"1": {"text": "#{demo.id}", "style": 2}, "2": {"text": "#{demo.name}", "style": 2}}},
    "len": 200
}

styles_list = [
    {"border": {"bottom": ["thin", "#000"], "top": ["thin", "#000"], "left": ["thin", "#000"], "right": ["thin", "#000"]}},
    {"border": {"bottom": ["thin", "#000"], "top": ["thin", "#000"], "left": ["thin", "#000"], "right": ["thin", "#000"]}, "align": "center"},
    {"border": {"bottom": ["thin", "#000"], "top": ["thin", "#000"], "left": ["thin", "#000"], "right": ["thin", "#000"]}, "align": "center", "valign": "middle"},
    {"border": {"bottom": ["thin", "#000"], "top": ["thin", "#000"], "left": ["thin", "#000"], "right": ["thin", "#000"]}, "align": "center", "valign": "middle", "bgcolor": "#01b0f1"},
    {"border": {"bottom": ["thin", "#000"], "top": ["thin", "#000"], "left": ["thin", "#000"], "right": ["thin", "#000"]}, "align": "center", "valign": "middle", "bgcolor": "#01b0f1", "color": "#ffffff"}
]

# 所有对象/数组字段用 json.dumps 转为字符串
save_data = {
    "designerObj": json.dumps(designer_obj, ensure_ascii=False),
    "name": "sheet1",
    "freeze": "A1",
    "freezeLineColor": "rgb(185, 185, 185)",
    "rows": json.dumps(rows_data, ensure_ascii=False),
    "cols": json.dumps({"len": 100}, ensure_ascii=False),
    "styles": json.dumps(styles_list, ensure_ascii=False),
    "merges": json.dumps([], ensure_ascii=False),
    "validations": "[]",
    "autofilter": "{}",
    "dbexps": "[]",
    "dicts": "[]",
    "loopBlockList": "[]",
    "zonedEditionList": "[]",
    "fixedPrintHeadRows": "[]",
    "fixedPrintTailRows": "[]",
    "hiddenCells": "[]",
    "submitHandlers": "[]",
    "rpbar": json.dumps({"show": True, "pageSize": "", "btnList": []}, ensure_ascii=False),
    "fillFormToolbar": json.dumps({"show": True, "btnList": ["save", "subTable_add", "verify", "subTable_del", "print", "close", "first", "prev", "next", "paging", "total", "last", "exportPDF", "exportExcel", "exportWord"]}, ensure_ascii=False),
    "hidden": json.dumps({"rows": [], "cols": [], "conditions": {"rows": {}, "cols": {}}}, ensure_ascii=False),
    "fillFormInfo": json.dumps({"layout": {"direction": "horizontal", "width": 200, "height": 45}}, ensure_ascii=False),
    "recordSubTableOrCollection": json.dumps({"group": [], "record": [], "range": []}, ensure_ascii=False),
    "displayConfig": "{}",
    "printConfig": json.dumps({"paper": "A4", "width": 210, "height": 297, "definition": 1, "isBackend": False, "marginX": 10, "marginY": 10, "layout": "portrait", "printCallBackUrl": ""}, ensure_ascii=False),
    "querySetting": json.dumps({"izOpenQueryBar": False, "izDefaultQuery": True}, ensure_ascii=False),
    "queryFormSetting": json.dumps({"useQueryForm": False, "dbKey": "", "idField": ""}, ensure_ascii=False),
    "area": json.dumps({"sri": 0, "sci": 0, "eri": 0, "eci": 0, "width": 100, "height": 25}, ensure_ascii=False),
    "chartList": "[]",
    "background": "false",
    "dataRectWidth": "700",
    "excel_config_id": report_id,
    "pyGroupEngine": "false",
    "isViewContentHorizontalCenter": "false",
    "fillFormStyle": "default",
    "sheetId": "default",
    "sheetName": "默认Sheet",
    "sheetOrder": "0"
}
save_result = api_request('/jmreport/save', save_data)
print('报表保存结果:', json.dumps(save_result, ensure_ascii=False, indent=2))
```

## 典型工作流总结

```
1. save (空报表)     →  先创建空报表，获取报表ID
2. queryFieldBySql   →  解析SQL，获取字段列表
3. saveDb            →  保存数据集（含字段映射、分页配置），关联报表ID
4. save (完整设计)   →  jsonStr内容放请求体顶层，保存完整报表设计
```

**关键注意事项：**
- Step 1 创建空报表时，`save` 接口首次调用会返回 `isRefresh: true`，此时报表已创建
- Step 4 的 `save` 请求体格式：`designerObj`（元数据）+ jsonStr 内容（rows/cols/styles 等）放在**同一层级**
- 禁止将 jsonStr 嵌套在 `designerObj.jsonStr` 字符串中，否则后端会清空 rows 数据
- `designerObj.type` 默认值为 `"0"`，不要传分类名称字符串（如 "demo"）

## 智能字段配置

### 字段显示名称推导

| 字段名模式 | 推导中文名 |
|-----------|-----------|
| id | ID/主键 |
| name / title | 名称/标题 |
| code / no | 编码/编号 |
| status | 状态 |
| amount / money / price / salary | 金额/费用/价格/薪资 |
| count / qty / num / age | 数量/年龄 |
| date / time / birthday | 日期/时间/生日 |
| create_by / update_by | 创建人/更新人 |
| create_time / update_time | 创建时间/更新时间 |
| sex | 性别 |
| email | 邮箱 |
| phone / mobile / tel | 电话/手机号 |
| content / remark | 内容/备注 |
| sys_org_code | 组织编码 |
| tenant_id | 租户ID |

### 是否在报表中显示

| 规则 | 是否显示 |
|------|---------|
| 业务字段（默认） | 显示 |
| id / 主键字段 | 通常隐藏 |
| create_by / update_by | 通常隐藏 |
| sys_org_code / tenant_id | 隐藏 |

## 高级功能

### SQL 参数化与动态条件

积木报表支持在SQL中使用参数和FreeMarker动态条件：

```sql
-- 基础参数
SELECT * FROM demo WHERE name like '%${name}%'

-- FreeMarker动态条件（参数为空时自动跳过）
select * from demo where 1=1
<#if isNotEmpty(name)> and name = '${name}'</#if>
<#if isNotEmpty(age)> and age = '${age}'</#if>

-- IN查询（v1.6.2+）
select * from demo where sex in(${DaoFormat.in('${sex}')})
select * from demo where age in(${DaoFormat.inNumber('${age}')})
```

### 查询配置

报表支持丰富的查询控件（文本、下拉单选/多选、范围、模糊、下拉树），详见 `references/query-config.md`。

关键配置点：
- **querySetting**：`izOpenQueryBar`(展开查询栏) / `izDefaultQuery`(自动查询)
- **控件默认值**：静态值 / `=dateStr('yyyy-MM-dd')` / `#{sysUserCode}`
- **JS增强**：级联下拉 `updateSelectOptions()` / 监听变化 `onSearchFormChange()`
- **参数优先级**：查询条件值 > URL参数 > 默认值

### 分组报表（纵向分组）

当用户要求"分组报表"、"按XX分组"、"按XX统计"时，必须使用分组语法，**不要**用普通的汇总SQL+明细SQL拆分方式。

#### 核心配置（3个必须项）

1. **jsonStr 顶层**添加分组标记：
```json
{
    "isGroup": true,
    "groupField": "数据集编码.分组字段名"
}
```

2. **save 请求体**中也要传这两个字段（与 rows/cols 同级）：
```python
save_data = {
    ...
    "isGroup": True,
    "groupField": "users.sex_name",
    ...
}
```

3. **分组列单元格**使用 `#{db.group(field)}` 语法，并配置聚合属性：
```json
{
    "text": "#{users.group(sex_name)}",
    "aggregate": "group",
    "subtotal": "groupField",
    "funcname": "-1",
    "subtotalText": "合计"
}
```

#### 分组单元格属性

| 属性 | 值 | 说明 |
|------|-----|------|
| `text` | `#{dbCode.group(fieldName)}` | 分组绑定，相同值自动合并单元格 |
| `aggregate` | `"group"` | 标记为分组聚合列 |
| `subtotal` | `"groupField"` | 启用小计/合计行 |
| `funcname` | `"-1"` / `"SUM"` / `"COUNT"` / `"AVG"` | 聚合函数，`"-1"`=不计算 |
| `subtotalText` | `"合计"` / `"小计"` | 小计行显示的文本 |

#### 多级分组

从左到右为高到低级别，每级用不同的 `subtotalText` 区分：
- 一级分组（如起始站）：`subtotalText: "合计"` — 一级分组切换时显示
- 二级分组（如终止站）：`subtotalText: "小计"` — 二级分组切换时显示
- `groupField` 始终指向**一级（最高级）分组字段**

**多级分组示例（按起始站+终止站分组）：**
```json
// save 请求体
{
    "isGroup": true,
    "groupField": "jp.kaishi",  // 指向一级分组字段
    ...
}

// 数据绑定行 cells
"1": {
    "text": "#{jp.group(kaishi)}",    // 一级分组
    "aggregate": "group",
    "subtotal": "groupField",
    "funcname": "-1",
    "subtotalText": "合计"
},
"2": {
    "text": "#{jp.group(jieshu)}",    // 二级分组
    "aggregate": "group",
    "subtotal": "groupField",
    "funcname": "-1",
    "subtotalText": "小计"
},
"3": {"text": "#{jp.bnum}"},          // 普通字段
```

#### 分组报表布局示例

```
第1行: 标题（合并单元格）
第2行: 表头（起始站 | 终止站 | 班次号 | 发车时间 | ...）
第3行: 数据绑定行（#{db.group(kaishi)} | #{db.group(jieshu)} | #{db.bnum} | ...）
```

预览效果：
```
┌────────┬────────┬────────┬──────────┐
│ 起始站  │ 终止站  │ 班次号  │ 发车时间  │
├────────┼────────┼────────┼──────────┤
│        │        │ K7725  │ 21:13    │
│        │ 邯郸   ├────────┼──────────┤
│ 北京西  │        │        小计       │
│        ├────────┼────────┼──────────┤
│        │ 深圳   │ G101   │ 06:44    │
│        │        │        小计       │
├────────┼────────┼────────┼──────────┤
│        │        │        合计       │
└────────┴────────┴────────┴──────────┘
```

#### 注意事项
- SQL 中必须按分组字段 `ORDER BY`，确保相同值相邻（多级分组时按一级、二级顺序排序）
- 数据集 `isPage` 设为 `"0"`（不分页），否则分组合并可能不完整
- `pyGroupEngine` 保持 `false`（标准分组不需要 Python 引擎）
- 列数较多时（>6列），考虑将 `printConfig.layout` 设为 `"landscape"`（横向打印）
- 完整示例见 `examples/vertical-group-subtotal-example.md`

#### 数据探查

`queryFieldBySql` 只返回字段元数据，不返回实际数据行。当需要了解数据内容以判断分组字段时：
- 优先通过 **pymysql 连接本地数据库**查看实际数据（`SELECT DISTINCT`、`GROUP BY` 等）
- 本地数据库名通常为 `jeecgboot3`（可通过 `SHOW DATABASES LIKE '%jeecg%'` 确认）
- 查看数据后再确定哪些字段适合作为分组依据

### CSS/JS/Python 增强

通过 `designerObj` 的 `cssStr`、`jsStr`、`pyStr` 字段传入增强代码。

### 多 Sheet

设置 `isMultiSheet` 为 1，通过 `sheets` 字段管理多个 sheet 页。

### 填报模式

设置 `submitForm` 为 1，启用数据填报功能，允许用户在报表中录入数据。

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401/认证失败） | 提示用户重新获取 X-Access-Token |
| `code:1001` 签名验证失败 | 接口需要签名，需在 Header 添加 X-Sign 和 X-TIMESTAMP，详见签名机制章节 |
| `签名验证失败:X-TIMESTAMP已过期` | 客户端与服务器时间差超过5分钟，检查系统时间 |
| `签名校验失败，参数有误！` | 签名计算不匹配，检查参数排序、JSON无空格格式、密钥是否正确 |
| SQL 解析失败 | 检查 SQL 语法是否正确，表是否存在 |
| 数据集编码重复 | 换一个 dbCode |
| jsonStr 格式错误 | 检查 JSON 字符串转义是否正确 |
| 中文乱码 | 确认使用 Python urllib（不要用 curl） |

## 与其他 Skill 的区别

| Skill | 产出物 | 适用场景 |
|-------|--------|---------|
| `jeecg-jimureport` | 积木报表（可视化Excel设计器） | 复杂布局报表、合并单元格、打印、填报 |
| `jeecg-onlreport` | Online 报表（SQL 驱动列表） | 简单数据查询报表 |
| `jeecg-onlform` | Online 表单（元数据CRUD） | 数据录入管理 |
| `jeecg-desform` | 设计器表单 JSON | 数据采集、审批表单 |
| `jeecg-codegen` | Java + Vue3 代码 + SQL | 自定义业务逻辑模块 |

## 图表与数据表格布局实战经验

### chart_bottom 布局（表格在上，图表在下）

**核心问题：** 积木报表的数据绑定行在预览时会展开显示多页数据，导致图表位置被推后。

**解决方案：**
1. 图表虚拟单元格需要放在数据展开区域之后
2. 图表开始行 = 数据绑定行 + pageSize + gap
3. 示例：数据绑定行=3, pageSize=10, gap=1 → 图表从第14行开始

```python
# 布局计算公式
page_size = config.get('pageSize', 10)
gap = config.get('gap', 1)  # 默认1行间距，负值可减少间距
data_binding_row = 3  # 标题行(1) + 表头行(2) + 数据绑定行(3)
chart_start = data_binding_row + page_size + gap  # 14
```

### 虚拟单元格行数

**关键发现：** 图表的 `virtualCellRange` 只需要 **1行**（不是多行）。

错误做法（早期版本）：
```python
row_count = (chart_height // 25) + 2  # 300px高度 = 14行
```

正确做法：
```python
row_count = 1  # 只用1行作为锚点，图表大小由width/height控制
```

设计器保存后的实际结构：
- 图表虚拟单元格只有1行
- 图表位置由 `chartList[].row` 和 `chartList[].width/height` 决定

### area 和 dataRectWidth 设置

为确保预览正确显示，需要设置正确的 `area` 和 `dataRectWidth`：

```python
# 计算列宽总和
total_width = sum(col.get('width', 100) for col in cols.values() if isinstance(col, dict))

# area 定义内容边界（告诉前端报表的实际范围）
# 注意：设计器保存后会重新计算 area，建议在图表底部添加2-3行空行来确保滚动正常
area = {
    "sri": 1,           # 起始行（UI行号）
    "sci": 1,           # 起始列
    "eri": chart_start, # 结束行（图表开始的行）
    "eci": col_count,   # 结束列
    "width": total_width,
    "height": title_h + header_h + (chart_start - 3) * row_h + chart_h
}
```

**滚动问题的解决方案（已自动化）：**

脚本已自动处理滚动条问题，无需手动操作：

1. 设置 `area = False`，让系统自动计算滚动高度
2. 在图表底部自动添加分页符行（位置 = chart_start + pageSize + 3）

```python
# 在图表下方添加分页符行（使用空格避免显示"1"）
pagination_row = chart_start + pageSize + 3
all_rows[str(pagination_row)] = {"cells": {"1": {"text": "   "}}}
```

这样系统就能正确识别滚动区域，滚动条自动正常工作。

### 合并单元格行号

**重要：** 合并单元格使用 **UI 行号**（不是代码行号）。

- 代码行号从 0 开始（但 rows 中的 key 从 "1" 开始）
- UI 行号从 1 开始
- 公式：`ui_row = code_row + 1`

示例：
```python
# 标题在代码第1行，合并 C1:H1
ui_row = 1 + 1  # = 2
merges.append(f"C{ui_row}:H{ui_row}")  # "C2:H2"
```

### 预览地址带 Token

报表预览地址需要携带 token 参数：

```
https://api3.boot.jeecg.com/jmreport/view/{report_id}?token={X-Access-Token}
```

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 表格和图表间距过大 | 图表虚拟单元格放在了数据展开区域内 | 图表从 `data_binding_row + pageSize + gap` 开始 |
| 图表与数据重叠 | 虚拟单元格行数过多 | 虚拟单元格只用1行 |
| 设计器与预览效果不一致 | area 设置不正确 | 设置正确的 area.sri/eri |
| 滚动条不显示 | area 范围计算错误 | 确保 area.eri 等于图表实际开始的行 |
| 间距仍偏大 | gap 默认值过大 | 将 gap 改为负值（如 -5）可以减少间距 |
| 滚动幅度太小 | 内容总高度不够 | 在图表底部添加2-3行空行或分页符，增加总高度 |
