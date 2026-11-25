---
name: paper-strategy
description: Use this skill to break down an empirical paper's identification strategy — its research question, setting, data, econometric method, and identification/endogeneity handling (a Problem-Setting-Data-Method-Identification decomposition). Explains what each method is for and why the author uses it, and maps key figures/tables to methods and Stata/R commands. Stays at the concept level (no formula derivations); never fabricates.
---

# paper-strategy（论文实证策略拆解）

从**实证方法与识别**角度拆解一篇论文：它用了哪些方法、凭什么可信、怎么处理内生性。按 **P-S-D-M-I 五层**梳理——问题（Problem）、情境（Setting）、数据（Data）、方法（Method）、识别（Identification）——并给出**图表 → 方法 → 命令**对照。对应第 1 讲配套阅读笔记的「实证方法与识别」，也用于第 3 讲。

## 何时用

- 想弄清一篇论文用了什么计量方法、识别策略是什么、怎么应对内生性；
- 想判断一篇论文的方法能不能迁移到自己的研究；
- 想顺着关键图表，快速建立「图表对应什么方法、方法对应什么命令」的对照。

## 使用方式（提示词）

把论文 PDF 连同下面的要求发给 agent：

> 请**只从「实证方法与识别」这一个角度**帮我写一份中文笔记，面向计量基础较弱的读者，包含：
>
> - 核心方法：主要用了哪些计量方法？每种一两句话说清它是干什么用的，**不要写公式推导**；
> - 识别策略：凭什么相信估计的是因果效应？处理组、对照组、政策时点分别怎么来的？
> - 内生性与稳健性：作者担心哪些干扰（趋势不平行、选择偏差、溢出污染等），又怎么缓解？
> - 图表与方法与命令对照：挑几张关键图表，说明它用的核心方法与对应的 Stata/R 命令。
>
> 只依据论文本身，不编造；名词保持克制；每条结论标注对应的图或表编号。

## 输出约定

- 五层结构（P-S-D-M-I）+ 一张「图表 / 方法 / 命令」对照表；
- **守初级班难度红线**：只讲方法「是什么、为什么用」，不做公式推导；超纲名词点到为止；
- 标注图表编号，便于回原文核对。

## 最小使用示例

> 用 paper-strategy 拆一下这篇论文的识别策略，重点告诉我它怎么处理内生性，以及主结果那张图用的什么方法、什么命令。

## 人工检查清单

- **AI 辅助、不替代判断**：方法能否迁移、识别是否站得住，由研究者自己把关。
- 图表编号、命令名回原文与复现代码核对。
- 超出你当前掌握的方法（如双重稳健、三重差分），先记下来即可，后续讲次与高级班再系统学。

## 来源与许可

- 原创：本课程为「连享会 2026 暑期班·初级班」编写，Agent 无关的开放 Skill，MIT（随仓库 `LICENSE-CODE`）。
- 最后验证日期：<!-- TODO: T7 彩排双端实测后填写 -->
