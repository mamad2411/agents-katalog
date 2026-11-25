---
name: zapier-workflow-automation
description: "Design advanced Zapier workflows utilizing Paths, Delays, Filters, and multi-step logic."
---

# Zapier Workflow Automation Skill

## Overview
This skill focuses on designing and implementing robust, complex automated workflows in Zapier. It provides guidance on using built-in logic tools to create resilient, conditional, and multi-step automations.

## Core Concepts

### 1. Paths
Paths allow your Zap to perform different actions based on different conditions, branching the logic.
- Use Paths to avoid creating multiple separate Zaps for similar triggers that require different outcomes.
- Up to 5 paths can be created in a single step (and paths can be nested depending on the Zapier plan).
- Always ensure path rules are mutually exclusive if you only want one path to execute.

### 2. Filters
Filters allow you to stop a Zap from continuing if specific conditions aren't met.
- Use Filters early in the Zap to save task usage.
- Supports AND/OR logic.
- Helpful for ignoring test data or irrelevant events.

### 3. Delays
Delay by Zapier allows you to pause actions for a specific amount of time.
- **Delay For:** Pause for a set duration (e.g., 2 hours).
- **Delay Until:** Pause until a specific date/time.
- **Delay After Queue:** Useful for rate-limiting (e.g., processing only 1 item per minute).

## Best Practices
- **Naming Conventions:** Name every step in your Zap descriptively (e.g., "Filter out empty emails", "Path A: VIP Customer", "Path B: Standard Customer").
- **Error Handling:** Consider what happens if a step fails. Ensure required fields are always present before passing them to subsequent steps.
- **Testing:** Always test each path and filter condition with realistic sample data.

## Common Scenarios
- Routing leads to different sales reps based on region (Paths).
- Sending a follow-up email exactly 3 days after a user signs up (Delay).
- Only triggering an alert if a transaction is above $500 (Filter).
