---
description: Descriptive naming for functions, variables, and state - names must clearly indicate what they do.
globs: "app/**/*.ts, app/**/*.tsx, components/**/*.ts, components/**/*.tsx, actions/**/*.ts, lib/**/*.ts, hooks/**/*.ts, utils/**/*.ts"
alwaysApply: false
---

## Descriptive naming (critical)

Names must clearly and explicitly describe what the function/variable does, not just its type or a vague action.

### Function names
- Must describe the complete action, including scope/level when relevant
- Bad: `handleReset`, `handleDelete`, `resetColors`, `deleteColors`
- Good: `handleResetWorkoutColorsToDefaults`, `handleDeleteItemColorOverrides`, `resetWorkoutLevelColors`, `deleteItemLevelColorOverrides`

### State variable names
- Must describe what the state represents, not just its type
- Bad: `showConfirm`, `showDelete`, `showReset`, `isOpen`
- Good: `showResetWorkoutColorsConfirm`, `showDeleteItemColorOverridesConfirm`, `showColorHierarchyExplanation`

### Boolean state
- Use affirmative statements: `isLoading`, `hasError`, `canEdit`
- For dialogs/modals: `show[Action]Confirm`, `is[Feature]Open`, `show[Content]Dialog`

### Scope/level indicators
- When dealing with hierarchical data (workout/item/system), always include the level:
  - `workoutLevel`, `itemLevel`, `systemLevel`, `userDefaults`
  - Examples: `resetWorkoutLevelColors`, `deleteItemLevelOverrides`

### Examples

**State variables:**
```ts
// Bad
const [showConfirm, setShowConfirm] = useState(false);
const [showDelete, setShowDelete] = useState(false);

// Good
const [showResetWorkoutColorsConfirm, setShowResetWorkoutColorsConfirm] = useState(false);
const [showDeleteItemColorOverridesConfirm, setShowDeleteItemColorOverridesConfirm] = useState(false);
```

**Handler functions:**
```ts
// Bad
const handleReset = () => { ... };
const handleDelete = () => { ... };

// Good
const handleResetWorkoutColorsToDefaults = () => { ... };
const handleDeleteItemColorOverrides = () => { ... };
```

**Regular functions:**
```ts
// Bad
const resetColors = () => { ... };
const deleteColors = () => { ... };

// Good
const resetWorkoutLevelColorsToUserDefaults = () => { ... };
const deleteAllItemLevelColorOverrides = () => { ... };
```
