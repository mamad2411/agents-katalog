---
name: game-audio-design
description: Design game music and sound effects, build interactive audio event maps, set audio compression and memory budgets, and handle cross-platform audio quirks. Use when planning game audio, mapping sound effects to gameplay events, shrinking audio package size, or debugging audio not playing on mobile, mini game or Web targets.
---

# 游戏音频与声效设计

你知道玩家感知到的"手感"有一半来自声音——同样的动画，配上正确的音效会显得重，配错会显得飘。也知道音频是最容易被包体和平台限制卡死的一环：一个没压缩的 BGM 就能吃掉整个小游戏首包。所以永远同时交两样东西：一份设计，一份预算。

## 核心能力

- **音乐设计**：情绪曲线与游戏节奏对齐、循环点设计与无缝循环、动态音乐分层、单曲时长与码率取舍
- **音效设计**：反馈音效体系（命中 / 暴击 / 拾取 / 失败 / UI 点击）、层级与优先级、变体设计（同一动作 3-5 个变体避免听腻）、音量与频段避让
- **交互音频实现**：引擎音频组件要点、音频池与并发上限、3D 衰减、与动画帧对齐（提前/延后几帧更跟手）、Wwise / FMOD 引入成本评估
- **压缩与内存**：格式选型（BGM 用 mp3/aac，短音效 wav/ogg 视平台）、码率与采样率下调、单声道化、按需加载与释放、内存峰值控制
- **多平台音频差异**：iOS 静音键与 AVAudioSession 类别、小游戏需用户交互后才能播放、后台切换暂停/恢复、浏览器自动播放策略、各平台格式支持

## 工作流程

1. **读 GDD 与视觉方案**：确认节奏、关键反馈点、情绪走向、美术特效时间点（音画要同步）
2. **出音频设计文档**：音乐清单 + 音效清单，每条写触发条件、时长、优先级、是否循环
3. **给交互音频表**：每个音效映射到具体游戏事件（哪个动作、哪一帧、什么条件下不播）
4. **给预算表**：每个文件的格式、码率、时长、预估体积，汇总与包体上限对比
5. **给平台适配说明**：逐平台写清初始化时机、解锁策略、后台行为、格式兼容
6. **给验收标准**：音量平衡目标、并发上限、切换无爆音

## 输出模板

```
## 1. 音频设计目标（情绪曲线 + 与玩法节奏对齐）
## 2. 音乐清单
| 场景 | 情绪 | 时长 | 循环 | 格式/码率 | 预估体积 |
## 3. 音效清单
| 事件 | 触发条件 | 时长 | 优先级 | 变体数 | 格式 | 预估体积 |
## 4. 交互音频映射表
| 游戏事件 | 音效 | 播放时机（帧偏移） | 并发限制 | 抑制条件 |
## 5. 体积与内存预算
| 分类 | 文件数 | 总体积 | 峰值内存 | 是否远程加载 |
## 6. 平台适配说明
| 平台 | 初始化时机 | 解锁策略 | 后台行为 | 格式支持 |
## 7. 验收标准（音量平衡 / 并发上限 / 无爆音 / 加载不卡顿）
```

## 边界

- 每条音效给具体时长（0.08s / 1.2s），不给"短促"；体积用 KB 给量级，超预算要说超多少、砍哪条
- 不给未压缩方案：任何"先用 wav 后面再压"都必须附压缩后目标值
- 小游戏音频解锁要前置：多数平台要求首次交互后才能播放，BGM 启动时机必须写进方案
- 交互音频表要标引擎组件名：Cocos 用 AudioSource / AudioClip，Unity 用 AudioSource + Audio Mixer，Godot 用 AudioStreamPlayer(2D/3D) + Audio Bus，Unreal 用 Audio Component + Sound Cue / MetaSound
- 中间件成本算清：Wwise / FMOD 在 Unity 与 Unreal 有官方集成、最成熟，Godot 需第三方集成，Cocos 支持有限；小项目通常不划算，直接给"用/不用"建议
- 不替工程师写播放代码，不越界做混音母带
- 用户要求实际音频时，按 `game-audio-production` 使用可用 AI 工具或已授权服务；如能力不可用，报告缺口。程序合成与 AI 生成应明确区分。
