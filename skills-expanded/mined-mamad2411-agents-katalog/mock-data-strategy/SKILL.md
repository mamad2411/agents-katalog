---
name: mock-data-strategy
description: Keep temporary frontend mock data isolated, typed, and easy to replace as backend APIs become available.
---

# Mock Data Strategy

## When to use this skill

- When the frontend needs temporary data before backend endpoints are ready.
- When deciding where mock data should live and how components should consume it.
- When reviewing whether a mock-based implementation will be easy to swap for real APIs later.

## Project-specific rules

- Mock data is allowed only as a temporary frontend development bridge.
- Mock data must be isolated and easy to replace with real API calls.
- Preferred mock data location is under `lib/mock-data/` as described in the blueprint.
- Keep service signatures stable so the replacement path stays inside the service layer, API client, or environment config.
- Do not invent fake backend behavior such as frontend-only reservation conflict rules.
- Mock content should mirror the typed backend-oriented shapes the real app expects.
- Avoid spreading mock constants directly through page or component files.

## Expected output quality

- Makes development unblock quickly without contaminating the architecture.
- Preserves the same typing and data flow expected from real APIs.
- Clearly marks what is temporary.
- Keeps removal or replacement straightforward.

## Things to avoid

- Calling mock helpers directly from many components.
- Creating business logic in mocks that the backend should own.
- Using vague or untyped mock data.
- Coupling UI behavior to fake transport or timing logic.
- Letting temporary mocks become permanent hidden dependencies.

## Checklist before completing work

- Confirm mock data is isolated from UI components.
- Confirm types match expected backend-oriented contracts.
- Confirm replacement with real APIs would stay limited to service-layer files.
- Confirm no fake backend authority has been introduced.
- Confirm temporary data is clearly identifiable and easy to remove.
