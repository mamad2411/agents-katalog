# decision-algorithm

> *"做重大人生决策不靠一时的热情，而靠可重复的决策算法。"*

基于老喻20年决策研究成果，融合 **期望值 + 凯利公式 + 贝叶斯定理（EKB框架）**，帮助你建立可纠错的决策闭环。

---

## 🚀 安装

将整个目录复制/链接到你的 AI 平台的 skills 目录即可：

```bash
# Claude Code
ln -s /path/to/decision-algorithm ~/.claude/skills/decision-algorithm

# OpenClaw
ln -s /path/to/decision-algorithm ~/.openclaw/workspace/skills/decision-algorithm

# Codex
ln -s /path/to/decision-algorithm ~/.codex/skills/decision-algorithm
```

---

## 📁 目录结构

```
decision-algorithm/
├── SKILL.md              # ⭐ 核心 Skill 入口（自包含 EKB 决策框架）
├── scripts/              # 工具脚本
│   ├── validate_skill.py       # 验证 SKILL.md 质量
│   ├── extract_course_algorithms.py
│   └── generate_skill.py
├── tools/                # 计算工具
│   └── decision_calculator.py  # 期望值/凯利公式计算器
├── references/           # 调研素材（如有）
├── books/                # 原书内容（开发参考）
├── README.md
└── LICENSE
```

---

## 🎯 使用方式

安装完成后直接提问：

```
我该不该辞职创业？
这笔投资该不该做？
纠结要不要分手
该怎么分配资金？
人生方向很迷茫
```

### 计算器工具

```bash
# 期望值计算
python3 tools/decision_calculator.py --ev -p 0.3 -g 100000 -l 20000

# 凯利公式
python3 tools/decision_calculator.py --kelly -p 0.4 -o 3

# 完整分析
python3 tools/decision_calculator.py --full -p 0.3 -g 100000 -l 20000 --capital 500000
```

---

## 📚 核心框架

| 维度 | 工具 | 解决的问题 |
|------|------|-----------| 
| 一维 | 胜率 + 赔率 | 赢的概率和回报是多少？ |
| 二维 | 期望值 | 这个决策值不值得做？ |
| 三维 | 凯利公式 | 该投入多少资源？ |
| 四维 | 贝叶斯更新 | 如何根据新信息调整判断？ |

---

MIT License
