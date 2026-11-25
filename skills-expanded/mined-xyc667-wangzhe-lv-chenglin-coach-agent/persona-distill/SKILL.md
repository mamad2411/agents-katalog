---
name: persona-distill
description: >-
  Distills a person from corpus text into DNA-level Persona Skills. Runs a
  4-stage pipeline (fractionate, condense, purify, package) to extract
  expression DNA, mental models, decision heuristics, anti-patterns, and honest
  boundaries. Use when the user asks to distill/extract/refine a person,
  create a persona skill, clone someone's thinking style, or mentions
  人物提炼/人格蒸馏/persona distillation.
---

# 人物提炼 · Persona Distillation

把语料中的「人」蒸馏成可运行的 Cursor Persona Skill。

**核心原则**：捕捉 _HOW they think_，不是 _WHAT they said_。

## 启动检查

开始提炼前，确认以下信息（缺失则向用户询问）：

1. **目标人物**：姓名 / 昵称 / 角色 ID（如 `zhangxuefeng`）
2. **语料来源**：`corpus/<id>/` 本地文件，或用户提供的链接/描述
3. **输出目录**：默认 `personas/<id>/`

## 工作流

复制此清单并跟踪进度：

```
提炼进度 · <persona_id>
- [ ] Stage 0: 语料摄入
- [ ] Stage 1: 分馏
- [ ] Stage 2: 冷凝
- [ ] Stage 3: 提纯 + DNA 五层
- [ ] Stage 4: 灌装 Skills
- [ ] 落盘 + 自检
```

---

## Stage 0: 语料摄入

**有本地语料** → 读取 `corpus/<persona_id>/` 下所有 `.txt` `.md` `.json` `.jsonl`

**只有名字/链接** → 搜索公开资料（文章、访谈、社交媒体、GitHub 等），整理成语料摘要后再继续。标注每条来源。

**语料不足**（< 2000 字有效文本）→ 告知用户并建议补充，或基于有限材料提炼但诚实边界须注明「低置信度」。

分块原则：每块 800~1500 字，块间保留 100 字重叠，避免从句中劈开。

---

## Stage 1: 分馏 · Fractional Distillation

逐块文本，按 **10 类塔板** 分离信号。每类信号附：
- 原文证据（直接引用，≤ 80 字）
- 显著度 salience（0~1）
- 来源文件/块 ID

### 10 类塔板

| 塔板 | 信号类型 | 提取什么 |
|:---:|:---|:---|
| speech | 表达风格 | 口癖、句式、语气、修辞 |
| catch | 金句/口头禅 | 反复出现的标志性表达 |
| values | 价值观 | 什么最重要、什么不可妥协 |
| know | 知识域 | 专业领域、常引用的框架 |
| emo | 情感模式 | 什么触发热情/愤怒/幽默 |
| rel | 关系姿态 | 对上级/下属/粉丝/对手的态度 |
| event | 关键事件 | 塑造人格的经历 |
| bg | 背景 | 教育、职业、地域等 |
| taboo | 雷区 | 绝不碰的话题/行为 |
| man | 人物关系 | 提及的重要他人及态度 |

输出中间文件：`personas/<id>/distillates.jsonl`（每行一条 Distillate）

```json
{"tower":"speech","signal":"短句、极端确定","evidence":"「这太 insane 了」","salience":0.85,"source":"interview.txt#chunk-3"}
```

---

## Stage 2: 冷凝 · Condensation

1. **同类合并**：同一塔板内语义相近的信号合并，salience 取 max
2. **跨文件互证**：≥2 个来源出现同一信号 → salience +0.15（上限 1.0）
3. **矛盾择优**：冲突信号保留 salience 更高、证据更多的

---

## Stage 3: 提纯 · Purification

1. 丢弃 salience < 0.35 的信号
2. 每类塔板保留 3~6 条最高显著信号
3. 同步提炼 **DNA 五层**（详见 [methodology.md](methodology.md)）

### 心智模型三重验证

候选心智模型必须**同时**通过三项才收录（宁缺毋滥）：

| 验证 | 标准 |
|:---:|:---|
| 跨域复现 | 在 ≥2 个不同话题/领域出现 |
| 有生成力 | 能推断 TA 对新问题的立场（须给示例） |
| 有排他性 | 非通用常识，体现独特视角 |

未通过的一律丢弃。

---

## Stage 4: 灌装 · Final Product

生成以下产出到 `personas/<id>/`：

### 4.1 persona_card.json

```json
{
  "persona_id": "<id>",
  "display_name": "<显示名>",
  "summary": "<200字以内人物摘要>",
  "tags": ["标签1", "标签2"],
  "expression_dna": { "vocabulary": [], "rhythm": "", "signature_metaphors": [], "opening_samples": [] },
  "mental_models": [{ "name": "", "principle": "", "cross_domain_evidence": [], "generative_example": "", "exclusivity": "" }],
  "decision_heuristics": [{ "rule": "", "trigger": "" }],
  "anti_patterns": [{ "pattern": "", "reason": "" }],
  "honest_boundaries": [{ "limitation": "", "reason": "" }],
  "error_reply": "<角色化报错回复>"
}
```

### 4.2 persona_card.md

人类可读版，含 DNA 五层摘要 + 三重验证证据。

### 4.3 Skills 目录

至少生成 3 个 Skill（模板见 [templates/persona-skill.md](templates/persona-skill.md)）：

| Skill | 用途 |
|:---|:---|
| `<id>-perspective` | 用 TA 的视角分析/回答 |
| `<id>-refuse` | TA 会拒绝/踩雷的场景 |
| `<id>-deep-dive` | 深度追问、展开论证 |

每个 SKILL.md 必须包含：角色扮演规则、回答工作流、心智模型（含三重验证证据）、决策启发式、表达 DNA、反模式、诚实边界。

### 4.4 preset_dialogues.json

6~8 组预设对话，覆盖：寒暄、探问、踩雷、求助、倾诉、告别。

---

## 落盘自检

完成前逐项确认：

- [ ] `persona_card.json` DNA 五层字段非空（mental_models ≥ 2）
- [ ] 每个 mental_model 有跨域证据 + 生成力示例 + 排他性说明
- [ ] Skills 用第一人称「我」，非第三人称转述
- [ ] honest_boundaries 至少 2 条（说明 skill 局限）
- [ ] anti_patterns 至少 3 条
- [ ] 所有引用有原文证据，无凭空捏造

---

## 激活已提炼人格

用户说「扮演 XX」「用 XX 的视角」→ 读取 `personas/<id>/skills/<id>-perspective/SKILL.md` 并按其规则回应。

首次激活输出一次免责声明，后续不再重复。

用户说「退出」「切回正常」→ 立即恢复默认助手模式。

---

## 附加资源

- 方法论详解：[methodology.md](methodology.md)
- Skill 输出模板：[templates/persona-skill.md](templates/persona-skill.md)
- 示例产出：[examples/sample-output.md](examples/sample-output.md)
