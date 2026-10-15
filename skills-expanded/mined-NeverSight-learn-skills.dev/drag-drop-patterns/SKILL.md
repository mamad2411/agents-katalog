---
name: drag-drop-patterns
description: Drag and drop interactions, visual feedback, drop zones, and reordering patterns
license: MIT
---

# Drag & Drop Patterns

Modern drag-and-drop UI patterns for complex interactions like equipment assignment, panel management, and list reordering. Based on dnd-kit, react-dnd, and WCAG 2.1 accessibility guidelines.

## 1. Drag Initiation

### Drag Handle Pattern
```tsx
interface DraggableItemProps {
  id: string;
  children: React.ReactNode;
}

function DraggableItem({ id, children }: DraggableItemProps) {
  const { attributes, listeners, setNodeRef, isDragging } = useDraggable({ id });
  
  return (
    <div ref={setNodeRef} className={isDragging ? 'opacity-50' : ''}>
      <button {...attributes} {...listeners} className="drag-handle cursor-grab active:cursor-grabbing p-2">
        <GripVertical className="w-4 h-4 text-gray-400" /> {/* ⋮⋮ icon */}
      </button>
      <div>{children}</div>
    </div>
  );
}
```

### Activation Constraints
```tsx
const sensors = useSensors(
  useSensor(MouseSensor, {
    activationConstraint: { distance: 10 } // 10px threshold prevents accidental drags
  }),
  useSensor(TouchSensor, {
    activationConstraint: { delay: 250, tolerance: 5 } // Long press for touch
  })
);
```

## 2. Drag Preview

### Ghost Element with Custom Preview
```tsx
function DragOverlayPreview({ item }: { item: Item }) {
  return (
    <DragOverlay>
      {item ? (
        <div className="bg-white border-2 border-blue-500 rounded-lg shadow-lg p-4 opacity-90">
          {item.name}
          {item.count > 1 && <Badge className="ml-2">{item.count}</Badge>}
        </div>
      ) : null}
    </DragOverlay>
  );
}
```

### Cursor & Visual States
```css
.dragging { opacity: 0.5; transform: scale(0.95); }
.drag-handle { cursor: grab; }
.drag-handle:active { cursor: grabbing; }
```

## 3. Drop Zone Feedback

### Valid/Invalid Drop Zones
```tsx
function DropZone({ id, accepts }: DropZoneProps) {
  const { isOver, setNodeRef } = useDroppable({ id, data: { accepts } });
  const canDrop = useCanDrop(accepts); // Check if active item matches
  
  return (
    <div
      ref={setNodeRef}
      className={cn(
        'min-h-32 rounded-lg border-2 border-dashed transition-colors',
        isOver && canDrop && 'border-green-500 bg-green-50',
        isOver && !canDrop && 'border-red-500 bg-red-50',
        !isOver && 'border-gray-300'
      )}
    >
      {children}
    </div>
  );
}
```

### Cursor Feedback
```tsx
const cursorClass = isOver 
  ? (canDrop ? 'cursor-copy' : 'cursor-not-allowed')
  : 'cursor-default';
```

## 4. Drop Indicators

### Insertion Line Between Items
```tsx
function DropIndicator({ active }: { active: boolean }) {
  if (!active) return null;
  
  return (
    <div className="relative h-0.5 my-2">
      <div className="absolute inset-0 bg-blue-500" />
      <div className="absolute -left-1 -top-1 w-2 h-2 rounded-full bg-blue-500" />
    </div>
  );
}

function SortableList({ items }: { items: Item[] }) {
  const { over } = useDndContext();
  
  return items.map((item, index) => (
    <>
      <DropIndicator active={over?.id === `gap-${index}`} />
      <SortableItem key={item.id} id={item.id} />
    </>
  ));
}
```

### Placeholder for Empty Zones
```tsx
{items.length === 0 && (
  <div className="text-center py-8 text-gray-400">
    Drop items here
  </div>
)}
```

## 5. Drag Constraints

### Axis Locking
```tsx
const restrictToVerticalAxis: Modifier = ({ transform }) => ({
  ...transform,
  x: 0
});

<DndContext modifiers={[restrictToVerticalAxis]}>
```

### Containment & Boundaries
```tsx
import { restrictToWindowEdges, restrictToParentElement } from '@dnd-kit/modifiers';

<DndContext modifiers={[restrictToWindowEdges]}>
```

### Snap to Grid
```tsx
const snapToGrid: Modifier = ({ transform }) => ({
  x: Math.round(transform.x / 20) * 20,
  y: Math.round(transform.y / 20) * 20
});
```

## 6. Multi-Select Drag

### Selected Items State
```tsx
function MultiDraggable({ id, selected }: { id: string; selected: string[] }) {
  const { attributes, listeners, setNodeRef, isDragging } = useDraggable({
    id,
    data: { selectedIds: selected.includes(id) ? selected : [id] }
  });
  
  const count = selected.length > 1 ? selected.length : null;
  
  return (
    <div ref={setNodeRef} className={selected.includes(id) ? 'ring-2 ring-blue-500' : ''}>
      {count && <Badge className="absolute -top-2 -right-2">{count}</Badge>}
      <button {...attributes} {...listeners}>Drag</button>
    </div>
  );
}
```

## 7. Keyboard Alternative [CRITICAL]

### Accessible Reordering
```tsx
const keyboardSensor = useSensor(KeyboardSensor, {
  coordinateGetter: sortableKeyboardCoordinates,
  keyboardCodes: {
    start: ['Space', 'Enter'],
    cancel: ['Escape'],
    end: ['Space', 'Enter'],
    up: ['ArrowUp'],
    down: ['ArrowDown']
  }
});
```

### Screen Reader Instructions
```tsx
<div
  role="button"
  tabIndex={0}
  aria-describedby="drag-instructions"
  {...attributes}
  {...listeners}
>
  <span id="drag-instructions" className="sr-only">
    Press Space to pick up, Arrow keys to move, Space to drop, Escape to cancel
  </span>
</div>
```

## 8. Cancel & Undo

### Escape to Cancel
```tsx
function DragContext() {
  const [items, setItems] = useState(initialItems);
  const [snapshot, setSnapshot] = useState<Item[]>([]);
  
  const handleDragStart = () => setSnapshot([...items]);
  
  const handleDragCancel = () => setItems(snapshot);
  
  return (
    <DndContext onDragStart={handleDragStart} onDragCancel={handleDragCancel}>
  );
}
```

### Undo after Drop
```tsx
const [history, setHistory] = useState<Item[][]>([]);

const handleDragEnd = (event: DragEndEvent) => {
  setHistory(prev => [...prev, items]);
  // Apply changes
};

const undo = () => {
  if (history.length > 0) {
    setItems(history[history.length - 1]);
    setHistory(prev => prev.slice(0, -1));
  }
};
```

## 9. Cross-Container Drag

### Multi-Container Setup
```tsx
function MultiContainer() {
  const containers = ['panel-1', 'panel-2', 'panel-3'];
  
  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over) return;
    
    const activeContainer = findContainer(active.id);
    const overContainer = over.id;
    
    if (activeContainer !== overContainer) {
      moveItemBetweenContainers(active.id, activeContainer, overContainer);
    }
  };
  
  return (
    <DndContext onDragEnd={handleDragEnd}>
      {containers.map(id => (
        <DropZone key={id} id={id} />
      ))}
    </DndContext>
  );
}
```

## 10. Touch Support

### Touch Configuration
```tsx
const touchSensor = useSensor(TouchSensor, {
  activationConstraint: {
    delay: 250,      // Long press 250ms
    tolerance: 5     // Allow 5px movement during press
  }
});
```

### Touch Feedback
```tsx
// Add haptic feedback on touch devices
const handleDragStart = () => {
  if ('vibrate' in navigator) {
    navigator.vibrate(50);
  }
};
```

## 11. Code Examples

### Complete useDragDrop Hook
```tsx
interface UseDragDropOptions {
  items: Item[];
  onReorder: (items: Item[]) => void;
}

function useDragDrop({ items, onReorder }: UseDragDropOptions) {
  const sensors = useSensors(
    useSensor(MouseSensor, { activationConstraint: { distance: 10 } }),
    useSensor(TouchSensor, { activationConstraint: { delay: 250, tolerance: 5 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );
  
  const [activeId, setActiveId] = useState<string | null>(null);
  
  const handleDragStart = (event: DragStartEvent) => setActiveId(event.active.id);
  
  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (over && active.id !== over.id) {
      const oldIndex = items.findIndex(item => item.id === active.id);
      const newIndex = items.findIndex(item => item.id === over.id);
      onReorder(arrayMove(items, oldIndex, newIndex));
    }
    setActiveId(null);
  };
  
  return { sensors, activeId, handleDragStart, handleDragEnd };
}
```

### TypeScript Interfaces
```tsx
interface DragItem {
  id: string;
  type: 'equipment' | 'weapon' | 'module';
  data: unknown;
}

interface DropZoneProps {
  id: string;
  accepts: DragItem['type'][];
  children: React.ReactNode;
  onDrop?: (item: DragItem) => void;
}

interface DragEndEvent {
  active: { id: string; data: { current: DragItem } };
  over: { id: string; data: { current: { accepts: string[] } } } | null;
}
```

## 12. Audit Checklist

### Drag Initiation
- [ ] [MAJOR] Drag handle is clearly visible (icon present)
- [ ] [MAJOR] Activation threshold prevents accidental drags (10px minimum)
- [ ] [MINOR] Cursor changes to `grab` on hover, `grabbing` on drag
- [ ] [MAJOR] Touch requires long-press (250ms minimum)

### Visual Feedback
- [ ] [CRITICAL] Drag preview shows what's being dragged
- [ ] [MAJOR] Original item has reduced opacity during drag (0.5 or less)
- [ ] [MAJOR] Multi-select shows count badge
- [ ] [MINOR] Smooth transitions on drag start/end

### Drop Zones
- [ ] [CRITICAL] Valid drop zones highlighted (border/background change)
- [ ] [CRITICAL] Invalid drop zones show "not-allowed" cursor
- [ ] [MAJOR] Drop indicator shows insertion point (horizontal line)
- [ ] [MINOR] Empty zones show placeholder text

### Keyboard Accessibility
- [ ] [CRITICAL] Space/Enter to pick up and drop
- [ ] [CRITICAL] Arrow keys to move
- [ ] [CRITICAL] Escape to cancel
- [ ] [CRITICAL] Screen reader instructions provided (aria-describedby)
- [ ] [MAJOR] Focus visible during keyboard drag

### Cross-Container
- [ ] [MAJOR] Items can move between containers
- [ ] [MAJOR] Invalid containers reject drops
- [ ] [MINOR] Visual feedback when hovering over target container

### Touch Support
- [ ] [MAJOR] Long-press activates drag on touch (250ms)
- [ ] [MINOR] Haptic feedback on drag start (if supported)
- [ ] [MAJOR] Touch tolerance prevents scroll conflict (5px)

### Cancel & Error Recovery
- [ ] [MAJOR] Escape cancels drag and restores position
- [ ] [MINOR] Undo available after drop
- [ ] [MAJOR] Invalid drops don't corrupt state

### Performance
- [ ] [MINOR] Smooth 60fps drag animation
- [ ] [MINOR] Large lists use virtualization if >100 items
- [ ] [MINOR] Preview uses lightweight component

**Critical Path**: Keyboard accessibility + valid/invalid drop zones + drag preview
**Total Severity Score**: 9 Critical, 11 Major, 8 Minor
