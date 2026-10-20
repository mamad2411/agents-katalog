---
name: domain-engine-integration
description: Wrap stateful domain engines (Tiptap, Univer, Remotion) into first-party OS contracts — engine mount protocols, artifact binding, revision synchronization, export coordination, and Surface↔Engine contracts for the Software Synthesis OS.
triggers: [Tiptap, Univer, Remotion, domain engine, engine mount, engine integration, engine contract, artifact binding engine, revision sync, export coordination, document engine, sheet engine, media engine, email engine]
---

# SKILL: Domain Engine Integration

## Core Principle
Domain engines (Tiptap, Univer, Remotion) are wrapped — never subclassed. Each engine exposes a canonical `EngineAdapter` interface. The OS interacts only with the adapter, never with engine internals. The adapter is responsible for artifact I/O, revision sync, and export.

---

## 1. Universal Engine Adapter Interface

```typescript
// engines/engine-adapter.ts

export interface EngineAdapter<TContent = unknown, TExportOptions = unknown> {
  /** Unique engine identifier */
  readonly engineKind: 'document' | 'sheet' | 'email' | 'media';

  /** Mount the engine into a DOM container. Returns unmount function. */
  mount(container: HTMLElement, options: MountOptions): Promise<() => void>;

  /** Load content from an artifact revision */
  loadRevision(revision: ArtifactRevision): Promise<void>;

  /** Get current content for saving as new revision */
  getContent(): TContent;

  /** Check if content has unsaved changes */
  isDirty(): boolean;

  /** Export content to a specific format */
  export(format: string, options?: TExportOptions): Promise<ExportResult>;

  /** Subscribe to content change events */
  onChange(handler: (content: TContent) => void): () => void;

  /** Set read-only mode */
  setReadOnly(readOnly: boolean): void;

  /** Destroy the engine instance */
  destroy(): void;
}

export interface MountOptions {
  artifactId?: string;
  readOnly?: boolean;
  userId: string;
  collabProvider?: HocuspocusProvider;
  theme?: 'light' | 'dark';
}

export interface ExportResult {
  format: string;
  data: Blob | string;
  mimeType: string;
  filename: string;
}
```

---

## 2. Tiptap Document Engine Adapter

```typescript
// engines/document/tiptap-adapter.ts
import { Editor } from '@tiptap/core';
import StarterKit from '@tiptap/starter-kit';
import Collaboration from '@tiptap/extension-collaboration';
import CollaborationCursor from '@tiptap/extension-collaboration-cursor';
import type { EngineAdapter, MountOptions } from '../engine-adapter';
import * as Y from 'yjs';

export class TiptapAdapter implements EngineAdapter<object, { format: 'html' | 'markdown' | 'json' }> {
  readonly engineKind = 'document' as const;
  private editor: Editor | null = null;
  private ydoc: Y.Doc | null = null;

  async mount(container: HTMLElement, options: MountOptions): Promise<() => void> {
    this.ydoc = options.collabProvider
      ? (options.collabProvider as any).document  // use shared Y.Doc from collab
      : new Y.Doc();

    const extensions = [
      StarterKit.configure({ history: false }),
      Collaboration.configure({ document: this.ydoc }),
    ];

    if (options.collabProvider) {
      extensions.push(
        CollaborationCursor.configure({
          provider: options.collabProvider,
          user: { name: options.userId, color: '#3B82F6' },
        })
      );
    }

    this.editor = new Editor({
      element: container,
      extensions,
      editable: !options.readOnly,
      editorProps: {
        attributes: { class: 'tiptap-editor prose prose-invert max-w-none' },
      },
    });

    return () => this.destroy();
  }

  async loadRevision(revision: ArtifactRevision): Promise<void> {
    if (!this.editor) throw new Error('Editor not mounted');
    if (revision.content_json) {
      this.editor.commands.setContent(revision.content_json);
    } else if (revision.blob_uri) {
      const res = await fetch(revision.blob_uri);
      const html = await res.text();
      this.editor.commands.setContent(html);
    }
  }

  getContent(): object {
    if (!this.editor) throw new Error('Editor not mounted');
    return this.editor.getJSON();
  }

  isDirty(): boolean {
    // Tiptap with Yjs: check if Y.Doc has pending updates
    return this.ydoc?.store.pendingStructs !== null ?? false;
  }

  async export(format: 'html' | 'markdown' | 'json'): Promise<ExportResult> {
    if (!this.editor) throw new Error('Editor not mounted');

    if (format === 'html') {
      const html = this.editor.getHTML();
      return {
        format: 'html',
        data: new Blob([html], { type: 'text/html' }),
        mimeType: 'text/html',
        filename: 'document.html',
      };
    }
    if (format === 'json') {
      const json = JSON.stringify(this.editor.getJSON(), null, 2);
      return {
        format: 'json',
        data: new Blob([json], { type: 'application/json' }),
        mimeType: 'application/json',
        filename: 'document.json',
      };
    }
    throw new Error(`Unsupported export format: ${format}`);
  }

  onChange(handler: (content: object) => void): () => void {
    if (!this.editor) throw new Error('Editor not mounted');
    const fn = () => handler(this.editor!.getJSON());
    this.editor.on('update', fn);
    return () => this.editor?.off('update', fn);
  }

  setReadOnly(readOnly: boolean): void {
    this.editor?.setEditable(!readOnly);
  }

  destroy(): void {
    this.editor?.destroy();
    this.editor = null;
  }
}
```

---

## 3. Univer Sheet Engine Adapter

```typescript
// engines/sheet/univer-adapter.ts
import { Univer, UniverInstanceType, createUniver, defaultTheme } from '@univerjs/core';
import { UniverDocsPlugin } from '@univerjs/docs';
import { UniverSheetsPlugin } from '@univerjs/sheets';
import type { EngineAdapter, MountOptions } from '../engine-adapter';

export class UniverSheetAdapter implements EngineAdapter<object> {
  readonly engineKind = 'sheet' as const;
  private univer: Univer | null = null;
  private workbookId: string | null = null;

  async mount(container: HTMLElement, options: MountOptions): Promise<() => void> {
    const { univerAPI } = createUniver({
      locale: LocaleType.EN_US,
      theme: options.theme === 'dark' ? darkTheme : defaultTheme,
      plugins: [UniverSheetsPlugin, UniverRenderEnginePlugin, UniverUIPlugin],
    });

    this.univer = univerAPI;

    const workbook = univerAPI.createUniverSheet({
      id: options.artifactId ?? `sheet_${Date.now()}`,
      sheetOrder: ['sheet1'],
      sheets: {
        sheet1: { id: 'sheet1', name: 'Sheet 1', cellData: {} },
      },
    });

    this.workbookId = workbook.getUnitId();

    // Mount into container
    document.querySelector('#app')?.appendChild(container);

    return () => this.destroy();
  }

  async loadRevision(revision: ArtifactRevision): Promise<void> {
    if (!this.univer || !this.workbookId) throw new Error('Sheet not mounted');
    if (revision.content_json) {
      // Apply snapshot to workbook
      this.univer.createUniverSheet(revision.content_json as IWorkbookData);
    }
  }

  getContent(): object {
    if (!this.univer || !this.workbookId) throw new Error('Sheet not mounted');
    return this.univer.getUniverSheet(this.workbookId)?.save() ?? {};
  }

  isDirty(): boolean {
    return true; // Univer tracks dirty state internally; integrate via command history
  }

  async export(format: 'xlsx' | 'csv' | 'json'): Promise<ExportResult> {
    if (!this.univer || !this.workbookId) throw new Error('Sheet not mounted');
    // Use @univerjs/sheets-export for XLSX
    // Fallback to JSON for now
    const data = JSON.stringify(this.getContent());
    return {
      format,
      data: new Blob([data], { type: 'application/json' }),
      mimeType: 'application/json',
      filename: `sheet.${format}`,
    };
  }

  onChange(handler: (content: object) => void): () => void {
    // Subscribe via Univer command bus
    const disposable = this.univer?.onCommandExecuted(() => handler(this.getContent()));
    return () => disposable?.dispose();
  }

  setReadOnly(readOnly: boolean): void {
    // Use Univer permission service
  }

  destroy(): void {
    this.univer?.dispose();
    this.univer = null;
  }
}
```

---

## 4. Artifact Binding and Revision Sync

```typescript
// engines/artifact-sync.ts

export class EngineArtifactSync {
  private saveTimer: ReturnType<typeof setTimeout> | null = null;
  private adapter: EngineAdapter;
  private artifactId: string;
  private currentRevision: number;

  constructor(adapter: EngineAdapter, artifactId: string, currentRevision: number) {
    this.adapter = adapter;
    this.artifactId = artifactId;
    this.currentRevision = currentRevision;
  }

  /** Start auto-save: save as new revision after N ms of inactivity */
  startAutoSave(debounceMs = 3000) {
    const unsubscribe = this.adapter.onChange(() => {
      if (this.saveTimer) clearTimeout(this.saveTimer);
      this.saveTimer = setTimeout(() => this.save(), debounceMs);
    });
    return unsubscribe;
  }

  async save(): Promise<void> {
    if (!this.adapter.isDirty()) return;

    const content = this.adapter.getContent();
    const nextRevision = this.currentRevision + 1;

    await createArtifactRevision({
      artifactId: this.artifactId,
      revisionNumber: nextRevision,
      contentJson: typeof content === 'object' ? content : null,
      blobUri: null,
    });

    this.currentRevision = nextRevision;
  }

  async loadLatest(): Promise<void> {
    const revision = await getLatestArtifactRevision(this.artifactId);
    if (revision) await this.adapter.loadRevision(revision);
  }

  destroy() {
    if (this.saveTimer) clearTimeout(this.saveTimer);
  }
}
```

---

## 5. Export Coordination

```typescript
// engines/export-coordinator.ts

export async function coordinateExport(
  adapter: EngineAdapter,
  artifactId: string,
  format: string
): Promise<ExportBundle> {
  // 1. Force-save current state as new revision
  const sync = new EngineArtifactSync(adapter, artifactId, 0);
  await sync.save();

  // 2. Request export from engine
  const result = await adapter.export(format);

  // 3. Upload to blob storage
  const blobUri = await uploadExportBlob(result.data, result.mimeType, artifactId, format);

  // 4. Record export in artifact metadata
  await recordArtifactExport(artifactId, { format, blobUri, exportedAt: new Date().toISOString() });

  return {
    artifactId,
    format,
    blobUri,
    mimeType: result.mimeType,
    filename: result.filename,
  };
}
```

---

## 6. Surface↔Engine Contract

The shell-web `EngineRenderer` component bridges the surface plan to the mounted engine:

```typescript
// shell-web/canvas/EngineRenderer.tsx
import { useRef, useEffect } from 'react';
import { getEngineAdapter } from '@/engines/registry';
import { EngineArtifactSync } from '@/engines/artifact-sync';
import { useCollaboration } from '@/hooks/useCollaboration';

export function EngineRenderer({ mount }: { mount: EngineMount }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const adapterRef = useRef<EngineAdapter | null>(null);
  const { provider } = useCollaboration(mount.nodeId);

  useEffect(() => {
    if (!containerRef.current) return;

    const adapter = getEngineAdapter(mount.engineKind);
    adapterRef.current = adapter;

    let syncInstance: EngineArtifactSync | null = null;
    let unmount: (() => void) | null = null;

    (async () => {
      unmount = await adapter.mount(containerRef.current!, {
        artifactId: mount.artifactId,
        readOnly: mount.mountMode === 'panel', // operator mode
        userId: getCurrentUserId(),
        collabProvider: provider ?? undefined,
        theme: 'dark',
      });

      if (mount.artifactId) {
        syncInstance = new EngineArtifactSync(adapter, mount.artifactId, 0);
        await syncInstance.loadLatest();
        syncInstance.startAutoSave();
      }
    })();

    return () => {
      syncInstance?.destroy();
      unmount?.();
      adapter.destroy();
    };
  }, [mount.nodeId, mount.engineKind]);

  return <div ref={containerRef} className="engine-container h-full w-full" />;
}
```

---

## 7. Engine Registry

```typescript
// engines/registry.ts
import { TiptapAdapter } from './document/tiptap-adapter';
import { UniverSheetAdapter } from './sheet/univer-adapter';

const ENGINE_REGISTRY: Record<string, () => EngineAdapter> = {
  document: () => new TiptapAdapter(),
  sheet: () => new UniverSheetAdapter(),
  // email: () => new ReactEmailAdapter(),
  // media: () => new RemotionAdapter(),
};

export function getEngineAdapter(kind: EngineMount['engineKind']): EngineAdapter {
  const factory = ENGINE_REGISTRY[kind];
  if (!factory) throw new Error(`No engine adapter registered for kind: "${kind}"`);
  return factory();
}
```

---

## 8. Checklist

Before integrating a new domain engine:
- [ ] Engine is wrapped in an `EngineAdapter` — OS code never imports engine internals directly
- [ ] `mount()` returns an unmount function — no memory leaks on route change
- [ ] `loadRevision()` handles both `content_json` and `blob_uri` (fallback gracefully)
- [ ] `export()` produces a valid Blob with correct MIME type
- [ ] Auto-save is debounced (min 3s) — never saves on every keystroke
- [ ] `setReadOnly()` is called when surface mode is `operator` or `viewer`
- [ ] Engine adapter is destroyed on component unmount
- [ ] Collaborative sessions use shared Y.Doc from the collab provider — not a separate Y.Doc
- [ ] Export bundles are stored as blob URIs (not inline JSON) for files > 1MB
