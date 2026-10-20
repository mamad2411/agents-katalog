---
name: arbox-studio-operations
description: Run gym operations against live Arbox data: leads, schedule, memberships
---

# Arbox studio operations

- **Classes / schedule**: **`arbox_get_schedule`** with `from_date` and `to_date` (`YYYY-MM-DD`); optional `location_id`, `box_category_id`, `staff_id`.
- **Find one person**: **`arbox_search_user`** (`type` = phone | email | name, plus `value`) — ALWAYS before creating a lead; then **`arbox_get_user`** for the full profile.
- **Leads**: **`arbox_list_leads`** (open), **`arbox_list_converted_leads`**, **`arbox_list_lost_leads`**. **Members**: **`arbox_list_users`**, **`arbox_list_user_memberships`**, **`arbox_list_user_notes`**.
- **Tasks**: **`arbox_list_tasks`** (`from_date`/`to_date` required), **`arbox_create_task`**, **`arbox_complete_task`**.
- **Writes** (need human confirmation): **`arbox_create_lead`**, **`arbox_update_lead_status`**, **`arbox_mark_lead_lost`**, **`arbox_create_user_note`**, **`arbox_book_trial_class`**, **`arbox_cancel_booking`**.
- Rare routes without a dedicated tool: **`arbox_public_get`** / **`arbox_public_post`** per Arbox OpenAPI.
- If Arbox is not connected, say so and point to Integrations.
