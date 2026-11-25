---
name: game-animation-production
description: Create or integrate game animation and VFX from AI-generated sprite sheets, image sequences, or available video-generation tools; validate frames, timing, and engine integration. Use when a game needs character, UI or VFX animation, when turning a sprite sheet or GIF into engine frames, or when animation timing and frame consistency look wrong.
---

# AI 游戏动效与动画

根据任务选择形式：UI 微动效与受击反馈优先引擎补间或粒子；角色动作、爆炸和特效可使用 AI 生成的动画 GIF，或生成精灵表再切帧。OpenAI Images API 的 GPT Image 2.6 支持 GIF 生成（2–16 帧），需要模型和组织具备相应权限。复杂视频运动只能使用当前实际可用的视频生成工具；不要假设 Codex 文本模型或脚本会生成视频。

Codex 会话中可用图像生成技能时，默认使用内置工具生成或编辑，不需要 API key。插件的直接 API 脚本需在用户明确选择 API 生成且本地配置 key 后调用；GIF 功能依赖模型权限，也可能产生费用。

内置工具的默认生成文件保存在 `$CODEX_HOME/generated_images/`。项目素材要先复制原图到仓库 `doc/temp/`，再做裁切或切帧；运行时文件也保留一份。不要假设内置工具有指定保存路径的参数。

## 生成

1. 查询当前会话实际可用的图像/动画工具及输入输出；优先使用宿主原生生成或编辑能力。不可用时说明缺少什么，由用户选择可接入服务或提供素材；不要声称已生成。
2. 收集主体参考、画风、动作、帧数、网格、画布、透明背景和循环需求。生成精灵表时要求固定视角、统一比例、每帧相同画布和锚点、按从左到右再从上到下排列、无文字与重叠。需要透明背景时优先请求透明输出。
3. 遵守项目的图片备份规则：原图、草稿、裁切图及最终图均按项目要求留存；生成后先备份，再处理。
4. 逐帧检查角色一致性、轮廓、抖动、透明边、动作方向及循环首尾；必要时重新生成或修图。AI 不保证逐帧一致，也不要把视频直接宣称为可用精灵表。

## 切帧与接入

先把 `PL` 设置为插件根目录，或将下方路径改成实际脚本绝对路径：

```bash
python "$PL/scripts/gen_ai_image.py" --prompt "8-frame looping run cycle, same small astronaut, side view, evenly spaced 4x2 sprite grid, transparent background, no labels" --format png --background transparent --out raw/run_sheet.png --backup-dir doc/temp
python "$PL/scripts/split_sprite_sheet.py" --input raw/run_sheet.png --cols 4 --rows 2 --frames 8 --fps 12 --loop --out-dir assets/animation/run --backup-dir doc/temp/run-frames
```

切帧工具只处理已有等网格图片，不调用生成模型。要求尺寸能被网格整除，并拒绝覆盖已有输出目录；`--backup-dir` 指定新目录时先保存帧备份，再复制到输出目录。输出 PNG 序列和通用 `animation.json`，不声称是特定引擎原生格式。按引擎版本创建动画资源、设置 FPS、循环与锚点，运行检查；记录生成来源与授权状态。
