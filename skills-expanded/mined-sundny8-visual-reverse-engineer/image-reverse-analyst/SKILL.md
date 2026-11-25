---
name: image-reverse-analyst
description: 图片反推专家（只做图片，不做视频）。上传一张图片后固定输出三段式结果：风格分析 → 可直接使用的中文图片生成提示词 → 严格 schema 的全英文 JSON。覆盖主体、构图、摄影、光影、色彩、材质、风格、情绪、文字、象征十大维度，并区分 OBSERVED / INFERRED / UNCERTAIN 三级可信度。当用户要求「反推这张图」「这张图是什么风格」「分析图片风格」「提取图片 JSON」「图片转提示词」「生成图片结构化描述」时使用。Analyzes a single image and returns style analysis, a Chinese image prompt, and a strict English JSON. Image only, no video.
agent_created: true
---

# 图片反推专家

## 用途

从用户上传的**一张图片**中反向分析视觉信息，推导出一套能重新生成相似画面的高质量提示词。

固定输出三段：**风格分析 → 中文图片提示词 → 全英文 JSON**。

定位是 **Image Reverse Engineering**，不是 Image Captioning。

| 图片描述器 | 本技能 |
| --- | --- |
| 「一个女人站在窗边，光线很柔和」 | 「85mm 焦段、浅景深、侧窗硬光 45°、主体压左三分点、暖调低反差」 |
| 一段文字 | 风格分析 + 中文提示词 + 结构化 JSON |
| 随口编参数 | 区分 OBSERVED / INFERRED / UNCERTAIN |

## 适用范围

**只处理图片。** 用户上传视频时不要用本技能，改用 `visual-reverse-engineer`（支持视频模式与连续性锁定）。

## 工作流

严格按顺序执行，**观察在前，生成在后**。

**Step 1 — 十大维度观察**
A 主体 / B 构图 / C 摄影 / D 光影 / E 色彩 / F 材质 / G 风格 / H 情绪 / I 文字 / J 象征。
读 `references/analysis-dimensions.md` 与 `references/style-mood-symbolism.md`。

**Step 2 — 标注可信度**
每一项标为 `OBSERVED` / `INFERRED` / `UNCERTAIN`。读 `references/uncertainty-and-safety.md`。

**Step 3 — 安全替换**
遇到敏感、不适宜或高风险内容时，用安全的视觉替代表达，不重复敏感词。读 `references/uncertainty-and-safety.md`。

**Step 4 — 重组中文提示词**
按 12 级优先级重组成一份完整、可直接使用的中文 Prompt。读 `references/reverse-prompt.md`。

**Step 5 — 生成英文 JSON**
严格按固定 schema 输出，全英文。读 `references/json-schema.md`。

**Step 6 — 按三段式输出**
格式固定，不得增删区块。读 `references/output-format.md`。

## 参考文件路由

| 需要什么 | 读哪个文件 |
| --- | --- |
| 十大分析维度（主体/构图/摄影/光影/色彩/材质） | `references/analysis-dimensions.md` |
| 风格 / 情绪 / 文字 / 象征 | `references/style-mood-symbolism.md` |
| 提示词重组与 12 级优先级 | `references/reverse-prompt.md` |
| JSON schema 与质量要求 | `references/json-schema.md` |
| 三级可信度与安全替换 | `references/uncertainty-and-safety.md` |
| 三段式固定输出格式 | `references/output-format.md` |
| 完整成品范例 | `references/examples.md` |
| 单段式完整提示词（给只吃 system prompt 的工具用） | `references/full-prompt.md` |

## 硬性约束

**风格必须首先回答。** 第一段开头就是「风格：XXX」，先定风格，再展开其他分析。这是本技能的固定结构。

**角度只能给近似值。** 可以写 `head turned approximately 15 degrees`、`three-quarter view`、`profile view`。
**但不要假装精确到无法从图片判断的程度。** 看不出就是看不出，标 `UNCERTAIN`。

**材质不能只写"high detail"。** 必须解释细节是什么、以及为什么产生这种质感。
```
Correct:  natural skin pores, subtle facial micro-texture, fine hair strands,
          realistic fabric weave, soft specular highlights, slightly weathered surface
Wrong:    highly detailed, high detail, ultra detailed
```

**不得编造图片中不存在的文字。** 没有文字就填 `"None"`。

**不得强行过度解读象征意义。** 没有明显象征就用固定句式：
```
concept: "No obvious symbolic concept"
representation: "The image primarily communicates through visual aesthetics and composition."
```

**绝不要声称"这就是原始 Prompt"。** 正确表述：这是根据最终图像反向重建的高概率 Prompt。

**JSON 必须严格合规**：valid JSON、只用双引号、无注释、无尾逗号、全英文、无 Markdown、无中文字符、无编造内容、无无依据的断言。缺项填 `"None"`。

**禁止空词堆砌**：
```
❌ masterpiece, best quality, ultra amazing, perfect, extremely detailed ×20
✅ 具体的视觉描述
```

## 输出契约

固定三段，标题照抄：

```
① 风格分析
风格：XXX

风格特点：
* XXX
* XXX
* XXX
* XXX

为什么判断为这种风格：
XXX

相近的视觉语言：
XXX

② 图片生成提示词
<一份完整、可直接使用的中文 Prompt>

③ JSON Prompt
<严格 schema 的全英文 JSON>
```

**注意：中文提示词与英文 JSON 的语言是固定的**——提示词用中文，JSON 全英文。不要颠倒。

详细规范见 `references/output-format.md`。

## 收尾自检

- [ ] 三段齐全，顺序正确，无多余区块
- [ ] 第一段开头是「风格：XXX」
- [ ] 每一项分析都标了 OBSERVED / INFERRED / UNCERTAIN
- [ ] 角度只给近似值，没有假装精确
- [ ] 材质解释了"细节是什么"，不是只写 high detail
- [ ] 无文字时 JSON 里填的是 `"None"`，没有编造
- [ ] 无象征时用了固定句式，没有过度解读
- [ ] 中文提示词覆盖全部 14 个要素
- [ ] JSON 是 valid JSON，全英文，无尾逗号，无注释
- [ ] 没有声称"这就是原始 Prompt"
- [ ] 没有出现 masterpiece / best quality 这类空词
