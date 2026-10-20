---
description: Enforces best practices for defining ActiveRecord models in a Rails project.
globs:
  - "app/models/**/*.rb"
---

# Models

<rule>
name: models_standard
description: Ensures that ActiveRecord models follow Rails conventions, including proper validations, associations, and inheritance from ApplicationRecord.

filters:
  - type: path
    pattern: "^app/models/.*\\.rb$"
    # Applies to all model files

actions:
  - type: suggest
    message: |
      Models should:
      1. Inherit from ApplicationRecord or another model if applicable.
      2. Include validations and associations using Rails conventions.
      3. Keep business logic minimal; delegate complex logic when necessary.
      4. Use scopes for query logic.
      5. Follow naming conventions that reflect the underlying database tables.

examples:
  - input: |
      # Bad example: Model not inheriting from ApplicationRecord and missing validations.
      class User
        # code
      end
    output: "Model should inherit from ApplicationRecord and include appropriate validations."
  - input: |
      # Good example
      class User < ApplicationRecord
        validates :email, presence: true, uniqueness: true
        has_many :posts
      end
    output: "Model adheres to Rails conventions with proper inheritance, validations, and associations."

metadata:
  priority: high
  version: 1.0
  related_rules:
    - rails_project_standard
  responsibility: "Standardize ActiveRecord model definitions"
</rule>
