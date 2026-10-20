---
name: openapi-designer
description: "Design complete OpenAPI 3.1 specifications for RESTful APIs. Covers schemas, security, examples, webhooks, and documentation generation."
category: developer-experience
tags: [openapi, swagger, api-spec, documentation, rest]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# OpenAPI Designer

## Purpose
Create comprehensive, accurate OpenAPI 3.1 specifications that serve as the single source of truth for API contracts.

## OpenAPI 3.1 Template

### Basic Structure
```yaml
openapi: 3.1.0

info:
  title: My API
  description: |
    # My API
    
    A complete REST API for managing resources.
    
    ## Authentication
    All endpoints require Bearer token authentication via Sanctum.
    
    ## Rate Limiting
    100 requests per minute per user. See `X-RateLimit-*` headers.
  version: 1.0.0
  contact:
    name: API Support
    email: api@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging
  - url: http://localhost:3000/v1
    description: Local development

security:
  - bearerAuth: []

tags:
  - name: Authentication
    description: Auth operations
  - name: Posts
    description: Post management

paths:
  /posts:
    get:
      tags: [Posts]
      summary: List posts
      description: Retrieve a paginated list of published posts.
      operationId: listPosts
      security: []  # Override: public endpoint
      parameters:
        - $ref: "#/components/parameters/PageParam"
        - $ref: "#/components/parameters/PerPageParam"
        - name: status
          in: query
          schema:
            type: string
            enum: [published, draft]
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PostCollection"
              example:
                data:
                  - id: "123"
                    title: "My Post"
                    status: published
                meta:
                  total: 100
                  page: 1
    post:
      tags: [Posts]
      summary: Create post
      operationId: createPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreatePostRequest"
      responses:
        "201":
          description: Post created
          headers:
            Location:
              schema:
                type: string
                example: /posts/123
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PostResource"
        "422":
          $ref: "#/components/responses/ValidationError"

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
        default: 1
    PerPageParam:
      name: per_page
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  schemas:
    PostResource:
      type: object
      required: [id, title, status, created_at]
      properties:
        id:
          type: string
          format: uuid
        title:
          type: string
          maxLength: 255
        status:
          type: string
          enum: [draft, published, archived]
        created_at:
          type: string
          format: date-time

    CreatePostRequest:
      type: object
      required: [title, body]
      properties:
        title:
          type: string
          minLength: 3
          maxLength: 255
        body:
          type: string
          minLength: 100
        tags:
          type: array
          items:
            type: string
          maxItems: 5

  responses:
    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
              errors:
                type: object
                additionalProperties:
                  type: array
                  items:
                    type: string
```

## Outputs
1. Complete OpenAPI 3.1 specification
2. Schema definitions for all models
3. Error response definitions
4. Postman/Insomnia collection export
5. Generated documentation (Redoc/SwaggerUI)
6. Mock server configuration
