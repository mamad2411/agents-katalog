---
name: canvas-diagram-editor-patterns
description: Build high-performance canvas and diagram editors using xyflow and Excalidraw — node positioning algorithms, auto-layout, minimap, zoom/pan optimization, edge routing, selection/multi-select, and collaborative canvas patterns for the Software Synthesis OS graph canvas.
triggers: [xyflow, ReactFlow, canvas editor, diagram editor, node positioning, auto-layout, minimap, zoom pan, edge routing, multi-select, Excalidraw, tldraw, canvas patterns, graph canvas]
---

# SKILL: Canvas / Diagram Editor Patterns (xyflow + Excalidraw)

## Core Principle
The canvas is a view over the graph — it must never own the data. All mutations flow from the canvas to the graph-compiler via patch operations. The canvas reads from Y.Doc (via Yjs binding) and writes patches. Never mutate graph state directly from canvas event handlers.

---

## 1. xyflow Setup with Graph Binding

```typescript
// shell-web/canvas/GraphCanvas.tsx
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  useReactFlow,
  addEdge,
  type Node,
  type Edge,
  type Connection,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { useGraphNodes, useGraphEdges } from '@/hooks/useGraphBinding';
import { useGraphPatch } from '@/hooks/useGraphPatch';
import { nodeTypes } from './node-types';

export function GraphCanvas() {
  const { nodes, edges } = useGraphBinding();       // synced from Y.Doc
  const { patchGraph } = useGraphPatch();
  const [flowNodes, setFlowNodes, onNodesChange] = useNodesState(nodes);
  const [flowEdges, setFlowEdges, onEdgesChange] = useEdgesState(edges);

  // Emit patch when node position changes (drag end only)
  const onNodeDragStop = useCallback((_: React.MouseEvent, node: Node) => {
    patchGraph([{
      op: 'update_node',
      nodeId: node.id,
      changes: { position: { x: node.position.x, y: node.position.y } },
    }]);
  }, [patchGraph]);

  // Emit patch when edge is created
  const onConnect = useCallback((connection: Connection) => {
    const edgeId = `edge_${Date.now()}`;
    patchGraph([{
      op: 'add_edge',
      edge: {
        id: edgeId,
        from: `${connection.source}.${connection.sourceHandle}`,
        to: `${connection.target}.${connection.targetHandle}`,
      },
    }]);
  }, [patchGraph]);

  // Emit patch when node or edge deleted
  const onNodesDelete = useCallback((deleted: Node[]) => {
    patchGraph(deleted.map(n => ({ op: 'remove_node', nodeId: n.id })));
  }, [patchGraph]);

  const onEdgesDelete = useCallback((deleted: Edge[]) => {
    patchGraph(deleted.map(e => ({ op: 'remove_edge', edgeId: e.id })));
  }, [patchGraph]);

  return (
    <ReactFlow
      nodes={flowNodes}
      edges={flowEdges}
      nodeTypes={nodeTypes}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onNodeDragStop={onNodeDragStop}
      onConnect={onConnect}
      onNodesDelete={onNodesDelete}
      onEdgesDelete={onEdgesDelete}
      fitView
      snapToGrid
      snapGrid={[16, 16]}
      deleteKeyCode="Delete"
      multiSelectionKeyCode="Shift"
    >
      <Background gap={16} color="#1e293b" />
      <Controls />
      <MiniMap nodeColor={getNodeColor} zoomable pannable />
    </ReactFlow>
  );
}

function getNodeColor(node: Node): string {
  const colorMap: Record<string, string> = {
    engine: '#3B82F6',
    compound: '#8B5CF6',
    connector: '#10B981',
    policy: '#F59E0B',
    artifact: '#EC4899',
  };
  return colorMap[node.data?.nodeType as string] ?? '#64748B';
}
```

---

## 2. Custom Node Types

```typescript
// shell-web/canvas/node-types/index.ts
import { EngineNode } from './EngineNode';
import { CompoundNode } from './CompoundNode';
import { ConnectorNode } from './ConnectorNode';
import { PolicyNode } from './PolicyNode';
import { ArtifactNode } from './ArtifactNode';

export const nodeTypes = {
  engine: EngineNode,
  compound: CompoundNode,
  connector: ConnectorNode,
  policy: PolicyNode,
  artifact: ArtifactNode,
};

// shell-web/canvas/node-types/EngineNode.tsx
import { Handle, Position, type NodeProps } from '@xyflow/react';

export function EngineNode({ data, selected }: NodeProps) {
  return (
    <div className={`node-engine ${selected ? 'ring-2 ring-blue-400' : ''}`}>
      <Handle type="target" position={Position.Left} />
      <div className="node-header">
        <span className="node-icon">{data.icon}</span>
        <span className="node-label">{data.label}</span>
      </div>
      {data.status && <StatusBadge status={data.status} />}
      <Handle type="source" position={Position.Right} id="output" />
    </div>
  );
}
```

---

## 3. Auto-Layout Algorithms

Use `@dagrejs/dagre` for automatic directed layout.

```typescript
// shell-web/canvas/layout/auto-layout.ts
import dagre from '@dagrejs/dagre';
import type { Node, Edge } from '@xyflow/react';

const NODE_WIDTH = 200;
const NODE_HEIGHT = 80;

export function applyDagreLayout(
  nodes: Node[],
  edges: Edge[],
  direction: 'LR' | 'TB' = 'LR'
): Node[] {
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: direction, ranksep: 80, nodesep: 60 });

  for (const node of nodes) {
    g.setNode(node.id, { width: NODE_WIDTH, height: NODE_HEIGHT });
  }
  for (const edge of edges) {
    g.setEdge(edge.source, edge.target);
  }

  dagre.layout(g);

  return nodes.map(node => {
    const pos = g.node(node.id);
    return {
      ...node,
      position: {
        x: pos.x - NODE_WIDTH / 2,
        y: pos.y - NODE_HEIGHT / 2,
      },
    };
  });
}

// Hook to trigger auto-layout and emit patches
export function useAutoLayout() {
  const { getNodes, getEdges } = useReactFlow();
  const { patchGraph } = useGraphPatch();

  return useCallback(() => {
    const nodes = getNodes();
    const edges = getEdges();
    const laid = applyDagreLayout(nodes, edges);

    const patches: GraphPatch[] = laid.map(n => ({
      op: 'update_node',
      nodeId: n.id,
      changes: { position: n.position },
    }));

    patchGraph(patches);
  }, [getNodes, getEdges, patchGraph]);
}
```

---

## 4. Edge Routing

Use orthogonal edge routing for cleaner diagrams.

```typescript
// shell-web/canvas/edges/OrthogonalEdge.tsx
import { BaseEdge, getStraightPath, type EdgeProps } from '@xyflow/react';

export function OrthogonalEdge({
  sourceX, sourceY, targetX, targetY,
  sourcePosition, targetPosition,
  data, markerEnd,
}: EdgeProps) {
  // Use elbow routing for horizontal graphs
  const midX = (sourceX + targetX) / 2;
  const d = `M ${sourceX},${sourceY} C ${midX},${sourceY} ${midX},${targetY} ${targetX},${targetY}`;

  const isError = data?.typeError;
  const isActive = data?.active;

  return (
    <BaseEdge
      path={d}
      markerEnd={markerEnd}
      style={{
        stroke: isError ? '#EF4444' : isActive ? '#3B82F6' : '#475569',
        strokeWidth: isActive ? 2 : 1.5,
        strokeDasharray: isError ? '5,5' : undefined,
      }}
    />
  );
}

export const edgeTypes = { default: OrthogonalEdge };
```

---

## 5. Zoom / Pan Optimization

```typescript
// shell-web/canvas/GraphCanvas.tsx — performance additions

// 1. Throttle position updates during drag (never on every pixel)
const onNodeDrag = useCallback(
  throttle((_: React.MouseEvent, node: Node) => {
    // Optimistically update local Y.Doc only (not Postgres)
    updateYDocNodePosition(node.id, node.position);
  }, 50), // 20fps max during drag
  []
);

// 2. Virtualize nodes outside viewport
import { useViewport } from '@xyflow/react';

function useVisibleNodes(nodes: Node[]) {
  const { x, y, zoom } = useViewport();
  const PADDING = 200;

  return useMemo(() => {
    const viewWidth = window.innerWidth / zoom;
    const viewHeight = window.innerHeight / zoom;
    const left = -x / zoom - PADDING;
    const top = -y / zoom - PADDING;

    return nodes.filter(n =>
      n.position.x >= left &&
      n.position.x <= left + viewWidth + PADDING * 2 &&
      n.position.y >= top &&
      n.position.y <= top + viewHeight + PADDING * 2
    );
  }, [nodes, x, y, zoom]);
}

// 3. Disable heavy renders when zoom < threshold
const { zoom } = useViewport();
const isDetailView = zoom > 0.5;
// Render simplified nodes when zoomed out far
```

---

## 6. Selection and Multi-Select

```typescript
// shell-web/canvas/selection/SelectionManager.tsx
import { useOnSelectionChange, useReactFlow } from '@xyflow/react';

export function useSelectionManager() {
  const { setNodes } = useReactFlow();
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());

  useOnSelectionChange({
    onChange: ({ nodes, edges }) => {
      const ids = new Set([...nodes.map(n => n.id), ...edges.map(e => e.id)]);
      setSelectedIds(ids);
      // Update presence with selected node IDs for collaborators
      updatePresenceSelection([...ids]);
    },
  });

  // Select all nodes in a package
  const selectPackageNodes = useCallback((packageKey: string) => {
    setNodes(nodes => nodes.map(n => ({
      ...n,
      selected: n.data?.package === packageKey,
    })));
  }, [setNodes]);

  // Group selection into compound node
  const groupSelected = useCallback(() => {
    if (selectedIds.size < 2) return;
    patchGraph([{
      op: 'add_node',
      node: createCompoundNode([...selectedIds]),
    }]);
  }, [selectedIds]);

  return { selectedIds, selectPackageNodes, groupSelected };
}
```

---

## 7. Minimap Configuration

```typescript
// Configurable minimap with node type coloring
<MiniMap
  nodeColor={(node) => {
    const colors: Record<string, string> = {
      engine: '#3B82F6',
      compound: '#8B5CF6',
      connector: '#10B981',
      policy: '#F59E0B',
    };
    return colors[node.data?.nodeType as string] ?? '#64748B';
  }}
  nodeStrokeWidth={2}
  zoomable
  pannable
  position="bottom-right"
  style={{ background: '#0F172A', border: '1px solid #1E293B' }}
/>
```

---

## 8. Excalidraw Whiteboard Mode

For freeform brainstorming mode (not graph execution):

```typescript
// shell-web/canvas/WhiteboardCanvas.tsx
import { Excalidraw, exportToBlob } from '@excalidraw/excalidraw';

export function WhiteboardCanvas({ graphInstanceId }: { graphInstanceId: string }) {
  const [excalidrawAPI, setExcalidrawAPI] = useState<ExcalidrawAPI | null>(null);

  // Persist whiteboard to artifact (not graph)
  const saveWhiteboard = useCallback(async () => {
    if (!excalidrawAPI) return;
    const elements = excalidrawAPI.getSceneElements();
    const appState = excalidrawAPI.getAppState();

    // Save as artifact revision
    await saveArtifactRevision(graphInstanceId, {
      contentJson: { elements, appState },
      artifactType: 'whiteboard',
    });
  }, [excalidrawAPI, graphInstanceId]);

  return (
    <div style={{ height: '100vh' }}>
      <Excalidraw
        ref={setExcalidrawAPI}
        onChange={debounce(saveWhiteboard, 2000)}
        theme="dark"
        UIOptions={{ canvasActions: { export: false, loadScene: false } }}
      />
    </div>
  );
}
```

---

## 9. Performance Checklist

- [ ] Node drag emits patches on `onNodeDragStop` only — not on every `onNodeDrag` pixel
- [ ] Y.Doc position updates during drag are local only (throttled at 20fps)
- [ ] Nodes outside viewport are not rendered (virtualization hook applied)
- [ ] Custom node components are wrapped in `React.memo`
- [ ] `edgeTypes` and `nodeTypes` objects are defined outside component (stable reference)
- [ ] Auto-layout runs only on explicit user trigger, never on graph load
- [ ] Minimap is `zoomable` and `pannable` — no minimap re-render on every canvas pan
- [ ] Selection state is managed by xyflow's internal state — do NOT mirror into React state
- [ ] Canvas is not re-rendered when only presence/cursor data changes (separate overlay)
