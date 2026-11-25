---
name: ui-page-settings
description: "How to build settings screens: the section list and how it becomes pages on a phone, grouping by what people look for, one save model per section, profile, security with password change, two-factor setup and sessions, notifications as a matrix of events by channel, billing, members, integrations, API keys shown once, the danger zone with typed confirmation, and search. Read before building or reworking settings."
---

# Settings

Generated settings are one long page of every option in cards, Save at
the top and again at the bottom, switches that save at once beside fields
that wait for Save, "Delete account" in red next to "Update profile", an
API key shown in full forever, and forty unlabelled notification
checkboxes. People come rarely, for one thing, often in a hurry (a security
worry, an email to stop): this skill lets them find it, change it, and know
it is saved.

One kind of screen. The measures are in `ui-layout` (section 2b: a form
keeps a readable column, left-aligned); fields, choices, tables and dialogs
have their `ui-part-*` skills; field behaviour is `frontend-forms`; the
server side of passwords, sessions and keys is `backend-auth`.

## 1. The layout

```
│ [app sidebar] │ Settings                                               │
│               │ ┌──────────────────┐  Notifications                    │
│               │ │ ⌕ Search         │  Changes save automatically.      │
│               │ │ Account          │  ──────────────────────────────── │
│               │ │   Profile        │  Event              Email   Push  │
│               │ │   Security       │  Mentions            [x]     [x]  │
│               │ │ ▌ Notifications  │  Comments on yours   [x]     [ ]  │
│               │ │   Preferences    │  Weekly summary      [ ]     [ ]  │
│               │ │ Workspace        │  Security alerts     [x]  always  │
│               │ │   General        │                                   │
│               │ │   Members        │                                   │
│               │ │   Billing        │                                   │
│               │ │   API keys       │                                   │
│               │ └──────────────────┘                                   │
```

- A left column of sections, 200 to 240px, beside a single column of fields
  at most 640px wide, both anchored to the shell's left edge, never centred.
  Tables (members, keys, invoices) may run wider, to about 960px.
- Each section is its own route (`/settings/notifications`) that emails
  and support answers can link to; its name is the `h1`, related settings
  grouped under `h2` headings.
- On a phone the section list is a page of its own (48 to 56px rows with a
  chevron), each section opening as a page with a back link to Settings.
  With two to four sections, a scrolling tab row instead.

## 2. Group by what people look for

| Section | Holds | Who sees it |
|---|---|---|
| Profile | Name, photo, username, public details | Everyone |
| Security | Email, password, passkeys, two-factor, sessions, activity | Everyone |
| Notifications | The matrix, digests, quiet hours | Everyone |
| Preferences | Theme, language, time zone, date format | Everyone |
| General (workspace) | Name, address, logo, defaults, deleting it | Admins |
| Members | People, roles, invitations | Admins; others read only |
| Billing | Plan, usage, payment method, invoices | Owners, billing role |
| Integrations | Connected services and what they may do | Admins |
| API keys | Keys, webhooks | Developers, admins |

- The person's settings apart from the workspace's, as two headed groups;
  names in the users' words ("Notifications", not "Communication
  preferences").
- Sections a person cannot change are read-only and say who can ("Only
  owners can change billing. Ask [owner name]."), or are hidden.

## 3. One save model per section

Say it once, and never mix the two in one group.

- **Saved on change**, for a control that takes effect at once: a switch,
  a radio group, a select (theme, language, one notification). Apply it
  straight away, show "Saved" beside it or in the group's header for 2 to 3
  seconds (`role="status"`), and on failure put the old value back with
  the reason ("Could not save. Try again.").
- **Explicit Save**, for a form of related fields (profile, billing
  address, workspace details): nothing changes until Save. The Save button
  sits at the end of the form, aligned with the fields; on a long form a
  bar appears once something changed ("Unsaved changes · Discard · Save
  changes"), sticky at the bottom. Leaving with unsaved changes asks first.
- A switch inside a Save form looks instant and is not
  (`ui-part-choices`): saved-on-change controls get their own group. A text
  field saved on change (a bio) waits 1 to 2 seconds after typing stops,
  then shows "Saving…" and "Saved at 14:02".

## 4. Profile and account

- Photo: upload, crop to the avatar's shape, preview, remove; initials when
  there is none (`ui-part-avatars`).
- Changing the email sends a link to the new address; the old one stays
  active until it is confirmed and is told of the change. Meanwhile:
  "Pending: confirm the link sent to new@... · Resend · Cancel". Changing
  a username warns what breaks (links, mentions).
- Email, password, two-factor, keys and deletion ask for the password or a
  passkey again when the last sign-in is not recent.

## 5. Security

- **Password**: the current one (`autocomplete="current-password"`), the
  new one (`autocomplete="new-password"`) with a show toggle and its rule
  in words ("At least 12 characters"), no rules about symbols; afterwards
  other sessions are signed out, and the page says so.
- **Passkeys**: "Add a passkey"; a list with a name the person can edit,
  when it was added and last used, and Remove.
- **Two-factor**, set up in four steps: choose the method (an authenticator
  app first, SMS only as a fallback); scan the QR code or type the setup
  key (shown as text in groups of four, with Copy); enter a 6-digit code
  (`autocomplete="one-time-code" inputmode="numeric"`); save the recovery
  codes, shown once with Copy, Download and Print, confirmed before Finish.
  Afterwards the status in words ("On · authenticator app · added 12 Mar
  2026"), with Regenerate codes and Turn off (asking again first).
- **Sessions and devices**: device and browser ("Chrome on macOS"), an
  approximate place (from the IP, labelled so), last active, "This device"
  marked; Sign out per row, and "Sign out of all other sessions". Recent
  sign-ins and security changes below, from the server's records.

## 6. Notifications as a matrix

- Rows are events grouped by topic (Comments, Mentions, Billing,
  Security), each named for what happens ("Someone mentions you"); columns
  are the channels that exist (Email, Push, In-app, WhatsApp).
- A real table, each checkbox named by its row and column:

```html
<table>
  <thead><tr><th scope="col">Event</th>
    <th scope="col" id="ch-email">Email</th><th scope="col" id="ch-push">Push</th></tr></thead>
  <tbody><tr>
    <th scope="row" id="ev-mention">Someone mentions you</th>
    <td><input type="checkbox" aria-labelledby="ev-mention ch-email" checked></td>
    <td><input type="checkbox" aria-labelledby="ev-mention ch-push"></td>
  </tr></tbody>
</table>
```

- Messages that are always sent (security alerts, receipts) shown ticked
  and locked, with the reason ("Always sent, for your security").
- Frequency (instant, a daily digest) and quiet hours where they apply,
  each saved on change; an email's unsubscribe link lands on its row.
- On a phone, one block per topic: each event with its channel switches
  under it, or one page per channel.

## 7. Billing, members, integrations

- **Billing**: the plan, its price and renewal date; usage against limits
  as numbers ("7 of 10 seats"); Change plan; the payment method as brand,
  last four digits and expiry, managed through the provider (Stripe's
  customer portal or its Payment Element), never your own card form;
  invoices as a table (date, number, amount, status, PDF); billing email
  and tax details. Cancelling says what happens, and when.
- **Members**: a table (name and email, role, last active); Invite by email
  with a role, each role described in one line; pending invitations with
  Resend, Revoke and expiry; change role; remove, saying what happens to
  their work; transfer ownership; seats against the plan.
- **Integrations**: each connected service with "Connected as [account]",
  what it can reach in plain words, the last sync and any error with its
  fix, and Disconnect (saying what stops working).

## 8. API keys

- A table: the name, the prefix and last four (`sk_live_…4f2a`), scopes,
  created by and when, last used (or "Never"), expiry; Revoke in a menu.
- Creating asks for a name ("What is this key for?"), the scopes (read-only
  by default), and an expiry (30 or 90 days, a date, or none with a
  warning). Then the key is shown once, in a read-only field with Copy and
  the line "Copy this key now. You will not see it again.", then Done.
  Afterwards only the prefix and last four remain: the server keeps a hash.
- Revoking names the key and what stops working, at once. Rotating is
  create, switch the callers, revoke (last used shows when the old key went
  quiet). Test and live keys labelled.
- Webhooks: the endpoint, the events, the signing secret revealed after
  asking for the password again, recent deliveries with status and Resend.
- Keys never go into URLs, logs, analytics or error reports.

## 9. The danger zone

- Last on its page (Security for the person's account, General for the
  workspace), set apart under a heading and a hairline in the danger
  colour, not a red block, and never beside Save.
- Each action in a sentence with what is lost, counted from real data
  ("Deletes 3 projects and 1,284 files and cancels the subscription"), the
  export offered first ("Download your data"), a button naming the action
  ("Delete workspace").
- The confirmation dialog repeats the consequence and asks to type the
  workspace's name (or the account's email); the button acts only once it
  matches, the password is asked again when needed; afterwards a
  confirmation email. A grace period ("restore within 30 days") only when
  the backend keeps one.
- Leave workspace and transfer ownership live here too; an owner transfers
  before deleting an account that owns a workspace.

## 10. Search, keyboard and screen readers

- With more than about eight sections or forty settings, a search field
  at the top of the list, matching labels and synonyms ("2FA", "MFA",
  "dark mode"); a result opens the section with the setting scrolled into
  view, focused and briefly highlighted.
- The list is a `nav` named "Settings" with `aria-current="page"`; after
  moving to a section in a single-page app, focus goes to its `h1`.
- Switches are real (`role="switch"` on a button with `aria-checked`, or on
  a checkbox), with their description tied by `aria-describedby`; "Saved"
  in a `role="status"` region; errors beside their field.
- The Save bar is announced politely and never steals focus; dialogs come
  from the component library (focus kept inside, Escape, focus returned).

## 11. States and the phone

- Loading: the list and the headings at once, skeletons per group
  (`ui-part-loading`). Plan-gated settings say which plan has them and link
  to Billing, only when that is true.
- Phone: the index page, then section pages with 16px padding; setting rows
  with the label and description at the left and the switch at the right,
  44px high at least; forms in one column; the Save bar above the safe
  area; tables as cards (a key: its name, prefix, last used, a menu).

## Check it

- `preview` with `login` at 360, 768 and 1440px: the list becomes an index
  page on a phone, nothing overflows, touch targets pass.
- In each section change something and reload: it is kept. Offline, a
  flipped switch returns with a message; leaving an edited form asks.
- A new API key shows in full once, only its prefix after a reload. The
  danger zone's button stays inactive until the exact name is typed.
- Keyboard through the list, switches and matrix; a screen reader reads
  "Someone mentions you, Email, checkbox, checked". Then `ui_check`.

## Avoid

One long page of every setting; Save at the top and at the bottom;
switches that wait for Save; Delete beside Save; a red block for the
danger zone; an API key visible after creation; deleting without saying
what goes; unlabelled checkboxes; "Communication preferences"; settings
shown as editable to people who cannot change them; a place from an IP
presented as exact; SMS as the only second factor; the settings column
floating centred in the shell.
