---
name: lgui-ui
description: "在 LGUI 工程里拼界面：按 UI 开发规范写 ui/ 里的 FairyGUI XML、用排布模式生成横竖两版、AI 出图后用 art split / art cut 拆图、加动效、在编辑器里和人一起改。要新做或修改界面的样子时用。"
license: MIT
---

# lgui-ui：拼界面

**什么时候用：** 新做一个界面，或者改界面的布局、图片、文字、动效。界面背后的功能（数据、操作）用 `lgui-code`。

**先读：** [UI 开发规范](../../references/ui-spec.md)。第 1 节是固定步骤，每次照做。

**输入：** 要做什么界面（UX 设计稿、参考图或描述）、放在哪个包、横竖屏要求。参考图和素材的来源不清楚时先问用户。只有一张原型图、还没和用户对过需求时，先用 `lgui-ux` 出设计稿（`design/<名字>/design.json`）：位置、文字、贴边方式、复用来源、要新做的组件和图片都以它为准，拼的时候不重新量。

**命令：**

| 要做的事 | 命令 |
|---|---|
| 新界面：按排布模式一次生成横竖两版 | `lgui new view <包>/<组件> --pattern split\|tabs\|grid\|dialog`（模式见规范 7.4） |
| 连功能骨架一起生成 | `lgui new module <名字> --pattern <模式>` |
| 查现有组件和控件名 | `lgui ui list` |
| 查有哪些通用的组件、图片、字体可以直接用（框架自带和项目自己的），谁在用、哪些可以合并 | `lgui ui list --shared`（规范第 10 节；第二个地方要用时才搬进 `Common`） |
| AI 出的网格大图拆成小图 | `lgui art split <大图> --grid 6x4 --size 128x128 --pkg <包> --names <名字>`（原图放进 `ui/art-src/`） |
| AI 出的图集页（物件漂过格线、大小不一、自由排布的九宫格零件）拆成小图 | `lgui art cut <整页图> --pkg <包> --names <名字文件>`：按透明区域找物件、整页统一缩放、去白边、九宫格保留拉伸区并写 `scale9grid`、平铺图查接缝并写 `scale="tile"`，出一张检查图；包里已有的同名图片直接替换、资源 ID 不变；每项可以写自己的尺寸、`fit`（拉伸图的固定方向正好等于尺寸）、`pkg=`（存进哪个包）。给 AI 出图的提示词照规范第 5.1 节「art cut 对输入图的要求」写 |
| 检查规范 | `lgui check`（`LGUI-UI-xxx`） |
| 看效果 | `lgui dev`；截图 `lgui verify` |
| 和人一起在编辑器里改 | `lgui editor`；编辑器开着时改已有控件的属性：`lgui editor props <组件> <控件> <属性>=<值> ...` |

**要点：** 直接编辑 `ui/` 里的 XML；ID 和名字照规范第 3 节；横竖两版控件名和类型一致；文字都写 `autoSize`；图里不放字（带字图片按第 9 节，用装载器）；不带图片文件时用 `icon://<名字>` 代码图标（第 5.2 节，只供网页端和 `lgui test`），不带 mp3 文件时按钮音效写 `synth://<名字>`（第 5 节，配合自定义 `audio`）；有网页三维宿主 `host/main.ts` 时，`hud` 层等 `inputMode` 为 `'game'` / `'all'` 的界面根 `<component>` 写 `opaque="false"` 让空白处透给底层画布（`LGUI-UI-070`）；跨包引用（子组件、图片）写 `pkg` + `src`，子组件跨包不写 `fileName`（第 2 节）；按钮、标签、下拉框的文字叫 `title`、图标装载器叫 `icon`，旋转缩放的控件设 `pivot`，动效要动整组就写高级组（`advanced="true"`），单行的文字写 `singleLine`（第 6、8 节）。动效在静态界面做好以后再加，见 [motion.md](references/motion.md)。

**产出：** `ui/` 里的组件和图片、`lgui check` 没有错误、横竖两张截图（文字没被截断、两版排得对）。
