---
name: reactflow
description: >-
  React Flow(@xyflow/react) 노드·엣지 그래프 UI 구현 가이드. 커스텀 노드/엣지, 핸들,
  controlled state, TypeScript, sub-flow/group, 레이아웃, Zustand 연동, React Flow UI
  (shadcn) 적용 시 사용. React Flow, xyflow, flow canvas, node editor 작업에 적용.
---

# React Flow

[React Flow Learn](https://reactflow.dev/learn) · [React Flow UI](https://reactflow.dev/ui) 기준.

## 적용 시점

- `@xyflow/react`로 인터랙티브 플로우/다이어그램을 새로 만들거나 수정할 때
- 커스텀 노드·엣지, 그룹/서브플로우, 레이아웃, 상태 연동을 설계·리뷰할 때
- React Flow UI(shadcn) 컴포넌트를 도입·커스터마이즈할 때

## 패키지·설치

```bash
npm install @xyflow/react
```

- 패키지명은 `@xyflow/react` (구 `reactflow` 아님)
- CSS 필수: `@xyflow/react/dist/style.css`
- 부모 컨테이너에 **width·height** 필수 (`100%` 또는 고정 px)

### Tailwind CSS 4 + 스타일 순서

`global.css` / `index.css`에서 **tailwind 이후** React Flow CSS를 import한다. `App.tsx`에서 import하지 않는다.

```css
@import "tailwindcss";
@layer base {
  @import "@xyflow/react/dist/style.css";
}
```

React Flow UI(shadcn) 사용 시에도 동일 규칙.

## 워크플로우

1. 요구사항 분류: 단순 뷰어 / 편집기 / 그룹·서브플로우 / 자동 레이아웃 / 실행 상태 표시
2. **controlled flow** 패턴으로 `nodes`·`edges` + change handler 구성
3. 커스텀 노드가 필요하면 `nodeTypes`를 컴포넌트 **밖**에 정의
4. 인터랙티브 요소에 `nodrag` / `nopan` / `nowheel` 적용
5. TypeScript union(`AppNode`, `AppEdge`)으로 타입 안전성 확보
6. shadcn·Tailwind 프로젝트면 React Flow UI로 빠른 시작 검토
7. 상세 API·UI 카탈로그는 [reference.md](reference.md) 참조

## 핵심 개념

| 용어 | 설명 |
|------|------|
| Node | `id`, `position`, `data`, 선택적 `type` |
| Edge | `id`, `source`, `target`, 선택적 `sourceHandle`/`targetHandle` |
| Handle | 노드 연결점. 다중 핸들은 고유 `id` 필요 |
| Viewport | `x`, `y`, `zoom`. pane 드래그·핀치/스크롤로 변경 |
| Connection line | 드래그 중 임시 엣지 |

기본 엣지 타입: `default`(bezier), `smoothstep`, `step`, `straight`  
기본 노드 타입: `default`, `input`, `output`, `group`

## Controlled Flow (필수 패턴)

`nodes`/`edges`를 props로 넘기면 **controlled**. 변경 핸들러 없으면 드래그·연결·삭제가 동작하지 않는다.

```tsx
import { useCallback, useState } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  applyNodeChanges,
  applyEdgeChanges,
  addEdge,
  type OnConnect,
  type OnNodesChange,
  type OnEdgesChange,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const onNodesChange: OnNodesChange = useCallback(
  (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
  [],
);
const onEdgesChange: OnEdgesChange = useCallback(
  (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
  [],
);
const onConnect: OnConnect = useCallback(
  (params) => setEdges((eds) => addEdge(params, eds)),
  [],
);
```

기본 키보드: `Shift`+드래그 영역 선택, `Cmd/Ctrl`+클릭 다중 선택, `Backspace` 삭제.

## 커스텀 노드

- **커스텀 노드를 기본으로 권장** (공식 문서)
- `nodeTypes`는 컴포넌트 외부 상수로 정의 (리렌더 방지)
- `NodeProps<YourNode>`로 `data` 타입 지정
- `memo` + `displayName` 권장

```tsx
const nodeTypes = { flowNode: FlowCanvasNode };

<NodeProps<FlowNode>>
```

### 핸들

```tsx
import { Handle, Position } from '@xyflow/react';

<Handle type="target" position={Position.Top} />
<Handle type="source" position={Position.Right} id="out-a" />
```

- 다중 source/target: 각 Handle에 고유 `id`, edge에 `sourceHandle`/`targetHandle` 지정
- 핸들 수·위치를 코드로 바꾸면 `useUpdateNodeInternals` 호출
- 숨길 때 `display: none` 금지 → `visibility: hidden` 또는 `opacity: 0`
- `connectionMode="Loose"`면 source/target 구분 없는 핸들 가능

### 유틸리티 CSS 클래스

| 클래스 | 용도 |
|--------|------|
| `nodrag` | 버튼·입력 등 — 노드 드래그·선택 방지 |
| `nopan` | 클릭 시 viewport pan 방지 |
| `nowheel` | 노드 내부 스크롤 시 캔버스 pan 방지 |

커스텀 노드는 기본 스타일 없음 — 프로젝트 스타일 시스템으로 직접 스타일링.

## 커스텀 엣지

```tsx
import { BaseEdge, getStraightPath, type EdgeProps } from '@xyflow/react';

export function CustomEdge({ id, sourceX, sourceY, targetX, targetY }: EdgeProps) {
  const [path] = getStraightPath({ sourceX, sourceY, targetX, targetY });
  return <BaseEdge id={id} path={path} />;
}

const edgeTypes = { 'custom-edge': CustomEdge };
```

경로 유틸: `getBezierPath`, `getSmoothStepPath`, `getStraightPath` 등.

## TypeScript

```tsx
type FlowNode = Node<FlowNodeData, 'flowNode'>;
type FlowEdge = Edge<FlowEdgeData, 'flowEdge'>;
type AppNode = BuiltInNode | FlowNode | GroupNode;
type AppEdge = BuiltInEdge | FlowEdge;

// ReactFlow·hooks에 제네릭 전달
const { getNodes } = useReactFlow<AppNode, AppEdge>();
const onNodesChange: OnNodesChange<AppNode> = useCallback(...);
```

- `Node<Data, Type>`에서 `type`은 `interface`가 아닌 **type alias**로 분리
- 복수 커스텀 노드: `NodeProps<SpecificNode>` 또는 union + type guard

## Sub-flow / 그룹

```tsx
// parent가 children보다 nodes 배열에서 먼저 와야 함
{
  id: 'group-1',
  type: 'group', // 또는 커스텀 그룹 노드
  position: { x: 0, y: 0 },
  style: { width: 400, height: 300 },
  data: { label: 'Group' },
},
{
  id: 'child-1',
  parentId: 'group-1',       // v11.11+ (구 parentNode)
  extent: 'parent',            // 부모 밖으로 드래그 방지
  expandParent: true,          // 가장자리 드래그 시 부모 자동 확장
  position: { x: 20, y: 50 },  // 부모 좌상단 기준 상대 좌표
  data: { label: 'Child' },
}
```

- `parentId`는 마크업 중첩이 아니라 **상대 좌표**만 설정
- 엣지는 기본적으로 노드 아래 z-index에 렌더

## 내장 컴포넌트 (children)

```tsx
<ReactFlow nodes={nodes} edges={edges} ...>
  <Background />
  <Controls />
  <MiniMap />
  <Panel position="top-left">...</Panel>
</ReactFlow>
```

`Panel`은 viewport에 고정된 오버레이 UI.

## Viewport 조작 모드

| 모드 | pan | zoom | select |
|------|-----|------|--------|
| 기본 (slippy map) | pointer drag | pinch/scroll | Shift+drag |
| 디자인 툴 (Figma류) | scroll, 중클릭, space+drag | pinch/cmd+scroll | pointer drag |

디자인 툴 모드: `panOnScroll`, `selectionOnDrag={true}`, `panOnDrag={false}`, 필요 시 `selectionMode="partial"`.

## 상태 관리 (Zustand 등)

노드 내부에서 그래프 상태를 갱신해야 하면:

1. `nodes`/`edges` + `onNodesChange`/`onEdgesChange`/`onConnect`를 store로 이동
2. 노드별 액션(`updateNodeData`)은 **불변 업데이트**로 `set({ nodes: ... })`
3. 노드 컴포넌트에서 store selector로 액션만 구독
4. React Flow 내부도 Zustand 사용 — `ReactFlowProvider` + `useReactFlow`로 자식에서 viewport/API 접근

```tsx
updateNodeColor: (nodeId, color) => {
  set({
    nodes: get().nodes.map((node) =>
      node.id === nodeId
        ? { ...node, data: { ...node.data, color } }
        : node,
    ),
  });
};
```

## 레이아웃 (외부 라이브러리)

React Flow는 내장 auto-layout 없음. 노드 배열을 계산해 `setNodes`로 반영.

| 라이브러리 | 용도 | 특징 |
|-----------|------|------|
| **dagre** | 트리/방향 그래프 | 단순, 빠름. 서브플로우 연결 이슈 주의 |
| **d3-hierarchy** | 단일 루트 트리 | 노드 크기 동일 가정 |
| **d3-force** | 물리 기반 | 반복 시뮬레이션, 성능 주의 |
| **elkjs** | 복잡·설정 많음 | 비동기, 서브플로우·엣지 라우팅 |

엣지 라우팅: `react-flow-smart-edge` 등 외부 솔루션 검토.

## React Flow UI (shadcn)

전제: shadcn + Tailwind 설정 완료.

```bash
npx shadcn@latest add https://ui.reactflow.dev/<component-name>
```

- 소스 코드가 프로젝트에 복사됨 (블랙박스 npm 패키지 아님)
- `components.json` alias로 설치 경로 변경 가능
- 기존 shadcn 컴포넌트와 병합·덮어쓰기 확인

### 주요 UI 컴포넌트

| 카테고리 | 컴포넌트 | 설치 URL slug |
|---------|---------|---------------|
| Node 유틸 | base-node | `base-node` |
| Node 유틸 | node-status-indicator | `node-status-indicator` |
| Controls | node-search | `node-search` |
| Custom Node | database-schema-node, zoom-slider 등 | 각 컴포넌트 페이지 참조 |

`BaseNode` 구조: `BaseNode` → `BaseNodeHeader` / `BaseNodeHeaderTitle` / `BaseNodeContent` / `BaseNodeFooter`  
인터랙티브 버튼에는 `nodrag` 필수.

`NodeStatusIndicator`: `status` = `success` | `loading` | `error` | `initial`, `variant` = `border` | `overlay`.

## 흔한 실수

- CSS 미import 또는 Tailwind 4에서 import 순서 오류
- 부모 div에 height 없음 → 빈 캔버스
- controlled flow인데 `onNodesChange`/`onEdgesChange` 누락
- `nodeTypes`/`edgeTypes`를 렌더마다 재생성 → 성능·버그
- 핸들 숨김에 `display: none` 사용
- sub-flow에서 parent 노드가 child보다 뒤에 배치
- 노드 `data` 직접 mutation (불변 업데이트 필요)

## 구현 체크리스트

- [ ] `@xyflow/react` + CSS import + 부모 크기
- [ ] controlled: `applyNodeChanges` / `applyEdgeChanges` / `addEdge`
- [ ] `nodeTypes` 컴포넌트 외부 정의
- [ ] 인터랙티브 UI에 `nodrag` 등 유틸 클래스
- [ ] TS: `AppNode`/`AppEdge` union + `NodeProps` 제네릭
- [ ] 그룹: `parentId`, `extent: 'parent'`, 배열 순서
- [ ] 레이아웃 필요 시 외부 라이브러리 + `setNodes` 반영

## 참고

- 상세 API·UI 카탈로그: [reference.md](reference.md)
- 공식 Learn: https://reactflow.dev/learn
- 공식 UI: https://reactflow.dev/ui
- TypeScript: https://reactflow.dev/learn/advanced-use/typescript
- Sub-flows: https://reactflow.dev/learn/layouting/sub-flows
