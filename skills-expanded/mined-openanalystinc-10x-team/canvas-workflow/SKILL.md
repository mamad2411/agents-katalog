---
name: canvas-workflow
description: |
  Visual workflow canvas for 10x-Team outreach system. Use this skill to design, visualize,
  and execute multi-platform outreach workflows on an infinite canvas powered by TLDraw.
allowed-tools:
  - Bash
  - Read
  - Write
  - WebFetch
---

# 10x-Team Visual Workflow Canvas

A TLDraw-based infinite canvas for designing and visualizing outreach workflows. Design workflows visually, configure nodes, connect them with arrows, and export to Claude Code for execution.

## Quick Start

```bash
# Start the canvas server
cd canvas && npm run dev -- --port 3006
```

Then open: **http://localhost:3006/**

## When to Use This Skill

Use this skill when the user:
- Wants to visually design an outreach workflow
- Needs to see their campaign as a visual diagram
- Wants to drag-and-drop skill nodes
- Needs to configure workflow steps
- Wants to export workflow configurations
- Wants to brainstorm campaign strategies visually

## Canvas Features

### Skill Nodes
Visual representations of 100X Outreach skills:

| Node | Icon | Description | Inputs | Outputs |
|------|------|-------------|--------|---------|
| Discovery | 🔍 | Find people using Exa AI | query | people |
| Audience | 👥 | Define target audience | - | filters |
| LinkedIn | 💼 | LinkedIn automation | person | sent |
| Twitter | 🐦 | Twitter/X automation | person | sent |
| Instagram | 📸 | Instagram automation | person | sent |
| Gmail | 📧 | Send emails via Gmail | person, template | sent |
| Template | 📝 | Message templates | context | message |
| Workflow | ⚡ | Multi-step sequences | trigger | complete |
| Campaign | 🚀 | Full outreach campaigns | audience, message | results |

### Node Configuration
Click any node to open the configuration panel:
- **Discovery**: Search query, max results, source (Exa/LinkedIn/Twitter)
- **LinkedIn**: Action (connect/message/view/like/comment), template, delay
- **Twitter**: Action (follow/dm/like/reply/retweet), template, delay
- **Instagram**: Action (follow/dm/like/comment/story_reply), template, delay
- **Gmail**: Subject, template, auto follow-up settings
- **Template**: Name, content with variables
- **Campaign**: Name, goal, daily limit

### Workflow Templates
Pre-built workflow configurations with connections:

| Template | Nodes | Description |
|----------|-------|-------------|
| 💼 B2B Outreach | 4 | 14-day professional sequence: Audience → Discovery → LinkedIn → Email |
| 🤝 Brand Partnership | 4 | 21-day brand outreach: Audience → Instagram/Twitter → Email |
| ⭐ Influencer Outreach | 5 | Value-first creator approach with social warm-up |
| 🌐 Multi-Platform | 5 | 30-day adaptive routing across all channels |
| 📧 Email Sequence | 4 | 7-day email drip campaign |
| 🔍 Discovery Pipeline | 4 | Find and qualify leads from multiple sources |

### Connections
Draw arrows between nodes to define workflow order:
1. Click the **🔗 Connect** button in the toolbar
2. Click the **source** node
3. Click the **target** node
4. Arrow is automatically drawn with proper styling

## Canvas Controls

| Action | How |
|--------|-----|
| Add Node | Click skill icon in toolbar |
| Move Node | Drag node |
| Select | Click node |
| Multi-select | Shift+click or drag box |
| Delete | Select + Delete/Backspace |
| Connect Nodes | Click 🔗, then source, then target |
| Configure Node | Select node → config panel appears |
| Pan | Drag empty space |
| Zoom | Scroll wheel |
| Fit View | Click "🔍 Fit View" button |

## Running Workflows (Auto-Execution)

When you click the **▶ Run** button in the canvas:

1. **Workflow is saved** to `output/workflow-queue/latest.json`
2. **Nodes turn orange** to indicate they're queued
3. **Go to Claude Code** and say: `/workflow run`
4. **Workflow executes** automatically with proper rate limiting

### The Run Flow

```
Canvas (Click Run) → Saves to workflow-queue → Claude Code → /workflow run → Executes Skills
```

### Workflow Queue Location

```
output/
└── workflow-queue/
    ├── latest.json          # Most recent workflow (always overwritten)
    └── workflow-{timestamp}.json  # Archived workflows
```

### JSON Format

The canvas exports workflows in this format:

```json
{
  "name": "10x-Team Workflow",
  "version": "1.0",
  "created": "2024-01-21T...",
  "nodes": [
    {
      "id": "shape:abc123",
      "type": "discovery",
      "label": "Find Prospects",
      "position": { "x": 100, "y": 100 },
      "config": {
        "query": "AI startup founders",
        "maxResults": 50
      }
    }
  ],
  "connections": [
    {
      "from": "shape:abc123",
      "to": "shape:def456"
    }
  ]
}
```

### Alternative Methods

**Method 1: Copy to Clipboard**
If auto-save fails, workflow is copied to clipboard as backup.

**Method 2: Manual Paste**
Paste workflow JSON directly in Claude Code and say "Run this workflow".

## Integration with Claude Code

The canvas works with Claude Code as the orchestration brain:

```
Canvas (Design) → Export JSON → Claude Code (Orchestrate) → Skills (Execute)
                                      ↓
                              10x Team Browser Extension
                              Gmail API
                              Exa AI
```

### Execution Flow

When user exports and pastes to Claude Code:

1. Claude Code parses the workflow JSON
2. Reads the execution order from connections
3. For each node in order:
   - Reads the node configuration
   - Calls the appropriate skill (discovery-engine, linkedin-adapter, etc.)
   - Passes inputs from previous nodes
   - Respects rate limits and delays
   - Updates node status
4. Reports completion

### Example Execution

```
User: "Run this workflow" (pastes JSON)

Claude Code:
1. Parses workflow with 4 nodes, 3 connections
2. Executes discovery-engine with query "AI founders"
3. Gets 50 people
4. For each person (with rate limiting):
   - Executes linkedin-adapter (connect)
   - Waits 24 hours
   - Executes gmail-adapter (send email)
5. Reports: "Workflow complete! 50 people contacted"
```

## Templates Library

The canvas includes 91 message templates across 4 platforms:

| Platform | Count | Categories |
|----------|-------|------------|
| LinkedIn | 29 | Connection Requests, Messages, InMails, Comments |
| Twitter | 22 | DMs, Tweets, Replies |
| Instagram | 22 | DMs, Comments, Stories |
| Email | 18 | Outreach, Follow-up, Promotional, Newsletters |

Templates can be selected directly in node configuration.

## Claude Code Commands

```bash
# Start canvas server
cd canvas && npm run dev -- --port 3006

# Build for production
cd canvas && npm run build

# Preview production build
cd canvas && npm run preview
```

## Node Properties

Each node has:
- **id** - Unique identifier
- **type** - Skill type (discovery, linkedin, etc.)
- **label** - Display name
- **description** - What the node does
- **status** - idle | running | completed | error
- **inputs** - Required inputs (blue badges)
- **outputs** - Produced outputs (green badges)
- **config** - Node-specific configuration
- **position** - x, y coordinates on canvas

## Rate Limiting

The canvas respects 100X Outreach rules:

| Platform | Between Actions | After Follow |
|----------|----------------|--------------|
| LinkedIn | 24-48 hours | 24 hours |
| Twitter | 24-48 hours | 4-24 hours |
| Instagram | 48-72 hours | 24-48 hours |
| Email | Varies | N/A |

## Best Practices

1. **Start with a template** - Load a pre-built workflow and customize
2. **Connect nodes left-to-right** - Maintains visual flow
3. **Configure before running** - Set templates and queries
4. **Test with small batches** - Set low maxResults first
5. **Use the config panel** - Click nodes to set parameters
6. **Export regularly** - Save workflows as JSON backups

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Delete | Remove selected nodes |
| Ctrl+A | Select all |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Scroll | Zoom in/out |

## Troubleshooting

### Connections not appearing
- Make sure you click the source node first, then the target
- Wait for the connection mode indicator to show "Target"
- Try zooming out to see if connection is off-screen

### Nodes not loading from template
- Clear the canvas first with "Clear All"
- Check browser console for errors
- Try refreshing the page

### Export not copying
- Check browser clipboard permissions
- Try the "Copy Prompt" button instead
- Manually copy from browser console
