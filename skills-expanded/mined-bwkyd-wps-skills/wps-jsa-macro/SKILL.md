---
name: wps-jsa-macro
description: |
  WPS宏代码助手。告诉我你要自动化什么操作，帮你写WPS JSA宏脚本，
  批量改名、自动填表、一键汇总，重复劳动交给宏。注意WPS用的是JavaScript不是VBA。
  用于帮助用户编写WPS宏脚本。当用户提到宏、macro、自动化、批量操作时触发。
  WPS JSA macro generator - automates repetitive tasks in WPS Office.
license: MIT
user-invocable: true
argument-hint: '[操作描述]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: WPS宏代码助手
  description_zh: 编写WPS JSA宏脚本，实现表格和文档的批量自动化操作
  tags:
    - WPS
    - JSA
    - JavaScript
    - 宏
    - 自动化
  version: 1.0.2
  license: MIT
---

# WPS 宏生成器

生成 WPS Office **JSA（JavaScript for Applications）** 宏脚本。

> **核心原则：WPS 宏 ≠ VBA。WPS 使用 JavaScript 语法，API 虽与 VBA 相似但有重要差异。
> 绝对不要输出 VBA 代码。**

## When to Use

- 用户需要在WPS中自动化重复操作
- 用户说"帮我写一个WPS宏"
- 用户需要批量处理WPS文档/表格/演示
- 用户需要在WPS表格中自动填充、计算、格式化
- 用户提到JSA、WPS脚本

## When NOT to Use

- 用户明确说 Excel VBA → 提醒用户WPS不支持VBA，询问是否需要JSA版本
- 用户需要生成独立文档 → 使用 `docx-writer`
- 用户需要公文排版 → 使用 `wps-gongwen`
- 需要的是 WPS 加载项（Add-in）开发 → 这是另一个话题

## JSA vs VBA 关键差异

**必须牢记这些差异，避免生成错误代码：**

| 特性 | VBA | WPS JSA |
|------|-----|---------|
| 语言 | Visual Basic | **JavaScript** |
| 变量声明 | `Dim x As Integer` | `var x = 0` 或 `let x = 0` |
| 函数定义 | `Sub / Function` | `function name()` |
| 字符串连接 | `&` | `+` |
| 注释 | `'` 单引号 | `//` 或 `/* */` |
| 数组索引 | 从1开始 | **从0开始**（但集合类从1开始） |
| 无返回值过程 | `Sub` | `function`（无区分） |
| For Each | `For Each x In col` | `for (var i = 1; i <= col.Count; i++)` |
| 错误处理 | `On Error` | `try...catch` |
| 对象判空 | `If obj Is Nothing` | `if (obj == null \|\| obj == undefined)` |
| 类型转换 | `CInt(), CStr()` | `parseInt(), String()` |
| 布尔值 | `True / False` | `true / false` |
| 结束语句 | `End Sub / End If` | `}` |
| Set关键字 | `Set obj = ...` | 不需要，直接 `var obj = ...` |

## JSA 核心 API 速查

### 全局对象

```javascript
// 应用对象
Application              // WPS应用实例
Application.ActiveDocument  // 当前活动文档（文字）
Application.ActiveWorkbook  // 当前活动工作簿（表格）
Application.ActivePresentation // 当前活动演示

// 控制台输出（调试用）
Console.log("message")   // WPS宏编辑器控制台

// 对话框
Application.alert("消息")  // 类似 MsgBox
```

### WPS 文字（Writer）

```javascript
// 文档操作
var doc = Application.ActiveDocument
var docs = Application.Documents
docs.Open("/path/to/file.docx")
docs.Add()  // 新建文档

// 内容操作
var range = doc.Content           // 全文范围
var paras = doc.Paragraphs        // 段落集合
var para = doc.Paragraphs.Item(1) // 第1段（从1开始）
para.Range.Text                   // 段落文本
para.Range.Font.Name = "宋体"
para.Range.Font.Size = 12
para.Range.Font.Bold = true

// 查找替换
var find = doc.Content.Find
find.Text = "旧文本"
find.Replacement.Text = "新文本"
find.Execute(undefined, undefined, undefined, undefined, undefined,
             undefined, undefined, undefined, undefined, undefined, 2)
// 最后参数 2 = wdReplaceAll

// 表格
var table = doc.Tables.Item(1)
table.Cell(1, 1).Range.Text     // 第1行第1列
table.Rows.Count                // 行数
table.Columns.Count             // 列数

// 书签
var bm = doc.Bookmarks.Item("书签名")
bm.Range.Text = "填入内容"

// 保存
doc.Save()
doc.SaveAs("/path/to/new.docx")
```

### WPS 表格（Spreadsheets）

```javascript
// 工作簿和工作表
var wb = Application.ActiveWorkbook
var ws = wb.ActiveSheet
var ws2 = wb.Sheets.Item("Sheet1")  // 按名称
var ws3 = wb.Sheets.Item(1)         // 按索引（从1开始）

// 单元格操作
var cell = ws.Range("A1")
cell.Value2 = "Hello"               // 设置值（用Value2更可靠）
cell.Formula = "=SUM(B1:B10)"       // 设置公式
cell.Font.Name = "宋体"
cell.Font.Size = 11
cell.Font.Bold = true
cell.Interior.Color = 0xFFFF00      // 背景色（BGR格式）

// 范围操作
var rng = ws.Range("A1:D10")
rng.Value2                          // 返回二维数组
rng.NumberFormat = "#,##0.00"       // 数字格式
rng.HorizontalAlignment = -4108    // xlCenter
rng.Borders.LineStyle = 1          // 边框

// 行列操作
ws.Rows(1).RowHeight = 30
ws.Columns("A").ColumnWidth = 15
ws.Rows("2:5").Delete()

// 遍历（注意：Cells索引从1开始）
var lastRow = ws.Range("A1").End(-4121).Row  // xlDown = -4121
// 或用 UsedRange
var lastRow2 = ws.UsedRange.Rows.Count

for (var i = 1; i <= lastRow; i++) {
    var val = ws.Cells(i, 1).Value2
    // 处理每行数据
}

// 自动筛选
ws.Range("A1:D1").AutoFilter()
ws.Range("A1:D1").AutoFilter(1, "条件值")  // 第1列筛选

// 数据透视表（基础）
// WPS表格数据透视表API与Excel基本一致
```

### WPS 演示（Presentation）

```javascript
// 演示文稿
var ppt = Application.ActivePresentation
var slides = ppt.Slides

// 幻灯片操作
var slide = slides.Item(1)
slides.Add(2, 1)  // 在第2位添加空白幻灯片（布局1=空白）

// 形状和文本
var shape = slide.Shapes.Item(1)
shape.TextFrame.TextRange.Text = "新标题"
shape.TextFrame.TextRange.Font.Size = 28

// 添加文本框
var newShape = slide.Shapes.AddTextbox(1, 100, 100, 400, 200)
// (方向, 左, 上, 宽, 高) 单位: pt
newShape.TextFrame.TextRange.Text = "内容"

// 遍历所有幻灯片
for (var i = 1; i <= slides.Count; i++) {
    var s = slides.Item(i)
    for (var j = 1; j <= s.Shapes.Count; j++) {
        var shp = s.Shapes.Item(j)
        if (shp.HasTextFrame) {
            Console.log(shp.TextFrame.TextRange.Text)
        }
    }
}
```

## 工作流程

### Step 1: 理解需求

确认：
- **操作对象**：文字/表格/演示？
- **操作内容**：具体要自动化什么？
- **触发方式**：手动运行 / 打开文档时自动执行？
- **输入输出**：需要用户输入什么？输出什么？

### Step 2: 编写 JSA 脚本

遵循以下规范：

**代码规范：**
```javascript
/**
 * 宏名称：功能简述
 * 作用：详细说明
 * 使用方法：在WPS中 开发工具 → 宏 → 选择此宏 → 运行
 */
function MacroName() {
    try {
        // 主逻辑

    } catch (e) {
        Application.alert("执行出错：" + e.message)
    }
}
```

**编码要点：**
1. 始终使用 `try...catch` 包裹主逻辑
2. 集合索引从 **1** 开始（`Sheets.Item(1)`，`Cells(1,1)`）
3. 用 `Value2` 而非 `Value` 读写单元格值
4. 用 `Application.alert()` 而非 `MsgBox`
5. 不要使用 `Set` 关键字
6. 不要使用 VBA 的 `Sub...End Sub` 语法
7. 字符串用 `+` 连接而非 `&`
8. 布尔值小写 `true/false`
9. 文件路径使用正斜杠 `/` 或双反斜杠 `\\`

### Step 3: 输出脚本

将JSA脚本写入 `.js` 文件，并提供使用说明：

```text
使用方法：
1. 打开 WPS 文档/表格/演示
2. 菜单栏 → 开发工具 → 宏编辑器（或按 Alt+F11）
3. 在编辑器中新建模块
4. 粘贴脚本代码
5. 运行（F5）或关闭编辑器后通过 开发工具→宏 运行
```

### Step 4: 调试建议

- 用 `Console.log()` 输出中间结果到宏编辑器控制台
- 复杂操作先在小数据集上测试
- 注意WPS版本差异（部分API在旧版本中不支持）

## 常见宏模板

### 批量替换文档内容
```javascript
function BatchReplace() {
    var doc = Application.ActiveDocument
    var replacements = [
        ["旧词1", "新词1"],
        ["旧词2", "新词2"]
    ]
    for (var i = 0; i < replacements.length; i++) {
        var find = doc.Content.Find
        find.ClearFormatting()
        find.Replacement.ClearFormatting()
        find.Text = replacements[i][0]
        find.Replacement.Text = replacements[i][1]
        find.Execute(undefined, false, false, false, false,
                     false, true, undefined, false, undefined, 2)
    }
    Application.alert("替换完成！")
}
```

### 表格数据汇总
```javascript
function SummarizeData() {
    var ws = Application.ActiveWorkbook.ActiveSheet
    var lastRow = ws.Cells(ws.Rows.Count, 1).End(-4162).Row // xlUp = -4162
    var sum = 0
    for (var i = 2; i <= lastRow; i++) {
        var val = parseFloat(ws.Cells(i, 2).Value2) || 0
        sum += val
    }
    ws.Cells(lastRow + 1, 1).Value2 = "合计"
    ws.Cells(lastRow + 1, 2).Value2 = sum
    ws.Cells(lastRow + 1, 1).Font.Bold = true
    ws.Cells(lastRow + 1, 2).Font.Bold = true
}
```

### 批量设置表格格式
```javascript
function FormatTable() {
    var ws = Application.ActiveWorkbook.ActiveSheet
    var rng = ws.UsedRange

    // 设置字体
    rng.Font.Name = "宋体"
    rng.Font.Size = 11

    // 边框
    for (var i = 7; i <= 12; i++) { // 所有边框类型
        rng.Borders.Item(i).LineStyle = 1
        rng.Borders.Item(i).Weight = 2
    }

    // 表头加粗+背景色
    var headerRow = ws.Range(ws.Cells(1, 1), ws.Cells(1, rng.Columns.Count))
    headerRow.Font.Bold = true
    headerRow.Interior.Color = 0xD9E1F2  // 浅蓝色（BGR）
    headerRow.HorizontalAlignment = -4108 // 居中

    // 自适应列宽
    rng.Columns.AutoFit()
}
```

## 示例

```bash
# 写一个批量替换文档内容的宏
/wps-jsa-macro 批量将文档中所有"旧公司名"替换为"新公司名"

# 写一个表格自动汇总宏
/wps-jsa-macro 汇总当前工作表B列的销售额，在最后一行显示合计

# 写一个PPT批量修改字体的宏
/wps-jsa-macro 将所有幻灯片中的Arial字体替换为微软雅黑
```

输出：生成 `.js` 文件，复制到WPS宏编辑器中运行即可。

## API 参考

详细 JSA API 参考见 [reference/wps-jsa-api.md](reference/wps-jsa-api.md)。
中文排版通用规范见 [../shared/chinese-typesetting.md](../shared/chinese-typesetting.md)。
