---
name: backend-dtos
description: Define Data Transfer Objects for API boundaries. Use when shaping
  request/response contracts.
metadata:
  tags: backend, dtos
---

# Backend DTOs & Contracts

## Use this skill when
- Defining request and response shapes
- Separating API contracts from internal entities/domain
- Serialization and back-compat planning

## Do not use this skill when
- Internal application objects (use value objects in the domain)

## Instructions
1. Define explicit DTOs for every request and response.
2. Never expose domain entities or ORM models directly.
3. Map domain ↔ DTO at the boundary with clear conversion.
4. Add example values and validation rules to DTOs.
5. Version structural changes to DTOs deliberately.
6. Keep field naming consistent with the API style guide.

## Output Format
- Endpoint | request DTO | response DTO | mapping

## Common Mistakes
- Serializing ORM models to JSON
- DTOs that mirror DB schema exactly
- Field names that leak storage details
