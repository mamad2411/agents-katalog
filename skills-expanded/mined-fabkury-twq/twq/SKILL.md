---
name: twq
description: Study a task, ask me clarifying questions, then proceed.
argument-hint: [task description]
disable-model-invocation: true
allowed-tools: AskUserQuestion
---

## Task

$ARGUMENTS

## Process

1. Study this task as applicable.
2. Ask me questions to collect my clarifications, preferences, and
   final decisions about this task. Use the AskUserQuestion tool and
   wait for my answers before proceeding.
   Feel free to ask more than one round of questions, reading my
   answers between rounds, especially if knowing my answers to initial
   questions allows you to ask better or more useful further questions.
3. Then proceed with the task.

Do not skip step 2.
