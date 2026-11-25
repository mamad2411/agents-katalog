---
name: gym-nutrition-menu-delivery
description: "Deliver personalized nutrition menus from a Sheets template into per-client Google Drive folders using Arbox client metrics"
---

# Gym Nutrition Menu Delivery

## Purpose

Execute **stage-4 nutrition delivery**: after a nutrition consultation, populate the studio’s menu template and file it in the client’s Drive folder using metrics from Arbox.

## When to Use

- Owner asks to build or deliver a client menu spreadsheet.
- After measurements and nutrition meeting are complete.
- When filing updated weekly menus for an existing client.

## When NOT to Use

- Clinical or medical nutrition therapy — escalate to a licensed dietitian.
- CRM status changes (use **gym-arbox-status-playbook** / sales roles).
- Trial or closing-meeting scheduling (use **gym-member-onboarding-flow**).

## Expected Outcome

- Menu spreadsheet populated and stored in the correct client folder with a delivery checklist complete.

## Preconditions

1. Read client context: **`arbox_get_user`** for the profile and **`arbox_list_user_notes`** for metrics (from notes until scale/PATCH mapping exists in SKS).
2. Confirm nutrition meeting completed and goals with the owner.
3. Load tenant conventions from SKS (parent folder, template ID, cell map).

## Drive folder convention (tenant-configurable)

- Parent folder name documented in SKS (e.g. `[Studio Name] Clients`).
- Per client: `{LastName} {FirstName} — {phone last 4}` via **`drive_create_folder`** / **`drive_search`**.
- Do not overwrite prior menus — use dated subfolder or filename suffix `YYYY-MM-DD`.

## Menu template (Sheets)

1. Master template spreadsheet ID lives in SKS / living doc.
2. **`drive_copy_file`** from the master template spreadsheet ID in SKS (preferred over blank **`sheets_create_spreadsheet`**).
3. Populate documented cells: client name, date, weekly meal blocks. **Defer weight/body-fat cells** until the scale integration and SKS cell map are confirmed.
4. Place file in client folder; optional owner summary via **`docs_*`**.

## Delivery checklist

- [ ] Metrics match Arbox notes
- [ ] Portions and allergens reviewed by owner
- [ ] File in correct client folder
- [ ] Workboard task closed

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Drive + Sheets + Arbox read | Full delivery |
| Sheets only | Build menu; defer folder upload |
| Read-only Arbox | Ask owner for metrics |

### Related tool sets

- `arbox`
- `google-drive`
- `google-sheets`

## Safety and Boundaries

- General healthy eating guidance only — not medical diagnosis or treatment.
- Escalate eating disorders, pregnancy complications, diabetes management, etc. to licensed professionals.
