---
name: ast-grep
description: AST 级代码结构化搜索与批量重构（Go/TS/Python/Kotlin 等）。当需要精确匹配语法结构（调用点、函数声明、嵌套模式）、排除注释与字符串误报、或做跨文件安全改写，而 rg/文本搜索噪声太大或无法表达结构时使用。
---

# ast-grep 结构化代码搜索与重构

`ast-grep`（旧别名 `sg`，本机两个命令等价）。以下坑位与绕过方法均在 ast-grep 0.45.3 + Go 实测验证（2026-09-03）。

## 选型：什么时候用

- rg/grep_search 表达不了的**结构匹配**：函数声明、调用表达式、嵌套上下文
- 要排除误报：注释/字符串里的同名文本（AST 匹配天然排除）
- **批量重构**：`rewrite -U` 或 scan 规则 + `fix`，只改代码节点，字符串/注释零误伤
- 简单字面量/正则搜索 → 用 rg 或 Qwen Code 的 grep_search（更快更省事，别杀鸡用牛刀）

## 常用命令

```bash
ast-grep run -p '<pattern>' -l <lang> [PATH]        # 搜索
ast-grep run -p '<旧>' -r '<新>' -l <lang> [PATH]    # 预览改写（加 -U 实际写盘）
ast-grep scan <path>                                 # 项目规则扫描（需 sgconfig.yml）
ast-grep run -p '...' -l go --json | jq 'length'     # 大结果只取统计，压缩上下文
ast-grep run -p '...' -l go --debug-query=ast        # 诊断：看模式被解析成了什么节点
```

## 元变量

- `$A`：单节点（任意表达式/标识符）；`$$$_`：匿名；`$$$ARGS`：零或多节点（参数列表/语句体）
- 大写命名只是捕获约定，不是语法要求

## ⚠️ 坑 1：Go 选择器调用 + 元变量 → 静默返回 0

**现象**：`run -p '$OBJ.Update($$$ARGS)' -l go` 无报错但 0 匹配；`c.Update($$$ARGS)`、`context.$FN(...)` 同样 0。

**根因**：tree-sitter-go 把 `a.B(` 优先解析为 `type_conversion`（类型转换）而非 `call_expression`，模式里的 `$` 未被识别为元变量。用 `--debug-query=ast` 诊断，看到 `ERROR + type_conversion` 而非 `call_expression` 即中招。

**不受影响的形态**（实测可用）：

- 全字面量：`context.TODO()`、`c.Update(context.TODO(), fetchedObject)` ✓
- 根元变量调用：`$FN($$$ARGS)` ✓
- 函数声明：`func $NAME($$$ARGS) $RET { $$$BODY }` ✓

**绕过**：用 YAML 结构规则代替模式文本（见下）。rewrite 需要选择器模式时，改用 `scan` 规则 + `fix:` + `--apply-fixes`。

## ⚠️ 坑 2：scan 单规则文件必须项目配置

`scan rule.yml`、`scan -r rule.yml`（无论是否位置参数）都报 `No ast-grep project configuration is found`。**规则文件必须放在 sgconfig.yml 的 ruleDirs 下，且在项目目录内运行**。临时一次性用法：

```bash
mkdir -p /tmp/sgproj/rules && printf 'ruleDirs:\n  - rules\n' > /tmp/sgproj/sgconfig.yml
cp my-rule.yml /tmp/sgproj/rules/
cd /tmp/sgproj && ast-grep scan /path/to/target
```

## ⚠️ 坑 3：`has` 里 `pattern` 的 kind 必须对得上

方法名位置在 Go 语法树里是 `field_identifier`，而 `pattern: Update` 生成 `identifier` —— kind 不匹配，永不命中（且无报错）。**用 `kind` + `regex` 组合**：只写 `regex: Update` 不限定 kind 会过匹配（如 `UpdateOptions`）。

## ✅ 验证过的结构规则模板：找 `.Method(` 调用点

```yaml
id: find-method-calls
language: go
rule:
  kind: call_expression
  has:
    field: function
    kind: selector_expression
    has:
      field: field
      kind: field_identifier
      regex: ^Update$   # 改方法名改这里；锚定 ^$ 防过匹配
```

输出带 file:line + 代码上下文。找函数声明、改写调用参数等同理：先想目标节点的 kind（`--debug-query=ast` 对真实代码片段跑一下就能看到），再用 `kind + has(field) + regex` 组合。

## 实践要点

- 先 run 预览、确认命中集，再 `rewrite -U`；scan + fix 同理
- 方法名/字段位置**不支持元变量**（`context.$FN(...)` 实测 0 匹配）——用 `field_identifier + regex` 代替
- 模式返回 0 且不符合预期时，第一反应是 `--debug-query=ast`，而不是换写法瞎试
