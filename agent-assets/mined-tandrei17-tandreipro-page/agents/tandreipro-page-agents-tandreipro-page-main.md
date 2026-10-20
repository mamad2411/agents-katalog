# Agent Instructions

## Scope

These instructions apply only to the `page-atrunkin` repository.

## Project Context

- Stack: React, TypeScript, Vite, Redux Toolkit, React Router, i18next, Formik, and Axios. Package manager: Yarn 4.12.0.
- Start from the files named by the task; inspect nearby implementations and follow their conventions. Avoid unrelated repository-wide exploration.
- Load the relevant file-specific guidance from `.github/instructions/` only for the area being changed.

## Working Rules

- Preserve user changes. Do not commit, push, or create branches unless explicitly requested.
- Do not run global lint/build checks for small changes. Use scripts defined in `package.json`; ask before running them after a large change unless the user requested validation.
- Keep repository documentation in English unless the user requests another language.

## Focused Guidance

- Tooling, dependencies, environment, and deployment: [`.github/instructions/01-project-tooling.instructions.md`](.github/instructions/01-project-tooling.instructions.md)
- React components, styles, and frontend security: [`.github/instructions/02-react-ui.instructions.md`](.github/instructions/02-react-ui.instructions.md)
- Redux state and services: [`.github/instructions/03-redux.instructions.md`](.github/instructions/03-redux.instructions.md)
- User-facing text and translations: [`.github/instructions/04-localization.instructions.md`](.github/instructions/04-localization.instructions.md)
- Axios client, hooks, utilities, and shared-code security: [`.github/instructions/05-shared-code.instructions.md`](.github/instructions/05-shared-code.instructions.md)
