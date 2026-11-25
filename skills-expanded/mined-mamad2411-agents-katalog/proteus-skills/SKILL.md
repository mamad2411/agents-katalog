---
name: proteus-skills
description: 使用 proteus-automatic-api Python 库创建、编辑和验证真实 Proteus/ISIS 工程，加载 MCU 固件、操作按钮/开关并读取仿真结果。用于用户要求 Proteus Skills、操作 .pdsprj、Proteus 自动化或在 Proteus 中测试按钮驱动电路的任务；普通电路讲解和概念配图不需要此技能。
license: MIT
---

# Proteus Skills

通过 `proteus_automatic_api` 交付可继续编辑的 `.pdsprj` 及可核对的原生结果。技能名称是 **Proteus Skills**，调用名是 `$proteus-skills`。独立代码仓库与 Python 分发包均名为 **`proteus-automatic-api`**，Python 导入名为 `proteus_automatic_api`。

技能与库独立分发。本技能不包含库源码、wheel、Proteus 软件、官方模板或第三方器件/固件。仓库中的 [原创 STM32 演示固件](examples/stm32) 单独列明用途；它们不替代本机 Proteus 资源。使用技能不要求克隆库仓库、将两者放在相邻目录或从技能目录运行任务。

所有 Proteus 操作必须通过 `proteus_automatic_api` 的公开 API 完成，包括选件、放置、连线、属性配置、仿真和结果读取。不得使用 Computer Use、OCR、屏幕坐标、鼠标键盘自动化或其他 GUI 操作工具补做步骤，也不得直接调用库的私有 UI 助手替代缺失的公开 API。`Session` 等公开接口内部驱动真实 Proteus 属于库工作流。

库未覆盖的操作必须明确报告能力缺口，不能自动回退到 GUI 后仍称其为本技能完成的操作。录制工具只可被动采集库真实执行的过程，不得驱动应用或修改工程。用户要求从零录制时，应从空白工程开始，记录实际选件、逐个放置、逐段连线、配置和验证；不能把完成态截图拼接称为完整绘制过程。公开 API 无法实时显示某个构建步骤时，明确说明限制，不伪造过程。

文件编辑保存后可用新的 `Session` 展示该步骤。原始录制和事件日志保留会话关闭、启动及等待过程，以及 `Library.search/get` 的实际查询、结果和操作时间；不能伪装成图形选件操作。发布 GIF 或视频默认只使用原生界面截图和原生配置对话框，不擅自添加外框、标题、API/结果说明或其他多余叠字。可剪去没有匹配窗口的等待段及其时长，保留全部真实窗口帧和实际操作顺序，不展示等待卡；独立调试工具窗不叠放到原理图上。剪辑范围、加速倍率及额外停帧写在媒体之外的说明中，原始录制和日志保持完整。

## 环境与版本

把“用户只有 Proteus，尚未安装 Python 库”作为正常首次使用场景。环境准备是必须执行的工作流，不是给用户阅读的前置条件。缺库时必须实际运行安装，验证成功后在同一任务中继续操作 Proteus；不能只给安装命令、等待用户手动安装或在安装成功后结束。

1. 检查 Windows、可用的 Python 3.10+ 和用户实际安装的 Proteus。优先使用任务已有虚拟环境；没有 Python 时协助从官方来源安装，不能把安装 Python 库说成安装了 Proteus 软件。
2. 在选定解释器中检查 `proteus_automatic_api` 的导入、版本、安装来源和本次所需接口。已有可用构建就继续；缺库时实际运行随技能提供的 [ensure_library.py](scripts/ensure_library.py)，不要仅展示命令；缺接口或用户要求更新时加 `--update`，详见 [首次安装与更新](references/distribution.md#首次安装与更新)。使用技能完成任务已包含为任务准备这个依赖的意图，不再询问是否要安装已声明的库；仍遵守宿主的执行权限。
3. 从固定的官方仓库 **https://github.com/kudoumakoto6523-design/Proteus_automatic_package** 查询默认分支最新提交，核对该提交的包名和公开接口，再安装其提交 SHA 对应的源码 ZIP。GitHub 是默认来源，不等待 PyPI、Release 或 wheel；不搜索同名仓库，不猜改名后的 URL，也不要求安装 Git。
4. 首次安装默认写入用户任务目录的 `.venv-proteus`，后续 pip、验证和任务脚本都使用同一解释器。安装失败不能进入电路操作；脚本成功后读取返回 JSON 中的 `python` 绝对路径，所有后续脚本用该解释器运行；检查本次所需 API 后立即继续用户的电路任务。不要在运行中的 Proteus 会话里换库，也不在每次 API 调用前检查更新。

在用户任务目录运行下面的命令；`<技能绝对路径>` 由 Agent 根据当前读取的本技能目录填写，不让用户寻找。示例解释器 `py -3.12` 换成已检测到的可用 Python。脚本只准备 Python 库，不启动或操作 Proteus。

```powershell
py -3.12 "<技能绝对路径>/scripts/ensure_library.py"
```

返回 `action=installed` 或 `action=reused` 且进程退出码为 0 后，使用返回的 `python` 继续本次工作流。只有实际安装失败或确实缺少必要资源，才报告具体阻断；不能将“尚未安装库”本身当作阻断。

当前操作示例已在 **Python 3.12 / proteus-automatic-api 0.2.0 / Proteus 8.16 SP3（8.16.36097）** 验证。GitHub 新提交仍需按其文档核对接口和 Proteus DLL 兼容性；不能把相同版本号视为相同构建。README 演示所需的 `label_offsets` 及新建工程固件隔离语义须单独确认，历史演示构建证据见 [分发说明](references/distribution.md#验证范围)。

| 资源 | 0.2.0 内置默认值（使用前验证） | 配置入口 |
|---|---|---|
| Proteus | `D:\Proteus\BIN\PDS.EXE` | `Session(project, executable=...)`，要求 PDS.EXE |
| 器件目录 | `C:\ProgramData\program\LIBRARY` | `Library(directory=...)`，仅查询 |
| 新建模板 | `C:\ProgramData\program\SAMPLES\Graph Based Simulation\Rescap.pdsprj` | `Circuit(template_project=...)` |

按任务检查所需路径；库不会自动探测安装。`import_device(..., library=...)` 的 `library` 是库名选择器，导入仍使用默认目录。`Library(directory=...)` 不会改变导入器；可以从有对应定义的 donor 工程导入。空模板初始化也可能回退到默认 Rescap 样例。不要把这些局部路径参数描述为完整可移植配置。

上述默认值来自库，不是技能仓库位置或对其他电脑的安装假设。示例中的 `template_path`、`executable_path`、`control_project_path`、`mcu_project_path`、`firmware_path`、`graph_project_path` 均由本次任务中已确认的绝对路径赋值；不需要创建额外配置文件。所有输出放到用户工作目录，技能安装目录仅提供说明。

## 按任务选择工作流

| 用户需求 | 接口与必读参考 |
|---|---|
| 新建、修改器件、连线、电源、网表 | [原理图与网表](references/api-workflows.md#原理图与网表)：`Circuit`、`Library`、`Session` |
| 固件、启停、按时运行、GPIO | [单片机仿真](references/api-workflows.md#单片机仿真)：`Simulation`、固件工具 |
| 按下/松开按钮、切换开关、改变逻辑输入 | [交互控制](references/interactive-controls.md)：`bind_controls` → 保存重开 → `press/release/set_switch` → 继续仿真验证响应 |
| 电压、电流、波形 CSV | [图表与模拟量](references/api-workflows.md#图表与模拟量)：已有图表/探针、`export_graph`、`sample_graph` |

只读取任务需要的参考。复用公共 API；不把研究脚本里的私有内存快照、DLL 偏移或演示型函数当成通用接口。

## 编辑和执行顺序

1. 确定用户要新建还是继续已有工程，以及输出位置、器件/固件和待验证行为。先读取现有元件与网络；引脚、电源、时钟按确切型号和固件确定。
2. **新建用 `Circuit(template_project=...)`，修改用 `Circuit.open(path)`。** 构造器创建空电路，不能用来保留原图；上述当前构建在保存新电路时由 API 移除模板的 `FIRMWARE*` 成员，避免旧 VSM Studio 项目覆盖新 MCU 固件。`Circuit.open()` 编辑保存则保留这些成员。原生修改或仿真已有项目时准备工作副本，同时处理其相对固件路径，不直接改 ZIP 成员转换工程。
3. 用 `pins(ref)` 的真实逻辑名称和世界坐标布线。单位为整数 `100000 = 1 mm`，Y 向上；位置不一定是器件中心。带封装映射的 MCU 引脚编号可能是组合编号或 `*`，不要按符号上显示的数字猜接线。优先采用清晰的正交走线，避免多余折返、斜穿文字和器件；原生重开后逐段检查实际路径，不能只看传入的坐标或网表。用公开 `update(ref, label_offsets={...})` 调整编号、值、器件名和参数文字的位置，保持所有文字、器件和导线在图框内留白；该接口不隐藏文字或删除参数。
4. 完成文件编辑和所需的 `bind_controls()` 后保存，再启动新的 `Session`。Proteus 会缓存控件绑定，不能靠打开会话中的 ADI 修改立即刷新。文件写入和会话操作串行进行；原生保存关闭后，继续文件编辑必须重新 `Circuit.open()`。同一 Session 的调用也串行执行，库没有并发锁。
5. 验证用户要求：重开检查值与网络；SDF 检查原生连接；继续仿真并读取输出检查电气/固件响应。按钮状态回读不能替代下游响应，网表通过也不能证明布局清晰或电路行为正确。

默认写新输出，已有目标需要明确 `overwrite=True`；用户要求更新原文件时可使用该参数，仍保留源文件变更检测。样例始终使用副本。`Session` 启动并只控制自己的进程，不附着到用户已有窗口。

## 能力边界与失败处理

- 结构重写仅支持已识别的单用户页、CDB v7、FILEVER 840/847。未知对象、图表、多页或多单元结构拒绝重写时，不能删除未知内容或换构造器绕过。只改属性可尝试副本上的 `Session.set_properties()`；其余报告公开 API 的能力缺口，不使用界面补做。
- 目录可查询不等于可导入，更不等于可仿真。核对模型、封装及 `pins()`；`VPULSE` 实例导入仍不支持。自动布线只有有限正交路径，复杂布局可能需要调整位置或手工路由。
- 支持六类二态控件，使用当前工程共享的 0–9 执行器键槽，每个控件占两个；其他绑定会减少最多五个控件的容量。不是任意引脚强制输入，也不覆盖多状态旋钮或外部 DLL 交互模型。
- 定时和交互有各自的 DLL 指纹限制。保留接口的拒绝行为；不改白名单/偏移，不用墙钟等待或“时间暂时不变”推断仿真成功。报告 `run_for()` 的实际时间、超出量和 `completion`。
- GPIO 日志是数字驱动事件；模拟量需要已有图表和探针。库尚无通用 ERC、任意图表/探针创建、通用实时引脚电压读取或原理图图片导出接口。图片不能替代真实工程。

`Session` 不是上下文管理器，`close()` 不自动保存。正常结束时 `sim.stop()`（如已仿真）、保存所需修改、`s.close()`。异常保留原始错误、工程和 `s.pid`，尝试正常关闭；未知保存对话框不自动放弃内容。

`s.process.poll() is None` 表示自有进程仍运行。只有明确可丢弃的测试副本，才可用该 Session 的 `s.process.terminate()`、`s.process.wait(timeout=5)` 清理。不要按进程名终止用户的其他 Proteus。失败后依据路径、模型、绑定、版本或对话框原因修正，不原样无限重试。

## 验证与交付

为本次任务保留简短可重跑脚本与必要断言；优先检查应连接/应分离的网络、目标值、输入时序和实际输出。使用本技能自带的公共 API 示例验证，不依赖库仓库的 `api/check_*.py` 或历史结果。完整库回归属于库仓库的维护工作，不是使用技能的前置条件。

交付工程绝对路径及实际产生的 SDF、CSV、日志/JSON 和脚本。分别说明文件重开、原生网表、交互状态、下游响应、视觉检查的完成情况，只报告本次证据支持的结论。
