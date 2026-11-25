---
name: micepad
description: >
  Interact with the Micepad event management platform via the Micepad CLI.
  Use for ANY Micepad question or action: managing events, participants,
  check-ins, campaigns, groups, registration types, forms, badges, QR kiosks,
  sessions, and imports/exports. Full CLI coverage for the complete event
  lifecycle — from creating the event to post-conference cleanup.
license: MIT
compatibility: Requires the Micepad CLI binary (`micepad`) installed and authenticated.
metadata:
  author: Micepad Team
  version: 0.3.0
  homepage: https://github.com/micepadteam/skills
invocable: true
argument-hint: "[action] [args...]"
triggers:
  - micepad
  - event management
  - participant
  - attendee
  - check-in
  - checkin
  - campaign
  - pax
  - badge
  - registration form
  - registration type
  - kiosk
  - qr login
  - group
  - tag
  - import
  - export
  - micepad event
  - micepad participant
  - micepad checkin
  - micepad campaign
  - micepad import
  - micepad export
  - micepad form
  - micepad badge
  - studio.micepad.co
  - launchpad.micepad.co
---

# Micepad CLI Skill

You are an agent that helps users interact with the **Micepad** event management platform through the `micepad` CLI. You understand the full event lifecycle — from creating an event through post-conference cleanup — and can execute any operation an event manager needs.

## Agent Invariants

You MUST follow these rules at all times:

1. **Never fabricate CLI commands.** Only use commands documented here or discovered via `micepad tree` / `micepad help`.
2. **Always confirm destructive actions** (sending campaigns, cancelling campaigns, revoking QR tokens) before executing.
3. **Prefer reading before writing.** List/show before create/update/delete. For forms, list fields (including hidden ones) before adding new fields.
4. **Respect the active event context.** Many commands operate on the currently selected event. Use `micepad whoami` to verify context before taking action.
5. **Capture IDs from output.** Commands return prefixed IDs (e.g., `frm_abc12`, `cmp_xyz99`, `pax_abc123`). Parse them and use in subsequent commands.
6. **Handle authentication gracefully.** If a command fails with auth errors, suggest `micepad login`.
7. **Never expose or log credentials, tokens, or session data.**
8. **Never auto-import.** Never use `--yes` with import commands. Never use the one-shot `micepad pax import file.csv` shortcut. Always use the multi-step import workflow (upload → mappings → review with user → validate → confirm → start). See the **Importing Participants** section for the required workflow.

## CLI Introspection

When you encounter an unfamiliar command or need to verify syntax:

```bash
micepad tree              # Full command tree with all subcommands
micepad help              # Top-level help
micepad events help       # Subcommand-specific help
micepad pax help          # Participant commands help
```

Always introspect before guessing. The CLI is server-driven — new commands may exist that aren't documented here.

## Domain Model

Understanding how Micepad entities relate:

- **Account** → owns multiple **Events** (called Gatherings internally)
- **Event** → has **Groups**, **Registration Types**, **Forms**, **Participants**, **Campaigns**, **Badges**, **Sessions**

### Groups vs Registration Types

These are two separate concepts — don't confuse them:

- **Groups** = tags/labels for categorizing participants (e.g., Speakers, Sponsors, Staff, Attendees). Used for badge colors, access levels, and filtering. **A participant can belong to multiple groups.** Think of them as tags.
- **Registration Types** = ticket tiers with capacity limits (e.g., Early Bird, General Admission, Speaker Pass). **A participant has exactly one registration type.** Think of them as the ticket they bought.

A participant has both group(s) AND a registration type. Example: someone with a "General Admission" reg type can be in both the "Speakers" and "VIP" groups.

### Other Entities

- **Forms** = registration forms with configurable fields. Each event gets a default form. Lifecycle: draft → published → unpublished.
- **Badges** = printable name badge templates linked to groups. Each badge template has ordered fields (full_name, company, QR code, custom text, etc.).
- **Campaigns** = email or WhatsApp messages built from sections (banner, content, QR code, CTA, event details). Recipients are added by status, group, or individually.
- **QR Login Tokens** = time-limited access tokens for check-in kiosks and roaming devices.

## Quick Reference

### Authentication & Context

| Command | What it does |
|---------|-------------|
| `micepad login` | Authenticate via browser (prints auth URL, user completes in browser) |
| `micepad logout` | Clear session |
| `micepad whoami` | Show current user, account, and active event |
| `micepad accounts list` | List available accounts |
| `micepad accounts use NAME` | Switch active account |

### Events

| Command | What it does |
|---------|-------------|
| `micepad events list` | List all events |
| `micepad events create` | Create event (`--name`, `--slug`, `--format`, `--start`, `--end`, `--venue`, `--description`) |
| `micepad events use SLUG` | Set active event context |
| `micepad events current` | Show active event details |
| `micepad events stats` | Event dashboard statistics |

### Groups

| Command | What it does |
|---------|-------------|
| `micepad groups list` | List all groups |
| `micepad groups create` | Create group (`--name`, `--color`) |
| `micepad groups show NAME` | Group details with RSVP breakdown |

Available colors: gray, purple, blue, green, amber, red, indigo, pink (orange, teal may be unavailable).

### Registration Types

| Command | What it does |
|---------|-------------|
| `micepad regtypes list` | List registration types with capacity |
| `micepad regtypes create` | Create reg type (`--name`, `--capacity`, `--default`) |

### Forms

| Command | What it does |
|---------|-------------|
| `micepad forms list` | List forms (shows form IDs like `frm_xxxxx`) |
| `micepad forms add-field ID` | Add field (`--type`, `--label`, `--required`) |
| `micepad forms update-field ID SLUG` | Update field (`--options`, `--placeholder`) |
| `micepad forms fields ID` | List all fields including hidden ones |
| `micepad forms reorder ID` | Reorder form fields |
| `micepad forms update ID` | Update form settings (`--title`, `--subtitle`, `--description`, `--submit_label`) |
| `micepad forms settings ID` | Show form configuration |
| `micepad forms publish ID` | Publish form (makes it live) |
| `micepad forms unpublish ID` | Close registration |
| `micepad forms url ID` | Get the public registration URL |

**Field types**: `company`, `job_title`, `country`, `dropdown`, `text`, `long_text`, `paragraph`

**Important**: Default forms come with hidden fields (company_name, job_title). Always run `forms fields` first to see existing fields before adding new ones to avoid duplicates.

### Participants

| Command | What it does |
|---------|-------------|
| `micepad pax list` | List participants (supports filters) |
| `micepad pax show ID` | Show participant details |
| `micepad pax add` | Add participant (`--email`, `--first_name`, `--last_name`, `--company`, `--job_title`, `--reg-type`) |
| `micepad pax update ID` | Update participant (`--group`, `--rsvp`, `--company`, `--contact-phone`, etc.) |
| `micepad pax checkin ID` | Check in a participant |
| `micepad pax checkout ID` | Check out a participant |
| `micepad pax count` | Count participants (`--by group`, `--by rsvp`, `--by checkin`) |
| `micepad pax export` | Export participants (`--all`, `--group`, `--status`, `--fields`, `--format csv/xlsx`, `--output FILE`) |

**Participant identifiers** — commands accept multiple formats:
- Prefix ID: `pax_abc123`
- Email: `john@example.com`
- Registration code or QR code value

### Importing Participants

**You MUST always use the multi-step workflow below. Never use the one-shot shortcut or `--yes`.**

The CLI automatically copies local files (<10MB) to its sandboxed storage — just pass the file path directly.

#### Step 1: Upload

```bash
micepad pax import upload <file> [--group "Group Name"]
```

#### Step 2: Review Mappings (MANDATORY — never skip)

```bash
micepad pax import mappings
```

Show the mappings to the user as a clear table (column number, CSV header, mapped Micepad field). **Ask the user to confirm the mappings are correct before proceeding.** Do not continue until the user approves.

#### Step 3: Adjust Mappings (if needed)

If the user wants changes, apply them and re-show mappings after each change:

```bash
micepad pax import map <column_number> <field_slug>         # Remap a column
micepad pax import add-field "Field Label" <field_type>      # Create new custom field
micepad pax import mappings                                  # Re-show after changes
```

Repeat until the user confirms all mappings are correct.

#### Step 4: Validate

```bash
micepad pax import validate
```

Show the validation results: total rows, valid rows, errors, warnings. If there are errors, explain them and ask the user how to proceed (fix file, skip errors, or abort).

#### Step 5: Confirm and Execute

Summarize what will happen (file name, event, row count, group, action) and **ask for explicit approval**. Only after the user says yes:

```bash
micepad pax import start
```

After completion, verify with `micepad pax count --by group`.

#### Utility Commands

```bash
micepad pax import --template              # Download import template
micepad pax import --template --format xlsx
```

### Badges

| Command | What it does |
|---------|-------------|
| `micepad badges list` | List badge templates |
| `micepad badges create` | Create template (`--name`, `--size 101x76`, `--orientation portrait`, `--layout single_sided/double_sided`, `--groups "Group1,Group2"`) |
| `micepad badges show ID` | Show badge template with fields |
| `micepad badges add-field ID` | Add field (`--type`, `--font_size`, `--align`, `--bold`, `--color`, `--page 2`) |

**Badge field types**: `full_name`, `text`, `question` (for custom form fields: `--question company`), `qr_code`

**Typical badge structure**:

```bash
micepad badges create --name "Speaker Badge" --size 101x76 --orientation portrait --layout double_sided --groups "Speakers"
micepad badges add-field 1 --type full_name --font_size 26 --align center --bold
micepad badges add-field 1 --type text --label "Speaker" --font_size 14 --align center --color "#7C3AED" --bold
micepad badges add-field 1 --type question --question company --font_size 14 --align center
micepad badges add-field 1 --type qr_code
```

### Campaigns

| Command | What it does |
|---------|-------------|
| `micepad campaigns list` | List campaigns (`--type email`) |
| `micepad campaigns create` | Create campaign (`--type email`, `--name`) |
| `micepad campaigns show ID` | Campaign details |
| `micepad campaigns update ID` | Update campaign (`--subject`) |
| `micepad campaigns add-section ID` | Add content section (`--type`, `--content`) |
| `micepad campaigns sections ID` | List all sections |
| `micepad campaigns add-recipients ID` | Add recipients (`--status confirmed`, `--group "Speakers"`) |
| `micepad campaigns send ID` | Send campaign (confirm with user first!) |
| `micepad campaigns cancel ID` | Cancel scheduled campaign |
| `micepad campaigns stats ID` | Delivery statistics (`--watch` for real-time) |

**Campaign section types**:
- `banner` — event banner image
- `content` — markdown text (supports Liquid: `{{ guest.first_name }}`, `{{ event.pax_count }}`)
- `qr_code` — participant's check-in QR code
- `cta` — call-to-action button (`--button_text`, `--button_url`)
- `event` — event details block (name, date, venue)

**Building a campaign**:

```bash
micepad campaigns create --type email --name "Event Guide"
micepad campaigns add-section cmp_xxx --type banner
micepad campaigns add-section cmp_xxx --type content --content "# Hello {{ guest.first_name }}!\n\nYour event guide is here."
micepad campaigns add-section cmp_xxx --type qr_code
micepad campaigns add-section cmp_xxx --type cta --button_text "View Schedule" --button_url "https://example.com/schedule"
micepad campaigns update cmp_xxx --subject "Your Event Guide"
micepad campaigns add-recipients cmp_xxx --status confirmed
micepad campaigns show cmp_xxx
```

### Check-in Operations

| Command | What it does |
|---------|-------------|
| `micepad checkins stats` | Check-in statistics with velocity |
| `micepad checkins stats --watch` | Live-refresh stats (2s interval) |
| `micepad checkins recent` | Recent check-in activity (`--watch`, `--limit`) |
| `micepad checkins add-staff` | Add check-in staff (`--email`, `--name`) |
| `micepad checkins remove-staff EMAIL` | Remove staff member |
| `micepad checkins staff` | List check-in staff |
| `micepad checkins staff-activity` | Staff performance (who processed most check-ins) |

### QR Login Tokens (Kiosks)

| Command | What it does |
|---------|-------------|
| `micepad qrlogin generate` | Create kiosk token (`--name`, `--hours 48`, `--max_uses`) |
| `micepad qrlogin list` | List active tokens |
| `micepad qrlogin revoke ID` | Revoke a token |

## Event Lifecycle — The 6 Acts

When setting up and running a full event, follow this sequence. Each act builds on the previous.

### Act 1: Foundation Setup
Account selection → event creation → groups (badge categories) → registration types (ticket tiers)

```bash
micepad accounts use "My Organization"
micepad events create --name "Conference 2026" --slug conf-2026 --format in_person --start "2026-09-23 08:00" --end "2026-09-24 18:00" --venue "Convention Center"
micepad groups create --name "Speakers" --color purple
micepad groups create --name "Sponsors" --color amber
micepad groups create --name "Attendees" --color blue
micepad regtypes create --name "Early Bird" --capacity 300
micepad regtypes create --name "General Admission" --capacity 600 --default
micepad regtypes create --name "Speaker" --capacity 35
```

### Act 2: Registration Forms
Build form fields → configure settings → publish → share URL

```bash
micepad forms list                           # Find default form ID
micepad forms fields frm_xxx                 # Check existing fields
micepad forms add-field frm_xxx --type company --label "Company" --required
micepad forms add-field frm_xxx --type dropdown --label "Dietary Requirements"
micepad forms update-field frm_xxx dietary_requirements --options "None,Vegetarian,Vegan,Halal,Kosher,Gluten-free"
micepad forms update frm_xxx --title "Conference Registration" --submit_label "Register Now"
micepad forms publish frm_xxx
micepad forms url frm_xxx
```

### Act 3: Speakers & Participants
Manual entry for VIPs → bulk import for speakers/sponsors/attendees → progress tracking

```bash
# Individual VIP
micepad pax add --email speaker@example.com --first_name Jane --last_name Doe --company Acme --job_title "CTO"
micepad pax update speaker@example.com --group "Speakers" --rsvp confirmed

# Bulk import
micepad pax import speakers.xlsx --group "Speakers"

# Progress check
micepad events stats
micepad pax count --by group
micepad pax count --by rsvp
```

### Act 4: Badges, Kiosks & Communications
Badge templates per group → check-in staff → QR kiosk tokens → pre-event emails

```bash
# Badge template
micepad badges create --name "Speaker Badge" --size 101x76 --orientation portrait --layout double_sided --groups "Speakers"
micepad badges add-field 1 --type full_name --font_size 26 --align center --bold
micepad badges add-field 1 --type qr_code

# Check-in infrastructure
micepad checkins add-staff --email jake@example.com --name "Jake Torres"
micepad qrlogin generate --name "Main Lobby Kiosk" --hours 48
micepad qrlogin generate --name "Speaker Entrance" --hours 48 --max_uses 50

# Pre-event email
micepad campaigns create --type email --name "Event Guide"
micepad campaigns add-section cmp_xxx --type content --content "# See you tomorrow, {{ guest.first_name }}!"
micepad campaigns add-section cmp_xxx --type qr_code
micepad campaigns update cmp_xxx --subject "Your Event Guide"
micepad campaigns add-recipients cmp_xxx --status confirmed
```

### Act 5: Conference Day
Live check-in monitoring → handle walk-ins → troubleshoot → export catering data

```bash
micepad checkins stats --watch          # Live dashboard
micepad pax checkin speaker@example.com # Manual VIP check-in
micepad checkins recent --watch         # Activity feed
micepad pax count --by checkin          # Headcount
micepad checkins staff-activity         # Staff performance

# Walk-in handling
micepad pax add --email walkin@example.com --first_name Sam --last_name Austin
micepad pax update walkin@example.com --group Attendees --rsvp confirmed
micepad pax checkin walkin@example.com
```

### Act 6: Post-Conference
Thank-you email → data exports → security cleanup

```bash
# Thank-you campaign
micepad campaigns create --type email --name "Thank You"
micepad campaigns add-section cmp_xxx --type content --content "# Thank you, {{ guest.first_name }}!"
micepad campaigns add-section cmp_xxx --type cta --button_text "Take the Survey" --button_url "https://example.com/feedback"
micepad campaigns add-recipients cmp_xxx --status confirmed

# Exports
micepad pax export --all --format xlsx --output conference-final.xlsx
micepad pax export --group "Speakers" --format csv --output speakers.csv

# Security cleanup
micepad qrlogin list
micepad qrlogin revoke qr_xxx
micepad checkins remove-staff vol1@example.com
micepad forms unpublish frm_xxx
```

## Filtering Participants

```bash
micepad pax list --status confirmed
micepad pax list --checkin checked_in
micepad pax list --checkin not_checked_in
micepad pax list --group "Speakers"
micepad pax list --search "shopify"
micepad pax list --status confirmed --checkin not_checked_in --limit 100
```

## Configuration

The CLI connects to `wss://studio.micepad.co/terminal` by default. Override with:

```bash
micepad configure --url "wss://studio.micepad.co/terminal"  # Persistent
export MICEPAD_URL="ws://localhost:3000/terminal"             # Local dev
```

## Error Handling

- **Authentication errors**: Run `micepad login` to re-authenticate
- **No active event**: Run `micepad events use SLUG` to set context
- **Permission denied**: Some commands require specific roles or plan levels
- **Team member limit**: Free plans limit staff count. Check plan limits before bulk-adding staff.
- **Duplicate fields on forms**: Always `forms fields` first. Fields bound to participant columns (company_name, job_title) should be unhidden, not duplicated.
- **`--watch` mode**: Runs continuously. Use briefly for verification, then Ctrl+C to proceed.
- **`--json` flag is broken**: Commands ignore `--json` and return table format. Do not rely on it for machine-readable output until fixed server-side.
