---
name: client-require-whitelist
description: 检查 DSH 客户端插件的 require(...) 是否都落在宿主的 9 项浏览器模块表里。表外的名字在浏览器里解析不到而且不报错，所以这件事值得变成一条会红的命令。改 lib/client.js 或任何客户端半边时用得上。
disable-model-invocation: true
---

# 客户端 `require` 白名单检查

> **这份技能默认关着**（frontmatter 里 `disable-model-invocation: true`）：它是"升格机制"的示例，
> 留在目录里给你随时调用，但不进模型的技能目录、模型也不能替你自己决定用它。
> 想让它也进模型目录，删掉那一行即可。

**症状**：客户端半边（`lib/client.js` 这类，交给 `window.__ModuleLoader__.load({ id, factory })` 跑的那半边）
写了 `require('@deepseek-ai/dsh-client-ui-xxx')` 这类名字，页面**不报错**，但那半边的功能就是不出现。

**原因**：浏览器里的模块表只有固定的 9 项 ——
`react`、`react/jsx-runtime`、`react-dom`、`react-dom/client`、`@deepseek-ai/cordis`、
`dsh-client-store`、`dsh-client-ui-slots`、`dsh-client-ui-primitives`、`dsh-client-ui-dockkit`。
表外的 specifier 解析不到，失败发生在工厂体里，于是表现成"插件没效果"而不是一条错误。

## 触发场景

- 你刚给客户端半边加了一个 `require`；
- 从别的插件抄了一段代码，名字看着对；
- 改了客户端产物之后，某块界面**静默**不出现。

## 做法（三步）

1. **先**把源码里所有 `require(...)` 的 specifier 抽出来（一条正则就够，不必解析 AST）；
2. **再**逐个对照上面那 9 项白名单，表外的单独列出来；
3. **最后**跑一次检查命令，让它成为会红的证据：

```bash
node scripts/check-requires.mjs lib/client.js
```

本技能自带这份检查与两个夹具（干净样本 / 坏样本），可以照抄或直接调用：

| 文件 | 用途 |
|---|---|
| `scripts/whitelist.mjs` | 白名单 + `offenders(src)` 纯函数（判断逻辑在这里） |
| `scripts/check-requires.mjs` | 命令行入口，表外非零退出 |
| `fixtures/ok.js` / `fixtures/bad.js` | 一绿一红两个样本 |

## 验证（怎么知道它还在工作）

```bash
node selftest.mjs        # 期望 7/7 passed
```

自测本身就是"能变红能变绿"的证明：干净样本必须绿、坏样本必须红。
想确认它不是恒绿，把 `scripts/whitelist.mjs` 里的 `WHITELIST` 删掉一项再跑 —— 干净样本会报表外，自测立刻 FAIL。

## 边界

- 这套检查只看 **specifier 名字**，不管那个模块实际导出了什么；名字对而导出缺失是另一类问题。
- 白名单是**宿主的**，会随宿主版本变；升级 DSH 之后值得重新对一次（词表来源是宿主客户端的模块表）。
- 服务端半边（`lib/index.js`）不受这份白名单约束。

## 附：一支诊断签（彩蛋）

结论后面可以带一支**叠词签**，给结局起个名字：

```bash
node scripts/check-requires.mjs --彩蛋 lib/client.js     # --egg 也行
```

| 签 | 什么结局 |
|---|---|
| **空荡荡** | 一个文件都没给 |
| **硬邦邦** | 有表外名字杵在那儿（最常见的那支） |
| **慢吞吞** | 扫了 ≥5 个文件**且都干净**（结论不受影响） |
| **亮晶晶** | 一个表外名字都没有 |

签表在 `scripts/whitelist.mjs` 的 `FORTUNES` 里，加一行就多一支；**顺序即优先级** ——
诊断（空荡荡 / 硬邦邦）排在口味签前面，免得彩蛋盖过结论。自测把四种结局各钉了一条断言。
