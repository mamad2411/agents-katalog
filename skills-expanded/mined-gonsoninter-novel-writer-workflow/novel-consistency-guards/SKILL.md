---
name: novel-consistency-guards
description: "Use throughout Phase 2 novel writing as a background guardrail - hard constraint scanning, cross-chapter consistency tables, hook-vs-body parity check - activated alongside chapter-sop and finalization"
allowed-tools: Read, Grep, Write, Edit, Bash
---

# 小说一致性护栏（Phase 2 · 贯穿写作期）

## 激活条件

**贯穿整个写作期一直在后台激活**。由以下 skill 主动引用：
- `novel-chapter-sop` 每一章 / 每一场景 写完后引用本 skill 做机械扫描
- `novel-finalization` 收口阶段引用本 skill 做全书扫描
- 用户手动说"扫一下所有章" / "一致性查一遍" 时直接调用

## 这个 skill 做三件事

1. **硬约束锁 + 脚本化机械扫描**
2. **跨章一致性四表维护**
3. **钩子区 vs 正文核对**

## 一、硬约束锁清单

`novel-ideation` 的 constitution 里应该锁死这些项。本 skill 负责扫描。

**典型红线**（按你的 constitution 调整）：

| 类别 | 红线 | 脚本检测方法 |
|---|---|---|
| 姓氏锁 | 某角色姓氏不得变（如"苏淮"不得误写成"林淮"） | `'林淮' in text` |
| 引号类型 | 必须中文全角 " " / ' '，禁止 ASCII | `'"' in text or "'" in text` |
| 破折号密度 | 每章正文 ≤ 7 个 "——" | `body.count('——') <= 7` |
| Markdown bold | 正文禁止 `**字**` | `'**' in text` |
| Meta "Ch N" | 正文不得出现"Ch X" / "第 X 章" 指涉 | `re.search(r'Ch\s*\d+', text)` |
| 超自然解释 | 禁止无物理/化学解释的超能力 | 人工+agent 审 |
| 全角引号配对 | 左右引号数量相等 | `text.count('"') == text.count('"')` |

## 扫描脚本模板（Python）

```python
# check_consistency.py
import re
import sys

def check_chapter(path):
    t = open(path).read()
    parts = t.split('\n\n', 2)
    body = parts[-1] if len(parts) >= 3 else t

    issues = []

    # 机械项
    wc = len(re.sub(r'\s', '', body))
    dashes = body.count('——')
    if dashes > 7:
        issues.append(f'破折号 {dashes} 超限')
    if '**' in t:
        issues.append(f'markdown bold {t.count("**")} 个')
    if '"' in t:
        issues.append(f'ASCII 双引号 {t.count(chr(34))} 个')
    if "'" in t:
        issues.append(f'ASCII 单引号 {t.count(chr(39))} 个')
    if t.count('"') != t.count('"'):
        issues.append(f'引号不配对 {t.count("“")}/{t.count("”")}')
    if '林淮' in t:
        issues.append(f'禁用姓氏"林淮" {t.count("林淮")} 次')
    if re.search(r'Ch\s*\d+', t):
        issues.append('出现 meta "Ch N" 引用')

    return wc, issues

if __name__ == '__main__':
    for path in sys.argv[1:]:
        wc, issues = check_chapter(path)
        status = '✅' if not issues else '❌ ' + ' / '.join(issues)
        print(f'{path}: {wc} 字 {status}')
```

**使用**：

```bash
python3 check_consistency.py chapters/*.md
```

每次写完 / 改完章节立刻跑。**修订时特别容易引入新问题**（手抖加破折号、复制粘贴带入 ASCII 引号），必须每次跑。

## 二、跨章一致性四表

长篇最容易翻车的地方，不是单章写得好不好，是跨章前后不一致。维护四张表：

### 表 1：道具链表

每个关键物件列：

```markdown
## 道具链 · 青玉簪

| 章 | 位置/状态 | 变化 |
|---|---|---|
| Ch 19 | 女主发髻（家中带出） | 首次出现 |
| Ch 28 | 女主发髻 | 男主深夜所赠、贴身带着 |
| Ch 37 | 异国巷道 | 被人碰断、玉簪掉在水沟 |
| Ch 38 | 男主内袋 | 只剩半截残身 |
| Ch 39 | 女主发髻 | 归还时换上新的玉簪 |
```

**每个关键物件都维护这种表**。写新章前先看表，写完后更新表。

### 表 2：时间锚表

每章开头时间戳，章间算跨度：

```markdown
| 章 | 时间锚 | 距上一章 |
|---|---|---|
| Ch 28 | 正月十八下午四点 | — |
| Ch 29 | 正月十八夜九点零二分 | +5 小时 |
| Ch 30 | 正月十八夜九点三十五分 | +33 分钟 |
| Ch 31 | 正月十八夜十点前后 | +25 分钟 |
| Ch 32 | 正月十八夜十点零七分 | +几分钟 |
```

**跨天/跨月章之间算几周几个月，防止钩子说"两个月后"实际是五周这种**。

### 表 3：术语一致性表

同一个东西在不同章节必须用**同一个名字**。改任何一处，全文对齐：

```markdown
| 概念 | 统一叫法 | 禁用别名 |
|---|---|---|
| 主角父亲当年灭门旧档复印件 | "父亲当年灭门那份旧档复印件" | "前世被查封笔录复印件"（歧义） |
| 关键公章 | "歪半格的那枚朱印" | "那枚章" / "旧朱印" |
| 配角护身符 | "桃木符"（前后统一） | "小木牌" / "护身符" |
```

### 表 4：关键数字表

年龄、年份、件数、金额、比分——特别容易前后不符：

```markdown
| 项 | 数值 | 出现章 |
|---|---|---|
| 主角灭门时年龄 | 8 岁 | Ch 19/30/31 |
| 前世主角死时年龄 | 28 岁 | Ch 1/29/30/32 |
| 灭门年份 | 2000 冬 | Ch 19/30/31 |
| 对决总比分 | 主角 5 胜 2 平 / 对手 0 胜 2 平 5 负 | Ch 33/34/35 |
| 反派台前刑期 | 有期徒刑 20 年 | Ch 39 |
| 反派幕后刑期 | 无期徒刑 | Ch 39 |
```

## 三、钩子区 vs 正文核对

很多 skill 和工具默认"钩子 = 章摘要"，但读者读的是正文。两者口径如果不一致，发布时删了钩子会发现**正文没兑现钩子里的承诺**。

**实战中最常见的钩子/正文冲突**：
- 比分（钩子写"五胜两平"，正文算出来"四胜两平一胜第七局"）
- 时间线（钩子写"两个月后"，正文里算出来是五周）
- 道具细节（钩子写"对手推门进拍卖行"，正文里是"推门进旧画廊"）
- 罪名（钩子列了"非法出境"，正文里没这一条）

**定稿前必须做一次钩子 vs 正文口径核对**。

### 核对方法

对每一章：
1. 把钩子段的关键名词、数字、时间、事件列出来（可以让 agent 帮你提取）
2. grep 正文看每一项是否出现
3. 数字项必须完全一致（比分 / 时间跨度 / 金额 / 件数）
4. 名词项要统一（同一物件的叫法）

## 反常识：破折号是可测量的风格指标

很多"风格问题"是主观判断，难量化。但破折号密度可以。

经验值：**正文每章破折号 ≤ 7 个，读起来不碎**。超过 10 个就明显有"破折号滥用"感。低于 3 个过于平实可能缺气口。

**这个指标比"句子通顺与否"稳得多**。写脚本统计就行，不用人工数。

## 与姐妹 skill 的关系

- **被 `novel-chapter-sop` 调用**：每一章/场景写完后做机械扫描
- **被 `novel-finalization` 调用**：收口阶段做全书扫描
- **被 `novel-ideation` 参照**：constitution 里的硬约束锁清单应该直接列在本 skill 可扫描的形式
- **不做什么**：不写正文、不做语义 review（那是 chapter-sop 里 agent 的事）、不决定修订优先级（那是 finalization 的事）

## 用法速查

| 场景 | 命令 / 动作 |
|---|---|
| 每章写完后扫一遍 | `python3 check_consistency.py chapters/N.md` |
| 全书批量扫 | `python3 check_consistency.py chapters/*.md` |
| 某个物件前后不一致 | 查"道具链表"那一行 |
| 算两章时间差 | 查"时间锚表" |
| 钩子写错数字 | 用"关键数字表"对齐 |
