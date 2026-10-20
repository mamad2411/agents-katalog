# DSA Coach - Deliberate Practice System

Your personal coding coach for mastering Data Structures and Algorithms through pattern-based repetition.

## Usage

`/dsa-coach <mode> [arguments]`

## Modes

### List Mode
**Command:** `/dsa-coach list`

Show all available batches with problem counts and patterns covered.

**What it does:**
- Lists all 5 batches with names
- Shows problem count per batch
- Displays patterns covered in each batch
- Shows which batch you're currently on
- Displays completion status

**When to use:** First time using the coach, or when you want to see what's available.

**Example output:**
```
Current Batch: Batch 1 (Foundation Patterns)

=== Available Batches ===

Batch 1: Foundation Patterns (15 problems) [CURRENT]
  Patterns: Hash Map, Two Pointers, Sliding Window, Stack, Binary Search, Linked List
  Progress: 8/15 completed (53%)

Batch 2: Trees and Graphs (11 problems)
  Patterns: Tree Traversal, DFS, BFS, Graph Algorithms
  Progress: 0/11 completed (0%)

Batch 3: Advanced Two Pointers & Sliding Window (5 problems)
Batch 4: Dynamic Programming Foundations (7 problems)
Batch 5: Backtracking & Recursion (5 problems)
```

### Setup Mode
**Command:** `/dsa-coach setup`

Initialize the practice directory structure and generate all problem files from your dsa-mastery-plan.md.

**What it does:**
- Creates directory structure in `dsa-practice/`
- Generates 43 problem files across 5 batches
- Initializes progress tracking and state files
- Sets up session history and variation directories

**When to use:** First time using the coach, or when resetting your practice environment.

### Practice Mode
**Command:** `/dsa-coach practice <batch> <problem-number>`

**Examples:**
- `/dsa-coach practice batch-1 1` - Practice Two Sum (problem #1 from Batch 1)
- `/dsa-coach practice batch-1 5` - Practice Valid Parentheses (problem #5)
- `/dsa-coach practice batch-2 3` - Practice problem #3 from Batch 2

**What it does:**
- Presents the problem statement
- Offers progressive hints (pattern → approach → pseudocode)
- You write solution in `dsa-practice/batches/<batch>/solutions/` directory
- Evaluates your code with 100-point rubric (correctness, complexity, quality, edge cases, explanation)
- Updates progress tracking and mastery levels
- Saves session notes

**When to use:** Learning problems, building understanding, improving solutions.

### Test Mode
**Command:** `/dsa-coach test <batch-list> [topics]`

**Examples:**
- `/dsa-coach test batch-1` - Test on random problems from Batch 1
- `/dsa-coach test batch-1,batch-2` - Test across multiple batches
- `/dsa-coach test batch-1 "hash-map,two-pointers"` - Test specific patterns from Batch 1
- `/dsa-coach test batch-1,batch-2 "all"` - Comprehensive test across Batch 1 and 2
- `/dsa-coach test all` - Test on random problems from ALL completed batches

**What it does:**
- Selects 3-5 problems based on topics (or random if not specified)
- Generates variations based on your mastery level (minor → moderate → significant)
- You solve variations with timer (self-reported)
- Evaluates each solution with detailed rubric
- Asks follow-up questions to test deep understanding
- Calculates overall score and provides verdict:
  - ≥85%: **Ready for next batch**
  - 75-84%: **Almost ready** (practice weak patterns)
  - 60-74%: **Need more practice**
  - <60%: **Review fundamentals**
- Identifies weak patterns and recommends specific problems to practice
- Tracks test history for trend analysis

**When to use:** After completing most problems in a batch, to assess readiness for the next level.

### Progress Mode
**Command:** `/dsa-coach progress [batch]`

**Examples:**
- `/dsa-coach progress batch-1` - Show Batch 1 progress
- `/dsa-coach progress` - Show current batch progress

**What it does:**
- Shows completion percentage (problems solved / total)
- Pattern breakdown (Hash Map: 3/3 ✓, Two Pointers: 2/3 ⚠)
- Mastery levels per problem (⭐⭐⭐⭐⭐ stars)
- Recent test results and verdicts
- Weak patterns identified
- Recommendations for next steps

**When to use:** Check progress, identify gaps, decide what to practice next.

## Philosophy

This coach follows the **Depth > Breadth** principle from your dsa-mastery-plan.md:
- Master 10-15 problems through repetition before moving on
- 6-phase learning: Initial Solve → Pattern Recognition → Speed Building → Variations → Teaching → Final Sprint
- Pattern-based learning: Recognize and apply fundamental patterns
- Deliberate practice with feedback

## Implementation

**For Claude:**
This command launches a specialized agent via the Skill tool. The complete workflow is defined in `.claude/agents/dsa-coach-agent.md`.

When invoked, load the agent definition and pass the mode + arguments to execute the appropriate workflow (setup/practice/test/progress).

**Practice Directory:**
All materials stored in `dsa-practice/` within this repo.

**Source:** Based on `dsa-practice/dsa-mastery-plan.md` (5 batches, 43 problems total).
