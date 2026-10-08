# 🧩 Multi-Step Skill System

## 🎯 Purpose

Transform a single prompt into a structured, multi-step skill system that handles complex workflows from start to finish.

This ensures reliability by breaking tasks into clear phases with validation checkpoints.

---

## 🧠 When to Use

Use this prompt when:
- a single prompt becomes too complex or unreliable  
- tasks require multiple steps or transformations  
- outputs depend on intermediate processing  
- you need higher control and validation across a workflow  

---

## ⚙️ The Prompt

```text
<role>
Act as a Skill System Architect for Claude, and expand a single working prompt into a multi-step skill system that covers the entire workflow.
</role>

<task>
Take my best-performing prompt and rebuild it as a complete skill system with clear phases, handoffs, and validation checkpoints.
</task>

<steps>
1. Ask me to paste the current prompt and explain the full workflow it supports
2. Break the workflow into phases — input, processing, validation, output
3. Write a dedicated skill for each phase with clear handoff instructions
4. Chain the skills sequentially with checkpoints between phases
5. Test the full system on 3 real use cases end-to-end
</steps>

<rules>
- Each skill must function independently
- Handoffs must be explicit — output of phase 1 becomes input of phase 2 exactly
- Checkpoints must catch failures before they propagate
- Test the full system, not just individual skills
</rules>

<output>
Workflow Map → Phase Skills → Handoff Instructions → End-to-End Test Results
</output>
