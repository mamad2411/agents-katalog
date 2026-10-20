---
description: Enforces best practices for writing reversible and well-structured Rails migrations.
globs:
  - "db/migrate/*.rb"
---

# Migrations

<rule>
name: migrations_standard
description: Ensures Rails migrations are clear, reversible, and follow naming conventions and indexing best practices.

filters:
  - type: path
    pattern: "^db/migrate/.*\\.rb$"
    # Applies to migration files in the db/migrate directory

actions:
  - type: suggest
    message: |
      Migrations should:
      1. Use descriptive file and class names that reflect their purpose.
      2. Be reversible, either via a defined 'down' method or using reversible blocks.
      3. Include appropriate indexing where needed for performance.
      4. Follow Rails conventions for timestamps and versioning.
      5. Avoid embedding complex logic within migration files.

examples:
  - input: |
      # Bad example: Irreversible migration with inline SQL
      class AddDetailsToUsers < ActiveRecord::Migration[6.0]
        def change
          add_column :users, :details, :text
          execute "UPDATE users SET details = 'default'"
        end
      end
    output: "Migrations should be reversible; consider using reversible blocks for data transformations."
  - input: |
      # Good example
      class AddProfileDataToUsers < ActiveRecord::Migration[6.0]
        def change
          add_column :users, :bio, :text
          add_index :users, :bio
        end
      end
    output: "Migration uses descriptive naming, includes indexing, and remains reversible."

metadata:
  priority: high
  version: 1.0
  related_rules:
    - rails_project
  responsibility: "Standardize migration structure and ensure reversibility"
</rule>
