---
name: peekaboo
description: 用 Peekaboo 操作桌面 App。
disable-model-invocation: true
---

# peekaboo

## 在 Blueprint 里（先读这一段）

- **先看清单，再动手**：`peekaboo see --window-id <窗口号> --tree --no-screenshot --json` 给的是文字清单（按钮、菜单、输入框和它们的编号），看不了图也能用；要看画面再截图。窗口号从 `peekaboo window list --app <软件名> --json` 拿。
- **截图放进项目**：`--path <项目里的位置>`（例如 `研究/截图/编辑器.png`），再用 `read_image` 看；截图目录须先存在。
- **不抢用户的鼠标键盘**：用户可能正在用这台电脑。只用后台方式操作（手册里的 background）；非得 `--foreground` 前台操作时，先在对话里问他，他同意了再做。
- **只碰任务要的那个软件。** 别的应用、窗口、剪贴板不看不动。
- **在这里 peekaboo 就在你自己的进程里跑**（环境里已经设了 `PEEKABOO_NO_REMOTE=1`，等于每条命令都带着 `--no-remote`）。下面官方手册里讲 Bridge、daemon、GUI host、`--bridge-socket` 的部分都跳过，别去起、停、切换它们。截屏卡住或只截到桌面壁纸时，加 `--capture-engine cg` 再试一次。
- **报没有权限**（录屏、辅助使用）时，按权限诊断指出的实际执行程序，在「系统设置 → 隐私与安全性」中开启相应权限。别假定执行程序一定是终端机，别自己想办法绕。
- 网页里面的内容（页面上的字、表单、控制台）用 `playwright-cli`，它更准；这份管网页以外的软件。
- 下面官方手册里讲 Peekaboo 开发、源码构建的部分跟你无关。

按当前操作查[官方操作手册](references/官方操作手册.md)中的命令。来源：openclaw/Peekaboo，MIT；截图示例使用项目内路径。
