# Miro MCP Skill

Access Miro whiteboards through the Model Context Protocol (MCP) server.

## Overview

This skill connects to your local Miro MCP server to create and manage whiteboards for collaborative planning, job preparation, and visual organization.

**Required:** The Miro MCP server must be running locally.

## Configuration

The skill connects to the Miro MCP server at: `C:/Users/clayb/OneDrive/Desktop/Donjon.Agency/mcp-server-miro/server.py`

Add to your `.opencode/mcp-config.json`:
```json
{
  "mcpServers": {
    "miro": {
      "command": "python",
      "args": ["C:/Users/clayb/OneDrive/Desktop/Donjon.Agency/mcp-server-miro/server.py"],
      "env": {
        "MIRO_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Available Tools

### Board Operations
- `create_board` - Create a new whiteboard
- `get_board` - Get board details
- `update_board` - Update board name/description
- `delete_board` - Delete a board
- `get_board_items` - List all items on a board

### Visual Items
- `create_shape` - Create geometric shapes with custom colors and text
- `create_sticky_note` - Add colorful sticky notes
- `create_text` - Add text labels and headings
- `create_card` - Add task/story cards with metadata
- `create_frame` - Create container sections

### Relationships
- `create_connector` - Connect items with arrows and lines

### Organization
- `create_tag` - Create colored tags
- `attach_tag` - Tag items for categorization
- `delete_item` - Remove specific items

## Usage Examples

**Create a job prep board:**
```
Create a Miro board called "JobPrep - Impel Software Architect"
```

**Add sticky notes:**
```
Add yellow sticky notes for must-have requirements
```

**Create visual diagrams:**
```
Create a tech stack diagram with connected shapes
```

## Resources

- [Miro API Documentation](https://developers.miro.com/reference/api-reference)
- Local MCP Server: C:/Users/clayb/OneDrive/Desktop/Donjon.Agency/mcp-server-miro/server.py

## Troubleshooting

**"MCP server not found" error:**
- Ensure the mcp-config.json has the miro server configured
- Verify the server.py file exists at the specified path
- Check that MIRO_ACCESS_TOKEN is set correctly

**"Connection refused" error:**
- The MCP server should start automatically when needed
- If issues persist, try restarting OpenCode
