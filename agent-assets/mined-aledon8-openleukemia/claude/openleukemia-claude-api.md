# API Layer Memory

Apply this inside `ai-service/app/api/`.

- API modules should handle routing, status codes, request parsing, and response models.
- Keep route handlers thin; call domain services for behavior.
- Use explicit `response_model` declarations.
- Do not embed consent, extraction, or ML business rules directly in route functions.
- When debugging an API symptom, trace from route to domain service to schema and back to tests.
