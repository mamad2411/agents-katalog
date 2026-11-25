---
name: progressive-disclosure-ux
description: Design the layered UX architecture that makes the Software Synthesis OS accessible to non-technical users while preserving full power for developers. Three-layer progressive disclosure: guided mode (intent only), visual builder (composable blocks), raw canvas (full graph). This is the primary competitive differentiator over n8n, Dify, and ComfyUI.
triggers: [progressive disclosure, non-technical users, guided mode, operator mode, ux layers, blank canvas problem, consumer ux, onboarding intelligence, skill ladder, user experience architecture, accessible workflow, no-code ux]
---

# SKILL: Progressive Disclosure UX Architecture

## Core Principle
The canvas is a power tool. Most users must never need to see it. The OS must have three distinct experience layers. Every user starts at the simplest layer that accomplishes their goal. Complexity is unlocked by choice, never forced.

**Why competitors failed:**
- n8n: blank canvas on signup → 80%+ abandonment
- Dify: AI workflow nodes visible to all users → cognitive overload
- ComfyUI: 400+ node palette default view → designed for ML engineers only

**The rule:** A business user should build a working proposal workspace faster in guided mode than a developer builds one in canvas mode.

---

## 1. The Three Experience Layers

```typescript
// shell-web/types/ux-layers.ts

export type ExperienceLayer = 'guided' | 'visual' | 'canvas';

export interface UserExperienceProfile {
  userId: string;
  defaultLayer: ExperienceLayer;
  unlockedLayers: ExperienceLayer[];
  currentLayer: ExperienceLayer;
  onboardingCompleted: boolean;
  featureDiscoveryState: FeatureDiscoveryState;
}

export interface FeatureDiscoveryState {
  hasCreatedFirstWorkspace: boolean;
  hasInstalledPackage: boolean;
  hasEditedArtifact: boolean;
  hasViewedCanvas: boolean;     // canvas is discovered, not forced
  hasCreatedCustomNode: boolean;
}

// Layer definitions
export const LAYER_DEFINITIONS = {
  guided: {
    label: 'Guided',
    description: 'Describe what you need. The OS builds it.',
    primaryUI: 'intent-bar',       // prominent AI prompt bar
    canvasVisible: false,
    nodeInspectorVisible: false,
    packageBrowserVisible: false,
    showArtifacts: true,
    showApprovals: true,
    showRunStatus: true,
  },
  visual: {
    label: 'Visual Builder',
    description: 'Compose with pre-built blocks and templates.',
    primaryUI: 'block-composer',   // drag blocks, not raw nodes
    canvasVisible: false,          // still no raw canvas
    blockPaletteVisible: true,     // curated block library
    templateGalleryVisible: true,
    nodeInspectorVisible: false,
    showArtifacts: true,
    showApprovals: true,
  },
  canvas: {
    label: 'Canvas',
    description: 'Full graph editor. Every node, every connection.',
    primaryUI: 'xyflow-canvas',
    canvasVisible: true,
    nodeInspectorVisible: true,
    packageBrowserVisible: true,
    rawConfigAccess: true,
  },
} as const;
```

---

## 2. Guided Layer — Intent Bar Architecture

The guided layer is the default for new users. The entire workspace is driven by a single, prominent AI prompt bar.

```typescript
// shell-web/features/guided-mode/IntentBar.tsx
import { useState } from 'react';
import { useIntentMutation } from '@/hooks/useIntentMutation';
import { SuggestionChips } from './SuggestionChips';
import { IntentConfirmDialog } from './IntentConfirmDialog';

export function IntentBar({ workspaceId }: { workspaceId: string }) {
  const [prompt, setPrompt] = useState('');
  const [showConfirm, setShowConfirm] = useState(false);
  const [pendingPlan, setPendingPlan] = useState<IntentPlan | null>(null);
  const { planIntent, isLoading } = useIntentMutation();

  const handleSubmit = async () => {
    if (!prompt.trim()) return;
    const plan = await planIntent({ prompt, workspaceId });
    setPendingPlan(plan);
    setShowConfirm(true);    // always confirm before mutating
  };

  return (
    <div className="intent-bar-container">
      {/* Prominent bar — above everything else in guided mode */}
      <div className="intent-bar">
        <textarea
          placeholder="What do you want to build? e.g. 'Build a proposal workspace that handles RFPs and routes approvals'"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSubmit()}
          className="intent-input"
          rows={2}
        />
        <button onClick={handleSubmit} disabled={isLoading}>
          {isLoading ? 'Planning...' : 'Build →'}
        </button>
      </div>

      {/* Context-aware suggestion chips */}
      <SuggestionChips workspaceId={workspaceId} onSelect={setPrompt} />

      {/* Confirm before applying changes */}
      {pendingPlan && (
        <IntentConfirmDialog
          plan={pendingPlan}
          onConfirm={() => { applyPlan(pendingPlan); setShowConfirm(false); }}
          onCancel={() => setShowConfirm(false)}
        />
      )}
    </div>
  );
}
```

### Suggestion chip generation (context-aware)

```typescript
// shell-web/features/guided-mode/SuggestionChips.tsx

interface Suggestion {
  label: string;
  prompt: string;
  category: 'start' | 'add' | 'automate' | 'export';
  icon: string;
}

// Generate suggestions based on workspace state
function generateSuggestions(
  installedPackages: string[],
  activeArtifacts: ArtifactRef[],
  workspaceActivity: WorkspaceActivity,
): Suggestion[] {
  const suggestions: Suggestion[] = [];

  // If empty workspace — starter prompts
  if (activeArtifacts.length === 0) {
    suggestions.push(
      { label: 'Build a proposal workspace', prompt: 'Build me a proposal workspace to respond to RFPs', category: 'start', icon: '📄' },
      { label: 'Create a report builder', prompt: 'Build a report builder that turns data into a presentation', category: 'start', icon: '📊' },
      { label: 'Set up an outreach campaign', prompt: 'Build an email outreach workspace with approval routing', category: 'start', icon: '✉️' },
      { label: 'Build a client portal', prompt: 'Create a client portal with file sharing and status tracking', category: 'start', icon: '🏢' },
    );
  }

  // If doc artifacts exist — next logical actions
  if (activeArtifacts.some(a => a.type === 'doc')) {
    suggestions.push(
      { label: 'Add approval workflow', prompt: 'Add an approval step before any document is exported', category: 'add', icon: '✅' },
      { label: 'Export as PDF bundle', prompt: 'Add an export step that bundles all documents into a PDF', category: 'export', icon: '📦' },
    );
  }

  // Industry-specific if detectable from workspace name
  // ...

  return suggestions.slice(0, 5);  // max 5 chips visible
}
```

---

## 3. Visual Builder Layer — Block Composer

Between guided and raw canvas. Users see "blocks" not "nodes". Blocks are curated, pre-configured node groups.

```typescript
// shell-web/features/visual-builder/BlockComposer.tsx

interface Block {
  id: string;
  label: string;
  description: string;
  icon: string;
  category: BlockCategory;
  underlyingNodes: string[];       // which graph nodes this block creates
  configSchema: JSONSchema;        // simplified, not the full node config
  previewImageUrl?: string;
}

type BlockCategory = 
  | 'collect'      // intake forms, file upload, data import
  | 'process'      // AI extraction, transforms, calculations
  | 'review'       // approval flows, comments, sign-off
  | 'create'       // docs, sheets, emails, reports
  | 'send'         // email, notifications, webhooks
  | 'export'       // PDF, DOCX, bundles
  | 'connect'      // CRM, Slack, Stripe, calendar
  | 'automate';    // schedule, trigger, repeat

// Block palette — curated, not 400 raw nodes
const BLOCK_LIBRARY: Block[] = [
  {
    id: 'block.rfp_intake',
    label: 'Collect Files',
    description: 'Accept file uploads from users or email',
    icon: '📥',
    category: 'collect',
    underlyingNodes: ['rfp.ingest', 'artifact.create'],
    configSchema: {
      type: 'object',
      properties: {
        allowedFormats: { type: 'array', items: { type: 'string' }, default: ['pdf', 'docx'] },
        label: { type: 'string', default: 'Upload a file' },
      },
    },
  },
  {
    id: 'block.doc_editor',
    label: 'Write a Document',
    description: 'Collaborative rich-text editor with AI assistance',
    icon: '✍️',
    category: 'create',
    underlyingNodes: ['document.workspace'],
    configSchema: {
      type: 'object',
      properties: {
        title: { type: 'string', default: 'Document' },
        seedFromPrior: { type: 'boolean', default: true },
      },
    },
  },
  {
    id: 'block.approval_gate',
    label: 'Require Approval',
    description: 'Block progress until a reviewer signs off',
    icon: '🔐',
    category: 'review',
    underlyingNodes: ['approval.route', 'approval.wait'],
    configSchema: {
      type: 'object',
      properties: {
        approverRole: { type: 'string', enum: ['owner', 'reviewer', 'custom'] },
        message: { type: 'string', default: 'Please review before proceeding' },
      },
    },
  },
  // ...all blocks
];

// The composer renders a visual drag-drop surface over blocks, not nodes
// Blocks connect with simple arrows — no ports visible
export function BlockComposer({ workspaceId }: { workspaceId: string }) {
  return (
    <div className="block-composer">
      <BlockPalette blocks={BLOCK_LIBRARY} />
      <BlockCanvas workspaceId={workspaceId} />
      <BlockInspector />                {/* simplified config, not raw node JSON */}
    </div>
  );
}
```

---

## 4. Layer Transition Architecture

Users move between layers by choice, never by force.

```typescript
// shell-web/features/layer-switcher/LayerSwitcher.tsx

// Rule: switching to canvas preserves EVERYTHING
// Rule: switching back to visual preserves canvas state (synced via graph-service)
// Rule: a guided user who switches to canvas earns "builder" badge — their profile upgrades

export function LayerSwitcher({
  profile,
  onChange,
}: {
  profile: UserExperienceProfile;
  onChange: (layer: ExperienceLayer) => void;
}) {
  const handleUpgrade = (layer: ExperienceLayer) => {
    // One-time discovery announcement before first canvas access
    if (layer === 'canvas' && !profile.unlockedLayers.includes('canvas')) {
      showDiscoveryAnnouncement({
        title: 'You found the Canvas',
        description: 'This is the full graph editor. Everything you built in guided mode is here as a visual graph. You can always switch back.',
        cta: 'Take me to the canvas',
      });
    }
    onChange(layer);
  };

  return (
    <div className="layer-switcher">
      {Object.entries(LAYER_DEFINITIONS).map(([key, def]) => (
        <button
          key={key}
          className={profile.currentLayer === key ? 'active' : ''}
          onClick={() => handleUpgrade(key as ExperienceLayer)}
          disabled={key === 'canvas' && !profile.unlockedLayers.includes('canvas')}
          title={def.description}
        >
          {def.label}
        </button>
      ))}
    </div>
  );
}
```

---

## 5. Onboarding Intelligence — Zero-to-Working in 90 Seconds

The "aha moment" must happen within 90 seconds of signup. This is the engineering target.

```typescript
// shell-web/features/onboarding/OnboardingOrchestrator.ts

interface OnboardingStep {
  id: string;
  condition: (profile: UserExperienceProfile) => boolean;
  action: 'show_prompt' | 'auto_install' | 'highlight_ui' | 'generate_sample';
  payload: Record<string, unknown>;
}

// Auto-onboarding sequence
const ONBOARDING_SEQUENCE: OnboardingStep[] = [
  {
    id: 'welcome_intent',
    condition: (p) => !p.hasCreatedFirstWorkspace,
    action: 'show_prompt',
    payload: {
      prefillPrompt: 'Build me a proposal workspace',
      headline: 'Tell me what you want to build',
      subtext: 'Describe any kind of work you do. I'll set it up in seconds.',
    },
  },
  {
    id: 'auto_demo',
    condition: (p) => !p.hasCreatedFirstWorkspace && p.skippedWelcome,
    action: 'generate_sample',
    payload: {
      samplePackage: 'pkg.proposal.studio',
      message: 'Here's an example to show what's possible.',
    },
  },
  {
    id: 'first_artifact',
    condition: (p) => p.hasCreatedFirstWorkspace && !p.hasEditedArtifact,
    action: 'highlight_ui',
    payload: {
      target: 'first-artifact-card',
      tooltip: 'Your document is ready. Click to open and edit it.',
    },
  },
];

export class OnboardingOrchestrator {
  getNextStep(profile: UserExperienceProfile): OnboardingStep | null {
    return ONBOARDING_SEQUENCE.find(step => step.condition(profile)) ?? null;
  }
}
```

---

## 6. Complexity Revelation Rules

These are non-negotiable product rules:

| Rule | Rationale |
|---|---|
| New workspaces always open in guided mode | Blank canvas kills conversion |
| Canvas mode requires explicit user action to enter | Never shown by default |
| Block palette has max 20 curated blocks | Not 400 nodes like ComfyUI |
| Every block has a one-sentence description | No jargon in guided/visual layers |
| Raw JSON config hidden behind "Advanced" toggle | Available but not default |
| Error messages are in plain English in all layers | "connection failed" not "ECONNREFUSED" |
| "Explain this workspace" always available | AI can describe any graph as plain English |
| Visual builder blocks map 1:1 to valid graph templates | Block actions always succeed — no orphaned config |

---

## 7. Checklist

- [ ] Guided mode (intent bar only) is the default for new users
- [ ] Suggestion chips are context-aware and updated per workspace state
- [ ] Block library is curated — max 20 initial blocks, not 400 nodes
- [ ] Canvas access is discovered by choice, not shown by default
- [ ] Layer transitions are lossless (state preserved both ways)
- [ ] Onboarding reaches "aha moment" within 90 seconds
- [ ] All three layers share the same graph-service backend (no data duplication)
- [ ] Every block in the visual layer maps to a validated graph template
- [ ] Plain-language error messages in guided and visual layers
- [ ] "Explain this workspace" AI endpoint exposed from all layers
