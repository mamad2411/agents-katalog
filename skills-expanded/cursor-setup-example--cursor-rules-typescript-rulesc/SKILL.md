---
description: Follow TypeScript coding standards including named exports preference, direct imports, and configuration-driven patterns for maintainable code
globs: *.ts,*.tsx
alwaysApply: false
---
# TypeScript Rules

Follow TypeScript coding standards for all .ts and .tsx files to maintain code quality and consistency.

## Eliminating Repetitive Patterns

### Configuration Over Repetition
When you see 3+ similar code blocks, extract into configuration-driven patterns:

```typescript
// ❌ WRONG - Repetitive if-else blocks
if (dataType === CompanyDataType.CORPORATE_CARBON_FOOTPRINT) {
  return processData(/* similar logic */);
}
if (dataType === CompanyDataType.PRODUCT_CARBON_FOOTPRINTS) {
  return processData(/* similar logic */);
}

// ✅ CORRECT - Configuration-driven
const ENGAGEMENT_KEYS = {
  [CompanyDataType.CORPORATE_CARBON_FOOTPRINT]: 'ccfEngagementProgress',
  [CompanyDataType.PRODUCT_CARBON_FOOTPRINTS]: 'pcfEngagementProgress',
} as const;

const progress = supplier.engagementData?.[ENGAGEMENT_KEYS[dataType]];
```

## Code Simplification

**Eliminate unnecessary abstractions:**
- Remove wrapper functions that don't add meaningful value
- Replace one-line functions with direct operations or object lookups

```typescript
// ✅ CORRECT - Direct object lookup
const DEFAULT_COMPLIANCE_LEVELS = {
  CorporateCarbonFootprint: "Collecting",
  RenewableEnergy: "Collecting",
} as const;

// ❌ WRONG - Unnecessary wrapper function
function getDefaultComplianceLevel(dataType: string) {
  switch (dataType) {
    case "CorporateCarbonFootprint": return "Collecting";
    default: return "Collecting";
  }
}
```

**Inline simple operations:**
- Replace switch statements with `const` object lookups for simple mappings
- Inline one-line functions directly where they're used

```typescript
// ✅ CORRECT - Inline simple handlers
<Dropdown
  onChange={(selectedItem) => {
    setFormData(prev => ({ ...prev, complianceLevel: selectedItem }));
  }}
/>

// ❌ WRONG - Unnecessary function extraction
const handleChange = (selectedItem) => {
  setFormData(prev => ({ ...prev, complianceLevel: selectedItem }));
};
```

## Import and Export Organization

### Prefer Named Exports Over Default Exports

**Use named exports for better IDE support, refactoring safety, and tree-shaking:**

```typescript
// ✅ CORRECT - Named exports
export const ComponentName: React.FC<ComponentNameProps> = ({ title }) => {
  return <div>{title}</div>;
};

export const utilityFunction = (data: string) => data.toUpperCase();

// ✅ CORRECT - Named imports
import { ComponentName, utilityFunction } from "./ComponentName";
```

```typescript
// ❌ WRONG - Default exports
const ComponentName: React.FC<ComponentNameProps> = ({ title }) => {
  return <div>{title}</div>;
};

export default ComponentName;

// ❌ WRONG - Default imports
import ComponentName from "./ComponentName";
```

**Why prefer named exports:**
- **IDE Support**: Better autocomplete, go-to-definition, and refactoring
- **Refactoring Safety**: Renaming exports automatically updates all imports

### Direct Imports Over Barrel Files

**Avoid index barrel files** - import modules directly from their source files:

```typescript
// ✅ CORRECT - Direct imports
import { ComponentName } from "@features/profile/components/ComponentName/ComponentName";

// ❌ WRONG - Index barrel file imports
import { ComponentName } from "@features/profile/components/ComponentName";
```

**Why avoid barrel files:** They add bloat, hide true dependencies, hurt tree-shaking, and risk circular dependencies.

# One-Way Import Flow for Types

**Types belong with their implementers, not their consumers.** Import types from the code that defines and uses them, never the other way around.

## Correct Approach

```typescript
// ✅ CORRECT - Type defined with implementing component
// ProgrammeRequirementTile.tsx
export type ProgrammeRequirementTileData = {
  dataType: { displayName: string; icon: React.ReactNode };
  isEnabled: boolean;
  complianceLevel?: string;
  deadlineWeeks?: number;
};

export const ProgrammeRequirementTile: React.FC<Props> = ({ tileData }) => {
  // Implementation
};

// ✅ CORRECT - Consumers import from implementer
// ProgrammeRequirementsTab.tsx
import { ProgrammeRequirementTile, ProgrammeRequirementTileData } from "./ProgrammeRequirementTile";
```

## Incorrect Approach

```typescript
// ❌ WRONG - Type separated from implementation
// getProgrammeRequirementsData.tsx
export type TileData = { /* ... */ }; // Belongs with component instead

// ProgrammeRequirementTile.tsx
import { TileData } from "./getProgrammeRequirementsData"; // Creates coupling
```

## Type Placement Priority

1. **Generated types** (`@generated/`) - Use when available
2. **Component types** - Co-locate with implementation
3. **Shared types** (`@{featureName}/common/`) - For genuine cross-component reuse within a feature
3. **Shared types** (`@shared/types`) - Only for genuine cross-feature reuse

This prevents circular dependencies, clarifies ownership, and keeps related code together.

## Type Safety and Organization

**Consolidate shared types in common locations:**
- Move shared types to `common/` folders to prevent duplication
- Use union types derived from API responses rather than custom enums

```typescript
// ✅ CORRECT - Shared types in common location
// src/features/settings/common/types.ts
export type ProgrammeRequirementApiKey = keyof ProgrammeRequirements;

// ✅ CORRECT - Let TypeScript infer when possible
const complianceLevelOptions = complianceConfig?.data_types?.[dataType]?.levels || [];
```

**Minimize string transformations:**
- Avoid unnecessary formatting for HTML attributes when consistency is sufficient
- Use API values directly when casing doesn't matter for functionality

```typescript
// ✅ CORRECT - Direct usage
const id = dataType;
const testId = `${dataType}-tile`;

// ❌ WRONG - Unnecessary transformation
const id = getDataTypeId(dataType);
const testId = `${transformCase(dataType)}-tile`;
```

## Testing

**Test only the public API (exported functions), not implementation details:**

```typescript
// ✅ CORRECT - Test main exported function
describe("getEngagementData", () => {
  it("returns COMPLETED when supplier has targets", () => {
    const result = getEngagementData(CompanyDataType.DECARBONISATION_INFORMATION, supplier, profile);
    expect(result.stage).toBe(EngagementFunnelStage.COMPLETED);
  });
});
```

**Use Playwright MCP for comprehensive component testing.** Follow the testing workflow in [@project-rules/playwright-mcp-testing](./playwright-mcp-testing.mdc).

## Refactoring Best Practices

**Refactor incrementally with verification:**
- Make small changes and verify with TypeScript compilation after each step
- Remove unused imports immediately as they become unused
- Clean up outdated comments during refactoring to keep code self-documenting (follow @core-rules/comments)

```typescript
// After each refactoring step:
// 1. Run: yarn tsc --noEmit
// 2. Remove unused imports
// 3. Remove outdated comments
// 4. Verify functionality still works as expected
