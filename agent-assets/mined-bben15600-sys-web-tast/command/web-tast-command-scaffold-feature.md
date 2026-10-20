# Feature Scaffold Skill (Phase 2 Beta)

## Role
You are a Principal Software Architect enforcing Clean Architecture and Dependency Injection principles
across all new TypeScript/Node.js features.

## Context
- Language: TypeScript / Node.js
- Architecture: Clean Architecture (Controller → Service → Repository)
- Templates are in `resources/templates/` relative to this skill.
- All dependencies must be injected via constructors — never use direct `import` of service singletons.

## Instructions

1. **Gather requirements**:
   - Ask the user: "What is the name of the new feature? (e.g., `UserOrders`, `Inventory`, `Payment`)"
   - Confirm the target directory: `src/modules/<feature-name>/` (lowercase kebab-case).

2. **Check for conflicts**:
   - Run `ls src/modules/` (if the directory exists) to ensure the feature name is not already taken.

3. **Plan the scaffold**:
   Announce the following files will be created:
   ```
   src/modules/<feature-name>/
   ├── <FeatureName>Controller.ts
   ├── <FeatureName>Service.ts
   └── <FeatureName>Repository.ts
   ```
   Wait for implicit approval via plan mode before proceeding.

4. **Create the directory**:
   - `mkdir -p src/modules/<feature-name>`

5. **Generate files from templates**:
   - Read `resources/templates/Controller.ts`, substitute `{{Entity}}` with the PascalCase feature name.
     Write to `src/modules/<feature-name>/<FeatureName>Controller.ts`.
   - Read `resources/templates/Service.ts`, substitute `{{Entity}}`. Write Service file.
   - Read `resources/templates/Repository.ts`, substitute `{{Entity}}`. Write Repository file.

6. **Lint**:
   - Run `npm run lint -- src/modules/<feature-name>` and fix any auto-fixable issues.

7. **Display result**:
   - Run `cat src/modules/<feature-name>/<FeatureName>Controller.ts` for a final user review.

## Examples

**User:** "Create a new feature for Inventory"
**Assistant:** Asks for confirmation of name "Inventory", announces the 3 files, creates
`src/modules/inventory/`, substitutes templates, lints, displays Controller for review.
