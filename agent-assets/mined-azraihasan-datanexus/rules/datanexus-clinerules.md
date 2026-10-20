# DataNexus Project Intelligence

This document captures important patterns, preferences, and project intelligence for the DataNexus project. It serves as a living document that will grow as we work together.

## Code Organization Patterns

1. **Component Organization**
   - Components are organized by feature domain (reports, exports, visualizations, etc.)
   - Shared/generic components placed at the root components directory
   - Feature-specific components in subdirectories

2. **Composable Patterns**
   - Composables are named with the 'use' prefix (e.g., useAuth, useFileManager)
   - Business logic is extracted from components into composables
   - Data fetching logic belongs in composables, not directly in components

3. **API Patterns**
   - Server API endpoints follow the Nuxt API routes convention
   - Export-related endpoints are grouped under `/reports/[id]/export/`
   - Report sharing endpoints follow RESTful patterns

## Naming Conventions

1. **Files and Components**
   - Vue components use PascalCase (e.g., ReportViewer.vue)
   - Composables use camelCase with 'use' prefix (e.g., useDataImport.ts)
   - Non-component TypeScript files use camelCase
   - Test files match the name of the file being tested with `.test.ts` suffix

2. **Variables and Functions**
   - Variables and functions use camelCase
   - Interface types use PascalCase
   - Constants likely use UPPER_SNAKE_CASE (to be confirmed)

## Testing Approach

1. **Test Organization**
   - Tests are organized mirroring the source code structure
   - Unit tests for components and composables
   - Integration tests for API endpoints and workflows
   - E2E tests for user scenarios
   - Mocks are stored in test/utils/mocks.ts and test/unit/mocks/

## Project-Specific Patterns

1. **Telecom Domain Models**
   - Tower data is a central entity in the system
   - Contract tracking for towers is a key feature
   - Revenue and payment reporting are important business functions

2. **Validation Workflow**
   - Data imports go through validation, normalization, and aggregation
   - ValidationSummary component displays validation results
   - Validation rules likely defined in types/validation.ts

3. **Report Paradigm**
   - Reports can be built from templates or custom-created
   - Reports can be shared with specific users
   - Reports can be exported in multiple formats

## Current Development Focus

1. **Collaboration Features**
   - Report sharing and access management
   - Email notifications for shared resources
   - Permissions-based access control

## Known Project Preferences

1. **TypeScript Usage**
   - Strong typing is used throughout the project
   - Type definitions are stored in the types/ directory

2. **Code Quality**
   - Unit tests are expected for new components and composables
   - Reuse of composables is preferred over duplicating logic

## To Be Clarified

1. **CSS Framework**
   - The specific CSS framework in use is not explicitly identified
   - Needs confirmation (possibly Tailwind, NuxtUI, or similar)

2. **State Management Approach**
   - Currently appears to be composable-based state management
   - May need confirmation of any global state patterns

3. **Developer Workflow**
   - Preferred branch strategy and PR process
   - Deployment approach and environments

---

This document will be updated as we learn more about the project patterns and preferences.
