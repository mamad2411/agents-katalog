---
name: ledger
description: 极简对话式记账。说"午饭 35"自动记账，支持查询今日/本月/年度/分类统计。
homepage: https://github.com/OutmanSay/ledger-cli
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: ["python3"]
    install:
      - id: clone
        kind: git
        repo: https://github.com/OutmanSay/ledger-cli.git
        label: "Clone ledger-cli"
---

# ledger — 极简对话式记账

说"午饭 35"自动记账，SQLite 本地存储，数据完全可控。

## 安装

```bash
git clone https://github.com/OutmanSay/ledger-cli.git ~/.openclaw/workspace/skills/ledger
```

## 使用

### 记一笔

用户说类似以下内容时，自动记账：

- "午饭 35"
- "打车 18"
- "老婆买衣服 299"
- "停车费 15"
- "买水果 25"

执行：
```bash
python3 ~/.openclaw/workspace/skills/ledger/ledger_tool.py add --amount 金额 --category 分类 --note "备注"
```

### 分类映射

| 用户说的 | 自动归类 |
|---------|---------|
| 吃饭/午饭/早饭/晚饭/外卖/咖啡/奶茶/零食/水果 | 食品酒水 |
| 打车/地铁/公交/停车/加油 | 行车交通 |
| 买东西/超市/日用 | 居家物业 |
| 玩/电影/旅游 | 休闲娱乐 |
| 老婆/孩子/送礼/红包 | 人情往来 |
| 看病/药/体检 | 医疗保健 |
| 衣服/鞋 | 衣服饰品 |
| 话费/网费 | 交流通讯 |
| 数码/订阅 | 学习进修 |

### 查询

| 用户说的 | 执行 |
|---------|------|
| "今天花了多少" | `ledger_tool.py today` |
| "本月花了多少" | `ledger_tool.py month` |
| "上个月花了多少" | `ledger_tool.py month 2026-03` |
| "最近花了什么" | `ledger_tool.py recent` |
| "本月吃饭花了多少" | `ledger_tool.py category 餐饮` |
| "搜一下奶茶" | `ledger_tool.py search 奶茶` |
| "本月统计" | `ledger_tool.py stats` |
| "今年花了多少" | `ledger_tool.py year` |

### 规则

1. 用户说的数字就是金额，不需要确认，直接记
2. 记完告诉用户：记了什么分类、多少钱
3. 如果用户没说分类只说了金额，问一句"这笔是什么消费？"
4. 数据库位置：和 `ledger_tool.py` 同目录下的 `ledger.db`
