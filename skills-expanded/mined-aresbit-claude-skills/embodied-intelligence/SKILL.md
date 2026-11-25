---
name: embodied-intelligence-skill
description: >-
  Expert tutor and reference for 具身智能 / embodied intelligence and robot
  learning, grounded in 《具身智能导论》— the 17-chapter Chinese textbook translated
  from UC Berkeley CS294-291 "Robots That Learn". Use this skill whenever the user
  asks about embodied AI / robot learning topics the book covers: 中枢模式发生器(CPG)、
  生物运动力学与步态、李群 SO(3)/SE(3) 机器人运动学与动力学、扩散模型/扩散策略
  (DDPM, score matching, flow matching, diffusion policy)、灵巧手与欠驱动协同、
  触觉感知(GelSight)、运动控制(LQR/MPC/阻抗控制)、卡尔曼滤波与预测控制、视频世界模型、
  强化学习(MDP/SAC/PPO/actor-critic)、行为克隆与动作分块、视觉模仿学习(UMI/跨具身)、
  足式运动(RMA)、导航(GOAT/可穿越性)、Sim-to-Real 灵巧操作、VLA 与 π0.5 长程规划。
  Trigger it for conceptual questions, math derivations, paper explanations,
  PyTorch implementation help, study/teaching, or "解释一下/推导/这门课/具身智能"
  requests in this domain — even when the user doesn't name the book. Prefer this
  skill over answering from memory, because it gives grounded, citable, notation-
  consistent answers and links to the exact chapter.
---

# 具身智能导论 — Knowledge Reference & Tutor

This skill answers questions about embodied intelligence by grounding them in
《具身智能导论》, a 17-chapter Chinese textbook (translated & expanded from UC
Berkeley CS294-291 "Robots That Learn", Spring 2026). The full chapters live in
`references/book/chXX_*.md`, with a 中英术语表 in `references/book/glossary.md`.

## How to use this skill

The book is ~1 MB across 17 chapters — do NOT read it all. Each chapter is a
self-contained ~50 KB unit. Work like this:

1. **Route the question to chapter(s)** using the index below (match by topic,
   keyword, paper, or method name).
2. **Read only the relevant chapter file(s)** with the Read tool. For a focused
   question, Grep the chapter for the specific term first, then read around it.
   For multi-topic questions, read the 2-3 chapters that apply.
3. **Answer grounded in the chapter**: use its derivations, its notation, its
   中英对照 terminology (cross-check `glossary.md`), and cite where it comes from
   — e.g. "见第9章 §二 卡尔曼滤波" — so the user can go deeper.
4. **Preserve math fidelity**: reproduce the book's LaTeX notation exactly; don't
   silently re-derive with different symbols. If you extend beyond the book, say
   so explicitly.
5. **Code questions**: each chapter has a §四 算法与代码实现 with PyTorch-flavored
   implementations — start from those rather than inventing a new API.

If a question falls **outside** the book's scope, say so plainly, then answer
from general knowledge while flagging that it's not from the book. Don't pretend
the book covers something it doesn't.

## Chapter routing index

Match the user's question to the chapter(s) by topic / keyword / paper, then read
that file from `references/book/`.

| Chapter file | 主题 | Route here when the question is about… |
|---|---|---|
| `ch01_导论.md` | 导论 | why robots should learn, 具身假设/embodiment, course overview, history of embodied AI, sense-plan-act vs learning |
| `ch02_生物运动力学.md` | 生物运动力学 | CPG 中枢模式发生器, Matsuoka 振荡器, Kuramoto 同步, 步态/gait, 占空比, DMP 动态运动基元, locomotion biomechanics (Ramdya & Ijspeert) |
| `ch03_机器人机构学.md` | 机构学 | 李群 SO(3)/SE(3), 旋转矩阵, 旋量/twist, 指数映射, 正/逆运动学, 雅可比, 拉格朗日 & 牛顿-欧拉动力学, DH 参数 |
| `ch04_扩散模型入门.md` | 扩散模型 | DDPM, 前向/反向扩散, score matching, denoising, 流匹配 flow matching, normalizing flows, ELBO (Papamakarios, Lipman) |
| `ch05_人手与机器人手.md` | 灵巧手 | 人手解剖学, 灵巧手设计, 欠驱动 underactuation, 协同 synergy, LEAP/软体手, 机械智能 (Piazza et al. 2019) |
| `ch06_本体感觉与触觉感知.md` | 触觉感知 | 触觉传感器, GelSight, 视触觉, 皮肤力学, 本体感受 proprioception, 机械感受器 (Jones, Gardner) |
| `ch07_运动控制的发展视角.md` | 发育运动控制 | 发育认知, 运动基元, CPG 视角, 跨模态视觉行走, 自监督运动 (Loquercio; Smith & Gasser) |
| `ch08_机器人动力学与控制.md` | 动力学与控制 | LQR, MPC 模型预测控制, 轨迹优化, 阻抗/导纳控制, 运动规划, 最优控制 (Kawato, Flanagan) |
| `ch09_计算神经科学与预测控制.md` | 预测控制 | 前向/逆向模型, 小脑模型, 卡尔曼滤波 Kalman filter, 贝叶斯估计, 精度加权, 预测控制, Land 茶实验 |
| `ch10_视频世界模型.md` | 世界模型 | 视频预测, 潜在动态模型, world action models (WAM), Track2Act, 点轨迹, 零样本策略 (Ye; Bharadhwaj) |
| `ch11_强化学习.md` | 强化学习 | MDP, 贝尔曼方程, policy gradient, actor-critic, SAC, PPO, 最大熵 RL, 探索/利用 (Haarnoja; OpenAI) |
| `ch12_行为克隆.md` | 行为克隆 | BC, 复合误差/compounding error, 扩散策略 diffusion policy, 动作分块 action chunking (Chi et al.) |
| `ch13_视觉模仿学习.md` | 视觉模仿 | UMI 手持夹爪, 跨具身 cross-embodiment, 相对轨迹表示, 鱼眼/隐性立体, 模仿学习数据 |
| `ch14_运动控制案例研究.md` | 足式运动 | RMA 快速运动适应, 四足/双足行走, teacher-student 蒸馏, 域随机化行走, 盲走→视觉 (Kumar, Agarwal) |
| `ch15_导航案例研究.md` | 导航 | GOAT, 语义地图, 可穿越性 traversability 估计, 自监督导航, 多目标导航 (Chang; Frey) |
| `ch16_灵巧操作案例研究.md` | 灵巧操作 | Sim-to-Real 迁移, 域随机化, 阻抗/导纳控制, 触觉操作, 柔顺 manipulation, 域偏移分析 (Lin; Choi) |
| `ch17_长程规划与语言.md` | VLA / 长程规划 | VLA 视觉-语言-动作模型, π0.5, Molmo, 语言在规划中的作用, 长程任务, 通用具身智能 (Physical Intelligence; Kim) |

### Cross-cutting topics (read multiple)
- **Diffusion for policies**: foundations in `ch04`, applied to control in `ch12`
  (diffusion policy) and `ch16` (manipulation).
- **CPG / 运动基元**: theory in `ch02`, developmental view in `ch07`.
- **Prediction & estimation**: `ch09` (Kalman/forward models) connects to `ch08`
  (MPC) and `ch10` (world models).
- **Sim-to-Real / domain randomization**: `ch14` (locomotion) and `ch16`
  (manipulation).
- **Learning paradigms map**: `ch11` (RL) vs `ch12`/`ch13` (imitation) — read
  `ch01` for how the whole course fits together.

## Answer style

- Match the user's language (the book is Chinese; answer in Chinese unless asked
  otherwise), keeping key terms as `中文 (English)` on first use, per the book.
- Lead with the intuition, then the formal result, mirroring the book's
  "物理直觉 + 完整推导" structure.
- Cite the chapter and section so the answer is verifiable and the user can read
  more. When you pull an equation or algorithm, point to where it lives.
