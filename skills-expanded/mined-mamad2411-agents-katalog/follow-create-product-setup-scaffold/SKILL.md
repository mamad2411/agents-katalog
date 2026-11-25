---
name: follow-create-product-setup-scaffold
description: Scaffold product structure — monorepo, packages, shared config, conventions
argument-hint: "[product-name]"
related:
  - follow-create-product
  - follow-monorepo
  - create-new-project-in-drive-d
  - implement-to-production
  - ask-me
---

## Goal

Scaffold a new product per conventions — structure, workspaces, shared config, tooling baseline

## Scope

- Covers the initial scaffold only — deploy → `workflows/deploy-mvp`
- Tech stack per the `/deep-review-codebase` catalog

## Execute

### 1. Confirm Requirements

> Goal: stack and scope clear before scaffolding

1. Ask/confirm product type, target users, and tech stack (`/ask-me` if unclear)
2. Pick defaults from the techstack catalog — never guess the stack

### 2. Scaffold Structure

> Goal: structure per monorepo/project conventions

1. Create the directory structure per product type
2. workspaces/packages + shared config (tsconfig, lint, format)
3. `AGENTS.md`, `README.md`, `.gitignore`, CI skeleton
4. init git + initial structure only — do not implement features

### 3. Verify Scaffold

> Goal: the scaffold runs

1. install deps + build/typecheck pass
2. dev server or entry point works

## Rules

- Scaffold only — continue features at `/implement-to-production`
- Every config follows `/update-config` conventions

## Expected Outcome

- Product scaffold ready — structure, config, and tooling baseline complete and running
