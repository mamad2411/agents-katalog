---
name: lgui-code
description: "在 LGUI 工程里写界面背后的功能：按 MVC 开发规范写 Model、View 绑定表、Controller、Service 和测试，用 new module 生成骨架，用 check 和 test 收口。要让界面能操作、接数据、接服务器时用。"
license: MIT
---

# lgui-code：写功能

**什么时候用：** 界面已经有了（或者用 `--pattern` 一起生成），要写数据、操作、请求、存档、多语言文字、测试。界面的样子用 `lgui-ui`。

**先读：** [MVC 开发规范](../../references/mvc-spec.md)。第 1 节是固定步骤，每次照做。

**输入：** 要做的功能（有 UX 设计稿 `design/<名字>/` 时，元素点了做什么、状态、数据、该用哪些框架能力、行为用例都以它为准）、用到哪些界面（`lgui ui list` 查组件和控件名）、要不要接服务器。

**命令：**

| 要做的事 | 命令 |
|---|---|
| 生成 Model、Controller、测试的骨架 | `lgui new module <名字>`；连界面一起：加 `--pattern <模式>` |
| 给已有模块加界面和 View | `lgui new view <包>/<组件> --pattern <模式>` |
| 类型检查和规范检查 | `lgui check`（`LGUI-MVC-xxx`、`LGUI-UI-03x`、`TSxxxx`），报错全部改掉 |
| ui/ 里的固定文字提取到文本表 | `lgui i18n extract`，再翻译其他语言的 `i18n/<语言>.json` |
| 跑测试 | `lgui test`（headless 后端、假时钟）；只跑一部分：`lgui test tests/bag.test.ts`、`--name 出售`；测位置、尺寸、文字排版：`--browser`（真浏览器，规范第 12 节） |

**要点：** `src/` 只 `import` 自 `lgui` 和 `lgui/ui`；Model 只放数据和规则；View 只写绑定表（显示类用 `pick`，动作只调用一个 Controller 方法）；Controller 改 Model、调服务、开关界面；Service 先写接口，再写真实实现和测试用的假实现；不带图片文件时可在 `src/icons.ts` 定义代码图标并通过 `lgui.app({ icons })` 注册（规范第 4 节）；不带 mp3 文件时声音地址可写 `synth://<名字>` 并在 `lgui.app({ platform: { audio } })` 或 `host/main.ts` 的 `defineWebHost({ audio })` 提供自定义声音出口（规范第 15 节）；网页三维游戏可在 `host/main.ts` 用 `defineWebHost({ mount(stage) })` 接收框架建好的底层画布和按 `inputMode` 分流后的输入（规范第 17 节，`src/` 和 `host/` 都不直接访问 `document`）。用户看得到的文字都用文本键。测试之间 Model 不重置，加 `reset()` 并在 `beforeEach` 里调用（规范第 12 节）。

**产出：** `src/` 和 `tests/` 里的代码，`lgui check` 没有错误，`lgui test` 全部通过。接着用 `lgui-verify` 截图。
