---
name: editor-workspace-patterns
description: Multi-tab editors, workspace management, dirty state, real-time validation, and complex editor UIs
license: MIT
---

# Editor & Workspace Patterns

Advanced patterns for building complex editor UIs with multi-tab workspaces, dirty state tracking, real-time validation, and professional workspace management. Designed for applications like code editors, customizers, and configuration tools.

## 1. Multi-Tab Interface

### Tab Structure
```tsx
interface Tab {
  id: string;
  title: string;
  icon?: React.ReactNode;
  isDirty: boolean;
  hasErrors: boolean;
  errorCount: number;
  isActive: boolean;
  canClose: boolean;
}

// Visual representation
// Active tab: bg-background border-b-2 border-primary
// Inactive tab: bg-muted hover:bg-muted/80
<div className="flex items-center gap-1 px-3 py-2">
  {tab.isDirty && <span className="text-primary">●</span>}
  <span>{tab.title}</span>
  {tab.errorCount > 0 && (
    <span className="ml-2 px-1.5 py-0.5 text-xs bg-destructive text-destructive-foreground rounded">
      {tab.errorCount}
    </span>
  )}
  <button className="ml-2 hover:bg-background/50 rounded p-0.5">×</button>
</div>
```

### Tab Overflow Handling
```tsx
const TabList = () => {
  const [showOverflow, setShowOverflow] = useState(false);
  
  return (
    <div className="flex items-center max-w-full">
      <div className="flex-1 overflow-x-auto scrollbar-thin">
        {visibleTabs.map(tab => <Tab key={tab.id} {...tab} />)}
      </div>
      {hasOverflow && (
        <DropdownMenu>
          <DropdownMenuTrigger className="px-2 py-1 hover:bg-muted">
            ⋯
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            {hiddenTabs.map(tab => (
              <DropdownMenuItem key={tab.id}>
                {tab.isDirty && "● "}{tab.title}
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
      )}
    </div>
  );
};
```

### Tab Reordering
Use `@dnd-kit/core` for drag-and-drop tab reordering with visual feedback during drag.

## 2. Dirty State Management

### DirtyStateTracker
```tsx
interface DirtyStateTracker {
  dirtyTabs: Set<string>;
  markDirty(tabId: string): void;
  markClean(tabId: string): void;
  isDirty(tabId: string): boolean;
  hasAnyDirty(): boolean;
}

class WorkspaceDirtyState implements DirtyStateTracker {
  private dirtyTabs = new Set<string>();
  private originalData = new Map<string, unknown>();

  markDirty(tabId: string) {
    this.dirtyTabs.add(tabId);
    window.onbeforeunload = (e) => {
      e.preventDefault();
      return "Unsaved changes";
    };
  }

  markClean(tabId: string) {
    this.dirtyTabs.delete(tabId);
    if (this.dirtyTabs.size === 0) {
      window.onbeforeunload = null;
    }
  }

  async promptSaveOnClose(tabId: string): Promise<'save' | 'discard' | 'cancel'> {
    // Return user choice from dialog
  }
}
```

### Close Tab Flow
```tsx
const handleCloseTab = async (tabId: string) => {
  if (dirtyState.isDirty(tabId)) {
    const choice = await confirmDialog({
      title: "Unsaved Changes",
      description: "Save changes before closing?",
      actions: [
        { label: "Save", value: "save", variant: "default" },
        { label: "Discard", value: "discard", variant: "destructive" },
        { label: "Cancel", value: "cancel", variant: "ghost" }
      ]
    });

    if (choice === 'cancel') return;
    if (choice === 'save') await saveTab(tabId);
  }
  
  removeTab(tabId);
};
```

## 3. Real-Time Validation

### Validation Architecture
```tsx
interface ValidationResult {
  field: string;
  severity: 'error' | 'warning' | 'info';
  message: string;
  path?: string[];
}

interface ValidationSummary {
  errors: ValidationResult[];
  warnings: ValidationResult[];
  isValid: boolean;
}

const useRealtimeValidation = (data: unknown, schema: ZodSchema) => {
  const [validation, setValidation] = useState<ValidationSummary>({
    errors: [],
    warnings: [],
    isValid: true
  });

  useEffect(() => {
    const timer = setTimeout(() => {
      const result = schema.safeParse(data);
      if (!result.success) {
        const errors = result.error.issues.map(issue => ({
          field: issue.path.join('.'),
          severity: 'error' as const,
          message: issue.message,
          path: issue.path as string[]
        }));
        setValidation({ errors, warnings: [], isValid: false });
      } else {
        setValidation({ errors: [], warnings: [], isValid: true });
      }
    }, 300); // Debounce

    return () => clearTimeout(timer);
  }, [data, schema]);

  return validation;
};
```

### Inline Validation Display
```tsx
<div className="space-y-1">
  <Input 
    className={cn(
      validation.errors.length > 0 && "border-destructive",
      validation.warnings.length > 0 && "border-yellow-500"
    )}
  />
  {validation.errors.map((err, i) => (
    <p key={i} className="text-sm text-destructive">{err.message}</p>
  ))}
  {validation.warnings.map((warn, i) => (
    <p key={i} className="text-sm text-yellow-600">{warn.message}</p>
  ))}
</div>
```

## 4. Workspace Layout

### Panel-Based Layout
```tsx
const WorkspaceLayout = () => {
  return (
    <ResizablePanelGroup direction="horizontal">
      <ResizablePanel defaultSize={20} minSize={15} collapsible>
        <Sidebar />
      </ResizablePanel>
      <ResizableHandle />
      <ResizablePanel defaultSize={80}>
        <div className="flex flex-col h-full">
          <TabBar />
          <div className="flex-1 overflow-auto">
            <EditorContent />
          </div>
          <StatusBar />
        </div>
      </ResizablePanel>
    </ResizablePanelGroup>
  );
};
```

### Collapsible Panels
Store panel states in localStorage for persistence across sessions.

## 5. Undo/Redo

### Command Pattern
```tsx
interface Command {
  execute(): void;
  undo(): void;
  redo(): void;
  describe(): string;
}

class UndoStack {
  private history: Command[] = [];
  private currentIndex = -1;

  execute(command: Command) {
    command.execute();
    this.history = this.history.slice(0, this.currentIndex + 1);
    this.history.push(command);
    this.currentIndex++;
  }

  undo() {
    if (this.canUndo()) {
      this.history[this.currentIndex].undo();
      this.currentIndex--;
    }
  }

  redo() {
    if (this.canRedo()) {
      this.currentIndex++;
      this.history[this.currentIndex].redo();
    }
  }

  canUndo() { return this.currentIndex >= 0; }
  canRedo() { return this.currentIndex < this.history.length - 1; }
}
```

### Keyboard Shortcuts
```tsx
useEffect(() => {
  const handler = (e: KeyboardEvent) => {
    if (e.ctrlKey || e.metaKey) {
      if (e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        undoStack.undo();
      } else if (e.key === 'z' && e.shiftKey || e.key === 'y') {
        e.preventDefault();
        undoStack.redo();
      }
    }
  };
  
  window.addEventListener('keydown', handler);
  return () => window.removeEventListener('keydown', handler);
}, []);
```

## 6. Auto-Save Patterns

### Debounced Auto-Save
```tsx
const useAutoSave = (data: unknown, saveFunc: (data: unknown) => Promise<void>) => {
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);

  useEffect(() => {
    const timer = setTimeout(async () => {
      setSaving(true);
      try {
        await saveFunc(data);
        setLastSaved(new Date());
      } catch (error) {
        // Handle conflict or error
        toast.error("Save failed. Please refresh.");
      } finally {
        setSaving(false);
      }
    }, 2000); // 2s debounce

    return () => clearTimeout(timer);
  }, [data, saveFunc]);

  return { saving, lastSaved };
};
```

### Save Indicators
```tsx
<div className="flex items-center gap-2 text-sm text-muted-foreground">
  {saving && (
    <>
      <Loader2 className="w-3 h-3 animate-spin" />
      <span>Saving...</span>
    </>
  )}
  {!saving && lastSaved && (
    <span>Saved {formatDistanceToNow(lastSaved)} ago</span>
  )}
</div>
```

### Conflict Detection
```tsx
const detectConflict = async (docId: string, localVersion: number) => {
  const serverDoc = await fetchDocument(docId);
  if (serverDoc.version > localVersion) {
    // Show conflict resolution dialog
    return true;
  }
  return false;
};
```

## 7. Configuration Tabs

### URL-Synced Tabs
```tsx
const useTabSync = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const activeTab = searchParams.get('tab') || 'general';

  const setActiveTab = (tab: string) => {
    setSearchParams({ tab });
  };

  return [activeTab, setActiveTab] as const;
};
```

### Lazy Loading Tab Content
```tsx
const TabContent = ({ tabId }: { tabId: string }) => {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (!loaded) {
      // Load heavy content only when tab becomes active
      loadTabContent(tabId).then(() => setLoaded(true));
    }
  }, [tabId, loaded]);

  if (!loaded) return <Skeleton />;
  return <ActualContent />;
};
```

### Tab Groups
```tsx
<Tabs>
  <TabsList>
    <TabsGroup label="General">
      <TabsTrigger value="profile">Profile</TabsTrigger>
      <TabsTrigger value="settings">Settings</TabsTrigger>
    </TabsGroup>
    <Separator orientation="vertical" className="h-4" />
    <TabsGroup label="Advanced">
      <TabsTrigger value="api">API</TabsTrigger>
      <TabsTrigger value="integrations">Integrations</TabsTrigger>
    </TabsGroup>
  </TabsList>
</Tabs>
```

## 8. Validation Display

### Error vs Warning Colors
- **Errors (blocking)**: Red/destructive - `border-destructive`, `text-destructive`
- **Warnings (non-blocking)**: Yellow - `border-yellow-500`, `text-yellow-600`
- **Info**: Blue - `border-blue-500`, `text-blue-600`

### Tab Badge with Error Count
```tsx
{tab.errorCount > 0 && (
  <Badge variant="destructive" className="ml-2">
    {tab.errorCount}
  </Badge>
)}
{tab.warningCount > 0 && tab.errorCount === 0 && (
  <Badge variant="outline" className="ml-2 border-yellow-500 text-yellow-600">
    {tab.warningCount}
  </Badge>
)}
```

### Validation Summary Panel
```tsx
<Card>
  <CardHeader>
    <CardTitle>Validation Results</CardTitle>
  </CardHeader>
  <CardContent>
    {validation.errors.length > 0 && (
      <div className="space-y-2">
        <h4 className="text-sm font-medium text-destructive">
          {validation.errors.length} Errors
        </h4>
        {validation.errors.map((err, i) => (
          <button
            key={i}
            onClick={() => jumpToField(err.field)}
            className="block w-full text-left text-sm p-2 hover:bg-muted rounded"
          >
            {err.field}: {err.message}
          </button>
        ))}
      </div>
    )}
  </CardContent>
</Card>
```

## 9. WorkspaceProvider Pattern

```tsx
interface WorkspaceContextValue {
  tabs: Tab[];
  activeTabId: string | null;
  dirtyState: DirtyStateTracker;
  validation: Map<string, ValidationSummary>;
  addTab: (tab: Omit<Tab, 'id'>) => string;
  removeTab: (id: string) => Promise<void>;
  setActiveTab: (id: string) => void;
  saveTab: (id: string) => Promise<void>;
  saveAll: () => Promise<void>;
}

const WorkspaceContext = createContext<WorkspaceContextValue | null>(null);

export const WorkspaceProvider = ({ children }: PropsWithChildren) => {
  const [tabs, setTabs] = useState<Tab[]>([]);
  const [activeTabId, setActiveTabId] = useState<string | null>(null);
  const dirtyState = useMemo(() => new WorkspaceDirtyState(), []);

  const removeTab = async (id: string) => {
    const tab = tabs.find(t => t.id === id);
    if (!tab) return;

    if (dirtyState.isDirty(id)) {
      const choice = await dirtyState.promptSaveOnClose(id);
      if (choice === 'cancel') return;
      if (choice === 'save') await saveTab(id);
    }

    setTabs(prev => prev.filter(t => t.id !== id));
    dirtyState.markClean(id);
  };

  const saveAll = async () => {
    const dirtyTabIds = tabs.filter(t => dirtyState.isDirty(t.id)).map(t => t.id);
    await Promise.all(dirtyTabIds.map(id => saveTab(id)));
  };

  return (
    <WorkspaceContext.Provider value={{ 
      tabs, 
      activeTabId, 
      dirtyState,
      addTab,
      removeTab, 
      setActiveTab, 
      saveTab,
      saveAll 
    }}>
      {children}
    </WorkspaceContext.Provider>
  );
};
```

## 10. Audit Checklist

### Multi-Tab Interface
- [CRITICAL] Tab close button requires confirmation if dirty
- [CRITICAL] Dirty indicator (●) visible on unsaved tabs
- [MAJOR] Error count badge visible on tabs with validation errors
- [MAJOR] Tab overflow handled with dropdown or scroll
- [MINOR] Tab reordering supported via drag-and-drop
- [MINOR] Tab icons displayed for visual identification

### Dirty State Management
- [CRITICAL] Browser unload warning when dirty tabs exist
- [CRITICAL] "Save/Discard/Cancel" dialog on close dirty tab
- [MAJOR] Dirty state persists across component remounts
- [MAJOR] "Save All" action available when multiple tabs dirty
- [MINOR] Dirty state cleared after successful save

### Real-Time Validation
- [CRITICAL] Validation runs on user input (debounced)
- [CRITICAL] Errors prevent save/submit actions
- [MAJOR] Warnings shown but don't block actions
- [MAJOR] Validation messages appear inline near fields
- [MINOR] Validation summary panel shows all issues
- [MINOR] Click validation message jumps to field

### Workspace Layout
- [MAJOR] Panels resizable with visible handles
- [MAJOR] Sidebar collapsible with toggle button
- [MINOR] Panel sizes persist in localStorage
- [MINOR] Responsive layout on smaller screens

### Undo/Redo
- [CRITICAL] Ctrl+Z / Cmd+Z triggers undo
- [CRITICAL] Ctrl+Shift+Z / Cmd+Shift+Z triggers redo
- [MAJOR] Undo/redo buttons disabled when stack empty
- [MINOR] Undo history tooltip shows command description

### Auto-Save
- [MAJOR] Auto-save debounced (1-3 seconds)
- [MAJOR] Save indicator shows "Saving..." and "Saved" states
- [CRITICAL] Conflict detection before auto-save
- [MINOR] Manual save option always available
- [MINOR] Last saved timestamp displayed

### Performance
- [CRITICAL] Tab content lazy-loaded (not all at once)
- [MAJOR] Validation debounced to avoid excessive re-renders
- [MAJOR] Large lists virtualized in editor panels
- [MINOR] Tab switches feel instant (<100ms)

### Accessibility
- [CRITICAL] Keyboard navigation works (Tab, Arrow keys)
- [MAJOR] Focus visible on all interactive elements
- [MAJOR] Screen reader announces tab changes and validation
- [MINOR] Tooltips on icon-only buttons
