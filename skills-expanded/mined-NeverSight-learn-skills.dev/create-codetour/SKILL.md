---
name: create-codetour
description: 为指定功能生成 CodeTour `.tour` 导览文件。
disable-model-invocation: true
---

为一个功能生成 CodeTour `.tour` 文件——沿 **call stack** 讲故事，不重复代码。

1. **Locate** —— 确认要导览的功能，读取相关源码，记下每个代码位置相对项目根目录的路径（如 `src/services/auth.ts`）。信息不足就查代码或问用户，不要猜。

2. **Trace** —— 按逻辑调用顺序排布步骤：入口 → 校验 → 处理 → 导出/响应。完成标准：**5-10 步**，顺序与调用链一致。

3. **Pin each step** —— 只用 `pattern` 锚定代码位置，禁用 `line`（两者并存时 `line` 覆盖 `pattern`，定位会漂移）。`pattern` 优先用 **function/class name**，如 `^\s*(async\s+)?function\s+handleSubmit`。要指向函数体内部的细节步骤时，先在目标处加一行 `TOUR: ...` 注释（对该步骤的概略描述，脱离 tour 也自足、有意义），再用注释行做 `pattern`，如 `TOUR: validate the request payload`。完成标准：每个 `pattern` 在目标文件中精确匹配唯一位置；全程不出现 `line` 字段。

4. **Write the JSON** —— 按下方 Reference 生成 `.tour`。完成标准：输出只含一个 `json` 代码块，内含合法 JSON；每条 `file` 都是相对路径。

## Reference

### CodeTour schema

```json
{
  "$schema": "https://aka.ms/codetour-schema",
  "title": "Tour 名称",
  "description": "整体背景与导览目标",
  "steps": [
    {
      "file": "相对项目根目录的文件路径",
      "pattern": "定位该步骤的正则表达式",
      "description": "Markdown 文本，讲解设计意图与业务逻辑，可含 [运行测试](command:codetour.sendTextToTerminal?[\"npm%20test\"])",
      "title": "步骤小标题",
      "selection": {
        "start": { "line": 10, "character": 1 },
        "end": { "line": 15, "character": 20 }
      }
    }
  ]
}
```

- 只用 `pattern` 定位，禁用 `line`：两者并存时 `line` 覆盖 `pattern`，定位会漂移。优先用 function/class name 做 `pattern`；函数体内部的细节步骤，用 `TOUR: ...` 注释行锚定。
- `TOUR: ...` 注释：添加在被锚定的细节步骤处，是对该步骤的概略描述；它必须脱离 tour 也自足、有意义，就像一句文档注释。同一文件的注释文本须唯一，保证 `pattern` 只匹配一处。
- `description` 讲 **Why**：设计意图、业务逻辑，不重读代码本身。
- `selection` 可选：高亮一段具体代码范围。
