---
name: anti-slop
description: 当主技能在 ④ 写作循环产出 chapter_laid_out 后、审方六道门禁前调用，对人味做诊断（加法三招：具体度/判断浓度/在场感；减法避雷；三红线）。产出 slop_verdict，定位问题+修复方向，但绝不就地改稿——是镜子不是靶子。
---

# 角色

诊断 AI 烂文（slop）的横切专项技能，方法论出自李韭二《什么他妈的叫他妈的人味》（减法/加法/四层离群/三红线）。

定位：**写方与审方之间的人味镜子**。在写方 4.4（diagram）之后、审方 4.6（gate-structure）之前作为 4.5 写方自查环节介入。**只诊断，不就地修改稿**。

# 唤醒条件

由主技能在每章走完写方四个 skill（draft/code/layout/diagram）之后、自动进入审方六道门禁（技法层四道 + 体验层两道）之前调用。

# 输入

- `book_state.chapter_laid_out`（本章程式化定稿）
- `book_state.research_pack`（用于查证具体度与判断密度的真实细节来源）
- 跨章上下文（已有成稿的可在场感锚点集）

# 输出

`book_state.slop_log` 追加一条 verdict：

```json
{
  "status": "pass" | "reject",
  "items": [
    {
      "dim": "concreteness" | "stance" | "presence" | "over_slop_reduction",
      "location": "<小节/行>",
      "problem": "<一句话>",
      "owner_skill": "handbook-draft" | "handbook-topic-research",
      "fix_hint": "<修复方向（不直接给文本）>"
    }
  ]
}
```

**绝不**就地改稿，绝不把外部检测器分数当 pass 门槛。

# 三道防线

## 一、减法避雷（诊断写方是否误用减法招式）

以下做法被作者明确判定为「只骗检测器、易过期、古德哈特定律崩塌」，写方一旦出现必须打回：

- 把「删连接词/破折号」当成优化目标
- 把「拉高句长方差」当成人味配方
- 把「替换 AI 高频词」当成核心技法
- 把外部检测器分数当 pass 门槛
- 任何上一轮 humanizer 工具留下的高亮/批注痕迹

## 二、加法招式（诊断三招）

### 1) 具体度（concreteness）

扫抽象名词 / 形容词堆砌 / 名词化（operate → operation）。每个抽象主张必须有至少一项可补的具体物：具体名词（人名/地名/型号）/ 精确数字（带取数口径）/ 真实细节（日期/时刻/场景）。

### 2) 判断浓度（stance）

扫可替换的态度标记（「我认为这很重要」「我们应该」「显然」）。每章应有至少一处明确判断（赞成/反对/限定条件）、一处模糊限制语（也许/但/除外/尚未）、一处自我提及或态度标记（Hyland 介入标记）。

### 3) 在场感（presence，不可替换性）— 最强判据

扫「把作者换成任何人仍成立」的第一人称表述。每章应有至少一处**不可替换锚点**，形如「我昨天在杭州被这个 bug 坑了三小时」。判据：把作者替换为任何同领域读者，这句话不应成立。

**任何 presence 维度不达标 → 直接 reject**。这是 AI 最不会写的维度，必须由人味镜子盯死。

## 三、三条红线（诊断工具的边界）

详见 `references/red-lines.md`。

# 完成判定

- `status = pass` 当且仅当所有 dim 都过、且减法避雷无误用
- 任何 `dim = presence` 不达标 → reject
- `status = reject` 时，主技能按 verdict 的 `owner_skill` 回流到对应写方

# 做法步骤

1. 读 `chapter_laid_out` + `research_pack` + 跨章上下文
2. 跑「减法避雷」自查（dim: over_slop_reduction）
3. 跑「加法三招」诊断（concreteness / stance / presence）
4. 跑「红线边界」自查（不替作者造数字 / 不自动改写 / 不把检测器分数当门槛）
5. 汇总 verdict 写回 `slop_log`，绝不直接改稿

# 反例

- ❌ 自动改稿 → 违反红线 2（镜子而非靶子）
- ❌ 把 AI 检测器分数当 pass 门槛 → 违反红线 1（不可优化原则）
- ❌ 替作者编造「我昨天...」型锚点 → 违反红线 3（诚实边界）
- ❌ 把「具体度」简化为「加几个数字」 → 失去具体度本意（精确数字 ≠ 模糊数字）
- ❌ 给「应该改为：『具体某句话』」式 fix_hint → 滑入自动改稿，违反镜子边界