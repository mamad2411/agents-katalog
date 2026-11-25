---
name: ai-coding-bishi
description: |
  国内大厂 AI Coding 笔试（阿里 / 蚂蚁 / 京东 / 美团 / 字节 / 拼多多 / 华为 / 科大讯飞等）
  秋招 / 春招 / 暑期实习通关手册。为零技术背景（产品经理、运营、学生）设计——
  你不写代码、不看报错、不做技术判断，全部由 AI 完成，你只负责复制粘贴 Prompt 和点按钮。

  触发词（中文）：
  - AI 编程笔试 / AI Coding 笔试 / aicoding 笔试 / 大厂笔试
  - 蚂蚁笔试 / 京东笔试 / 阿里笔试 / 美团笔试 / 字节笔试 / 拼多多笔试
  - 秋招笔试 / 春招笔试 / 暑期实习笔试 / 校招笔试
  - 帮我通过 AI Coding 笔试 / 走一遍 AI 编程笔试流程 / 我要考 AI 编程

  触发词（English）：AI coding exam / AI coding interview prep / AI pair programming exam

  何时使用：
  1. 用户即将/正在参加国内大厂 AI Coding 笔试
  2. 用户需要一份手把手指挥 AI 完成整场笔试的 Prompt 清单
  3. 用户拿到 README 形式的题目，要在 2 小时内交付可运行的后端服务
  4. 用户是非技术背景（产品经理、运营、学生），看不懂代码和报错

  何时不用：
  - 用户是熟练开发者、只想要小技巧（本 skill 是完整流程，会太重）
  - 纯算法题（LeetCode 类，需要不同的方法论）
  - 与考试/评分无关的日常开发任务
author: Carly
version: 5.5
---

# AI Coding 笔试通关手册 · 15 步流程 (v5.5)

**核心信念**：你不是程序员，你是产品经理。你的工作是**判断、决策、指挥 AI**。
AI 负责写代码、读报错、调 bug；你只复制粘贴 Prompt 和点按钮。

**目标**：120 分钟大厂 AI Coding 笔试，**60 分保底，80+ 冲刺**。

---

## 🚦 15 步流程总览

```
考前 5 min       │ ① 认识牛客界面 → ② 选 Python → ③ 复制 baseline
─────────────────┼─────────────────────────────────────────
Round 0 (3 min)  │ ④ 开场白设定 AI 身份
Round 0.5 (2 min)│ ⑤ 环境验证（pytest / fastapi 是否预装）
─────────────────┼─────────────────────────────────────────
需求 (10 min)    │ ⑥ AI 反过来问你 5 个是非题 → ⑦ AI 写 spec.md
─────────────────┼─────────────────────────────────────────
方案 (3 min)     │ ⑧ AI 推荐一条方案，你只点头
─────────────────┼─────────────────────────────────────────
计划 (5 min)     │ ⑨ AI 生成 plan.md（施工蓝图 + 进度记录）
─────────────────┼─────────────────────────────────────────
实现 (70 min)    │ ⑩ 每轮发【主 Prompt】,AI 自动跑 5 步：
                 │    读 spec+plan → 写测试 → 写代码+重启 → 跑测 → 更新 plan
                 │                                              ↓
                 │                             报错就用「报错翻译大师」
─────────────────┼─────────────────────────────────────────
验收 (25 min)    │ ⑪ SIGKILL 持久化测试 → ⑫ QA 自检
                 │ → ⑬ 生成 DELIVERY.md → ⑭ 清理 → ⑮ 点提交
```

---

## 🆘 主 Prompt（本手册最重要的一段）

每一轮（Round 1 / Round 2 / ...）只发一次这段 Prompt，把 `N` 替换成轮次数字：

```
现在开始 Round N。

【第 0 步 · 强制重读上下文（每轮必做）】
请你先在心里跑这两条命令，读完再动手：
1. cat spec.md   ← 读需求规格
2. cat plan.md   ← 读施工蓝图 + 当前进度

读完后先回答我 3 个问题（不要抢跑写代码）：
Q1. 我们现在在 Round 几?
Q2. 本轮 plan.md 里写的目标是什么?
Q3. 本轮完成的验证标准是什么?

【第 1 步 · 先写测试】
- 只写 pytest 测试文件，保存到 tests/test_roundN.py
- 覆盖本轮所有场景
- 【硬约束】保存用 heredoc：cat > tests/test_roundN.py << 'TESTEOF' ... TESTEOF
- 给我保存文件的完整命令
- 【严禁写实现代码!】

我保存并跑测试后（应该全失败），会告诉你结果。

【第 2 步 · 写实现代码】
- 只写让测试通过的最小代码
- 【严禁修改测试文件】
- 【硬约束】保存用 heredoc：cat > main.py << 'MAINEOF' ... MAINEOF
- 保存代码后，必须给我以下【完整重启组合】命令（照抄，不要改）：
  ```
  pkill -f uvicorn
  sleep 1
  uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/server.log 2>&1 &
  sleep 2
  curl -s http://localhost:8000/ && printf "\n✅ 服务活着\n" || printf "\n❌ 服务挂了\n"
  pytest tests/ -v
  ```
- 【铁律】改了代码不重启服务 = 老代码还在跑 = 测试结果没意义

【第 3 步 · 等我告诉你测试结果】
- 全绿 → 进入【第 4 步】
- 有红 → 你分析根因，只改实现，不改测试
- 服务挂了 → 让我跑 `tail -30 /tmp/server.log` 把日志给你

【第 4 步 · 同步更新 plan.md（本轮完成前必做!）】
本轮全部测试通过后，你必须做以下 3 件事：
1. 更新 plan.md：Round N → ✅，Round N+1 → 🔄，"完成数" +1
2. 给我保存更新后 plan.md 的 heredoc 命令
3. 验证方式：cat plan.md | head -15 应看到 Round N 状态是 ✅

完成后告诉我："Round N 已完成并同步进度，可以进入 Round N+1"

现在开始【第 0 步】：读 spec.md 和 plan.md，回答 3 个问题。
```

---

## 🆘 报错翻译大师（v5 核心武器）

**遇到任何报错**（终端里的红字），就用这段：

```
【你之前写的代码报错了】

【完整报错内容】
---
[粘贴终端里所有红字，不删任何东西]
---

【请你】
1. 用 3 句大白话告诉我：哪里出错了、为什么、严重不严重
2. 分类是 A/B/C 哪一种：
   A. 代码 bug（你改代码）
   B. 环境问题（我要装东西 or 改配置）
   C. 测试写错了（理论上不该改，先确认）
3. 直接给我修复方案：
   - 如果是 A，给我改好的完整 main.py + 保存命令 + 重启服务命令
   - 如果是 B，给我要执行的命令
   - 如果是 C，先解释为什么这个测试可能是错的
4. 修完后我该跑什么命令验证已修好?
```

---

## 📚 深入参考（按需加载）

- `references/01-prep.md` — 牛客界面地图、选语言、复制 baseline、环境验证
- `references/02-requirements.md` — 5 个是非题需求对齐、生成 spec.md
- `references/03-planning.md` — 方案推荐、plan.md 施工蓝图
- `references/04-round-loop.md` — 主 Prompt 完整版 + 每轮机制详解
- `references/05-troubleshoot.md` — 5 种失稳诊断、换会话套餐、卡 bug 处方
- `references/06-final-review.md` — SIGKILL 测试、QA 自检、DELIVERY.md、交卷清单
- `references/prompts.md` — 12 个关键 Prompt 抽取（考场速查）
- `references/glossary.md` — 术语大白话表（终端 / 端口 / SIGKILL / 幂等...）
- `references/commands.md` — 终端命令速查表（20 条）
- `references/errors.md` — 常见报错关键词查询表

---

## 🎯 最终交付物（交卷时 `work/` 里应该有）

| 文件 | 用途 | 来源 |
|---|---|---|
| `main.py` | **判分入口**（牛客判分机器就跑它） | AI 写，你保存 |
| `spec.md` | 需求护身符（AI 跑偏时甩它） | Step 7 |
| `plan.md` | 施工蓝图 + 进度记录 | Step 9 |
| `DELIVERY.md` | 人工评审友好的交付说明 | Step 14 |
| `tests/*.py` | 你的测试文件（加分项） | 每轮 |

**交卷前要删的**：`__pycache__/`、`*.pyc`、`*.db`（运行时数据库文件）。

---

## 🥔 一句话记忆

> **需求对齐 → spec.md 护身符 → plan.md 施工图 → 每轮主 Prompt（读→测→码→跑→更进度）→ SIGKILL → QA → 交付 → 交卷**

理论根基、方法论演进、参考文献详见 [README.md](./README.md)。
