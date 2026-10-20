---
alwaysApply: false
---
You are an expert in modern React (React 19) and TypeScript, specialized in:
Ant Design 5, Pro Components, TanStack React Query 5, React Router v7,
DnD-Kit, Vite 7, and scalable component-driven frontend architecture.

Your job is to write frontend code that integrates perfectly into the QLDA FE project,
following its conventions, patterns, folder structure, and component behaviors.

===========================================================
📌 1. GENERAL REACT + TYPESCRIPT RULES
===========================================================
- Use React 19 with function components only.
- Use TypeScript strictly; avoid "any".
- Write explicit props types:
    type Props = { ... }
- Use named exports unless file is a page-level index.
- Avoid unnecessary re-renders using useCallback + useMemo.
- Avoid inline logic inside JSX; extract small functions when needed.
- Keep components small, pure, predictable.
- Keep UI logic in components and business logic in hooks/services.

===========================================================
📌 2. PROJECT ARCHITECTURE (PATTERN, NOT STRICT)
===========================================================
The project follows a consistent modular structure:

src/
 ├── App.tsx
 ├── main.tsx
 ├── assets/
 ├── components/               → shared UI components
 ├── context/                  → AuthProvider, global contexts
 ├── hooks/                    → reusable custom hooks
 ├── layouts/                  → AppLayout, AuthLayout
 ├── pages/                    → feature pages grouped by domain
 ├── services/                 → axios API modules
 ├── types/                    → shared FE types matching BE
 ├── styles/                   → CSS
 └── utils/                    → helpers & constants

Rules:
- Shared UI → src/components
- Domain-specific UI → src/pages/<domain>/components
- Page routes ALWAYS live in src/pages/<domain>/index.tsx
- DO NOT put API logic into components (use services)

===========================================================
📌 3. REACT ROUTER RULES (v7)
===========================================================
- Use <BrowserRouter> in App.tsx.
- Use:
    import { Route, Routes, Navigate } from 'react-router-dom';
- Private routes must be wrapped with <PrivateRoute/>.
- Use loader and suspense patterns when required.
- Pages MUST live inside src/pages/**.

===========================================================
📌 4. ANT DESIGN & PRO COMPONENTS RULES
===========================================================
- Use Ant Design 5 components: Button, Space, Table, Modal, Form, Input…
- Use Pro Components for tables/forms only when beneficial.
- Prefer responsive layout using Grid, Row, Col.
- UI must be clean, simple, consistent.
- Use message.success | message.error for notifications.
- Use Typography.Text for readable content.
- Keep Modal fully controlled (open={isOpen} onCancel={...}).

===========================================================
📌 5. REACT QUERY 5 RULES
===========================================================
- ALL API calls use React Query via services/ layer.
- NEVER call axios directly inside components.
- Must use:
    const { data, isLoading } = useQuery({ queryKey, queryFn });
    const mutation = useMutation({ mutationFn });
- After mutations, ALWAYS invalidate relevant query keys.

Query key rules:
- Projects: ['projects']
- Project detail: ['project', projectId]
- Columns: ['columns', projectId]
- Tasks: ['tasks', columnId]
- Labels: ['labels', projectId]

===========================================================
📌 6. SERVICES / API RULES
===========================================================
All API calls must:
- live in src/services/*.services.ts
- use axios instance from api.ts
- return typed responses
- avoid mixing UI logic
- be named consistently:
    projectService.create()
    taskService.updatePosition()
    userService.getProfile()

DO NOT:
- construct URLs manually inside components
- mutate axios instance outside api.ts

===========================================================
📌 7. TYPESYSTEM RULES
===========================================================
Types must match backend exactly (NestJS + TypeORM entities):
- user.type.ts
- group.type.ts
- project.type.ts
- project-board.ts (columns + tasks)
- task.type.ts

Rules:
- Do not rename fields unless requested by user.
- Use optional fields only when truly optional from backend.
- Avoid nested “any”.

===========================================================
📌 8. DND-KIT RULES (COLUMN + TASK DRAGGING)
===========================================================
This is CRITICAL for QLDA's board UI.

Required components:
- SortableColumn.tsx
- SortableTask.tsx
- TaskList.tsx
- AddColumnCard.tsx
- AddTaskCard.tsx

Rules:
- Must use:
    DndContext
    SortableContext
    PointerSensor
    KeyboardSensor
    closestCenter / rectSortingStrategy
- NEVER change column.id or task.id.
- ALWAYS update backend position using:
    columnService.updatePosition(...)
    taskService.updatePosition(...)

Task drag:
- within same column → use arrayMove
- across columns → remove + insert + update columnId

Column drag:
- reorder based on new index
- update backend with new position

Do not break:
- add task flow
- add column flow
- task modal logic
- react-query updaters

===========================================================
📌 9. FORM MANAGEMENT RULES
===========================================================
- Use Ant Form OR React Hook Form consistently inside modals.
- Validation must be inside form rules or useController (RHF).
- Avoid mixing uncontrolled & controlled inputs.
- Always reset form when modal closes.

===========================================================
📌 10. UI/UX RULES
===========================================================
- Keep visual layout simple (Space, Flex, Card).
- Use Skeleton or Spin for loading states.
- Avoid unnecessary animations.
- Respect minimal spacing (gap={8}, padding).
- Use meaningful icons from Ant Design Icons.

===========================================================
📌 11. PERFORMANCE RULES
===========================================================
- Use useMemo for computed lists (sorted tasks/columns).
- Use React.memo around TaskCard, Column components.
- Prevent unnecessary rerenders with stable keys.
- Do NOT re-render the entire board on small updates.

===========================================================
📌 12. CLEAN CODE RULES
===========================================================
- No inline styles except very simple ones.
- No commented-out code.
- Keep components below ~150 lines; split when needed.
- Use constants from utils/constants.ts.
- Use descriptive names: selectedTask, activeColumn, isAdding.

===========================================================
📌 13. ERROR HANDLING
===========================================================
- Use message.error('…') for API errors.
- Always guard against undefined data.
- Display empty states: <Empty /> for tables/boards.

===========================================================
📌 14. AI BEHAVIOR RULES
===========================================================
- Follow existing patterns + coding style of the project.
- Respect folder placement for new components/services/hooks.
- Do not generate code that breaks DnD behavior.
- Do not rewrite entire files unless explicitly requested.
- Output FULL file content when asked for “full code”.
- Ask clarifying questions when changes affect multiple components.
- Prefer simple, maintainable solutions instead of over-engineered ones.
