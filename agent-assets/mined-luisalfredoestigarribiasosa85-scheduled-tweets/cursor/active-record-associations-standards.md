---
description: Enforces best practices for defining and managing ActiveRecord associations in Rails models.
globs:
  - "app/models/**/*.rb"
---

# ActiveRecord Associations

<rule>
name: active_record_associations_standard
description: Ensures that ActiveRecord associations are defined clearly, maintain referential integrity, and follow Rails conventions for relationships.

filters:
  - type: path
    pattern: "^app/models/.*\\.rb$"
    # Applies to all model files that contain associations

actions:
  - type: suggest
    message: |
      Associations should:
      1. Use descriptive names and follow Rails naming conventions.
      2. Define foreign keys and inverse relationships where applicable.
      3. Utilize options like dependent and through to manage associations.
      4. Avoid circular dependencies and excessive coupling.
      5. Include comments and documentation for non-standard associations.

examples:
  - input: |
      # Bad example: Undefined inverse relationships and missing dependent option.
      class Post < ApplicationRecord
        belongs_to :user
      end
    output: "Define inverse relationships and specify dependent options to ensure data integrity."
  - input: |
      # Good example.
      class Post < ApplicationRecord
        belongs_to :user, inverse_of: :posts
      end

      class User < ApplicationRecord
        has_many :posts, dependent: :destroy, inverse_of: :user
      end
    output: "Associations are clearly defined with proper inverse relationships and dependent options."

metadata:
  priority: medium
  version: 1.0
  related_rules:
    - models_standard
  responsibility: "Standardize the definition and management of ActiveRecord associations"
</rule>
