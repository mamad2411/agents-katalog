---
description: Enforces standards for building API endpoints within a Rails application.
globs:
  - "app/controllers/api/**/*.rb"
---

# API

<rule>
name: api_standard
description: Provides guidelines for creating API endpoints that adhere to RESTful design, versioning, and proper response formatting in Rails.

filters:
  - type: path
    pattern: "^app/controllers/api/.*\\.rb$"
    # Applies to API controllers in the app/controllers/api directory

actions:
  - type: suggest
    message: |
      API controllers should:
      1. Follow RESTful conventions for CRUD actions.
      2. Use versioning in the URL or headers.
      3. Return standardized JSON responses.
      4. Handle errors gracefully with appropriate HTTP status codes.
      5. Include clear documentation for each endpoint.

examples:
  - input: |
      # Bad example: API controller with inconsistent response format and lack of versioning.
      class Api::UsersController < ApplicationController
        def index
          render json: User.all
        end
      end
    output: "Ensure API responses are consistent and include versioning information."
  - input: |
      # Good example.
      module Api
        module V1
          class UsersController < ApplicationController
            def index
              users = User.all
              render json: { data: users, status: 'success' }, status: :ok
            end
          end
        end
      end
    output: "API controller follows RESTful design with versioned responses and standardized JSON output."

metadata:
  priority: medium
  version: 1.0
  related_rules:
    - rails_project_standard
  responsibility: "Standardize the development of API endpoints in a Rails application"
</rule>
