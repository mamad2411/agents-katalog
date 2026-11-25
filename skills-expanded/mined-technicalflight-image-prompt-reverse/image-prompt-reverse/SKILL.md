---
name: image-prompt-reverse
description: 把一张图片逆推成生成提示词（image to prompt）。看图后法证式重建它最可能的原始生成提示词，产出中文与英文两套重建提示词、4×2 风格标签、结构化 JSON prompt、recreation_prompt / prompt_core / negative_prompt，并对双语输出做语言桶校验。当用户说"反推提示词""这张图用了什么 prompt""图片转提示词""解析出这张图的 prompt""照这张图的风格帮我写 prompt""怎么做出这种图"时使用。
agent_created: true
---

# 图片 → 提示词 反推

一句话：给一张图，产出一份能再造出它的提示词（中文 + 英文 + 结构化）。

## 触发判定

- **该用**：反推 / 还原 / 解析某张图的提示词；想知道某张 AI 图、海报、杂志页、商品图是怎么生成的；照某张图的风格写可复用的 prompt。
- **不该用**：只要一句图片描述（直接看图回答即可）；真的要生成图片（走 ImageGen）；修图/去水印（走图像处理类技能）。

## 环境

只有第 3 步需要跑命令，并且**没有任何第三方依赖**：`scripts/validate_analysis.py` 只用 Python 标准库（`argparse` / `json` / `re` / `sys`），不需要安装任何包。

- 需要 Python 3.8 或以上（只用标准库，无第三方依赖；已声明 `from __future__ import annotations`，不使用高版本专属语法）；
- 脚本路径相对于本技能目录，下文命令里的 `<skill>` 指本技能所在目录：

```bash
python "<skill>/scripts/validate_analysis.py" analysis.json
```

脚本也支持从标准输入读取：`cat analysis.json | python "<skill>/scripts/validate_analysis.py" -`。

## 三步

### 1. 把图看进来

- 本地文件 → 直接 `Read`；
- 网址 → 先落盘再 Read：`curl -L -A "Mozilla/5.0" -o shot.jpg "<图片地址>"`（防盗链取不到就请用户存图给路径，别硬刚）；
- 只有"页面上的某张图" → 请用户截图；若环境里有浏览器自动化能力（例如 `agent-browser` 技能），也可以让它截图后取用。

**必须真的读到图像内容再分析**，不要凭文件名或 URL 猜内容。长边超过 2200px 时先压一道再读。

### 2. 按契约产出 JSON

契约在 `references/prompt-contract.md`，按三件东西拼出这一轮的指令：

1. 第 1 节的**分析指令整段**（工作准则 + 观察项 + 产出要求）；
2. 第 2 节的**四项上下文**（来源 / 替代文本 / 像素尺寸 / 画面比例），取不到的写 `N/A`；
3. 第 3 节的**输出 schema**。

然后看图产出 JSON，写成 `analysis.json`。输出结构如下（严格照 schema）：

```json
{
  "zh": { "prompt": "...", "analysis": "..." },
  "en": { "prompt": "...", "analysis": "..." },
  "zh_style_tags": ["...×4"], "en_style_tags": ["...×4"],
  "json_prompt": { "subject": "...", "...": "共 12 个字段" },
  "recreation_prompt": "...", "prompt_core": "...", "negative_prompt": "..."
}
```

三条铁律：

1. **只写可见事实**——不编造品牌、logo、精确文字、艺术家名、机身/镜头型号、渲染引擎、具体地点、隐藏物体；
2. **语言分桶不许串味**——zh 桶简体中文、en 桶英文，标签同理；`json_prompt` 与另外三条提示词一律英文；
3. **人像必须给族裔与肤色线索**——基于可见证据；真的看不清就写明"族裔不可辨"，但肤色与发型照写。

> 模型若额外返回 `ja` 等契约外字段，按契约忽略，不用去修它。

### 3. 校验（必做，别跳）

```bash
python "<skill>/scripts/validate_analysis.py" analysis.json
```

- 退出码 `0` = 通过；`1` = 语言桶勾兑或标签不合格；`2` = schema 缺字段。
- 非 0 时按 `references/validation-rules.md` 的自愈顺序改自己的输出，再跑一遍：
  - 结构坏 / 缺字段 → 用契约 5.1 节的结构修复提示词补；
  - 语言勾兑 → 用 5.2 节的语言修复规则重写该桶（只搬运/翻译，**不许新增视觉细节**）。
- 诊断会打印每桶的汉字/假名/字母计数与阈值，照着改比反复重读输出可靠得多。
- 校验分两层：桶级（prompt + analysis 合并）+ **prompt 单字段**。后者专治"prompt 写错语言、analysis 写对"这种被长文本稀释的漏判。
- 需要规范化标签（去重、英文长标签缩写、截断到 4 条）时加 `--normalize`，会把整理后的 JSON 打到 stdout。

### 交付

`analysis.json` 作为产物文件交给用户，并在回复里直接给出：

- **中文重建提示词**、**英文重建提示词**（正文，方便直接复制）；
- 4 条**风格标签**；
- 说明另外三条的用途：`recreation_prompt`（最完整的复刻提示词，130–220 词）、`prompt_core`（精简可复用）、`negative_prompt`（排除常见伪影）。

## 常见坑

- **别跳过第 3 步**：双语输出最典型的失败是"中文桶混英文""英文桶写成中文"，肉眼扫一版发现不了，校验器一秒给结论。
- **标签要短**：英文标签 1–3 词（<24 字符），过长的由脚本按缩写表处理。
- **quality_modifiers 不许灌水**：`highly detailed`、`masterpiece` 这类空话在契约里被明确禁止替代具体描述。
- **族裔/肤色是强制项而非可选项**，但必须落在可见证据上。
- **不确定就写宽泛但可用的措辞**，不要为了显得具体而编造。

## 文件说明

```
image-prompt-reverse/
├── SKILL.md
├── references/
│   ├── prompt-contract.md    分析指令 + 双语 JSON schema + 两类修复指令（核心资产）
│   └── validation-rules.md   中英语言桶阈值（含 prompt 单字段护栏）、标签缩写表、自愈顺序
└── scripts/
    └── validate_analysis.py  校验与诊断（退出码 0/1/2，支持 --normalize / --json）
```
