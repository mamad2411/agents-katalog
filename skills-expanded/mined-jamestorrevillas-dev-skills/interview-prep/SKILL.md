---
name: interview-prep
description: Use this skill when preparing for technical interviews, system design interviews, behavioral interviews, or mock interview practice. Trigger on keywords: interview, interview prep, mock interview, LeetCode, system design interview, behavioral question, STAR method, interview practice, job interview, coding interview.
---

# Interview Preparation

## Interview Types & What They Test

| Type | What They're Testing | How to Prepare |
|---|---|---|
| Coding / DSA | Problem-solving, CS fundamentals | LeetCode patterns, not random problems |
| System Design | Architecture thinking, trade-offs | Practice frameworks, read real systems |
| Behavioral | Past behavior predicts future | STAR stories for 6-8 scenarios |
| Technical Discussion | Depth of knowledge, communication | Know your stack deeply, read vs write trade-offs |

---

## Coding Interview: Pattern-First Approach

Don't grind random problems. Learn patterns:

| Pattern | When to Use |
|---|---|
| Two Pointers | Sorted arrays, palindromes, pair sums |
| Sliding Window | Subarray problems, longest/shortest window |
| Fast & Slow Pointers | Cycle detection, linked list middle |
| BFS / DFS | Trees, graphs, shortest path |
| Binary Search | Sorted data, "find in X" problems |
| Dynamic Programming | Overlapping subproblems, optimization |
| Heap / Priority Queue | K largest/smallest, streaming data |

### Problem-Solving Template
```
1. Clarify: "Can I have duplicates? What's the input range? What to return if empty?"
2. Example: Walk through a small example out loud
3. Brute force: State the naive solution first
4. Optimize: "I can improve this by..."
5. Code: Write clean, named code
6. Test: Trace through your example + edge cases
7. Complexity: State time and space complexity
```

---

## System Design Interview Framework

```
1. Clarify requirements (2-3 min)
   - Functional: What does it do?
   - Scale: Users, requests/sec, data volume
   - Non-functional: Latency, availability, consistency

2. Estimate scale (2 min)
   - Back-of-envelope: storage, throughput, bandwidth

3. High-level design (5-10 min)
   - Draw main components and their relationships
   - Define the API

4. Deep dive (10-15 min)
   - Zoom into the hardest part
   - Address bottlenecks proactively

5. Bottlenecks & trade-offs (5 min)
   - What would fail at scale?
   - What did you consciously trade off?
```

---

## Behavioral Interview: STAR Method

```
Situation: Set the scene (1-2 sentences)
Task:      What was your responsibility?
Action:    What did YOU specifically do? (most important part)
Result:    What was the outcome? Quantify if possible.
```

### Prepare Stories for These Scenarios
1. Technical challenge you solved
2. Conflict with a teammate — how you handled it
3. Time you failed and what you learned
4. When you had to learn something quickly
5. A project you're most proud of
6. When you disagreed with a decision but executed anyway
7. When you went beyond your role to help the team

### Anti-Patterns
- Using "we" when you should say "I" — be specific about YOUR contribution
- Vague results — quantify: "reduced load time by 40%", "unblocked 3 teammates"
- No reflection — always include what you learned

---

## Using AI for Interview Prep

```
"Act as a technical interviewer for a [senior/mid] 
[frontend/backend/full-stack] developer role.

Ask me coding/system design/behavioral questions.
After each answer:
- Tell me what I did well
- Tell me what a stronger answer would include
- Rate my answer: Strong / Adequate / Needs Work

Start with a medium difficulty question."
```

---

## The Day-Of Checklist
- [ ] Good sleep the night before (cognitive performance > cramming)
- [ ] Clarify before coding — interviewers value communication
- [ ] Think out loud — they want to see your process
- [ ] It's okay to pause and think — silence is better than wrong
- [ ] Ask for hints if truly stuck — it shows self-awareness
- [ ] End with questions — shows genuine interest
