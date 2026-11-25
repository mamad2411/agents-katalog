---
name: huashu-article-edit
description: Standardised article editing workflow that ensures the scope of changes is clear, progress is trackable, and all modifications are documented. Use when the user says "edit article", "revise article", "adjust content", or "tweak this piece".
---

# Article Editing Skill

A standardised article editing workflow that solves the problem of losing editing work due to session interruptions.

## When to Use

- The user asks to edit, revise, or polish an existing article
- Multiple edits need to be made to an article
- Tasks include content trimming, tone adjustment, structural reorganisation, etc.

## Execution Workflow

### Step 1: Read the Target Article in Full

- Use the Read tool to read the article completely
- Quickly understand the article's topic, structure, and current state

### Step 2: List All Planned Edits

- Based on the user's requirements, list all items that need to be changed
- For each item, indicate: location (which paragraph), type of change (delete / rewrite / adjust), and specific content
- **Wait for user confirmation of scope before making any changes**

### Step 3: Incremental Editing + Save After Each Batch

- Save the file after every related group of edits is completed
- Report progress to the user after every 3–5 edits:

```text
  Progress: X/Y items completed
  ✅ Done: [list]
  ⏳ Remaining: [list]
  ```

### Step 4: Summary Upon Completion

- Provide a summary of all changes made
- Explain the rationale behind each edit
- If any external information was referenced, include the sources

## Key Principles

- **Confirm before acting**: Never assume the scope of changes
- **Save as you go**: Save after each batch of edits to prevent loss due to session interruption
- **Transparent changes**: The user should always know what was changed and why
- **Preserve style**: Edits must still conform to Huashu's writing style (see SHARED-RULES.md)

## Relationship with the Proofreading Workflow

- Once editing is complete, the user may trigger a three-pass proofreading review (`/AI-taste-proofreading`) if needed
- The Editing Skill focuses on "changing per requirements"; the Proofreading Skill focuses on "reducing AI-sounding language"

**Last Updated**: 2026-02-06

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
