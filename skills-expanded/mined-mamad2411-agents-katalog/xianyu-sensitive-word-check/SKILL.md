---
name: xianyu-sensitive-word-check
description: 检测文案是否触发闲鱼平台敏感词、违禁词或极限词。Use when the user asks to check/copy for 闲鱼敏感词、违禁词、极限词、广告法禁用词, validate product descriptions before publishing on 闲鱼/Xianyu, or review whether text may cause listing takedown or account penalties.
---

# 闲鱼敏感词检测

## 触发后第一步

1. 读取词库：[word_categories.md](word_categories.md)
2. 读取 Skill 内置扩展词库（逗号分隔 txt）：
   - [data/builtin/product_banned_words.txt](data/builtin/product_banned_words.txt) — 商品违禁词（397 条）
   - [data/builtin/copyright_words.txt](data/builtin/copyright_words.txt) — 商品版权词（1561 条）
   - [data/builtin/piracy_violation_words.txt](data/builtin/piracy_violation_words.txt) — 平台盗版违规词（193 条）
3. 若存在 [data/custom_words.txt](data/custom_words.txt)，合并进检测范围
4. 对用户提供的文案执行检测，按下方流程输出报告

## 检测流程

```
检测进度：
- [ ] 1. 原文预处理（去多余空白，保留语义）
- [ ] 2. 词库精确匹配（含大小写、全半角变体）
- [ ] 3. 谐音/拆字/符号间隔变体匹配
- [ ] 4. 正则模式匹配（手机号、链接、社交账号）
- [ ] 5. 上下文语义审查（隐晦引流、私下交易）
- [ ] 6. 输出分级报告与修改建议
```

## 匹配规则

### 精确与变体

对词库中每条词，同时检查：

| 变体类型 | 示例（词：微信） |
|---------|----------------|
| 大小写 | 微信、VX、vx、Vx |
| 全半角 | 微信、微　信 |
| 谐音替换 | 威信、薇信、维信 |
| 符号间隔 | 微-信、微*信、微 信 |
| 数字替换 | 微1信、微Ⅹ信 |

变体检测逻辑：去除空格、标点、特殊符号后做子串匹配；英文词忽略大小写。

### 正则模式（命中即报）

```text
手机号：1[3-9]\d{9}（含空格/横线分隔写法）
固话：0\d{2,3}[-\s]?\d{7,8}
邮箱：[\w.-]+@[\w.-]+\.\w+
网址：http(s)?://、www.、.com/.cn/.net 等 TLD
社交号：微信/vx/v信/qq/QQ号/抖音号/小红书号 + 数字或字母串
```

### 语义风险（无精确词库命中时也需标注）

- 暗示绕过平台：「不走闲鱼」「私下转」「加我看货」
- 绝对化承诺：「全网最低」「假一赔万」「100%正品」
- 医疗功效：「治疗」「根治」「药到病除」
- 违禁品类暗示：「高仿」「1:1」「原单」「尾单渠道」
- 平台风控高频词：「论文」「论文分析」「教育」等，即使非售卖语境也可能触发机器审核

## 风险等级

| 等级 | 含义 | 典型类别 |
|-----|------|---------|
| 🔴 高危 | 大概率下架/限流/封号 | 引流、私下交易、违禁品、色情暴力、商品违禁词、版权词、盗版违规词、平台风控词 |
| 🟠 中危 | 审核拦截或人工复审 | 极限词、虚假承诺、医疗功效 |
| 🟡 低危 | 可能触发机器审核 | 模糊营销用语、边界极限词 |

## 输出格式

必须使用以下模板回复：

```markdown
## 闲鱼敏感词检测报告

**检测结论**：[通过 / 存在风险 / 不建议发布]

**统计**：高危 N 处 | 中危 N 处 | 低危 N 处

### 命中明细

| 等级 | 命中内容 | 类别 | 位置/上下文 | 建议 |
|-----|---------|------|------------|------|
| 🔴 | ... | 外部引流 | 「...加微信...」 | 删除联系方式，改用平台内沟通 |

### 修改建议

1. [具体可执行的改写建议]
2. ...

### 合规改写示例（可选）

原文：……
改写：……
```

无命中时：

```markdown
## 闲鱼敏感词检测报告

**检测结论**：通过

**统计**：高危 0 | 中危 0 | 低危 0

当前文案未命中内置词库与常见模式。注意：平台规则会更新，发布前仍建议人工复核。
```

## 本地脚本（可选）

批量或 CI 场景可执行：

```bash
python .cursor/skills/xianyu-sensitive-word-check/scripts/check_text.py "待检测文案"
python .cursor/skills/xianyu-sensitive-word-check/scripts/check_text.py --file path/to/copy.txt
```

运行业务场景示例（每个检测模式配套真实案例）：

```bash
python .cursor/skills/xianyu-sensitive-word-check/examples/business_cases.py
```

脚本输出 JSON；人工审查仍以本 Skill 的分级报告为准。案例说明见 [examples.md](examples.md)。

## 注意事项

- 词库基于公开规则与常见违禁类型整理，**不能替代**闲鱼官方实时审核
- 品牌名、品类词可能因上下文不同而有不同结论，标注时需说明上下文
- 用户若提供「仅检查引流词」等范围，只检测指定类别
- 修改建议应给出可发布的替代表达，而非仅删除

## 附加资源

- 完整分类词库：[word_categories.md](word_categories.md)
- 业务场景示例（含可运行代码）：[examples.md](examples.md)
