---
name: surface-compiler
description: Design and implement the surface-compiler service — graph-to-UI compilation, layout planning from graph state, builder vs operator mode transformation, card/panel/editor selection rules, dynamic surface mounting, and artifact binding for the Software Synthesis OS.
triggers: [surface compiler, UI compiler, layout planning, builder mode, operator mode, surface mounting, artifact binding, surface resolution, panel selection, graph to UI, surface-compiler]
---

# SKILL: Surface Compiler (Graph → UI)

## Core Principle
The surface compiler is a pure function: given a graph + workspace mode + installed surface definitions, it produces a declarative surface plan. It does not render. It does not hold state. The shell-web consumes the plan and mounts components.

---

## 1. Compiler Inputs and Outputs

```typescript
// surface-compiler/types.ts

export interface CompileSurfaceInput {
  graph: GraphDocument;
  workspaceMode: 'builder' | 'operator' | 'viewer';
  installedSurfaces: SurfaceDefinition[];
  activeArtifacts: ArtifactRef[];
  userId: string;
  userRoles: string[];
}

export interface SurfacePlan {
  layoutKind: 'split' | 'full' | 'sidebar' | 'canvas' | 'tabbed';
  panels: ResolvedPanel[];
  tabs?: ResolvedTab[];          // used when layoutKind = 'tabbed'
  mountedEngines: EngineMount[];
  boundArtifacts: ArtifactBinding[];
  hiddenNodeIds: string[];       // nodes not surfaced in this mode
}

export interface ResolvedPanel {
  id: string;
  kind: 'editor' | 'card' | 'list' | 'canvas' | 'chat' | 'form' | 'placeholder';
  title: string;
  nodeId?: string;
  width: 'narrow' | 'medium' | 'wide' | 'full';
  collapsible: boolean;
  visible: boolean;
  order: number;
  props: Record<string, unknown>;
}

export interface EngineMount {
  nodeId: string;
  engineKind: 'document' | 'sheet' | 'email' | 'media' | 'canvas';
  packageKey: string;
  artifactId?: string;
  mountMode: 'embedded' | 'fullscreen' | 'panel';
}

export interface ArtifactBinding {
  nodeId: string;
  artifactId: string;
  artifactType: string;
  bindingRole: 'output' | 'input' | 'reference';
}
```

---

## 2. Surface Resolution

Determine which surface definition to use for the current graph state.

```typescript
// surface-compiler/surface-resolver.ts

export function resolveSurface(
  graph: GraphDocument,
  installedSurfaces: SurfaceDefinition[]
): SurfaceDefinition | null {
  // Priority 1: explicit surface defined on graph root (future: graph.surface)
  // Priority 2: surface matching a compound package node present in the graph
  for (const node of graph.nodes) {
    if (node.type === 'compound' && node.surface?.kind) {
      const match = installedSurfaces.find(
        s => s.packageKey === node.package && s.key === node.surface?.kind
      );
      if (match) return match;
    }
  }

  // Priority 3: surface registered by dominant engine node
  const engineNodes = graph.nodes.filter(n => n.type === 'engine');
  if (engineNodes.length === 1) {
    const match = installedSurfaces.find(
      s => s.packageKey === engineNodes[0].package
    );
    if (match) return match;
  }

  // Priority 4: canvas fallback for pure graph/automation workflows
  const hasConnectors = graph.nodes.some(n => n.type === 'connector');
  if (hasConnectors) {
    return CANVAS_FALLBACK_SURFACE;
  }

  return null;
}
```

---

## 3. Layout Planning

Map graph nodes onto panels according to the resolved surface definition.

```typescript
// surface-compiler/layout-planner.ts

export function planLayout(
  graph: GraphDocument,
  surface: SurfaceDefinition,
  mode: CompileSurfaceInput['workspaceMode']
): ResolvedPanel[] {
  const panels: ResolvedPanel[] = [];

  for (const [order, panelSpec] of surface.panels.entries()) {
    const nodeId = panelSpec.nodeRef;
    const node = nodeId ? graph.nodes.find(n => n.id === nodeId) : undefined;

    const visible = isPanelVisibleInMode(panelSpec, mode);
    const kind = selectPanelKind(node, panelSpec, mode);

    panels.push({
      id: panelSpec.id,
      kind,
      title: panelSpec.title ?? node?.surface?.title ?? '',
      nodeId: nodeId,
      width: panelSpec.width ?? 'medium',
      collapsible: panelSpec.collapsible ?? false,
      visible,
      order,
      props: buildPanelProps(node, panelSpec, mode),
    });
  }

  // Add unassigned engine nodes as auto-panels
  const assignedNodeIds = new Set(surface.panels.map(p => p.nodeRef).filter(Boolean));
  for (const node of graph.nodes) {
    if (!assignedNodeIds.has(node.id) && node.type === 'engine') {
      panels.push(buildAutoPanel(node, mode, panels.length));
    }
  }

  return panels.sort((a, b) => a.order - b.order);
}

function selectPanelKind(
  node: NodeDefinition | undefined,
  spec: SurfacePanelSpec,
  mode: string
): ResolvedPanel['kind'] {
  if (!node) return spec.kind;

  // Engine nodes always render as editors
  if (node.type === 'engine') return 'editor';

  // In operator mode: compound nodes show as cards, not canvas
  if (mode === 'operator' && node.type === 'compound') return 'card';

  return spec.kind;
}

function isPanelVisibleInMode(spec: SurfacePanelSpec, mode: string): boolean {
  // Placeholder panels are hidden in operator mode
  if (spec.kind === 'canvas' && mode === 'operator') return false;
  return true;
}

function buildAutoPanel(node: NodeDefinition, mode: string, order: number): ResolvedPanel {
  return {
    id: `auto_${node.id}`,
    kind: node.type === 'engine' ? 'editor' : 'card',
    title: node.surface?.title ?? node.definition,
    nodeId: node.id,
    width: 'medium',
    collapsible: true,
    visible: true,
    order,
    props: {},
  };
}
```

---

## 4. Builder vs Operator Mode Transformation

```typescript
// surface-compiler/mode-transformer.ts

export function applyModeTransformation(
  panels: ResolvedPanel[],
  engineMounts: EngineMount[],
  mode: CompileSurfaceInput['workspaceMode']
): { panels: ResolvedPanel[]; engineMounts: EngineMount[]; hiddenNodeIds: string[] } {
  const hiddenNodeIds: string[] = [];

  if (mode === 'operator') {
    // Operator mode: hide graph topology, promote artifact outputs
    const transformed = panels.map(p => {
      // Hide raw canvas panels
      if (p.kind === 'canvas') {
        hiddenNodeIds.push(p.nodeId ?? '');
        return { ...p, visible: false };
      }
      return p;
    });

    // Operator engine mounts are full-panel, not embedded
    const transformedMounts = engineMounts.map(m => ({
      ...m,
      mountMode: 'panel' as const,
    }));

    return { panels: transformed, engineMounts: transformedMounts, hiddenNodeIds };
  }

  if (mode === 'viewer') {
    // Viewer mode: read-only, no config panels, no empty placeholders
    const transformed = panels
      .filter(p => p.kind !== 'form' || p.nodeId)
      .map(p => ({ ...p, props: { ...p.props, readOnly: true } }));

    return { panels: transformed, engineMounts, hiddenNodeIds };
  }

  // Builder: full access
  return { panels, engineMounts, hiddenNodeIds };
}
```

---

## 5. Engine Mount Resolution

```typescript
// surface-compiler/engine-mounter.ts

const ENGINE_KIND_MAP: Record<string, EngineMount['engineKind']> = {
  'engine.document': 'document',
  'engine.sheet': 'sheet',
  'engine.email': 'email',
  'engine.media': 'media',
};

export function resolveEngineMounts(
  graph: GraphDocument,
  activeArtifacts: ArtifactRef[]
): EngineMount[] {
  const mounts: EngineMount[] = [];

  for (const node of graph.nodes) {
    if (node.type !== 'engine') continue;

    const engineKind = ENGINE_KIND_MAP[node.package];
    if (!engineKind) continue;

    // Find a live artifact bound to this node's output
    const artifactId = activeArtifacts.find(a => a.sourceNodeId === node.id)?.artifactId;

    mounts.push({
      nodeId: node.id,
      engineKind,
      packageKey: node.package,
      artifactId,
      mountMode: 'embedded',
    });
  }

  return mounts;
}
```

---

## 6. Artifact Binding

```typescript
// surface-compiler/artifact-binder.ts

export function bindArtifacts(
  graph: GraphDocument,
  activeArtifacts: ArtifactRef[]
): ArtifactBinding[] {
  const bindings: ArtifactBinding[] = [];
  const artifactMap = new Map(activeArtifacts.map(a => [a.sourceNodeId, a]));

  for (const node of graph.nodes) {
    const artifact = artifactMap.get(node.id);
    if (artifact) {
      bindings.push({
        nodeId: node.id,
        artifactId: artifact.artifactId,
        artifactType: artifact.artifactType,
        bindingRole: 'output',
      });
    }

    // Input bindings from node.inputs
    for (const [, portBinding] of Object.entries(node.inputs)) {
      if (portBinding.binding?.startsWith('artifact:')) {
        const artifactId = portBinding.binding.replace('artifact:', '');
        bindings.push({
          nodeId: node.id,
          artifactId,
          artifactType: 'unknown',
          bindingRole: 'input',
        });
      }
    }
  }

  return bindings;
}
```

---

## 7. Compiler Entrypoint

```typescript
// surface-compiler/index.ts

export async function compileSurface(input: CompileSurfaceInput): Promise<SurfacePlan> {
  // Step 1: resolve surface definition
  const surface = resolveSurface(input.graph, input.installedSurfaces);
  const layoutKind = surface?.layout ?? 'canvas';

  // Step 2: plan layout panels
  const rawPanels = surface
    ? planLayout(input.graph, surface, input.workspaceMode)
    : buildCanvasFallbackPanels(input.graph);

  // Step 3: engine mounts
  const engineMounts = resolveEngineMounts(input.graph, input.activeArtifacts);

  // Step 4: mode transformation
  const { panels, engineMounts: transformedMounts, hiddenNodeIds } =
    applyModeTransformation(rawPanels, engineMounts, input.workspaceMode);

  // Step 5: artifact bindings
  const boundArtifacts = bindArtifacts(input.graph, input.activeArtifacts);

  return {
    layoutKind,
    panels,
    mountedEngines: transformedMounts,
    boundArtifacts,
    hiddenNodeIds,
  };
}
```

---

## 8. Shell-Web Consumption

The shell-web consumes `SurfacePlan` and mounts components declaratively:

```typescript
// shell-web/SurfaceRenderer.tsx
import { useSurfacePlan } from '@/hooks/useSurfacePlan';
import { PanelRenderer } from './PanelRenderer';
import { EngineRenderer } from './EngineRenderer';

export function SurfaceRenderer() {
  const plan = useSurfacePlan(); // fetches from surface-compiler via API

  return (
    <SurfaceLayout kind={plan.layoutKind}>
      {plan.panels.filter(p => p.visible).map(panel => (
        <PanelRenderer key={panel.id} panel={panel} />
      ))}
      {plan.mountedEngines.map(mount => (
        <EngineRenderer key={mount.nodeId} mount={mount} />
      ))}
    </SurfaceLayout>
  );
}
```

---

## 9. Checklist

Before shipping any surface-compiler change:
- [ ] `compileSurface` is a pure function — no DB calls, no side effects
- [ ] Surface resolution priority order is documented and tested with fixtures
- [ ] Operator mode hides all canvas/builder panels — verified with snapshot tests
- [ ] Viewer mode sets `readOnly: true` on all panel props
- [ ] Engine mounts without live artifacts still render (with empty state)
- [ ] Unassigned engine nodes get auto-panels — no silent drops
- [ ] Surface plan is re-compiled on every graph version change (never cached stale)
- [ ] Shell-web renders a loading skeleton if surface plan is not yet available
