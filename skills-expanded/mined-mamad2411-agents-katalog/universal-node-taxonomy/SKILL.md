---
name: universal-node-taxonomy
description: Define the complete, extensible node taxonomy for the Software Synthesis OS — every node type that can represent any software artifact humans have ever built. Nodes are not just workflow steps. They are UI elements, data models, business rules, AI agents, complete applications, domain constructs, and composable capability units. This taxonomy is what makes "all software humans ever built" representable in one graph.
triggers: [node taxonomy, node types, universal nodes, node model, what is a node, node categories, node hierarchy, software taxonomy, composable nodes, everything is a node, node definition model, node kinds]
---

# SKILL: Universal Node Taxonomy

## Core Principle
In most workflow tools a node = a step in a pipeline. In this OS a node = a unit of software capability. A node can be a button, a database table, a pricing rule, a document editor, a video clip, a complete CRM, an AI agent, or a policy gate. Every piece of software humans have ever built can be expressed as a composition of nodes.

---

## 1. The Complete Node Kind Hierarchy

```typescript
// packages/graph-types/src/node-taxonomy.ts

/**
 * TIER 1 — Atomic Nodes (single-responsibility, not composable further)
 * These are the primitives of the OS.
 */
export type AtomicNodeKind =
  | 'data.input'         // Accepts a typed value from user input (form field, upload, etc.)
  | 'data.transform'     // Transforms data from one type to another
  | 'data.filter'        // Filters a dataset by condition
  | 'data.merge'         // Merges two data streams
  | 'data.split'         // Splits data into branches
  | 'logic.condition'    // Boolean decision (if/else branching)
  | 'logic.loop'         // Iterate over a dataset
  | 'logic.delay'        // Time-based pause
  | 'logic.gate'         // Approval or policy gate (blocks until resolved)
  | 'logic.trigger'      // Starts a graph (schedule, webhook, event)
  | 'artifact.create'    // Creates a new artifact
  | 'artifact.read'      // Reads an existing artifact
  | 'artifact.update'    // Updates/revises an artifact
  | 'artifact.export'    // Exports an artifact to a file format
  | 'artifact.share'     // Generates a share link for an artifact
  | 'compute.llm'        // Calls an LLM with a prompt
  | 'compute.embed'      // Generates embeddings
  | 'compute.classify'   // Classifies input into categories
  | 'compute.extract'    // Extracts structured data from unstructured input
  | 'compute.generate'   // Generates content (text, image, audio, video)
  | 'compute.score'      // Scores/ranks a set of items
  | 'ui.card'            // Renders a summary card in the surface
  | 'ui.form'            // Renders a user input form
  | 'ui.button'          // Renders an action button
  | 'ui.status'          // Renders a status indicator
  | 'ui.progress'        // Renders a progress tracker
  | 'ui.chart'           // Renders a data visualization
  | 'ui.table'           // Renders a data table
  | 'ui.notification'    // Renders a notification or alert
  | 'connector.read'     // Reads data from an external API/service
  | 'connector.write'    // Writes data to an external API/service
  | 'connector.trigger'  // Listens for events from external services
  | 'connector.oauth'    // Manages OAuth connection for a service
  | 'secret.bind'        // Binds a named secret to a node input
  | 'metric.count'       // Emits a count metric
  | 'metric.time'        // Emits a timing metric
  | 'audit.log';         // Writes an immutable audit log entry

/**
 * TIER 2 — Engine Nodes (stateful, long-lived, wrap a domain engine)
 * Engine nodes own an artifact and provide a rich editing surface.
 */
export type EngineNodeKind =
  | 'engine.document'    // Rich text document (Tiptap/BlockNote)
  | 'engine.sheet'       // Spreadsheet (Univer)
  | 'engine.slide'       // Presentation (Univer slides)
  | 'engine.email'       // Email composer (React Email)
  | 'engine.form'        // Form builder with schema
  | 'engine.dashboard'   // Dashboard with chart widgets
  | 'engine.canvas'      // Freeform whiteboard (Excalidraw)
  | 'engine.code'        // Code editor with execution
  | 'engine.media.video' // Video timeline (Remotion)
  | 'engine.media.audio' // Audio waveform editor (wavesurfer.js)
  | 'engine.media.image' // Image editor / AI image generation
  | 'engine.chat'        // Chat interface (AI or human)
  | 'engine.knowledge'   // Knowledge base with semantic search
  | 'engine.calendar'    // Calendar and scheduling (Cal.com)
  | 'engine.inbox';      // Message/notification inbox

/**
 * TIER 3 — Compound Nodes (a mini-graph packaged as a single node)
 * Compound nodes are reusable sub-workflows that appear as a single unit on the canvas.
 * They hide internal complexity. A compound node IS a graph internally.
 */
export type CompoundNodeKind =
  | 'compound.approval_flow'    // Multi-step approval with comments
  | 'compound.ai_extractor'     // File → AI extraction → structured dataset
  | 'compound.email_campaign'   // List + template + approval + send
  | 'compound.export_bundle'    // Collect artifacts + render + package
  | 'compound.onboarding_flow'  // Multi-step intake form with conditional branching
  | 'compound.billing_checkout' // Payment capture + confirmation + artifact receipt
  | 'compound.lead_qualifier'   // Enrich + score + route leads
  | 'compound.content_publisher'// Draft + review + schedule + publish
  | 'compound.data_pipeline'    // Import + transform + validate + store
  | 'compound.report_generator';// Data → charts → narrative → export

/**
 * TIER 4 — Agent Nodes (autonomous, LLM-driven, can call other nodes)
 * Agent nodes are goal-directed. They decide what to do next at runtime.
 */
export type AgentNodeKind =
  | 'agent.planner'      // Breaks a goal into sub-tasks
  | 'agent.researcher'   // Searches and synthesizes information
  | 'agent.writer'       // Drafts documents, emails, reports
  | 'agent.reviewer'     // Reviews artifacts and produces feedback
  | 'agent.coder'        // Writes and executes code
  | 'agent.analyst'      // Analyzes data and produces insights
  | 'agent.coordinator'  // Delegates to other agents
  | 'agent.executor'     // Executes a plan by calling connector and engine nodes
  | 'agent.monitor'      // Watches for conditions and triggers actions
  | 'agent.custom';      // User-defined agent with custom system prompt

/**
 * TIER 5 — Application Nodes (entire applications packaged as a node)
 * These are full-featured applications that can appear as a node in a larger graph.
 * They are the highest-level composable unit — software eating software.
 */
export type ApplicationNodeKind =
  | 'app.crm'            // Full CRM: contacts, deals, pipeline, emails
  | 'app.project'        // Project management: tasks, timeline, team
  | 'app.billing'        // Billing: subscriptions, invoices, payment links
  | 'app.helpdesk'       // Support: tickets, knowledge base, SLA
  | 'app.wiki'           // Documentation wiki with permissions
  | 'app.analytics'      // Analytics dashboard with data source bindings
  | 'app.portal'         // External-facing client portal
  | 'app.marketplace'    // Product/service marketplace
  | 'app.booking'        // Appointment booking system
  | 'app.ecommerce'      // E-commerce storefront
  | 'app.cms'            // Content management system
  | 'app.lms'            // Learning management system
  | 'app.hrms'           // HR management system
  | 'app.inventory'      // Inventory and supply chain management
  | 'app.custom';        // User-defined app composed of sub-graphs

/**
 * TIER 6 — Policy / Governance Nodes
 */
export type PolicyNodeKind =
  | 'policy.approval'    // Requires human approval before continuing
  | 'policy.rbac'        // Checks role-based access before action
  | 'policy.budget'      // Blocks if cost exceeds budget
  | 'policy.rate_limit'  // Rate limits an action
  | 'policy.compliance'  // Validates compliance rule (GDPR, HIPAA, etc.)
  | 'policy.schedule'    // Only allows action within a time window
  | 'policy.audit';      // Logs all passes/blocks for audit

// Union of ALL node kinds — every node in the OS is one of these
export type NodeKind =
  | AtomicNodeKind
  | EngineNodeKind
  | CompoundNodeKind
  | AgentNodeKind
  | ApplicationNodeKind
  | PolicyNodeKind;
```

---

## 2. Node Definition Contract (Extended)

```typescript
// packages/graph-types/src/node-definition.ts

export interface NodeDefinition {
  key: string;                            // unique: "engine.document", "connector.gmail.send"
  kind: NodeKind;                         // tier classification
  tier: 1 | 2 | 3 | 4 | 5 | 6;
  packageKey: string;                     // owning package
  
  // Schema
  inputSchema: JSONSchema;
  outputSchema: JSONSchema;
  configSchema?: JSONSchema;             // static config (not runtime bindings)
  requiredInputs: string[];
  
  // Execution
  run?: (ctx: RunContext) => Promise<NodeResult>;   // Tier 1-3
  agent?: AgentDefinition;                           // Tier 4 only
  subGraph?: string;                                  // Tier 5: key of embedded graph template
  policyRules?: PolicyRule[];                         // Tier 6
  
  // UI
  ui: {
    label: string;
    description: string;
    icon: string;
    color?: string;
    tags: string[];
    
    // Canvas appearance
    canvasWidth: 'compact' | 'standard' | 'wide';
    canvasHeight: 'compact' | 'standard' | 'tall' | 'auto';
    
    // Surface behavior
    defaultSurface: SurfaceKind;
    supportedSurfaces: SurfaceKind[];
    operatorVisible: boolean;              // show in operator mode?
    builderOnly: boolean;                  // only visible in builder mode?
    
    // Block composer representation (Tier 1-3 only)
    blockLabel?: string;                   // short label for visual builder
    blockDescription?: string;            // one sentence for visual builder
    blockCategory?: BlockCategory;
    blockPreviewImageUrl?: string;
  };
  
  // Permissions required
  permissions: string[];
  
  // Danger classification
  dangerLevel: 'safe' | 'warning' | 'dangerous';
  dangerReason?: string;
}
```

---

## 3. The Software Coverage Matrix

Every category of software humans have ever built maps to node combinations in this taxonomy:

| Software Category | Primary Node Kinds | Tier |
|---|---|---|
| Word processor | `engine.document` | 2 |
| Spreadsheet | `engine.sheet` | 2 |
| Email client | `engine.inbox` + `engine.email` + `connector.read/write` | 2 |
| CRM | `app.crm` or `engine.document` + `data.*` + `connector.write` | 5 or composed |
| Project management | `app.project` or `compound.*` + `engine.document` + `ui.*` | 5 or composed |
| Billing system | `app.billing` + `connector.stripe.*` + `engine.email` | 5 |
| E-commerce | `app.ecommerce` + `connector.*` + `engine.form` + `artifact.*` | 5 |
| Video editor | `engine.media.video` + `compute.generate` + `artifact.export` | 2 |
| Knowledge base | `engine.knowledge` + `compute.embed` + `ui.table` | 2 |
| Approval workflow | `policy.approval` + `engine.document` + `connector.write` | composed |
| Data pipeline | `compound.data_pipeline` or `data.*` + `connector.*` | 3 or atomic |
| AI chatbot | `engine.chat` + `compute.llm` + `engine.knowledge` | 2+1 |
| Marketing campaign | `compound.email_campaign` + `connector.write` + `artifact.*` | 3 |
| Client portal | `app.portal` or `compound.onboarding_flow` + `ui.*` | 5 or composed |
| Analytics dashboard | `app.analytics` or `engine.dashboard` + `data.*` | 5 or 2 |
| LMS | `app.lms` + `engine.document` + `engine.media.*` + `ui.*` | 5 |
| HR system | `app.hrms` + `policy.approval` + `connector.*` | 5 |
| Code editor + CI | `engine.code` + `agent.coder` + `connector.*` | 2+4 |
| Social media scheduler | `compound.content_publisher` + `connector.write` | 3 |
| Booking system | `engine.calendar` + `connector.write` + `engine.email` | 2 |

---

## 4. Node Composition Rules

```typescript
// packages/graph-types/src/composition-rules.ts

// Rule 1: Tier 5 (Application) nodes contain a full sub-graph
// They expose only a simplified interface to the parent graph
// Internally they are complete graphs with their own nodes, edges, artifacts

// Rule 2: Compound nodes (Tier 3) can be expanded/collapsed on canvas
// Expanding a compound node reveals its internal nodes as an embedded canvas
// Changes to internal nodes propagate back through the compound's output ports

// Rule 3: Agent nodes (Tier 4) can call any Tier 1-3 nodes at runtime
// They receive a NodeCallContext that gives them access to the node executor
// They cannot call other Agent nodes (no agent recursion without explicit permission)

// Rule 4: Policy nodes are evaluated before any node they are upstream of
// A policy node's "block" output must be handled or the graph fails validation

// Rule 5: Application nodes are composed from other packages
// An app.crm is a compound of: engine.document, data.*, connector.*, ui.*, engine.form
// The OS can GENERATE application node wrappers from compound package templates

export interface CompoundNodeExpansion {
  compoundNodeId: string;
  internalGraph: CanonicalGraph;   // the full graph inside the compound
  inputMappings: PortMapping[];    // compound input → internal node input
  outputMappings: PortMapping[];   // internal node output → compound output
}

export interface ApplicationNodeManifest {
  appKind: ApplicationNodeKind;
  entryGraph: string;              // key of the graph template that IS this application
  exposedPorts: ExposedPort[];     // what the app exposes to parent graphs
  embeddedPackages: string[];      // packages that compose this application
}
```

---

## 5. Node Palette Configuration by Layer

```typescript
// shell-web/config/node-palette-config.ts

// Guided layer — no node palette shown
export const GUIDED_NODE_PALETTE: null = null;

// Visual builder layer — curated blocks only
// Never exposes raw atomic nodes. Only compound + engine + application.
export const VISUAL_BUILDER_PALETTE_TIERS = [2, 3, 5] as const;  // engine, compound, app only
export const VISUAL_BUILDER_MAX_VISIBLE = 20;  // strict cap

// Canvas layer — full node palette
export const CANVAS_PALETTE_ALL_TIERS = [1, 2, 3, 4, 5, 6] as const;
// But grouped and searchable — not a flat list
export const CANVAS_PALETTE_GROUPS = [
  { label: 'Data', tiers: [1], kinds: ['data.*', 'artifact.*'] },
  { label: 'Logic', tiers: [1], kinds: ['logic.*', 'policy.*'] },
  { label: 'Engines', tiers: [2], kinds: ['engine.*'] },
  { label: 'Composites', tiers: [3], kinds: ['compound.*'] },
  { label: 'AI Agents', tiers: [4], kinds: ['agent.*'] },
  { label: 'Applications', tiers: [5], kinds: ['app.*'] },
  { label: 'Connectors', tiers: [1], kinds: ['connector.*'] },
  { label: 'UI', tiers: [1], kinds: ['ui.*'] },
];
```

---

## 6. Checklist

- [ ] All 6 node tiers defined in `packages/graph-types/src/node-taxonomy.ts`
- [ ] Every first-party package maps its nodes to a specific tier and kind
- [ ] Visual builder palette only exposes Tier 2, 3, 5 nodes (never raw atomics)
- [ ] Compound nodes support expand/collapse on canvas
- [ ] Application nodes contain a full embedded graph (not just a wrapper stub)
- [ ] Agent nodes receive a `NodeCallContext` with access to Tier 1-3 node executor
- [ ] Policy nodes are validated at graph compile time (not only at runtime)
- [ ] Node search supports filtering by tier, kind, category, and text
- [ ] Every node has a `blockLabel` and `blockDescription` for visual builder display
- [ ] Software coverage matrix maps to valid node compositions
