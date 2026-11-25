---
tags: [design, drawer, resizable, mouse, drag]
name: drawer-resizable-mouse-drag
description: Make Ant Design Drawer resizable via mouse drag with styled-components handle, min/max width constraints, and transition suppression during drag
category: design
trigger: When adding resize-by-drag functionality to a drawer or side panel component
version: 1.0.0
source_project: lucida-ui
---

# Resizable Drawer with Mouse Drag

## Steps

1. **Create resize handle** with styled-components:
   ```tsx
   const ResizableHandle = styled.div`
     position: absolute; left: 0; top: 0; bottom: 0;
     width: 4px; cursor: col-resize; z-index: 10;
     &:hover { background: var(--color-border-interactive); }
   `;
   ```

2. **Add mouse event listeners** for drag:
   ```tsx
   const onMouseDown = (e) => {
     e.preventDefault();
     const startX = e.clientX;
     const startWidth = currentWidth;

     // Suppress transition during drag
     const wrapper = document.querySelector('.ant-drawer-content-wrapper');
     if (wrapper) wrapper.style.transition = 'none';

     const onMouseMove = (moveE) => {
       const newWidth = Math.min(MAX_WIDTH, Math.max(MIN_WIDTH, startWidth + (startX - moveE.clientX)));
       setWidth(newWidth);
     };

     const onMouseUp = () => {
       if (wrapper) wrapper.style.transition = '';
       document.removeEventListener('mousemove', onMouseMove);
       document.removeEventListener('mouseup', onMouseUp);
     };

     document.addEventListener('mousemove', onMouseMove);
     document.addEventListener('mouseup', onMouseUp);
   };
   ```

3. **Define constraints**:
   - `MIN_WIDTH = 440` (minimum usable content width)
   - `MAX_WIDTH = window.innerWidth - menuOffset` (don't overlap sidebar)

4. **Apply width** to Ant Drawer:
   ```tsx
   <Drawer width={width} {...props}>
     <ResizableHandle onMouseDown={onMouseDown} />
     {children}
   </Drawer>
   ```

## Key details
- Setting `transition: 'none'` on `.ant-drawer-content-wrapper` during drag prevents jittery animation
- Restore transition on mouseup for smooth open/close animation
- `menuOffset` accounts for sidebar width in the host layout
