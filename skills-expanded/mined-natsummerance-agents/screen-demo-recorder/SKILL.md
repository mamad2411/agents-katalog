---
name: screen-demo-recorder
description: |
  开源桌面屏幕录制与剪辑工作流（Recordly）：整屏/单窗口录制、麦克风与系统音频、时间线剪辑（trim/变速/缩放区域/标注）、光标美化与自动缩放建议、摄像头气泡画中画、样式化背景相框，导出 MP4/GIF 并可保存 .recordly 工程续剪。触发场景：用户说"录个产品 demo/操作教学视频"、"录屏加缩放和光标特效"、"导出 GIF 动图"、"加背景相框/画中画/字幕标注"。不适用于：网页内嵌的用户会话 DOM 级录制回放（走 rrweb-session-recording）、直播实时推流。
source_project: webadderallorg/Recordly
tags: [screen-recording, demo-video, video-editing, gif-export, cursor-effects]
---

# Screen Demo Recorder（Recordly 演示视频录制剪辑法）

## R (Reading) — 源项目核心设计

> "Recordly is your open-source screen recorder and editor for walkthroughs, demos, product videos." —— 定位是"录完即剪"的桌面应用：平台原生采集层（macOS ScreenCaptureKit / Windows WGC+WASAPI / Linux Electron），PixiJS 做场景合成渲染，"the same scene logic used in preview is rendered into exported MP4 or GIF output"；".recordly files store the source media path plus editor state so work can be reopened later"。

（来源：https://raw.githubusercontent.com/webadderallorg/Recordly/main/README.md ）

## I (Interpretation) — 方法论骨架

核心洞察：**把"原始录屏"当素材而不是成品**——缩放、光标动效、相框全部后置到编辑阶段合成，录制阶段只管忠实捕获。

1. **采集层按平台选型**：macOS 14+ 用 ScreenCaptureKit（可干净排除真实光标）；Windows 10 Build 19041+ 用 WGC 原生助手 + WASAPI 系统音频；Linux 走 Electron 捕获（不支持隐藏光标，系统音频通常需 PipeWire）。
2. **录制范围与音轨决策**：整块显示器或单个应用窗口二选一，同时确定麦克风/系统音频开关。
3. **时间线区域模型**：一切剪辑都是 timeline region——trim、手动缩放区、依据光标活动生成的自动缩放建议、加速/减速区、文字/图片/图形标注、额外音轨、裁切感知编辑。
4. **光标是可调角色**：显示/隐藏、大小、平滑、运动模糊、点击弹跳、摇摆、loop mode（服务无缝循环导出）。
5. **合成三件套**：摄像头气泡（预设位/自定义 X-Y/镜像/随缩放反应）× 相框（壁纸/纯色/渐变/模糊/内边距/圆角/阴影）× 宽高比预设。
6. **工程可持久化**：`.recordly` 保存媒体路径 + 编辑器状态，随时重开继续剪。

## A1 (Past Application) — 源项目的典型应用

### 案例: 从录制到 MP4/GIF 导出的标准流程
- **输入**: 选定屏幕或窗口 + 音频选项 → 启动录制，停止后直接跳入编辑器。
- **做法**: 时间线上修剪废段、采纳并微调自动缩放建议、套壁纸/渐变相框、开启光标平滑 + 点击弹跳、可选挂载摄像头气泡；先存 `.recordly` 工程再导出。
- **结果**: 同一套 scene 逻辑分别产出高质量 MP4 与轻量循环 GIF（帧率/循环/尺寸预设可调），README 头图即为"MP4 to GIF export"实测效果。项目由 OpenScreen fork 而来，80% 以上代码已分叉。

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 产品/功能发布：要一支带缩放强调、光标动效、品牌相框的 demo 或 walkthrough 视频。
2. 教学与文档：录操作教程并导出 GIF，内嵌 README / 工单 / 聊天窗口做轻量传播。
3. 存量素材再加工：手里有旧录屏或 `.recordly` 工程，要补标注、变速、换相框后重新导出。

### 语言信号
- "录个产品演示 / 操作教学视频"
- "录屏加自动缩放、光标点击特效"
- "导出成 GIF / MP4"
- "加个背景相框 / 摄像头画中画 / 标注字幕"

### 与相邻 skill 的区分
- 与 rrweb-session-recording 的区别：本 skill 产出**给人看的成品视频文件**（MP4/GIF，桌面级采集 + 后期动效合成）；rrweb 产出**给程序看的结构化事件流**（嵌入网页记录 DOM 变更与交互，用于会话回放/问题复现）。要"发出去的视频"来这里，要"嵌进应用的录制代码"去那里。

## E (Execution) — 可执行步骤

1. **需求定档** — 确认用途（demo/教程/GIF）、目标平台、是否人像出镜。完成标准: 一句话写出"为 X 录制 Y 内容，交付 Z 格式"。
2. **环境与安装检查** — 按平台核对最低版本（macOS 14+ / Win10 19041+ / 现代 Linux），从 releases 下载或 `npm install && npm run dev` 源码运行；本地构建遇 macOS 拦截用 `xattr -rd com.apple.quarantine` 去隔离。完成标准: 应用启动并能看到录制界面。
3. **录制** — 选屏幕或窗口，配好麦克风/系统音频，开始→操作→停止自动进编辑器。完成标准: 素材完整覆盖目标操作路径，无意外弹窗入镜。
4. **时间线剪辑** — trim 废段、采纳/微调自动缩放建议、加速冗余段、补文字标注。完成标准: 无死操作片段，每个关键点均有缩放或标注强调。
5. **视觉合成** — 配置光标平滑/点击弹跳、相框壁纸或渐变、可选摄像头气泡与宽高比。完成标准: 预览中光标清晰、画面有品牌感、无元素溢出。
6. **工程落盘** — 先保存 `.recordly` 再考虑导出。完成标准: 工程文件存在，重开可见全部编辑状态。
7. **导出验收** — 按渠道导出 MP4（质量档位）与/或 GIF（帧率/循环/尺寸预设）。完成标准: 成品在目标渠道实播通过，GIF 循环衔接自然。

## B (Boundary) — 边界

### 不适用场景（≥2条）
- 网页内嵌的**用户真实操作录制与会话回放**（客服复现、行为观察、报错附带现场）→ 属于 DOM 事件流方案，走 rrweb-session-recording。
- **直播/实时推流**：本 skill 是"先录后剪"的离线管线，不具备直播能力。
- 自动化测试的过程截图/录像 → 用 Playwright 等 E2E 工具自带能力。

### 已知局限 / 失败模式（≥1条）
- Linux 下 Electron 捕获无法隐藏真实光标，若再开启渲染光标叠加会出现**双光标**；
- Windows 19041 以下版本回退捕获时真实光标可能残留；系统音频支持随平台而异（Linux 通常需 PipeWire，macOS 需 14+ ScreenCaptureKit 工作流）。

### 隐私红线
- 录制**他人**屏幕（员工、家人、会议参与者）前必须取得明确告知与同意；"偷偷装工具录员工屏幕考核"类请求一律拒绝并说明合规前提。
- 导出前排查画面与音频中的敏感信息（密码框、客户数据、内网地址、私人消息通知弹窗），用 crop/trim 移除后再交付；`.recordly` 工程内含原始媒体引用，外发前须确认源素材无敏感内容。

## 相关 skills
- contrasts-with: rrweb-session-recording（成品视频 vs 结构化事件流回放）

---

## 审计信息
- **验证**: V1 ✓ / V2 ✓ / V3 ✓
- **蒸馏时间**: 2026-08-25；**来源**: webfetch `https://raw.githubusercontent.com/webadderallorg/Recordly/main/README.md`（本地 upstream 目录缺失该仓库；HEAD 路径传输失败后按备选 main 分支获取成功）
