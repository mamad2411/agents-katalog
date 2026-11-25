---
name: create-system-prompt
description: This skill should be used when the user asks to "create an agent instruction", "add agent instructions", "scaffold an agent sample", "create a system prompt sample", "add a system prompt", "create a new agent", "build an agent", or needs to create a new agent instruction sample with proper folder structure, README, and sample.json metadata inside the agent-instructions folder. Do NOT use this skill for simple prompt samples that are not agent instructions.
---

# Create an Agent Instruction / System Prompt Sample

This skill guides creating new agent instruction samples for the pnp/copilot-prompts repository. These samples live inside `samples/agent-instructions/` and represent agents whose system prompt / instructions are the contribution. Contributors build an agent in Microsoft Copilot Studio and share the instructions (system prompt) that power it.

## Before Starting

**Critical**: Always ask the user for the following information before scaffolding:

1. **Agent name** — a short, descriptive name for the agent (e.g., "Communication Assistant", "Smart Crop Doctor", "Elevator Pitch Alchemist")
2. **Agent instructions / system prompt** — the full system prompt text that defines the agent's behavior, personality, skills, and operating principles
3. **Summary** — a short description of what the agent does and why it's useful
4. **Use case category** — one or more categories the agent falls into:
   - 🎮 **Gaming** — AI-powered game ideas, NPC interactions, procedural storytelling
   - 📚 **Storytelling & Creative Writing** — Fiction, poetry, and immersive storytelling prompts
   - 🤖 **AI Assistants** — Virtual assistants, chatbots, and productivity helpers
   - 🛠️ **Productivity & Tools** — Code generation, automation, and workflow improvements
   - 🎓 **Education** — Learning aids, tutoring, and interactive teaching tools
   - 🏥 **Healthcare & Wellbeing** — AI for mental health, fitness, and well-being support
   - 🌎 **Other** — If the idea doesn't fit the above
5. **Author name** — the contributor's full name
6. **Author GitHub username** — the contributor's GitHub handle

If the user doesn't provide all details upfront, ask for the missing ones before proceeding.

## Sample Directory Structure

Create the sample in `samples/agent-instructions/{agent-name}/`:

```
samples/agent-instructions/{agent-name}/
├── assets/
│   ├── demo.png             # Required static preview
│   └── sample.json          # Metadata for the M365 Solution Gallery
├── README.md                # Documentation with agent instructions
```

**Folder naming rules:**
- Use lowercase and hyphens only (e.g., `daily-chore-children`, `communication-assistant`, `peace-keeper-agent`)
- Do NOT use periods/dots in the folder name
- Keep it concise but descriptive — it should hint at what the agent does
- Do NOT include prefixes like `m365-` or `github-` — agent instruction folders use plain descriptive names

## Step 1: Create README.md

Create `samples/agent-instructions/{agent-name}/README.md` using this structure:

```markdown
# 🎯 {Agent Name}

## Summary

{Short summary of what this agent does, its purpose, and why it's useful.}

## Instruction

```
{The full agent instructions / system prompt goes here.

This is the core contribution — the complete system prompt that defines:
- The agent's identity and purpose
- Execution steps or workflow
- Operating principles and guidelines
- Tone and personality
- Example interactions (optional)
- Limitations and constraints (optional)}
```

## 🏆 Use Case Category

{Mark the applicable categories with [x]:}

- [ ] 🎮 **Gaming** – AI-powered game ideas, NPC interactions, procedural storytelling
- [ ] 📚 **Storytelling & Creative Writing** – Fiction, poetry, and immersive storytelling prompts
- [ ] 🤖 **AI Assistants** – Virtual assistants, chatbots, and productivity helpers
- [ ] 🛠️ **Productivity & Tools** – Code generation, automation, and workflow improvements
- [ ] 🎓 **Education** – Learning aids, tutoring, and interactive teaching tools
- [ ] 🏥 **Healthcare & Wellbeing** – AI for mental health, fitness, and well-being support
- [ ] 🌎 **Other** – If your idea doesn't fit the above, tell us what it's about!

## Contributors 👨‍💻

[{Author Name}](https://github.com/{github-username})

## Version history

Version|Date|Comments
-------|----|--------
1.0|{Month DD, YYYY}|Initial release

## Instructions 📝

- Make sure you have Microsoft 365 Copilot in your tenant.
- Access Copilot studio agent builder
- On the left-hand rail, select Create an agent - New agent
- Add description to refine agents behavior. Make sure to use short, precise and simple description.
- Paste the prompt in the Instructions field, and alter it according to your needs.
- Try out your agent in the same window.

## Prerequisites

Copilot License

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20{agent-name}%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/copilot-prompts/copilotprompts-agent-{agent-name})
```

**README rules:**
- **NEVER rephrase, rewrite, or modify the user's system prompt / agent instructions.** Copy the prompt exactly as provided by the user — word for word, character for character. The user's original wording is the contribution; do not "improve", shorten, expand, or restructure it.
- The file must be named `README.md`
- Include `![Screenshot of the agent in use](./assets/demo.png)` after the title
- The **Instruction** section is the most important part — it contains the full system prompt in a fenced code block
- The system prompt should be well-structured with clear sections (Purpose, Execution Steps, Operating Principles, Tone, etc.)
- The **Instructions 📝** section (how to use) always describes the Copilot Studio agent builder workflow
- The tracking image at the bottom MUST follow the pattern: `https://m365-visitor-stats.azurewebsites.net/copilot-prompts/copilotprompts-agent-{agent-name}`
- Include the Help and Disclaimer sections exactly as shown
- Use the current date for the version history in `{Month DD, YYYY}` format
- Mark the correct Use Case Category checkboxes based on what the user selected

## Step 2: Create Metadata (assets/sample.json)

Create `samples/agent-instructions/{agent-name}/assets/sample.json`:

```json
[
  {
    "name": "copilotprompts-agent-{agent-name}",
    "source": "pnp",
    "title": "{Agent Title}",
    "shortDescription": "{Short description of what the agent does}",
    "url": "https://github.com/pnp/copilot-prompts/tree/main/samples/agent-instructions/{agent-name}",
    "downloadUrl": "https://pnp.github.io/download-partial/?url=https://github.com/pnp/copilot-prompts/tree/main/samples/agent-instructions/{agent-name}",
    "longDescription": [
      "{A longer description of what the agent does and why it's useful.}"
    ],
    "creationDateTime": "{YYYY-MM-DD}",
    "updateDateTime": "{YYYY-MM-DD}",
    "products": [
      "Copilot"
    ],
    "metadata": [],
    "thumbnails": [
      {
        "type": "image",
        "order": 100,
        "url": "https://github.com/pnp/copilot-prompts/raw/main/samples/agent-instructions/{agent-name}/assets/demo.png",
        "alt": "{Description of the agent screenshot}"
      }
    ],
    "authors": [
      {
        "gitHubAccount": "{github-username}",
        "pictureUrl": "https://avatars.githubusercontent.com/{github-username}",
        "name": "{Author Name}"
      }
    ],
    "references": [
      {
        "name": "Microsoft Copilot",
        "description": "Microsoft Copilot",
        "url": "https://copilot.microsoft.com/"
      }
    ]
  }
]
```

**Key metadata rules:**
- `name`: Always `copilotprompts-agent-{agent-name}` where `{agent-name}` is the folder name
- `shortDescription` and `longDescription[0]`: Should describe the agent's purpose; `longDescription` can be more detailed
- `creationDateTime` and `updateDateTime`: Use `YYYY-MM-DD` format with the current date
- `products`: Always `["Copilot"]` for agent instruction samples
- `source`: Always `"pnp"`
- `url`: Points to `samples/agent-instructions/{agent-name}` on GitHub main branch
- `downloadUrl`: Uses the pnp partial download service URL pointing to the same path
- `pictureUrl` for authors: Use `https://avatars.githubusercontent.com/{username}`
- `thumbnails`: Point to the required sample-specific static PNG and provide descriptive alt text

## Step 3: Remind About Screenshots

After creating the files, remind the user to:
1. Add a screenshot of the agent in action as `assets/demo.png`
2. Update the thumbnail URL and alt text if a different PNG filename is used
3. Keep the screenshot reference in `README.md` aligned with that file
4. Additional GIF, JPEG, or WebP media is optional, but at least one static PNG is required

## Writing Good Agent Instructions

When helping a user craft their system prompt, encourage them to include these sections:

1. **Purpose / Identity** — Who is the agent? What is its core mission?
2. **Execution Steps** — Step-by-step workflow the agent follows
3. **Operating Principles / Guidelines** — Rules and constraints for the agent's behavior
4. **Tone** — How the agent should communicate (warm, professional, playful, etc.)
5. **Example Interactions** (optional) — Sample conversations showing expected input/output
6. **Limitations** (optional) — What the agent cannot or should not do
7. **Privacy and Safety** (optional) — Any data handling or safety considerations

The system prompt should be detailed enough that anyone can paste it into Copilot Studio's Instructions field and get a working agent.

## Validation Checklist

Before finalizing, verify:
- [ ] Folder is inside `samples/agent-instructions/` (NOT directly under `samples/`)
- [ ] Folder name is lowercase with hyphens only, no dots, no app-host prefix
- [ ] `README.md` exists
- [ ] `README.md` contains the full system prompt in a fenced code block under the **Instruction** section
- [ ] At least one Use Case Category is checked
- [ ] `assets/` folder exists
- [ ] `assets/` contains at least one sample-specific static PNG
- [ ] `assets/sample.json` exists with valid JSON
- [ ] `sample.json` `name` field matches pattern `copilotprompts-agent-{agent-name}`
- [ ] `sample.json` `products` is `["Copilot"]`
- [ ] `sample.json` URLs include the full path `samples/agent-instructions/{agent-name}`
- [ ] `sample.json` dates are in `YYYY-MM-DD` format
- [ ] README tracking image URL matches `copilotprompts-agent-{agent-name}`
- [ ] README contains Instructions, Help, and Disclaimer sections
- [ ] Author information is filled in

## Key Rules

- **NEVER rephrase, rewrite, or modify the user's system prompt / agent instructions.** Always copy them verbatim into the README's Instruction section. The user's exact wording is the contribution.
- **This skill is for agent instruction / system prompt samples ONLY** — not for simple prompt samples
- Samples MUST go in `samples/agent-instructions/{agent-name}/`, never directly under `samples/`
- Every sample requires `README.md`, `assets/sample.json`, and at least one sample-specific static PNG in `assets/`
- The core contribution is the **system prompt / agent instructions** in the README's Instruction section
- The `products` field in sample.json is always `["Copilot"]` (these are Copilot Studio agents)
- Prerequisites are always "Copilot License"
- The Instructions section always describes the Copilot Studio agent builder workflow
- The `sample.json` feeds the [M365 Solution Gallery](https://adoption.microsoft.com/en-us/sample-solution-gallery/) — accuracy matters
- Follow existing naming patterns in the `agent-instructions` folder for consistency
