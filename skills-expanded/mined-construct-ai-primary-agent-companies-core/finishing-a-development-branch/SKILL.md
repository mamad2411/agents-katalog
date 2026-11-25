---
memory_layer: durable_knowledge
para_section: pages/skills/finishing-a-development-branch
gigabrain_tags: git, branching, completion, integration, workflow
openstinger_context: development-completion, branch-integration, workflow-finalization
last_updated: 2026-03-30
related_docs:
  - docs/superpowers/plans/
  - docs/superpowers/specs/
related_skills:
  - executing-plans
  - using-git-worktrees
  - verification-before-completion
frequency_percent: 92.0
success_rate_percent: 95.0
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 3: Present Options

Present exactly these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d <feature-branch>
```

Then: Cleanup worktree (Step 5)

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then: Cleanup worktree (Step 5)

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5)

### Step 5: Cleanup Worktree

**For Options 1, 2, 4:**

Check if in worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

If yes:
```bash
git worktree remove <worktree-path>
```

**For Option 3:** Keep worktree.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Present exactly 4 structured options

**Automatic worktree cleanup**
- **Problem:** Remove worktree when might need it (Option 2, 3)
- **Fix:** Only cleanup for Options 1 and 4

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

**Always:**
- Verify tests before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## When to Use This Skill

**Trigger Conditions:**
- After completing all implementation tasks in a development branch
- When all tests pass and work is ready for integration
- After successful execution of plans using executing-plans or subagent-driven-development
- When needing to decide between local merge, PR creation, or branch preservation
- After verification that all acceptance criteria are met
- When work in isolated worktree is complete and ready for integration
- Before finalizing any development work for production deployment

**Prerequisites:**
- All implementation tasks completed successfully
- Tests passing in the development environment
- Work completed in isolated git worktree (not main/master)
- Acceptance criteria verified and met
- Code ready for integration or review

## Step-by-Step Procedure

### Step 1: Comprehensive Test Verification
**Verify all tests pass before any integration decisions:**

```javascript
// Run complete test suite verification
async function verifyAllTests() {
  const testResults = {
    unit: await runCommand('npm run test:unit'),
    integration: await runCommand('npm run test:integration'),
    e2e: await runCommand('npm run test:e2e'),
    build: await runCommand('npm run build')
  };

  // Check all results
  const allPassed = Object.values(testResults).every(result => result.exitCode === 0);

  if (!allPassed) {
    const failures = Object.entries(testResults)
      .filter(([_, result]) => result.exitCode !== 0)
      .map(([type, result]) => `${type}: ${result.errorMessage}`);

    throw new Error(`Tests failed:\n${failures.join('\n')}`);
  }

  return testResults;
}
```

**Verification Requirements:**
- Unit tests pass completely
- Integration tests pass
- End-to-end tests pass (if applicable)
- Build completes successfully
- No test regressions introduced

**If any tests fail:** Stop immediately and fix issues before proceeding

### Step 2: Determine Base Branch and Context
**Identify the target branch for integration:**

```bash
# Determine base branch automatically
determineBaseBranch() {
  # Try common base branch names
  for (const baseBranch of ['main', 'master', 'develop', 'development']) {
    try {
      const mergeBase = execSync(`git merge-base HEAD ${baseBranch}`, { encoding: 'utf8' }).trim();
      if (mergeBase) {
        return baseBranch;
      }
    } catch (error) {
      // Branch doesn't exist or no common base
      continue;
    }
  }

  // Ask user if automatic detection fails
  return await promptUser('What is the base branch for this work? (main/master/develop)');
}

# Get branch information
const currentBranch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
const baseBranch = determineBaseBranch();
const worktreePath = execSync('git worktree list | grep $(pwd) | awk \'{print $1}\'', { encoding: 'utf8' }).trim();
```

**Context Gathering:**
- Current feature branch name
- Target base branch for integration
- Worktree path for cleanup decisions
- Commit history and changes summary

### Step 3: Present Integration Options
**Offer exactly 4 structured completion options:**

```javascript
// Present completion options to user
async function presentCompletionOptions(context) {
  const options = [
    {
      id: 1,
      title: `Merge back to ${context.baseBranch} locally`,
      description: 'Integrate changes directly into base branch',
      action: 'local_merge'
    },
    {
      id: 2,
      title: 'Push and create a Pull Request',
      description: 'Push branch and open PR for review',
      action: 'create_pr'
    },
    {
      id: 3,
      title: 'Keep the branch as-is',
      description: 'Preserve branch and worktree for later handling',
      action: 'preserve'
    },
    {
      id: 4,
      title: 'Discard this work',
      description: 'Permanently delete branch and all changes',
      action: 'discard'
    }
  ];

  console.log('🎯 Implementation complete. What would you like to do?\n');

  options.forEach(option => {
    console.log(`${option.id}. ${option.title}`);
    console.log(`   ${option.description}\n`);
  });

  const choice = await promptUser('Enter option number (1-4):');
  return options.find(opt => opt.id === parseInt(choice));
}
```

**Option Presentation:**
- Exactly 4 options (no more, no less)
- Clear, concise descriptions
- No additional explanations or recommendations
- Structured numerical selection

### Step 4: Execute Selected Option
**Implement the chosen completion strategy:**

#### Option 1: Local Merge
```bash
# Switch to base branch
git checkout "$BASE_BRANCH"

# Pull latest changes
git pull origin "$BASE_BRANCH"

# Merge feature branch
git merge "$CURRENT_BRANCH"

# Verify tests on merged result
npm test

# If tests pass, delete feature branch
if [ $? -eq 0 ]; then
  git branch -d "$CURRENT_BRANCH"
  echo "✅ Successfully merged and cleaned up branch"
else
  echo "❌ Tests failed after merge - please resolve conflicts"
  exit 1
fi
```

#### Option 2: Create Pull Request
```bash
# Push feature branch to remote
git push -u origin "$CURRENT_BRANCH"

# Generate PR description
PR_BODY=$(cat << EOF
## Summary
$(git log --oneline "$BASE_BRANCH..HEAD" | head -5)

## Changes
$(git diff --stat "$BASE_BRANCH..HEAD")

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Build succeeds
- [ ] Manual testing completed
EOF
)

# Create PR using GitHub CLI
gh pr create \
  --title "$(git log --oneline -1 | sed 's/^[a-f0-9]* //')" \
  --body "$PR_BODY" \
  --base "$BASE_BRANCH" \
  --head "$CURRENT_BRANCH"

echo "✅ Pull request created successfully"
```

#### Option 3: Preserve Branch
```bash
# Keep branch and worktree intact
echo "📁 Branch '$CURRENT_BRANCH' preserved"
echo "📂 Worktree kept at: $(pwd)"
echo "💡 You can return to this work later or handle it manually"

# No cleanup performed
exit 0
```

#### Option 4: Discard Work
```bash
# Require explicit confirmation
read -p "⚠️  This will permanently delete branch '$CURRENT_BRANCH' and all commits. Type 'discard' to confirm: " confirmation

if [ "$confirmation" != "discard" ]; then
  echo "❌ Confirmation failed - work preserved"
  exit 1
fi

# Show what will be deleted
echo "🗑️  Will delete:"
echo "   Branch: $CURRENT_BRANCH"
echo "   Commits: $(git log --oneline "$BASE_BRANCH..HEAD" | wc -l)"
echo "   Worktree: $(pwd)"

# Switch to base branch and delete feature branch
git checkout "$BASE_BRANCH"
git branch -D "$CURRENT_BRANCH"

echo "✅ Work discarded successfully"
```

### Step 5: Worktree Cleanup
**Clean up development environment based on chosen option:**

```bash
# Worktree cleanup logic
cleanupWorktree() {
  local action=$1
  local worktree_path=$(pwd)

  case $action in
    "local_merge"|"create_pr"|"discard")
      # Remove worktree for completed work
      if git worktree list | grep -q "$worktree_path"; then
        echo "🧹 Cleaning up worktree..."
        cd ..
        git worktree remove "$worktree_path"
        echo "✅ Worktree removed"
      else
        echo "ℹ️  Not in a worktree - no cleanup needed"
      fi
      ;;
    "preserve")
      # Keep worktree for later use
      echo "📂 Worktree preserved at: $worktree_path"
      echo "💡 Use 'git worktree remove $worktree_path' when done"
      ;;
  esac
}

# Execute cleanup based on chosen action
cleanupWorktree "$SELECTED_ACTION"
```

**Cleanup Rules:**
- Remove worktree for Options 1, 2, 4 (completed work)
- Preserve worktree for Option 3 (work kept for later)
- Ensure clean environment state

### Step 6: Final Status Report
**Provide completion summary and next steps:**

```javascript
// Generate completion report
function generateCompletionReport(choice, results) {
  const report = {
    action: choice.action,
    timestamp: new Date().toISOString(),
    branch: results.branch,
    baseBranch: results.baseBranch,
    commits: results.commitCount,
    worktreeCleaned: results.worktreeRemoved,
    nextSteps: getNextSteps(choice.action)
  };

  // Log completion
  console.log('🎉 Development branch completion successful!');
  console.log(`Action: ${choice.title}`);
  console.log(`Branch: ${results.branch}`);
  console.log(`Next: ${report.nextSteps}`);

  return report;
}

function getNextSteps(action) {
  switch (action) {
    case 'local_merge':
      return 'Changes integrated locally - ready for push if needed';
    case 'create_pr':
      return 'PR created - await review and approval';
    case 'preserve':
      return 'Branch preserved - handle manually later';
    case 'discard':
      return 'Work discarded - start fresh if needed';
  }
}
```

**Completion Reporting:**
- Action taken summary
- Branch and integration status
- Next steps guidance
- Worktree cleanup status

## Success Criteria

- [ ] All tests pass before presenting options
- [ ] Base branch correctly identified
- [ ] Exactly 4 options presented clearly
- [ ] Chosen option executed correctly
- [ ] Worktree cleaned up appropriately
- [ ] Final status reported accurately
- [ ] No uncommitted changes left behind
- [ ] Branch state matches chosen option

## Common Pitfalls

1. **Proceeding with Failing Tests** - Never offer options until all tests pass
2. **Wrong Base Branch** - Always verify merge-base before operations
3. **Automatic Assumptions** - Present all 4 options, let user choose
4. **Missing Confirmations** - Require typed confirmation for destructive actions
5. **Improper Cleanup** - Only remove worktree when work is truly complete
6. **Incomplete Reporting** - Always provide clear next steps

## Integration Options Reference

### Local Merge Workflow
```bash
# Complete local integration
git checkout main && git pull && git merge feature-branch && npm test && git branch -d feature-branch
```

### Pull Request Workflow
```bash
# PR creation with proper setup
git push -u origin feature-branch
gh pr create --title "Feature: description" --body "Detailed description with test plan"
```

### Preservation Workflow
```bash
# Keep for later handling
echo "Branch preserved - handle manually"
# No cleanup performed
```

### Discard Workflow
```bash
# Safe deletion with confirmation
echo "Type 'discard' to permanently delete branch and all commits"
# Only proceed with exact confirmation
```

## Cross-References

### Related Procedures
- [Executing Plans Skill](skills/executing-plans/SKILL.md) - Calls this skill upon completion
- [Subagent Driven Development Skill](skills/subagent-driven-development/SKILL.md) - Alternative completion path
- [Using Git Worktrees Skill](skills/using-git-worktrees/SKILL.md) - Worktree creation and cleanup

### Related Skills
- `executing-plans` - Plan execution that leads to this skill
- `subagent-driven-development` - Alternative execution method
- `using-git-worktrees` - Worktree management
- `verification-before-completion` - Quality assurance integration

### Related Agents
- `DevForge_AI_Team` - Development workflow assistance
- `QualityForge_AI_Team` - Quality verification and testing
