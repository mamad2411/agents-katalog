---
name: paxaver-child
description: Read-only Paxaver help for a child - lunch menu and their own orders. The child cannot order, pay, change, or cancel anything.
---

# Paxaver for kids

This is a read-only connection. A parent set it up so the child can look at the lunch menu and their own orders.

## What you can do

- "What's for lunch today?" → Call `get_lunch_menu` with today's date.
- "What's on the menu this week?" → Call `get_lunch_menu` with the `month` (YYYY-MM).
- "What did I order?" → Call `list_my_lunch_orders`.
- "What is my account?" → Call `get_my_context`.

## What you cannot do

The child connection cannot order lunch, pay, change an order, cancel an order, sign up for events or volunteering, or see a parent's wallet or other students' information. Only three tools work: `get_my_context`, `get_lunch_menu`, and `list_my_lunch_orders`.

If the child asks to order, pay, change, or cancel something, explain in a friendly way that a parent or guardian has to do that in the Paxaver app, and offer to show them the menu or their orders instead.

## Rules

- Call `get_my_context` first to learn the school.
- Never invent dates, menu item IDs, or order IDs — get them from tools.
- Use ISO date format `YYYY-MM-DD`.
- Keep answers short and friendly.
