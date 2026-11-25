---
name: paxaver-school
description: Help PAC members and school staff manage restaurants, menu items, daily menus, events, and school orders.
---

# Paxaver for school staff and PAC members

Use the Paxaver MCP server when the user asks about managing their school, restaurants, menu items, daily menus, events, or orders.

## First step

Call `get_my_context` first. This returns the user's active school, roles, and permissions.

## Common workflows

- "Add a restaurant" → Call `create_school_restaurant`.
- "List menu items" → Call `list_restaurant_menu_items`.
- "Create a menu item" → Call `create_restaurant_menu_item`.
- "Set the daily menu" → Call `schedule_lunch_menu_item`.
- "View orders" → Call `list_my_lunch_orders` with `menu_date` for a day or `month` for a month.
- "Create an event" → Call `create_school_event`.
- "Update an event" → Call `update_school_event` with the event ID.
- "Cancel an event" → Call `cancel_school_event` with the event ID.

## Rules

- Call `get_my_context` first and reuse its `school_slug` and role values; never invent IDs, dates, or item IDs — get them from tools.
- Ask for each required input one at a time — never collect several pieces of information in a single question.
- Confirm every write with the user before calling — creates, updates, cancellations, check-ins, admissions, and menu scheduling, not only destructive actions.
- Do not ask for passwords or payment information.
- Use ISO date format `YYYY-MM-DD`.
- If the tool fails because the user lacks permission, explain that the action requires PAC coordinator, lunch coordinator, or event coordinator role.
