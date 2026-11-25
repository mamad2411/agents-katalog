---
name: promo-video-pipeline
description: "把 Remotion 宣传片按分镜拆成独立工作项并行派发子代理，主线程先冻结共享组件，合并后以真实渲染证据作为完成门。TRIGGER: 宣传片、promo video、分镜并行派发、remotion render、视频渲染、video pipeline、scene 并行产出、AIOS promo、timeline.json 分镜"
installCatalogName: promo-video-pipeline
clients: [codex, claude, gemini, opencode, hermes, grok, workbuddy, pi, zcode, qoder]
scopes: [global, project]
defaultInstall:
  global: false
  project: true
tags: [general, video, remotion, parallel, workflow, verification]
repoTargets: [codex, claude, gemini, opencode, hermes, grok, agents, workbuddy, pi, zcode, qoder]
---

# Promo Video Pipeline

在 `video/` 这个 Remotion 子应用里产宣传片：分镜拆成独立工作项 → 并行派发子代理 → 主线程合并 → 以真实渲染产物作为完成门。命令面以 `video/scripts/render.mjs` 与 `video/package.json` 为准，本文件不发明参数。

## 1. 前置输入（先声明，再开工）

- 分镜脚本 + 证据合同：`video/README.md` 的分镜表（帧区间、画面、字幕）与「画面主张与代码证据」表
  （每条主张 → `file:line`）。派发前以它为准；改画面不改证据表等于交付假主张。
- 场景清单：`video/src/timeline.json` 的 `scenes[].id / label / frames / captions`；当前 8 个场景
  （`hook crash resume route work team proof cta`）、1355 帧、30fps（45.2 秒）、1080x1920 竖版、`compositionId` 为 `AiosPromo`。
- 时长与台词唯一真源：`video/src/timeline.ts` 与 `video/scripts/render.mjs` 读同一份 json，帧区间只在
  `timeline.ts` 累加；字幕只写在 json 里，由 `PromoVideo.tsx` 注入场景。其他文件不得硬编码帧数或自带 cues。
- 片长由旁白决定：json 里的字幕同时是配音稿（`npm run srt` 导出 SRT 给剪映「文本朗读」），所以每一拍的
  `frames / fps` 必须 ≥ 该拍字幕朗读所需秒数（估算器 `video/scripts/narration.mjs`，4.5 字/秒 + 每句 0.12s 换气）。
  `npm test` 的「每拍窗口放得下该拍的旁白」会在砍帧数或加文案时先红 —— 那是硬门禁，不是建议。
- 冻结点：webpack 入口 `video/src/index.ts`（`render.mjs` 的 ENTRY，只做 `registerRoot`）、场景注册表
  `SCENE_BY_ID`（在 `video/src/PromoVideo.tsx`）、场景入参契约 `SceneProps`（`video/src/timeline.ts`）、
  共享 primitive `video/src/components/**`（`stage` `panel` `terminal` `text` `diagram` `ide`）与
  `video/src/theme.ts`（竖版 `layout` / `size` 令牌）由主线程先写定，之后转为只读。
- 入口或共享 primitive 尚未落盘时：主线程自己先写，不派发；否则多个子代理会同时改同一批文件。

## 2. 独立性判定（派发之前必须成立）

- 每个工作项只有一个文件 owner。
- 共享 `video/src/components/**` 的场景**不独立**：主线程先冻结共享 primitive，之后每个子代理只允许新建或编辑自己的 `video/src/scenes/<id>.tsx`。
- `video/src/PromoVideo.tsx` 的 `SCENE_BY_ID` 注册表与 `video/src/index.ts` 由主线程独占改写，子代理不碰入口与注册表。
- `timeline.json` 对子代理只读；要改帧数就回报主线程，由主线程改 json 并重跑 `npm test`。
- 以上任一不成立 → 保持串行，不进入派发。

## 3. 计划与派发（沿用 aios-work-dispatch 约定）

```bash
aios plan start --title "<宣传片目标>" --task "<整片目标>"
aios plan task hook --target video/src/scenes/hook.tsx --allow-write "video/src/scenes/hook.tsx"
aios plan task cta --target video/src/scenes/cta.tsx --allow-write "video/src/scenes/cta.tsx"
aios work --task "<宣传片目标>" --dry-run --json
```

- 先建结构化 plan，让引擎拿到真实 owner 与依赖；再从 dry-run 预览核对工作项、依赖、路径冲突、merge gate。
- 每个节点带 recipe header：`tools` 白名单（写场景 = edit；只做分镜/取证 = read-only）、`model` + 显式 `task-type`（场景绘制声明 `frontend`，程序不从自由文本反推类型）、`max_turns`、`output_schema`。
- `output_schema` 是下游触发条件：schema 校验不过的产物不回传下游，只作为结构化反馈回到本节点。
- 完整 header 与结果 schema 见 `references/dispatch-contract.md`。
- 预览不授权执行：见第 4 节。

## 4. 审批边界（强制）

- 无 `--scene` 的整片渲染（1355 帧，实测 07:06）与 live 模型派发都消耗时间/费用并写大产物，开工前取得用户明确批准。
- live 派发、整片渲染、commit/push 是三道独立批准，前一次批准不外推到后一次。
- 单场景 `--scene` 渲染与单帧 `--still` 属于已批准派发范围内的小颗粒可逆产物。
- 渲染产物不入库：`video/.gitignore` 已把 `out/` 挡在提交之外；提交面只有 `.tsx`、`timeline.json`、文档。

## 5. 命令面（照抄代码）

```bash
cd video && npm run render -- --output out/aios-promo.mp4
cd video && npm run render -- --scene hook --output out/scene-hook.mp4
cd video && npm run render -- --still --frame "14,75,164,250,319,420,489,570,639,700,760,814,900,999,1090,1164,1290,1345"   # 一次 bundle 出多张静帧
cd video && npm run typecheck
cd video && npm test
cd video && npm run srt        # 导出 out/aios-promo.srt 配音稿（与字幕同一真源）
cd video && npm run studio
```

- 参数只有这些：`--output`（默认 `out/aios-promo.mp4`，相对 `video/` 解析）、`--scene <id>`（只渲染该场景帧区间 `from .. to-1`；未知 id 以退出码 1 终止并列出可选 id）、`--still`、`--frame "N,M,..."`（配合 `--still`，默认 `60`，产出 `out/still-<NNNN>.png`）、`--composition`、`--concurrency N`（默认 `max(2, min(cpus-2, 10))`）、`--browser <本机 chrome 路径>`，等价环境变量 `REMOTION_BROWSER_EXECUTABLE`。
- 没有 `--still-output`：静帧路径由帧号决定，别为它加参数。
- 非 TTY 每 +2.5% 打一行进度便于 agent 采集；TTY 为单行动态条。换场景时插一行 `✔ 上一场完成 → 进入 <id> · <label>`。

## 6. 子代理如何报进度（不用 tail 日志）

- 读 `video/out/render-progress.json`：`phase`、`percent`、`renderedFrames`、`totalFrames`、`currentScene`、`currentSceneLabel`、`etaSeconds`、`elapsedSeconds`、`outputMb`、`stitchStage`、`compositionId`、`outputFile`、`concurrency`、`updatedAt`。
- 写入按 >350ms 节流，`final: true` 立刻写；整片成功的最后一条 `phase` 为 `done`，单帧为 `still-done`。
- 并发渲染会互相覆盖这一个进度文件：同一时刻只让一个渲染持有 `out/`，其余子代理用各自的 `--output out/scene-<id>.mp4` 区分产物。

## 7. 证据门（机械判定）

- 子代理返回结构化结果：`scene_id`、`files_touched`、`typecheck_exit_code`、`still_path`、`scene_render_exit_code`、`segment_output`。
- 主线程合并顺序固定：接线 `video/src/PromoVideo.tsx` 的 `SCENE_BY_ID` → `cd video && npm run typecheck` 退出码 0 → `cd video && npm test` 退出码 0 → 已批准的整片渲染。
- 完成判据四项同时为真：`video/out/aios-promo.mp4` 存在且 size > 0；进度 json 的 `phase` 等于 `done`；`renderedFrames` 等于 `totalFrames` 等于 `timeline.json` 帧数之和（当前 1355）；typecheck 与 test 退出码为 0。
- 竖版排版（面板撞字、diff 出框、字幕折行留孤字、轨道压进度条）只有静帧能暴露，代码审查看不见：整片渲染前先出上面那组验收帧，逐张看过。
- 验收帧要按 `场景起点+14` 覆盖每一拍的**入场窗口**，不能只抽落定时刻：落定帧全绿、成片里却有一整秒空屏是真实发生过的缺陷（900 帧那一版的 `team` 卡片等到 local 30 才淡入，整片第 547 帧中间整块空）。判据是「这一拍内任意一帧都不留无内容的大块空白」，不是「这一拍结束时长什么样」。
- 改帧数（重切节奏、拉长片长）会让每一拍边界右移，入场验收帧号必须按新起点重新算，旧帧号落在新时间轴上是另一拍的画面。
- 整片渲完后用仓库自带的 ffmpeg 从**成片**里回抽问题帧复核（`video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -i out/aios-promo.mp4 -ss <帧号/30> -frames:v 1 out/recheck.png`）：静帧从源码渲染，编码后的真实画面才是观众看到的。
- 分辨率与时长用仓库自带的 ffprobe 核对（本机没有全局 ffmpeg）：`video/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe -v error -show_entries format=duration:stream=width,height -of default=nw=1 out/aios-promo.mp4`。
- 任一判据为假 → 交出失败证据（命令、退出码、错误摘要），不报告完成；声称完成前走 `verification-before-completion`。
- `video/tests/` 缺失时 `npm test`（`node --test "tests/*.test.mjs"`）以非零退出码失败：把它记成待补的门禁，不当作已验证。

## 8. 失败与恢复

- 单场景渲染失败：同 id 重试一次且必须附带变化的假设（错误摘要 + 改动点），否则不重试。
- 浏览器启动失败：按 `render.mjs` 的提示显式传 `--browser` 指向本机 Chrome。
- 中断后用 `aios work --task "<宣传片目标>" --session <session> --retry-blocked`，先复核 owner、批准与命令面。

## 谁决定什么

- 模型：分镜能否拆成独立工作项、`task-type` 声明、证据是否已齐。
- 代码：帧区间、退出码、产物存在性、进度 json —— 程序只读这些客观事实，不猜意图。
- 用户：live 派发、整片渲染、commit/push 的批准。
