---
name: detail-page-patterns
description: UX patterns for detail/view pages including headers with actions, tabbed content, multi-column layouts, and related data displays
license: MIT
---

# Detail Page UX Patterns

Detail pages display comprehensive information about a single entity with actions, related data, and navigation.

## Page Header Pattern

### Header with Back Navigation and Actions
```tsx
// REQUIRED: Detail page header structure
<PageLayout
  title={item.name}
  subtitle={item.subtitle || item.type}
  backLink="/items"
  backLabel="Back to Items"
  headerContent={
    <div className="flex items-center gap-2">
      <Button variant="secondary" onClick={handleEdit}>
        <EditIcon className="w-4 h-4 mr-1.5" />
        Edit
      </Button>
      <Button variant="danger-outline" onClick={handleDelete}>
        <TrashIcon className="w-4 h-4 mr-1.5" />
        Delete
      </Button>
    </div>
  }
>
  {/* Page content */}
</PageLayout>
```

### Header Button Patterns
| Action | Variant | Icon Position |
|--------|---------|---------------|
| Edit | `secondary` | Left of text |
| Delete | `danger-outline` | Left of text |
| Save | `primary` | Left of text |
| Export | `ghost` | Left of text |
| More Actions | `ghost` | Icon only (kebab) |

## Tabbed Content Navigation

### URL-Synced Tabs
```tsx
interface TabConfig {
  id: string;
  label: string;
  icon?: ReactNode;
  count?: number;
}

function DetailPageTabs({ tabs, activeTab, onTabChange }: {
  tabs: TabConfig[];
  activeTab: string;
  onTabChange: (tabId: string) => void;
}) {
  const router = useRouter();

  // Sync with URL on mount
  useEffect(() => {
    const urlTab = router.query.tab as string;
    if (urlTab && tabs.some(t => t.id === urlTab)) {
      onTabChange(urlTab);
    }
  }, [router.query.tab]);

  const handleTabClick = (tabId: string) => {
    // Update URL without navigation
    router.replace(
      { pathname: router.pathname, query: { ...router.query, tab: tabId } },
      undefined,
      { shallow: true }
    );
    onTabChange(tabId);
  };

  return (
    <div className="border-b border-border mb-6">
      <div className="flex gap-1 -mb-px overflow-x-auto">
        {tabs.map((tab) => {
          const isActive = tab.id === activeTab;
          return (
            <button
              key={tab.id}
              onClick={() => handleTabClick(tab.id)}
              className={`
                flex items-center gap-2 px-4 py-3 text-sm font-medium
                border-b-2 transition-colors whitespace-nowrap
                ${isActive
                  ? 'border-accent text-accent'
                  : 'border-transparent text-text-secondary hover:text-white hover:border-border'
                }
              `}
            >
              {tab.icon}
              {tab.label}
              {tab.count !== undefined && (
                <span className={`
                  px-1.5 py-0.5 text-xs rounded-full
                  ${isActive ? 'bg-accent/20 text-accent' : 'bg-surface-raised text-text-muted'}
                `}>
                  {tab.count}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
```

### Tab Content Rendering
```tsx
// Tab content should lazy-render to avoid unnecessary data fetching
function DetailPage() {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <>
      <DetailPageTabs
        tabs={[
          { id: 'overview', label: 'Overview', icon: <InfoIcon /> },
          { id: 'history', label: 'History', icon: <ClockIcon />, count: 12 },
          { id: 'settings', label: 'Settings', icon: <GearIcon /> },
        ]}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />

      {/* Conditional rendering - only mount active tab */}
      {activeTab === 'overview' && <OverviewTab data={data} />}
      {activeTab === 'history' && <HistoryTab itemId={data.id} />}
      {activeTab === 'settings' && <SettingsTab item={data} />}
    </>
  );
}
```

## Multi-Column Layout

### Sidebar + Main Content
```tsx
// Desktop: Sidebar left, main content right
// Mobile: Stacked vertically
<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
  {/* Sidebar - summary/metadata */}
  <div className="lg:col-span-1 space-y-4">
    <SummaryCard item={item} />
    <MetadataCard item={item} />
    <QuickActionsCard onAction={handleAction} />
  </div>

  {/* Main content - detailed info */}
  <div className="lg:col-span-2 space-y-6">
    <PrimaryContentCard item={item} />
    <RelatedItemsSection itemId={item.id} />
  </div>
</div>
```

### Main Content + Sidebar (Reverse)
```tsx
// For content-heavy pages where main content should come first
<div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
  {/* Main content - 3/4 width */}
  <div className="lg:col-span-3 space-y-6">
    <DetailedContentArea item={item} />
  </div>

  {/* Sidebar - 1/4 width */}
  <div className="lg:col-span-1 space-y-4">
    <StatusCard status={item.status} />
    <RelatedLinksCard links={item.links} />
  </div>
</div>
```

## Summary Card Pattern

### Entity Summary Header
```tsx
function SummaryCard({ item }) {
  return (
    <Card>
      {/* Visual header with avatar/icon */}
      <div className="flex items-start gap-4 mb-4">
        <div className="w-16 h-16 rounded-xl bg-accent/20 flex items-center justify-center">
          <ItemIcon className="w-8 h-8 text-accent" />
        </div>
        <div className="flex-1 min-w-0">
          <h2 className="text-xl font-bold text-white truncate">{item.name}</h2>
          <p className="text-sm text-text-secondary">{item.type}</p>
          <StatusBadge status={item.status} className="mt-2" />
        </div>
      </div>

      {/* Key stats grid */}
      <div className="grid grid-cols-2 gap-3">
        <StatItem label="Created" value={formatDate(item.createdAt)} />
        <StatItem label="Updated" value={formatDate(item.updatedAt)} />
        <StatItem label="Items" value={item.itemCount} />
        <StatItem label="Score" value={`${item.score}%`} />
      </div>
    </Card>
  );
}

function StatItem({ label, value }) {
  return (
    <div className="bg-surface-base/50 rounded-lg p-3">
      <div className="text-xs text-text-muted uppercase tracking-wide mb-1">{label}</div>
      <div className="text-sm font-medium text-white">{value}</div>
    </div>
  );
}
```

## Metadata Display

### Key-Value Metadata List
```tsx
function MetadataCard({ metadata }) {
  return (
    <Card>
      <h3 className="text-sm font-semibold text-white mb-4">Details</h3>
      <dl className="space-y-3">
        {metadata.map(({ label, value, type }) => (
          <div key={label} className="flex justify-between items-start gap-4">
            <dt className="text-sm text-text-secondary flex-shrink-0">{label}</dt>
            <dd className="text-sm text-white text-right">
              {type === 'link' ? (
                <a href={value.href} className="text-accent hover:underline">
                  {value.text}
                </a>
              ) : type === 'badge' ? (
                <Badge variant={value.variant}>{value.text}</Badge>
              ) : (
                value
              )}
            </dd>
          </div>
        ))}
      </dl>
    </Card>
  );
}
```

## Related Items Section

### Related Data with View All
```tsx
function RelatedItemsSection({ items, title, viewAllHref }) {
  const displayItems = items.slice(0, 5);
  const hasMore = items.length > 5;

  return (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        {hasMore && (
          <Link href={viewAllHref} className="text-sm text-accent hover:underline">
            View all ({items.length})
          </Link>
        )}
      </div>

      {items.length === 0 ? (
        <p className="text-sm text-text-secondary py-4 text-center">
          No related items yet
        </p>
      ) : (
        <div className="space-y-2">
          {displayItems.map((item) => (
            <RelatedItemRow key={item.id} item={item} />
          ))}
        </div>
      )}
    </Card>
  );
}

function RelatedItemRow({ item }) {
  return (
    <Link href={`/items/${item.id}`}>
      <a className="flex items-center gap-3 p-2 -mx-2 rounded-lg hover:bg-surface-raised/50 transition-colors group">
        <div className="w-8 h-8 rounded bg-surface-base flex items-center justify-center">
          <ItemIcon className="w-4 h-4 text-text-muted" />
        </div>
        <div className="flex-1 min-w-0">
          <span className="text-sm text-white group-hover:text-accent truncate block">
            {item.name}
          </span>
          <span className="text-xs text-text-muted">{item.type}</span>
        </div>
        <ChevronRightIcon className="w-4 h-4 text-text-muted group-hover:text-accent" />
      </a>
    </Link>
  );
}
```

## Timeline/History Pattern

### Activity Timeline
```tsx
function ActivityTimeline({ activities }) {
  return (
    <div className="relative">
      {/* Vertical line */}
      <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-border" />

      <div className="space-y-6">
        {activities.map((activity, index) => (
          <div key={activity.id} className="relative flex gap-4">
            {/* Timeline dot */}
            <div className={`
              relative z-10 w-8 h-8 rounded-full flex items-center justify-center
              ${activity.type === 'create' ? 'bg-emerald-500/20 text-emerald-400' :
                activity.type === 'update' ? 'bg-blue-500/20 text-blue-400' :
                activity.type === 'delete' ? 'bg-red-500/20 text-red-400' :
                'bg-surface-raised text-text-muted'}
            `}>
              <ActivityIcon type={activity.type} className="w-4 h-4" />
            </div>

            {/* Content */}
            <div className="flex-1 pt-1">
              <p className="text-sm text-white">{activity.description}</p>
              <p className="text-xs text-text-muted mt-1">
                {activity.user} - {formatRelativeTime(activity.timestamp)}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Collapsible Sections

### Expandable Detail Section
```tsx
function CollapsibleSection({ title, icon, defaultOpen = true, children }) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <Card>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 -m-4 mb-0 hover:bg-surface-raised/30 rounded-t-xl transition-colors"
      >
        <div className="flex items-center gap-3">
          {icon && <span className="text-accent">{icon}</span>}
          <h3 className="text-base font-semibold text-white">{title}</h3>
        </div>
        <ChevronDownIcon
          className={`w-5 h-5 text-text-muted transition-transform duration-200 ${
            isOpen ? 'rotate-180' : ''
          }`}
        />
      </button>

      {isOpen && (
        <div className="pt-4 mt-4 border-t border-border">
          {children}
        </div>
      )}
    </Card>
  );
}
```

## Delete Confirmation Flow

### Inline Delete with Confirmation
```tsx
function DeleteAction({ itemName, onDelete }) {
  const [showConfirm, setShowConfirm] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await onDelete();
    } finally {
      setIsDeleting(false);
    }
  };

  if (!showConfirm) {
    return (
      <Button variant="danger-outline" onClick={() => setShowConfirm(true)}>
        <TrashIcon className="w-4 h-4 mr-1.5" />
        Delete
      </Button>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-text-secondary">Delete "{itemName}"?</span>
      <Button
        variant="danger"
        size="sm"
        onClick={handleDelete}
        disabled={isDeleting}
      >
        {isDeleting ? 'Deleting...' : 'Confirm'}
      </Button>
      <Button
        variant="ghost"
        size="sm"
        onClick={() => setShowConfirm(false)}
        disabled={isDeleting}
      >
        Cancel
      </Button>
    </div>
  );
}
```

## Edit Mode Pattern

### Inline Edit vs Modal Edit Decision
| Use Inline Edit | Use Modal Edit |
|-----------------|----------------|
| Single field change | Multiple related fields |
| Simple text/number | Complex form with validation |
| Frequent edits expected | Rare edits |
| No confirmation needed | Needs save/cancel flow |

### Inline Edit Field
```tsx
function InlineEditField({ value, onSave, label }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(value);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isEditing) {
      inputRef.current?.focus();
      inputRef.current?.select();
    }
  }, [isEditing]);

  const handleSave = async () => {
    if (editValue !== value) {
      await onSave(editValue);
    }
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleSave();
    if (e.key === 'Escape') {
      setEditValue(value);
      setIsEditing(false);
    }
  };

  if (!isEditing) {
    return (
      <button
        onClick={() => setIsEditing(true)}
        className="group flex items-center gap-2 text-left"
      >
        <span className="text-white">{value}</span>
        <EditIcon className="w-3 h-3 text-text-muted opacity-0 group-hover:opacity-100" />
      </button>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <input
        ref={inputRef}
        value={editValue}
        onChange={(e) => setEditValue(e.target.value)}
        onKeyDown={handleKeyDown}
        onBlur={handleSave}
        className="bg-surface-base border border-accent rounded px-2 py-1 text-white text-sm"
        aria-label={label}
      />
    </div>
  );
}
```

## Audit Checklist for Detail Pages

### Critical (Must Fix)
- [ ] Has back navigation to parent list - users get trapped
- [ ] Delete has confirmation step - data loss risk
- [ ] Stacks to single column on mobile - mobile users blocked
- [ ] Loading states for async sections - appears broken

### Major (Should Fix)
- [ ] Has appropriate header actions (Edit, Delete) - no way to modify
- [ ] Uses tabs for multiple content sections - overwhelming without organization
- [ ] Tabs sync with URL (shareable) - can't share specific views
- [ ] Multi-column layout on desktop - wasted space
- [ ] Summary card with key stats - key info not visible
- [ ] Empty states for sections with no data - confusing gaps

### Minor (Nice to Have)
- [ ] Metadata displayed in scannable format - readability
- [ ] Related items show count and "view all" - navigation convenience
- [ ] Collapsible sections where appropriate - information density
- [ ] Timeline for history/activity - context for changes
- [ ] Edit flows are clear (inline vs modal) - consistency
