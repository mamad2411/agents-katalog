---
name: excalidraw-draw
description: Collaborative whiteboard with Excalidraw
version: 1.0.0
tags: [collaboration, whiteboard, drawing, self-hosted]
---

# Excalidraw – Virtual Whiteboard

Excalidraw is a collaborative, hand-drawn-style virtual whiteboard
for sketching diagrams, wireframes, and ideas.

- **GitHub**: github.com/excalidraw/excalidraw (95 000+ ⭐)
- **License**: MIT
- **Security**: No server-side storage (end-to-end encrypted). No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{EXCALIDRAW_URL}}` | Base URL of self-hosted Excalidraw |

## Usage Examples

### Access the whiteboard

```bash
curl -s "{{EXCALIDRAW_URL}}"
```

## AI Agent Tips

- End-to-end encrypted live collaboration via shareable links.
- Export to PNG, SVG, or JSON for embedding in docs.
- Library of shapes and icons for common diagram elements.
- Embeddable React component for integrating into other apps.
