---
name: chinese-novelist
description: 分章节创作中文中长篇小说（10–50 章），覆盖立项问答、大纲规划、逐章写作、续写未完成的小说项目和全书校验。用户要求写小说、写连载故事或继续之前的小说项目时使用。单篇短故事或润色已有文本不用本 Skill，改用 lieflat-less-ai-tone。
metadata:
  source: 基于 PenglongHuang/chinese-novelist-skill (MIT License, Copyright (c) 2026 PenglongHuang) 针对 Antigravity 全局规则与流式写入机制做本地衔接修订
---

# 中文小说创作

> **上游致谢与精简包说明**：本 Skill 基于开源项目 [PenglongHuang/chinese-novelist-skill](https://github.com/PenglongHuang/chinese-novelist-skill)（作者：`PenglongHuang`，[MIT License](https://github.com/PenglongHuang/chinese-novelist-skill/blob/master/LICENSE)）构建；本文件为适配 Antigravity 全局规则与 `BidiGenerateContent` 流式工具调用特性的衔接入口。**本精简包仅含本 `SKILL.md` 规则壳，不含 `references/` 与 `scripts/` 子文件——除非用户已按 [`UPSTREAM.md`](https://github.com/anyu0804/antigravity-agent-rules/blob/main/skills/chinese-novelist/UPSTREAM.md) 将上游完整目录拉取到本机，否则请直接按本文件内嵌的各阶段规则执行，切勿调用文件读取工具（`read_file` / `view_file`）在本地查找 `references/...` 或 `scripts/...`，以免触发 `ENOENT` 空耗轮次。**

## 写作原则

1. 用动作、对话和细节呈现人物状态，情绪结论不由叙述者直接宣布。
2. 每章至少一个冲突或转折，推动主线或人物关系。
3. 每章结尾留一个钩子：未解的问题、新的威胁或反转。
4. 人物、设定和时间线以 `01-大纲.md`、人物档案和 `03-连续性记录.md` 为准，前后不得矛盾。
5. **设定集终态与当前状态严格隔离（硬账本约束）**：涉及兵力编制、金钱/积分、装备解锁、人物生死或时空坐标的题材，必须以动态更新的 `03-连续性记录.md`（或工作区总结账本）核算期初余额、本章收支、期末结余与**当前已解锁可用清单**；严禁将设定集里的全书满编终态表当作当前章节已解锁库存直接越界刷出。
6. **真实参数核验与跨章钩子回修**：凡本地设定集未显式写死的真实武器装备参数（装填方式、制导体制、射程包线、功率吨位）、工业/地理史实（设施关停年代、海拔视距、季节气候）及数学编码校验位（如 ISO 6346、弹道飞行时间），落笔前必须按 `SEARCH-ROUTING` 检索核实或用脚本实算，严禁凭记忆脑补缝合；新章若临时调整上一章末尾预告的路线或解锁目标，必须同步用 `edit_file` 回修上一章结尾钩子，安排局部反转前须回查是否违背前文已确立的空间/物理排他前提。

## 与全局规则的衔接

- 项目文件夹建在当前工作区：`./chinese-novelist/{yyyyMMdd-HHmm}-{小说名}/`，不写工作区以外的路径。
- 第三、四阶段不向用户提问，但按全局 §4A 汇报进度：每完成一批章节（默认 5 章）报一句进度，汇报不暂停写作。
- 重写已完成章节属于覆盖已有成果。第二阶段确认时一并取得授权；重写前把原稿存到 `chapters/_prev/`。
- 去 AI 味：每章写完后按 lieflat-less-ai-tone 的规则自检，文学体裁豁免照常适用。不对全书做二次改写。
- **模型阶段分工建议（4c / 4a 协同）**：阶段 1–2（立项问答、`01-大纲.md` 结构推演）与阶段 4（全书连续性、时间线与伏笔回收核查）可使用 `Gemini 4 Carbon` 强化逻辑严密性；阶段 3（逐章正文写作）优先切换至文笔更自然松弛、首字延迟更低的 `Gemini 4 Argon`（建议 `Low` 或 `Medium` 思考档位）。若使用 Carbon 执笔正文，须配合具体对白/叙事节奏正反例软化其默认偏冷静的文档语感。
- **防断流分块落盘（Antigravity `BidiGenerateContent` 整包缓冲规避）**：Antigravity 客户端的 `BidiGenerateContent` 流在服务端生成 `write_file` 工具 JSON 参数时采用整包缓冲（参数全部生成完毕前流处于 0 字节静默），单次写入超过 ~2,500 字极易因后台缓冲超过 90~120 秒而触发流静默中断（`The stream was interrupted` / `stream idle timeout`）。撰写每章正文（3,000–5,000+ 字）时，**严禁单次 `write_file` 一次性写入整章**；必须按场景分 **2–4 段** 落盘（首段用 `write_file` 创建章节文件，后续段落用 `write_file` + `Append: true` 依次追加；**Argon 下每次调用的 `Content` 严格控制在 1,500–2,000 字以内，若当前会话为思考耗时更长的 `Gemini 4 Carbon`，须下调思考档位至 `Low` / `Medium` 并将单次 `Content` 进一步收紧至 1,000–1,500 字以内**）。
- **解码边界污染清洗（防 `$]` 双回复与思考外溢传染）**：Gemini 4 系列在长解码或采样边界偶发错失 EOS 吐出字面量 `$]`、单气泡平行续写下一轮或漏出内部自纠错草稿；一旦某段章节或大纲产物末尾出现 `$]`、自问自答续写或 `</thought>` 残片，进入下一段 `Append` 或下一章前必须先裁除污染尾部，严禁将脏文本留在上下文中引发后续章节自注意力传染。

## 流程

以下各阶段直接按本节说明执行（下方链接均指向原上游 GitHub 仓库网页供人工参考；**本精简包不含本地 `references/flows/` 子文件，请勿调用读取工具查找本地相对路径**）。

### 0 初始化

读取用户偏好。工作区已有未完成项目（`02-写作计划.json` 里还有未完成章节）时，报告当前进度并从断点续写；若工作区未走阶段 1–2 立项而是直接提供了现成设定集与既有章节，动笔续写前必须先通读设定集与既有章节，建立或补齐 `03-连续性记录.md`（含当前已解锁清单与资金/积分期末结余）。不输出欢迎语。
→ 上游参考：[phase0-initialization.md](https://github.com/PenglongHuang/chinese-novelist-skill/blob/master/references/flows/phase0-initialization.md)

### 1 立项问答

- 必答 Q1–Q3：题材与创意、主角、核心冲突。用户已经说过的不再问。
- Q4–Q8（世界观、视角与基调、主题、目标读者、章数与每章字数）一次列出，每项附推荐默认值，用户回“默认”即可。
- 标题：给 3–5 个候选，用户选择或自拟。

→ 上游参考：[phase1-layer1-core.md](https://github.com/PenglongHuang/chinese-novelist-skill/blob/master/references/flows/phase1-layer1-core.md) / [phase1-layer2-customize.md](https://github.com/PenglongHuang/chinese-novelist-skill/blob/master/references/flows/phase1-layer2-customize.md) / [phase1-layer3-title.md](https://github.com/PenglongHuang/chinese-novelist-skill/blob/master/references/flows/phase1-layer3-title.md)

### 2 规划与确认

生成 `01-大纲.md`、人物档案、`02-写作计划.json`，以及空的 `03-连续性记录.md`。一次确认以下内容：大纲、章数与字数、写作模式、是否允许自动重写不合格章节。确认后不再提问。
→ 上游参考：[phase2-planning.md](https://github.com/PenglongHuang/chinese-novelist-skill/blob/master/references/flows/phase2-planning.md)

### 3 写作

- 模式：默认 `serial`，主 Agent 逐章写。`parallel` 只在运行环境能派生写作子代理时可选。
- 每章流程：读本章大纲、`03-连续性记录.md`（核对当前已解锁可用清单、积分/资金期初余额与前文排他约束）和上一章结尾约 500 字（若本章路线相对上章结尾钩子有调整，先同步回修上章结尾） → **按场景分 2–4 段调用 `write_file`（首段新建、后续 `Append: true`；Argon 单次 ≤ 2,000 字，Carbon 单次 ≤ 1,500 字）完成本章写作** → 字数检查 → 去 AI 味自检 → 更新 `02-写作计划.json` 中的章节状态 → 在 `03-连续性记录.md` 追加本章摘要（≤150 字）、新埋的伏笔、已回收的伏笔和人物状态变化。

→ 上游参考：[phase3-writing.md](https://github.com/PenglongHuang/chinese-novelist-skill/blob/master/references/flows/phase3-writing.md)

### 4 全书校验

- 字数统计与目标偏差在 ±10% 以内为合格（若未拉取上游 `scripts/check_chapter_wordcount.py`，直接读取章节文件统计字符数）。
- 字数不合格时，先在原章内扩写或删减。违背大纲或与连续性记录冲突时才整章重写。每章最多 3 轮。
- 结局：全部合格报 `PASS`；仍有不合格章节报 `FAIL`，列出章号和原因。

→ 上游参考：[phase4-validation.md](https://github.com/PenglongHuang/chinese-novelist-skill/blob/master/references/flows/phase4-validation.md)

## 共享机制

偏好系统、写作计划 JSON 结构、字数检查脚本。
→ 上游参考：[shared-infrastructure.md](https://github.com/PenglongHuang/chinese-novelist-skill/blob/master/references/flows/shared-infrastructure.md)
