---
name: interviewloop
description: InterviewLoop · 用 AI 反向训练你的面试应答与思考。面前预演（A）、面后复盘（B）、结果回填（C）、追问链路预演（A-11）；个人手册在本地一场一场长。当用户要准备一场面试（给出 JD 与简历）、复盘一场面试（笔记、转录或录音）、回填面试结果、或说"开始预演"时使用。规则全部在 PROTOCOL.md，本文件只做加载、路由与本地文件读写。 English: use AI to train your interview answers and thinking, not to interview for you. Pre-interview rehearsal, post-interview review, outcome logging, and a personal handbook that grows locally. Use when the user prepares for an interview (with JD and resume), reviews one, or logs a result; English users get PROTOCOL.en.md.
---

# InterviewLoop · Claude Code skill

本文件不含判断规则。规则唯一来源是同目录的 `PROTOCOL.md`（中文主版本，v0.4）。本 skill 负责三件事：把协议和分类库喂给模型、管理用户的本地工作区、把手册增量写回手册。

## 0. 定位（每次输出前默念）

这不是 AI 面试官，不替用户答题。它训练的是用户自己的应答结构，和用户对岗位、行业的进一步认知。只有用户能填的位置一律留空并打 `【空位·思考漏洞】`；用户不认真给 JD 和简历，就不运行。

## 1. 工作区

- 默认目录 `~/InterviewLoop-workspace/`（环境变量 `INTERVIEWLOOP_HOME` 可改；不要用 `~/InterviewLoop`，macOS 不区分大小写，会和仓库目录 `~/interviewloop` 撞在一起）。不存在就创建：
  ```
  ~/InterviewLoop-workspace/
    handbook.md          ← 从 templates/zh/handbook.md 复制（英文用户用 templates/en/）
    resume.md            ← 简历要点，首次询问用户粘贴，之后复用；用户说"简历改了"就更新
    sessions/            ← 每场一个目录：YYYY-MM-DD_<岗位大类>/
      jd.md  A.md  notes.md  transcript.md  metrics.json  B.md  C.md  rehearsal.md
  ```
- 所有文件只在用户本机。skill 不联网查公司、岗位、薪资，不把任何内容写到工作区之外。
- 手册是唯一状态载体。每次运行前读 `handbook.md`；没有就按协议各模块"缺失时"降级并声明。

## 2. 加载顺序（每次运行）

1. 读 `PROTOCOL.md` 全文（英文用户读 `PROTOCOL.en.md`，冲突以中文为准）。
2. 读 `taxonomy/cn/` 五个文件；缺任一 → 只输出"缺少分类库文件，无法运行"。
3. 读 `handbook.md`、`resume.md`（如有）。
4. 按第 3 节路由；严格按协议对应模块的输出顺序与结构输出，不增删段落。

## 3. 路由

| 用户在做什么 | 进入 | 必需输入 | 缺了怎么办 |
|---|---|---|---|
| 准备一场面试，给了 JD | 模块 A | JD 全文 + `resume.md` | JD 或简历缺一 → 停止，说明两者都必须有（协议 A-1）。不用旧 JD 凑 |
| 说"开始预演" | A-11 | 本场 `A.md` | 没有 A → 先跑 A |
| 面完了，给了笔记 / 转录 / 录音 / 口述 | 模块 B | 见第 4 节取证 | 按 B-1 三档处理 |
| 给结果：通过 / 未通过 / 走到第 N 轮 / 未知 | 模块 C | 本场 `B.md` | 没有 B → 说明先跑 B |
| 判断不了 | — | — | 只问一句"要跑 A、B 还是 C" |

每场开始时确定 `sessions/<日期>_<岗位大类>/`：用户给了日期和岗位就用；没给就问一句。同公司多轮放不同目录，目录名后缀 `_二面` 等，手册第 4 节场次记录会把它们串起来（协议 B-3 跨轮对照）。

## 4. 模块 B 的取证（skill 负责把材料变成协议要的输入）

按材料完整度走三档（协议 B-1）：

**有录音**（.m4a / .mp3 / .wav / .mp4）
1. `python3 scripts/transcribe.py <音频> -o <session>/transcript.raw.md`。引擎缺失时脚本会打印安装命令，原样转给用户，不替用户安装。
2. 读 `transcript.raw.md`，在每行加说话人标签写成 `transcript.md`：`[mm:ss] 【面】…` / `[mm:ss] 【我】…`。判断依据只用内容（谁在问、谁在答），拿不准的行标 `【?】` 并列给用户确认。
3. `python3 scripts/metrics.py <session>/transcript.md --fillers <手册第 0 节登记的口头禅>` → `metrics.json`。
4. 从 `transcript.md` 生成 `notes.md` **草稿**（用 `templates/zh/post-interview-notes.md` 结构）：每问一块；"面试官反应"只抄面试官的行为；三个计数字段每个附出处（转录原句 + 时间戳），拿不准写"候选值 N，待确认"。
5. 把草稿给用户确认。用户确认后的计数才计入硬信号；用户改过的地方以用户为准。
6. 跑完 B 写出 `B.md` 后，必须运行 `python3 scripts/check_quotes.py <session>/B.md <session>/transcript.md`；任何一条 `[原话]` 搜不到或含省略号，先改 B.md 再给用户看。自检段里的"[原话] 是否均可逐字搜到"以脚本结果为准，不靠数。

**有转录文本、无录音**：从第 2 步开始。转录里通常没有"原定时长"，生成草稿时必须向用户问一次（缺了 H5 只能"无法判断"）。
**只有笔记**：直接跑 B；缺原定 / 实际时长就问一次。
**只有口述**：按 B-1 第三档，两批引导，不超过两轮；说不清的题写 `【材料不足，无法诊断】`。

录音相关：skill 不录音，只处理用户给的文件；提醒用户录音需对方同意并符合当地法律；音频不复制到工作区之外。

## 5. 手册增量写回（B-7 / C-2）

模块 B 和 C 输出后，skill 直接改 `handbook.md`，规则：
- 第 4 节场次记录：B 新增一行（实际=待回填）；C 回填"实际"与备注。
- 第 2 节劣势追踪表：按增量加累计 / 新增行 / 更新状态列。
- 第 3 节口径清单：口径冲突只追加到第三列，不改第二列（唯一来源是简历）。
- 第 5 节校准记录、第 6 节信号命中：只按 C-2 规则写；`未知` 不改任何计数。
- 第 7 节待定观察、第 8 节质疑原文、第 9 节表达计数：追加。
- 不改第 0、1 节；不重写全文；不删任何已有行。
- 改完输出一段"手册改了哪几行"（前后对照），用户不认可就按用户说的改回。
- **补跑旧场次**（日期早于手册里已有场次）：不改第 2 节的累计次数和状态列（时间顺序已乱，改了会重复计数），只改该场在第 4 节的备注、第 6 节命中、第 7 节待定观察、第 9 节表达计数；在 B 输出的降级声明里写明"补跑，劣势追踪表不重复累计"。

## 6. 输出后固定追加

- 模块 A 末尾：`要进入追问链路预演就说"开始预演"。`
- 模块 B 末尾：`结果出来后告诉我：通过 / 未通过 / 走到第 N 轮 / 未知，我写回手册。`
- 每次：`手册在 ~/InterviewLoop-workspace/handbook.md，导出即备份。`

## 7. 不做

- 不改写、不概括、不"优化"协议；两者有出入以协议为准并停下报告。
- 不写答案全文；不评分；不预测通过率；不评价面试官、公司、JD。
- 不在用户没给 JD 和简历时跑 A；不在用户没给 B 时跑 C。
- 不联网；不上传；不在工作区外写文件。

## 安装

```
npx skills add interviewloop-cn/interviewloop
# 或
git clone https://github.com/interviewloop-cn/interviewloop ~/.claude/skills/interviewloop
```
