# Prompt Engineering Interactive Tutorial

Anthropic's comprehensive step-by-step course on engineering optimal prompts for Claude. 9 chapters + appendix, each with a lesson, exercises, and a live playground. Available in two variants: Anthropic 1P (direct API) and Amazon Bedrock.

**Source:** `anthropics/prompt-eng-interactive-tutorial` (public)
**Local clone:** `/home/user/anthropics/prompt-eng-interactive-tutorial`
**Notebooks path:** `/home/user/anthropics/prompt-eng-interactive-tutorial/Anthropic 1P/`
**Google Sheets version:** https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8/

---

## Course Structure

### Beginner

| Chapter | File | Key concept |
|---------|------|-------------|
| 1 | `01_Basic_Prompt_Structure.ipynb` | Messages API: `model`, `max_tokens`, `messages`; alternating user/assistant turns |
| 2 | `02_Being_Clear_and_Direct.ipynb` | Golden Rule: show your prompt to a colleague — if they're confused, Claude's confused |
| 3 | `03_Assigning_Roles_Role_Prompting.ipynb` | Role prompting in system prompt or user turn; include audience context |

### Intermediate

| Chapter | File | Key concept |
|---------|------|-------------|
| 4 | `04_Separating_Data_and_Instructions.ipynb` | Prompt templates with placeholders; separate fixed instructions from variable input |
| 5 | `05_Formatting_Output_and_Speaking_for_Claude.ipynb` | XML tags for structured output; prefilling the assistant turn ("speaking for Claude") |
| 6 | `06_Precognition_Thinking_Step_by_Step.ipynb` | Chain-of-thought: spell out reasoning steps; thinking only counts if it's out loud |
| 7 | `07_Using_Examples_Few-Shot_Prompting.ipynb` | Few-shot prompting; zero/one/n-shot; examples beat long descriptions for format/tone |

### Advanced

| Chapter | File | Key concept |
|---------|------|-------------|
| 8 | `08_Avoiding_Hallucinations.ipynb` | Give Claude an "out"; ask for evidence first; grounding techniques |
| 9 | `09_Complex_Prompts_from_Scratch.ipynb` | Full complex prompt structure for chatbots, legal, financial, coding use cases |

### Appendix

| Notebook | Topic |
|----------|-------|
| `10.1_Appendix_Chaining Prompts.ipynb` | Multi-step prompt chains |
| `10.2_Appendix_Tool Use.ipynb` | Function/tool calling |
| `10.3_Appendix_Search & Retrieval.ipynb` | RAG and retrieval patterns |

---

## Core Techniques by Chapter

### Ch 1 — Basic Prompt Structure
Minimum Messages API call requires `model`, `max_tokens`, and `messages` (alternating `user`/`assistant` turns). The `assistant` turn can be prefilled to steer Claude's continuation.

### Ch 2 — Being Clear and Direct
Claude has no implicit context. The more explicitly you state what you want, the better. Golden Rule: if a colleague handed this prompt would be confused, rewrite it.

### Ch 3 — Role Prompting
Priming Claude with a specific role improves performance, tone, and style:
```
System: You are a senior securities attorney advising a Fortune 500 board.
```
Include the intended audience for even better calibration. Works in either the system prompt or user turn.

### Ch 4 — Separating Data from Instructions
Use placeholder templates to keep instructions stable while swapping in variable data:
```python
PROMPT = f"Classify the sentiment of this review: <review>{review_text}</review>"
```
XML tags make the boundary between instruction and data unambiguous.

### Ch 5 — Formatting Output & Prefilling
Ask Claude to wrap output in XML tags for reliable extraction:
```python
"Put your answer inside <answer></answer> tags."
```
Prefill the assistant turn to force a specific starting point:
```python
messages=[
    {"role": "user", "content": "Write a haiku about fog."},
    {"role": "assistant", "content": "<haiku>"}  # Claude continues from here
]
```

### Ch 6 — Thinking Step by Step (Precognition)
For complex or nuanced tasks, spell out the reasoning steps explicitly. Invisible thinking doesn't help — the chain of thought must be in Claude's output:
```
First, identify the key claim. Then, find evidence for and against it.
Finally, based on your analysis, give your verdict.
```
Note: Claude can be sensitive to ordering; if results are inconsistent, try reordering steps.

### Ch 7 — Few-Shot Prompting
Examples beat instructions for getting the right format or tone. A few well-chosen examples (`n-shot`) let Claude extrapolate the pattern:
```
Input: [example 1 input]   Output: [example 1 output]
Input: [example 2 input]   Output: [example 2 output]
Input: [real input]        Output:
```

### Ch 8 — Avoiding Hallucinations
Techniques:
1. **Give Claude an out**: "Only answer if you are certain. If unsure, say 'I don't know'."
2. **Ask for evidence first**: "Find direct quotes from the document before answering."
3. **Combine with other techniques**: role prompting, few-shot, step-by-step reasoning all help reduce hallucination.

### Ch 9 — Complex Prompts (Recommended Structure)
For complex prompts, use this ordered structure (not all elements required every time):
1. **Role / persona** — who Claude is
2. **Task description** — what Claude must do
3. **Rules and constraints** — what Claude must and must not do
4. **Background context** — relevant information
5. **Conversation history** (if applicable)
6. **Immediate task** — the specific request
7. **Thinking steps** — how to reason through it
8. **Output format** — how to structure the response

Start with all elements to get it working, then slim down.

---

## Amazon Bedrock Variant

The `AmazonBedrock/` directory contains the same course adapted for the Bedrock API (boto3 + CloudFormation). Structure mirrors the Anthropic 1P version.

---

## Setup

```python
import anthropic
client = anthropic.Anthropic(api_key="sk-ant-...")

def get_completion(prompt, system="", prefill=""):
    messages = [{"role": "user", "content": prompt}]
    if prefill:
        messages.append({"role": "assistant", "content": prefill})
    return client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        system=system,
        messages=messages
    ).content[0].text
```

---

## Prompts

### Work through a chapter

```
Open /home/user/anthropics/prompt-eng-interactive-tutorial/Anthropic 1P/[chapter].ipynb.
Walk through the lesson and exercises step by step, explaining what each technique demonstrates.
```

### Debug a failing prompt

```
Using the techniques from the prompt engineering tutorial at
/home/user/anthropics/prompt-eng-interactive-tutorial:
Review this prompt: [prompt]
Identify which technique(s) from Chapters 2–8 would most improve it and rewrite it.
```

### Build a complex prompt from scratch

```
Using Chapter 9's complex prompt structure from
/home/user/anthropics/prompt-eng-interactive-tutorial/Anthropic 1P/09_Complex_Prompts_from_Scratch.ipynb:
Build a production-quality prompt for [use case].
Apply: role prompting, clear instructions, XML delimiters, step-by-step reasoning, output formatting.
```

### Teach the full course

```
Using /home/user/anthropics/prompt-eng-interactive-tutorial:
Give a condensed walkthrough of all 9 chapters.
For each chapter, state the core principle and show one before/after example prompt.
```
