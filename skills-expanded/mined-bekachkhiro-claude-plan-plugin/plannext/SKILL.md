---
name: planNext
description: Plan Next Task Recommendation
---

# Plan Next Task Recommendation

You are an intelligent task prioritization assistant. Your role is to analyze the project plan and recommend the best next task to work on.

## Objective

Analyze PROJECT_PLAN.md to find the optimal next task based on dependencies, current phase, complexity, and project momentum.

## Usage

```bash
/planNext
```

No arguments needed - analyzes the entire project state.

## Process

### Step 0: Load User Language & Translations

**CRITICAL: Execute this step FIRST, before any output!**

Load user's language preference using hierarchical config (local → global → default) and translation file.

**Pseudo-code:**
```javascript
// Read config with hierarchy (v1.1.1+)
function getConfig() {
  // Try local config first
  if (fileExists("./.plan-config.json")) {
    try {
      return JSON.parse(readFile("./.plan-config.json"))
    } catch (error) {}
  }

  // Fall back to global config
  const globalPath = expandPath("~/.config/claude/plan-plugin-config.json")
  if (fileExists(globalPath)) {
    try {
      return JSON.parse(readFile(globalPath))
    } catch (error) {}
  }

  // Fall back to defaults
  return { "language": "en" }
}

const config = getConfig()
const language = config.language || "en"

// Cloud config (v1.2.0+)
const cloudConfig = config.cloud || {}
const isAuthenticated = !!cloudConfig.apiToken
const apiUrl = cloudConfig.apiUrl || "https://api.planflow.tools"
const autoSync = cloudConfig.autoSync || false

// Load translations
const translationPath = `locales/${language}.json`
const t = JSON.parse(readFile(translationPath))
```

**Instructions for Claude:**

1. Try to read `./.plan-config.json` (local, highest priority)
2. If not found/corrupted, try `~/.config/claude/plan-plugin-config.json` (global)
3. If not found/corrupted, use default: `language = "en"`
4. Use Read tool: `locales/{language}.json`
5. Store as `t` variable

### Step 1: Read PROJECT_PLAN.md

Use the Read tool to read PROJECT_PLAN.md from the current working directory.

If file doesn't exist, output:
```
{t.commands.update.planNotFound}

{t.commands.update.runPlanNew}
```

**Example:**
- EN: "❌ Error: PROJECT_PLAN.md not found in current directory. Please run /planNew first to create a project plan."
- KA: "❌ შეცდომა: PROJECT_PLAN.md არ მოიძებნა მიმდინარე დირექტორიაში. გთხოვთ ჯერ გაუშვათ /planNew პროექტის გეგმის შესაქმნელად."

### Step 2: Parse All Tasks

Extract all tasks with their properties:

For each task (`#### TX.Y: Task Name`), extract:
- **Task ID**: e.g., T1.1
- **Task Name**: e.g., "Project Setup"
- **Status**: TODO, IN_PROGRESS, DONE, BLOCKED
- **Complexity**: Low, Medium, High
- **Estimated**: Hours (e.g., "2 hours")
- **Dependencies**: List of task IDs or "None"
- **Phase**: Derived from task ID (T1.X = Phase 1, T2.X = Phase 2, etc.)
- **Description**: Task details

Create a mental model of all tasks.

### Step 3: Filter Available Tasks

A task is **available** if:
1. ✅ Status is TODO (not DONE, not IN_PROGRESS, not BLOCKED)
2. ✅ All dependencies are completed (status = DONE)
3. ✅ Task is in current phase or earlier incomplete phase

**Current Phase** = Lowest phase number that still has incomplete tasks

Example:
- Phase 1: 3/4 tasks done → Phase 1 is current
- Phase 2: 0/5 tasks done → Not current yet
- Phase 3: 0/3 tasks done → Not current yet

### Step 4: Rank Available Tasks

Score each available task using multiple factors:

#### Factor 1: Phase Priority (Weight: 40%)
```
Score = 100 if in current phase
Score = 50 if in next phase
Score = 0 if beyond next phase
```

Complete earlier phases before starting later ones (mostly).

#### Factor 2: Dependency Impact (Weight: 30%)
```
Count how many tasks depend on this task (directly or indirectly)
Score = (dependent_count / max_dependent_count) × 100
```

Prioritize tasks that unlock many others (critical path).

#### Factor 3: Complexity Balance (Weight: 20%)
```
Check recently completed tasks' complexity:
- If last task was High → prefer Low or Medium (Score: 100)
- If last task was Low → prefer Medium or High (Score: 100)
- Otherwise → Medium complexity gets Score: 100

Prevents burnout and maintains momentum.
```

#### Factor 4: Natural Flow (Weight: 10%)
```
Score = 100 if task ID is sequential (e.g., T1.1, T1.2, T1.3)
Score = 50 otherwise

Following sequential order often makes sense.
```

#### Calculate Total Score
```
Total = (Phase × 0.4) + (Dependencies × 0.3) + (Complexity × 0.2) + (Flow × 0.1)
```

Sort tasks by total score (highest first).

### Step 5: Select Top Recommendation

Pick the highest-scored task as the primary recommendation.

Also identify 2-3 alternative tasks (next highest scores).

### Step 6: Generate Recommendation

Display a detailed recommendation using translations.

**Pseudo-code:**
```javascript
const task = recommendedTask
const complexityText = t.templates.complexity[task.complexity.toLowerCase()]
// EN: "Low", "Medium", "High"
// KA: "დაბალი", "საშუალო", "მაღალი"

let output = t.commands.next.title + "\n\n"
output += t.commands.next.recommendedTask + "\n"
output += `T${task.id}: ${task.name}\n\n`
output += t.commands.next.complexity + " " + complexityText + "\n"
output += t.commands.next.estimated + " " + task.estimated + "\n"
output += t.commands.next.phase + " " + task.phase + "\n\n"
output += t.commands.next.dependenciesCompleted + "\n\n"
output += t.commands.next.whyThisTask + "\n"
output += reasons.map(r => "• " + r).join("\n") + "\n\n"
output += t.commands.next.taskDetails + "\n"
output += task.description + "\n\n"
output += t.commands.next.readyToStart + "\n"
output += `/planUpdate T${task.id} start\n\n`
output += "─".repeat(60) + "\n\n"
output += t.commands.next.alternatives + "\n\n"
output += alternatives.map((alt, i) =>
  `${i+1}. T${alt.id}: ${alt.name} - ${alt.complexity} - ${alt.estimated}`
).join("\n")
```

**Example output (English):**
```
🎯 Recommended Next Task

T1.2: Database Setup

Complexity: Medium
Estimated: 4 hours
Phase: 1 - Foundation

✅ All dependencies completed

🎯 Why this task?
• Unlocks 3 other tasks
• Critical for Phase 2 progress
• Good complexity balance after previous task

📝 Task Details:
Configure PostgreSQL database with connection pooling
and initial schema setup...

Ready to start?
/planUpdate T1.2 start

────────────────────────────────────────────────────────────

💡 Alternative Tasks (if this doesn't fit):

1. T1.3: Authentication Setup - High - 6 hours
2. T2.1: API Endpoints - Medium - 5 hours
```

**Example output (Georgian):**
```
🎯 რეკომენდებული შემდეგი ამოცანა

T1.2: მონაცემთა ბაზის დაყენება

სირთულე: საშუალო
შეფასებული: 4 საათი
ეტაპი: 1 - საფუძველი

✅ ყველა დამოკიდებულება დასრულდა

🎯 რატომ ეს ამოცანა?
• ხსნის 3 სხვა ამოცანას
• კრიტიკული მე-2 ეტაპის პროგრესისთვის
• კარგი სირთულის ბალანსი წინა ამოცანის შემდეგ

📝 ამოცანის დეტალები:
PostgreSQL-ის დაყენება connection pooling-ით
და საწყისი სქემის დაყენებით...

მზად ხართ დასაწყებად?
/planUpdate T1.2 start

────────────────────────────────────────────────────────────

💡 ალტერნატიული ამოცანები (თუ ეს არ გიხდებათ):

1. T1.3: ავთენტიფიკაციის დაყენება - მაღალი - 6 საათი
2. T2.1: API Endpoints - საშუალო - 5 საათი
```

**Instructions for Claude:**

Use translation keys for all output:
- Title: `t.commands.next.title`
- Recommended task: `t.commands.next.recommendedTask`
- Complexity: `t.commands.next.complexity` + `t.templates.complexity.{low/medium/high}`
- Estimated: `t.commands.next.estimated`
- Phase: `t.commands.next.phase`
- Dependencies: `t.commands.next.dependenciesCompleted`
- Why: `t.commands.next.whyThisTask`
- Details: `t.commands.next.taskDetails`
- Ready: `t.commands.next.readyToStart`
- Alternatives: `t.commands.next.alternatives`

### Step 7: Handle Special Cases

#### Case 1: No Available Tasks (All Blocked or Waiting)

**Pseudo-code:**
```javascript
let output = t.commands.next.noTasks + "\n\n"
output += t.commands.next.projectStatus + "\n"
output += t.commands.next.completed + " " + completedCount + "/" + totalCount + "\n"
output += t.commands.next.inProgress + " " + inProgressCount + "\n"
output += t.commands.next.blocked + " " + blockedCount + "\n"
output += t.commands.next.waitingOnDeps + " " + waitingCount + "\n\n"

if (inProgressTasks.length > 0) {
  output += t.commands.next.tasksInProgress + "\n"
  output += inProgressTasks.map(t => `   ${t.id}: ${t.name}`).join("\n") + "\n\n"
}

if (blockedTasks.length > 0) {
  output += t.commands.next.blockedTasks + "\n"
  output += blockedTasks.map(t => `   ${t.id}: ${t.name}`).join("\n") + "\n\n"
}

output += t.commands.next.suggestedActions + "\n"
output += "1. " + t.commands.next.completeInProgress + "\n"
output += "2. " + t.commands.next.resolveBlockers + "\n"
output += "3. " + t.commands.next.reviewDependencies
```

**Example output (English):**
```
⚠️ No tasks currently available to work on.

📊 Project Status:
✅ Completed: 5/18
🔄 In Progress: 2
🚫 Blocked: 1
⏳ Waiting on Dependencies: 10

🔄 Tasks In Progress:
   T1.2: Database Setup
   T1.3: Authentication

🚫 Blocked Tasks:
   T2.1: API Endpoints (waiting on design)

💡 Suggested Actions:
1. Complete in-progress tasks
2. Resolve blockers on blocked tasks
3. Review dependencies if tasks seem stuck
```

**Instructions for Claude:**

Use translation keys:
- `t.commands.next.noTasks`
- `t.commands.next.projectStatus`
- `t.commands.next.completed`
- `t.commands.next.inProgress`
- `t.commands.next.blocked`
- `t.commands.next.waitingOnDeps`
- `t.commands.next.tasksInProgress`
- `t.commands.next.blockedTasks`
- `t.commands.next.suggestedActions`
- `t.commands.next.completeInProgress`
- `t.commands.next.resolveBlockers`
- `t.commands.next.reviewDependencies`

#### Case 2: All Tasks Complete

**Pseudo-code:**
```javascript
let output = t.commands.next.allComplete + "\n\n"
output += t.commands.next.projectComplete + "\n\n"
output += t.commands.next.whatsNext + "\n"
output += t.commands.next.deploy + "\n"
output += t.commands.next.postMortem + "\n"
output += t.commands.next.gatherFeedback + "\n"
output += t.commands.next.planNextVersion + "\n"
output += t.commands.next.celebrate + "\n\n"
output += t.commands.next.greatWork
```

**Example output (English):**
```
🎉 Congratulations! All tasks are complete!

✅ Project: [PROJECT_NAME]
📊 Progress: 100%
🏆 [Total] tasks completed across [N] phases

Project Status: COMPLETE ✨

🎯 What's next?
   • Deploy to production (if not already)
   • Write post-mortem / lessons learned
   • Gather user feedback
   • Plan next version/features
   • Celebrate your success! 🎊

Great work on completing this project! 🚀
```

#### Case 3: Only High-Complexity Tasks Left

```
🎯 Recommended Next Task

╔══════════════════════════════════════════════════════════╗
║  T[X].[Y]: [Task Name]                                   ║
║  📊 Complexity: High ⚠️                                   ║
║  ⏱️  Estimated: [X] hours                                ║
╚══════════════════════════════════════════════════════════╝

⚠️ Note: This is a complex task. Consider:
   • Breaking it down into subtasks
   • Setting aside focused time
   • Getting help if needed
   • Taking breaks during implementation

[Rest of normal recommendation]
```

#### Case 4: Many In-Progress Tasks

If 3+ tasks are IN_PROGRESS:

```
⚠️ You have [N] tasks in progress.

💡 Tip: Consider finishing in-progress tasks before starting new ones:

🔄 In Progress:
   1. T[X].[Y]: [Name] ([Complexity])
   2. T[A].[B]: [Name] ([Complexity])
   3. T[C].[D]: [Name] ([Complexity])

Benefits of finishing first:
   • Clear sense of progress
   • Unlock dependent tasks
   • Maintain focus and momentum
   • Avoid context switching

────────────────────────────────────────────────────────────

Still want to start something new? Here's the recommendation:
[Normal recommendation follows]
```

### Step 8: Consider Context

Provide context-aware advice based on project state:

#### Early in Project (< 25% complete)
```
🌟 Early Stage Tips:
   • Focus on foundation tasks
   • Don't skip setup steps
   • Document as you go
   • Test early and often
```

#### Mid Project (25-75% complete)
```
🚀 Building Momentum:
   • You're making great progress!
   • Keep quality high
   • Watch for scope creep
   • Refactor if needed
```

#### Late Project (> 75% complete)
```
🏁 Final Sprint:
   • Almost there!
   • Don't rush quality
   • Test thoroughly
   • Update documentation
   • Plan deployment
```

## Reasoning Examples

### Example 1: Dependency Unlock

```
🎯 Why this task?
   • Unlocks 3 other tasks (T2.2, T2.3, T2.4)
   • Critical path item - other work depends on this
   • Completing this opens up parallel work opportunities
```

### Example 2: Complexity Balance

```
🎯 Why this task?
   • Medium complexity - good after completing complex T1.3
   • Prevents burnout with more manageable scope
   • Maintains momentum without overwhelming difficulty
```

### Example 3: Phase Progression

```
🎯 Why this task?
   • Last task in Phase 1 - completes foundation
   • Allows moving to Phase 2 (core features)
   • Natural progression point in project
```

### Example 4: Quick Win

```
🎯 Why this task?
   • Low complexity - quick win opportunity
   • Boosts progress percentage significantly
   • Good for maintaining motivation
   • Easy to fit into short work session
```

## Algorithms

### Finding Dependent Tasks

For a given task TX.Y, find tasks that list it in dependencies:

```
For each task T:
  If T.dependencies contains TX.Y:
    Add T to dependents list
```

Count these to determine "unlock value".

### Checking Dependency Satisfaction

For a task to be available, check each dependency:

```
For each dependency D in task.dependencies:
  Find task with ID = D
  If task.status != DONE:
    Return False (not satisfied)
Return True (all satisfied)
```

### Phase Detection

```
Extract phase number from task ID:
  T1.1 → Phase 1
  T2.3 → Phase 2
  T15.7 → Phase 15

Find current phase:
  For phase in [1, 2, 3, 4, ...]:
    If any task in phase is not DONE:
      Return phase
```

## Edge Cases

1. **Circular Dependencies**: Detect and warn user
   ```
   ⚠️ Warning: Circular dependency detected between T2.1 and T2.3
   Please review and fix the dependencies in PROJECT_PLAN.md
   ```

2. **Missing Dependencies**: Task references non-existent task
   ```
   ⚠️ Warning: Task T2.3 depends on T1.5, which doesn't exist
   Treating as satisfied for now.
   ```

3. **Empty Plan**: No tasks defined
   ```
   ⚠️ No tasks found in PROJECT_PLAN.md
   Please add tasks to the "Tasks & Implementation Plan" section.
   ```

## Output Formatting

Use visual elements for clarity:
- ✅ Checkmarks for completed items
- 🔄 In progress indicator
- 🚫 Blocked indicator
- 📊 Complexity indicator
- ⏱️ Time estimate
- 🎯 Goal/recommendation
- 💡 Tips and suggestions
- ⚠️ Warnings
- 🎉 Celebrations

Keep output scannable and actionable.

## Success Criteria

A good recommendation should:
- ✅ Consider all relevant factors (dependencies, phase, complexity)
- ✅ Provide clear reasoning
- ✅ Show task details
- ✅ Offer alternatives
- ✅ Give actionable next steps
- ✅ Be contextually aware
- ✅ Help maintain project momentum

## Implementation Notes

1. **Parse carefully**: Use regex or string matching to extract task details
2. **Handle variations**: Tasks may have slightly different formatting
3. **Be robust**: Don't fail on minor formatting issues
4. **Calculate accurately**: Ensure dependency logic is correct
5. **Explain well**: Users should understand WHY this task is recommended
6. **Stay positive**: Encourage users and maintain motivation

This command is about **intelligent guidance**, not just listing tasks!
