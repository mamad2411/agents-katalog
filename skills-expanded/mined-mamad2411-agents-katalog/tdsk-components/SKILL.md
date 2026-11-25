---
name: "tdsk-components"
description: "Knowledge base for the shared React components library (@tdsk/components)"
tags: ["react", "mui", "components", "hooks", "frontend", "shared-library"]
---
# Components Repo Skill

## Overview

- Shared React component library (`@tdsk/components`) consumed by Admin and Threads SPAs
- MUI-based components, custom hooks, Monaco editor, artifact rendering (Markdown, Mermaid), chat UI primitives
- Theming with dark/light mode via `makeTheme(variant, breakpoints)`
- Built with tsup, tested with vitest

## Directory Structure

```
repos/components/
├── src/
│   ├── components/       # 40 React UI component directories (incl. Avatar, Chip, NavRail)
│   ├── hooks/            # 41 custom hooks across 10 categories (incl. analytics/)
│   ├── contexts/         # CacheContext provider
│   ├── hocs/             # TooltipHoc, OverlayScroll
│   ├── services/         # storage, clipboard, cacheService, eventEmitter, overlayScrollBody
│   ├── theme/            # colors, theme factory, helpers, dims, gutter
│   ├── types/            # TypeScript type definitions (17 files)
│   ├── utils/            # omit, date, inputs, helpers, customEvt, isValidFuncComp, overlayScrollOpts, getAvatarColor, fetcher
│   ├── constants/        # values, monaco, events, elements, auth
│   └── index.ts          # Main export barrel
├── configs/              # biome.json, vitest.config.ts, aliases.ts
├── scripts/              # getEntries, setupTests, loadEnvs, addToProcess
└── package.json
```

## Barrel Export Notes

Several items are NOT re-exported from their parent `index.ts` barrels and must be imported by direct path:
- **Components**: `InfoTip/`, `NotificationCount/` not in `src/components/index.ts`
- **Icons**: `NamedIcon` not in Icons barrel (imports from `./index` internally)
- **Hooks**: `definitions/` category (`useDefsFilters`) not in `src/hooks/index.ts`
- **Hooks**: `useForceUpdate`, `useMergedRef` not in `components/` hooks barrel
- **Hooks**: `useMonacoActions` not in `monaco/` hooks barrel
- **Inputs**: `AutoInput.tsx`, `SelectInputValue.tsx` not in Inputs barrel
- **Card**: `CardActions` exists but not exported from Card barrel

## Components by Category

| Category | Components |
|----------|-----------|
| **Artifact/Chat** | ArtifactRenderer, MarkdownRenderer, MermaidRenderer, MessageBubble, FilePreview, ToolCallDisplay |
| **Header** | Header (+styled), AppLogo, UserMenu |
| **Inputs** | FormInput, SelectInput, SelectListItem, TagsInput, CronInput, TextInput, InputLabel, AdminInput, SliderInput, SwitchInput, InlineSelect, CheckboxInput, InputContainer, CheckContainer, InputStateHandler, SelectCategoryInput, Textarea, OutlinedInput, AutoInputText |
| **Buttons** | Button, DialButton, IconButton, ButtonGroup, LoadingButton |
| **Dialogs** | Dialog, DialogActions, DraggableDialog |
| **Drawer** | Drawer (right-anchored, header/title/close/content/actions), DrawerActions (save/create/cancel/delete) |
| **Monaco** | Monaco, MonacoActions, LangSelect |
| **Icons** | Icon + 28+ named SVG icons (Anthropic, OpenAI, Ollama, ZAI, MCP, Sandbox, Gitlab, etc.) |
| **Layout** | Accordion (+Action/Actions/InfoAction), Card, Section (+Actions), Tabs, List (+Item), Menu (+Items/Multilevel/IconMenuItem/Back/Header/Context), Collapse, Resize |
| **Selectors** | SelectorButton, SelectorMenu |
| **Auth/Access** | FeatureGate, Login, Permissions |
| **Chat** | ChatComponents |
| **Utility** | ClipboardCopy, Confirm (+Delete), Definitions (+Definition/ComplexDefs/DefsFilters), Dropdown (+DDHeader), Empty, Image, InlineDom, Loading (+Dots), MemoChildren, Portal, RenderType (+Icon), Text (+Elements/Pair), Tooltip |

## Hooks by Category

| Category | Hooks |
|----------|-------|
| **dom** | useInput, useKeyDown, useIsMobile, useSyncValue, useDisplayDate, useDownloadText, useWindowResize, useFormattedTime, useCopyToClipboard |
| **components** | useProp, useCron, useInline, useResize, useToggle, useEnsureRef, useEffectOnce, useStateReset, useForceRender, useLayoutMaxWidth |
| **data** | useRecall, useTimeout, useInterval, useArrToggle |
| **api** | useFetch, useLoadDynamic |
| **theme** | useTheme, useColor, useColors, useIsDarkMode, useJoinSx |
| **featureFlags** | useFeatureFlag |
| **monaco** | useMonaco |
| **permissions** | useCanPerform, usePermissions, usePermissionsContext |
| **definitions** | useDefsFilters (NOT in hooks barrel) |

## Architecture

Each component follows: `ComponentName/ComponentName.tsx` + `ComponentName.styles.tsx` (Emotion) + `index.ts` barrel. Styling uses MUI theme + `@emotion/styled`. Components support render props, compound patterns (Dialog+DialogActions), controlled/uncontrolled inputs, and forward refs.

## Key Patterns

- **Theme**: `makeTheme('dark')` / `makeTheme('light')` creates MUI theme instances
- **HOCs**: `TooltipHoc(Component)`, `OverlayScroll`
- **Cache**: `CacheProvider` context with `GlobalCache.set/get`
- **Gutter**: Spacing via `gutter.px`, `gutter.dpx`, `gutter.hpx`, `gutter.qpx`, `gutter.tpx`

## Integration Points

- **Consumed by**: Admin repo (`repos/admin/`), Threads repo (`repos/threads/`)
- **Key deps**: `react-markdown`, `remark-gfm`, `mermaid`, `@monaco-editor/react`, `react-resizable-panels`
- **Build**: tsup → `dist/` (CJS: `dist/index.js`, ESM: `dist/esm/index.js`, Types: `dist/index.d.ts`)
- **Test**: Vitest + `@testing-library/react` + jsdom
