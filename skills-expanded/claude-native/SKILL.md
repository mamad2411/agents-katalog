---
# Preserve native field values, YAML formatting, and comments on Claude.
name: claude-native
description: Use when testing Claude native skill portability and projection.
allowed-tools: Read Bash
disable-model-invocation: true
user-invocable: false
disallowed-tools: [Write, Edit]
context: fork
agent: Explore
background: true
model: sonnet
effort: high
paths:
  - 'src/**'
shell: bash
argument-hint: '[topic]'
arguments:
  - name: topic
    description: Topic to inspect
---
# Native fixture

Read the requested topic. Shell interpolation is source data: !`printf fixture`.
