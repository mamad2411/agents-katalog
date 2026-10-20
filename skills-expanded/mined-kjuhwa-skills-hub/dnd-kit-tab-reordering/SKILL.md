---
tags: [design, dnd, kit, tab, reordering]
name: dnd-kit-tab-reordering
description: Implement horizontal tab drag reordering using @dnd-kit/core + @dnd-kit/sortable with PointerSensor and CSS.Transform
category: design
trigger: When adding drag-to-reorder functionality to tabs, lists, or any horizontal sortable UI
version: 1.0.0
source_project: lucida-ui
---

# @dnd-kit Tab Reordering

## Steps

1. **Install dependencies**: `@dnd-kit/core`, `@dnd-kit/sortable`, `@dnd-kit/utilities`

2. **Create DraggableTabNode wrapper**:
   ```tsx
   const DraggableTabNode = ({ id, ...props }) => {
     const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id });
     const style = { transform: CSS.Transform.toString(transform), transition };
     return React.cloneElement(props.children, {
       ref: setNodeRef, style, ...attributes, ...listeners,
     });
   };
   ```

3. **Wrap tab bar with DndContext + SortableContext**:
   ```tsx
   <DndContext sensors={[useSensor(PointerSensor)]} onDragEnd={handleDragEnd}>
     <SortableContext items={tabKeys} strategy={horizontalListSortingStrategy}>
       {tabs.map(tab => <DraggableTabNode key={tab.key} id={tab.key}>{tab.node}</DraggableTabNode>)}
     </SortableContext>
   </DndContext>
   ```

4. **Handle reorder** in `onDragEnd`:
   ```tsx
   const handleDragEnd = ({ active, over }) => {
     if (active.id !== over?.id) {
       setItems(prev => arrayMove(prev, prev.indexOf(active.id), prev.indexOf(over.id)));
     }
   };
   ```

5. **Strategy**: Use `horizontalListSortingStrategy` for tabs, `verticalListSortingStrategy` for lists.

## Key details
- `CSS.Transform.toString()` converts dnd-kit's transform object to CSS transform string
- `PointerSensor` works for mouse; add `TouchSensor` for mobile
- `cloneElement` injects ref + style + listeners onto existing tab node without extra wrapper DOM
