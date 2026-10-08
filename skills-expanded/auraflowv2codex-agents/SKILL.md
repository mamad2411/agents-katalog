# Aura Flow V2 — Development Agent Guide

## Overview
Single-file frontend (`index.html`) + single-file backend (`Code.gs`) + Google Sheets. Professional SaaS quality.

## Rules
- Avoid duplicate/legacy code; prefer small pure helpers.
- Keep required helpers:
  - `ensurePermission_(session, perm)`
  - `logActivity_(session, action, targetId)`
  - `nowIso_()`
- Login must work after every phase.

## Phases
1. Backend — Auth/session/bootstrap.
2. Frontend — Login + proxy + shell.
3. Backend — Tasks/Subtasks + roles + activity/mood.
4. Frontend — Dashboard/Kanban/Focus/Analytics.
5. Both — Bulk upload, CSV/PDF export, Admin panel.
6. Polish — errors, a11y, mobile, performance.

Each phase ≤ 15 mins; deliver complete files.

## Git
- Single branch: `main`. No squashes/amends.
- Commit message format:


## Testing
- After backend edits → run `firstRunInit()`.
- After frontend edits → verify login & main flows.
- Validate role enforcement with sample users.

## Roles
- **Admin**: full access, user mgmt.
- **Sub-Admin**: manages managers and below.
- **Manager**: assigns to interns.
- **Intern**: self-assigned tasks only.
