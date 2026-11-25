---
name: lgui-setup
description: "装好 LGUI 之后建工程、检查环境、打开网页预览。用户第一次用 LGUI、要新建一个 UI 工程、或者 lgui 命令报环境问题时用。"
license: MIT
---

# lgui-setup：建工程、检查环境、打开预览

**什么时候用：** 第一次用 LGUI；要新建工程；`lgui` 报环境错误（Node 版本、找不到 Chrome / Edge、工具加载失败）。

**命令行在哪：** 本技能所在目录往上两级是插件目录，命令行是 `node <插件目录>/tools/lgui.mjs`（下面写作 `lgui`）。用绝对路径，不要从当前目录猜。

**输入：** 工程放在哪个文件夹（用户没说就先问，不要自己定）。

**步骤：**

1. `lgui doctor`：检查 Node（24 或更高）、随插件带的工具、Chrome / Edge。报错就把原文告诉用户，按提示处理；Node 和浏览器要用户自己装。
2. `lgui init <文件夹>`：建工程（`ui/`、`src/`、`tests/`、`i18n/`、`.lgui/`；包里不放任何图片文件的纯代码工程用 `lgui init <文件夹> --code-only`）。文件夹不是空的会报错，不会覆盖。
3. 进工程目录，`lgui dev`：打开网页预览，把网址告诉用户。它一直运行、不会自己退出——放到后台跑（不想自动开浏览器加 `--no-open`）；改 `ui/`、`src/`、`i18n/` 会自动刷新；Ctrl+C 停止。
4. 已有工程：不要 `init`，直接 `lgui doctor` 和 `lgui dev`。提示版本不一致时运行 `lgui upgrade`，按它打印的更新记录改代码。

**产出：** 工程目录、预览网址、`doctor` 里还没解决的问题。

**接下来：** 有原型图要照着做，先用 `lgui-ux` 出 UX 设计稿；拼界面用 `lgui-ui`，写功能用 `lgui-code`，截图、测试和打正式网页包（`lgui build`）用 `lgui-verify`。工程目录和 `.lgui/project.json` 的字段见 [project-layout.md](../../references/project-layout.md)；错误码见 [error-codes.md](../../references/error-codes.md)。
