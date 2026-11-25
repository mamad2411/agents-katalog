---
name: rete-js
description: Build visual node editors and flow-based programming interfaces using Rete.js v2. Use this skill whenever the user wants to create a node editor, a visual scripting system, a node-based workflow builder, a flow-based programming interface, or any drag-and-drop graph UI in the browser. Also triggers on "Rete.js", "rete-js", "node editor", "node graph", "visual programming", "flow editor", "blueprint editor", "node-based UI", "dataflow graph", "visual workflow", "rete area plugin", "rete engine", "ClassicPreset", "NodeEditor graph", "connect nodes visually", or any request to build an interface where users can create and wire together nodes.
---

# Rete.js v2 - Visual Node Editor

Rete.js (pronounced /ˈriː.ti/, "network" in Italian) is a TypeScript framework for building visual node editors — the kind of interface you see in Blender's shader editor, Unreal Blueprint, or n8n. It manages the data graph plus optional 2D rendering, user interaction, and graph processing.

**Docs**: https://retejs.org/docs  
**Examples**: https://retejs.org/examples  
**Quick start (Rete Kit)**: `npx rete-kit`

> You are working with **Rete.js v2**. The v1 API is completely different — ignore v1 patterns.

---

## The Four-Layer Architecture

Every Rete.js editor is composed of these layers, stacked in order:

```
NodeEditor   ← data layer (nodes & connections as plain objects)
  └─ AreaPlugin   ← 2D canvas (zoom, pan, translate)
       └─ ConnectionPlugin   ← user interaction with wires
       └─ RenderPlugin   ← draws nodes, connections, controls
```

The editor itself is framework-agnostic. The render plugin chooses your UI framework (React, Vue, Angular, Svelte, Lit).

---

## Installation

```bash
# Core (always needed)
npm i rete rete-area-plugin rete-connection-plugin rete-render-utils

# Pick one render plugin
npm i rete-react-plugin styled-components react@19 react-dom@19
# OR: npm i rete-vue-plugin
# OR: npm i rete-angular-plugin@17
# OR: npm i rete-svelte-plugin

# Optional but commonly needed
npm i rete-engine              # dataflow / control flow processing
npm i rete-context-menu-plugin # right-click menu to add/delete nodes
npm i rete-minimap-plugin      # minimap overview
npm i rete-arrange-plugin      # auto-layout nodes (uses elkjs internally)
npm i rete-structures          # advanced graph traversal helpers
npm i rete-history-plugin      # undo/redo
npm i rete-readonly-plugin     # lock editing
```

### CDN (no build step)

```html
<script src="https://cdn.jsdelivr.net/npm/rete/rete.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/rete-area-plugin/rete-area-plugin.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/rete-connection-plugin/rete-connection-plugin.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/rete-react-plugin/rete-react-plugin.min.js"></script>
<!-- Then access via Rete, ReteAreaPlugin, ReteConnectionPlugin, ReteReactPlugin globals -->
```

---

## Complete Setup Example (React)

This is the canonical starting pattern. Every Rete.js editor follows this structure:

```typescript
import { NodeEditor, GetSchemes, ClassicPreset } from "rete";
import { AreaPlugin, AreaExtensions } from "rete-area-plugin";
import { ConnectionPlugin, Presets as ConnectionPresets } from "rete-connection-plugin";
import { ReactPlugin, Presets, ReactArea2D } from "rete-react-plugin";
import { createRoot } from "react-dom/client";

// 1. Define your TypeScript types
type Schemes = GetSchemes<
  ClassicPreset.Node,
  ClassicPreset.Connection<ClassicPreset.Node, ClassicPreset.Node>
>;
type AreaExtra = ReactArea2D<Schemes>;

export async function createEditor(container: HTMLElement) {
  const socket = new ClassicPreset.Socket("socket");

  // 2. Editor — the data layer
  const editor = new NodeEditor<Schemes>();

  // 3. Area — the 2D canvas
  const area = new AreaPlugin<Schemes, AreaExtra>(container);

  // 4. Connection plugin — handles drawing connections on drag
  const connection = new ConnectionPlugin<Schemes, AreaExtra>();
  connection.addPreset(ConnectionPresets.classic.setup());

  // 5. Render plugin — draws everything using React
  const render = new ReactPlugin<Schemes, AreaExtra>({ createRoot });
  render.addPreset(Presets.classic.setup());

  // 6. Wire them together (order matters)
  editor.use(area);
  area.use(connection);
  area.use(render);

  // 7. Enable useful extensions
  AreaExtensions.selectableNodes(area, AreaExtensions.selector(), {
    accumulating: AreaExtensions.accumulateOnCtrl(),
  });
  AreaExtensions.simpleNodesOrder(area); // selected node floats on top

  // 8. Add nodes
  const nodeA = new ClassicPreset.Node("A");
  nodeA.addControl("value", new ClassicPreset.InputControl("text", { initial: "hello" }));
  nodeA.addOutput("out", new ClassicPreset.Output(socket));
  await editor.addNode(nodeA);

  const nodeB = new ClassicPreset.Node("B");
  nodeB.addInput("in", new ClassicPreset.Input(socket));
  await editor.addNode(nodeB);

  // 9. Connect A → B
  await editor.addConnection(new ClassicPreset.Connection(nodeA, "out", nodeB, "in"));

  // 10. Position nodes and fit viewport
  await area.translate(nodeB.id, { x: 300, y: 0 });
  AreaExtensions.zoomAt(area, editor.getNodes());

  // Cleanup function — call this when your component unmounts
  return { destroy: () => area.destroy() };
}
```

### React component wrapper

```tsx
import { useRete } from "rete-react-plugin";

function App() {
  const [ref, editor] = useRete(createEditor);
  return <div ref={ref} style={{ width: "100%", height: "100vh" }} />;
}
```

---

## Nodes, Inputs, Outputs, Controls

### ClassicPreset basics

```typescript
const socket = new ClassicPreset.Socket("number"); // socket type — connections only valid between matching sockets

const node = new ClassicPreset.Node("Add");

// Ports
node.addInput("left",  new ClassicPreset.Input(socket, "Left"));
node.addInput("right", new ClassicPreset.Input(socket, "Right"));
node.addOutput("value", new ClassicPreset.Output(socket, "Value"));

// Built-in controls (renders as <input>)
node.addControl("label", new ClassicPreset.InputControl("text", {
  initial: "hello",   // starting value
  readonly: false,
  change(value) { console.log("changed:", value); }
}));
node.addControl("amount", new ClassicPreset.InputControl("number", { initial: 0 }));

await editor.addNode(node);
```

### Custom node classes (recommended for real projects)

Extend `ClassicPreset.Node` to bundle a node's structure into a reusable class:

```typescript
class AddNode extends ClassicPreset.Node<
  { left: ClassicPreset.Socket; right: ClassicPreset.Socket },
  { value: ClassicPreset.Socket },
  { }
> {
  constructor(socket: ClassicPreset.Socket) {
    super("Add");
    this.addInput("left",  new ClassicPreset.Input(socket, "Left"));
    this.addInput("right", new ClassicPreset.Input(socket, "Right"));
    this.addOutput("value", new ClassicPreset.Output(socket, "Value"));
  }
}

// Use in Schemes
type Node = AddNode | NumberNode;
type Schemes = GetSchemes<Node, ClassicPreset.Connection<Node, Node>>;
```

### Reading/writing graph data

```typescript
editor.getNodes()           // Node[]
editor.getConnections()     // Connection[]
editor.getNode(id)          // Node | undefined
editor.getConnection(id)    // Connection | undefined

await editor.removeNode(node.id);
await editor.removeConnection(connection.id);

// Incoming/outgoing connections for a node
const conns = editor.getConnections();
const incoming = conns.filter(c => c.target === node.id);
const outgoing = conns.filter(c => c.source === node.id);
```

---

## Graph Processing (rete-engine)

The engine lets you evaluate the graph. Two approaches:

### Dataflow (pull-based, like Blender shaders)

Nodes implement a `data()` method. Call `engine.fetch(nodeId)` to pull data from that node and all its predecessors.

```typescript
import { DataflowEngine } from "rete-engine";

class AddNode extends ClassicPreset.Node {
  // ... constructor adds inputs/outputs ...

  data(inputs: { left?: number[][]; right?: number[][] }): { value: number } {
    const left  = (inputs.left?.[0]?.[0])  ?? 0;
    const right = (inputs.right?.[0]?.[0]) ?? 0;
    return { value: left + right };
  }
}

const engine = new DataflowEngine<Schemes>();
editor.use(engine);

// Trigger processing — traverses predecessors automatically
const result = await engine.fetch(outputNode.id);
// result = { value: <computed number> }
```

### Control flow (push-based, like Unreal Blueprints)

Nodes implement `execute()` and call `forward()` to pass control to the next step.

```typescript
import { ControlFlowEngine } from "rete-engine";

class LogNode extends ClassicPreset.Node {
  execute(input: "enter", forward: (output: "exec") => void) {
    console.log("executed!");
    forward("exec"); // pass control onward
  }
}

const engine = new ControlFlowEngine<Schemes>();
editor.use(engine);
engine.execute(startNode.id); // triggers the chain
```

### Hybrid (exec + data ports)

Use both engines on the same graph — exec ports for control, data ports for values:

```typescript
const controlflow = new ControlFlowEngine<Schemes>(node => ({
  inputs:  () => ["exec"],
  outputs: () => ["exec"],
}));
const dataflow = new DataflowEngine<Schemes>(({ inputs, outputs }) => ({
  inputs:  () => Object.keys(inputs).filter(k => k !== "exec"),
  outputs: () => Object.keys(outputs).filter(k => k !== "exec"),
}));
```

---

## Common Plugins

### Context Menu

Right-click to add nodes or delete existing ones:

```typescript
import { ContextMenuPlugin, ContextMenuExtra, Presets as ContextMenuPresets } from "rete-context-menu-plugin";

type AreaExtra = ReactArea2D<Schemes> | ContextMenuExtra;

const contextMenu = new ContextMenuPlugin<Schemes>({
  items: ContextMenuPresets.classic.setup([
    ["Add",    () => new AddNode(socket)],
    ["Number", () => new NumberNode(socket)],
    ["Math", [                               // submenu
      ["Multiply", () => new MultiplyNode(socket)],
    ]],
  ]),
});
area.use(contextMenu);

// Render plugin must also register the context menu preset
render.addPreset(Presets.contextMenu.setup());
```

### Minimap

```typescript
import { MinimapPlugin, MinimapExtra } from "rete-minimap-plugin";

type AreaExtra = ReactArea2D<Schemes> | MinimapExtra;

const minimap = new MinimapPlugin<Schemes>({ boundViewport: true });
area.use(minimap);
render.addPreset(Presets.minimap.setup({ size: 200 }));
```

### Auto-arrange (layout)

```typescript
import { AutoArrangePlugin, Presets as ArrangePresets } from "rete-arrange-plugin";

const arrange = new AutoArrangePlugin<Schemes>();
arrange.addPreset(ArrangePresets.classic.setup());
area.use(arrange);

await arrange.layout(); // auto-positions all nodes
```

### History (undo/redo)

```typescript
import { HistoryPlugin, HistoryExtensions, Presets as HistoryPresets } from "rete-history-plugin";

const history = new HistoryPlugin<Schemes>();
history.addPreset(HistoryPresets.classic.setup());
area.use(history);

// Ctrl+Z / Ctrl+Y keybindings helper
HistoryExtensions.keyboard(history);

// Or call programmatically
await history.undo();
await history.redo();
```

### Readonly

```typescript
import { ReadonlyPlugin } from "rete-readonly-plugin";

const readonly = new ReadonlyPlugin<Schemes>();
// Important: readonly must be used BEFORE other plugins in the chain
editor.use(readonly.root);
area.use(readonly);

readonly.enable();   // lock editing
readonly.disable();  // unlock
```

---

## Node Customization (React)

### Styled nodes

The quickest way to restyle nodes without rebuilding the full component:

```tsx
import { Presets } from "rete-react-plugin";
import { css } from "styled-components";

const redBorderStyle = css<{ selected?: boolean }>`
  background: #1a1a2e;
  ${props => props.selected && css`border-color: #e94560;`}
`;

function StyledNode(props: { data: Schemes["Node"] }) {
  return <Presets.classic.Node styles={() => redBorderStyle} {...props} />;
}

render.addPreset(Presets.classic.setup({
  customize: {
    node(context) {
      if (context.payload instanceof SpecialNode) return StyledNode;
      return Presets.classic.Node; // default for all others
    },
  },
}));
```

### Custom controls

Replace built-in controls with any React component:

```tsx
render.addPreset(Presets.classic.setup({
  customize: {
    control(context) {
      if (context.payload instanceof SliderControl) {
        return ({ data }: { data: SliderControl }) => (
          <input
            type="range"
            min={data.min}
            max={data.max}
            value={data.value}
            onPointerDown={e => e.stopPropagation()} // prevent area from grabbing drag
            onChange={e => data.setValue(+e.target.value)}
          />
        );
      }
      if (context.payload instanceof ClassicPreset.InputControl) {
        return Presets.classic.Control; // keep default for standard controls
      }
    },
  },
}));
```

> Always call `e.stopPropagation()` on `onPointerDown` inside interactive controls, otherwise the area plugin intercepts mouse events.

---

## Import / Export

Rete.js has no built-in serialization — export is a manual process. The recommended pattern:

```typescript
// Export
async function exportGraph(editor: NodeEditor<Schemes>) {
  const nodes = editor.getNodes().map(node => ({
    id: node.id,
    type: node.constructor.name,   // e.g. "AddNode"
    label: node.label,
    position: area.nodeViews.get(node.id)?.position ?? { x: 0, y: 0 },
    controls: Object.fromEntries(
      Object.entries(node.controls).map(([key, ctrl]) => [
        key,
        ctrl instanceof ClassicPreset.InputControl ? ctrl.value : null,
      ])
    ),
  }));

  const connections = editor.getConnections().map(c => ({
    id: c.id, source: c.source, sourceOutput: c.sourceOutput,
    target: c.target, targetInput: c.targetInput,
  }));

  return { nodes, connections };
}

// Import
async function importGraph(data: ReturnType<typeof exportGraph>, editor, area) {
  const nodeMap: Record<string, ClassicPreset.Node> = {};

  for (const saved of data.nodes) {
    const node = createNodeByType(saved.type, saved);  // your factory function
    node.id = saved.id;
    await editor.addNode(node);
    await area.translate(node.id, saved.position);
    nodeMap[saved.id] = node;
  }

  for (const c of data.connections) {
    await editor.addConnection({
      id: c.id,
      source: c.source, sourceOutput: c.sourceOutput,
      target: c.target, targetInput: c.targetInput,
    });
  }
}
```

---

## Advanced Graph Traversal (rete-structures)

For complex graph queries, `rete-structures` is cleaner than manual filtering:

```typescript
import { structures } from "rete-structures";

const graph = structures(editor);

graph.roots()                        // nodes with no incoming connections
graph.leaves()                       // nodes with no outgoing connections
graph.incomers(nodeId)               // directly connected predecessors
graph.outgoers(nodeId)               // directly connected successors
graph.predecessors(nodeId)           // all upstream nodes (recursive)
graph.successors(nodeId)             // all downstream nodes (recursive)
graph.filter(nodePredicate, connPredicate)  // subset of graph
graph.union({ nodes, connections })  // merge two subgraphs
graph.difference({ nodes, connections })    // subtract a subgraph
```

---

## Plugin System (advanced)

All Rete.js objects extend `Scope`, which forms a signal pipeline. Plugins communicate by emitting signals through pipes:

```typescript
// Intercept all node additions
editor.addPipe(context => {
  if (context.type === "nodecreate") {
    console.log("node being added:", context.data);
  }
  return context; // must return context to allow the action; return undefined to cancel
});

// Cancel an action (e.g. prevent removing certain nodes)
editor.addPipe(context => {
  if (context.type === "noderemove" && context.data.id === protectedNodeId) {
    return; // returning undefined blocks the action
  }
  return context;
});
```

---

## TypeScript Cheat Sheet

```typescript
// Minimal schemes (no ClassicPreset)
import { NodeEditor, BaseSchemes } from "rete";
type Schemes = BaseSchemes; // { id: string } nodes, { id, source, target } connections

// ClassicPreset schemes (standard)
import { GetSchemes, ClassicPreset } from "rete";
type Schemes = GetSchemes<ClassicPreset.Node, ClassicPreset.Connection<ClassicPreset.Node, ClassicPreset.Node>>;

// Custom node union schemes
type MyNode = AddNode | NumberNode | OutputNode;
type Schemes = GetSchemes<MyNode, ClassicPreset.Connection<MyNode, MyNode>>;

// AreaExtra — extend when adding plugins that render extra elements
import { ReactArea2D } from "rete-react-plugin";
import { ContextMenuExtra } from "rete-context-menu-plugin";
import { MinimapExtra } from "rete-minimap-plugin";
type AreaExtra = ReactArea2D<Schemes> | ContextMenuExtra | MinimapExtra;
```

---

## Renderer Differences

| Feature | React | Vue | Angular | Svelte | Lit |
|---------|-------|-----|---------|--------|-----|
| Install | `rete-react-plugin` | `rete-vue-plugin` | `rete-angular-plugin` | `rete-svelte-plugin` | `@retejs/lit-plugin` |
| `useRete` hook | ✅ | ✅ | ❌ (use service) | ❌ | ❌ |
| Peer dep | `react react-dom styled-components` | `vue@3` | `@angular/core` | `svelte` | `lit` |

All renderers support the same presets: `classic`, `contextMenu`, `minimap`, `reroute`.

---

## Key Patterns and Pitfalls

- **`addNode` / `addConnection` are async** — always `await` them, especially before reading positions or connecting nodes.
- **Plugin order matters** — add `readonly` before interaction plugins; add `render` after `connection`.
- **`AreaExtra` must include all render-plugins' extras** — missing a type here causes TypeScript errors when adding those plugins.
- **`zoomAt` needs rendered nodes** — call it after nodes are visible on screen, or set `node.width`/`node.height` explicitly.
- **`stopPropagation` in controls** — any interactive element inside a node must call `e.stopPropagation()` on `onPointerDown` to prevent the area plugin from treating it as a drag.
- **Socket compatibility** — connections are only valid between ports that share a socket instance (or the same socket type if you manage it that way). Create one shared socket for compatible ports.
- **Avoid v1 APIs** — v2 has no `Component` class, no `Input` class at top level, no event system like `editor.on('nodecreated')`. Use pipes instead.

---

## How to Integrate Graphology

Rete.js owns the **visual editor layer** — nodes as DOM elements, connections as SVG paths, user interaction. Graphology owns the **data/algorithms layer** — graph structure, traversal, metrics, layouts. They compose cleanly: build the UI in Rete, sync to a Graphology instance, run algorithms, apply results back.

```bash
npm i graphology graphology-dag graphology-shortest-path graphology-metrics graphology-layout-forceatlas2
```

> **Always import by name, not by default.** `import Graph from 'graphology'` imports the base `Graph` class (mixed type, `multi: false`). Be explicit: `import { DirectedGraph } from 'graphology'`.

### One-shot snapshot

Build a Graphology graph from the current Rete editor state:

```typescript
import { DirectedGraph } from 'graphology';

function syncReteToGraphology(editor: NodeEditor<Schemes>): DirectedGraph {
  const graph = new DirectedGraph();

  for (const node of editor.getNodes()) {
    graph.addNode(node.id, { label: node.label });
  }
  for (const conn of editor.getConnections()) {
    // mergeEdge is safe: if two Rete connections share the same source/target
    // node pair (different ports), it updates rather than throwing
    graph.mergeEdge(conn.source, conn.target, {
      reteConnId: conn.id,
      sourceOutput: conn.sourceOutput,
      targetInput: conn.targetInput,
    });
  }

  return graph;
}
```

### Live sync with pipes

Use Rete's pipe system to keep the Graphology graph current as the user edits:

```typescript
import { DirectedGraph } from 'graphology';

const graph = new DirectedGraph();

editor.addPipe(context => {
  switch (context.type) {
    case 'nodecreated':
      graph.mergeNode(context.data.id, { label: context.data.label });
      break;
    case 'noderemoved':
      if (graph.hasNode(context.data.id)) graph.dropNode(context.data.id);
      break;
    case 'connectioncreated': {
      const { source, target, id, sourceOutput, targetInput } = context.data;
      graph.mergeEdge(source, target, { reteConnId: id, sourceOutput, targetInput });
      break;
    }
    case 'connectionremoved': {
      const { source, target, id } = context.data;
      graph.edges(source, target)
        .filter(e => graph.getEdgeAttribute(e, 'reteConnId') === id)
        .forEach(e => graph.dropEdge(e));
      break;
    }
  }
  return context;
});
```

> Use **past-tense** pipe types (`nodecreated`, `connectioncreated`) for sync — they fire after Rete confirms the action. Use **present-tense** types (`nodecreate`, `connectioncreate`) when canceling: returning `undefined` from the pipe blocks the action.

### Prevent cycles before they're drawn

Intercept `connectioncreate` (present-tense, cancelable) to reject connections that would introduce a cycle:

```typescript
import { hasCycle } from 'graphology-dag';

editor.addPipe(context => {
  if (context.type === 'connectioncreate') {
    const { source, target } = context.data;
    // Test on a copy so the real graph is never polluted
    const test = graph.copy() as DirectedGraph;
    test.mergeNode(source);
    test.mergeNode(target);
    test.mergeEdge(source, target);
    if (hasCycle(test)) return; // returning undefined cancels the connection
  }
  return context;
});
```

### Shortest path highlighting

Find a path between two nodes and collect the Rete connection IDs along it:

```typescript
import { bidirectional } from 'graphology-shortest-path';

function getPathConnectionIds(fromId: string, toId: string): Set<string> {
  const path = bidirectional(graph, fromId, toId); // ['a','b','c'] | null
  const ids = new Set<string>();
  if (!path) return ids;

  for (let i = 0; i < path.length - 1; i++) {
    graph.edges(path[i], path[i + 1]).forEach(e => {
      ids.add(graph.getEdgeAttribute(e, 'reteConnId') as string);
    });
  }
  return ids; // use in your render customization to style matching connections
}
```

### Auto-layout: apply ForceAtlas2 positions to Rete nodes

```typescript
import circular from 'graphology-layout/circular';
import forceAtlas2 from 'graphology-layout-forceatlas2';

async function applyForceLayout(
  editor: NodeEditor<Schemes>,
  area: AreaPlugin<Schemes, AreaExtra>
) {
  const g = syncReteToGraphology(editor);
  circular.assign(g); // FA2 requires an initial x/y on every node

  // Raw call — returns a positions map without mutating the graph
  const positions = forceAtlas2(g, {
    iterations: 100,
    settings: forceAtlas2.inferSettings(g),
  });

  // FA2 coordinates are normalized (~±3); scale up for comfortable pixel spacing
  const SCALE = 300;
  for (const node of editor.getNodes()) {
    const pos = positions[node.id];
    if (pos) await area.translate(node.id, { x: pos.x * SCALE, y: pos.y * SCALE });
  }

  AreaExtensions.zoomAt(area, editor.getNodes());
}
```

### Topological sort for Dataflow execution order

For `DataflowEngine` graphs, derive execution order explicitly:

```typescript
import { topologicalSort } from 'graphology-dag';

async function processInOrder(editor: NodeEditor<Schemes>, engine: DataflowEngine<Schemes>) {
  const g = syncReteToGraphology(editor);
  // topologicalSort throws if a cycle exists — guard with hasCycle first if needed
  const order = topologicalSort(g);

  for (const nodeId of order) {
    const result = await engine.fetch(nodeId);
    console.log(nodeId, result);
  }
}
---

## Related Skills

| Skill | How it complements Rete.js |
|---|---|
| **graphology** | Rete.js manages the visual editor layer; Graphology can be the underlying graph data model. Export the Rete editor's nodes and connections to a `graphology` `Graph`, then run algorithms on it — shortest path between two nodes, betweenness centrality to find bottleneck nodes, connected-component detection, or GEXF serialization for persistence. |
| **frontend-design** | Rete.js ships with minimal default styling. The frontend-design skill covers building a polished, distinctive visual identity for your node editor — dark-mode canvas, custom node card designs, accent colors for different node types, and the overall chrome that makes editors feel professional. |
| **css-design** | Custom node, socket, and connection styling in Rete.js is done by overriding CSS. The css-design skill covers CSS custom properties (design tokens for socket colors, node border radii), pseudo-element tricks for connection line styling, container queries for compact vs. expanded node views, and WCAG-compliant focus/hover states for keyboard-accessible editors. |
| **animation-specialist** | Animated node insertion/removal, connection drawing, and layout transitions require `requestAnimationFrame` loops or GSAP tweens applied to Rete's area positions. The animation-specialist skill covers spring dynamics, easing curves, and GSAP timeline patterns useful for making graph mutations feel smooth rather than instantaneous. |
| **web-components** | When using the `@retejs/lit-plugin` renderer, nodes are rendered as Lit-based Web Components. The web-components skill covers Shadow DOM encapsulation, `<slot>` composition, lifecycle callbacks (`connectedCallback`, `attributeChangedCallback`), and CSS-in-shadow patterns essential for building complex custom node renderers without a full framework. |

