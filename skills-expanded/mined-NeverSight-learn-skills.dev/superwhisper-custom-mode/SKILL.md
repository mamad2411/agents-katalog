---
name: superwhisper-custom-mode
description: Superwhisper custom mode advisor — recommends full mode configurations (instructions, examples, context options, auto-activation) for specific use cases, and supports A/B testing iterations when modes need refinement.
---

# Superwhisper Custom Mode Advisor

This skill helps users create and refine Superwhisper custom modes. It recommends not just the prompt, but the full configuration: instructions, examples, context toggles, auto-activation, and audio options.

## Reference Material

Read before generating recommendations:

- **[references/superwhisper-software-reference.md](references/superwhisper-software-reference.md)** — What the software offers on each platform, what sections the AI receives, all configurable options, default modes, and real-world custom mode examples with rationale.

## Workflows

### Desktop: Create a New Mode

1. **Understand the use case** — What app(s)? What should the output look like? Is this a formatter, a transformer, or an assistant-style mode?

2. **Ask the user to create a blank custom mode in Superwhisper** — Have them:
   - Create a new custom mode in the app
   - Enable the context options they think they'll need (or that you recommend)
   - Do a test dictation (e.g., "this is a test")
   - Share the JSON file (the mode's config) AND the history prompt (Settings > History > Prompt > copy)

3. **Analyze what Superwhisper assembled** — The history prompt shows exactly what the AI received: which context sections were included, what the app context looks like for their environment, etc.
   - **Important**: Context sections (Clipboard, User Selected Text, Application Context) only appear in the history prompt when data was available at the time of dictation. A missing section may mean "enabled but empty," not "disabled." Check the JSON file's toggle fields to confirm what's actually enabled.

4. **Edit the JSON directly** — Modify the `"prompt"`, `"promptExamples"`, context toggles, `"activationApps"`, and any other fields. Return the complete updated JSON file for the user to import.
   - **JSON file naming**: The filename (without extension) and the `"key"` field inside the JSON must match.

5. **Generate 3 test dictations** — Create 3 sample texts the user should dictate to stress-test the mode. Each should target a different aspect:
   - **Test 1: Clean input** — A straightforward dictation that matches the mode's primary use case. Validates the happy path.
   - **Test 2: Messy input** — Includes self-corrections, filler words, false starts, or rambling. Tests how well the mode cleans up natural speech.
   - **Test 3: Edge case** — Targets something specific to the mode's purpose that could trip it up (e.g., a question that shouldn't be answered, mixed languages, a command embedded in content, markdown that should be preserved, etc.).

   Present these as exact text the user can read aloud, along with what the expected output should look like for each.

6. **User runs the tests** — They dictate each sample, then report back with the history prompt + transcribed text + AI processed text for each. Analyze the results:
   - If all 3 pass → mode is ready for real-world use
   - If any fail → iterate: adjust the JSON (instructions, examples, or settings) and re-test the failing cases

### Desktop: Update an Existing Mode

The user provides:
- The mode's **JSON file**
- The **history prompt** (the full prompt Superwhisper sent to the AI)
- The **transcribed text** (what the STT model produced)
- The **AI processed text** (what the AI returned)

This gives full visibility into what happened. Analyze the gap between expected and actual output, then edit the JSON and return the updated file.

### Desktop: Evaluate and Iterate

Once the JSON file is already in the session, the user can run quick evals by providing:
- **History prompt** + **transcribed text** + **AI processed text** per test

Analyze each result. If changes are needed, propose two variants for A/B testing:
- **Variant A** — conservative change (minimal edit to address the problem)
- **Variant B** — more significant rework (structural change to instructions or examples)

**Variant naming**: 
- Variant A: `{original-key}-a.json` with `"key": "{original-key}-a"`
- Variant B: `{original-key}-b.json` with `"key": "{original-key}-b"`

This lets the user import both and test side-by-side. Explain what each variant changes and why.

### Mobile: Create or Update

Mobile only supports custom instructions — no JSON files, no context toggles, no examples.

**To create**: Discuss the use case, provide the instructions text.

**To update**: The user provides:
- The **instructions** text
- The **transcribed text**
- The **AI processed text**

Analyze and suggest instruction changes.

## Working with History Prompts

The history prompt is the complete prompt Superwhisper sent to the AI:

```
INSTRUCTIONS:
[Custom prompt]

EXAMPLES OF CORRECT BEHAVIOR:
User: [Example input]
Assistant: [Example output]

SYSTEM CONTEXT:
[Auto-generated]

USER INFORMATION:
[Auto-generated]

APPLICATION CONTEXT:
[Auto-generated]

USER MESSAGE:
[The actual dictation]
```

Key understanding:
- **INSTRUCTIONS** — the editable custom prompt
- **EXAMPLES OF CORRECT BEHAVIOR** — already configured in the UI as Input/Output pairs. Don't suggest "moving them to the UI" — they're already there. Evaluate their quality and suggest better ones if needed.
- **SYSTEM CONTEXT, USER INFORMATION** — always included on desktop, auto-generated
- **APPLICATION CONTEXT, USER CLIPBOARD CONTENT, USER SELECTED TEXT** — only appear when the toggle is enabled AND data was available. A missing section doesn't necessarily mean "disabled."
- **USER MESSAGE** — the transcribed dictation being processed

## Prompt Writing Guidelines

### Principles

Write instructions that are:

1. **Clear purpose** — Start with a role and purpose statement. This sets the foundation for how the AI will process content.
2. **Specific requirements** — Create a detailed list of what you expect. Being explicit helps the AI understand exactly what you need.
3. **Well-structured** — Organize instructions into separate sections for different components. This modular approach makes instructions easier to understand and modify.
4. **Simple first** — Write direct, straightforward instructions without unnecessary complexity. Clear communication leads to better results.

Start simple. Only add complexity when testing reveals the AI needs more guidance. A plain-text prompt that works is better than an elaborate XML prompt that's hard to maintain.

### When to Use XML Tags

XML tags are **optional**. They help when instructions have multiple distinct concerns that benefit from clear separation (e.g., the Slack mode has formatting rules, @mention logic, paragraph structure, and special cases — XML keeps these organized).

Don't use XML when:
- The instructions are short and straightforward
- There's only one main task with a few rules
- The mode uses a less capable or local AI model (some may misinterpret XML tags)

The Claude Desktop mode is a good example — plain text, minimal instructions, heavy reliance on examples. Very effective.

### Referencing Context in Instructions

Use these exact names when referencing context sections:
- **User Message** — the transcribed dictation
- **Application Context** — active app, focused element, visible names
- **Clipboard Context** / **User Clipboard Content** — recently copied text
- **User Selected Text** — selected text before dictation

### Examples

- Provide 2-3 Input/Output pairs per mode
- Examples should cover the range of expected inputs (short/long, simple/complex)
- For modes that adapt to context (like Slack @mentions), include examples showing different scenarios
- When editing JSON directly, add examples to the `"promptExamples"` array with `"input"` and `"output"` fields

### Context Toggle Recommendations

- **Application Context** — enable when the mode needs to adapt to the active app, use name spellings, or detect conversation type. Avoid for terminal apps (noisy context causes hallucinations).
- **Clipboard Context** — enable when the user might copy reference text before dictating.
- **User Selected Text** — enable when the mode transforms selected text based on voice commands. Requires JSON config edit.
- **When in doubt, less is more** — unnecessary context can confuse the AI. The Claude Desktop example works well with all contexts off.
