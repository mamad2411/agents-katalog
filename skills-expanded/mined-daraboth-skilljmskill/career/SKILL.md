---
name: career
description: Developer career growth — technical interview prep (4-phase problem solving, LeetCode patterns), resume/portfolio improvement, behavioral questions, and planning career progression. Use when the user asks about interviews, coding challenges, resume review, portfolio projects, "how do I get better at X as a dev", or is preparing for a specific role. Tailored to software engineers, not general career coaching.
---

# Skill: Career

> **Purpose**: Prepare for interviews, improve your profile, and grow as a developer.

## When to Use
- Preparing for technical interviews
- Improving resume or portfolio
- Planning career growth
- Problem-solving practice

---

## Technical Interview Prep

### The 4-Phase Approach

**Phase 1: Understand the Problem (2-3 min)**
```
1. Read the problem twice
2. Identify: What's the input? What's the output?
3. Ask clarifying questions:
   - Edge cases? (empty input, null, very large)
   - Constraints? (time/space, input size)
   - Expected output format?
4. Write 2-3 test cases by hand
```

**Phase 2: Plan (3-5 min)**
```
1. Think of the brute force solution first
2. State its time/space complexity
3. Can you optimize? Think about:
   - Can a HashMap reduce lookup time?
   - Can sorting help?
   - Is there a pattern (sliding window, two pointers)?
4. Describe your approach before coding
```

**Phase 3: Code (15-20 min)**
```
1. Write clean, readable code
2. Use meaningful variable names
3. Handle edge cases
4. Talk through your logic as you write
```

**Phase 4: Verify (3-5 min)**
```
1. Trace through with your test cases
2. Check edge cases
3. State the time/space complexity
4. Mention possible improvements
```

---

### Common Problem Patterns

| Pattern | When to Use | Example |
|---------|------------|---------|
| HashMap | Need fast lookup | Two Sum, counting frequencies |
| Two Pointers | Sorted array, finding pairs | Pair sum, palindrome check |
| Sliding Window | Contiguous subarray/substring | Max sum subarray, longest substring |
| Stack | Matching/nesting | Valid parentheses, expression evaluation |
| BFS/DFS | Trees, graphs, grids | Shortest path, connected components |

### Example: Two Sum (JavaScript)
```javascript
function twoSum(nums, target) {
  const seen = new Map();
  
  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];
    
    if (seen.has(complement)) {
      return [seen.get(complement), i];
    }
    
    seen.set(nums[i], i);
  }
  
  return []; // No solution found
}

// Time: O(n), Space: O(n)
// Test: twoSum([2, 7, 11, 15], 9) → [0, 1]
```

---

## Problem-Solving Strategy

### When You're Stuck in an Interview
1. **Say it out loud**: "I'm thinking about using a HashMap here because..."
2. **Start with brute force**: It's better than silence
3. **Look for patterns**: Sort the input and see if it helps
4. **Think about similar problems**: "This reminds me of..."
5. **Ask for a hint**: Better than staring silently

### Practice Plan
| Week | Focus | Daily Goal |
|------|-------|-----------|
| 1-2 | Arrays & Strings | 1 easy problem |
| 3-4 | HashMaps & Sets | 1 easy/medium problem |
| 5-6 | Stacks & Queues | 1 medium problem |
| 7-8 | Trees & Graphs | 1 medium problem |
| 9-10 | Mixed review | 1 medium, timed (30 min) |

---

## Resume Improvement

### Project Descriptions (STAR Format)
```
❌ Bad:
"Built a task manager application"

✅ Good:
"Built a CLI task manager in Java that handles CRUD operations 
with file-based persistence, serving as a practical exercise 
in OOP design, error handling, and modular architecture"
```

### Formula
**[Action verb] + [what you built] + [technology] + [impact/learning]**

### Strong Action Verbs
`Built`, `Designed`, `Implemented`, `Optimized`, `Debugged`, `Refactored`, `Automated`, `Integrated`

### What to Include
- **Projects**: 2-3 solid projects with GitHub links
- **Skills**: Languages, tools, and concepts you can actually discuss
- **Impact**: Numbers if possible ("reduced load time by 40%")
- **Learning**: Show growth ("started with X, now building Y")

---

## Portfolio Projects (Build These)

### Tier 1: Foundation
1. **CLI Task Manager (Java)** — CRUD, file persistence, clean OOP
2. **REST API Client (JavaScript)** — Fetch data, display, handle errors
3. **Personal Website** — HTML/CSS/JS, responsive, deployed

### Tier 2: Intermediate
4. **URL Shortener (Java)** — HashMap-based, CLI, generates short codes
5. **Chat Log Analyzer (JavaScript)** — Parse files, find patterns, generate stats
6. **Budget Tracker (Java)** — Categories, monthly reports, file I/O

### Each Project Should Demonstrate
- Clean code with consistent style
- Error handling
- A README with setup instructions
- At least one design decision you can explain

---

## Behavioral Interview Prep

### Common Questions + Framework
```
Q: Tell me about a challenging bug you fixed.
A: (Situation) I was working on... 
   (Task) The app was crashing when...
   (Action) I used systematic debugging: reproduce, isolate, identify...
   (Result) Found the root cause was... Fixed it in 30 min. 
            Added input validation to prevent it in the future.
```

### Questions to Prepare
1. Tell me about a project you're proud of
2. Describe a time you disagreed with a teammate
3. How do you handle tight deadlines?
4. What's your biggest weakness? (Pick a real one you're working on)
5. Why do you want to work here? (Research the company)

---

## Best Practices
1. **Practice daily** — 1 problem per day for 30 days beats 30 problems in 1 day
2. **Explain as you code** — interviewers care about your thought process
3. **Build real projects** — portfolio > certificates
4. **Network actively** — communities, meetups, open source contributions
5. **Keep learning publicly** — write blog posts, share on GitHub

## Common Mistakes
| Mistake | Fix |
|---------|-----|
| Jumping to code without planning | Spend 5 min understanding + planning |
| Silent coding in interviews | Narrate your thinking process |
| Only listing technologies on resume | Show what you built and why it mattered |
| Grinding problems without understanding | Review solutions and understand patterns |
| Waiting until "ready" to apply | Apply now, learn during the process |
