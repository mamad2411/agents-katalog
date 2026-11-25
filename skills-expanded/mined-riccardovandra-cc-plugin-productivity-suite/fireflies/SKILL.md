---
name: fireflies
description: Extracts meeting transcripts from Fireflies.ai. Lists available transcripts with search by participant name or date, displays full transcript in conversation. Use when user asks to get Fireflies transcripts, meeting recordings, call notes, or mentions a conversation with someone.
---

# Fireflies Transcript Extraction

Pull meeting transcripts from Fireflies.ai for review or analysis.

---

## Activation

This skill activates when user:

-   Mentions "Fireflies" or "meeting transcript"
    
-   Asks about a "call" or "conversation" with someone
    
-   Wants to review meeting notes
    
-   References a recorded meeting
    

---

## Capabilities

| Operation | Description | Module |
| --- | --- | --- |
| Extract | List, select, and extract transcripts | EXTRACT.md |

---

## Quick Start

```
User: "Get my call with Owen"
→ Lists transcripts filtered by "Owen"
→ User selects the right one
→ Displays full transcript
→ Asks if user wants to save
```

```
User: "Show my recent Fireflies transcripts"
→ Lists last 20 transcripts
→ User picks one to extract
```

---

## Workflow

1.  **List** - Show available transcripts (optionally filtered)
    
2.  **Select** - User chooses which transcript
    
3.  **Extract** - Fetch and display full text
    
4.  **Save** (optional) - Store to `context/calls/`
    

---

## Environment

| Variable | Description |
| --- | --- |
| FIREFLIES_API_KEY | API key from Fireflies.ai settings |

---

## Scripts

```bash
# List transcripts
uv run .claude/skills/fireflies/scripts/fireflies.py list [options]

# Options:
#   --participant, -p  Filter by name/email
#   --from-date, -f    From date (YYYY-MM-DD)
#   --to-date, -T      To date (YYYY-MM-DD)
#   --limit, -l        Max results (default: 20)

# Get specific transcript
uv run .claude/skills/fireflies/scripts/fireflies.py get <id> [--output PATH]
```

---

## Output Location

When saving: `context/calls/{sales-calls|client-calls}/{date} - {title}.md`