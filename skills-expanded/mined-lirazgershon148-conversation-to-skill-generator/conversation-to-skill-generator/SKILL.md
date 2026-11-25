---
name: conversation-to-skill-generator
description: Analyzes conversations to extract patterns and workflows, then generates Skill.md files matching user's style. Use to convert successful chats into reusable skills.
---

# Conversation to Skill Generator

**Version:** 2.1.0  
**Last Updated:** October 28, 2025  
**Status:** Production Ready


A meta-skill that analyzes existing conversations and generates properly formatted Skill.md files based on identified patterns, workflows, and best practices—while preserving the user's communication style.

## When to Use This Skill

Use this skill when you want to:
- Convert a successful conversation into a reusable skill
- Extract workflows and methodologies from completed chats
- Transform one-off solutions into standardized frameworks
- Capture specialized knowledge for future use
- Build a library of domain-specific skills from actual usage patterns

**Common trigger phrases:**
- "Analyze this conversation and generate a skill"
- "Extract a skill from this completed conversation"
- "Turn our past discussion into a reusable skill"
- "Generate Skill.md from this conversation"
- "Create a skill based on the workflow in this chat"

---

## Prerequisites

Before using this skill, ensure:
- You have access to the conversation (current chat, share link, or copied text)
- The conversation contains a clear workflow, methodology, or pattern worth capturing
- You understand the basic Skill.md format (see `reference/skill-structure-guide.md`)

**⚠️ CRITICAL:** Always read `reference/anthropic-best-practices.md` before creating any skill to ensure compliance with current standards.

---

## Core Process (5 Steps)

### Step 1: Gather Conversation Data

**Three input methods:**

**A. In-Place Analysis (Easiest)**
- At the end of your current conversation, say: "Analyze this conversation and generate a skill"
- Claude will analyze the current context
- Best for: Conversations you just completed

**B. Share Link (Clean)**
- Click "Share" on any conversation → Copy URL
- In a new chat: "Analyze this conversation and create a skill: [URL]"
- Best for: Past conversations or conversations from others

**C. Copy-Paste (Fallback)**
- Copy full conversation text
- Paste with context: "Here's a conversation I want to turn into a skill: [paste]"
- Best for: When other methods aren't available

---

### Step 2: Read Documentation & Analyze

**Critical order - Claude MUST follow:**

1. **FIRST:** Read `reference/anthropic-best-practices.md` ⚠️
   - This is NON-NEGOTIABLE
   - Ensures generated skill complies with current Anthropic standards
   - Reviews format requirements, structure rules, security considerations

2. **SECOND:** Read `reference/analysis-framework.md`
   - Learn how to analyze conversations comprehensively
   - Understand content analysis vs. style analysis
   - Apply contextual understanding techniques

3. **THIRD:** Perform the analysis
   - Read entire conversation (all messages from both user and Claude)
   - Identify patterns, workflows, tools, and methodologies
   - Analyze communication style contextually (not in isolation)
   - Determine if workflow is generalizable

For detailed analysis guidance, see: `reference/analysis-framework.md`

---

### Step 3: Present Summary for Confirmation

After analysis, present a concise summary to the user:

```
📊 Conversation Analysis Summary:

**Identified Workflow:** [Brief description]

**Key Elements:**
- Main purpose: [...]
- Core methodology: [...]
- Tools/technologies: [...]
- Repeatable patterns: [...]

**Proposed Skill:**
- Name: [suggested-skill-name]
- Description: [what it does + when to use - under 180 chars]
- Structure: [Simple / Advanced with reference files]

**Communication Style:** [Brief note on tone/approach that worked]

---

Does this look correct? Any adjustments needed before I generate the full skill?
```

**Wait for user confirmation before proceeding.**

---

### Step 4: Generate Skill Structure

Based on user confirmation, generate the skill using:

**For simple skills:**
- Use template from `templates/skill-template-simple.md`
- Single SKILL.md file, self-contained

**For complex skills:**
- Use template from `templates/skill-template-advanced.md`
- Create reference files for detailed content
- Organize by domain if multiple areas covered

**Quality checks:**
- Review `reference/quality-checklist.md` before finalizing
- **⚠️ Ensure Context Awareness Rule is included in Step 1 of generated skill**
- Ensure description is under 180 characters
- Verify YAML frontmatter is correct
- Confirm all file references are one level deep
- Check for consistent terminology

For complete structure guidelines, see: `reference/skill-structure-guide.md`

---

### Step 5: Present & Iterate

Present the generated skill to the user in a clear format:

```markdown
# Generated Skill: [skill-name]

[Show complete SKILL.md content]

---

## Additional Files (if applicable)
- reference/[filename].md
- templates/[filename].md
- resources/[filename].md

---

## Next Steps:
1. Review the skill content
2. Request any adjustments
3. Download as ZIP file
4. Upload to Claude.ai (Settings > Capabilities)
5. Test with varied prompts

Would you like me to adjust anything?
```

**Iterate based on user feedback** until the skill meets their needs.

---

## Key Principles

When generating skills, always:

1. **Follow Anthropic Standards**
   - Read `reference/anthropic-best-practices.md` first
   - Keep SKILL.md under 500 lines
   - Use progressive disclosure for complex content

2. **Prioritize Description Quality**
   - The description field (max 180 chars recommended) is CRITICAL
   - Must include both "what it does" + "when to use it"
   - Use specific keywords that trigger activation

3. **Include Context Awareness**
   - Every skill MUST include Context Awareness Rule in Step 1
   - This ensures Claude reads full conversation history before acting
   - Prevents ignoring user's earlier messages or context
   - Critical for maintaining continuity in conversations

4. **Understand Style Contextually**
   - Analyze conversation dynamics, not isolated messages
   - Match the successful communication pattern that emerged
   - Balance user's voice with clarity (don't sacrifice usability)

5. **Create Evaluation Scenarios**
   - Before extensive documentation, create 3 test scenarios
   - See `resources/evaluation-scenarios.md` for examples
   - Test the skill with varied prompts after creation

6. **Collaborate with User**
   - Present draft, get feedback, iterate
   - Make skills feel personalized and relevant
   - Ensure clarity and usability

---

## File Organization

This skill uses progressive disclosure:

- **SKILL.md** (this file) - High-level guide with core process
- **reference/** - Detailed guides loaded when needed
  - `analysis-framework.md` - How to analyze conversations
  - `anthropic-best-practices.md` - Anthropic's official guidelines
  - `skill-structure-guide.md` - Complete structure reference
  - `quality-checklist.md` - Pre-creation validation
- **templates/** - Ready-to-use templates
  - `skill-template-simple.md` - Basic template
  - `skill-template-advanced.md` - Complex template with references
- **resources/** - Additional materials
  - `evaluation-scenarios.md` - Test cases
  - `common-triggers.md` - Activation phrases
  - `external-links.md` - Official documentation links

---

## Troubleshooting

**Skill doesn't activate when expected:**
- Check description includes clear trigger keywords
- Ensure skill is toggled ON in Settings > Capabilities
- Try more explicit trigger phrases
- Review Claude's thinking to see activation logic

**Generated skill is too complex:**
- Split into multiple focused skills
- Use reference files for detailed content
- Keep SKILL.md under 500 lines

**Style doesn't match user preferences:**
- Re-analyze conversation with focus on successful exchanges
- Ask user for explicit style preferences
- Iterate based on feedback

For comprehensive troubleshooting, see official resources in `resources/external-links.md`

---

## Meta Note

This skill is itself an example of what it creates—it was generated through the process it describes!

**Remember:** A good skill doesn't just capture a workflow—it captures it in a way that's clear, usable, and feels natural to the person who will use it.

---

## Quick Reference

**Before creating:** Read `reference/anthropic-best-practices.md`  
**During analysis:** Follow `reference/analysis-framework.md`  
**For structure:** Check `reference/skill-structure-guide.md`  
**Before finalizing:** Review `reference/quality-checklist.md`  
**For testing:** Use scenarios from `resources/evaluation-scenarios.md`
