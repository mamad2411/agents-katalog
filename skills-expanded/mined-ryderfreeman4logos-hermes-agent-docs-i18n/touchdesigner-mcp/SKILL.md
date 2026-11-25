---
name: touchdesigner-mcp
description: "Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execute Python, build real-time visuals. 36 native tools."
version: 1.1.0
author: kshitijk4poor
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [TouchDesigner, MCP, twozero, creative-coding, real-time-visuals, generative-art, audio-reactive, VJ, installation, GLSL]
    related_skills: [native-mcp, ascii-video, manim-video, hermes-video]

---

# TouchDesigner 集成（twozero MCP）

## 重要规则

1. **绝不要猜测参数名称。** 首先调用 `td_get_par_info` 获取操作类型的参数信息。您所使用的训练数据并不适用于 TD 2025.32 版本。
2. **如果出现 `tdAttributeError` 异常，请立即停止。** 在继续操作之前，先对出错的节点调用 `td_get_operator_info`。
3. **切勿在脚本回调中硬编码绝对路径。** 应使用 `me.parent()` 或 `scriptOp.parent()` 来获取路径。
4. **优先使用原生 MCP 工具，而非 `td_execute_python`。** 请使用 `td_create_operator`、`td_set_operator_pars`、`td_get_errors` 等函数。仅当需要处理复杂的多步骤逻辑时，才考虑使用 `td_execute_python`。
5. **在构建代码之前先调用 `td_get_hints`。** 该函数会返回与您正在处理的操作类型相关的特定提示信息。

## 架构设计

```
Hermes Agent -> MCP (Streamable HTTP) -> twozero.tox (port 40404) -> TD Python
```

36种原生工具。免费插件（无需付费或许可——截至2026年4月已确认）。
具备上下文感知能力（可识别选定的操作及当前网络环境）。
中心节点健康检查：执行`GET http://localhost:40404/mcp`命令，即可获取包含实例PID、项目名称以及TD版本的JSON数据。

## 设置（自动化方式）

运行设置脚本即可自动完成所有配置：

```bash
bash "${HERMES_HOME:-$HOME/.hermes}/skills/creative/touchdesigner-mcp/scripts/setup.sh"
```

该脚本将执行以下操作：
1. 检查TD是否正在运行
2. 若未缓存则下载twozero.tox文件
3. （如缺失）在Hermes配置中添加`twozero_td` MCP服务器
4. 测试端口40404上的MCP连接
5. 告知仍需执行的手动操作（将.tox文件拖入TD，开启MCP开关）

### 手动操作步骤（需手动完成，无法自动化）
1. **将`~/Downloads/twozero.tox`文件拖入TD网络编辑器** → 点击“安装”
2. **启用MCP功能**：点击twozero图标 → 设置 → MCP → 选择“自动启动MCP” → 确定
3. **重启Hermes会话**，以便系统加载新的MCP服务器

设置完成后，请进行验证：
```bash
nc -z 127.0.0.1 40404 && echo "twozero MCP: READY"
```

## 环境说明

- **非商业用途的 TD** 的分辨率上限为 1280×1280。此时需使用 `outputresolution = 'custom'` 并手动指定宽度和高度。
- **编码格式**：首选 `prores`（在 macOS 上表现最佳），若不可用则可使用 `mjpa` 作为替代方案。而 H.264/H.265/AV1 格式则需要商业许可。
- 在设置参数之前，务必先调用 `td_get_par_info` 函数——不同版本的 TD 该函数的参数名称可能有所不同（详见重要规则 #1）。

## 工作流程

### 第 0 步：探测（在构建任何内容之前）

```
Call td_get_par_info with op_type for each type you plan to use.
Call td_get_hints with the topic you're building (e.g. "glsl", "audio reactive", "feedback").
Call td_get_focus to see where the user is and what's selected.
Call td_get_network to see what already exists.
```

无需临时节点，也无需进行清理操作。这完全取代了旧有的发现流程。

### 第一步：清理 + 构建

**重要提示：请将清理与创建操作拆分为独立的MCP调用。** 若在同一个`td_execute_python`脚本中同时销毁并重新创建同名节点，将会引发“无效的操作对象”错误。详情请参阅问题清单#11b。

对于每个节点，请使用`td_create_operator`函数（该函数会自动处理视口定位问题）：

```
td_create_operator(type="noiseTOP", parent="/project1", name="bg", parameters={"resolutionw": 1280, "resolutionh": 720})
td_create_operator(type="levelTOP", parent="/project1", name="brightness")
td_create_operator(type="nullTOP", parent="/project1", name="out")
```

如需批量创建或配置连接，可使用 `td_execute_python` 命令：

```python
# td_execute_python script:
root = op('/project1')
nodes = []
for name, optype in [('bg', noiseTOP), ('fx', levelTOP), ('out', nullTOP)]:
    n = root.create(optype, name)
    nodes.append(n.path)
# Wire chain
for i in range(len(nodes)-1):
    op(nodes[i]).outputConnectors[0].connect(op(nodes[i+1]).inputConnectors[0])
result = {'created': nodes}
```

### 第 2 步：设置参数

建议使用原生工具（可验证参数有效性，且不会导致程序崩溃）：

```
td_set_operator_pars(path="/project1/bg", parameters={"roughness": 0.6, "monochrome": true})
```

对于表达式或特定模式，可使用 `td_execute_python`：

```python
op('/project1/time_driver').par.colorr.expr = "absTime.seconds % 1000.0"
```

### 第3步：数据传输

请使用 `td_execute_python` 命令——目前暂无内置的数据传输工具：

```python
op('/project1/bg').outputConnectors[0].connect(op('/project1/fx').inputConnectors[0])
```

### 第4步：验证

```
td_get_errors(path="/project1", recursive=true)
td_get_perf()
td_get_operator_info(path="/project1/out", detail="full")
```

### 第 5 步：显示 / 捕获

```
td_get_screenshot(path="/project1/out")
```

或者通过脚本打开一个窗口：

```python
win = op('/project1').create(windowCOMP, 'display')
win.par.winop = op('/project1/out').path
win.par.winw = 1280; win.par.winh = 720
win.par.winopen.pulse()
```

## MCP 工具快速参考

**核心工具（最常用）：**
| 工具 | 功能 |
|------|------|
| `td_execute_python` | 在 TD 中运行任意 Python 代码，可完整访问 API。 |
| `td_create_operator` | 创建带有参数及自动定位功能的节点。 |
| `td_set_operator_pars` | 安全地设置参数（会进行验证，避免程序崩溃）。 |
| `td_get_operator_info` | 检查单个节点的信息：连接关系、参数及错误状态。 |
| `td_get_operators_info` | 一次性检查多个节点的信息。 |
| `td_get_network` | 查看指定路径下的网络结构。 |
| `td_get_errors` | 递归查找错误与警告信息。 |
| `td_get_par_info` | 获取某种操作类型的参数名称（替代自动发现功能）。 |
| `td_get_hints` | 在构建之前获取相关模式与提示。 |
| `td_get_focus` | 查看当前处于激活状态的网络及选中内容。 |

**读/写工具：**
| 工具 | 功能 |
|------|------|
| `td_read_dat` | 读取 DAT 文件的文本内容。 |
| `td_write_dat` | 写入或修改 DAT 文件的内容。 |
| `td_read_chop` | 读取 CHOP 通道的值。 |
| `td_read_textport` | 读取 TD 控制台的输出内容。 |

**可视化工具：**
| 工具 | 功能 |
|------|------|
| `td_get_screenshot` | 将某个操作视图捕获为文件。 |
| `td_get_screenshots` | 同时捕获多个操作视图的截图。 |
| `td_get_screen_screenshot` | 通过 TD 捕获实际屏幕画面。 |
| `td_navigate_to` | 在网络编辑器中跳转到指定操作。 |

**搜索工具：**
| 工具 | 功能 |
|------|------|
| `td_find_op` | 按名称或类型在整个项目中查找操作。 |
| `td_search` | 搜索代码、表达式及字符串参数。 |

**系统工具：**
| 工具 | 功能 |
|------|------|
| `td_get_perf` | 性能分析（显示帧率及运行缓慢的操作）。 |
| `td_list_instances` | 列出所有正在运行的 TD 实例。 |
| `td_get_docs` | 获取关于特定 TD 主题的详细文档。 |
| `td_agents_md` | 读取或编写针对各 COMP 的 Markdown 文档。 |
| `td_reinit_extension` | 修改代码后重新加载扩展模块。 |
| `td_clear_textport` | 在调试会话开始前清空控制台内容。 |

**输入自动化工具：**
| 工具 | 功能 |
|------|------|
| `td_input_execute` | 向 TD 发送鼠标或键盘操作指令。 |
| `td_input_status` | 查询输入队列的当前状态。 |
| `td_input_clear` | 停止输入自动化操作。 |
| `td_op_screen_rect` | 获取某个节点在屏幕上的坐标。 |
| `td_click_screen_point` | 在截图中的指定点进行点击操作。 |
| `td_screen_point_to_global` | 将截图中的像素坐标转换为绝对屏幕坐标。 |

上表列出了典型创意工作流中会用到的 32 种工具。其余 4 种工具（`td_project_quit`、`td_test_session`、`td_dev_log`、`td_clear_dev_log`）为管理员或开发模式下的实用工具——如需包含完整参数规范的 36 种工具的完整参考信息，请查阅 `references/mcp-tools.md`。

## 关键实现规则

**GLSL 时间处理：** GLSL TOP 中不可使用 `uTDCurrentTime`。应通过“值”页面来获取时间信息。
```python
# Call td_get_par_info(op_type="glslTOP") first to confirm param names
td_set_operator_pars(path="/project1/shader", parameters={"value0name": "uTime"})
# Then set expression via script:
# op('/project1/shader').par.value0.expr = "absTime.seconds"
# In GLSL: uniform float uTime;
```

**回退方案**：始终使用 `rgba32float` 格式的常量 TOP 值（8 位数值会被限制在 0-1 范围内，从而导致着色器无法正常运行）。

**反馈 TOP 值设置**：应参考 `top` 参数的相关说明，而非直接输入数据线。首次处理完成后，“源数据不足”的问题即可解决；出现“处理依赖循环”警告属于正常现象。

**分辨率限制**：非商业用途的渲染分辨率上限为 1280×1280，此时需设置 `outputresolution = 'custom'`。

**大型着色器处理**：先将 GLSL 代码写入 `/tmp/file.glsl` 文件，再通过 `td_write_dat` 或 `td_execute_python` 命令将其加载进来。

**顶点/点数据访问（TD 2025.32 版本）**：应使用 `point.P[0]`、`point.P[1]`、`point.P[2]` 这种格式，而非 `.x`、`.y`、`.z`。

**扩展功能相关**：在 CONSTANT 模式下，`ext0object` 格式的写法为 `"op('./datName').module.ClassName(me)"`。使用 `td_write_dat` 编辑完扩展代码后，需调用 `td_reinit_extension` 函数以重新初始化该扩展。

**脚本回调函数**：务必通过 `me.parent()` 或 `scriptOp.parent()` 方法来使用相对路径。

**节点清理操作**：在遍历节点之前，务必先执行 `list(root.children)` 来获取所有子节点列表，并同时检查每个子节点的 `valid` 状态。

```python
# via td_execute_python:
root = op('/project1')
rec = root.create(moviefileoutTOP, 'recorder')
op('/project1/out').outputConnectors[0].connect(rec.inputConnectors[0])
rec.par.type = 'movie'
rec.par.file = '/tmp/output.mov'
rec.par.videocodec = 'prores'  # Apple ProRes — NOT license-restricted on macOS
rec.par.record = True   # start
# rec.par.record = False  # stop (call separately later)
```

H.264/H.265/AV1编码需要商业许可证。在MacOS系统上可使用`prores`格式，或作为备选方案使用`mjpa`格式。
提取帧：`ffmpeg -i /tmp/output.mov -vframes 120 /tmp/frames/frame_%06d.png`

**TOP.save()函数不适用于动画处理**——它每次都会捕获相同的GPU纹理。应始终使用MovieFileOut函数。

### 开始录制前的检查清单

1. 通过`td_get_perf`函数确认帧率大于0。若帧率为0，则录制结果将为空。相关问题可参考故障排除指南中的#38-39条。
2. 通过`td_get_screenshot`函数确认着色器输出并非黑色。出现黑色输出说明存在着色器错误或输入数据缺失。相关问题可参考故障排除指南中的#8、#40条。
3. **若需录制音频**：请先让音频开始播放，然后再延迟3帧开始录制。相关问题可参考故障排除指南中的#19条。
4. **在开始录制之前设定输出路径**——如果在同一脚本中同时设置这两个参数，可能会导致竞争条件。

## 基于音频信号的GLSL实现方案（经验证有效）

### 正确的信号处理流程（2026年4月测试通过）

```
AudioFileIn CHOP (playmode=sequential)
  → AudioSpectrum CHOP (FFT=512, outputmenu=setmanually, outlength=256, timeslice=ON)
  → Math CHOP (gain=10)
  → CHOP to TOP (dataformat=r, layout=rowscropped)
  → GLSL TOP input 1 (spectrum texture, 256x2)

Constant TOP (rgba32float, time) → GLSL TOP input 0
GLSL TOP → Null TOP → MovieFileOut
```

### 关键的音频响应规则（经实测验证）

1. **TimeSlice 必须保持开启状态**，才能用于 AudioSpectrum 功能。若关闭该选项，则会处理整个音频文件——即超过 24000 个采样点——从而导致数据溢出。
2. 需通过 `outputmenu='setmanually'` 和 `outlength=256` 手动将输出长度设置为 256。默认输出长度为 22050 个采样点。
3. **切勿使用 Lag CHOP 来实现频谱平滑处理**。Lag CHOP 在时间切片模式下运行，会将 256 个采样点扩展至 2400 多个，并将所有数值平均至接近零的水平（约 1e-06）。这样一来，着色器将无法接收到可用数据。这在测试中是导致音频同步故障的最主要原因。
4. **同样也不建议使用 Filter CHOP**——其也会引发与频谱数据相同的时间切片扩展问题。
5. 如有需要，可通过在 GLSL 着色器中使用带有反馈纹理的时间插值功能来实现平滑处理：`mix(prevValue, newValue, 0.3)`。这种方式可实现完美帧同步，且不会产生任何管线延迟。
6. **CHOP to TOP 的数据格式为 'r'，布局方式为 'rowscropped'**。频谱输出为 256x2 的结构（立体声）。第一个声道的采样点位于 y=0.25 处。
7. **数学增益值应为 10（而非 5）**。原始频谱在低频段的数值约为 0.19，设置增益为 10 后，着色器可获得的可用数值约为 5.0。
8. **无需使用 Resample CHOP**。可直接通过 AudioSpectrum 的 `outlength` 参数来控制输出大小。

### GLSL 频谱采样方式

```glsl
// Input 0 = time (1x1 rgba32float), Input 1 = spectrum (256x2)
float iTime = texture(sTD2DInputs[0], vec2(0.5)).r;

// Sample multiple points per band and average for stability:
// NOTE: y=0.25 for first channel (stereo texture is 256x2, first row center is 0.25)
float bass = (texture(sTD2DInputs[1], vec2(0.02, 0.25)).r +
              texture(sTD2DInputs[1], vec2(0.05, 0.25)).r) / 2.0;
float mid  = (texture(sTD2DInputs[1], vec2(0.2, 0.25)).r +
              texture(sTD2DInputs[1], vec2(0.35, 0.25)).r) / 2.0;
float hi   = (texture(sTD2DInputs[1], vec2(0.6, 0.25)).r +
              texture(sTD2DInputs[1], vec2(0.8, 0.25)).r) / 2.0;
```

完整的构建脚本及着色器代码请参阅 `references/network-patterns.md`。

## 操作符快速参考

| 类别 | 颜色 | Python 类型 / MCP 类型 | 后缀 |
|------|-------|---------------------|------|
| TOP | 紫色 | noiseTOP、glslTOP、compositeTOP、levelTop、blurTOP、textTOP、nullTOP | TOP |
| CHOP | 绿色 | audiofileinCHOP、audiospectrumCHOP、mathCHOP、lfoCHOP、constantCHOP | CHOP |
| SOP | 蓝色 | gridSOP、sphereSOP、transformSOP、noiseSOP | SOP |
| DAT | 白色 | textDAT、tableDAT、scriptDAT、webserverDAT | DAT |
| MAT | 黄色 | phongMAT、pbrMAT、glslMAT、constMAT | MAT |
| COMP | 灰色 | geometryCOMP、containerCOMP、cameraCOMP、lightCOMP、windowCOMP | COMP |

## 安全注意事项

- MCP 仅在本地主机运行（端口 40404），且不支持身份验证——任何本地进程均可发送指令。
- `td_execute_python` 以 TD 进程用户的身份拥有对 TD Python 环境及文件系统的完全访问权限。
- `setup.sh` 会从官方的 404zero.com 地址下载 twozero.tox 文件。如有疑虑，请自行核对下载内容。
- 该技能绝不会将数据发送到本地主机之外，所有 MCP 通信均在本地完成。

## 参考资料

| 文件 | 内容 |
|------|------|
| `references/pitfalls.md` | 来自实际使用中的宝贵经验教训 |
| `references/operators.md` | 包含各类操作符及其参数与使用场景的完整列表 |
| `references/network-patterns.md` | 音频响应、生成式处理、GLSL 编程、实例化等技术方案 |
| `references/mcp-tools.md` | 详尽的 twozero MCP 工具参数规范 |
| `references/python-api.md` | TD Python：op() 函数、脚本编写及扩展功能 |
| `references/troubleshooting.md` | 连接诊断与问题排查指南 |
| `references/glsl.md` | GLSL 变量、内置函数及着色器模板 |
| `references/postfx.md` | 后处理效果：光晕、CRT 效果、色差、反馈辉光等 |
| `references/layout-compositor.md` | HUD 布局模式、面板网格及 BSP 风格布局 |
| `references/operator-tips.md` | 线框渲染技巧及 TOP 反馈效果设置指南 |
| `references/geometry-comp.md` | 几何 COMP：实例化、POP 与 SOP 的区别以及形态变形功能 |
| `references/audio-reactive.md` | 音频频段提取、节拍检测及音量包络跟随技术 |
| `references/animation.md` | LFO 动画、计时器、关键帧、缓动函数以及表达式驱动的运动控制 |
| `references/midi-osc.md` | MIDI/OSC 控制器、TouchOSC 以及多机器同步功能 |
| `references/particles.md` | POP 效果及传统的 particleSOP：粒子发射、力场应用及碰撞处理 |
| `references/projection-mapping.md` | 多窗口输出、角点固定、网格变形及边缘混合技术 |
| `references/external-data.md` | HTTP、WebSocket、MQTT、串行通信、TCP 以及 webserverDAT 功能 |
| `references/panel-ui.md` | 自定义参数、面板 COMP 组件、按钮/滑块/输入框以及 panelExecuteDAT 功能 |
| `references/replicator.md` | replicatorCOMP：基于数据的克隆功能、布局管理及回调机制 |
| `references/dat-scripting.md` | DAT 类操作的执行方式：chop/dat/parameter/panel/op/executeDAT |
| `references/3d-scene.md` | 灯光系统、阴影效果、IBL/立方体贴图、多摄像机渲染以及 PBR 材质 |
| `scripts/setup.sh` | 自动化设置脚本 |

---

> 你并非在编写代码，而是在操控光线。
