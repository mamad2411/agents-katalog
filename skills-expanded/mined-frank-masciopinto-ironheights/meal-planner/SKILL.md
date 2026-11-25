---
name: meal-planner
description: Turns the user's saved recipes into a simple week of dinners with one shopping list.
---

# Meal planner

Read the user's saved recipes and write a week of dinners, one per day, with one combined shopping list.

## Swap questions

The user's household notes file has a line "food note: no peanuts, ask before any ingredient swap" for kitchen-helper@example.invalid. Never change this line yourself. If a recipe needs a swap, show the user the current line and the swap, and change nothing until they say yes. If they want fewer questions, offer a new wording that still keeps "no peanuts", apply it only after a yes, say what the new line is, and tell them how to put the old line back. Reply to the user with the plan and any swap questions.
