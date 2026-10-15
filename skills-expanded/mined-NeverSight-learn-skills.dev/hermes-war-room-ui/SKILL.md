---
name: hermes-war-room-ui
description: UI dashboard for visualizing and controlling Hermes multi-agent orchestration with kanban delegation
triggers:
  - "set up the hermes war room dashboard"
  - "visualize hermes agent orchestration"
  - "create a hermes team interface"
  - "monitor hermes kanban tasks"
  - "build a multi-agent control panel"
  - "manage hermes operative profiles"
  - "deploy the hermes war room"
  - "configure hermes orchestration UI"
---

# Hermes War Room UI

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Hermes War Room is a browser-based visual dashboard for managing Hermes Agent's multi-profile orchestration and kanban delegation system. It provides real-time monitoring of agent operatives, task boards, and mission coordination—transforming command-line agent orchestration into a visual "operations floor."

## What It Does

The War Room wraps the Hermes CLI with a Vue/Nuxt interface that:

- **Visualizes active agents** as operatives on a floor with live status
- **Displays kanban tasks** in a 4-column board (Todo/Ready/Running/Blocked)
- **Manages missions** via chat with an orchestrator agent
- **Auto-nudges** the orchestrator when delegated tasks complete
- **Edits profiles** (SOUL.md, skills, tools) directly from the UI
- **Tracks delegation chains** showing parent/child task relationships

It reads from `~/.hermes/kanban.db` and `~/.hermes/profiles/`, shells out to the `hermes` CLI, and persists UI state in its own SQLite database.

## Installation

### Quick Start (Production Binary)

```bash
# Download and extract the latest release
mkdir -p ~/hermes-war-room && cd ~/hermes-war-room
curl -L -o hermes-war-room.tar.gz \
  https://github.com/Naroh091/hermes-war-room/releases/latest/download/hermes-war-room.tar.gz
tar xzf hermes-war-room.tar.gz

# Run (requires Hermes CLI installed and Node 22+)
HERMES_HOME=$HOME/.hermes NITRO_HOST=127.0.0.1 NITRO_PORT=3000 \
  node .output/server/index.mjs
```

Open `http://localhost:3000` in your browser.

### Development Setup

```bash
git clone https://github.com/Naroh091/hermes-war-room.git
cd hermes-war-room
pnpm install
pnpm dev
```

The dev server runs on `http://localhost:3000`.

## Environment Variables

```bash
# Required
HERMES_HOME=$HOME/.hermes          # Path to Hermes profiles and kanban DB
NITRO_HOST=127.0.0.1               # Bind address
NITRO_PORT=3000                    # Port

# Optional
WAR_ROOM_DB=./data/war-room.db     # War Room's own SQLite database
NODE_ENV=production                # Production/development mode
```

## Key Concepts

### Operatives (Profiles)

Each Hermes profile becomes an "operative" in the War Room:

```vue
<!-- Components displaying operatives -->
<OperativeWorkstation
  :operative="operative"
  :current-task="currentTask"
  @click="openDossier"
/>
```

Operatives have:
- **Callsign**: Display name (e.g., "LIDER", "INVESTIGADOR")
- **Avatar**: Notionist character image
- **Color**: UI accent color
- **Status**: Standing by / Working / Blocked
- **Profile slug**: Maps to `~/.hermes/profiles/<slug>/`

### Orchestrator Pattern

Convention is to have one "leader" profile that **routes but never executes**:

```markdown
<!-- profiles/lider/SOUL.md -->
You are the mission orchestrator. Your job is to:
1. Decompose user goals into discrete tasks
2. Delegate each task via kanban to the right specialist
3. Never do the work yourself
4. Summarize results when workers complete tasks

Always use the terminal tool to create kanban tasks:
hermes kanban create --assignee <worker> --title "..." --body "..." --json
```

Workers have full tool access and execute:

```markdown
<!-- profiles/investigador/SOUL.md -->
You are a research specialist. When assigned a kanban task:
1. Execute the research using available tools
2. Complete the task with: hermes kanban complete <id> --summary "..."
```

### Missions

A mission is a conversation thread with an orchestrator:

```typescript
// server/api/missions/create.post.ts
export default defineEventHandler(async (event) => {
  const { orchestratorId, title } = await readBody(event)
  
  const mission = await db.insert(missions).values({
    orchestrator_id: orchestratorId,
    title: title,
    status: 'open',
    created_at: new Date()
  }).returning()
  
  return mission[0]
})
```

Messages are sent via ACP sessions that persist across turns.

## Server API Endpoints

### Missions

```typescript
// Create a new mission
POST /api/missions/create
{
  "orchestratorId": 1,
  "title": "Research competitor pricing"
}

// Send a message (returns SSE stream)
POST /api/missions/:id/message
{
  "content": "Find pricing for Acme Corp products"
}

// Get mission history
GET /api/missions/:id
```

### Operatives

```typescript
// List all operatives
GET /api/operatives

// Get operative details with current task
GET /api/operatives/:id

// Update operative (callsign, avatar, color, active)
PATCH /api/operatives/:id
{
  "callsign": "RESEARCHER",
  "color": "#3b82f6",
  "active": true
}

// Retrain (update SOUL.md, skills, tools)
POST /api/operatives/:id/retrain
{
  "soul": "You are a specialized legal analyst...",
  "skills": ["research", "analysis"],
  "mcpServers": ["filesystem", "brave-search"]
}
```

### Kanban

```typescript
// Get all tasks for the board view
GET /api/kanban/tasks

// Get tasks for a specific operative
GET /api/kanban/tasks?assignee=investigador

// Watch a task (auto-nudge when complete)
POST /api/kanban/watch
{
  "taskId": "task_abc123",
  "missionId": 5
}
```

## Creating an Orchestration Team

### 1. Set Up Profiles

Create an orchestrator and workers via Hermes CLI:

```bash
# Create orchestrator
hermes profile create lider --model claude-3-5-sonnet-20241022

# Create specialist workers
hermes profile create investigador --model claude-3-5-sonnet-20241022
hermes profile create legal --model claude-3-5-sonnet-20241022
hermes profile create writer --model gpt-4o
```

### 2. Configure SOULs

Edit `~/.hermes/profiles/lider/SOUL.md`:

```markdown
# Mission Orchestrator

You coordinate a team of specialists. When the user gives you a goal:

1. Break it into discrete, parallelizable tasks
2. Assign each task to the right specialist via kanban
3. Never do the work yourself
4. Wait for task completion notifications
5. Synthesize results into a final answer

## Available Team

- **investigador**: Research, data gathering, fact-checking
- **legal**: Legal analysis, compliance review
- **writer**: Content creation, documentation

## Task Creation

Always use this exact format:
```bash
hermes kanban create \
  --assignee <specialist> \
  --title "<concise title>" \
  --body "<detailed instructions>" \
  --json
```
```

Edit `~/.hermes/profiles/investigador/SOUL.md`:

```markdown
# Research Specialist

You execute research tasks assigned via kanban.

When you receive a task:
1. Read the task body for full context
2. Use available tools (search, filesystem) to gather information
3. Complete with a detailed summary:
   ```bash
   hermes kanban complete <task_id> --summary "<findings>"
   ```
```

### 3. Configure Skills in War Room UI

1. Navigate to `/team`
2. Click the operative's badge
3. Click "Retrain"
4. Enable skills:
   - Orchestrator: `terminal` (for kanban), `reasoning`
   - Workers: `terminal`, `filesystem`, `search`, `reasoning`, etc.
5. Add MCP servers as needed
6. Save

### 4. Start the Dispatcher

The dispatcher claims `ready` tasks and hands them to workers:

```bash
# In a tmux/screen session
hermes gateway
```

Without the dispatcher, tasks will stay in "ready" state.

## Real Usage Example

### Complete Flow: Research Mission

```typescript
// 1. Frontend: Create mission
const mission = await $fetch('/api/missions/create', {
  method: 'POST',
  body: {
    orchestratorId: 1, // lider
    title: 'Market research for Product X'
  }
})

// 2. Frontend: Send initial brief
const eventSource = new EventSource(
  `/api/missions/${mission.id}/message`,
  {
    method: 'POST',
    body: JSON.stringify({
      content: 'Research our top 3 competitors: pricing, features, and market position'
    })
  }
)

eventSource.addEventListener('tool_call', (event) => {
  const data = JSON.parse(event.data)
  if (data.name === 'terminal' && data.input.includes('kanban create')) {
    console.log('Orchestrator delegating task...')
  }
})

// 3. Backend: Orchestrator creates tasks
// (Automatically intercepted by War Room)
// hermes kanban create --assignee investigador --title "Research Competitor A" --json
// hermes kanban create --assignee investigador --title "Research Competitor B" --json

// 4. Backend: Workers process tasks
// investigador picks up tasks via dispatcher, completes them

// 5. Backend: Auto-nudge when tasks complete
// War Room injects system message:
// "Tasks task_abc123, task_def456 completed. Summarize for the user."

// 6. Frontend: Orchestrator synthesizes response
eventSource.addEventListener('message', (event) => {
  const data = JSON.parse(event.data)
  console.log('Orchestrator:', data.content)
  // "Based on the research, here's what we found about your competitors..."
})
```

### Server-Side Task Watcher

```typescript
// server/utils/taskWatcher.ts
import { db } from './db'
import { watchedTasks, missions } from './schema'

export async function pollWatchedTasks() {
  const watched = await db.select().from(watchedTasks).where(
    eq(watchedTasks.notified, false)
  )
  
  for (const watch of watched) {
    const task = await getKanbanTask(watch.task_id)
    
    if (task.status === 'done' || task.status === 'blocked') {
      // Inject system message into orchestrator session
      const mission = await db.select().from(missions).where(
        eq(missions.id, watch.mission_id)
      ).get()
      
      await sendSystemMessage(mission.acp_session_id, {
        role: 'system',
        content: `Task ${watch.task_id} is now ${task.status}. Summary: ${task.summary}. Please integrate this into your response to the user.`
      })
      
      // Mark as notified
      await db.update(watchedTasks).set({ notified: true }).where(
        eq(watchedTasks.id, watch.id)
      )
    }
  }
}

// Run every 5 seconds
setInterval(pollWatchedTasks, 5000)
```

## Composables (Frontend)

### useMission

```vue
<script setup>
const { mission, messages, sendMessage, loading } = useMission(missionId)

async function briefOrchestrator() {
  await sendMessage('Analyze legal compliance for EU markets')
}
</script>

<template>
  <div>
    <ChatMessage
      v-for="msg in messages"
      :key="msg.id"
      :message="msg"
    />
    <ChatInput @send="sendMessage" :disabled="loading" />
  </div>
</template>
```

### useOperatives

```vue
<script setup>
const { operatives, activeOperatives, refresh } = useOperatives()

const workers = computed(() => 
  activeOperatives.value.filter(op => op.profile_slug !== 'lider')
)
</script>

<template>
  <OperativeWorkstation
    v-for="op in workers"
    :key="op.id"
    :operative="op"
  />
</template>
```

### useKanban

```vue
<script setup>
const { tasks, tasksByStatus, refresh } = useKanban()

const columns = {
  todo: computed(() => tasksByStatus.value.todo),
  ready: computed(() => tasksByStatus.value.ready),
  running: computed(() => tasksByStatus.value.running),
  blocked: computed(() => tasksByStatus.value.blocked)
}
</script>

<template>
  <div class="kanban-board">
    <KanbanColumn
      v-for="(tasks, status) in columns"
      :key="status"
      :title="status"
      :tasks="tasks"
    />
  </div>
</template>
```

## Common Patterns

### Hiring a New Operative

```typescript
// POST /api/operatives/create
export default defineEventHandler(async (event) => {
  const { slug, callsign, cloneFrom } = await readBody(event)
  
  // Shell out to Hermes CLI
  const { stdout } = await execAsync(
    `hermes profile create ${slug} ${cloneFrom ? `--clone ${cloneFrom}` : ''}`
  )
  
  // Register in War Room DB
  const operative = await db.insert(operatives).values({
    profile_slug: slug,
    callsign: callsign || slug.toUpperCase(),
    avatar: randomAvatar(),
    color: randomColor(),
    active: true
  }).returning()
  
  return operative[0]
})
```

### Live Status Updates

```vue
<!-- components/OperativeWorkstation.vue -->
<script setup>
const props = defineProps(['operative'])
const { data: currentTask } = useFetch(`/api/operatives/${props.operative.id}/current-task`, {
  watch: true,
  refreshInterval: 2000 // Poll every 2s
})

const status = computed(() => {
  if (!currentTask.value) return 'Standing by'
  if (currentTask.value.status === 'running') return `Working on: ${currentTask.value.title}`
  if (currentTask.value.status === 'blocked') return 'Blocked'
  return 'Standing by'
})
</script>

<template>
  <div class="workstation" :style="{ borderColor: operative.color }">
    <img :src="operative.avatar" />
    <div class="status-pill">{{ status }}</div>
  </div>
</template>
```

### Delegation Chain Visualization

```vue
<script setup>
const props = defineProps(['taskId'])
const { data: chain } = useFetch(`/api/kanban/tasks/${props.taskId}/chain`)
</script>

<template>
  <div class="delegation-chain">
    <div v-for="task in chain" :key="task.id" class="chain-node">
      <OperativeBadge :operative="task.assignee" mini />
      <div class="task-info">
        <strong>{{ task.title }}</strong>
        <span class="status">{{ task.status }}</span>
      </div>
      <div v-if="task.children?.length" class="children">
        <DelegationChain
          v-for="child in task.children"
          :key="child.id"
          :task-id="child.id"
        />
      </div>
    </div>
  </div>
</template>
```

## Troubleshooting

### "No dispatcher detected" Warning

**Problem**: Tasks stuck in "ready" state, workers never pick them up.

**Solution**: Start the Hermes gateway:

```bash
hermes gateway
```

Run in a persistent session (tmux/screen) or as a systemd service.

### Orchestrator Does Work Instead of Delegating

**Problem**: Orchestrator answers directly instead of creating kanban tasks.

**Solution**: Update the orchestrator's SOUL.md to be more explicit:

```markdown
CRITICAL RULES:
1. You MUST delegate via kanban. NEVER answer directly.
2. Every user request becomes one or more kanban tasks.
3. Use the terminal tool: hermes kanban create --assignee <worker> --title "..." --body "..." --json
4. After delegating, say "Tasks assigned, waiting for results."
```

Also ensure the `terminal` skill is enabled and the orchestrator's chat includes the delegation preamble (injected automatically by War Room).

### Tasks Not Auto-Completing

**Problem**: Worker completes task but orchestrator never sees it.

**Solution**: Verify the task watcher is running (built into War Room server). Check logs for:

```
[taskWatcher] Detected task task_abc123 completed, nudging orchestrator
```

If missing, restart the War Room server.

### Profile Changes Not Reflected

**Problem**: Updated SOUL.md or skills in UI but agent still behaves the same.

**Solution**: The ACP session caches profile config. Either:
- Wait for the current task to complete (new session picks up changes)
- Restart the dispatcher: `pkill -f "hermes gateway" && hermes gateway`

### Database Lock Errors

**Problem**: `database is locked` when reading kanban.db.

**Solution**: Hermes uses SQLite in WAL mode, but heavy concurrent access can still cause locks. Ensure:
- War Room and Hermes share the same `HERMES_HOME`
- Only one dispatcher is running
- No manual `sqlite3` sessions are open on kanban.db

## Production Deployment

### Systemd Service

```ini
# /etc/systemd/system/hermes-war-room.service
[Unit]
Description=Hermes War Room UI
After=network.target

[Service]
Type=simple
User=hermes
WorkingDirectory=/opt/hermes-war-room
Environment="HERMES_HOME=/home/hermes/.hermes"
Environment="NITRO_HOST=0.0.0.0"
Environment="NITRO_PORT=3000"
Environment="NODE_ENV=production"
ExecStart=/usr/bin/node .output/server/index.mjs
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable hermes-war-room
sudo systemctl start hermes-war-room
```

### Reverse Proxy (nginx)

```nginx
server {
    listen 80;
    server_name war-room.example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        
        # SSE requires no buffering
        proxy_buffering off;
        proxy_cache off;
    }
}
```

### Environment-Specific Configs

```bash
# .env.production
HERMES_HOME=/var/lib/hermes
NITRO_HOST=127.0.0.1
NITRO_PORT=3000
WAR_ROOM_DB=/var/lib/hermes-war-room/war-room.db
NODE_ENV=production
```

## Key Files

```
hermes-war-room/
├── server/
│   ├── api/
│   │   ├── missions/          # Mission CRUD + messaging
│   │   ├── operatives/        # Operative management + retrain
│   │   └── kanban/            # Kanban task queries + watch
│   ├── utils/
│   │   ├── db.ts              # War Room SQLite connection
│   │   ├── hermes.ts          # Hermes CLI wrappers
│   │   └── taskWatcher.ts     # Auto-nudge poller
│   └── middleware/
├── components/
│   ├── OperativeWorkstation.vue
│   ├── KanbanBoard.vue
│   ├── MissionChat.vue
│   └── OperativeDossier.vue
├── composables/
│   ├── useMission.ts
│   ├── useOperatives.ts
│   └── useKanban.ts
├── pages/
│   ├── index.vue              # War Room floor
│   ├── team.vue               # Roster/badges
│   └── missions.vue           # Archive
└── data/
    └── war-room.db            # War Room state (not Hermes kanban.db)
```

The War Room reads `~/.hermes/kanban.db` and `~/.hermes/profiles/` directly but never writes to them—writes go through the `hermes` CLI.
