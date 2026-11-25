---
name: excalidraw-vibe-planning
description: |
  Collaborative visual brainstorming and architecture design using Excalidraw MCP.

  Triggers when user mentions:
  - "vibe plan" or "vibe planning"
  - "brainstorm architecture" or "architecture diagram"
  - "draw out" or "sketch out" system design
  - "let's diagram" or "visualize this"
  - "excalidraw session" or "whiteboard this"
---

# Excalidraw Vibe Planning

Collaborative visual brainstorming and architecture design using Excalidraw MCP server.

## What it does

Transforms abstract ideas into visual diagrams in real-time. Use this skill when you want to:
- Brainstorm system architecture
- Map out data flows
- Design API contracts
- Plan frontend component hierarchies
- Visualize database schemas
- Explore microservices relationships
- Create user journey maps

## Prerequisites

1. **Excalidraw Canvas Server** must be running:
   ```bash
   docker run -d -p 3000:3000 --name mcp-excalidraw-canvas ghcr.io/yctimlin/mcp_excalidraw-canvas:latest
   ```

2. **Excalidraw MCP** configured in `.opencode/mcp-config.json`:
   ```json
   {
     "excalidraw": {
       "type": "local",
       "command": ["docker", "run", "-i", "--rm", "-e", "EXPRESS_SERVER_URL=http://host.docker.internal:3000", "-e", "ENABLE_CANVAS_SYNC=true", "ghcr.io/yctimlin/mcp_excalidraw:latest"],
       "enabled": true
     }
   }
   ```

3. **OpenCode restart** after config changes

## How to use

### 1. Start with a concept

Describe what you want to build at a high level. Include:
- The core problem you're solving
- Key entities/components
- Integrations with external systems
- Scale considerations

### 2. Iterate visually

I'll create diagrams and we can refine together:
- Add/remove components
- Show data flows
- Mark synchronous vs async interactions
- Highlight potential bottlenecks
- Annotate with questions/decisions

### 3. Document decisions

Once we land on an architecture, I'll capture:
- Component responsibilities
- Interface contracts
- Technology choices
- Open questions for later

## Available MCP Tools

### Canvas Operations
- `excalidraw_create_element` - Add rectangles, text, arrows
- `excalidraw_update_element` - Modify existing elements
- `excalidraw_delete_element` - Remove elements
- `excalidraw_get_canvas_info` - Get current canvas state

### Layout & Organization
- `excalidraw_group_elements` - Group related components
- `excalidraw_align_elements` - Align and distribute
- `excalidraw_distribute_elements` - Even spacing
- `excalidraw_layer_elements` - Control z-index

### Scene Management
- `excalidraw_clear_canvas` - Start fresh (confirm first!)
- `excalidraw_export_svg` - Export for documentation
- `excalidraw_export_png` - Export for presentations

### Viewport Control
- `excalidraw_zoom_to_selection` - Focus on specific area
- `excalidraw_zoom_to_fit` - See entire diagram

## Design Patterns

### Color Coding
- **Blue (#339af0)** - User-facing components (UI, APIs)
- **Green (#51cf66)** - Data stores (DB, cache, blob)
- **Orange (#ff922b)** - External services (3rd party APIs)
- **Purple (#9775fa)** - Background workers (queues, jobs)
- **Gray (#adb5bd)** - Infrastructure (load balancers, gateways)

### Shape Conventions
- **Rectangles** - Services/components
- **Cylinders** - Databases/storage
- **Clouds** - External services
- **Diamonds** - Decision points
- **Arrows** - Data flow direction

### Layout Approaches
- **Left-to-right** - Request/response flows
- **Top-to-bottom** - Layered architecture (frontend → backend → data)
- **Hub-and-spoke** - Microservices around a core
- **Swimlanes** - Multi-tenant or multi-service flows

## Example Sessions

### Example 1: New SaaS Platform

**User:** "I want to build a project management SaaS. Let's vibe plan it out."

**Process:**
1. Start with high-level boxes: Web App, API Gateway, Core Services, Database
2. Break down Core Services: Auth, Projects, Tasks, Notifications, Billing
3. Add external integrations: Stripe, SendGrid, S3 for file storage
4. Show data flows: User creates project → API → Project Service → DB → Notification Service → Email
5. Mark real-time features: WebSocket connections for live updates
6. Annotate scale decisions: "Read replicas for tasks?" "Cache layer for projects?"

### Example 2: Refactoring Monolith

**User:** "We need to break our monolith into services. Can you help visualize an approach?"

**Process:**
1. Draw current state: Single box labeled "Monolith" with arrows to DB
2. Identify bounded contexts: User Management, Orders, Inventory, Shipping
3. Draft target state: Separate service boxes with event bus between them
4. Show migration path: Strangler fig pattern, gradually moving routes
5. Highlight risks: Data consistency, transaction boundaries, testing strategy
6. Create decision matrix: Which service to extract first?

### Example 3: AI Feature Integration

**User:** "I want to add AI-powered recommendations to our e-commerce app."

**Process:**
1. Current architecture: Web → API → Product Service → PostgreSQL
2. Add AI components: Embedding Service, Vector DB (Pinecone), LLM Gateway
3. Show flows:
   - Product ingestion: Product Service → Embedding Service → Vector DB
   - Recommendation request: User action → API → Embedding Service → Vector search → Results
4. Considerations: Latency, cost, caching strategies, fallback logic
5. Annotate: "Batch embedding updates?" "Real-time vs cached recommendations?"

## Safety Guidelines

1. **Confirm before clear** - Always ask before wiping the canvas
2. **Save periodically** - Export SVG/PNG as checkpoints
3. **Label WIP areas** - Mark sections as "exploratory" vs "decided"
4. **One concept at a time** - Don't overcrowd; create multiple diagrams if needed

## Tips for Great Sessions

- **Start abstract** - Big boxes first, details later
- **Ask questions** - "Is this synchronous?" "What happens if this fails?"
- **Use annotations** - Text boxes for assumptions, constraints, TODOs
- **Iterate fast** - Don't perfect; rough and rapid is the vibe
- **Capture output** - Export final diagrams for documentation

## Troubleshooting

**Canvas won't connect?**
- Check Docker: `docker ps | grep excalidraw`
- Verify port 3000 not in use: `lsof -i :3000`
- Check OpenCode MCP config is valid JSON

**Changes not appearing?**
- Canvas auto-syncs every few seconds
- Try `excalidraw_get_canvas_info` to refresh state
- Check browser at http://localhost:3000

**Docker issues?**
- Restart container: `docker restart mcp-excalidraw-canvas`
- View logs: `docker logs mcp-excalidraw-canvas -f`
- Full reset: Remove and recreate container
