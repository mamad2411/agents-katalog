---
name: lgui-unity
description: "将已有 LGUI 工程导出到 Unity 6000.6/PuerTS 3.0.3，检查本地包、启动场景和 Windows IL2CPP Player。用于 LGUI 原生交付，不用于普通 Unity 游戏逻辑。"
license: MIT
---

# lgui-unity：导出、运行和验证 Unity

先读 [unity.md](../../references/unity.md)。输入是已有 LGUI 工程和目标 Unity 工程目录；用户已经指定路径时直接使用。先完成网页功能，再验证原生端。

**命令行：** 本技能目录往上两级是插件目录。使用绝对路径 `node "<插件目录>/tools/lgui.mjs"`，以下简写为 `lgui`；在 LGUI 工程根目录执行。

1. 核对 Unity 6000.6.x；Windows IL2CPP 模块和 C++ 工具链；工程内 `Packages/com.tencent.puerts.core/`、`Packages/com.tencent.puerts.v8/` 两个官方 3.0.3 实际目录。缺项按任务授权处理；导出命令不会自动安装软件，也不修改 `Library/PackageCache/`。
2. 运行 `lgui check`、`lgui test`，再执行 `lgui unity export --to "<Unity 工程路径>"`。导出会核对固定补丁摘要；未知文件报错时按原因修复，不绕过校验。工程若使用了网页专用的代码图标（`icon://…`），导出会报 `LGUI-CLI-144` 并拒绝写入，需先换成 `ui/` 包里登记的 PNG 图片。版本不一致时先确认 `.lgui/project.json` 的 `unityProject` 指向要升级的目标，必要时按 unity.md 调整，再运行 `lgui upgrade` 并导出；升级命令不读取导出的 `--to`。
   工程用了项目字体且缺 TMP Settings 时，导出会自动导入 TMP Essential Resources：先查工程的 UGUI 包缓存、本地包，再查对应版本的 Unity Hub 默认安装和 Windows `%LOCALAPPDATA%\Programs\Unity\<版本>` 用户安装；找不到报 LGUI-CLI-143 并列出候选路径。已有 TMP Settings 时不改写资源。
3. 等 Unity 导入和 C# 编译结束，打开 `Assets/LGUI/LGUIBoot.unity` 点 Play，检查真实画面和操作。已有场景不覆盖；脚本资源是 `Game/game.js`。保留 `Assets/LGUI/link.xml`，包内的模板不能代替它。
   项目字体与系统回退字都要验收：普通/粗体中英文、描边、投影及 shrink。`shadowOffset="4,4"` 是右、下各 4 个设计像素，生僻字回退不应因字体图集不同变成另一偏移。与网页比像素时，先核实际视口、Game/Player 屏幕尺寸及缩放，用已知尺寸纯色标尺验证 1:1，再保存未缩放的无损截图；等运行时目标文字已显示，不凭截图文件名、文件尺寸或采样工具退出成功认定通过。Editor 与 Release IL2CPP 分别看真实画面；超限 shrink 的预期 `LGUI-RT-183` 与额外错误分开记录。
4. 打 Windows Player 前，按 unity.md 配置 IL2CPP、Release、非 Development，运行 PuerTS 的 **Generate il2cpp/Reflection Mode**（`GenV2WithoutWrapper()`），完成导入后再构建。反射模式仍需要委托和值类型原生桥；不要用类型静态 wrapper 生成代替。普通交付保持 `LGUIBoot.debugPort = -1`。
5. 检查自动换版前确认工程配置 `orientation = "both"`，以及预期组件的 `@portrait` 版本；锁定方向或共用同一版时按实际配置验收。在实际 Player 检查功能、文字、平台服务、格式化，以及窗口横竖切换、语言切换后的选中项和滚动位置。按用户需要保留网页和 Player 的横竖截图，并打开可操作的页面或客户端供验收。竖窗口可以检查手机比例布局，不能代替物理设备输入验证。

界面、代码和翻译回到 `ui/`、`src/`、`i18n/` 修改后重新导出；用户代码只使用 `lgui`。导出的两个资源目录会整目录替换，用户自己的 C# 放在 `Assets/LGUI/` 以外。

图集导入范围、跨包依赖、ArtText 生命周期、列表位置、modal 顺序和网络策略见参考文档的「运行约定」。检查实际组件引用，不靠预先打开别的界面建立包依赖；区分正常流程和预期失败用例，保留完整错误，不用专门失败探针的配置替代普通 Player 配置。

维护者需要复现像素和内存验收时，按参考文档的「本轮验证范围与维护者复现」使用仓库开发工具，明确图形模式、原始 VM、暂停堆采样和正式 0/200 快照。有限 200 次窗口的结论写清范围，不推广为全堆逐字节或任意更长生命周期已证明；普通客户端双比例人工验收另记。

**交回：** 导出目标、Editor Play 与 Release Player 分别的结果、运行日志和截图路径、未执行项及原因。文件生成、Editor 运行和 Player 验收分别记录；内存、包体数据只引用实际测量结果。报错含错误码，见 [error-codes.md](../../references/error-codes.md)。
