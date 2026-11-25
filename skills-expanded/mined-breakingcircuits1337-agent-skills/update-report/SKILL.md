---
name: update-report
description: Use when completing changes that affect memory, documentation, or capabilities - documents what changed and verifies functionality
---

# Update Report

## Overview

Document all changes made during a session with verification that code actually works. Update relevant memory files after any modifications to ensure continuity.

## When to Use

- After making changes to memory files (CLAUDE.md, SOUL.md, USER.md, etc.)
- After creating new skills or updating existing ones
- After modifying project structure or configuration
- After adding new capabilities or tools

## Core Workflow

### 1. Document Changes

Create a clear summary of what was modified:
- **Files changed**: List all modified/created files
- **Purpose**: Why the changes were made
- **Capabilities added**: What new functionality exists
- **Verification**: Proof that changes work (not just "should work")

### 2. Verify Before Claiming

**ALWAYS verify code can do what you claim before stating it:**

| Claim Type | Verification Method |
|------------|---------------------|
| Script works | Run the script with test input |
| Memory loads | Run memory.py and check output |
| Command exists | Run the command with --help or test |
| File created | Read the file back and confirm content |
| Skill works | Run a test scenario with the skill |

**NEVER claim capabilities without proof.** "Should work" = "didn't verify"

### 3. Update Memory

After any changes that affect knowledge base:

1. **Update LONG-TERM (CLAUDE.md)** for:
   - New infrastructure
   - New tools/services
   - Changed configurations
   - New skills

2. **Update USER.md** for:
   - New projects
   - Changed user context

3. **Update TOOLS.md** for:
   - New commands/scripts
   - Changed tool capabilities

4. **Update MEDIUM_TERM.md** for:
   - Active project changes
   - Recent learnings

5. **Update SHORT_TERM.md** for:
   - Current session tasks
   - Session-specific context

### 4. Verify Memory Loads

After updating memory files, always run:
```bash
python3 /home/bc/bin/memory.py
```

Confirm:
- All files load without errors
- Content is correct and complete
- No missing sections

## Update Report Template

```markdown
## Update Report - [Date]

### Summary
[Brief overview of what was done]

### Changes Made

| File | Change Type | Verification |
|------|-------------|--------------|
| path/to/file | created/modified | [proof it works] |

### Capabilities Added
- [New capability with verification method]

### Memory Updates
- [Files updated in memory hierarchy]

### Verification
- [ ] Ran memory loader - confirmed working
- [ ] Tested new capabilities - [results]
- [ ] [Other verifications]
```

## Red Flags - Don't Do This

- Claiming "should work" without running it
- Updating memory without verifying loads
- Forgetting to update relevant memory files
- Stating capabilities that weren't tested
- Skipping verification steps when "sure" it works

## Quick Reference

```bash
# Verify memory loads
python3 /home/bc/bin/memory.py

# Test a script
python3 /path/to/script.py [test_args]

# Check file exists and has content
cat /path/to/file

# Verify command works
command --help
```

## Real Example

**Task**: Create memory system with 7 files

**Verification performed**:
1. Created each file with write tool
2. Ran `python3 /home/bc/bin/memory.py`
3. Confirmed all 7 sections loaded
4. Verified content was correct in output

**Memory updated**: CLAUDE.md, USER.md, TOOLS.md, MEDIUM_TERM.md

**Result**: Verified working, not "should work"
