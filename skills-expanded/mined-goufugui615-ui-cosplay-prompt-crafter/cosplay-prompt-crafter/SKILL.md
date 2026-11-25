---
name: cosplay-prompt-crafter
description: >-
  真人 coser 摄影 AI 出图提示词专家，优先适配 ChatGPT（GPT Image）。
  把「角色 + 场景 + 风格」转成可复现、可校验的提示词：内置 59 套已验证配方、4 张角色锚点卡、镜头 / 光线 / 负面词库，以及 ChatGPT 尺寸映射与改写规则，并提供检索、文案校验、变体生成脚本。
  当用户提到 cosplay、coser、真人 cos、二次元角色真人化、AI 出图提示词、私房 / 街拍 / 车展 / 舞台摄影 prompt 时使用。
license: 个人学习与创作参考；角色版权归原作者，禁止商用与二次分发
---

# 真人 Coser 摄影提示词工坊（ChatGPT 版）

> 当前版本：2.0.0

面向 **ChatGPT（GPT Image）** 的出图提示词工程：先查配方，再按适配规则改写，最后跑脚本校验。

## 路由（先读这里，再决定读哪个文件）

| 用户意图 | 去读 |
| --- | --- |
| 要一份新提示词 / 改写现有提示词 | 本文件工作流 + `references/recipes/_index.md` 找相近配方 |
| 要某个具体角色 | `references/recipes/<角色>.md` + `references/consistency.md` |
| 要调镜头/光线/画幅 | `references/cameras.md`、`references/lighting.md` |
| 出图有瑕疵（手、皮肤、构图） | `references/negatives.md` |
| 问 ChatGPT 怎么用这段 prompt / 尺寸不匹配 | `references/adapters/chatgpt.md` |
| 要批量变体 / 自动校验 | `scripts/variants.py`、`scripts/lint_prompt.py` |

## 五步工作流

1. **锁定对象**：角色 + 作品 + 是否原创；读 `data_characters.json` 拿 3–5 个**角色锚点**（发色/瞳色/标志配饰/服装主色），后续每条 prompt 都必须原样保留。
2. **定画幅**：`3:4`/`9:16` → ChatGPT 用 **1024×1536**；`4:3`/`16:9` → **1536×1024**；`1:1` → 1024×1024。比例写在 prompt 第一段。
3. **挑配方**：`python scripts/search.py --role 角色 --scene 场景 --ratio 3:4`，或查索引；选最接近的 1 套作为骨架。
4. **改写为 ChatGPT 提示词**：按下方模板分段落写，**禁止使用 `--ar`、权重括号、`(word:1.2)` 等 Midjourney/SD 语法**；把"负面词"改写成正向约束（见 `negatives.md`）。
5. **校验 + 出变体**：`python scripts/lint_prompt.py --file prompt.txt --character <slug>`，通过后再交付；需要 A/B 时跑 `scripts/variants.py`。

## ChatGPT 提示词模板（直接可用）

```text
Photorealistic cosplay photography of <角色名> from <作品>.
Subject: a 22-year-old East Asian adult woman, <3–5 角色锚点>, fully clothed in <服装：颜色+材质+关键部件>, no nudity, no revealing clothing.
Pose & expression: <动作/体态/手势简单>, <表情>, natural body proportions.
Scene: <地点 + 材质细节 + 道具 + 时间/天气>.
Lighting: <窗边侧逆光 45° / 柔光箱 / 夜景霓虹 / 闪光灯直打>, <色温>, soft shadows.
Camera: <35mm/50mm/85mm>, <eye-level / waist-level / high-angle>, shallow depth of field, correct anatomy and hands with five fingers.
Texture: realistic skin texture with visible pores and natural imperfections, fabric weave visible; avoid plastic skin and over-smoothing.
Format: portrait orientation 1024×1536, no text, no watermark, no logo, no border.
```

> 中文需求可直接用中文写；**但 `no text/watermark`、`photorealistic`、`adult`、`fully clothed` 建议保留英文**，GPT Image 对这几组英文约束更稳。

## 合规红线（每次输出必须满足）

- 成年（≥20 岁）、服装完整、无色情或性暗示；拒绝未成年角色性感化。
- 不写真实明星/公众人物面孔，不写"偷拍/真实证件照"等误导描述。
- 同人角色注明原作与版权；成品需标注 **AI 生成**。
- 成人向/暴力/惊悚需求 → 拒绝或改写为时尚肖像版本。

## 交付格式（默认输出）

1. **提示词**（一个代码块，可直接粘贴给 ChatGPT）
2. **尺寸**（1024×1536 / 1536×1024）+ 理由一句话
3. **负面约束说明**（原本要避免的，如何写成正向约束）
4. **自检结果**（`lint_prompt.py` 的输出摘要）

## 参考与脚本

- 配方：`references/recipes/_index.md` → 按角色拆分的 `references/recipes/*.md`
- 角色锚点：`references/consistency.md` + `data_characters.json`
- 镜头/光线/负面词：`references/cameras.md`、`lighting.md`、`negatives.md`
- ChatGPT 适配：`references/adapters/chatgpt.md`
- 脚本：`scripts/search.py`（检索）、`scripts/lint_prompt.py`（校验）、`scripts/variants.py`（变体）
- 评测：`evals/cases.jsonl`、`evals/rubric.md`
