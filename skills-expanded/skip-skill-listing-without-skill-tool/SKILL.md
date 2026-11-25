---
name: skip-skill-listing-without-skill-tool
description: "Omit skill-listing attachments for agents that do not expose the Skill tool, so discoverability context is only sent where it can be acted on."
metadata:
  author: ychampion
---

# SKILL: Skip Skill Listing Without Skill Tool
**Domain:** command-surfaces  
**Trigger:** Apply when an attachment or context injector is about to advertise capabilities to an agent that may not have the tool needed to use them.
**Source Pattern:** Distilled from reviewed command-surface and listing-control patterns.

## Core Method
Before generating capability-discovery context, verify that the receiving agent actually exposes the execution surface for it. If the agent lacks the `Skill` tool, return no skill-listing attachment at all rather than spending tokens on a catalog it cannot invoke. This keeps the prompt focused on actionable affordances and avoids confusing agents with instructions they have no mechanism to execute.

## Key Rules
- Check tool availability before doing any skill-listing work, including command collection or formatting.
- Treat missing execution surfaces as a hard stop, not as a degraded listing mode.
- Keep the guard close to the listing entrypoint so later refactors cannot accidentally compute listings for unsupported agents.
- Prefer actionable context over informative-but-unusable context; if the agent cannot call the tool, omit the attachment.

## Example Application
If a background helper agent is configured only with file and shell tools, skip injecting a skill catalog even if the parent session supports skills. The helper sees only the tools it can actually use, while the main agent continues receiving skill-listing updates normally.

## Anti-Patterns (What NOT to do)
- Do not send a skill listing just because the overall application supports skills; the specific consumer must expose the `Skill` tool.
- Do not compute and then discard the listing after expensive formatting work; guard before the heavy path starts.
