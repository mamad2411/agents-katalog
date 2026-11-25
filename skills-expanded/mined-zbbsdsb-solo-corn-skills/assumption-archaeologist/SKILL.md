---
name: assumption-archaeologist
description: Uncovers, challenges, and validates hidden assumptions in ideas, plans, and decisions. Helps users excavate implicit beliefs, categorize them by risk and impact, design tests to validate them, build dashboards to track them, and stress-test them under various scenarios.
category: deep-thinking
version: 1.0.0
tags:
  - assumptions
  - validation
  - decision-making
  - risk-assessment
  - critical-thinking
  - hypothesis-testing
operations:
  - excavate
  - categorize
  - design-test
  - build-dashboard
  - stress-test
---

# Assumption Archaeologist Skill

## Overview

The Assumption Archaeologist is a systematic framework for uncovering, challenging, and validating the hidden assumptions that underpin every idea, plan, and decision. Like an archaeologist carefully sifting through layers of earth to reveal ancient artifacts, this skill helps users dig beneath the surface to find the implicit beliefs that shape their thinking.

**Core Philosophy**: Every decision rests on assumptions. The quality of your decisions depends on the validity of those assumptions.

This skill provides a structured approach to:
- **Excavate** hidden assumptions from any context
- **Categorize** them by risk, impact, and confidence
- **Design tests** to validate or invalidate them
- **Build dashboards** to track assumption status over time
- **Stress-test** assumptions under extreme scenarios

## Why Assumptions Matter

Assumptions are the unstated beliefs we take for granted. They're like the invisible foundation of a building—if they're weak, the entire structure can collapse.

### Common Sources of Hidden Assumptions
- "This is how it's always been done"
- "Everyone knows that..."
- "Our users will love it because we love it"
- "The market will grow at X%"
- "Our competitors won't respond"
- "Technology will work as expected"

### The Cost of Unvalidated Assumptions
- Wasted resources building features no one wants
- Missed market opportunities
- Failed product launches
- Strategic blind spots
- Avoidable risks

## Core Operations

### 1. Excavate
Dig beneath the surface to uncover implicit assumptions.

**How it works**:
- Analyze statements, plans, and decisions for unstated premises
- Ask "What must be true for this to work?"
- Identify causal chains and dependency relationships
- Surface both explicit and implicit beliefs

**Key Questions**:
- What are we taking for granted here?
- What would have to be true for this to succeed?
- What are we assuming about users, market, technology, or competitors?
- What dependencies are we not mentioning?

### 2. Categorize
Organize assumptions by their characteristics and importance.

**Categorization Dimensions**:
- **Impact**: How much would it matter if this assumption is wrong?
  - High (catastrophic failure)
  - Medium (significant setback)
  - Low (minor inconvenience)
- **Risk**: How likely is this assumption to be wrong?
  - High (very uncertain)
  - Medium (some uncertainty)
  - Low (well-supported)
- **Confidence**: How confident are we in this assumption?
  - 0-25% (wild guess)
  - 26-50% (educated guess)
  - 51-75% (reasonable confidence)
  - 76-100% (near certainty)
- **Type**: What kind of assumption is it?
  - User assumptions (behavior, needs, preferences)
  - Market assumptions (size, growth, trends)
  - Technical assumptions (feasibility, performance, scalability)
  - Business assumptions (unit economics, revenue, costs)
  - Competitive assumptions (rival behavior, barriers)

### 3. Design Test
Create experiments to validate or invalidate assumptions.

**Test Design Principles**:
- **Falsifiability**: Can we prove it wrong?
- **Speed**: How quickly can we get an answer?
- **Cost**: How much will it cost to test?
- **Reliability**: How confident can we be in the result?

**Test Types**:
- **User Research**: Interviews, surveys, usability tests
- **MVP Experiments**: Minimal viable product tests
- **Market Tests**: Landing pages, pre-orders, crowdfunding
- **Technical Spikes**: Proof-of-concept implementations
- **Competitor Analysis**: Benchmarking and research

### 4. Build Dashboard
Create a tracking system for assumptions and their status.

**Dashboard Components**:
- Assumption inventory with categorization
- Test plans and schedules
- Results and status updates
- Risk indicators and alerts
- Decision points and triggers

**Tracking Metrics**:
- Number of assumptions validated/invalidated
- Confidence level changes over time
- Test coverage (what % of critical assumptions tested)
- Impact of wrong assumptions (lessons learned)

### 5. Stress Test
Challenge assumptions under extreme or adversarial conditions.

**Stress Test Scenarios**:
- **Best Case**: Everything goes perfectly—does this still hold?
- **Worst Case**: Everything that can go wrong does—how does this fail?
- **Black Swan**: Unlikely but high-impact events
- **Competitor Response**: What if competitors react aggressively?
- **Market Shifts**: Sudden changes in market conditions
- **Technology Failure**: Key tech components break

**Stress Test Questions**:
- What would break this assumption?
- How would we know if it's failing?
- What's our contingency if it's wrong?
- How would we recover?

## Architecture

```
assumption-archaeologist/
├── SKILL.md                    # This file - skill overview and index
└── references/
    ├── excavation/             # Techniques for uncovering assumptions
    ├── categorization/         # Frameworks for organizing assumptions
    ├── testing/                # Test design and execution guides
    ├── dashboards/             # Tracking and visualization templates
    ├── stress-testing/         # Scenario planning frameworks
    └── templates/              # Worksheets and checklists
```

## Quick Start

### Step-by-Step Workflow

1. **Start with a Decision or Plan**
   - Pick something you're working on: a product idea, strategy, project plan
   - Write down the core statement or goal

2. **Excavate Assumptions**
   - Ask "What must be true for this to work?"
   - Keep asking "Why?" and "What else?" until you can't think of more
   - Don't judge yet—just capture everything

3. **Categorize and Prioritize**
   - Score each assumption on impact and risk
   - Focus on high-impact, high-risk assumptions first
   - Group similar assumptions together

4. **Design Validation Tests**
   - For each critical assumption: "How can we test this quickly and cheaply?"
   - Start with the riskiest, highest-impact assumptions
   - Design tests that can falsify, not just confirm

5. **Build Your Dashboard**
   - Track assumptions, tests, and results
   - Update confidence levels as you learn
   - Set triggers for when to revisit assumptions

6. **Stress Test the Plan**
   - Challenge assumptions under extreme scenarios
   - Prepare contingencies for critical failures
   - Document what you'd do differently

## Usage Patterns

### Pattern 1: Pre-Launch Validation
Before launching a product or feature:
- Excavate all key assumptions
- Prioritize by impact and risk
- Test the most critical ones first
- Adjust plan based on findings

### Pattern 2: Strategic Planning
When developing strategy:
- Surface implicit strategic assumptions
- Categorize by strategic importance
- Stress test under various futures
- Build contingency plans

### Pattern 3: Post-Mortem Analysis
After a failure or setback:
- Identify which assumptions failed
- Analyze why they weren't detected earlier
- Update your assumption inventory
- Improve your excavation process

### Pattern 4: Ongoing Tracking
For long-term projects:
- Maintain a living assumption dashboard
- Regularly review and retest assumptions
- Update confidence levels as new data comes in
- Trigger decisions when confidence crosses thresholds

## Integration with Other Skills

This skill works synergistically with:

**Landing Skill**
- Excavate assumptions before committing to a direction
- Test assumptions early in the ideation process
- Use stress testing to prepare for execution risks

**Product Builder Skill**
- Validate assumptions before building
- Test product assumptions with MVPs
- Track assumption validity throughout development

**Principle Skill**
- Use questioning to excavate deeper assumptions
- Challenge assumptions through Socratic dialogue
- Extract principles from assumption failures

**Mental Models Skill**
- Apply first principles to uncover foundational assumptions
- Use inversion to stress test from failure perspective
- Combine models for multi-angle assumption analysis

## Examples

### Example 1: Product Idea Excavation

**Idea**: "We should build a subscription meal kit service for busy professionals"

**Excavated Assumptions**:
- Busy professionals want meal kits rather than takeout
- They're willing to pay $X per meal
- They have time to cook 30-minute meals
- They'll order consistently (not just once)
- We can source ingredients at scale affordably
- Delivery logistics are feasible in our target area
- Competitors won't capture the market first

**Categorization**:
- High Impact: "They'll order consistently" (retention is existential)
- High Risk: "They have time to cook" (busy professionals may not)
- Medium Impact: "We can source affordably" (affects profitability)
- Low Risk: "Delivery logistics feasible" (other companies do it)

**Test Design**:
- Landing page with pre-orders (tests interest and willingness to pay)
- Survey about cooking time availability
- Small-scale delivery test in one neighborhood

### Example 2: Stress Testing a Business Model

**Business Model**: "We'll offer free software and monetize via enterprise sales"

**Stress Test Scenarios**:
- **Worst Case**: Enterprises don't see value in paid features
- **Black Swan**: A major competitor open-sources a similar product
- **Market Shift**: Companies stop spending on enterprise software
- **Competitor Response**: Competitors cut enterprise prices 50%

**Contingencies**:
- Alternative monetization: Usage-based pricing
- Partnership strategy: Integrate with existing enterprise tools
- Cost optimization: Maintain low burn rate

## Best Practices

1. **Be Exhaustive**: When excavating, capture everything—you can prioritize later
2. **Prioritize Ruthlessly**: Focus on high-impact, high-risk assumptions first
3. **Design for Falsification**: The best tests can prove assumptions wrong
4. **Test Early, Test Cheap**: Don't wait—validate assumptions as soon as possible
5. **Update Continuously**: Assumptions change as you learn; keep your dashboard current
6. **Document Everything**: Track what you learned from wrong assumptions
7. **Embrace Being Wrong**: Invalidating an assumption early saves you from bigger problems later

## Common Pitfalls to Avoid

- **Confirmation Bias**: Only looking for evidence that confirms assumptions
- **Analysis Paralysis**: Over-categorizing without taking action
- **Testing the Wrong Things**: Focusing on easy-to-test but low-impact assumptions
- **Set It and Forget It**: Not revisiting assumptions as circumstances change
- **Underestimating Impact**: Being optimistic about how bad it would be if wrong

## Maintenance

This skill is designed to evolve:
- **Excavation techniques**: Updated with new questioning frameworks
- **Categorization systems**: Refined based on what works in practice
- **Test patterns**: Expanded with new validation methods
- **Dashboard templates**: Enhanced with better visualization and tracking
- **Stress scenarios**: Updated with emerging risks and market shifts

---

*The most dangerous assumptions are the ones you don't know you're making.*
