---
name: notion-blocks-formatter 
description: >
  Formats and publishes content to Notion with full control over block types and formatting.
  Use this skill whenever the user wants to push, send, publish, paste, or save content into Notion.
  Also triggers when the user says things like "put this in Notion", "send to Notion", "publish to Notion",
  "format for Notion", or "save this to my Notion page". The skill asks which formatting profile to use,
  navigates the user's Notion workspace to pick a destination page, and publishes using the Notion API.
---

# Notion Block formatter Skill

Formats content and publishes it to a chosen Notion page via the API.

---

## How this skill works

When invoked, follow these steps **in order**:

1. **Check for saved formatting profiles** (see below)
2. **Ask the user which profile to use** (or define a new one)
3. **Ask for destination page** — navigate the workspace interactively
4. **Convert content to Notion blocks** using the chosen profile
5. **Publish via Notion API**

---

## Step 1 — Formatting Profiles

Profiles are stored in memory within this skill session and persist across the conversation.

At the start of each session, profiles start empty. The user can define and name them during the conversation.

**Built-in default profile (always available):**
```
Default Profile:
- # Heading 1       → toggle_heading_1
- ## Heading 2      → toggle_heading_2
- ### Heading 3     → toggle_heading_3
- > Quote           → quote block
- **text**          → bold
- *text*            → italic
- Plain paragraph   → paragraph (normal text)
- - bullet          → bulleted_list_item
- 1. item           → numbered_list_item
- --- or divider    → divider
```

**User-defined profiles** are created when the user types rules in plain English like:
- "headings as toggle 2, subheadings as toggle 3, quotes as callout"
- "all headings bold toggle 1, body text normal, bullets as numbered"

Parse these plain English rules and map them to Notion block types (see references/notion-blocks.md).

---

## Step 2 — Ask which profile to use

At the start of every invocation, show available profiles and ask:

```
📋 Formatting Profiles:
  1. Default (toggle headings, bold text, quotes)
  [2. Any user-saved profiles listed here]
  N. Define a new formatting

Which would you like to use? (type number or describe new rules)
```

If the user picks an existing profile → proceed to Step 3.

If the user defines new rules:
- Parse their plain English into a profile
- Show them a summary: "Got it — here's what I'll apply: ..."
- Ask: "Save this as a named profile for next time? (yes / no, and what name?)"
- Then proceed to Step 3.

---

## Step 3 — Navigate to destination page

You need a Notion API key and the page ID where content will be published.

### First-time setup (if no API key provided yet)
Tell the user:
```
I need your Notion API key and the page to publish to.

Setup (takes 2 min):
1. Go to notion.so/my-integrations → New integration → copy the API key
2. Open your target Notion page → click ··· → Connections → add your integration
3. Copy the page URL — the ID is the last part after the final dash

Paste your API key here to continue:
```

### Page navigation (once API key is available)

Use the Notion API to list pages the integration has access to:

```
GET https://api.notion.com/v1/search
Body: { "filter": { "value": "page", "property": "object" } }
Headers: { "Authorization": "Bearer API_KEY", "Notion-Version": "2022-06-28" }
```

Display results as a numbered list:
```
📁 Your Notion pages:
  1. My Notes
  2. Projects
  3. Research
  ...

Type a number to select, or type a page name to search.
After selecting, I'll show any subpages inside it.
```

When user selects a page, fetch its child blocks to find nested pages:
```
GET https://api.notion.com/v1/blocks/{page_id}/children
```

Filter children where `type === "child_page"` and display them as a sub-list:
```
📄 Inside "Projects":
  1. Q1 Planning
  2. Product Roadmap
  3. → Paste here (this page)

Go deeper, or choose "Paste here"?
```

Repeat this drill-down until the user says "paste here" or selects a page with no subpages.

---

## Step 4 — Convert content to Notion blocks

Read the reference file for all supported block types:
→ `references/notion-blocks.md`

Parse the user's content and map each element to the correct Notion block based on the chosen profile.

**Key rules:**
- Toggle headings wrap their content as `children` inside the toggle block
- Bold/italic are `annotations` on `rich_text`, not separate blocks
- Nested content (e.g. body text under a heading) should be `children` of the toggle block above it
- Always preserve the order of content

**Example mapping for Default Profile:**

Input:
```
## Why Habits Matter
Small habits compound over time. **Start small.**
> "We are what we repeatedly do." — Aristotle
```
- A paragraph with mixed bold/italic needs multiple `rich_text` spans

Output blocks:
```json
[
  {
    "type": "toggle",
    "toggle": {
      "rich_text": [{ "type": "text", "text": { "content": "Why Habits Matter" }, "annotations": { "bold": false } }],
      "children": [
        {
          "type": "paragraph",
          "paragraph": {
            "rich_text": [
              { "type": "text", "text": { "content": "Small habits compound over time. " } },
              { "type": "text", "text": { "content": "Start small." }, "annotations": { "bold": true } }
            ]
          }
        },
        {
          "type": "quote",
          "quote": {
            "rich_text": [{ "type": "text", "text": { "content": "\"We are what we repeatedly do.\" — Aristotle" } }]
          }
        }
      ]
    }
  }
]
```

---

## Step 5 — Publish to Notion

```
POST https://api.notion.com/v1/blocks/{destination_page_id}/children
Headers:
  Authorization: Bearer {API_KEY}
  Content-Type: application/json
  Notion-Version: 2022-06-28
Body:
  { "children": [ ...converted blocks ] }
```

On success, confirm to the user:
```
✅ Published to "[Page Name]" in Notion!
   X blocks created.
   Open page → [notion.so/page-id]
```

On error, show the error message and suggest fixes (e.g. "Make sure your integration is connected to this page").

---

## Profile memory across the conversation

Keep a `profiles` object in context like:
```
profiles = {
  "Default": { ...default mapping... },
  "Blog Style": { "##": "toggle_2", "###": "toggle_3", ">": "callout", ... },
  ...
}
```

When a user saves a new profile, add it here and reference it by name in future invocations.

---

## Edge cases

- **No headings in content** — treat all text as paragraphs
- **Deeply nested content** — Notion only supports 1 level of children inside toggles; flatten anything deeper into sequential blocks
- **Code blocks** — map ``` fenced blocks to Notion `code` block type
- **Tables** — map markdown tables to Notion `table` blocks
- **Images** — skip with a note: "Images must be added manually in Notion"
- **API rate limits** — if publishing many blocks, batch into chunks of 100

---

Read `references/notion-blocks.md` before converting any content.