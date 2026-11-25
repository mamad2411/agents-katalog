---
name: apiz-use
description: 场景化指导agent使用apiz完成电商作图、视频生成、角色设计、图片本地化等实际任务，包含可复制的命令模板、提示词框架和避坑指南
---

# apiz-use — APIZ 场景化实战指南

本skill提供apiz在真实业务场景下的工作流指导、可直接复制的命令模板和经过验证的提示词框架，帮助agent高效完成各类AI生成任务。

## 何时使用本skill

当用户提出以下类型需求时，必须引用本skill：
- 🛒 电商相关：淘宝/天猫主图重构、产品海报、九宫格宣传图、手绘风格海报
- 🎬 视频相关：产品宣传视频、分镜短剧、原生对白视频、故事板转视频
- 🧑 角色相关：原创角色设计、角色一致性保持、微表情控制
- 🌐 本地化相关：图片文字翻译、多语言版本、模特本地化替换
- 🔧 工具相关：淘宝/天猫素材批量下载、Codex/CLI环境配置

## 快速决策树

```
用户需求
├─ 生成/编辑图片
│   ├─ 电商主图/产品图/海报 → references/10-ecommerce-image.md
│   ├─ 图片翻译/换文字/换模特 → references/40-image-localization.md
│   └─ 角色人设/表情 → references/30-character-design.md
├─ 生成视频
│   ├─ 产品宣传/故事板/九宫格/对白短剧 → references/20-video-generation.md
│   ├─ 提示词结构/镜头语言/分镜拆分 → references/21-seedance2-deep-guide.md
│   ├─ 图生视频稳定性/角色一致性 → references/21-seedance2-deep-guide.md
│   ├─ 音画同步/旁白TTS/字幕对齐 → references/21-seedance2-deep-guide.md
│   ├─ 筛选剪辑/延长融合/成片检查 → references/21-seedance2-deep-guide.md
│   └─ Vlog/产品/角色/国风/儿童/科普实战 → references/21-seedance2-deep-guide.md
├─ 批量下载电商素材 → references/50-cli-workflows.md
└─ 需要命令/参数参考 → references/00-command-cheatsheet.md
```

## 核心原则（必须遵守）

1. **先确认再批量**：重要需求先出1张样图确认风格、产品不变形，再批量生产
2. **必须先上传图片**：所有参考图必须通过 `apiz upload` 上传到APIZ CDN，不要直接使用电商平台URL（防盗链会导致拉图失败）
3. **视频必加负向约束**：所有视频提示词必须包含「不要分屏/不要边框/不要字幕/不要水印/不要logo/不要直接展示故事板纸面」
4. **原生对白写进提示词**：不要用 `audio_files` 参数注入音频，台词直接写在视频提示词里，用时间轴标注
5. **注意JSON转义**：shell中 `--params` 后面的JSON必须转义双引号：`--params "{\"key\":\"value\"}"`
6. **代词要明确**：提示词中避免使用「它/这个/那个」等代词，换成具体名词（如「这个产品」→「电动车挡风被」）
7. **生成前查余额**：批量任务前运行 `apiz account balance --json` 确认积分充足
8. **视频超时换模型**：`st-ai/super-seed2-lite` 偶发卡 70% 超时，重要任务优先用 `fal-ai/kling-video/o3/pro/image-to-video`（成功率 ~100%）；失败后不要同参数硬重试，先缩短时长或换模型

## 积分价格参考

| 模型 | 类型 | 价格 |
|------|------|------|
| `openai/gpt-image-2/edit` | 图片编辑 | 64积分/张（1K/high，实测） |
| `st-ai/super-seed2-lite` | 视频生成 | 80积分/秒（5s≈250-400积分） |
| `fal-ai/kling-video/o3/pro/image-to-video` | 图生视频（稳） | 80积分/秒（5s=400积分） |

## 文件索引

| 文件 | 内容 |
|------|------|
| `references/00-command-cheatsheet.md` | 完整CLI命令速查、参数表、JSON转义指南 |
| `references/10-ecommerce-image.md` | 电商图片工作流：主图、九宫格、海报 |
| `references/20-video-generation.md` | 视频生成工作流：分镜、对白、产品宣传 |
| `references/21-seedance2-deep-guide.md` | Seedance 2.0 深度指南：提示词/镜头/分镜/图生视频稳定性/音画同步/筛选剪辑/6类实战模板（基于12篇官方教程） |
| `references/30-character-design.md` | 角色设计：一致性保持、微表情控制 |
| `references/40-image-localization.md` | 图片本地化：翻译文字、替换模特 |
| `references/50-cli-workflows.md` | 工具链：素材下载、环境配置 |
| `references/prompt-library.md` | 提示词模板库，直接复制修改 |
| `references/troubleshooting.md` | 常见错误排查 |
