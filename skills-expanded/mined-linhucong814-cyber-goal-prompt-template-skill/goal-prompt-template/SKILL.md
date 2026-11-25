---
name: goal-prompt-template
description: "Turn a rough one-sentence goal, idea, task, or Chinese request into a polished executable agent prompt or /goal prompt. Use when the user asks to optimize a prompt/question, 一句话达成目的, 自动翻译成提示词, 帮我写 /goal, agent 提示词模板, asks 你来执行最佳实践, or wants fewer and better clarifying questions before execution."
---

# Goal Prompt Template

## Purpose

Convert a short user goal into an executable task specification. If the user wants a prompt, return a usable final prompt. If the user explicitly asks you to execute the task, use that specification to complete the authorized work.

## Core Rules

1. Treat the user's input as the final desired outcome, even if it is only one sentence.
2. Infer sensible defaults from context and state important assumptions inside the final prompt.
3. Ask questions only when missing information blocks execution, changes risk, or makes success unverifiable. Ask at most three questions.
4. If questions are required, still provide a provisional final prompt with placeholders for the missing answers.
5. Preserve the user's language unless they request another language.
6. In prompt-only mode, make the output directly copyable and omit tutorial text. In execution mode, briefly state the intended outcome, do the work, and report verified results.
7. For inspection, debugging, refactoring, UI review, or fix tasks without authorization to modify, use an approval gate: `检查完成之后制定修复方案并向我汇报，在批准后执行`. Respect existing authorization: if the user already asked to apply the changes, do not add another approval step for that same scope. Existing tool and environment permission requirements still apply.

## Choose The Mode

- **Prompt-only:** The user asks to optimize a prompt, write a template, or produce a `/goal` prompt. Return the requested prompt and do not start the described task.
- **Execute:** The user asks you to do the work, including “你来执行最佳实践” or “按最佳实践直接完成”. Derive the target outcome, scope, deliverables, and verifiable completion criteria, then perform the authorized work. Do not stop after returning a prompt.
- A request for a `/goal` prompt does not itself authorize starting a persistent goal, creating an automation, or delegating to other agents. Use those capabilities only when explicitly requested or otherwise authorized by applicable instructions.

## Execution Mode

Read the available context and identify the actual deliverable. State a short plan and any material assumption, then execute within the user's authorized scope. Use relevant available skills when they improve the result; do not assume any particular optional skill is installed.

Ask at most three questions, only for missing information that blocks a correct or authorized next step. Continue independent work while awaiting an answer when possible. Permission for one action does not extend to unrelated accounts, costs, publications, or messages.

Verify the result against the completion criteria. Report what was delivered, where to find it, how it was checked, and any remaining blocker. If a step cannot be completed, say so explicitly instead of treating a plan or draft as a finished result.

## Choose The Template

- Use **General Agent Prompt** for normal one-off tasks: writing, analysis, review, coding, debugging, planning, research, or file work.
- Use **/goal Prompt** when the user says `/goal`, asks for a persistent/executable final goal, wants the agent to continue until completion, or the task has multiple phases and acceptance criteria.
- Use **Clarifying Questions + Provisional Prompt** only when execution would otherwise be unsafe, blocked, or impossible to verify.

## General Agent Prompt

Output this structure, filled in with concrete details from the user's sentence:

```text
请作为可执行任务的 agent，完成以下目标。

目标：
[用一句清晰的话重写用户的最终目标]

背景：
[补充必要背景；没有就写“用户只提供了简短目标，请基于现有上下文合理推断。”]

范围：
- [包含什么]
- [不包含什么，如能推断]

具体要求：
- [可执行要求 1]
- [可执行要求 2]
- [可执行要求 3]

工作方式：
- 先快速理解现有上下文，再行动。
- 信息不足但不阻塞时，采用合理假设并在结果中说明。
- 遇到会改变文件、数据、配置、账户、费用或外部状态的操作时，先说明计划和影响。
- [检查/修复类任务且用户尚未授权修改时，加入：检查完成之后制定修复方案并向我汇报，在批准后执行]

交付物：
- [用户最终应该收到什么]

完成标准：
- [如何判断任务完成]
- [如何验证结果]
```

## /goal Prompt

Use this when the user wants a durable task for `/goal`:

```text
/goal

任务目标：
[把用户的一句话整理成一个明确、可执行、可完成的最终目标]

背景说明：
[必要背景、现状、已知限制；没有明确背景时写出合理假设]

具体要求：
- [要求 1]
- [要求 2]
- [要求 3]

约束与边界：
- [技术、时间、权限、风格、安全、不要做什么]
- 信息不足但不阻塞时，请自行合理假设，并在汇报中说明。
- 如果需要修改文件、运行命令、调用外部服务或产生费用，请先说明影响。

执行流程：
1. 读取并理解相关上下文。
2. 制定简短执行计划。
3. 执行任务并进行必要验证。
4. 汇报结果、关键修改、验证方式和剩余风险。

完成标准：
- [可验证标准 1]
- [可验证标准 2]
- [可验证标准 3]

最终提示词：
[将以上内容合并成一段可直接交给 agent 执行的完整提示词。检查/修复类任务且用户尚未授权修改时，以“检查完成之后制定修复方案并向我汇报，在批准后执行”结尾。]
```

## Clarifying Questions + Provisional Prompt

When essential information is missing, output:

```text
需要补充的信息：
1. [只问会改变执行结果的关键问题]
2. [可选]
3. [可选]

暂定最终提示词：
[使用上面的 General Agent Prompt 或 /goal Prompt，把未知项写成明确占位符]
```

## Prompt Quality Checklist

Before responding, ensure the final prompt:

- Starts from the user's final goal, not from prompt-writing mechanics.
- Names the expected deliverable.
- Defines scope and constraints.
- Includes verification or completion standards.
- Minimizes questions and uses assumptions for non-blocking gaps.
- Is ready to paste into Codex, another agent, or `/goal`.
