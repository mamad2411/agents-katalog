---
name: atomic-scene-motion
description: Build complete non-presenter animation scenes using parameterized templates for UI focus, object handoff, routing, geometry, charts and gallery selection. Choose boundaries by complete visible actions rather than a fixed duration. Use for fine-grained explainer scene design inspired by target-video references.
---

# 完整动作场景模板

这是动作级制作技能。每个实例保留一个完整可见过程，以主体、目标和结果定义边界，不设 5 秒或其他固定时长限制。一次选择到落位、一次分支判断、一次反馈回路应完整呈现。多个独立结果可以拆为连续场景，保持对象 ID、摄像机和最终状态衔接，不强制硬切镜头。

本文件与同目录 references 可独立使用，不依赖原视频或 motion-skills；原片只用于审美校准。保留 55 个非真人动作配方；A47（真人录制倒数）、A48、A58 已移除且不复用编号。A14 等结尾可以合理停留，须注明阅读或收尾用途。真人出镜、真人旁叠加图形、录制人物预览均不纳入参考片段与模板；素材库缩略图中的人物属于界面内容，不作为真人讲解模板。

## 制作顺序

1. 把解释拆为可见动词：选择、连接、过滤、展开、到达、验证。每个动词选择一个模板。
2. 填写下方实例结构，读 [55 个动作配方](references/recipes.md)，再按对应的 [实现内核](references/implementation.md) 制作。一个完整场景可包含多个配方阶段，如 A44→A45→A46；不能把每一阶段机械导出为独立场景。
3. 先定资产和输入/输出状态，再定路径。不能用空白卡片代替素材、用随机摆动代替执行结果。
4. 本项目旁白使用 CosyVoice；最终音频经 Seqvio 实际对齐后生成语义锚点。按完整动作和语义锚点调整时长，不以秒数强行切开动作或旁白。cue 级时间不等于逐词时间。
5. 先看 0%、25%、50%、75%、100% 状态，再正常速度播放；检查对象交接与因果。未实际播放和听审时如实标注，不声称已通过。

## 必填实例

以下是作者规格，不宣称是 Seqvio 的原生 schema。通过项目的实际适配器生成时间线。

```json
{
  "id": "choose-photo",
  "template": "A45",
  "durationSeconds": 2.4,
  "assets": [{"id": "photo-3", "path": "assets/photo-3.webp"}],
  "inputs": {"selectedId": "photo-3", "sourceRect": [0.52, 0.35, 0.18, 0.22]},
  "outputs": {"selectedId": "photo-3", "targetRect": [0.30, 0.24, 0.40, 0.50]},
  "action": "cursor selects photo; photo lifts; other thumbnails recede",
  "anchor": {"cueId": "narration-04", "phrase": "选中这张图片", "event": "selection"},
  "handoff": {"nextTemplate": "A46", "preserve": ["photo-3", "cropFocus", "targetRect"]},
  "sound": {"event": "selection", "asset": null},
  "validation": ["same image", "cursor hits transformed rect", "no crop jump"]
}
```

归一化坐标相对于合成画布，矩形数组依次为 x、y、width、height。跨镜继承的是物体变换后的实际状态；不能把目标矩形直接当作未经摄像机变换的局部坐标。

## 节奏和同步约束

- 单元应有准备、主动作、结果三阶段。可从 0-20%、20-75%、75-100% 起调；具体曲线和比例是制作建议，非对原片工程的测量。
- 密集信息需要阅读时，减少当镜内容，或拆出下一步高亮/比较单元。不得为了满足短时长把旁白或代码加速到不可理解。
- 演示点击、撞击、落位等音效绑定实际视觉事件帧，并扣除音效文件内部起音偏移。分开记录语言锚点和音效锚点。
- 帧率决定视觉时间精度。30 fps 一帧约 33.3ms，不能声称已验证 10ms 级同步。测量并记录输出音频采样率、视觉事件帧和实测误差。
- 不规定每个动作都配 whoosh/click；音效说明视频尤其要保留对比和听辨空间。波形必须由实际演示音频生成。

## 放行检查

时长 d > 0 且由完整过程决定；至少一个可解释状态变化，或明确标注阅读/结尾；没有真人出镜；输入输出资产有效；画面只突出一个主动作；光标、连线不脱离目标；颜色和比例有语义；文字在目标输出尺寸可读；跨场景对象没有无意跳变；随机 seek 与顺序播放一致。

品牌、资质、百分比、人物形象须换成当前项目可用且准确的内容。禁止把模板编号、参考时间码、场景名、调试文字自动加到成片左上角。资产来源和调试信息存入制作报告。
