---
name: demo-fun-facts-workflow
description: Given any topic, returns three surprising true facts plus one catchy title for them. Runs a tiny two-step aevatar workflow (facts then title) and is watchable in the observatory. A minimal demo of a workflow-carrying ornn skill.
version: "0.1"
metadata:
  category: mixed
  output-type: text
  runtime:
    - aevatar-workflow
  tool-list:
    - aevatar_start_workflow
  tags: [demo, workflow, facts, title, aevatar]
---

# Demo: fun facts workflow

This skill ships one prebuilt aevatar workflow, **`demo_fun_facts`**, and exists mainly as a
minimal, self-contained example of a *workflow-carrying* ornn skill (no external connectors, no
clock dependency, single terminal step). The workflow YAML lives in `assets/demo_fun_facts.yaml`.

Given a topic, a run does two things in order:

1. **facts** — an `llm_call` lists exactly three surprising-but-true facts about the topic as
   bullet points.
2. **title** — a second `llm_call` writes one catchy single-line title (≤10 words) that captures
   those three facts. This is the terminal step, so its output is the run result.

There is no web search and no arithmetic — it is pure LLM, which keeps the example dependency-free
and reliably runnable in any scope.

## How to run

1. Mount it: `use_skill("demo-fun-facts-workflow")` — this puts `demo_fun_facts` into the scope
   workflow catalog.
2. Start it:

   ```
   aevatar_start_workflow:
     workflow_id: demo_fun_facts
     inputs:
       prompt: "honeybees"
   ```

   The `prompt` is the topic. The run is fire-and-observe: it returns a `run_id` immediately and
   finishes asynchronously — watch it in `/workflow/observatory`.

## Notes

- The engine has **no clock**; if you ever want a time-bounded topic, put the window in the prompt.
- Output is plain text: three fact bullets followed by the generated title.
- To evolve this into a real pipeline (multi-source, citations, scoring), re-author with
  `aevatar-workflow-authoring` rather than extending this demo.
