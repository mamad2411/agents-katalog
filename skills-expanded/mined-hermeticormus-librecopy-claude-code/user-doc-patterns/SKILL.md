---
name: "user-doc-patterns"
description: "End-user documentation patterns: user vs developer documentation, writing for non-technical readers, article types, and screenshot guidelines. Use when writing help center or product documentation."
---

# User Doc Patterns

> Patterns for writing clear, accessible end-user documentation.

## Knowledge Base

### User Documentation vs Developer Documentation

| User Docs | Developer Docs |
|-----------|---------------|
| Task-oriented ("How do I...") | Concept-oriented ("How does it work...") |
| Plain language | Technical language |
| Screenshots and visual aids | Code examples |
| Step-by-step procedures | API references |
| Feature names and UI labels | Function signatures and parameters |
| Avoids technical internals | Explains technical internals |

### Writing for Non-Technical Readers

**Vocabulary rules:**
- Use "click" not "select" or "actuate"
- Use "type" not "enter" or "input"
- Use "choose" not "select from the dropdown"
- Use "go to" not "navigate to"
- Use "shows" not "renders" or "displays"
- Use "saves" not "persists"

**Sentence structure:**
- Active voice: "Click the button" not "The button should be clicked"
- Imperative for instructions: "Open Settings" not "You should open Settings"
- Short sentences: Under 25 words per sentence
- One idea per sentence

**Formatting:**
- Bold exact UI labels: Click **Save Changes**
- Use > for navigation paths: **Settings** > **Team** > **Permissions**
- One action per numbered step
- Use notes/warnings for important caveats

### Article Types

**Walkthrough** (procedural):
```
Title: "How to [accomplish task]"
Structure: Prerequisites > Steps > Confirmation > Related
Use when: User needs to complete a specific task
```

**Overview** (conceptual):
```
Title: "[Feature name]: What it does and how it works"
Structure: What > Why > Key concepts > Getting started link
Use when: User needs to understand a feature before using it
```

**Troubleshooting** (problem-solving):
```
Title: "Fix: [problem description]"
Structure: Symptom > Cause > Solution > Prevention
Use when: User encounters a specific error or problem
```

**FAQ** (reference):
```
Title: "[Topic] FAQ"
Structure: Grouped questions with direct answers
Use when: Users have many small questions about a topic
```

### Screenshot Guidelines

1. **Show only the relevant area** -- crop to the element being discussed
2. **Annotate with arrows or highlights** -- draw attention to the specific button/field
3. **Use consistent dimensions** -- same width for all screenshots in an article
4. **Include alt text** -- describe what the screenshot shows for screen readers
5. **Update on UI changes** -- stale screenshots are worse than no screenshots
6. **Mark screenshot locations** -- use `![Description](path)` markers even before screenshots exist

## Patterns

1. **Task-First Titles**: "How to export your data" not "Data Export Feature." Users search for tasks, not features.
2. **Prerequisites Gate**: List everything the user needs before starting. Prevents frustration from discovering requirements mid-task.
3. **One Path**: Document the recommended path. Do not document every possible way to accomplish the task. Mention alternatives in a note.
4. **Confirmation Step**: End every procedure with how to verify it worked. Users need to know they succeeded.
5. **Next Actions**: After completing a task, suggest what the user might want to do next. Keeps them productive.

## Anti-Patterns

1. **Engineer Brain**: Explaining database schema when the user just wants to change their password.
2. **The Options Overload**: Documenting every setting, toggle, and checkbox in one article. Focus on the common tasks.
3. **Passive Instructions**: "The settings page can be accessed by clicking..." -- just say "Click **Settings**."
4. **Assuming Navigation**: "Go to the billing page" -- say where it is: "Click **Settings** in the sidebar, then click **Billing**."
5. **Jargon Leak**: Using words like "authentication," "endpoint," "payload," or "schema" in user-facing docs.
6. **No Context**: Step 1: "Click Create." Where is the Create button? On what page? What does it create?

## References

- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Plainlanguage.gov](https://www.plainlanguage.gov/)
- [Nielsen Norman Group - Help and Documentation](https://www.nngroup.com/articles/help-and-documentation/)
