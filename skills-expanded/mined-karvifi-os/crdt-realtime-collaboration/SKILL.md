---
name: crdt-realtime-collaboration
description: Implement real-time collaborative graph editing using Yjs and Hocuspocus — CRDT document model, conflict resolution, presence tracking, cursor synchronization, and operational transforms for the Software Synthesis OS graph canvas.
triggers: [Yjs, Hocuspocus, CRDT, real-time collaboration, collaborative editing, conflict resolution, presence tracking, cursor sync, operational transforms, multiplayer, collaborative graph]
---

# SKILL: CRDT / Real-time Collaboration (Yjs + Hocuspocus)

## Core Principle
The canonical graph lives in Postgres (graph-service). Yjs provides the ephemeral collaborative layer on top. On disconnect or conflict, Yjs awareness state is discarded; the Postgres version wins. Never let Yjs become the source of truth.

---

## 1. Architecture Overview

```
shell-web (browser)
  └── Y.Doc (graph state mirror)
       └── y-websocket provider → Hocuspocus server
                                       └── graph-service (authoritative Postgres)
                                       └── Hocuspocus extensions:
                                             - Auth
                                             - Persistence (Postgres)
                                             - Logger
```

**Key rule:** Hocuspocus persists the Y.Doc to Postgres by converting it to a graph patch and calling graph-service's PATCH endpoint. It does NOT write raw Yjs binary to the canonical store.

---

## 2. Hocuspocus Server Setup

```typescript
// collab-server/server.ts
import { Server } from '@hocuspocus/server';
import { Logger } from '@hocuspocus/extension-logger';
import { Database } from '@hocuspocus/extension-database';
import * as Y from 'yjs';
import { extractGraphPatch } from './graph-sync';
import { verifyCollabToken } from './auth';

export const hocuspocus = Server.configure({
  port: 4000,

  extensions: [
    new Logger({ log: (msg) => console.log('[hocuspocus]', msg) }),

    new Database({
      // Load existing graph into Y.Doc on connect
      async fetch({ documentName }) {
        const [workspaceId, graphInstanceId] = documentName.split(':');
        const graphJson = await fetchGraphFromService(workspaceId, graphInstanceId);
        if (!graphJson) return null;

        const ydoc = new Y.Doc();
        loadGraphIntoYDoc(ydoc, graphJson);
        return Y.encodeStateAsUpdate(ydoc);
      },

      // Persist Y.Doc changes back to graph-service as graph patches
      async store({ documentName, state }) {
        const [workspaceId, graphInstanceId] = documentName.split(':');
        const ydoc = new Y.Doc();
        Y.applyUpdate(ydoc, state);
        const patch = extractGraphPatch(ydoc);
        await patchGraphInService(workspaceId, graphInstanceId, patch);
      },
    }),
  ],

  async onAuthenticate({ token, documentName }) {
    const payload = await verifyCollabToken(token);
    if (!payload) throw new Error('Unauthorized');

    const [workspaceId] = documentName.split(':');
    if (payload.workspaceId !== workspaceId) throw new Error('Forbidden');

    return { userId: payload.userId, roles: payload.roles };
  },

  async onConnect({ documentName, context }) {
    console.log(`User ${context.userId} joined ${documentName}`);
  },
});
```

---

## 3. Y.Doc Structure for Graph

Map the canonical graph document into Yjs types:

```typescript
// collab-server/graph-ydoc.ts
import * as Y from 'yjs';

export function loadGraphIntoYDoc(ydoc: Y.Doc, graph: GraphDocument) {
  const yNodes = ydoc.getMap<Y.Map<unknown>>('nodes');
  const yEdges = ydoc.getMap<Y.Map<unknown>>('edges');
  const yMeta = ydoc.getMap<unknown>('meta');

  ydoc.transact(() => {
    // Load nodes
    for (const node of graph.nodes) {
      const yNode = new Y.Map<unknown>();
      yNode.set('id', node.id);
      yNode.set('type', node.type);
      yNode.set('package', node.package);
      yNode.set('definition', node.definition);
      yNode.set('position', new Y.Map(Object.entries(node.position)));
      yNode.set('config', node.config);
      yNodes.set(node.id, yNode);
    }

    // Load edges
    for (const edge of graph.edges) {
      const yEdge = new Y.Map<unknown>();
      yEdge.set('id', edge.id);
      yEdge.set('from', edge.from);
      yEdge.set('to', edge.to);
      yEdges.set(edge.id, yEdge);
    }

    yMeta.set('graphId', graph.graphId);
    yMeta.set('version', graph.version);
    yMeta.set('name', graph.name);
  });
}

export function extractGraphPatch(ydoc: Y.Doc): GraphPatch[] {
  // Convert Y.Doc current state back to graph patches
  // This runs on every store() call
  const yNodes = ydoc.getMap<Y.Map<unknown>>('nodes');
  const patches: GraphPatch[] = [];

  for (const [nodeId, yNode] of yNodes.entries()) {
    patches.push({
      op: 'update_node',
      nodeId,
      changes: {
        position: Object.fromEntries((yNode.get('position') as Y.Map<number>).entries()),
        config: yNode.get('config') as Record<string, unknown>,
      },
    });
  }

  return patches;
}
```

---

## 4. Browser-side Yjs Provider

```typescript
// shell-web/hooks/useCollaboration.ts
import * as Y from 'yjs';
import { HocuspocusProvider } from '@hocuspocus/provider';
import { useEffect, useRef, useState } from 'react';

export function useCollaboration(workspaceId: string, graphInstanceId: string) {
  const ydocRef = useRef<Y.Doc>(new Y.Doc());
  const [provider, setProvider] = useState<HocuspocusProvider | null>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const docName = `${workspaceId}:${graphInstanceId}`;
    const collabToken = getCollabToken(); // JWT from session

    const p = new HocuspocusProvider({
      url: process.env.NEXT_PUBLIC_COLLAB_WS_URL!,
      name: docName,
      document: ydocRef.current,
      token: collabToken,
      onConnect: () => setConnected(true),
      onDisconnect: () => setConnected(false),
    });

    setProvider(p);
    return () => p.destroy();
  }, [workspaceId, graphInstanceId]);

  return { ydoc: ydocRef.current, provider, connected };
}
```

---

## 5. Presence Tracking

Presence is ephemeral — stored in Yjs awareness, never in Postgres.

```typescript
// shell-web/hooks/usePresence.ts
import { Awareness } from 'y-protocols/awareness';

export interface PresenceState {
  userId: string;
  name: string;
  color: string;
  cursor?: { x: number; y: number };
  selectedNodeIds: string[];
}

export function usePresence(provider: HocuspocusProvider | null, user: User) {
  useEffect(() => {
    if (!provider) return;
    const awareness = provider.awareness as Awareness;

    // Set local presence
    awareness.setLocalStateField('user', {
      userId: user.id,
      name: user.name,
      color: generateUserColor(user.id),
      cursor: null,
      selectedNodeIds: [],
    } satisfies PresenceState);

    return () => awareness.setLocalStateField('user', null);
  }, [provider, user]);

  // Get all remote presences
  const getPresences = (): PresenceState[] => {
    if (!provider) return [];
    const awareness = provider.awareness as Awareness;
    return [...awareness.getStates().entries()]
      .filter(([clientId]) => clientId !== provider.awareness.clientID)
      .map(([, state]) => state.user)
      .filter(Boolean);
  };

  return { getPresences };
}

function generateUserColor(userId: string): string {
  const colors = ['#F87171', '#60A5FA', '#34D399', '#FBBF24', '#A78BFA'];
  const hash = userId.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0);
  return colors[hash % colors.length];
}
```

---

## 6. Cursor Synchronization on Canvas

```typescript
// shell-web/canvas/CollabCursors.tsx
import { usePresence } from '@/hooks/usePresence';
import { useReactFlow } from '@xyflow/react';

export function CollabCursors({ provider }: { provider: HocuspocusProvider }) {
  const { getPresences } = usePresence(provider, useCurrentUser());
  const { screenToFlowPosition } = useReactFlow();
  const [presences, setPresences] = useState<PresenceState[]>([]);

  useEffect(() => {
    const awareness = provider.awareness;
    const update = () => setPresences(getPresences());
    awareness.on('change', update);
    return () => awareness.off('change', update);
  }, [provider]);

  // Update own cursor on mouse move
  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    const pos = screenToFlowPosition({ x: e.clientX, y: e.clientY });
    provider.awareness.setLocalStateField('user', {
      ...provider.awareness.getLocalState()?.user,
      cursor: pos,
    });
  }, [provider]);

  return (
    <div className="collab-cursors-overlay" onMouseMove={handleMouseMove}>
      {presences.map(p => p.cursor && (
        <CollabCursor key={p.userId} presence={p} />
      ))}
    </div>
  );
}
```

---

## 7. Conflict Resolution Strategy

| Scenario | Resolution |
|----------|-----------|
| Two users move same node simultaneously | Last-write-wins on position (CRDT merge) |
| Two users add edge to same port | Both edges added; graph compiler flags type conflict |
| User A deletes node while user B edits it | Delete wins; B sees "node removed" toast |
| Offline user reconnects with stale state | Yjs merges; graph-service validates on next persist |
| Diverged Y.Doc and Postgres state | Postgres wins — reset Y.Doc from authoritative graph |

**Divergence recovery:**
```typescript
// collab-server/divergence-recovery.ts
export async function reconcileYDocWithPostgres(
  ydoc: Y.Doc,
  graphInstanceId: string
) {
  const authoritative = await fetchGraphFromService('', graphInstanceId);
  if (!authoritative) return;

  // Reset Y.Doc completely from Postgres state
  const newDoc = new Y.Doc();
  loadGraphIntoYDoc(newDoc, authoritative);
  const update = Y.encodeStateAsUpdate(newDoc);

  ydoc.transact(() => {
    Y.applyUpdate(ydoc, update);
  });
}
```

---

## 8. Security Rules

- Collab token must be a short-lived JWT (max 1h) signed by api-gateway
- Token must encode `workspaceId` and `userId` — Hocuspocus validates on every connect
- Document names are `workspaceId:graphInstanceId` — validate both parts match token claims
- Awareness state is ephemeral and never persisted — do NOT store cursor positions
- Rate-limit connections per userId (max 5 concurrent collab sessions per user)

---

## 9. Checklist

Before shipping collab features:
- [ ] Hocuspocus `store()` calls graph-service PATCH, never writes raw Yjs binary to Postgres
- [ ] Collab token is validated on every `onAuthenticate` — no anonymous access
- [ ] Y.Doc structure matches canonical graph contract (nodes, edges, meta maps)
- [ ] Presence state never includes sensitive data (no emails, no secrets)
- [ ] Divergence recovery runs if Y.Doc version diverges from Postgres version by > 10
- [ ] Cursor updates are throttled to 30fps max
- [ ] Hocuspocus has a connection limit per document (default: 50, configurable per plan)
- [ ] Collab server is horizontally scalable (Redis pub/sub for multi-instance awareness)
