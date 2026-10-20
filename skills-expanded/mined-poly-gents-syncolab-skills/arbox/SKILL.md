---
name: arbox
description: Arbox public API for gym scheduling, members, and leads
---

# Arbox

1. Prefer the DEDICATED tools — each maps to one Arbox endpoint with pre-validated params so you never build raw API queries: **`arbox_get_schedule`** (classes), **`arbox_search_user`** / **`arbox_get_user`** (find people), **`arbox_list_leads`** / **`arbox_list_users`** (lists), **`arbox_list_statuses`** / **`arbox_list_sources`** / **`arbox_list_lost_reasons`** / **`arbox_list_locations`** / **`arbox_list_membership_types`** / **`arbox_list_task_types`** / **`arbox_list_staff_members`** (reference IDs), **`arbox_list_tasks`**, **`arbox_list_user_notes`**, **`arbox_list_user_memberships`**; writes: **`arbox_create_lead`**, **`arbox_update_lead_status`**, **`arbox_mark_lead_lost`**, **`arbox_create_user_note`**, **`arbox_create_task`**, **`arbox_complete_task`**, **`arbox_book_trial_class`**, **`arbox_cancel_booking`**.
2. Call **`arbox_verify_connection`** at most ONCE per session — any successful Arbox call already proves the connection.
3. Load reference catalogs (statuses, sources, locations, …) once per session and reuse the IDs; reads are cached server-side (reference ~30 min, schedule ~2 min, lists ~1 min).
4. **`arbox_public_get`** / **`arbox_public_post`** / **`arbox_public_patch`** are escape hatches ONLY for routes without a dedicated tool (e.g. `v3/reports/{reportName}`, `v3/message`, `v3/users/memberships`, `v3/customFields`). Query names are snake_case per Arbox OpenAPI.
5. List responses are truncated (a `truncated` flag and `total_items` are returned) — use `page`/`limit` params or filters instead of pulling everything.
6. Never paste API keys into chat. Treat member data as sensitive.
