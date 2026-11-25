---
name: exploration
description: An open-ended pattern where agents autonomously conduct research, generate hypotheses, and explore solution spaces without a predefined path. Use when user asks to "add exploration to my agent", "balance exploration and exploitation", or mentions curiosity-driven, search strategies, or novelty seeking.
---

# Exploration & Discovery

In the Exploration pattern, the goal is not to execute a known task, but to *find* new information or solutions. Agents act as scientists or researchers: they formulate a hypothesis, test it (by searching, coding, or simulating), analyze the results, and iterate. This allows for genuine novelty and discovery.

## Use Cases

-   **Agent Laboratory**: A team of agents (Professor, Postdoc, Reviewer) writing a research paper.
-   **Creative Studio**: Agents collaborating to write a screenplay or design a game.
-   **Scenario Planning**: Simulating how a stock portfolio would perform under various economic conditions.

## Implementation Pattern

```python
def exploration_loop(topic):
    knowledge_base = []
    
    # Phase 1: Hypothesis Generation
    hypotheses = brainstorming_agent.run(f"Generate ideas about {topic}")
    
    for hypothesis in hypotheses:
        # Phase 2: Experiment / Research
        # Agent autonomously decides search queries or code to run
        evidence = researcher_agent.run(f"Test this hypothesis: {hypothesis}")
        
        # Phase 3: Analysis
        conclusion = analyst_agent.run(
            prompt="Does the evidence support the hypothesis?",
            input={"hypothesis": hypothesis, "evidence": evidence}
        )
        
        knowledge_base.append(conclusion)
        
    # Phase 4: Synthesis
    return writer_agent.run("Write a report based on these conclusions", input=knowledge_base)
```


## Examples

**Input**: "Survey the latest research on LLM memory architectures and identify the top 3 open problems."

**What the agent does**:
1. Generates 5 hypotheses about unsolved memory challenges
2. Searches arXiv for recent papers on each hypothesis
3. Cross-references citation counts to rank relevance
4. Synthesizes findings into a structured research brief

**Output**: A 2-page research brief with identified gaps and recommended next steps.

---

**Input**: "Explore competitor pricing pages and build a comparison matrix."

**Output**: A structured table comparing plans, features, and pricing across 8 competitors, with a gap analysis highlighting differentiation opportunities.


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Agent explores indefinitely | Missing stopping criteria | Set explicit iteration limit (`max_iterations=10`) and convergence condition |
| All hypotheses converge to same answer | Insufficient diversity in brainstorming | Add temperature variation or inject contrarian perspectives |
| Research results are outdated | Search tool returning cached content | Set a task-appropriate recency window and record publication and event dates |
| Agent loses track of prior findings | Context window exceeded | Use an external knowledge store; summarize findings at each iteration |
| Exploration produces no actionable output | No synthesis step | Always include a final `writer_agent` pass to consolidate findings |
