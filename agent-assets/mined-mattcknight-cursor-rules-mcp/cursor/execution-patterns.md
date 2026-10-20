---
description: Execution patterns and workflow standards for AI task execution
alwaysApply: false
tags: [ai-guidelines, execution, workflow, patterns]
priority: 2
version: 1.0.0
---
### Phase 1: [Name]
🔄 Working...
[Execute operation]
✅ Step complete

✅ **Phase 1 COMPLETE**

---

### Final Summary
✅ **TASK COMPLETE!**

What was done:
- Item 1 ✅
- Item 2 ✅

Verification: [command to verify]
Next steps: [recommendation]
```

---

## Command Execution Rules

### Never Chain Commands
```powershell
❌ Copy-Item "a.md" "b.md"; Copy-Item "c.md" "d.md"
✅ Execute one command, wait, then next
```

### Limit Recursive Operations
```powershell
❌ Get-ChildItem -Recurse (without limits)
✅ Get-ChildItem -Depth 1 or -Depth 2
```

### Single Operation Per Command
- One file copy at a time
- One directory creation at a time
- One validation check at a time

---

## Progress Updates

**For operations > 30 seconds:**
- **MUST** warn user: "This operation may take 1-2 minutes"
- **MUST** provide progress updates: "Creating file 3 of 10..."
- **SHOULD** give timeout guidance if operation appears stuck

---

## Error Handling

**If ANY command fails:**
1. Acknowledge immediately: "❌ Error occurred"
2. Explain what went wrong
3. Provide options to user
4. DON'T continue silently

---

## Completion Signals

**ALWAYS end with:**
```markdown
✅ **COMPLETE!** [Task name]

Summary: [What was accomplished]
Files created: [Count]
Verification: [How to check]
Next: [Recommendation]
```

---

## Uncertainty Handling

When uncertain about ANY fact:

```
⚠️ UNCERTAIN: [Topic]

I cannot find confirmation for [specific fact] in the source documents.

Checked:
- ✗ Requirements document
- ✗ Technical design document
- ✗ Architecture documents

Recommendation:
1. [Suggested action]
2. [Alternative approach]

Please confirm or provide source document.
```

---

## Code Generation Guidelines

### Before Generating Code

1. **Load Context:**
   - Requirements documents
   - Design specifications
   - Architecture documents
   - Existing code patterns

2. **Validate Against Rules:**
   - Check forbidden patterns
   - Verify required patterns
   - Confirm coding standards

3. **Provide Traceability:**
   - Cite requirement ID
   - Link to design section
   - Reference test coverage

### After Generating Code

4. **Generate Tests:**
   - Unit test for each method
   - Integration test for each flow
   - Update test count

5. **Update Documentation:**
   - Mark requirement progress
   - Update design documents if architecture changed
   - Create decision records if architectural decision made

---

## Quick Reference Commands

### Validate Context
```
1. Load project rules
2. Load requirements documents
3. Load design specifications
4. Confirm: All loaded, no conflicts, ready to proceed
```

### Start Implementation
```
Task: Implement [REQUIREMENT_ID]

1. Show current code
2. Propose changes with requirement comments
3. Generate unit tests
4. Check if docs need updates
```

### End Session
```
Generate session summary:
- Implemented: [list]
- Tests created: [count]
- Docs updated: [list]
- Next: [recommendation]
- Blockers: [any issues]
```

---

## Session Documentation

### End-of-Session Summary

**When to Offer:**
- After completing multi-step task
- When user says "done", "that's all", etc.
- After significant document updates
- When TODO list completed

**How to Offer:**
- Wait for natural pause
- Say: "Would you like me to create a session summary?"

**Location:** `docs/session-logs/session_YYYY-MM-DD_HHMM.md`

**Include:**
- User goals
- All user prompts (chronological)
- Work completed
- Files modified
- Commands run
- Issues encountered
- Next steps
- Artifacts created

**Important:**
- Never create unless user requests or accepts offer
- Keep factual and concise
- Include exact user prompts (don't paraphrase)
- Document successes AND failures

---

## Best Practices

### General Principles

1. **Validate before assuming** - Check actual code/files
2. **Be accurate** - Code quality matters for production projects
3. **Never make assumptions** - Ask or search codebase
4. **Always check source of truth** - Requirements override assumptions
5. **Test claims against code** - Verify names, methods, signatures

### Communication Standards

1. **Be Clear:** Use simple, direct language
2. **Be Factual:** State what IS, not what MIGHT BE
3. **Be Explicit:** Don't assume user knows context
4. **Be Complete:** Include all relevant information
5. **Be Professional:** Maintain consistent tone

### Workflow Standards

1. **Plan First:** Outline approach before executing
2. **Update Frequently:** Keep user informed of progress
3. **Verify Always:** Check results after each operation
4. **Document Decisions:** Explain why choices were made
5. **Clean Up:** Remove temporary files when done

---

## Anti-Patterns to Avoid

### ❌ DON'T:
- Start work without explaining the plan
- Chain multiple risky operations together
- Continue silently after errors
- Make assumptions about user's environment
- Skip verification steps
- Leave temporary files behind
- Provide vague progress updates ("working on it...")
- Declare success without verification

### ✅ DO:
- Explain the plan upfront
- Execute operations one at a time
- Report errors immediately
- Ask when uncertain
- Verify each step
- Clean up temporary artifacts
- Provide specific progress ("updating file 3 of 5...")
- Verify and report completion with evidence

---

## Summary

**Key Principles:**
1. **Communicate clearly** - Explain what you're doing and why
2. **Execute safely** - One operation at a time, verify results
3. **Handle errors gracefully** - Report immediately, provide options
4. **Complete thoroughly** - Verify work, provide summary
5. **Stay factual** - Only state what you know, admit uncertainty

**Remember:** The user expects professional, reliable, and transparent execution. Always err on the side of over-communication rather than under-communication.

---

**Rule Status:** ✅ ACTIVE  
**Scope:** ALL AI task execution and communication  
**Purpose:** Ensure reliable, transparent, and professional AI behavior
