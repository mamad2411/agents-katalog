# Parallel Implementation

Implement changes across multiple files using parallel agents.

## Instructions

When implementing a feature that touches multiple areas, spawn specialized agents in PARALLEL:

1. **Backend Agent** - Python scripts, data pipeline
2. **Frontend Agent** - JavaScript, MapLibre, UI
3. **Docs Agent** - Update documentation
4. **Test Agent** - Add/update tests

## Workflow

### 1. Plan Phase (You do this)
- Identify files to change
- Determine which agents needed
- Define clear scope for each

### 2. Spawn Phase (PARALLEL)
Spawn all implementation agents in a SINGLE message:

```
<Task: Backend - implement infer_road_dates.py>
<Task: Frontend - update createRoadFilter in app.js>
<Task: Docs - update DATA_SCHEMA.md with road fields>
```

### 3. Verify Phase (You do this)
- Check agent outputs
- Resolve any conflicts
- Run validation

## Agent Scoping Rules

Each agent should:
- Have a CLEAR, LIMITED scope
- Know which files to modify
- Understand the interfaces to other agents
- NOT overlap with other agents

## Example: Adding Water Layer

```markdown
## Backend Agent Scope
Files: scripts/ingest/fetch_osm_water.py, scripts/normalize/normalize_water.py
Task: Fetch and normalize water data to schema

## Frontend Agent Scope
Files: frontend/app.js (water layers section only)
Task: Add water-historical source and layers

## Docs Agent Scope
Files: docs/tech/DATA_SCHEMA.md (water section)
Task: Document water schema fields

## Test Agent Scope
Files: Run validation scripts
Task: Verify water layer displays correctly
```

## Conflict Resolution

If agents produce conflicting changes:
1. Architecture agent has priority on patterns
2. Schema changes must be consistent
3. Frontend waits for backend interfaces

## Key Patterns

### Interface First
Define interfaces between agents before spawning:
```
Backend exports: data/sources/osm/water.geojson
Frontend expects: GeoJSON with {wtype, sd, ed, ev, name}
```

### Atomic Changes
Each agent produces a complete, working change:
- Not partial implementations
- Includes error handling
- Follows existing patterns

### Clear Handoffs
Agents declare their outputs:
```
## Agent Output
Created: scripts/ingest/fetch_osm_water.py
Modified: none
Exports: data/sources/osm/water.geojson (41 features)
```
