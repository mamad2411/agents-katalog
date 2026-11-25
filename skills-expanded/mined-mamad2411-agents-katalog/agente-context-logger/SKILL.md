---
name: agente-context-logger
description: Mantiene un historial de sesiones del agente en markdown dentro de una carpeta `logs_md_agente` en el root del proyecto. Utilízalo para registrar avances, decisiones críticas y próximos pasos, permitiendo que futuros agentes o tú mismo en una sesión posterior recuperéis el contexto rápidamente. Úsalo al finalizar tareas importantes o al terminar la sesión.
---

# Agent Context Logger

## Purpose
This skill is designed to bridge the context gap between different sessions or different agents working on the same project. It creates and maintains a human-readable (and agent-readable) log of activities in a dedicated `logs_md_agente` folder.

## 🚨 WHEN TO TRIGGER (CRITICAL RULE) 🚨

**YOU MUST NOT EXPECT THE USER TO ASK FOR A LOG.** You are strictly required to execute this skill **autonomously** in these situations:

- **IMMEDIATELY AFTER COMPLETING A FEATURE/FIX/DEPLOYMENT**: Before you reply to the user saying "It's done!", you MUST create/update the log file in `logs_md_agente` summarizing what you just did.
- **At the start of a session**: To read past logs using `view_file` and catch up on the project state.
- **When switching contexts or ending a session**: To summarize progress and list pending tasks for yourself or the next agent.
- **When requested by the user**: Specifically when they want a "checkpoint" or "summary" of current progress.


## Implementation Guide

### 1. Ensure Log Directory
- Locate the project's root directory.
- Check for the existence of a folder named `logs_md_agente`.
- If it's missing, create it.

### 2. File Naming Convention
- Use the format: `YYYY-MM-DD_session_summary.md`
- For multiple sessions in a day, use: `YYYY-MM-DD_HH-mm_session_summary.md`

### 3. Log Content Structure
Each log entry should follow this template for consistency:

```markdown
# Session Log: [Date and Time]

## 🎯 Objective
- [Primary goal of the session]

## ✅ Completed Tasks
- [List of accomplishments]
- 📝 **Modified Files**:
  - `path/to/file1.ts`: [Brief description of the changes explicitly tying the feature/bug to this file]
  - `path/to/file2.tsx`: [Brief description of the changes explicitly tying the feature/bug to this file]

## 🛠️ Technical Decisions & Rationale
- [Decision 1]: [Why?]
- [Decision 2]: [Why?]

## 🚧 Current State & Pending Work
- [List of tasks that are still in progress or planned]
- [Known issues or blockers]

## 💡 Recommendations for the Next Agent
- [Specific advice or warnings]
- [Where to pick up from]
```

### 4. Reading Logs
When starting work on an existing project, the agent SHOULD check this folder to understand the history of the project.

- List files in `logs_md_agente`.
- Read the most recent logs to gain context.
