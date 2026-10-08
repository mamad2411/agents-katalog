# Eval: Angular Quality Gates

## Prompt

Enable strictTemplates and a CI `check` script (lint, headless test with coverage, production build) for our Angular 19 app. Fix template type errors in the Dashboard module without disabling strict mode globally.

## Expected Agent Behavior

- Updates angular.json / tsconfig / package.json and CI
- Fixes template and TS errors in Dashboard
- Documents npm run check for local use
- Keeps coverage and lint in pipeline

## Failure Signals

- Sets strictTemplates false globally
- Removes ng test from CI
- Uses $any() on all template bindings
